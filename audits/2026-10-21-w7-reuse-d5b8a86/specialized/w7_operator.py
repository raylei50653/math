#!/usr/bin/env python3
"""Compiled, matrix-free W7 operator in original frozen coordinates.

NumPy is required. SciPy is needed only for aslinearoperator().
Numerical discovery only; final certificates still use independent/check.py.
"""
from collections import defaultdict
import ctypes
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

import numpy as np
from numpy.ctypeslib import ndpointer

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
ROOT = AUDIT.parents[1]
TEMPLATES = AUDIT / 'templates'


def _i32(a):
    a = np.asarray(a)
    if a.size and (a.min() < 0 or a.max() >= 2**31):
        raise ValueError('index or coefficient outside nonnegative int32 range')
    return np.ascontiguousarray(a, dtype=np.int32).reshape(-1)


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def native():
    source = HERE / 'kernels.cpp'
    flags = ['-O3', '-std=c++17', '-march=native', '-shared', '-fPIC']
    compiler = subprocess.check_output(['g++', '--version'], text=True).splitlines()[0]
    key = hashlib.sha256((source.read_text()+compiler+str(flags)).encode()).hexdigest()[:20]
    build = HERE / 'build'
    build.mkdir(exist_ok=True)
    library = build / ('w7_'+key+'.so')
    if not library.exists():
        subprocess.run(['g++', *flags, str(source), '-o', str(library)], check=True)
    lib = ctypes.CDLL(str(library))
    I = ndpointer(dtype=np.int32, ndim=1, flags='C_CONTIGUOUS')
    F = ndpointer(dtype=np.float64, ndim=1, flags='C_CONTIGUOUS')
    lib.unit_sum.argtypes = [ctypes.c_int, I, I, F, F]
    lib.template_sum.argtypes = [ctypes.c_int, I, I, I, I, I, I, I,
                                ctypes.c_int, F, F, F, F]
    lib.project.argtypes = [ctypes.c_int, I, F, ctypes.c_int, I, I, I, F]
    lib.lift_adjoint.argtypes = [ctypes.c_int, I, F, ctypes.c_int, I, I, I, F]
    for name in ('unit_sum', 'template_sum', 'project', 'lift_adjoint'):
        getattr(lib, name).restype = None
    return lib, {'compiler': compiler, 'flags': flags, 'source_sha256': _sha(source)}


class W7Operator:
    """A=[D; Q_selected], default all ten positivity forms.

    backend='template' shares 333 local incidence shapes; 'direct' sums the
    unit-incidence matrix without storing floating-point coefficients.
    positive=() gives D alone; positive=(9,) selects the target row.
    workspace() returns private buffers for repeated calls through *_into.
    Separate workspaces make concurrent calls safe. Original X IDs never move.
    """
    def __init__(self, backend='template', positive=tuple(range(10)), reference='mindeg'):
        if backend not in ('template', 'direct'):
            raise ValueError('backend must be template or direct')
        self.backend = backend
        self.positive = tuple(positive)
        if len(set(self.positive)) != len(self.positive) or any(
                not isinstance(p, int) or isinstance(p, bool) or p not in range(10)
                for p in self.positive):
            raise ValueError('positive must contain unique row IDs in 0..9')
        base = json.loads((AUDIT / 'BASE.json').read_text())
        cache = ROOT/'audits/2026-10-20-w7-count-opt-d5b8a86/cache/model.npz'
        pin = next(p for p in base['inputs'] if p['path'] == str(cache.relative_to(ROOT)))
        if _sha(cache) != pin['sha256']:
            raise ValueError('frozen model cache SHA256 mismatch')
        d = np.load(cache)
        self.ns = len(d['live'])
        self.nh = len(d['hrow'])
        self.nx = len(d['cptr'])-1
        self.shape = (2*self.ns+len(self.positive), self.nx)
        self.dtype = np.dtype(np.float64)
        self.cptr, self.cidx = _i32(d['cptr']), _i32(d['cidx'])
        if reference == 'mindeg':
            deg = np.bincount(self.cidx, minlength=self.nh).reshape(-1, 3)
            self.ref = _i32(np.argmin(deg, axis=1))
        elif reference == 'h2':
            self.ref = np.full(self.ns, 2, dtype=np.int32)
        else:
            raise ValueError('reference must be mindeg or h2')
        self.reference = reference
        self.pp, self.pi, self.pv = [0], [], []
        for l in self.positive:
            states = np.flatnonzero(d['P'][l])
            self.pi.extend(states)
            self.pv.extend(d['P'][l, states])
            self.pp.append(len(self.pi))
        self.pp, self.pi, self.pv = map(_i32, (self.pp, self.pi, self.pv))
        self.capacity = 0
        if backend == 'direct':
            # CSR gather order for C; original CSC order for C^T.
            order = np.argsort(self.cidx, kind='stable')
            degree = np.bincount(self.cidx, minlength=self.nh)
            self.rptr = _i32(np.r_[0, np.cumsum(degree)])
            self.ridx = _i32(np.repeat(np.arange(self.nx), np.diff(self.cptr))[order])
        else:
            self._templates(d['hrow'])
            del self.cptr, self.cidx
        self.lib, self.build_info = native()
        d.close()

    def _templates(self, hrow):
        report = json.loads((TEMPLATES/'report.json').read_text())
        def read(name):
            path = TEMPLATES/name
            if _sha(path) != report['exports'][name]['sha256']:
                raise ValueError('frozen template export SHA256 mismatch: '+name)
            return json.loads(gzip.decompress(path.read_bytes()))
        cols = {int(k): v for k, v in read('templates.json.gz').items()}
        hk = {int(h): i for i, h in enumerate(hrow)}
        qr = defaultdict(dict)
        for h, state, q, k, phase, live in read('row_map.json.gz')['rows']:
            if live:
                qr[q][phase] = hk[h]
        qc = defaultdict(dict)
        for j, (q, k, col) in enumerate(read('column_map.json.gz')['original_column_order']):
            qc[q][col] = j
        groups = defaultdict(list)
        for q, rows in qr.items():
            k = sum(((q>>i)^(q>>((i+1)%13)))&1 for i in range(13))//2
            groups[k, tuple(sorted(rows))].append(q)
        meta, rp, ri, cp, ci, rm, cm = [], [], [], [], [], [], []
        for (k, phases), qs in sorted(groups.items()):
            qs.sort()
            local = {r: i for i, r in enumerate(phases)}
            allowed = [j for j, col in enumerate(cols[k]) if all(r in local for r in col)]
            if any(set(qc[q]) != set(allowed) for q in qs):
                raise ValueError('incomplete original-column map')
            nr, nc, ng = len(phases), len(allowed), len(qs)
            meta.extend([nr, nc, ng, len(rp), len(ri), len(cp), len(ci), len(rm), len(cm)])
            byrow = [[] for _ in phases]
            cptr = [0]
            for j, col in enumerate(allowed):
                for r in cols[k][col]:
                    ri_local = local[r]
                    ci.append(ri_local)
                    byrow[ri_local].append(j)
                cptr.append(cptr[-1]+len(cols[k][col]))
            cp.extend(cptr)
            rptr = [0]
            for js in byrow:
                ri.extend(js)
                rptr.append(rptr[-1]+len(js))
            rp.extend(rptr)
            rm.extend(qr[q][r] for r in phases for q in qs)
            cm.extend(qc[q][j] for j in allowed for q in qs)
            self.capacity = max(self.capacity, nr*ng, nc*ng)
        self.nb = len(meta)//9
        (self.meta, self.rptr, self.ridx, self.tcptr, self.tcidx,
         self.rows, self.cols) = map(_i32, (meta, rp, ri, cp, ci, rm, cm))
        # Every native scatter target occurs exactly once; no stale/overwritten outputs.
        if not np.array_equal(np.sort(self.rows), np.arange(self.nh)) or not np.array_equal(
                np.sort(self.cols), np.arange(self.nx)):
            raise ValueError('template maps do not cover original coordinates exactly once')

    def workspace(self):
        return tuple(np.empty(n, dtype=np.float64) for n in
                     (self.nh, self.capacity, self.capacity))

    def _vector(self, x, n):
        x = np.asarray(x)
        if np.iscomplexobj(x) or x.shape not in ((n,), (n, 1)):
            raise ValueError('expected a real vector of length '+str(n))
        return np.ascontiguousarray(x, dtype=np.float64).reshape(-1)

    def _buffers(self, x, out, nout, workspace):
        if not isinstance(out, np.ndarray) or out.shape != (nout,) or out.dtype != self.dtype or not out.flags.c_contiguous or not out.flags.writeable:
            raise ValueError('out must be a contiguous float64 vector of the output length')
        w = self.workspace() if workspace is None else workspace
        if len(w) != 3 or any(not isinstance(a, np.ndarray) or a.ndim != 1 or a.dtype != self.dtype
                or not a.flags.c_contiguous or not a.flags.writeable or len(a) < n for a, n in
                zip(w, (self.nh, self.capacity, self.capacity))):
            raise ValueError('invalid workspace')
        arrays = [x, out, *w]
        if any(np.shares_memory(a, b) for i, a in enumerate(arrays) for b in arrays[:i]):
            raise ValueError('input, output and workspace must not overlap')
        return w

    def _incidence(self, x, out, transpose, w):
        if self.backend == 'direct':
            self.lib.unit_sum(self.nx if transpose else self.nh,
                              self.cptr if transpose else self.rptr,
                              self.cidx if transpose else self.ridx, x, out)
        else:
            self.lib.template_sum(self.nb, self.meta, self.rptr, self.ridx,
                                  self.tcptr, self.tcidx, self.rows, self.cols,
                                  int(transpose), x, out, w[1], w[2])

    def matvec_into(self, x, out, workspace=None):
        x = self._vector(x, self.nx)
        w = self._buffers(x, out, self.shape[0], workspace)
        self._incidence(x, w[0], False, w)
        self.lib.project(self.ns, self.ref, w[0], len(self.positive), self.pp, self.pi, self.pv, out)
        return out

    def rmatvec_into(self, y, out, workspace=None):
        y = self._vector(y, self.shape[0])
        w = self._buffers(y, out, self.nx, workspace)
        self.lib.lift_adjoint(self.ns, self.ref, y, len(self.positive), self.pp, self.pi, self.pv, w[0])
        self._incidence(w[0], out, True, w)
        return out

    def matvec(self, x):
        return self.matvec_into(x, np.empty(self.shape[0]))

    def rmatvec(self, y):
        return self.rmatvec_into(y, np.empty(self.nx))

    def recover_z(self, x):
        """Original live-state order; this is a consistent Z only when D x=0."""
        x = self._vector(x, self.nx)
        w = self.workspace()
        self._incidence(x, w[0], False, w)
        return w[0][3*np.arange(self.ns)+self.ref]/2

    def aslinearoperator(self):
        from scipy.sparse.linalg import LinearOperator
        return LinearOperator(self.shape, matvec=self.matvec, rmatvec=self.rmatvec, dtype=self.dtype)

    @property
    def operator_storage_bytes(self):
        """Resident NumPy operator buffers; excludes Python/DSO overhead and workspace."""
        return sum(v.nbytes for v in vars(self).values() if isinstance(v, np.ndarray))
