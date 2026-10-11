# 2026-10-03：ε=2 單 triangle 保留原兩點接回排除

接手基準 `722bfa6`；工作樹已有原 root 刪除、原路徑 K₅ 的未提交
bundle，完整保留。使用者要求「繼續推進 ε ≥ 3」。先讀 HANDOFF、
STATUS、Kempe 導覽、Git 及原停止點報告，選定相鄰 mixed、原 N=G−zw
仍拒絕、N 的全 degree-4 內部是單 triangle 加原樹枝的窄問題。
使用 math-research-handoff-publish 工作流程，未使用 Graphify、
sub-agents，未 commit／push。成果見
[專題報告](../c5_excess_two_triangle_edge.md)，當前停止點由
[Kempe 導覽](../c5_kempe_guide.md) 維護。

## 任意大小推進

沿用原 N 的 minimality／degree-4 飽和、triangle 接枝、路徑枝正常形
及第一分叉排除。零枝沒有原 nonedge 可接回；原樹枝不分叉且至多
兩枝。十八份 canonical lifts 留下原附件序列 X^(2a+1),leaf，或
八份單枝 contexts 的 X,Y^(2a),leaf。原枝每點都有 b₄ 與其他框附件。

同枝 z,w 的原中間路段與原 zw 給環，以 z／中段／w、b₄、外側
apex 加其餘 B 直接給 K₅。其他兩點配置每枝至多一個 marker：
將 marker 前後的未標記同附件區段縮成零、一、二點，分別保持空、
奇正、偶正長度；marker、triangle、leaf 保留。局部 |S|≥2 的原
區段傳遞保留兩側端點完整關係，逐段拼回便保留原 z,w 的十列
完整有序色對。兩個 markers 的 branch sets 是 singleton；不能用
舊 boundary／bridge 縮減代替這份新聯合等價。

固定必要域只有 528 份正常形：320 單-run triangle／枝、136 兩-run
triangle／枝、72 跨枝。接回 Σ histogram 為 894:52、990:32、1018:52、
1022:392；全部 392 份 T4 全收者都保持原單缺失，原 zw 沒有完整 Σ
增益。連同前兩輪樹與雙 triangle，刪 zw 仍拒絕的相鄰 mixed 全分支
排除，得到 **ε=2 相鄰 mixed 必有 Σ(G−zw)=Ω**。共同下界仍 ε≥2。

沒有把各列的不同 witnesses 合成一份共同染色，也沒有把原 multi-contact
關係換成 marginals。這次縮減明列原頂點到目標的 branch sets；其他
原 contacts 可以落在被縮區段，沒有聲稱每個原接點都單獨保持為目標點。
來源的完整分量／contacts／ownership／attachments 持續保存。

## 固定證書及實際研究重播

[Checker](../../scripts/c5_excess_two_triangle_edge.py)／
[artifact](../../artifacts/c5_excess_two_triangle_edge/observations.json) 保留十八份
基底的原邊、全部附件、apex rotations、逐邊 q-critical witnesses，
並由原邊集重算十列 Σ；八份兩-run contexts 同樣核對實際接線。

528 份正常形的 5,280 次完整有序色對查詢由 DP 與原邊集的獨立
完整回溯比較，接回後另直接回溯核對同 tuple 異色過濾。每份正常形
另把每個正未標記區段加長兩點，保存原長圖、原 marker 位置、全
原分量、目標映射及完整原長圖 tuple witnesses。共 528 個保留
marker 的固定縮減，19 張長圖的 3,040 次獨立 pinned 回溯核對全部
16 個有序色對及空纖維；最長原圖包含五框點共有 28 頂點。

十一份可用色集的 1,408 次 endpoint 控制另區分空段與正偶段。
26 張同枝原圖的 280 次原 nonedge 接回都有明列 K₅ branch sets，
且另保留 2,800 次完整色對查詢。實際圖的 marginal 負控制保留
K={(0,0),(3,3)} 與原圖／列／witness：兩個端點 marginals 相同，
相乘卻誤造原 relation 沒有的異色對。

```bash
python3 scripts/c5_excess_two_triangle_edge.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_triangle_edge.py --check
python3 scripts/c5_excess_two_path_edge.py --check
python3 scripts/c5_excess_two_root_deletions.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_forks.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

新 checker 兩種 hashseed 及兩個前輪 checker 全通過逐 byte 重播。
Path reduction 的 120 palette-switch、20 三-run、8 第一段重複原
minor 及八份兩-run 正常形重播通過；fork checker 的 90,112 lifts／
88 份 subdivisions 重播通過。`lake build` 通過（8,831 jobs，只有
既有 style／unused simp warnings），未新增 Lean theorem。

文件檢查通過（472 Markdown、4,882 local links）；DocGraph 通過
（62 documents、213 relations、5 families，0 errors／notes）。大型
產物完整性 `ok=119`，無 missing／changed／stale；`git diff --check` 通過。

新 artifact 為 15,364,827 bytes，按既有大型產物規則登錄 MANIFEST／
generated ignore；登錄共 119 份產物、114 個 producers。專題、導覽、
STATUS、README 的 excess 入口及前兩輪後續標記一併更新。
HANDOFF 研究線與進行中 tag 未變，依薄索引規則保持原內容。

十八份 canonical 的 177,280 lifts 全分類、全 degree-4 Gallai 合成、
唯一 degree-6 全批、來源 catalogue、全部 mixed／no-mixed 出口及
Lean axiom audit 沒有重跑；本輪直接驗證所用十八份基底與八份正常形，
完備性沿用其紙面／有限 topology 信任範圍。沒有新增外部文獻 oracle
或 disk 實現結論。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留原兩輪未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、c5_kempe_guide與即時git status，
再讀docs/c5_excess_two_triangle_edge.md及本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk，ε=2只剩雙degree5。
新增：單triangle加任意原樹枝，刪原zw仍拒絕的最後一型全排。
同枝原環給K5；triangle/枝與跨枝原兩點用保留markers singleton的區段縮減。
528必要正常形，392份T4全收者均保持原單缺失，違反zw的完整Σ minimality。
528原長圖縮減、3040獨立pinned查詢、280原K5與全部tuple witnesses保存。
連同樹/雙triangle，ε=2相鄰mixed必有Σ(G−zw)=Ω；共同ε≥2仍未升為ε≥3。
重播python3 scripts/c5_excess_two_triangle_edge.py --check，另hashseed17。
紙面+Python，未新增Lean theorem。原contacts若被縮有明列branch sets，
不聲稱全部原contacts都留作目標獨立座標，不使用marginals或分量獨立S4。
下一窄題：相鄰恰一原mixed且N=G−zw全收，拒絕列完整K只含對角線，
核對所有minimal q-cores保留zw後的原省略身份及root degree。
Proper core至少一root降4；(4,4)若保留mixed只能是共用單接點。
若G本身是q-core，雙roots均degree5仍保留，不能套唯一degree5分離定理。
全收的多mixed、no-mixed、非相鄰roots與原unary側例外仍保留。
```
