# 2026-10-03：ε=2 唯一 mixed 的兩側原 unary 省略全收

接手基準 `722bfa6`。使用者要求「繼續推進 ε ≥ 3」。先讀 HANDOFF、
STATUS、Kempe 導覽、即時 Git 與相關記憶，沿用
math-research-handoff-publish。保留全部前序未提交成果；本輪未用
Graphify 或 sub-agents，未 commit／push。
成果見 [專題報告](../c5_excess_two_mixed_core_two_unary.md)，目前停止點
由 [Kempe 導覽](../c5_kempe_guide.md)維護。

## 任意大小結論與證據界線

固定完整 Σ=933／941、Σ edge-minimal、induced-C₅ disk、ε=2、
相鄰雙 degree-5 roots，且恰一份原 mixed。在這些全部前提下，
兩側各省略一份原單接點 unary U、V，所得原圖必接受全部十列。
結合原省略身份表及雙 spoke／spoke＋unary 排除，所有 (4,4)
保留原 mixed 的 minimal rejected-row core 均不可能。若有 (4,4)
core，必恰只省略 incidence-(1,1) 的原 mixed。
**共同下界仍 ε≥2，未證 ε≥3；未新增 Lean theorem。**

反設省略圖拒絕 singleton q，連通 degree-4 飽和使它自己為 q-core。
原 mixed 形狀迫原 triangle z,w,x，且原 roots 不在路徑枝縮減區。
U、V 各保持任意大小、全部原附件及非空完整 endpoint relation。
先保留 core 的全部 root/contact tuples 與全圖 witnesses，再檢查
原 zu、wv 的兩條字面不等式；只有在此後才投影到聯合 root-pair
relation，不能相乘 root marginals。

兩份原固定支援各有自己的 local-shape 函數；跨列 transport
在同一四色框，每列對兩個變數給 binary constraint。全部 UNSAT
附精確 propagation proof，另一 verifier 直接重算可用 pairs；
全部必要相容者附完整 shape assignments，再對原 root-pair relation
核對十列接受／拒絕。自由 schedule 或相容 assignment 不宣稱實現。

僅為拓撲反證，共同收縮原互斥 U、V 為兩點，保留實際支援及
各自原 root 邊；不宣稱保持 unary 染色或 Σ。原 core 的 run minor
branch sets 與 U、V、B 互斥，故可在同一來源同步縮減。
每份具名實際支援對映至它包含的一份較小支援對，僅刪多餘支援邊，
不以較小支援重選禁色。全部較小必要圖的 boundary-apex 圖保存
明示 K₅／K₃,₃ subdivision paths，非 disk 反證沿 minor 傳遞。

## 固定必要域與完整控制

沿用 126 必要正常形、570 具名原 root 邊，不重開來源 catalogue。
933／941 各五像合計 5,700 次目標比較：

| 目標 | 已空必要列 | 任意雙 unary 仍接受拒絕列 | 固定支援階段 |
| --- | ---: | ---: | ---: |
| 933 | 570 | 1,084 | 1,196 |
| 941 | 1,140 | 773 | 937 |

2,133 個殘留的 2,184,192 次支援對必要比較中，2,083,333 次
跨列不相容；其餘 100,859 次同源雙收縮星非 disk，零殘留。
字面 root-pair relation／target 相同的查詢共享，實際 solver
執行 386,048 互異支援對查詢：368,859 UNSAT proofs、17,189
相容 assignments；全部 UNSAT 都只需 propagation，無分支。

每份 core 中去掉候選 mask 重複的相容支援對共 43,265 份；
3,180 份較小支援對證書覆蓋全部，**3,176 K₃,₃、4 K₅**。
全部 path 的實際邊、內點互斥、branch 頂點及九／十份鄰接獨立核對。

[Checker](../../scripts/c5_excess_two_mixed_core_two_unary.py)／
[artifact](../../artifacts/c5_excess_two_mixed_core_two_unary/observations.json)
保存原 core 完整邊、critical witnesses、contacts／attachments／support、
ownership、完整 joint tuples、接合算子、兩份固定支援 transport、
逐查詢 proofs／assignments、具名實際支援到 minor 的映射及 paths。

5,700 次 core／自由二 endpoint 算子與獨立全圖回溯一致，
1,282,500 次全部 15×15 非空 endpoint relations 的完整雙接合
通過。26 張原長圖保存原 components、contact tuples、附件及
branch sets，780 次跨縮減 root-pair 關係相等；不同 contact
座標不冒充跨縮減等價。64 張實際接上原 singleton／edge／path／
triangle unary 對的完整圖，640 次十列接合與全圖回溯一致，
兩份原 unary 及全圖的完整 coloring witnesses 明列。
這些控制不宣稱 disk、Σ-minimal 或任意 unary 分類。

負控制保存 form 0、原 roots (5,7)、target 934 的逐列自由禁色對：
列 3、4 為 (2,1)，列 6 為 (2,空)，其餘皆 (空,空)。它可在
算子中匹配目標，但不存在符合雙固定支援及 disk 必要 minor 的
同一原 U、V。不是來源實現。

## 實際驗證及未重跑範圍

以下均已執行；新 checker 兩種 hashseed 逐 byte 重播一致：

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check
python3 scripts/c5_excess_two_mixed_core_spokes.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
```

原雙 spoke checker 的 6,068 接回、242,720 原 spoke 子集比較、
26 原長圖重播通過。原 run 化約的 120 palette-switch、20 三-run、
8 第一段重複排除與八份兩-run 必要正常形通過。`lake build`
通過（8,831 jobs，僅既有 style／unused simp warnings），未形式化新報告。

新大型 artifact 為 107,665,331 bytes，已由 MANIFEST 及 generated
ignore 登錄；目前共 122 產物／117 producers。直接大型輸入為原
雙 triangle artifact，小型原枝／run 證書與 imported source hashes 明列。
報告、前序後續標記、README、導覽與 STATUS 一併更新；HANDOFF
研究線及 tags 不變，依薄索引規則保持原內容。

以下收尾檢查均通過：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

文件檢查：478 Markdown、4,945 local links，anchors／index／handoff
全通過。DocGraph：62 documents、213 relations、5 families，
0 errors／notes。Artifact status 為 `ok=122`，無 missing／changed／
stale；`git diff --check` 通過。

未重跑：原 spoke＋unary 全份 checker、177,280 triangle lifts 全分類、
triangle fork 全批、全 degree-4 Gallai 合成、唯一 degree-6 全分拆、
root 刪除／原 zw 接回其他分支、一般來源 catalogue、其他出口與
Lean axiom audit。沿用它們既有任意大小及有限 topology 信任界線；
新 checker 重驗實際採用的原 cores 與完整染色，不重證外部 degree-list 定理。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留前序未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、Kempe導覽及即時git status，
再讀docs/c5_excess_two_mixed_core_two_unary.md及本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk、ε=2只剩雙degree5。
相鄰mixed刪roots/zw全收。唯一mixed的(4,4)保留core已全排原省略身份：
雙spoke、spoke+原unary，以及本輪兩側各一原單接點unary U,V。
原省略圖G-U-V必全收Ω，含root交換；若有(4,4)core只能省略原mixed，incidences(1,1)。
126必要forms/570原root邊/5700目標比較；2133弱殘留覆蓋2184192支援對比較，
2083333跨列不相容，100859必要相容者全由3180雙收縮星K5/K3,3 subdivisions排除。
實際386048互異支援查詢/368859 UNSAT proofs/17189相容assignments；不宣稱實現。
1282500完整雙接合控制、26原長圖/780色對、64原雙unary圖/640十列比較通過。
完整root/contact tuples、同框full witnesses、原U/V supports/ownership保留。
兩個原unary只在拓撲minor反證收縮；較小支援只刪minor邊，不重選原禁色。
重播uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_two_unary.py --check，另hashseed17。
紙面+Python，無新Lean theorem；共同ε≥2仍未升為ε≥3。
下一窄題：恰只省略原mixed C(1,1)，保留C完整二接點relation及原G-C-zw兩側全圖relation，
全部實際支援與共同色框，再接回C/zw，不能相乘C marginals。
(5,4)/(4,5)、G自身(5,5)q-core、多mixed、no-mixed、非相鄰/unary側例外仍保留。
一般出口、來源實現及K∞=K≤5仍未證。
```
