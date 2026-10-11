#!/usr/bin/env python3
"""Exclusive metadata generation and bounded read-only audit; no source enumeration."""
import argparse
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent.parent
DISPATCH = REPO / 'audits/2026-10-11-n45-s-long-s-rfibre-dispatch'
BASE = 'f2692089ad4259808e27d9b7e882ac09505b180a'
TASK = 'N45-S-LONG-S-T2-Q0-RESTORE'
PENDING = '待獨立驗收'
COL = set(range(4))
LITERALS = ['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']
Q_ROWS = {0:'01212',1:'01202',2:'01201',3:'01021',4:'01012'}
ASSIGNED = [(933,[0,2,3,4]),(941,[0,2,3]),(941,[0,2,4])]
COORDS = {'original_e':['r','b4'],'original_r':'r','X_definition':'G minus exactly rb4',
          'root_order':['r','s'],'r_retained_spokes':[], 'original_s_spokes':[0,2]}

def read(path):
    return json.loads(path.read_text())

def dump_new(path, value):
    with path.open('x') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)+'\n')

def digest(path):
    data = path.read_bytes()
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def colour_map(values, perm):
    return [perm[v] for v in values]

def calibration():
    p01, p12 = [1,0,2,3], [0,2,1,3]
    cases=[]
    for pair in itertools.combinations([0,1,2],2):
        ds=set(pair); dl=COL-ds
        q1_dl=set(colour_map(dl,p01))
        q1_allowed=COL-(ds|q1_dl)
        q2_ds=set(colour_map(ds,p12))
        cases.append({'beta_D_S':sorted(ds),'beta_D_L':sorted(dl),
            'q1_D_L':sorted(q1_dl),'q1_allowed_r':sorted(q1_allowed),
            'excluded_by_original_q1_acceptance':not q1_allowed,
            'q2_D_S':sorted(q2_ds),
            'q2_r1_fibre_empty_in_surviving_case':1 in q2_ds if q1_allowed else None})
    transports=[]
    for piece, support, target, perm in [('L',[2,3,4],'01202',p01),('S',[4,0],'01201',p12)]:
        beta_values=[int(Q_ROWS[0][i]) for i in support]
        target_values=[int(target[i]) for i in support]
        transports.append({'piece':piece,'ordered_actual_support':support,
            'beta_values':beta_values,'target_literal':target,'target_values':target_values,
            'whole_piece_colour_permutation':perm,'mapped_beta_values':colour_map(beta_values,perm),
            'all_16_ordered_pin_maps':[{'beta_pin':[a,b],'target_pin':[perm[a],perm[b]]}
                                     for a,b in itertools.product(range(4),repeat=2)],
            'fibre_semantics':'full actual-piece assignment bijection, all preimages and empties; no source values supplied'})
    return {'status':PENDING,'scope':'bounded forbidden-column arithmetic and literal transport metadata only',
        'control_status':'triggered and holds','source_graphs_enumerated':0,
        'cases':cases,'support_transports':transports,'target_source_executed':False,
        'target_source_trigger_count':None}

def input_metadata():
    pins=read(DISPATCH/'input-pins.json')
    groups={'BASE_blobs':[],'sealed_audit_SHA256':[]}
    for record in pins['inputs']:
        item=copy.deepcopy(record)
        item['dispatch_frozen_path']=str((DISPATCH/record['frozen_path']).relative_to(REPO))
        key='BASE_blobs' if record['authority']=='BASE Git blob' else 'sealed_audit_SHA256'
        groups[key].append(item)
    return {'task_id':TASK,'status':PENDING,'base':BASE,**groups,
        'dispatch_metadata_SHA256':[{ 'path':str(p.relative_to(REPO)),**digest(p)}
             for p in [DISPATCH/'input-pins.json',DISPATCH/'delivery.json',DISPATCH/'TASK_B_T2_Q0.md']],
        'external_theorem_pins':[{'name':'Dvořák degree-list Lemma 7 / Theorem 10, Gallai block palettes',
            'declared_url':'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
            'sha256':'50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea',
            'bytes':164927,'git_blob':None,'authority':'inherited external theorem pin from sealed accepted review',
            'role':'upstream dependency of accepted BASE/old B lemmas; no fresh theorem claim',
            'origin_refetched':False,'direct_external_theorem_revalidation_executed':False}],
        'missing_BASE_blobs':read(ROOT/'findings.json')['findings'],
        'historical_authority_policy':'Original B pending fields unchanged; adoption via sealed review/corrections only',
        'accepted_corrections':{'query_partition':[12,4,10,4],
            'SF_RESIDUAL_added_dependency':'SF-T2-Q0-Q1-RESTORED'},
        'input_copy_policy':'read dispatch authority in place; SHA256 compared before/after; no physical/quarantine substitution'}

def claims_metadata():
    rows=[
        ('T2Q0-S3','For every assigned-contract source and eta in {beta,q1,q2}, every full X(eta) lift',
         ['actual U012','F_U(beta)={1}','original s-spokes b0,b2'],
         's=3; complete U preimage avoiding 3 is nonempty; U fibres coincide across these rows',
         'exact full-assignment restriction and emptiness statement',['sealed review SF-T2-ROLE','K6/K8/K9/K10'],2),
        ('T2Q0-BETA-PARTITION','For every assigned-contract source, at the original beta / s=3 pin',
         ['X own beta rejection/minimality','original r-split22','no retained r-spoke','short S N-diagonal'],
         'D_L(beta;3) disjoint-union D_S(beta;3)=Col, both size 2, and 3 not in D_S(beta;3)',
         'same-source necessary full forbidden-column statement',['BASE long-contract section 5','sealed original B REPORT section 4','T2Q0-S3'],2),
        ('T2Q0-L-Q1-TRANSPORT','For every original full L assignment and every ordered (a,b) pin',
         ['actual L support234','beta=01212','q1=01202','same original L edges/contacts/attachments'],
         'pi01 maps Lambda_L(beta;a,b) bijectively to Lambda_L(q1;pi01(a),pi01(b)); at b=3 the forbidden r column maps by pi01',
         'complete local assignment / tuple / preimage / empty fibre bijection',['K9/K10','literal support identity 212 -> 202'],2),
        ('T2Q0-S2-FORCED','For every source satisfying all assigned premises',
         ['q1 not in original Q(G)','K2 exact original signature','q1 S40 and U012 unchanged'],
         '2 is in D_S(beta;3), so Lambda_S(beta;2,3) is empty',
         'new necessary full pinned-fibre emptiness theorem',['T2Q0-S3','T2Q0-BETA-PARTITION','T2Q0-L-Q1-TRANSPORT'],2),
        ('T2Q0-S-Q2-TRANSPORT','For every original full S assignment and every ordered (a,b) pin',
         ['actual S support40','q2=01201','same original S edges/contacts/attachments'],
         'pi12 maps Lambda_S(beta;a,b) bijectively to Lambda_S(q2;pi12(a),pi12(b)); beta(2,3) maps to q2(1,3)',
         'complete local assignment / tuple / preimage / empty fibre bijection',['K9/K10','literal support identity 20 -> 10'],1),
        ('T2Q0-Q2-EMPTY1','For every assigned-contract source and every b in Col',
         ['full X restrictions onto the actual S and U','original retained s-spokes'],
         'L_X(q2;1,b) is empty; all q2 lifts have s=3',
         'new whole-source all-pin emptiness theorem',['T2Q0-S2-FORCED','T2Q0-S-Q2-TRANSPORT','T2Q0-S3','sealed review SF-JOIN'],1),
        ('T2Q0-Q2-RESTORE','For every assigned-contract source, there exists a complete q2 X lift; every such lift',
         ['accepted Q(X)={beta}','q2(b4)=1','restore exactly original rb4'],
         'has r != 1 and is a complete G(q2) lift; the full q2 X and G lift sets coincide',
         'new arbitrary-size full-lift original-edge restoration theorem',['T2Q0-Q2-EMPTY1','sealed review accepted SF-QX','sealed review SF-T2-EXTEND and inherited E2 chain','sealed review SF-RESTORE'],1),
        ('T2Q0-COVER3','For each of the three assigned schedules and every source satisfying all K1-K12 premises',
         ['Q(G)=933/0234 or 941/023 or 941/024','q2 in the entire same-frame Delta'],
         'there is a complete restored q2 lift, contradicting original G rejection; no source in the three schedules',
         'arbitrary-size source-exclusion paper candidate',['T2Q0-Q2-RESTORE','K2 exact original rejection sets'],1),
        ('T2Q0-CALIBRATION','For every one of the fixed three abstract column cases and two literal support transports',
         ['control-plan.json fixed finite inputs/limits','no actual source supplied'],
         'column arithmetic and all sixteen pin maps match proof-calibration.json; assigned coverage has ten rows x sixteen pins per schedule',
         'finite metadata / algebra calibration only',['control-plan.json','proof-calibration.json'],1),
    ]
    claims=[]
    for ident, quantifier, premises, conclusion, kind, deps, colour in rows:
        claims.append({'id':ident,'status':PENDING,'quantifier':quantifier,
            'premises':['K1-K12 frozen long-contract section 1','assigned common domain in REPORT section 1']+premises,
            'conclusion':conclusion,'conclusion_type':kind,'dependencies':deps,
            'original_coordinates':{**COORDS,
                'literal_b4_colours':{'01212':2,'01202':2,'01201':1},
                'new_restoration_literal':'01201','new_restoration_b4_colour':1},
            'proof_location':'REPORT.md sections 2-4' if ident!='T2Q0-CALIBRATION' else 'audit.py calibration/check',
            'new_sufficient_premises_added':False,
            'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'}})
    return {'task_id':TASK,'status':PENDING,'base':BASE,'claims':claims,
        'adoption':'pending external independent acceptance; internal checks do not adopt',
        'SF_QX_trust_boundary':'Accepted review SF-QX retains SF-T2-EXTEND/BASE E2 paper and inherited finite-terminal dependencies; not replayed here',
        'q1_role':'K2 original accepted row used only as auxiliary existence; no Delta restoration counted',
        'scope_expansion':False}

def coverage_metadata():
    raw=read(DISPATCH/'authority/sealed/audits/2026-10-11-n45-s-long-s-fibre/obligations.json')
    schedules=[]
    for orbit,qg in ASSIGNED:
        found=[s for s in raw['schedules'] if s['t_s']==2 and s['beta_q']==0 and s['SigmaG_orbit']==orbit and s['QG']==qg]
        assert len(found)==1
        old=found[0]
        rows=copy.deepcopy(old['all_ten_literal_obligations'])
        assert len(rows)==10
        for row in rows:
            literal=''.join(map(str,row['literal']))
            q=next((j for j,v in Q_ROWS.items() if v==literal),None)
            row['current_paper_analysis']={'literal_b4_colour':int(literal[4]),
                'restoration_condition':'a != literal(b4)',
                'G_rejection_necessary_empty_r_values':[a for a in range(4) if a!=int(literal[4])] if q in qg else [],
                'concrete_relations_and_preimages_supplied':False}
            for pin in row['pins']:
                a,b=pin['r'],pin['s']
                reasons=[]
                if literal==Q_ROWS[0]: reasons.append('accepted original beta rejection: all X pins empty')
                if b in {int(literal[0]),int(literal[2])}: reasons.append('retained original s-spoke constraint')
                if literal in [Q_ROWS[0],Q_ROWS[1],Q_ROWS[2]] and b==1: reasons.append('actual U012 F_U={1}')
                if literal==Q_ROWS[2] and a==1 and b==3: reasons.append('T2Q0-Q2-EMPTY1 via complete S pi12 bijection')
                pin['new_paper_necessary_empty_reasons']=reasons
                pin['concrete_fibre_values_supplied']=False
                pin['new_q2_restoration_pool_member']=(literal==Q_ROWS[2] and b==3 and a!=1)
        extra=[]
        for q in qg:
            if q not in [0,2]:
                extra.append({'q':q,'literal':Q_ROWS[q],
                    'exact_fibres':[{'r':a,'s':b} for a,b in itertools.product(range(4),repeat=2) if a!=int(Q_ROWS[q][4])],
                    'status':'individual restoration not proved in this delivery',
                    'required_by_original_G_rejection':'empty in any purported source',
                    'schedule_status':'already paper-excluded by q2; these separate row restorations are not required'})
        schedules.append({'id':f'B-{orbit}-'+''.join(map(str,qg)),
            'SigmaG_orbit':orbit,'QG':qg,'beta_q':0,'beta_literal':Q_ROWS[0],
            'Delta':[{'q':q,'literal':Q_ROWS[q],'original_rejection_requires_all_X_lifts_r':int(Q_ROWS[q][4])}
                     for q in qg if q!=0],
            'original_s_spoke_variants':[[0,2]],'original_coordinates':COORDS,
            'proved_restoration_rows':[{'q':2,'literal':Q_ROWS[2],'all_nonempty_X_lifts':'s=3 and r != 1',
                'collectively_nonempty_fibres':[{'r':a,'s':3} for a in [0,2,3]],
                'individual_nonempty_fibre':'not specified; no actual source supplied',
                'claims':['T2Q0-Q2-EMPTY1','T2Q0-Q2-RESTORE']}],
            'proved_source_minor':None,'schedule_result':'arbitrary-size paper exclusion candidate',
            'status':PENDING,'unresolved_assigned_schedule_residual':None,
            'individual_restoration_not_proved':extra,
            'all_ten_literal_obligations':rows,
            'historical_obligation_record_fields':{k:v for k,v in old.items() if k!='all_ten_literal_obligations'},
            'historical_record_policy':'verbatim fields are provenance only; new theorem and coverage stated separately'})
    return {'task_id':TASK,'status':PENDING,'base':BASE,'schedules':schedules,
        'assigned_schedule_count':3,'assigned_schedule_spoke_combinations':3,
        'distinct_s_spoke_variants':[[0,2]],'paper_covered_schedule_count':3,
        'actual_source_count':None,'concrete_relations_supplied':False,'full_lift_counts_supplied':False,
        'same_source_obligations':{'pieces':['U','L','S'],'actual_C':['r','L','S'],
            'actual_supports':{'U':[0,1,2],'L':[2,3,4],'S':[4,0]},
            'ordered_shared_contacts':'retain actual vertices and original order; no independent shared coordinate',
            'assignments_tuples_preimages':'all original piece assignments and all tuple preimages, no values invented',
            'isolated_factor':'all Col^I assignments retained',
            'X_edge_witnesses':'each retained nonboundary edge, same beta, X-f exact full witness',
            'G_edge_witnesses':'each original nonboundary edge, its own allowed gamma_f, G-f exact full witness'},
        'paper':'all three schedules closed as candidate, pending independent acceptance',
        'finite_calibration':{'executed':True,'status':'triggered and holds','scope':'three column cases and coverage metadata only'},
        'old_19_source_controls_reexecuted':False,'new_source_graph_search_executed':False,
        'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'},
        'source_realizability':'not established','Lean':{'executed':False,'new_theorem':False},
        'general_N45_N2_E':'not established','residual_outside_assignment':'other 21 necessary schedules unchanged by this delivery'}

def build():
    dump_new(ROOT/'control-plan.json',{'task_id':TASK,'status':PENDING,
        'fixed_inputs':{'beta':Q_ROWS[0],'q1':Q_ROWS[1],'q2':Q_ROWS[2],
            'D_S_cases':[[0,1],[0,2],[1,2]],'pi01':[1,0,2,3],'pi12':[0,2,1,3],
            'ordered_supports':{'L':[2,3,4],'S':[4,0]},'assigned':ASSIGNED},
        'upper_bounds':{'column_cases':3,'literal_support_transports':2,
            'pin_maps_per_transport':16,'coverage_schedules':3,'literal_rows_per_schedule':10,
            'ordered_pins_per_row':16,'new_source_graphs':0},
        'ordinary_and_seed17_read_only':True,
        'negative_controls':['corrupt q2_D_S to omit the proved r1 blocker','delete a diagonal coverage pin'],
        'missing_BASE_blob_dependent_replays_executed':False,'old_19_controls_reexecuted':False})
    dump_new(ROOT/'inputs.json',input_metadata())
    dump_new(ROOT/'claims.json',claims_metadata())
    dump_new(ROOT/'coverage.json',coverage_metadata())
    cert=calibration()
    dump_new(ROOT/'proof-calibration.json',cert)
    wrong=copy.deepcopy(cert)
    wrong['cases'][1]['q2_D_S']=[0,2]
    dump_new(ROOT/'negative-controls/bad-q2-column.json',wrong)
    wrong=copy.deepcopy(coverage_metadata())
    pins=wrong['schedules'][0]['all_ten_literal_obligations'][0]['pins']
    pins[:]=[p for p in pins if (p['r'],p['s'])!=(3,3)]
    dump_new(ROOT/'negative-controls/missing-diagonal.json',wrong)
    print(json.dumps({'status':'metadata generated','acceptance':PENDING,'new_source_graphs':0},ensure_ascii=False,sort_keys=True))

def verify_inputs():
    data=read(ROOT/'inputs.json')
    assert data==input_metadata(), 'input metadata mismatch'
    for record in data['BASE_blobs']:
        data_bytes=subprocess.check_output(['git','show',BASE+':'+record['path']],cwd=REPO)
        blob=subprocess.check_output(['git','rev-parse',BASE+':'+record['path']],cwd=REPO).decode().strip()
        assert blob==record['git_blob']
        assert hashlib.sha256(data_bytes).hexdigest()==record['sha256']
        assert len(data_bytes)==record['bytes']
    for record in data['BASE_blobs']+data['sealed_audit_SHA256']:
        for path in [REPO/record['path'],REPO/record['dispatch_frozen_path']]:
            assert digest(path)=={'bytes':record['bytes'],'sha256':record['sha256']}
    for record in data['sealed_audit_SHA256']:
        assert record['git_blob'] is None and not record['included_in_BASE_claimed']

def check(cert_path,coverage_path):
    verify_inputs()
    cert=read(cert_path); expected=calibration()
    assert cert==expected, 'calibration certificate mismatch'
    plan=read(ROOT/'control-plan.json')
    assert plan['upper_bounds']['column_cases']==len(cert['cases'])==3
    assert len(cert['support_transports'])==2
    for tr in cert['support_transports']:
        assert tr['mapped_beta_values']==tr['target_values'], 'literal support mismatch'
        assert tr['whole_piece_colour_permutation'][3]==3
        assert len(tr['all_16_ordered_pin_maps'])==16
    survivors=[c for c in cert['cases'] if not c['excluded_by_original_q1_acceptance']]
    assert len(survivors)==2
    assert all(2 in c['beta_D_S'] and c['q2_r1_fibre_empty_in_surviving_case'] for c in survivors)
    coverage=read(coverage_path)
    assert coverage==coverage_metadata(), 'coverage mismatch (all diagonal/empty pin positions required)'
    assert read(ROOT/'claims.json')==claims_metadata(), 'claims metadata mismatch'
    count=0
    for s in coverage['schedules']:
        assert 2 in s['QG'] and 1 not in s['QG']
        assert s['original_s_spoke_variants']==[[0,2]]
        for literal,row in zip(LITERALS,s['all_ten_literal_obligations'],strict=True):
            assert literal==''.join(map(str,row['literal']))
            pins=row['pins']
            assert {(p['r'],p['s']) for p in pins}==set(itertools.product(range(4),repeat=2))
            assert len(pins)==16
            assert row['gamma_b4']==int(literal[4])
            count+=len(pins)
    assert count==480
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO).decode().strip()==BASE
    before=read(ROOT/'custody-before.json')
    for path,old in before['files'].items():
        assert digest(REPO/path)==old, 'input/old-certificate drift: '+path
    print(json.dumps({'acceptance':PENDING,'status':'triggered and holds',
        'scope':'bounded metadata/algebra calibration only','column_cases':3,'support_transports':2,
        'coverage_pin_positions':480,'source_graphs_enumerated':0,
        'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'}},ensure_ascii=False,sort_keys=True))

def native_run(label,args,seed17=False):
    env=os.environ.copy()
    if seed17: env['PYTHONHASHSEED']='17'
    p=subprocess.run(args,cwd=REPO,env=env,capture_output=True)
    (ROOT/'logs'/f'{label}.stdout').open('xb').write(p.stdout)
    (ROOT/'logs'/f'{label}.stderr').open('xb').write(p.stderr)
    dump_new(ROOT/'logs'/f'{label}.command.json',{'argv':args,'cwd':str(REPO),
        'environment_override':{'PYTHONHASHSEED':'17'} if seed17 else {},'exit':p.returncode,
        'capture':'native subprocess separate stdout/stderr'})
    return p

def run_checks():
    args=['python3','-B',str(ROOT/'audit.py'),'check']
    normal=native_run('normal',args)
    seed=native_run('seed17',args,seed17=True)
    bad=native_run('negative-q2-column',args+['--certificate',str(ROOT/'negative-controls/bad-q2-column.json')])
    diagonal=native_run('negative-missing-diagonal',args+['--coverage',str(ROOT/'negative-controls/missing-diagonal.json')])
    assert normal.returncode==seed.returncode==0
    assert normal.stdout==seed.stdout and normal.stderr==seed.stderr
    assert bad.returncode!=0 and b'calibration certificate mismatch' in bad.stderr
    assert diagonal.returncode!=0 and b'coverage mismatch' in diagonal.stderr
    result={'task_id':TASK,'acceptance':PENDING,'scope':'bounded metadata/algebra only',
        'ordinary':{'exit':normal.returncode,'status':'triggered and holds'},
        'seed17':{'exit':seed.returncode,'status':'triggered and holds'},
        'normal_seed17_stdout_stderr_equal':True,
        'negative_controls':[{'id':'bad-q2-column','exit':bad.returncode,'status':'triggered and holds','expected':'rejected'},
            {'id':'missing-diagonal','exit':diagonal.returncode,'status':'triggered and holds','expected':'rejected'}],
        'failed_source_certificates':[],'all_native_logs_retained':True,
        'old_19_controls_reexecuted':False,'missing_BASE_blob_replays_executed':False,
        'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'}}
    dump_new(ROOT/'checks.json',result)
    print(json.dumps(result,ensure_ascii=False,sort_keys=True))

def finish():
    before=read(ROOT/'custody-before.json')
    after={p:digest(REPO/p) for p in before['files']}
    assert after==before['files']
    head=native_run('head-after',['git','rev-parse','HEAD'])
    diff=native_run('tracked-diff-after',['git','diff','--binary','HEAD'])
    initial_head=(ROOT/'logs/head-before.stdout').read_bytes()
    initial_diff=(ROOT/'logs/tracked-diff-before.stdout').read_bytes()
    assert head.returncode==diff.returncode==0
    assert head.stdout==initial_head and diff.stdout==initial_diff
    preflight=native_run('dispatch-final',['python3','-B',str(DISPATCH/'check_dispatch.py'),'--check'])
    assert preflight.returncode==0
    dump_new(ROOT/'custody-after.json',{'base':BASE,'files':after,'same_as_before':True,
        'zero_input_old_certificate_drift':True,'HEAD_and_tracked_diff_unchanged':True,
        'scope':'all 60 recorded authority/live input/old-certificate files plus HEAD/tracked diff'})
    dump_new(ROOT/'internal-paper-checks.json',{'task_id':TASK,'status':PENDING,
        'role':'three task-internal read-only proof checks; does not constitute independent adoption',
        'checks':[{'id':'q2_restore_paper','finding':'full q2 proof valid; q1 may use K2 directly'},
            {'id':'q3q4_geometry','finding':'full assignment transports and all three q2 schedule coverage valid'},
            {'id':'independent_proof_check','finding':'no extra premise or shared/pin coordinate gap found'}],
        'agent_writes':False,'other_batch_worker_conclusions_used':False})
    payload=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='delivery.json':
            payload.append({'path':str(p.relative_to(ROOT)),**digest(p)})
    dump_new(ROOT/'delivery.json',{'task_id':TASK,'status':PENDING,'base':BASE,
        'result':'three assigned schedules covered by full q2 rb4 restoration paper candidate',
        'adopted':False,'payload':payload,'payload_files':len(payload),
        'payload_bytes':sum(p['bytes'] for p in payload),'metadata_exclusions':['delivery.json'],
        'finite_source_executed':False,'finite_source_trigger_count':None,
        'claims_scope':'exactly three assigned t_s2 beta_q0 schedules; no general N45/N2/E or Lean',
        'shared_original_other_worker_files_modified':False,
        'commit_push_PR_external_messages':False,'new_source_graph_search':False})
    print(json.dumps({'status':'delivery sealed','acceptance':PENDING,'payload_files':len(payload),
                      'input_old_certificate_drift':0},ensure_ascii=False,sort_keys=True))

def verify_delivery():
    d=read(ROOT/'delivery.json')
    paths={p['path'] for p in d['payload']}
    live={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p.name!='delivery.json'}
    assert live==paths
    assert len(paths)==d['payload_files']
    assert sum(p['bytes'] for p in d['payload'])==d['payload_bytes']
    for record in d['payload']:
        assert digest(ROOT/record['path'])=={'bytes':record['bytes'],'sha256':record['sha256']}
    assert d['status']==PENDING and not d['adopted']
    print(json.dumps({'status':'sealed payload verified','acceptance':PENDING,
        'payload_files':d['payload_files'],'delivery_sha256':digest(ROOT/'delivery.json')['sha256']},ensure_ascii=False,sort_keys=True))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode',choices=['build','check','run-checks','finish','verify-delivery'])
    p.add_argument('--certificate',type=Path,default=ROOT/'proof-calibration.json')
    p.add_argument('--coverage',type=Path,default=ROOT/'coverage.json')
    args=p.parse_args()
    if args.mode=='build': build()
    elif args.mode=='check': check(args.certificate,args.coverage)
    elif args.mode=='run-checks': run_checks()
    elif args.mode=='finish': finish()
    else: verify_delivery()

if __name__=='__main__':
    main()
