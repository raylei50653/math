#!/usr/bin/env python3
"""One-time scoped HIGH1 documentation adoption from the recorded intake texts."""
import difflib,json
from review import ROOT,OUT,WORKER,BASE,contract,sha,put
AUTH='docs/c5_excess_two_nonadjacent_unit_core45.md'
HISTORY='docs/history/2026-10-10-n45-high1-adoption.md'

def main():
    assert not (OUT/'acceptance.json').exists() and not (ROOT/HISTORY).exists()
    originals=json.loads((OUT/'shared-before.json').read_text())
    for rel in list(originals)[:5]:assert (ROOT/rel).read_text()==originals[rel],rel
    s=originals[AUTH]
    marker='完成限定採納與 LOW 覆蓋核對。\n'
    s=s.replace(marker,marker+'''後續 [HIGH1](../audits/2026-10-10-n45-s-high1/REPORT.md)經
[H1A 紙面](../audits/2026-10-10-n45-h1a/REPORT.md)、
[H1R 原圖與完整關係](../audits/2026-10-10-n45-h1r/REPORT.md)、
[H1C 封存](../audits/2026-10-10-n45-h1c/REPORT.md)及
[HIGH1 監督採納](../audits/2026-10-10-n45-high1-supervision/REPORT.md)，完成完整 H1–H13 內的限定採納。
''',1)
    s=s.replace('其餘必要化約不宣稱實現或排除。','**N45-S-HIGH1 已排除：** 原 U incidence=1在 s、原 s兩 spokes全留，僅省略原 r一條 spoke；\n完整 H1–H13、X=M及 U/P/Q全留，十項 claims已獨立採納，見§2.5。\nHIGH2／HIGH3、long等其餘必要化約不宣稱實現或排除。',1)
    s=s.replace('限定 LOW 已由 LOW1／LOW2 覆蓋排除，HIGH 仍 OPEN','限定 LOW 已由 LOW1／LOW2 覆蓋排除；HIGH1另經完整契約排除，HIGH2／HIGH3仍OPEN')
    table='| S-SHORT-U-LOW scoped composition |'
    pos=s.index('\n',s.index(table))
    s=s[:pos]+'''
| HIGH1-CORE／COMP／JOIN／RESTORE／F／MAP | X自己的45／54身份；實際C與U的(2,1)完整接合、全部r色fibres與原e恢復條件；BASE (2,1)的排除／指定X延拓分清 | 全部H1–H13；X指定延拓不提升為G；H1A／H1R各核十claim，工具不裁paper |
| HIGH1-K33／ARC／REJECT／EXCLUSION | 原G的六bags九鄰接迫P/Q支援邊頂點互斥；原U盾弧長2、support連續三點；同列未用D的完整G lifts迫Q(G)⊆該三點，矛盾完整933／941 | 任意大小paper＋明列BASE／Gallai信任；只關U incidence1在s且s兩spokes的HIGH1，無新有限來源或Lean |
'''.rstrip()+s[pos:]
    section='''### 2.5 N45-S-HIGH1：原 K₃,₃ 與同列完整 G lifts

只取§1精確S身份：原U只接s、唯一原sx且無U–r；P/Q各actual support恰真原框邊兩端，
(m_r,m_s)=(3,2)，s對P/Q各一，r分配1與2。原r/s各兩spokes，僅省略e=rb_i，
X保rb_j及全部s-spokes；U/P/Q整份全留。X=G−e=M自己的β-minimality另列，
有效H連通／full B-touch、原degree4/5、Σ-critical／ε2、所有具名ordered資料、空fibres與full lifts
及共同整圖D5／S4／root swap均保留。全部十三項前提逐字見
[HIGH1 H1–H13](../audits/2026-10-10-n45-s-high1/REPORT.md)。

H_X−s恰C={r}∪P∪Q與U，原s contacts分配(2,1)。接合C完整雙tuple及r色fibres、
U單contact fibre、同一s色與全部isolated free factors，restriction／union逐項雙射；
恢復G僅另加r≠γ(b_i)，不能先丟r投影。X自己的minimality與degree-list slack給精確private cover；
BASE局部N-diagonal限制F_C={β(b_j)}、F_U={未用D}。BASE (2,1)指定列延拓仍只屬X。

若P/Q兩個不同支援邊共端v，在**原G**取左bags P,Q,O=B−{v}，右bags {r},{s},{v}。
三左bags連通且六bags互斥；P/Q各有兩root原contacts與真v附件，O–v有原框邊，
r/s各兩個不同spokes確保O–r／O–s各有原邊，合九鄰接成K₃,₃。O–r可用被省略e，
因這一步在原G；故兩支援邊頂點互斥。原sx的critical witness與避U外路接回BASE unary盾下界，
再用原盾弧連續／邊互斥迫U恰佔唯一剩餘長2框弧，actual support恰其連續三點T。

對任一proper三色literal γ，若T沒有看到全部三個已用色，取已用而未在U support出現的h，
以完整U assignments的(D,h)換色雙射及單contact禁色容量≤1，得到U存在避D的完整lift。
同一γ令**原r=s=D**，BASE E4§4.1提供P/Q完整同色N-diagonal lifts，全部原spokes含e均合法，
union即為原G完整coloring。故原拒絕q_k必有k∈T；完整933的四拒點不能落於T，
941的三個非連續拒點也不能等於T，共同整圖D5像照留，933 q2未漏。

[H1A](../audits/2026-10-10-n45-h1a/REPORT.md)與[H1R](../audits/2026-10-10-n45-h1r/REPORT.md)
各獨立核十claims，無新增前提或gap；[監督接受紀錄](../audits/2026-10-10-n45-high1-supervision/acceptance.json)
逐字保全部H1–H13。這是任意大小paper，沿用BASE原盾／N-diagonal／(2,1)論證及
[外部Dvořák Gallai Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)信任界；
封存與有限toy只核語義／算術，未建立或執行HIGH1 finite source，沒有trigger數或新Lean。

'''
    s=s.replace('## 3. 精確 OPEN 與下一個窄分支',section+'## 3. 精確 OPEN 與下一個窄分支',1)
    start=s.index('S 的兩 short 分支原按 LOW／HIGH')
    end=s.index('## 4. 證據、重播與保留失敗',start)
    s=s[:start]+'''S的兩short分支原按LOW／HIGH區分；限定LOW已由§2.4全排，HIGH1另由§2.5限定排除。
HIGH仍保(U原incidence,t_s)=(2,1)、(3,0)兩支；一般HIGH合成尚未關閉。

下一個窄題 **N45-S-HIGH2：原U incidence=2在s、s唯一spoke**。
(m_r,m_s)=(3,2)，原r兩spokes只刪e留rb_j；U兩原contacts及cycle、P/Q全留，X=M自己minimal。
H_X−s恰C={r}∪P∪Q與U，contacts(2,2)，須查完整ordered tuples、r色fibres與恢復原e的條件。
不能沿用HIGH1的單contact容量；原K₃,₃共端特殊case須重建具名原bags與九鄰接。
[HIGH2完整任務與八pins](history/2026-10-10-n45-high1-adoption.md)已備、尚未啟動；推導義務不作已採結論。
§1指定U身份已由§2.2全排；HIGH3、long、原55、其他cores、無45／54來源、一般N2／E及ε≥3仍OPEN。

'''+s[end:]
    evidence='''本輪HIGH1 worker 91 payload＋3個精確top-level metadata＝94 regular，無symlinks；
34frozen inputs為16BASE／17current／1external，九原派工pins及receipt十二commands／24streams核回。
原checker與完整receipt在共享文件採納前normal／seed17實際exit0且各對stdout一致。
採納後17個current輸入可能變動，改由獨立凍結verifiers與父端custody核回，不宣稱原live-input checker仍適用。
H1A／H1R兩份paper、H1C artifact-only均封存；父端六次完整重播exit0、normal／seed17各對byte一致。
H1C獨立Cartesian算術只校準toy的240literal rows／16rootqueries／2160 X及1560 G lifts，沒有HIGH1來源。
四種父端wrong-artifact probes各實際exit2命中certificate／input-index／receipt／payload-inventory階段；
H1C另核十項工具negatives，均不裁source前提。H1C保5,899 tracked bytes與worker94檔bytes/modes；
父端另核原Git-listed 32,713 regular、27symlinks及四nested repo目錄存在，遞迴內容不在其hash範圍。
既存歷史缺檔／E4 provenance與whole-worktree DocGraph 62 duplicate-ID FAIL保留，formal docs另核。
完整範圍與停L2記錄見[HIGH1監督報告](../audits/2026-10-10-n45-high1-supervision/REPORT.md)。

'''
    s=s.replace('## 4. 證據、重播與保留失敗\n\n','## 4. 證據、重播與保留失敗\n\n'+evidence,1)
    edits={AUTH:s}
    rel='docs/c5_kempe_guide.md';s=originals[rel]
    s=s.replace('HIGH／long、其他cores及一般N2／E仍OPEN；[HIGH1任務](history/2026-10-10-n45-low2-adoption.md)已備、尚未啟動。\nHIGH1的X−s有C與U兩分量，須重核(2,1)完整接合及恢復spoke的r色條件；沒有新LOW2來源或Lean。','該輪[HIGH1任務](history/2026-10-10-n45-low2-adoption.md)保留發布時語境；沒有新LOW2來源或Lean。\n**HIGH1限定採納（2026-10-10）：** [H1A／H1R／H1C及監督](../audits/2026-10-10-n45-high1-supervision/REPORT.md)\n核十claims與全部H1–H13，排除原U incidence1在s、s兩spokes全留、僅刪r原spoke且X=M的HIGH1。\n實際(2,1)接合保全部r色fibres；原G的K₃,₃九鄰接、U盾support及同列未用D的完整原G lifts成立。\nBASE／外部Gallai、paper與toy分層，沒有新HIGH1有限來源或Lean。HIGH2／HIGH3、long與一般N2／E仍OPEN。\n[下一HIGH2雙contact／single-spoke任務](history/2026-10-10-n45-high1-adoption.md)與八pins已備、未啟動；\n須重核(2,2)完整tuples／r色fibres、原K₃,₃共端case與原e接回，停止L2。')
    edits[rel]=s
    rel='docs/STATUS.md';s=originals[rel].replace('（LOW2與限定S-SHORT-U-LOW採納）','（HIGH1完整契約限定採納）',1)
    s=s.replace('HIGH／long、其他cores及一般N2／E仍OPEN；HIGH1任務已備尚未啟動','HIGH1完整H1–H13另已排；HIGH2／HIGH3、long、其他cores及一般N2／E仍OPEN；HIGH2八pins已備未啟動',1)
    marker='| [N45-S-LOW2交付]'
    pos=s.index(marker)
    s=s[:pos]+'''| [N45-S-HIGH1交付](../audits/2026-10-10-n45-s-high1/REPORT.md)、[H1A紙面](../audits/2026-10-10-n45-h1a/REPORT.md)、[H1R原圖／完整關係](../audits/2026-10-10-n45-h1r/REPORT.md) | 十claims在全部H1–H13內的任意大小排除已採納；原G K₃,₃／原U盾support／同列未用D完整G lifts成立；BASE／Gallai明列，無新有限來源或Lean |
| [H1C封存](../audits/2026-10-10-n45-h1c/REPORT.md)、[HIGH1監督採納](../audits/2026-10-10-n45-high1-supervision/REPORT.md) | worker91payload／3exact metadata、34frozen inputs／九pins／十二commands核回；三完整稽核父端normal／seed17各同bytes；wrong-artifact negatives命中，歷史及62duplicate-ID FAIL保留，H1C不裁paper |
| [HIGH1採納與HIGH2任務](history/2026-10-10-n45-high1-adoption.md) | 只採完整HIGH1；下一原U雙contact在s／sole spoke、實際(2,2)完整join與r色fibres；八pins與全文已備未啟動，HIGH3／long及一般N2／E仍OPEN，停止L2 |
'''+s[pos:]
    s=s.replace('LOW2及§1限定LOW覆蓋採納；HIGH1完整任務與pins已備、未啟動；實際X−s兩分量需另核(2,1)接合；HIGH／long及一般N2／E仍OPEN，停止L2','LOW2及§1限定LOW覆蓋採納；原HIGH1任務／pins保留該輪發布語境，後續限定HIGH1採納與HIGH2任務見上列最新紀錄，歷史正文不改')
    s=s.replace('三份獨立稽核及覆蓋已驗收，HIGH1已備尚未啟動','三份獨立稽核及覆蓋已驗收；原HIGH1任務保留當輪日期語境，後續HIGH1已限定採納')
    marker='- [2026-10-10：LOW2、限定LOW採納與HIGH1任務]'
    pos=s.index(marker);s=s[:pos]+'- [2026-10-10：HIGH1限定採納與HIGH2任務](history/2026-10-10-n45-high1-adoption.md)；三獨立稽核已驗收，HIGH2八pins與完整任務已備、未啟動\n'+s[pos:]
    edits[rel]=s
    rel='docs/c5_phase_b_common_lemmas.md';s=originals[rel]
    s=s.replace('spoke省略仍留HIGH與long；沒有新finite來源或Lean。','後續[HIGH1完整契約](c5_excess_two_nonadjacent_unit_core45.md#25-n45-s-high1原-k₃₃-與同列完整-g-lifts)\n另排原U incidence1在s、s兩spokes全留且X=M的spoke身份：原K₃,₃九鄰接、原U三點support\n與同列未用D的完整G lifts給矛盾；BASE／外部Gallai明列。仍留HIGH2／HIGH3與long，沒有新finite來源或Lean。')
    edits[rel]=s
    rel='artifacts/c5_excess_two_e4/REPORT.md';s=originals[rel]
    pos=s.index('\n')+1;s=s[:pos]+'''
**後續（2026-10-10，HIGH1限定採納）。** [HIGH1監督驗收](../../audits/2026-10-10-n45-high1-supervision/REPORT.md)
在[N45全部H1–H13](../../docs/c5_excess_two_nonadjacent_unit_core45.md)內，排除原U incidence1在s、
s兩spokes全留且只刪原r-spoke、X=M的HIGH1。H1A／H1R各核十claims；原G K₃,₃及同列
未用D的完整G lifts成立，BASE／Gallai與工具分層。HIGH2／HIGH3、long、其他cores／原55及N2／E仍OPEN。
無新有限來源或Lean；下列有日期的歷史正文及FAIL保留，原三列量詞未提升。
'''+s[pos:];edits[rel]=s
    for rel,text in edits.items():
        assert text!=originals[rel],rel
        (ROOT/rel).write_text(text)
    with (OUT/'documentation.diff').open('x') as f:
        for rel,text in edits.items():f.write(''.join(difflib.unified_diff(originals[rel].splitlines(True),text.splitlines(True),fromfile='before/'+rel,tofile='after/'+rel)))
    incoming=json.loads((OUT/'incoming-audits.json').read_text())
    claims=json.loads((WORKER/'claims.json').read_text())['claims']
    acceptance={'BASE':BASE,'decision':'accepted_full_HIGH1_only','full_source_contract':contract(),
        'accepted_claim_ids':[c['id'] for c in claims],'accepted_claims':claims,
        'paper_verdict':'arbitrary finite full H1-H13 source excluded; two independent paper reviews and supervisor reconstruction',
        'paper_proved_by_tool':False,'trust':['named frozen BASE paper arguments and their existing external/structural/finite trust','external Gallai Lemma7/Theorem10','standard original-graph K33 nonplanarity'],
        'external_url':'https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf','external_pdf_sha256':'50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea',
        'independent_audits':{r:{k:v for k,v in x.items() if k!='full_tree'} for r,x in incoming.items()},
        'worker':json.loads((OUT/'inputs-before.json').read_text())['checks'],
        'worker_current_input_post_adoption':'frozen independent replay and supervisor custody; original live-input worker checker not claimed',
        'finite_source_controls':'not established; not executed; no HIGH1 trigger count','source_realization':False,
        'new_Lean':False,'general_N2_E':'OPEN','HIGH2':'OPEN','HIGH3':'OPEN','long':'OPEN',
        'adopted_shared_sha256':{r:sha((ROOT/r).read_bytes()) for r in edits},'new_history':HISTORY,
        'propagation_stop':'L2; five shared files and one new history; HANDOFF/README routing unchanged',
        'retained_failures':['historical two BASE missing docs','historical E4 provenance','whole-worktree DocGraph 62 duplicate-ID errors'],
        'evidence_boundaries':['H1C artifact-only; maths not adjudicated','fixed-domain toy is calibration only','H1C 5899 tracked byte custody; untracked old inputs only','supervisor Git-listed original regular/symlink state, nested repository directory presence only','X prescribed-row extensions are not G extensions','HIGH2 proposed geometry/private-cover deductions are task obligations, not adopted results'],
        'commit_push':False}
    put('acceptance.json',acceptance)
    pinpaths=[AUTH,'audits/2026-10-09-n45-s/REPORT.md','audits/2026-10-09-n45-su-a/independent-judgment.json',
              'audits/2026-10-10-n45-s-high1/REPORT.md',
              *[f'audits/2026-10-10-n45-{s}/independent-judgment.json' for s in ['h1a','h1r','h1c']],
              str(OUT.relative_to(ROOT))+'/acceptance.json']
    pins={'BASE':BASE,'task':'N45-S-HIGH2','status':'prepared; not launched','output':'audits/2026-10-10-n45-s-high2/',
          'pins':[{'path':r,'sha256':sha((ROOT/r).read_bytes())} for r in pinpaths]}
    put('high2-task-pins.json',pins)
    history='''# HIGH1 限定採納與 HIGH2 任務

日期：2026-10-10。研究 BASE `'''+BASE+'''`。

[HIGH1 worker](../../audits/2026-10-10-n45-s-high1/REPORT.md)十claims在全部H1–H13內已正式採納。
[H1A](../../audits/2026-10-10-n45-h1a/REPORT.md)與[H1R](../../audits/2026-10-10-n45-h1r/REPORT.md)
各自獨立裁紙面／原圖與完整關係，沒有新增充分前提或gap；
[H1C](../../audits/2026-10-10-n45-h1c/REPORT.md)只接受artifact integrity。
[監督接受紀錄](../../audits/2026-10-10-n45-high1-supervision/acceptance.json)逐字保十三項前提，
[權威頁§2.5](../c5_excess_two_nonadjacent_unit_core45.md)保原G K₃,₃、U盾弧及同列未用D full lifts。
任意大小paper依賴BASE與外部Gallai；toy／封存不承擔source排除，沒有HIGH1有限來源、trigger數或新Lean。
只關HIGH1；HIGH2／HIGH3、long、原55、其他cores及一般N2／E仍OPEN。
本輪只更新五份相连共享文件加本歷史紀錄，停止L2；無commit／push。

## HIGH2 派工全文（已備，未啟動）

任務ID：N45-S-HIGH2。唯一新輸出 `audits/2026-10-10-n45-s-high2/`；若該目錄已存在，立即STOP，
不得覆寫或重用。以下八pins先逐檔核回；任何不符只交finding並停止，不自行更新pin。

'''
    for pin in pins['pins']:history+='- '+pin['path']+'\n  SHA256 '+pin['sha256']+'\n'
    history+='\n完整任務契約與義務如下。兩個可嘗試的推導（禁色角色、擴大O袋）均是待證義務，不是本輪採納結論。\n\n```text\n'+(OUT/'high2-task-body.txt').read_text()+'```\n'
    with (ROOT/HISTORY).open('x') as f:f.write(history)
    print(json.dumps({'adopted_scope':'full HIGH1 only','shared_existing':len(edits),'new_history':1,'HIGH2_pins':8,'HIGH2_launched':False},sort_keys=True))
if __name__=='__main__':main()
