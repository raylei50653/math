# 2026-10-03：ε=2 t=0 全部分拆與唯一 degree-6 分支排除

**後續發布（2026-10-03）**：本輪與前序 t=3 的完整證據包一併整理
提交推送，見 [發布紀錄](2026-10-03-excess-two-degree-six-publish.md)。
下文保留研究當時的未提交語境；即時發布狀態以 Git 為準。

接手基準 `4701f4c`；工作區已有上一輪 t=3 的未提交 checker、artifacts、
報告及入口更新。使用者要求「推進 t = 0」。先讀 HANDOFF、STATUS、
Kempe 導覽及 Git，確認前序 t=1、2、3 已完成，唯一 degree-6 root
僅剩無 spoke 的六原接點。本輪保留接手時變更，沒有 commit／push。
成果及任意大小證明見 [t=0 全分拆報告](../c5_excess_two_no_spoke_complete.md)。

## 成果與證據界線

來源前提是完整 Σ 為 933／941 或整圖 D₅ 像、每條非框邊 Σ-critical、
induced-C₅ disk 外框、ε=2、唯一完整 degree-6 root、其他有效內點
完整 degree 四。原 H−r 分量、有序六接點、全部附件、實際支援、
ownership、環序及同一字面色框保留。t=0 十一種原分拆全排：

| 原分拆 | 紙面機制／固定控制 |
| --- | --- |
| (6) | 四 palettes 迫正 K₄、負 bridge；完整 degree 飽和，六葉迫兩原 K₄ 與單 bridge，原六 contacts 給 K₅。432 份完整六接點 tuples、864 刪 contact lifts、16 palette 型／52 incidence 型及負控制 |
| (5,1) | 另一原分量的真實外路徑恢復原五接點三 palettes 的 K₅，容量≤2 加 unary≤1 不足四色；40 份零-spoke 外部原 unary 路徑 K₅ |
| (3,3) | 另一原分量恢復三接點兩禁色 K₅，每份容量≤1 |
| 七種至少三分量分拆 | 完整 Σ 私有 contact 見證、真實外路徑及原短支援迫每份 span≥2；共同 annulus 區塊總 span≤5，六跨度矛盾；480 份零-spoke two-hub lifts |
| (4,2) | 20 份具名環狀包絡、200 queries 的同源 S₄ profiles 先留 7,200 份；160 組原 binary 拒絕列 pair schemas，各含 45 份 profiles，共同袋支援全有兩框弧 K₅ |

單分量 (6) 不假設外部 hub 或 K₄-free，獨立用原圖 K₅ 排除。
多分量的非空 boundary 支援由完整 Σ 刪 contact 的私有色見證及
T4 全收證成；不依賴每列 q-minimality。短支援引理原先額外假設
直接 spoke，其唯一用途是 K₄ 排除的外部連通 hub；真實外路徑 L
可直接替代。原報告增加有日期的適用範圍說明，舊 checker／產物不改。

(4,2) 保留完整四接點 relation，只對原兩接點分量使用 binary
路徑及全部原袋。實際外部 anchors 僅取另一四接點分量的兩個
真實包絡端點；不新增 spoke 或把包絡內部虛構為附件。每份同源
profile 由全部十列共同 equality classes 決定。180 queries 在此層
已空，20 queries 各有 360 份抽象資料。所有原拒絕列的 binary
pair queries 共用唯一原 bridge 路徑及固定袋支援；每個共同族都
非空，排除來自同一份連通框弧 witness，而非空 relation 誤報。

逐袋族以直接 24 置換獨立核對，框弧分割以 connected subsets／
刪框邊兩法重算。20 份 geometry 另以所有 directed cyclic arcs 的
開框邊 masks 互斥重算。160 份來源證書全部是 common-two-frame-arcs
K₅，不需四接點 active forest、首橋、D 身份或原省略全收。每個
schema 的 profile digest、multiplicity 及每 query 的完整代表保存；
沒有把四接點 pair 強制含 D，負控制保存其各種 membership 模式。

完整七接點代數核對 4,096 singleton fibers 及 5,480 份所選完整
relation pairs；原 contacts 的座標不合併。相同四接點 marginals
在同一 binary relation 下，root projections 分別為 {2,3}、U，
確實不能乘 marginals。一般完整 relations 的涵蓋由 singleton
ordered-tuple fibers 的聯集恆等式承擔，而非所選 finite relation
families 的大小。Reduction 的另一 marginal 碰撞為空 root join／U。

獨立審閱分別核對無 spoke 外部 hub、完整 Σ 私有見證、(6) 的
四 palettes／飽和 K₄、五接點任選三禁色與二框弧 Z 包含原 C₄
的適用前提；沒有發現阻擋問題。本輪重讀外部
[Dvořák 講義 Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
確認 degree-list／Gallai 前提。任意大小來源化約、共同 τ、真實
tethers 及 Jordan 次序由紙面和明列前序依賴承擔，Python 只證
固定必要域、具名 minor skeletons 及完整 relation 代數。

所以 t=0、1、2、3 全排，T4 又迫 t≤3，完成唯一 degree-6 root
的 ε=2 分支。同一來源若 ε=2，必有兩個完整 degree-5 roots。
兩 roots（含 mixed、相鄰／非相鄰）仍保留，不能推 ε≥3；一般
來源、一般單側／共同出口與 `K∞=K≤5` 未證，未新增 Lean theorem。

## 本輪實際重播

新增兩 checker 生成各自產物，重播命令如下：

```bash
python3 scripts/c5_excess_two_no_spoke_reduction.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_spoke_reduction.py --check
python3 scripts/c5_excess_two_no_spoke_four_two.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_spoke_four_two.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_excess_two_five_contact.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

上述新增 checker（含 hashseed17）及四個沿用 checker 均通過。
`lake build` 通過（8,831 jobs，既有 style／unused simp warnings）；
文件檢查通過（465 Markdown、4,799 local links），DocGraph 通過
（62 documents、213 relations、5 families，0 errors／notes），
`git diff --check` 通過。

原 `uv run` 因 sandbox 的 `/home/ray/.cache/uv` 唯讀而不能建立 lock。
改用既有 pinned `.venv/bin/python tools/artifacts.py status`，其 Python
3.14 與 requirements 的版本檢查及全部 manifest audit 通過：`ok=116`。
無缺檔、changed 或 stale，未修改依賴／cache 或 artifact manifest。
新增兩份 JSON 分別為 369,116 bytes（reduction）、800,759 bytes
（four/two），每份均小於 1 MB，不需加入大型產物 manifest。

Reduction 核對 864 刪 contact lifts，實際保存 24 份代表（各36份的
count）及全 432 tuples／染色 witnesses，全部 lifts 可重建。
原 HANDOFF 的線索引及進行中標記維持，停止點更新於 Kempe 導覽；
README 與 STATUS 的入口／直接索引同步。接手時 t=3 成果的正文保留，
加上後續涵蓋說明；沒有覆寫其原生成證書。

未重跑前序 t=1、2、3
全批 checkers、歷史 source catalogue、全部 degree-4/Gallai 有限證書
或 Lean axiom audit；`lake build` 不把新紙面 topology 提升為 Lean theorem。

## 接手摘要

```text
工作目錄 /home/ray/developer/ai/math；本輪 t=0 完成，尚未 commit／push。
先讀 docs/HANDOFF.md、docs/STATUS.md、docs/c5_kempe_guide.md，再讀
docs/c5_excess_two_no_spoke_complete.md 及本研究紀錄，查即時 git status。
來源：完整 Σ 933/941 或 D5 像、Σ edge-minimal、induced-C5 disk、ε=2，
唯一 degree-6 root、其餘有效內點完整 degree4。無 spoke 十一分拆全排；
連同 t=1/2/3 及 T4 上界，完成唯一 degree6 的整條 ε=2 分支。
(6) = 飽和兩K4+原bridge 的 K5；(4,2) = 20 geometry/200 queries，
7200 同源弱 profiles 由160 原 binary pair schemas 的兩框弧 K5 全排。
重播 scripts/c5_excess_two_no_spoke_reduction.py --check 及
scripts/c5_excess_two_no_spoke_four_two.py --check，另各用 hashseed17。
停止於紙面+Python，不是 Lean 新 theorem；ε≥2 仍不能提高為 ε≥3。
若 ε=2，只剩兩個 degree5 roots。下一窄入口先核對相鄰型的既有共同
分離對兩候選完整Σ的適用前提；保留 mixed/no-mixed、原接點、附件、
所有同源完整 relations 及同一字面色框，不重開圖 catalogue。
```
