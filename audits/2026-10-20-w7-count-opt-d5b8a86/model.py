#!/usr/bin/env python3
"""Shared loader for the frozen W7 cone (discovery only; never a verdict).

Coordinate maps kept by every derived model:
  state  s  -> canonical C13 id   live[s]
  half-row k -> encoded half-row  hrow[k], its state hstate[k]
  column j  -> frozen zero-based column index j (unchanged)
Each live state s has half-rows tri[s] = (h0,h1,h2) in increasing encoded order.
The X-only model replaces the three rows 2Z_s = S_h by S_h0-S_h2 = 0,
S_h1-S_h2 = 0 and recovers Z_s = S_h2/2 (any of the three sums).
"""
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SRC = ROOT / 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting'
SHA = {
    'caps.json.gz': '01547476f7afdc88ab224d640eaef363cfe765dd29e8983ca9df7aa63fdd68a3',
    'orbits.json.gz': '542ee11de93a846bfbc321b098214b153c5b600318ba2e0bc5621a73ad2a55ad',
}
CACHE = HERE / 'cache/model.npz'
POS_ROWS = (0, 2, 3, 5, 7, 8, 9)
TARGETS = (44459, 44466)
LABELS = ['G[01012]', 'G[01023]', 'G[01201]', 'G[01203]', 'G[01213]', 'G[01231]',
          'G[01232]', 'G[01232,h=a]', 'G[01232,h=b]', 'Z[44459]+Z[44466]']


def pinned(name):
    raw = (SRC / name).read_bytes()
    if hashlib.sha256(raw).hexdigest() != SHA[name]:
        raise RuntimeError('frozen input SHA256 mismatch: ' + name)
    return json.loads(gzip.decompress(raw))


def build():
    caps = pinned('caps.json.gz')
    orb = pinned('orbits.json.gz')
    live = np.array(orb['live'], dtype=np.int64)
    li = {int(s): i for i, s in enumerate(live)}
    per = {}
    for r, s in orb['rowids']:
        if s in li:
            per.setdefault(li[s], []).append(r)
    tri = np.array([sorted(per[i]) for i in range(len(live))], dtype=np.int64)
    assert tri.shape == (len(live), 3)
    hrow = tri.reshape(-1)                      # half-row k = 3*s + position
    hstate = np.repeat(np.arange(len(live)), 3)
    hk = {int(r): k for k, r in enumerate(hrow)}
    cols = orb['columns']
    cptr = np.zeros(len(cols) + 1, dtype=np.int64)
    cptr[1:] = np.cumsum([len(c) for c in cols])
    cidx = np.fromiter((hk[r] for c in cols for r in c), dtype=np.int64, count=int(cptr[-1]))
    P = [[caps['matrices']['G'][j][int(s)] for s in live] for j in POS_ROWS]
    P += [[p[int(s)] for s in live] for p in caps['sectors']]
    P.append([int(int(s) in TARGETS) for s in live])
    P = np.array(P, dtype=np.int64)
    CACHE.parent.mkdir(exist_ok=True)
    np.savez_compressed(CACHE, live=live, tri=tri, hrow=hrow, hstate=hstate,
                        cptr=cptr, cidx=cidx, P=P)


class Model:
    def __init__(self):
        if not CACHE.exists():
            build()
        d = np.load(CACHE)
        for k in d.files:
            setattr(self, k, d[k])
        self.ns = len(self.live)
        self.nh = len(self.hrow)
        self.nx = len(self.cptr) - 1
        self.state_of = {int(s): i for i, s in enumerate(self.live)}

    def incidence(self):
        """Half-row x column 0/1 matrix C (scipy csc), C[k,j]=1 iff hrow k in column j."""
        from scipy.sparse import csc_matrix
        return csc_matrix((np.ones(len(self.cidx)), self.cidx, self.cptr),
                          shape=(self.nh, self.nx))

    def reference(self, mode='mindeg'):
        """Reference position per state: 'h2' (old sparse/), or the min-degree half-row."""
        if mode == 'h2':
            return np.full(self.ns, 2)
        deg = np.bincount(self.cidx, minlength=self.nh).reshape(-1, 3)
        return np.argmin(deg, axis=1)

    def difference(self, ref=None):
        """Row 2s+a: S_{other_a(s)} - S_{ref(s)}, a=0,1 (exact integer entries).

        other_0 < other_1 are the two non-reference positions of state s."""
        from scipy.sparse import csr_matrix
        ref = self.reference('h2') if ref is None else ref
        pos = self.cidx % 3
        st = self.cidx // 3
        col = np.repeat(np.arange(self.nx), np.diff(self.cptr))
        isref = pos == ref[st]
        slot = pos - (pos > ref[st])             # 0/1 among the non-reference positions
        rr = np.r_[(2 * st + slot)[~isref], 2 * st[isref], 2 * st[isref] + 1]
        cc = np.r_[col[~isref], col[isref], col[isref]]
        vv = np.r_[np.ones(int((~isref).sum())), -np.ones(2 * int(isref.sum()))]
        D = csr_matrix((vv, (rr, cc)), shape=(2 * self.ns, self.nx))
        D.sum_duplicates()
        D.eliminate_zeros()
        return D

    def zmap(self, ref=None):
        """ns x nx matrix R with R X = 2Z (row s = S_{ref(s)})."""
        ref = self.reference('h2') if ref is None else ref
        C = self.incidence().tocsr()
        return C[3 * np.arange(self.ns) + ref]

    def positivity_rows(self, ref=None):
        """10 x nx rows: 2 * P_l Z expressed in X through the references."""
        R = self.zmap(ref)
        return np.asarray((R.T @ self.P.T).T)    # 10 x nx


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
