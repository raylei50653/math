# 2026-10-03：ε=2 四-spoke mixed-(1,1) 加各側 unary 的子型完成

使用者要求「繼續推進 ε ≥ 3」及「繼續」。接手HEAD=`0e38127`，
cwd=`/home/ray/developer/ai/math`，保留既有未提交短／長face成果，
同一續研turn完成原crosscut、短框弧joint及本頁不相交pairs三份窄證書。
未commit／push，未重開來源catalogue，前序artifacts原樣保留。

## 整個原子型完成

[完成報告](../c5_excess_two_mixed_core_four_spoke_disjoint_pairs.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py)、
[artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs/observations.json)
在固定完整Σ933／941／整圖D₅像、Σ edge-minimal induced-C₅ disk、
有效H連通、ε=2、相鄰雙完整degree-5 roots、其餘有效內點完整degree四，
唯一原mixed incidence11與兩原單接點unary、兩側各兩spokes的前提下，
封閉剩餘14／18不相交pairs，完成原47／75份必要框架。
原contacts可共鄰但不複製頂點；全部原C/U/V、actual supports、附件、
bridges、旁支、ownership、環序及共同字面色框保持。

先由原[unary crosscut](../c5_excess_two_mixed_core_four_spoke_crosscut.md)
新排8／16，unequal22／40→14／24。再以
[短框弧完整joint](../c5_excess_two_mixed_core_four_spoke_short_arc.md)
排941最後六份共用框點，至14／18。最後不相交pairs分成：

- 933的4份、941的8份有一側全部incident faces短，原接線非critical。
- 兩候選各10份迫兩unary同在唯一共同兩段長框弧；原支援次序使跨度和≤2，
  criticality／短支援迫各至少二，固定一份原unary接線非critical。

只替換已證短的整份原unary，原C及另一unary逐點保持；只主張五角色
投影等式，不主張完整六角色joint等式。原shortsupport、crosscut、
完整tupleoperator各保留證據邊界，沒有新的跨列容量或palette假設。

因此整份四spoke(2,2)、mixed11+各側一unary子型排除，含root交換；
原47／75份由共用pair7／9、短face8／16、三段長face10／10、
crosscut8／16、共用短框弧0／6及本輪disjoint14／18覆蓋。
**ε≥3仍未證；其他incidence及雙root分支仍保留。**

## 固定證書與實際驗證

32原骨架各64rotations，恰兩份disk embeddings且faces集相同，
共2,048assignments／64disk rotations；另核對原apex rotation。
對前序原helper的96rotation assert不作修改，避免改變前序產物。
每份共同長face窮盡actual支援子集、原交錯paths與明示apex
subdivision；完整joint替換沿用前序字面原unary算子。
實際保存1,280支援對、80雙非短pairs全部不相容、60apex subdivisions；
32root swaps、12,800共同D₅支援對、3,200列搬運、1,400短face外路徑
搬運與600subdivision搬運核對。原47／75完整identity ledger綁定所有
六階段，確認無重複／遺漏，原necessarydomain與原spokeedges逐身份相同。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_arc.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

新crosscut、shortarc及disjoint三份checker兩hashseed重播通過；長face／shortsupport已在
同一turn重播通過。前序原完整degreeunary replacement payload沿用範圍
由新checker核對，不宣稱重建這些disjoint來源圖。沒有新增Lean theorem，
lake build不形式化本輪topology；未重跑degree-6全分拆、R系列、
歷史docs漂移audit、全倉來源catalogue、一般出口／Kempe closure或Lean axiom audit。

README、STATUS、Kempe導覽、整合頁與前序報告後續狀態同步；HANDOFF
線與tags未變，保持薄索引。新證書本地保留，MANIFEST／.gitignore
登錄producer、依賴及fingerprints。最終文件檢查通過510份Markdown／
5,242個本地links；anchors、index、handoff均通過，DocGraph為
62documents／213relations／5families、零errors／notes。Artifact
status=ok137，無missing／changed／stale，git diff --check通過。
同一turn的lake build通過8,831jobs，只見既有AttachmentOrder／SymRelabel
linter warnings；沒有Lean檔案變更，後兩份Python證書未重跑相同Lean build。
獨立紙面／程式審核及原root-swap actual支援對再核對均通過。

Disjoint新artifact=1,773,561bytes，SHA256
`e58e36b14e56730ddb422b80b9ec11b487e4c03f98402b66c9755c1bac61634c`。
Crosscut／shortarc原bytes與hash見各自紀錄；三份新產物本地保留。

## 精確停止點與貼用摘要

下一原incidence是mixed-(1,2)+a側一原unary，含root交換。
兩個b-contacts y₀,y₁是不同原頂點，允許x與其中一點相同；保留
原R_C(x,y₀,y₁)、R_U(u)、全部actualsupports與原六角色joint。
先核對一條原spoke省略後的core身份與原disk接線，再接回原relation。
Mixed22無unary、較少spokes、單省略、(5,5)q-core、多mixed／no-mixed、
非相鄰及unary側例外保留；共同下界ε≥2，ε≥3／來源實現／一般出口／
K∞=K≤5未證，最新停止點見[Kempe導覽](../c5_kempe_guide.md)。

```text
cwd=/home/ray/developer/ai/math；先讀HANDOFF/STATUS/Kempe導覽和git status。
HEAD=0e38127；本輪未commit/push，原短／長face未提交成果保持。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk、ε=2、相鄰雙degree5 roots。
四spoke(2,2)、唯一mixed(1,1)+各側一原單接點unary已整型排除，含root交換。
同輪crosscut新排8/16，shortarc再排0/6，最後disjoint14/18全排；原47/75全部覆蓋。
Disjoint分一側全部faces短4/8與同一兩段長框弧10/10，原criticality與跨度矛盾。
完整C/U/V、actualsupports及同框joint保持，只替換短原unary，原接線非critical。
checker：python3 scripts/c5_excess_two_mixed_core_four_spoke_disjoint_pairs.py --check。
下一mixed(1,2)+a側unary，保留原ternaryR_C(x,y0,y1)與原spoke省略core身份。
mixed(2,2)無unary／其他雙root分支保留；紙面+固定Python，ε≥3未證，無新Lean theorem。
```
