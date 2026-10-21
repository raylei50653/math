#!/usr/bin/env python3
"""Read-only custody, complete model, and (when present) exact certificate replay."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

D = Path(__file__).resolve().parent
ROOT = D.parents[1]


def custody():
    base = json.loads((D/'BASE.json').read_text())
    if base['base'] != 'd5b8a8605bcbcef7aebbcf1934dad7ba255ccf02':
        raise RuntimeError('BASE mismatch')
    for rec in base['inputs']:
        raw = (ROOT/rec['path']).read_bytes()
        if len(raw) != rec['size']:
            raise RuntimeError(('input byte drift',rec['path']))
        if hashlib.sha256(raw).hexdigest() != rec['sha256']:
            raise RuntimeError(('input SHA drift',rec['path']))
    return len(base['inputs'])


def seal(path):
    records = json.loads(path.read_text())
    for rec in records:
        raw = (D/rec['path']).read_bytes()
        if len(raw) != rec['bytes'] or hashlib.sha256(raw).hexdigest() != rec['sha256']:
            raise RuntimeError(('output seal drift',rec['path']))
    return len(records)


def residual(model, independent):
    data = json.loads((D/'RESIDUAL.json').read_text())
    require = independent.require
    require(data['base'] == independent.BASE, 'residual BASE mismatch')
    require(data['all_state_count'] == len(model['states']), 'residual all states')
    require(data['initial_zero_states'] == model['caps']['initial_zero'], 'residual initial zeros')
    require(data['closure_zero_states'] == [i for r in model['orbit']['rounds'] for i in r], 'residual closure zeros')
    require(data['live_z_states'] == sorted(model['live']), 'residual live coordinates')
    require(data['x_column_ids'] == {'first':0,'last':307196,'ordering':'exact list order in orbits.json.gz columns'}, 'residual X coordinates')
    require(data['dimensions'] == {'equalities':183924,'z':61308,'x':307197,'equality_nonzeros':4448132}, 'residual dimensions')
    require(len(data['mandatory_strict_positivities']) == 10, 'residual positivity count')
    for rec, coefficients in zip(data['mandatory_strict_positivities'],model['positives']):
        if 'coefficient_path' in rec:
            vector = model['caps']
            for key in rec['coefficient_path']:
                vector = vector[key]
        else:
            vector = [0]*len(model['states'])
            for i,v in rec['sparse_coefficients']:
                vector[i] = v
        require(vector == coefficients, 'residual mandatory positivity mismatch')
    require(data['additional_112_type_conditions_included'] is False, 'residual 112-type scope')
    require(len(data['complete_inputs']) == 2, 'residual complete input count')
    for rec,name in zip(data['complete_inputs'],('caps.json.gz','orbits.json.gz')):
        expected_path = 'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/'+name
        require(rec['path'] == expected_path, 'residual complete input path')
        raw = (ROOT/rec['path']).read_bytes()
        require(len(raw) == rec['bytes'], 'residual input bytes')
        require(hashlib.sha256(raw).hexdigest() == rec['sha256'] == independent.SHA[name], 'residual input SHA')
        blob = hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(blob == rec['git_blob'], 'residual Git blob')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--certificate', type=Path)
    ap.add_argument('--controls', action='store_true')
    ap.add_argument('--orbits', action='store_true')
    ap.add_argument('--seal', type=Path)
    args = ap.parse_args()
    count = custody()
    output_seal = args.seal or (D/'OUTPUTS.json' if (D/'OUTPUTS.json').exists() else None)
    sealed = seal(output_seal) if output_seal else None
    spec = importlib.util.spec_from_file_location('independent',D/'independent/check.py')
    independent = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(independent)
    model = independent.load_model()
    residual(model,independent)
    result = {'input_custody':'PASS','frozen_files':count,
              'model':'PASS independent reconstruction',
              'complete_residual':'PASS exact coordinates and all ten positive quantities',
              'states':len(model['states']),'live_z':len(model['live']),
              'orbit_x':len(model['orbit']['columns']),
              'half_row_equalities':len(model['active_rows']),
              'all_ten_mandatory_positivities_present':True}
    command = [sys.executable,'-B',str(D/'sparse/replay_exact_residual.py'),
               str(D/'sparse/warm2-44459/exact-dual-residual.json.gz')]
    run = subprocess.run(command,capture_output=True,text=True)
    if run.returncode != 0:
        raise RuntimeError((run.stdout,run.stderr))
    result['incomplete_integer_residual'] = json.loads(run.stdout)
    certificate = args.certificate
    if certificate is None and (D/'certificate.json').exists():
        certificate = D/'certificate.json'
    if certificate is not None:
        data = json.loads(certificate.read_text())
        result['exact_certificate'] = independent.check_certificate(model,data)
        if args.controls:
            result['negative_controls'] = independent.negative_controls(model,data)
    else:
        result.update(necessary_cone='OPEN',exact_certificate=None,
                      source_excluded=False,source_realized=False)
        if args.controls:
            result['malformed_controls'] = independent.malformed_controls(model)
    if args.orbits:
        command = [sys.executable,'-B',str(ROOT/'audits/2026-10-20-r6-941-j1-five-edge-417732f/counting/orbits.py')]
        run = subprocess.run(command,capture_output=True,text=True)
        if run.returncode != 0:
            raise RuntimeError((run.stdout,run.stderr))
        result['complete_orbit_generation'] = json.loads(run.stdout.splitlines()[-1])
    custody()
    if output_seal:
        seal(output_seal)
        result['sealed_outputs'] = sealed
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
