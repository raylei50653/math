# 2026-10-03：ε=2 唯一 mixed 的原 leaf 色纖維與五-spoke 排除

接手基準 `722bfa6`，工作目錄 `/home/ray/developer/ai/math`。先讀
HANDOFF、STATUS、即時 Git、單 spoke 原附件報告、非相鄰 two-spoke
分離及相關記憶，使用 math-research-handoff-publish。保留前序未提交
bundle；未用 Graphify／sub-agents，未 commit／push。
成果見 [專題報告](../c5_excess_two_mixed_core_leaf_fibers.md)，目前停止點
由 [Kempe 導覽](../c5_kempe_guide.md)維護。

## 新結論與證據界線

固定完整 Σ=933／941、Σ edge-minimal、指定 induced-C₅ disk、ε=2、
相鄰雙 degree-5 roots、恰一份原 mixed，其餘內點完整 degree 四。
前輪941剩下四組五-spoke附件及 root交換，共八份有序支援；一次
整圖 boundary 搬運後全成 a-spokes=123、b-spokes=14、q₄=01012。
完整候選像只餘998／1004，分別拒絕 singleton {1,2,4}／{1,3,4}。

同色原 spoke a1／a3 省略圖自己都是 minimal q₄-core；原 C+a 在
五邊形側，原 unary U 在四邊形側。leaf a 的 slack query 迫原
S_U(q₄)={0}。保留原 (b,a,y,u) full joint tuples，接回原 spoke
恰過濾 a≠β_e；不把相邻列延拓直接當原來源接受列。

在 q₃=01021 與 q₂=01201，a 被原三 spokes 固定為3，b只餘0／2。
同一 C 的全部實際附件作 (0 2) 完整換色，同一 U 的支援則字面
相同。兩個原目標在 q₂、q₃ 接受性不同，迫 S_U(q₃)=S_U(q₂)={0}。

新任意大小 unary 引理排除 S_U(q₄)=S_U(q₃)={0}：固定 b=0，
兩份 tight Gallai palettes 在同一原 block incidence 上保留0／3
membership；q₃ 的奇圈 palettes={2,3}，故q₄的原奇圈 palettes
只能是{1,3}／{2,3}，不含0。每個原圈點的0／h方向沿原bridge
到原外部端點；b–b_other–b₀ 與另一框點構成兩 hubs，三圈 arcs
給原圖 K₅ minor。任意U大小、圈數及bridge長度均由紙面覆蓋。

因此 **941五-spoke全排，933／941原總spokes都≤4**。
**共同ε≥2不變；單 spoke 省略尚未全排，ε≥3未證，沒有新Lean theorem。**
沒有一般來源實現或新的圖 catalogue；沿用外部 degree-list 定理、
前輪 all-degree-four／two-spoke 區域與連通外框 K₄／actual-tether 引理。

## 完整證書與原圖控制

[Checker](../../scripts/c5_excess_two_mixed_core_leaf_fibers.py)／
[artifact](../../artifacts/c5_excess_two_mixed_core_leaf_fibers/observations.json)
保存八份具名 frame 搬運及全部十列共同色置換、28份完整joint代數、
五種原block palette選項與八份degree-4圈點方向身份。24份明示
K₅ extracted-shape控制逐邊核對互斥連通branch sets與十份鄰接。
它們不是完整degree-4來源或disk witnesses；不從有界控制外推引理。

十五張固定全圖保存同一C、U、原 contacts／ownership、全部實際
附件、K有序(a,y) relation與完整(b,a,y,u) tuples，各附原全染色。
**450次**完整joint接合與獨立全圖窮盡相同；**7,200次**固定(b,a)
的完整(y,u)色纖維與獨立pinned回溯相同，包含空纖維。非空M被
原spoke全濾空及共鄰contact marginals誤造tuple的控制均保存。
三張圖確有雙列U singleton0，附各自實際原圖K₅，明示其非disk性。

新 artifact 為 **2,397,122 bytes**；MANIFEST／generated ignore 登錄，
共125份大型產物／120 producers。新producer依賴前輪單spoke
artifact；保留前序成果。README、STATUS、導覽及前輪後續標記更新。
HANDOFF的研究線與tags未變，依薄索引規則保持原內容。

## 實際驗證與未重跑範圍

新checker預設hashseed與17逐byte重播均通過：

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
```

直接前序原附件及 actual-tether／K₅ 層重播通過：

```bash
uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_single_spoke.py --check
uv run --with networkx==3.5 python scripts/c5_two_spoke_adjacent_21.py --check
lake build
```

單spoke前序重驗666骨架／58 subdivisions、全部112五-spoke原身份
及60接合／960pinned控制，保留其原必要殘餘artifact，不修改舊查詢
flag冒充新層排除。Adjacent層重驗48 K₅控制、240列／480完整
relation控制、3,840 joins。lake build通過，8,831 jobs，僅既有
linter warnings；沒有形式化新palette比較、block incidence或topology。

文件、DocGraph、artifact及whitespace收尾命令：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

上述收尾檢查均通過：484 Markdown／5,005 local links，anchors、
直接索引及HANDOFF無錯；DocGraph為62 documents／213 relations／
5 families，0 errors／notes；artifact status為ok=125，沒有missing、
changed或stale；git diff --check無輸出且exit 0。

未重跑：前序完整mixed省略／雙unary／spoke＋unary大型checker、
一般全degree-four分類、nonadjacent／middle／reflection／split-support
全批、唯一degree-6各分拆、root／zw刪除全批、一般來源catalogue、
其他出口及Lean axiom audit。新Python不重證外部Gallai定理或任意
大小幾何來源 lemma；paper dependencies hashes明列。

## 跨對話接手摘要

```text
工作目錄 /home/ray/developer/ai/math；基準722bfa6，保留前序未提交bundle，
本輪未commit/push。先讀HANDOFF、STATUS、Kempe導覽及git status，
再讀docs/c5_excess_two_mixed_core_leaf_fibers.md與本輪history。
固定完整Σ933/941、Σ edge-minimal induced-C5 disk、ε=2相鄰雙degree5、
唯一mixed，全部(4,4)拒絕核心已排。單原spoke省略若拒絕，
省略圖自己就是唯一degree5 minimal core。前輪941五-spoke的四組
附件及root交換本輪全排：共同搬到a123/b14、q4，Σ像998/1004。
保存(b,a,y,u)完整joint relation、原leaf色纖維與原C/U完整witnesses。
q3/q2完整同源接合迫U在q4/q3都只取0；兩份tight原block palettes
保留0/3 membership，q4原奇圈palette不含0，actual tethers與原框邊
給K5。故933/941原總spokes都≤4。450全圖接合、7200 pinned纖維、
24 extracted K5與3張實際双列singleton0非disk原圖控制全核對。
下一窄入口：四-spoke (3,1)及root交換，先固定mixed(1,1)加一-spoke側
兩份原單unary，刪三-spoke側同色spoke的t=1,(2,1,1)core；保存原leaf、
C及兩unary的完整joint relations、actual attachments、同一frame再接回。
其他四/較少spokes、原unary單省略、G自己(5,5)core及其他來源分支保留。
單spoke省略尚未全排；共同ε≥2不變，ε≥3未證，紙面+Python，未Lean化。
重播：uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_leaf_fibers.py --check
```
