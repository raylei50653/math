"""Exclusive paper/coverage metadata, derived from pinned adopted schedules."""
import json
from itertools import product
from pathlib import Path

HERE=Path(__file__).resolve().parent
REVIEW=HERE/'authority/sealed/audits/2026-10-11-n45-s-long-s-review'
LITERALS=['01012','01021','01023','01201','01202','01203','01212','01213','01231','01232']
Q=['01212','01202','01201','01021','01012']

def write(name,data):
    with (HERE/name).open('x') as f:
        json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True); f.write('\n')

def main():
    domain=json.loads((REVIEW/'remaining-schedules.json').read_text())
    remaining=domain['remaining_schedules']
    assert len(remaining)==24
    assert sum(len(x['s_spoke_domain']) for x in remaining)==38
    cert=json.loads((HERE/'certificate.json').read_text())
    summary=json.loads((HERE/'logs/check-normal.stdout').read_text())
    assigned=[]
    for schedule in remaining:
        sid=f"T{schedule['t_s']}-S{schedule['SigmaG_orbit']}-Q{''.join(map(str,schedule['QG']))}-B{schedule['beta_q']}"
        entry={**schedule,'schedule_id':sid,'assigned_role':'auxiliary transfer for every schedule; no source exclusion task',
            'new_proved_restoration_rows':[],'new_source_minors':[],
            'concrete_source_relations':None,'concrete_source_preimage_counts':None,
            'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'},
            'variants':[]}
        for spokes in schedule['s_spoke_domain']:
            rows=[]
            for literal in LITERALS:
                q=Q.index(literal) if literal in Q else None
                is_beta=q==schedule['beta_q'] if q is not None else False
                is_delta=q in schedule['Delta'] if q is not None else False
                cells=[]
                for a,b in product(range(4),repeat=2):
                    spoke_ok=all(b!=int(literal[h]) for h in spokes)
                    status=('necessarily empty by actual s-spoke' if not spoke_ok else
                            'necessarily empty at beta' if is_beta else
                            'necessarily empty if complete source on Delta, original rb4 restores' if is_delta and a!=int(literal[4]) else
                            'source-specific full preimages not supplied')
                    cells.append({'r':a,'s':b,'s_spoke_factor':spoke_ok,
                        'rb4_restorable':a!=int(literal[4]),'full_X_fibre_obligation':status,
                        'C_interface':'all full assignments and empty cells defined by TF-BLOCK/C-PIN; target values not supplied',
                        'actual_U_fibre':'not supplied', 'concrete_full_X_preimages':None,
                        'G_fibre_obligation':'necessarily empty by original rb4' if a==int(literal[4]) else status})
                rows.append({'literal':literal,'q':q,'is_beta':is_beta,'is_Delta':is_delta,
                    'gamma_b4':int(literal[4]),'full_X_row_obligation':'reject' if is_beta else 'accept by adopted SF-QX',
                    'full_G_row_obligation':'reject' if is_beta or is_delta else 'accept by source complete Sigma',
                    'pins':cells,
                    'OPEN_fibres':{'r_colours':[a for a in range(4) if a!=int(literal[4])],
                        's_condition':'b avoids all literal s-spokes and actual Lambda_U(gamma;b) is nonempty',
                        'C_ambient_condition':'tau belongs to (Col-{b})^2; full Phi_C(gamma;tau,a) must be nonempty to contradict true-source required emptiness',
                        'actual_values_supplied':False} if is_delta else None})
            entry['variants'].append({'original_s_spokes':spokes,'ten_rows':rows})
        assigned.append(entry)
    coverage={
        'task_id':'N45-S-LONG-S-BLOCK-TRANSFER','status':'待獨立驗收','base':domain['base'],
        'coordinate_contract':{'U_owner':'s','U_support':'012','L_support':'234','S_support':'40',
            'original_e':['r','b4'],'original_r':'r','original_r_split':[2,2],
            'retained_r_spokes':[],'whole_source_normalization_count':1},
        'paper':{'recurrence':'arbitrary finite actual block-tree, full restriction/union bijection',
            'K11_K12_required_for_recurrence':False,'source_exclusion_by_this_task':False},
        'finite_calibration':{'executed':True,'status':'triggered and holds',
            'declared_cases':5,'valid_cases':4,'failed_declared_cases':cert['failed_cases'],
            'upper_bound_cases':8,'upper_bound_C_vertices':11,'actual_max_C_vertices':7,
            'rows':summary['rows'],'assignments':summary['assignments'],
            'ambient_cells':summary['ambient_cells'],'empty_ambient_cells':summary['empty_ambient_cells'],
            'ordered_pins':summary['ordered_pins'],'spoke_filtered_pin_cells':summary['spoke_filtered_pin_cells'],
            'same_C_across_rows':True,'source_lifts_computed':False,'disk_topology_verified':False,
            'K11_K12':'not supplied; target source not triggered'},
        'controls':[
            {'id':'recurrence-versus-independent-original-edges','status':'triggered and holds','executed':True},
            {'id':'normal-seed17-replay','status':'triggered and holds','executed':True},
            {'id':'negative-r-colour','status':'triggered and holds','meaning':'expected rejection of changed full preimage r coordinate'},
            {'id':'negative-empty-cell','status':'triggered and holds','meaning':'expected rejection of missing empty ambient cell'},
            {'id':'negative-original-branch','status':'triggered and holds','meaning':'expected rejection of missing original l2 vertex'},
            {'id':'BRIDGE_BAD6-degree4-premise','status':'counterexample','scope':'predeclared interface degree check only; not K1-K12 source'},
            {'id':'whole-X-G-target','status':'not triggered','executed':False,'trigger_count':None},
            {'id':'nonempty-free-isolated-factor','status':'not triggered','executed':False,'paper_formula_retained':True}
        ],
        'target_source':{'executed':False,'trigger_count':None,'status':'not triggered'},
        'source_realizability':{'established':False,'status':'OPEN'},
        'Lean':{'executed':False,'new_theorem':False},
        'general_N45_N2_E':{'established':False,'status':'OPEN'},
        'inherited_schedule_counts':domain['counts'],
        'assigned_schedule_count':24,'assigned_schedule_spoke_variants':38,
        'schedules_are_source_counts':False,'complete_geometry_coverage':'not enumerated',
        'assigned_schedules':assigned,
        'inherited_restoration_excluded_schedules':[
            {**s,'authority':'sealed adopted review, not this task',
             'dependencies':['SF-T2-Q0-Q1-RESTORED','SF-QX','SF-RESTORE','K1-K12'],
             'restored_row':'01202'} for s in domain['excluded_schedules']],
        'minimal_named_residual':'same-source-Delta-restorable-r-fibre-nonemptiness',
        'precise_residual':'exists gamma in Delta,a!=gamma(b4),b with literal s-spoke factor1,full C(gamma;a,b) and actual U(gamma;b) nonempty',
        'stronger_cross_row_fibre_lemma':{'asserted':False,'tested':False,'abstract_relation_counterexample':None}
    }
    write('coverage.json',coverage)
    common={'original_e':['r','b4'],'original_r_coordinate':'r',
            'normalization':'one common source/frame normalization U012/L234/S40',
            'status':'待獨立驗收','new_source_exclusion':False}
    def claim(cid,quantifier,premises,conclusion,kind,deps,proof):
        return {**common,'id':cid,'quantifier':quantifier,'premises':premises,
                'conclusion':conclusion,'conclusion_type':kind,'dependencies':deps,'evidence':proof}
    claims=[
        claim('TF-BLOCK','every finite actual connected C with actual bridge/odd-cycle block-tree, every literal attachment assignment gamma',
              ['all original edges occur exactly once in actual blocks','actual all-vertex/block incidence is a tree','all literal B attachments retained'],
              'V-REC/K-REC restriction and union are mutually inverse on every complete proper original-C assignment',
              'arbitrary-size paper identity',['local original edge inequalities','induction on actual block incidence tree'],['transfer-proof.md sections2-4','transfer.py']),
        claim('TF-FIBRES','every original ordered contact list including repeated shared vertices, every ambient tuple and r colour, every ordered(a,b)',
              ['TF-BLOCK','fixed actual contact order and named vertex coordinates'],
              'bijection restricts to all full tuple inverse images; all empty cells, r colours, diagonal pins and original branch coordinates retained',
              'arbitrary-size exact interface identity',['TF-BLOCK'],['transfer-proof.md section5','certificate.json']),
        claim('TF-X','every actual X with same original C/U components, every proper gamma and all16 pins',
              ['actual full C and U original edges/attachments supplied','all actual s contacts and literal spokes supplied','no rs or retained r spoke','isolated original vertices retained'],
              'all full X lifts biject to spoke-factor times Lambda_C(gamma;a,b) times actual Lambda_U(gamma;b) times Col^I',
              'conditional exact graph factorization; U/G absent in microcases',['TF-FIBRES','restriction/union on disjoint actual components'],['transfer-proof.md section6']),
        claim('TF-RESTORE','every same original pair G=X+rb4, every literal gamma and ordered(a,b)',
              ['same original vertices and all retained edges','original removed e=rb4'],
              'full G lift set equals full X lift set for a!=literal gamma(b4), otherwise empty; no unused-colour substitution',
              'arbitrary-size restored-edge identity',['original edge inequality'],['transfer-proof.md section7']),
        claim('TF-COLOR','every fixed actual piece and colour permutation pi satisfying each literal attachment and root-pin constraint',
              ['same actual piece vertices/edges/contacts','pi sends each gamma attachment colour to gamma-prime attachment colour','shared vertices and target root pins coherent'],
              'full assignments and every tuple inverse image transport bijectively; return to common literal frame before component join',
              'conditional paper colour-transport identity',['bijection of four colours','TF-FIBRES','TF-X'],['transfer-proof.md section8']),
        claim('TF-FINITE','exactly four valid named C microcases,ten literal rows,all64 ambient cells,all16 pins and three spoke factors per row',
              ['cases.json fixed before enumeration','BRIDGE_BAD6 invalid case preserved','original full degree4 verified for valid cases','disk topology unverified','no actual U/G or K11/K12 witnesses'],
              'all1344 full assignments and complete interface preimages match independent original-edge enumeration; three corrupt certificates rejected',
              'finite interface calibration only',['TF-BLOCK implementation','independent stdlib direct enumerator'],['certificate.json','degree-audit.json','logs/check-normal.stdout','negative-plan.json']),
        claim('TF-DOMAIN','24 inherited necessary schedules and every original s-spoke variant (38 variant records)',
              ['sealed adopted acceptance/corrections','K1-K12 for any asserted target source'],
              'full Delta and ten rows/all16 pins preserved as symbolic source obligations; no target relation or preimage count fabricated',
              'inherited necessary domain; same-source restoration OPEN',
              ['SF-QX','SF-RESTORE','SF-T2-Q0-Q1-RESTORED','query partition12+4+10+4','sealed remaining-schedules.json'],['coverage.json','transfer-proof.md section9'])
    ]
    write('claims.json',{'task_id':'N45-S-LONG-S-BLOCK-TRANSFER','status':'待獨立驗收',
         'base':domain['base'],'claims':claims,
         'recurrence_requires_K11_K12':False,'promotion_to_target_source_requires_K1_K12':True,
         'target_source':coverage['target_source'],
         'evidence_layers':{'paper':'proved scoped identities pending independent review','finite':'triggered and holds',
                           'source':'not triggered','source_realizability':'OPEN','Lean':'not executed','general_N45_N2_E':'OPEN'}})
    print(json.dumps({'claims':len(claims),'assigned_schedules':24,'schedule_spoke_variants':38,
                      'complete_symbolic_pin_obligations':38*10*16,'new_source_exclusions':0},sort_keys=True))

if __name__=='__main__':
    main()
