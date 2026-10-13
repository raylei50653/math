# 2026-10-03：ε=2 唯一 mixed 的原省略身份與雙 spoke 核心排除

接手基準 `722bfa6`，保留原 root 刪除、原路徑 K₅、單 triangle 接回
的未提交 bundle。使用者要求「繼續推進 ε ≥ 3」。先讀 HANDOFF、
STATUS、Kempe 導覽、Git 與相關記憶，再選定現行唯一 mixed、
N=G−zw 全收分支的 proper core 原省略身份問題。
使用 math-research-handoff-publish 流程，未用 Graphify 或 sub-agents，
未 commit／push。成果見 [專題報告](../c5_excess_two_mixed_core_spokes.md)，
當前停止點由 [Kempe 導覽](../c5_kempe_guide.md) 維護。

## 任意大小進展及精確結論

Degree-4 飽和使每份原分量只能全取或全不取；minimal q-core 已必
保留原 z,w,zw，每個 root 至多失去一條原 incidence。
Proper core 的所有原省略身份因此窮盡為：降一側 degree 時省略該側
一份原單容量因子；兩側都降四且保留 mixed 時各省略一份原單容量
因子；若省略 mixed，必恰只省略 incidence=(1,1) 的原 C。
若兩 roots 都仍五，core 就是整張 G，該雙 root 缺口維持。

保留 mixed 的 (4,4) core 是全 degree-4，迫原 contacts 共用 x，
z,w,x 成原 triangle。C 必從 x 起為一條原路徑，或 x 經直接 bridge
接另一 triangle；原 C 及其完整附件沒有被換成新 singleton。
兩側各省略一條 spoke 時，所有分量都仍在，G 恰為原 core 的雙
spoke 接回。既有枝分類及局部奇偶傳遞保持全部原 triangle／root
聯合 relation，即使刪 zw 也成立；所有原 spokes 都作用於仍具名
的 triangle roots。

126 份固定必要正常形、570 份具名原 root 邊、6,068 次雙 spoke
接回，全無 933／941 的十個目標 D₅ masks。因此該 proper core
的兩個原省略因子至少一份必是原單接點 unary。
任意大小覆蓋是紙面分類／傳遞合成；新 Python 證固定完整必要域，
沒有新增來源圖 catalogue、disk 實現判定或 Lean theorem。
**共同下界仍 ε≥2，尚未證 ε≥3。**

## 證書及已執行研究驗證

[Checker](../../scripts/c5_excess_two_mixed_core_spokes.py)／
[artifact](../../artifacts/c5_excess_two_mixed_core_spokes/observations.json) 保存
196 份整數身份配置的 7,442 個子集核對；它們沒有圖或支援實現宣稱。
圖層重用十八份原單 triangle、八份兩-run contexts、由八十份裸
triangle 重算所得的 36 份 T4 必要支援，及由 128 份原雙 triangle
lifts 重算 Σ 後選出的 64 份 q₄ 核心，不把保存 Σ flags 當作 oracle。

每個 root/contact joint tuple 保存同一原邊集的完整 coloring witness，
共鄰 contact 只有一個座標；先作原 spokes 過濾及原 zw 異色過濾，
再投影 root pair。6,068 接回的 60,680 十列查詢與完整回溯相等，
四個原 spoke 子集另有 242,720 次完整回溯比較。3,466 份 T4 全收
者的 N 都全收，G 的 Σ 為 942:70、956:36、958:306、1006:122、
1012:70、1014:122、1020:306、1022:2,434。放寬域仍含其他三拒絕型，
不宣稱所有接回至多兩拒絕，也未替它們證 disk 或 Σ-minimality。

26 張固定原長圖（最長含五框點共 16 頂點）保存原完整分量、所有
contacts／attachments／support、run 原順序、收縮 branch sets、
兩個 singleton 原 roots。780 次長圖完整 root-pair 比較及 8,720 次
逐列接回比較相等；長圖與短圖各自保存完整 contact relation，跨
縮減只宣稱 triangle／root relation 保持。
實際 marginal 負控制的 N 色對是 {(2,2),(3,3)}，兩側 marginals
相乘會誤造 (2,3),(3,2)，而加入原 zw 後精確 relation 為空。
完整圖、兩條原 spokes、該列及兩份全圖 witnesses 都保存。

以下已執行並通過：

```bash
python3 scripts/c5_excess_two_mixed_core_spokes.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_spokes.py --check
python3 scripts/c5_excess_two_triangle_edge.py --check
python3 scripts/c5_excess_two_root_deletions.py --check
uv run --with networkx==3.5 python scripts/c5_triangle_path_reduction.py --check
lake build
```

新 checker 兩種 hashseed 逐 byte 重播通過；單 triangle 前輪 528
必要正常形／392 T4、528 原長圖、280 原 K₅ 控制通過；root 刪除
前輪 512 接回、400 原條件分量 relation、60 刪 root 等式通過。
Path reduction 重播 120 palette-switch、20 三-run、8 第一段重複
排除及八份兩-run 正常形通過。`lake build` 通過（8,831 jobs，
僅既有 style／unused simp warnings），沒有形式化本輪新結論。

新 artifact 為 113,696,727 bytes，已按大型產物規則登錄 MANIFEST
及 generated ignore；manifest 共 120 份產物、115 個 producers。
專題、導覽、STATUS、README excess 入口與前輪後續標記一併更新。
HANDOFF 研究線及進行中 tag 未變，依薄索引規則保持原內容。
文件檢查通過（474 Markdown、4,902 local links）；DocGraph 通過
（62 documents、213 relations、5 families，0 errors／notes）。大型
產物狀態 `ok=120`，無 missing／changed／stale；`git diff --check` 通過。

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

未重跑：單 triangle 的 177,280 lifts 全分類、triangle fork 全批、
全 degree-4 Gallai 合成、唯一 degree-6 全分拆、來源 catalogue、
全部 mixed／no-mixed 出口及 Lean axiom audit。
其任意大小分類及有限 topology 完備性仍在既有信任界線內；新
checker 核對實際用到的原基底、兩-run contexts、完整 tuple 染色，
沒有重新證明所有 topology 前序或外部 degree-list 定理。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留先前未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、c5_kempe_guide與即時git status，
再讀docs/c5_excess_two_mixed_core_spokes.md及本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk，ε=2只剩雙degree5。
相鄰mixed的刪roots/zw均全收；本輪聚焦恰一原mixed、N=G−zw全收。
新增proper core完整原省略表：degree損失各至多1，整份原C取捨。
(4,4)保留mixed迫原共鄰triangle z,w,x；C為原路徑或x接第二triangle。
兩側各省略spoke的126必要正常形、570原root邊、6068接回全無933/941五像。
所以這型兩省略因子至少一份是原單接點unary；共同ε≥2仍未升為ε≥3。
60680十列查詢、242720原spoke子集查詢、26原長圖/780色對/8720接回保存。
每圖完整root/contact tuples、同框full witnesses、contacts/attachments/ownership保存。
縮減只保原triangle/root relation，不聲稱全部原contacts留作目標singleton。
重播python3 scripts/c5_excess_two_mixed_core_spokes.py --check，另hashseed17。
紙面+Python，未新增Lean theorem；lake build通過。
下一窄題：(4,4)仍保留原mixed，省略一條原spoke及一份原單接點unary V，
含root交換；固定原z,w,x，保留V任意大小、附件及非空完整endpoint relation。
兩unary省略、只省略mixed、(5,4)/(4,5)、整圖(5,5)q-core仍未排除，
不能把唯一degree5的M相鄰列分離升成G的完整Σ分離。
多mixed、no-mixed、非相鄰roots/unary側例外、一般出口與K∞=K≤5仍保留。
```
