#!/usr/bin/env python3
"""Claims, complete symbolic obligations, and internal review provenance."""
import json
from setup import OUT, BASE, dump
from checker import ROWS, QROWS

def claim(cid,quantifier,premises,conclusion,kind,section,deps=(),open_obligations=()):
    return {'id':cid,'quantifier':quantifier,'premises':premises,'conclusion':conclusion,
       'conclusion_type':kind,'adoption':'candidate pending independent acceptance',
       'evidence':[{'layer':'paper derivation','path':'REPORT.md','section':section}]+
                  [{'layer':'BASE paper dependency','path':p} for p in deps],
       'finite_source_status':'not triggered','finite_source_trigger_count':None,
       'unresolved_obligations':list(open_obligations)}

if __name__=='__main__':
    K='K1–K12 exactly; original U owner=s; (t_s,m_s,n_U)=(1,2,2) or (2,2,1)'
    claims=[
     claim('SF-JOIN','Every finite source satisfying K; every proper literal gamma; all 16 ordered r/s pins',
       [K,'actual original vertices/edges and contacts; no s pin before constructing C/U'],
       'Restriction/union identifies the complete C/U product at one s color with all X lifts, retaining every preimage, r fibre, empty fibre and isolated free factor.',
       'exact complete-assignment identity','2'),
     claim('SF-PRIVATE','Every such X; every retained s-spoke and every component/contact incident edge',
       [K,'X own same-beta deletion witnesses'],
       'F_C(beta) union F_U(beta)=Col-beta(N_B(s)); private_C and private_U are nonempty; each contact has a full same-beta private witness.',
       'necessary covering and private-witness theorem candidate','3',('docs/c5_degree5_interfaces.md',)),
     claim('SF-R-PROFILES','Both specified profiles; both S support types; all positive original r-contact splits',
       [K,'original shield/star restrictions; singleton S04'],
       'Both support types force t_r=1 and no retained r-spoke. Pair admits (1,3),(2,2),(3,1) before Gallai; singleton only (1,3).',
       'necessary original incidence profiles','4',('audits/2026-10-10-n45-s-long-contract/REPORT.md','audits/2026-10-09-n45-s/REPORT.md')),
     claim('SF-SPLIT-EXCLUSION','Every arbitrary-size source in K and the two profiles',
       [K,'SF-PRIVATE','SF-R-PROFILES','external connected degree-list Gallai characterization','BASE connected-exterior K4 lemma'],
       'C is K4-free Gallai; r meets exactly two odd-cycle blocks, so k_L^r=k_S^r=2. Singleton S and pair r-splits (1,3)/(3,1) have no source under this contract.',
       'limited source-exclusion paper candidate','4',('docs/c5_degree5_tree_components.md','docs/c5_degree5_interfaces.md'),
       ('Independent acceptance of the exact Gallai/hub/block premise mapping.',)),
     claim('SF-C-BOUND','For every proper gamma of the same remaining pair (2,2) source, including every T4 row',
       [K,'SF-SPLIT-EXCLUSION structure','BASE any-row double-forbidden bridge-path lemma'],
       '|F_C(gamma)|<=1; F_C may be empty away from beta. At beta: t_s=1 gives singleton C and complementary pair U; t_s=2 gives complementary singleton C/U.',
       'same-source all-row necessary forbidden bound','4',('docs/c5_single_spoke_two_two.md','docs/c5_single_spoke_bridge_path.md')),
     claim('SF-T1-MAP','Every remaining pair source; all five beta positions, two original s-spokes and three singleton C roles',
       [K,'t_s=1','SF-C-BOUND','actual support C0234/U012 after a single common whole-source normalization',
        'BASE arbitrary-size complete support/schema cover and all subsequent source exclusions'],
       'Only four final necessary queries remain: beta3/spoke0 record511; beta3/spoke2 record90; beta4/spoke0 record90; beta4/spoke2 record511; C forbids1, U forbids{2,3}. They are not source realizations.',
       'necessary-profile restriction, conditional on BASE source-exclusion chain','6',
       ('docs/c5_single_spoke_two_two.md','docs/c5_single_spoke_residual_locality.md','artifacts/c5_single_spoke_two_two/observations.json','artifacts/c5_single_spoke_residual_locality/support_table.md'),
       ('BASE final JSON is missing; no replay or replacement claimed. Paper dependencies remain explicit.',)),
     claim('SF-T1-EXTEND','Every actual T4-accepting X in the single-spoke (2,2) BASE class',
       [K,'t_s=1','own beta minimality and actual complete C/U (2,2)'],
       'X extends the two adjacent-singleton rows to beta. This does not control the color of internal vertex r.',
       'specified X extension','6',('docs/c5_single_spoke_residual_locality.md',),('Restore e by a complete lift with r!=gamma(b_i).',)),
     claim('SF-T2-MAP','Every remaining pair source, all original beta rows and both forbidden-role orders',
       [K,'t_s=2','C0234/U012; s-spokes02; named e=rb4 in the same geometry frame','BASE complete sector theorem'],
       'Only beta0 or beta2 are compatible: beta3/4 duplicate spoke color; beta1 transports to forbidden03. Both C/U role orders were considered before further proof.',
       'limited source restriction','7',('docs/c5_degree5_two_spoke_sectors.md',)),
     claim('SF-T2-ROLE','Every source remaining after SF-T2-MAP',
       [K,'t_s=2','SF-SPLIT-EXCLUSION','actual induced pentagon Gamma=(s,b0,b4,b3,b2)',
        'BASE all-degree4 minimal three-color singleton structure without T4'],
       'F_C(beta)={unused3}, F_U(beta)={used beta1=1}. The alternative C=1 yields an actual three-color pentagon obstruction with shared odd cycles and is excluded.',
       'derived forbidden roles via limited source-exclusion candidate','7',('docs/c5_multi_odd_cycles.md',),
       ('The remaining virtual-pentagon row with s=3 is four-color; the three-color theorem does not apply and T4 is not inherited.',)),
     claim('SF-T2-EXTEND','Every remaining actual t_s=2 source; both beta0/beta2 presentations',
       [K,'SF-T2-ROLE','same-source nonadjacent Case II, with joint whole-source reflection when needed'],
       'BASE gives the two adjacent-singleton X extensions; no internal r color bound follows.',
       'specified X extension','7',('docs/c5_two_spoke_nonadjacent.md','docs/c5_two_spoke_reflection.md'),('Restore e on the same complete X lift.',)),
     claim('SF-QX','Every remaining source in either specified profile',
       [K,'BASE X extension of both beta neighbors','X epsilon1 and own Sigma-criticality; BASE E2 QX singleton/adjacent-pair theorem'],
       'Q(X)={beta}; every gamma in the entire transported Q(G)-{beta} is accepted by X.',
       'complete X boundary-signature candidate','6–9',('artifacts/c5_excess_one_e2/REPORT.md','audits/2026-10-10-n45-s-long-contract/REPORT.md'),
       ('This is not Sigma(G) or a restored original-source coloring.',)),
     claim('SF-RESTORE','Every proper gamma, all16 pins and all complete lifts of the same G/X',
       [K,'X differs by only the named original e=rb_i'],
       'L_G(gamma;a,b)=L_X(gamma;a,b) when a!=gamma(b_i), otherwise empty. On Delta=Q(G)-Q(X), all X lifts have r=gamma(b_i).',
       'exact original-edge restoration identity','8',('audits/2026-10-10-n45-s-long-contract/REPORT.md',)),
     claim('SF-T2-Q0-Q1-RESTORED','Every remaining t_s=2 source with beta=q0, and all its complete X lifts at gamma=q1',
       [K,'SF-T2-ROLE','same-source U012 identical beta/gamma attachments; L234 complete (0 1) transport fixing r2/s3; S40 identical attachments',
        'BASE q1 X extension'],
       'All X(q1) lifts have s=3 and r!=2, so every lift restores rb4. If q1 belongs to transported Q(G), this is a limited source contradiction.',
       'restoration into original G and limited source-exclusion paper candidate','8',('docs/c5_two_spoke_nonadjacent.md',),
       ('Other gamma rows and beta=q2 restoration remain separate obligations.',)),
     claim('SF-RESIDUAL','Every remaining pair(2,2) source and its entire transported 933/941 rejection set',
       [K,'SF-QX','SF-RESTORE'],
       'Original G restoration was proved only for t_s2 beta0->q1. Four of the 28 raw Q/beta schedules are excluded when q1 is an original rejection; 24 remain. Exact residual is the same-source ten-row r-fibre/geometry obligation on original rb4.',
       'precise unresolved source-exclusion obligation','9',(),
       ('Supply a complete original source with all K data, or prove on that same source at least one Delta r!=gamma4 full fibre is nonempty.',
        'All original G critical witnesses and X same-beta minimal witnesses, ordered/shared contacts, rotation and full lifts remain joint requirements.',
        'No total pair exclusion, general N2/E closure, new source realization or Lean theorem.'))]
    claims[3]['evidence'].append({'layer':'external theorem','url':'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf',
        'locator':'Lemma7/Theorem10','frozen_path':'external/gallai.pdf'})
    claims.append({'id':'SF-FINITE','quantifier':'19 frozen prior controls; 21 original r-spoke omissions; all10 literals and16 pins',
       'premises':['fixed BASE original edge inventories; no new graphs or graph-size search'],
       'conclusion':'Complete unpinned C piece join, C/U joint, direct whole X lifts and exact G spoke filter agree; all ambient C r fibres and all tuple preimages saved.',
       'conclusion_type':'finite interface calibration','evidence':[{'layer':'finite control','path':'certificate.json'},
           {'layer':'actual execution','path':'checks.json'}],'control_status':'triggered and holds',
       'finite_source_status':'not triggered','finite_source_trigger_count':None,
       'unresolved_obligations':['No qualifying K1–K12 finite source was established or validated. Controls all accept every X row.',
         'Nonempty isolated factor was not triggered. Rotation/source-criticality/full contract was not certified by this checker.']})
    dump(OUT/'claims.json',{'task_id':'N45-S-LONG-S-FIBRE','base':BASE,'claims':claims,
      'evidence_layers':{'paper':'candidate pending independent acceptance','external_theorem':'separate frozen primary reference',
         'finite_control':'interface and necessary-table arithmetic only','source_realization':'not established',
         'Lean':'no new theorem; no execution','general_proposition':'remaining OPEN'}})
    cert=json.loads((OUT/'certificate.json').read_text());schedules=[]
    for s in cert['schedules']:
        j=s['beta_q'];q=set(s['QG']);rows=[]
        restored_q1=s['t_s']==2 and j==0
        excluded=restored_q1 and 1 in q
        spoke_variants=[[0],[2]] if s['t_s']==1 else [[0,2]]
        for i,gamma in enumerate(ROWS):
            h=QROWS.index(gamma) if gamma in QROWS else None
            beta=h==j;delta=h in q and not beta
            pins=[]
            for a in range(4):
                for b in range(4):
                    empty=beta or (delta and a!=gamma[4])
                    if restored_q1 and h==1 and (a==2 or b!=3):empty=True
                    pins.append({'r':a,'s':b,'X_fibre':'necessarily empty' if empty else 'source-specific; not supplied',
                       'G_fibre':'necessarily empty' if h in q or a==gamma[4] else 'source-specific; not supplied',
                       'full_preimages':'not supplied; source was not realized',
                       'actual_s_spoke_variants':[{'original_s_spokes':sp,
                         'X_fibre':'necessarily empty' if empty or b in {gamma[k] for k in sp} else 'source-specific; not supplied'}
                          for sp in spoke_variants]})
            rows.append({'literal_index':i,'literal':gamma,'q_position':h,'gamma_b4':gamma[4],
              'X_row':'reject beta' if beta else 'accept by BASE/E2 or original accepted row',
              'G_row':'reject by transported target Sigma' if h in q else 'accept by transported target Sigma',
              'required_nonempty':'none' if beta else ('at least one X pin with r=gamma_b4' if delta else 'at least one G/X pin with r!=gamma_b4'),
              'pins':pins})
        schedules.append(dict(s,original_s_spoke_variants=spoke_variants,
           schedule_verdict='limited source-exclusion candidate SF-T2-Q0-Q1-RESTORED' if excluded else 'unresolved necessary source profile',
           same_source_restored_row=1 if restored_q1 else None,
           all_ten_literal_obligations=rows))
    dump(OUT/'obligations.json',{'task_id':'N45-S-LONG-S-FIBRE','scope':'symbolic complete source obligations; no source relation fabricated',
       'geometry':{'U_support':[0,1,2],'L_support':[2,3,4],'S_support':[4,0],
         'e':['r','b4'],'r_retained_spokes':[],'r_contact_split':[2,2],'s_mixed_split':[1,1]},
       'raw_schedule_count':len(schedules),'excluded_schedules':sum(s['schedule_verdict'].startswith('limited') for s in schedules),
       'residual_schedules':sum(s['schedule_verdict'].startswith('unresolved') for s in schedules),'schedules':schedules})
    dump(OUT/'reviews.json',{'independent_acceptance':'pending; internal read-only subtasks are not adoption',
      'internal_reviews':[{'task':'single_spoke_routes','scope':'BASE t1 cover, 30 necessary queries, extension/restoration distinction'},
       {'task':'two_spoke_routes','scope':'all t2 sectors/orders, actual pentagon role proof, full rejection schedules'},
       {'task':'fibre_proof_review','scope':'private witnesses, full r fibres, all-row C bound, Gallai block mapping'}],
      'corrections_retained':['After geometry normalization, transport the full original Q(G); do not recanonicalize Sigma independently.',
        'Missing BASE final JSON is a finding; physical bytes excluded, never substituted.',
        'Four-color virtual-pentagon rejection cannot use the three-color structure theorem or inherit original T4 pins.',
        'Root field absent in old controls; infer original named roots from piece owners.',
        'All source trigger counts stay null; finite controls certify interface only.']})
    print(f'{len(claims)} claims; {len(schedules)} complete ten-row/16-pin obligation schedules.')
