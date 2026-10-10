#!/usr/bin/env python3
"""Write a reviewable report from the scoped decision and actual recorded evidence."""
import json
from review import OUT,BASE,contract

def main():
    a=json.loads((OUT/'acceptance.json').read_text());incoming=json.loads((OUT/'incoming-audits.json').read_text())
    text='''# N45-S-HIGH1 監督裁決與後續停點

日期：2026-10-10。研究 BASE `'''+BASE+'''`。

**正式接受完整 H1–H13 內的 HIGH1 任意大小紙面排除。** 十項claims由兩份獨立數學稽核與監督重建支持，
沒有新增充分前提或gap。工具稽核只接受artifact完整性；paper、BASE／外部定理、toy及source／Lean證據分層。
[接受紀錄](acceptance.json)逐字保契約及worker claims；[原交付](../2026-10-10-n45-s-high1/REPORT.md)保持候選時語境、封存未改。
本輪只採HIGH1；HIGH2／HIGH3、long、原55、其他cores、無45／54來源、一般N2／E及ε≥3仍OPEN。

## 1. 原來源契約與十項裁決

以下共同作用於任意大小同一原G；全部前提一起使用，不能拆成一般(2,1)或一般HIGH排除。

| ID | 完整來源前提 |
| --- | --- |
'''
    for key,value in contract().items():text+=f'| {key} | {value} |\n'
    text+='''
| CLAIM | 採納結果與量詞界線 |
| --- | --- |
| HIGH1-CORE | 指定X自身完整degrees(4,5)、β-minimality及繼承disk／T4；不自G criticality遺傳 |
| HIGH1-COMP | 實際H_X−s恰原C={r}∪P∪Q與U，原contacts(2,1) |
| HIGH1-JOIN | 任一proper literal γ、全部ordered tuples／r,s pins／ambient空非空fibres／完整assignments與I自由因子的restriction／union雙射 |
| HIGH1-RESTORE | 任一γ的原G full lifts恰原X full lifts另加r≠γ(b_i)；不丟r投影 |
| HIGH1-F | 固定原拒β的精確private cover，F_C={β(b_j)}、F_U={未用D}；一般γ的unpinned relations非空 |
| HIGH1-MAP | 各原β及spoke orbit逐項滿足BASE (2,1)充分前提；指定split／nonadjacent延拓仍屬X，不提升G |
| HIGH1-K33 | P/Q真支援邊共端時，原G六互斥連通bags及九條原鄰接給K₃,₃ |
| HIGH1-ARC | 原critical U-contact witness／避U外路與原盾規則迫U盾弧長2、actual support恰連續三點 |
| HIGH1-REJECT | 任一proper三色γ，若U support未看全三已用色，同列未用D完整U／P／Q lifts與r=s=D直接接回原G |
| HIGH1-EXCLUSION | 完整H1–H13的任意有限原G不存在；完整933／941、933 q2及共同整圖搬運保留 |

[H1A紙面](../2026-10-10-n45-h1a/REPORT.md)逐claim核量詞／依賴／完整前提，
[H1R原圖／關係](../2026-10-10-n45-h1r/REPORT.md)另核full lifts／原bags／盾弧；二者未互讀本輪peer judgments。
H1A前提逐字相同；H1R十三項paraphrases經監督逐項對回原契約，結構gate只核顯式欄位，不當語義定理驗證。
完整監督推導見[paper reconstruction](paper-reconstruction.md)；結構／原檔gate見[judgment gate](judgment-gate.json)。

## 2. 關鍵紙面論證與信任界

若P/Q支援邊共端v，在原G取左P,Q,B−v，右r,s,v。P/Q至各root及v有六原邊，
B−v至v有框邊，r/s各兩個不同spokes給B−v至r/s兩原邊，六bags連通／互斥、九鄰接完整。
可使用省略e，因這一步在原G。故两支援邊頂點互斥。原sx的Σ-critical full witness給U真正盾；
H−U連通且full B-touch提供避U的實際外路。BASE unary盾下界≥2、連續／邊互斥、actual support涵蓋全σ點
迫U恰位於剩餘長2框弧，support為連續三點T。

若三色γ未在T看全三個已用色，選其中一個缺於U support的h；在完整U assignments上換(D,h)，
以單contact禁色容量≤1得避D的full lift。同一γ、同一原G設r=s=D，用BASE E4§4.1的局部N-diagonal
給P/Q完整同色lifts，union接回所有原邊含恢復e與孤立free factors。因此Q(G)⊆T。
933拒四點不能包含於T；941的三個非連續拒點不能等於T，所有共同整圖D5像照留。

信任包括凍結BASE原盾／完整N-diagonal／(2,1)論證及其已明列結構／有限化約信任、標準K₃,₃非平面性，
以及[外部Dvořák Gallai Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
官方PDF凍結SHA `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`；
外部定理和BASE論證沒有由Python或Lean重新證明。没有新HIGH1 finite source，未建立／未執行／無trigger數；
同源有限正常形、source realizability及一般N2／E未關閉，沒有新Lean，也未將lake build當paper驗證。

## 3. 封存、實際重播與負控制

原worker精確91 payload、3 top-level metadata、94 regular／0 symlinks；nested同名metadata一律仍為payload。
34 frozen inputs＝16BASE Git blobs＋17 current＋1 external；九派工pins核回，receipt綁十二actual commands及24 streams。
初始原checker normal／seed17及worker完整receipt normal／seed17各actual exit0、各對stdout byte一致，
[初始實際工具回傳](initial-replays.json)保留。採納後17 current輸入可變，後续用凍結獨立verifiers與父端custody，
不宣稱worker原live-input checker仍適用。

[H1C](../2026-10-10-n45-h1c/REPORT.md)僅裁工具／封存，獨立Cartesian重算1,960,670 bytes certificate，
SHA `0aa93b73a4a46b204004752d8c32fce899f689d875d4e3368c4808b1e8e0f1bf`。
240 literal rows、每canonical row十列中的64 C tuple/r fibres及4 U fibres、每literal row16雙root pins，
2160 X／1560 G toy lifts只校準語義；不充來源排除或正觸發。
H1R另做2400 commonD5／S4 whole transports與兩個過強relation版本的反例校準，不當HIGH1 source。

父端四wrong-artifact probes均actual exit2：bad certificate命中certificate byte comparison；
bad input-index命中fixed-domain input validation；bad正式receipt命中delivery／receipt exact binding；
省略nested receipt命中payload inventory。兩個receipt probes用正式delivery，不使用synthetic override。
H1C十項獨立工具negatives全部命中其預期拒絕階段。負控制只核fail-closed artifact行為。

'''
    text+='| 獨立稽核 | Payload | 精確receipt metadata | Full regular | Manifest SHA256 |\n| --- | --- | --- | --- | --- |\n'
    for rel,x in incoming.items():text+=f"| {rel.rsplit('-',1)[-1].upper()} | {x['payload_files']} | {x['receipt_bound_metadata_files']} | {len(x['full_tree'])} | `{x['manifest_sha256']}` |\n"
    text+='''
父端六次完整獨立封存重播實際exit0，三對normal／seed17各stdout byte一致；[獨立envelope intake](incoming-audits.json)
綁三完整不可變tree及judgment SHA。正式採納前再次核所有原Git-listed檔案identity。

## 4. 文件傳播、後續任務與失敗保留

更新[authority](../../docs/c5_excess_two_nonadjacent_unit_core45.md)、[guide](../../docs/c5_kempe_guide.md)、
[STATUS](../../docs/STATUS.md)、[Phase B直接consumer](../../docs/c5_phase_b_common_lemmas.md)、
[E4父題](../../artifacts/c5_excess_two_e4/REPORT.md)，加新[採納／HIGH2派工歷史](../../docs/history/2026-10-10-n45-high1-adoption.md)。
[當輪文檔差異](documentation.diff)只比較本轮shared-before，不混入先前未提交更動。
依DOCUMENTATION停L2；HANDOFF／README路由不變，舊歷史與所有舊audit未改，無commit／push。

[HIGH2 outline](high2-task-outline.md)與[八pins](high2-task-pins.json)已備、未啟動。
下一題只取原U雙contact在s／s唯一spoke、X=M自己minimal、C與U的(2,2)完整join／r色fibres／原e接回。
可嘗試由N-diagonal＋private cover推C/U禁色角色(1,2)，以及共端特殊case以(B−v)∪U重建原bags；
兩者是新的待證義務，每條充分前提／原邊需重核，不當本輪HIGH1自動推論。
原U cycle、ordered tuples及全部full lifts不可換成單contact，HIGH3／long／一般N2／E仍OPEN。

歷史BASE check_docs缺兩路徑actual exit1保留原stderr；兩個E4 provenance replay FAIL保留、未重跑。
whole-worktree DocGraph的62 duplicate-ID FAIL保留；正式docs另驗。根目錄封存只精確排當前MANIFEST／delivery
及十個綁定receipt metadata，nested同名檔仍進payload。`checks.json`、`adoption-state.json`與最終封存
`MANIFEST.sha256`／`delivery.json`记录實際checks／允許變更與不可變payload，不由exit紀錄證paper。

## 5. 驗證與 custody 結果

結果待以下已授權檢查執行後填入；封存前必須替換本段。
'''
    (OUT/'REPORT.md').write_text(text.replace('两支援','兩支援').replace('没有','沒有').replace('后续','後續').replace('本轮','本輪').replace('记录','記錄'))
if __name__=='__main__':main()
