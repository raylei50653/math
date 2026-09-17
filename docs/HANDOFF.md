# 新對話交接：四色 boundary-state／constraint gadget 研究

更新：2026-09-17。工作目錄 `/home/ray/math`。**新對話先讀本文件，再依需要讀分階段報告；不要從零重跑已完成的搜尋。**

## 研究路線總覽（2026-09-15 文件整理）

新增 [C5 boundary relations：有界代表與特殊反例路線](c5_boundary_relations.md)。
區分待證主命題 `K∞=K≤5`、與它等價的全域較小代表存在性，以及指定局部規則的
額外完備性要求；§5.1 對照既有 screen、completion、Lean 代數與 B₅ face 的實際進度。
此總覽整理主命題與證明路線；最新研究成果與停止點以下節為準。

## 最新研究：四內點核心與無界 odd-path 家族（2026-09-17）

報告：[四內點最小阻礙](c5_four_vertex_cores.md)。候選 A 一般三出口仍未證。
接續 list-critical 化約，完整核對四有效內點的六個連通內部形狀與所有可用 lists，
只剩 P4、diamond、K4 共 18 組 minimal list assignments。
展開 boundary attachments 得 4,965 個模板，200 個 disk，其中 100 個接受全部 T4；
100 個都只拒絕指定 singleton。模板含 automorphism 重複，不是不重複圖數。
因此，若候選 A 的某單側出口失敗，該側每個 minimal obstruction 至少五個有效內點。
這是紙面化約加 Python／NetworkX 核對的條件式結論，未新增 Lean theorem。

100 個 disk/T4 templates 的同色 boundary quotient 都是 `K2 ∨ C5`。
另找到可反覆延長的 P4 core：用帶兩個共同 boundary 鄰居的三邊路徑替換一條邊，
保持 disk、單缺失 relation 與逐邊 minimality；得到 k=4,6,8,… 的無界家族，
quotient 為 `K2 ∨ C_(k+1)`。任意 k 由紙面歸納，計算另核對 k=4、6 及局部 patch。
因此一般 T4 disk 最小阻礙不能假定有固定內點上限；這些單缺失圖不是候選 A 反例。

**下一個窄問題：** 對任意 `K2 ∨ C_(2m+1)` 型 boundary-color quotient，
disk＋全部 T4 能否保證 minimal obstruction 只缺一個 singleton？先研究整個
無界 odd-cycle 家族的分離性，不直接擴大 k=5 枚舉。不假定所有 cores 都是此型。
共同 pivotal edge 仍是獨立問題。

**接手順序與停止範圍：** 先讀新報告 §3 的同色 quotient，再讀 §4 的局部替換引理，
最後處理 §5 的整個 odd-cycle 家族分離問題。先固定 missing singleton q，明確列出
三個 boundary 色類在 `K2 ∨ C_(2m+1)` 中的位置及其拆回有序 C5 的 attachments；
不要假設同色識別保存平面性，也不要假設 p、q 共用完整 coloring。
四內點分類已完成；不重跑舊全量 audit，不自動擴大 k=5 枚舉。沒有背景研究工作。

重播：`uv run --with networkx==3.5 python scripts/c5_four_vertex_cores.py --check`，
另跑 list-core checker、`lake build` 與文件檢查。兩輪 scripts、證書、報告與入口文件
一併納入本次發布提交。
驗證通過：兩個 checker、`lake build`（8,820 jobs）、142 個本地連結及 whitespace。

以下前輪段落保留研究歷史；其中的「下一個問題」以本節最新停止點為準。

## 前輪研究：list-critical cores 與小阻礙分離（2026-09-17）

報告：[list-critical cores 與小阻礙分離](c5_weak_list_cores.md)。
候選 A 未證。本輪紙面分類了至多三個有效內點的 minimal singleton obstruction：
只能是同一單色 list 的內部邊，或同一兩色 list 的內部三角形。
固定 boundary、只商內點置換共 190 個模板，35 個 disk，其中 25 個接受 T4；
這 25 個全部只拒絕指定的一個 singleton。完整 relations、逐邊 minimality 和
boundary-apex planarity 已核對；分類及 apex/disk 等價屬紙面，計算未進 Lean。

**條件式進展：** 任意大小來源 G 若有至多三有效內點的 minimal q-obstruction，
就有只釋放 p 的出口。故單側出口失敗要求該側所有 minimal obstructions 至少四個
有效內點。一般 minimal obstruction 的有效內點 degree≥4；degree-4 點誘導
Gallai forest（紙面推論，引用 degree-choosability 定理）。共同出口仍未處理。

只在兩 patterns 改色頂點的 star 刪邊，五個舊代表都只能共同釋放，故這種局部化不足。
另測一個代表的 22 次 disk vertex splits：13 個保留 relation，但全是 degree-3
附加點，兩側核心仍為舊三角形；106,496 個 subset 核對，不算非平凡域外支持。
未跑 k=4 全圖搜尋，未重播舊全量 audit，未新增 Lean theorem。

**下一個窄問題：** 找或排除四個有效內點的 minimal q-obstruction，它接受 T4
卻同時拒絕相鄰 p。先按 degree/list 與 Gallai 結構分型；找到這種 core 只反駁
較強的逐-core 分離猜想，尚不自動反駁候選 A，因可能有其他可分離的 cores。

重播：`uv run --with networkx==3.5 python scripts/c5_weak_list_cores.py --check`。
另重播 flow-repair、critical-core、candidate、quotient checkers；驗證細節見新報告。
上述五個 checker、`lake build`（8,820 jobs）、136 個本地連結與 whitespace 均通過。
本輪產物與四內點後續成果一併納入本次發布提交；原四內點問題已由上節完成。

## 前輪研究：repair sets、dual flows 與非同面控制（2026-09-16）

報告：[repair sets、dual flows 與非同面控制](c5_weak_flow_repairs.md)。
候選 A 未證；三出口已有 deletion-side 精確充要條件。對每個缺失 pattern r，
令 R_r 是 inclusion-minimal 的刪邊修復集。單側 p 出口 iff 某個 p-repair
不包含任何 q-repair；共同出口 iff 兩 repairs 共享最後邊 e，且它們的 union−e
尚不包含任一側 repair。

固定 disk drawing 後，四色寫成 F₂²；primal edge 色差是 plane dual flow。
repair sets 恰是相應 boundary demand flows 的 minimal zero-edge sets。
相鄰 p,q demands 只在 outer dual vertex z 的兩條相鄰 edges 上相差同一非零量。
因此剩餘缺口已成為明確的 plane-dual 5-pole flow-repair intersection lemma。

新增負控制由兩個單缺失 K5 obstruction 沿 C5 分置兩側組成。聯集是平面圖且
relation 仍為 Ω\{p0,p1}，但 repair families 互斥，W 只有兩個單側出口、沒有 Ω。
其 C5 不同面：加 boundary apex 後含顯式 K3,3 subdivision。這證明一般平面性、
relation 與單調性都不足；證明必須使用五條 dual boundary edges 同繞 z 的 cyclic disk 結構。

五個 disk representatives 各側 9 個單邊 repairs：共享 8、各自私有 1；
新 checker 從全部 5×1,024 subset tables 重算。控制的 16,384 subsets 以兩種
coloring 算法交叉核對，另回溯 root 與 14 個單刪圖。未跑 k=4 disk search、
未重播全量 audit、未新增 Lean theorem。本節與前輪 critical-core 產物一併發布；
接手時以本文件頂端的 flow-repair stopping point 為準。

**下一個窄問題：** 先證 repair 排他性式 (2) 的一側。假設每個 minimal p-zero-set
都包含 q-zero-set，利用兩 demands 只差 z 上相鄰兩邊的 flow symmetric difference，
嘗試導出第三個已知可延拓 demand 的矛盾；若失敗，只找最小 abstract 5-pole control
並測 cyclic planarity，不擴大一般圖枚舉。

重播：`uv run --with networkx==3.5 python scripts/c5_weak_flow_repairs.py --check`，
再跑 critical-core、candidate、quotient checkers；完整驗證狀態見新報告 §5。
驗證已通過：四個 checker、`lake build`（8,820 jobs）、142 個本地連結與 whitespace。

## 前輪研究：相鄰雙缺失的最小阻礙化約（2026-09-16）

報告：[最小阻礙與三種 critical-edge 出口](c5_weak_critical_cores.md)。
候選 A 未證；本輪已在紙面證出三出口的精確充要條件，不需要平面性：
只釋放 p iff 存在 minimal q-obstruction 接受 p；反向對稱。
同時釋放 iff 有 minimal p/q-obstructions A、B 與共同邊 e，使
(A∪B)−e 同時接受 p,q。須排除所有替代阻礙，不能只說 e 擊中所選 A、B。

五個封存代表各有唯一的 p/q 阻礙：各 9 邊、共享 8 邊、各 1 私有邊。
全 5,120 個代表子集核對兩因子公式，15 個直接出口另核對 240-row 回溯。
這是同一 D5 orbit 的機制解釋，非域外驗證，亦未分析每個同 Σ 具體圖。
未跑 k=4、未重播全量 deletion audit、未新增 Lean theorem。

**下一個窄問題：** 先處理報告 §2 式 (3) 的兩族阻礙分離：是否任意候選 A
disk graph 的每側，都存在接受另一缺失 singleton 的 minimal obstruction？
再處理式 (4) 的共同 pivotal edge；不假定唯一阻礙，不假定兩 fibers 共用 coloring。

重播：`uv run --with networkx==3.5 python scripts/c5_weak_critical_cores.py --check`，
另跑下節兩個小 checker。新報告已連至 README 與候選報告，並納入後續 publication commit。
驗證：三個 checker、`lake build`（8,820 jobs）、135 個本地連結與 whitespace 通過。

## 前輪候選定理：相鄰雙 singleton 完全釋放（2026-09-16）

報告：[weak deletion 候選定理](c5_weak_candidates.md)。首選命題：若包含全部 T4，
且恰好缺失 singleton 位於相鄰 boundary 頂點的兩個三色 patterns，則 W 恰有
「各放回一個、一起放回兩個」三個出口。五個位置、15 條邊全部符合；一般情況未證。
五個位置是同一 D5 orbit，候選式由同一份 87-state 資料歸納並回測，尚無域外驗證。
下一個證明缺口是三種 critical-edge 型態的存在性；H 可隨型態不同。

較廣有限規律：T4⊆Σ 的 16 個來源，其 W 恰為 observed strict upper cone，
共 50 邊；也按 k=0..3 分別核對。全部 86 個非 Ω 來源滿足 ∪W=Ω；
56 個分支來源滿足 ∩W=Σ。由 forbidden patterns 定義的 30-state family
恰好辨識所有 W={Ω} 狀態，其中單缺失 orbit 的 10 類可由單調性直接紙面證明。

checker：[c5_weak_candidates.py](../scripts/c5_weak_candidates.py)；
[完整結果](../artifacts/c5_weak_candidates/observations.json)。
亦保存失敗控制及 235-edge 抽象替代 DAG，證明上述規則仍不足以決定全部 W。
驗證：candidate／quotient `--check`、`lake build`（8,820 jobs）、文件連結及 whitespace 通過。
未跑 k=4、未重跑 deletion audit、未修改原 quotient 證書、未新增 Lean theorem。
停止於候選式與有限核對；優先證相鄰雙 singleton 命題，不自動擴大枚舉。

**接手順序：** 先讀報告 §1 的命題 A 與單缺失 orbit 紙面基底，再讀證書的
`candidates.adjacent_singleton_pair`。下一步只處理 `(1,0)、(0,1)、(1,1)`
三種釋放型態：各自尋找 silent-reachable H 與一條 critical edge，或找出此命題的
結構障礙；不要假定兩個 boundary fibers 共用完整 coloring。
這裡是兩個**缺失** singleton patterns，與既有 Kempe 相鄰 singleton 存在性引理不同。

本輪最小重播只需：

```bash
python scripts/c5_weak_quotient.py --check
python scripts/c5_weak_candidates.py --check
```

以下各節保留歷史背景與當時的指令；本輪接手不需要重跑舊全量 deletion audit。

## 前輪有限分析：87-state weak quotient（2026-09-16）

報告：[weak quotient 與 relation inclusion order](c5_weak_quotient.md)。
直接讀取封存 `c5_weak_deletion_audit`，沒有重跑全量 audit、沒有跑 k=4。
W 有 225 邊；inclusion covers 也有 225 邊，但只有 105 邊重合，各有 120 差異。
TC(W) 有 266 對，strict inclusion 有 706 對，缺少 440 對；W 的 reduction 有
185 邊，最長 DAG depth 3。D5 全部 870 次比較通過。

最小 relation witness：`165⊊167⊊431`，`W(165)={431,757}`，
從 165 只能到 `{431,757,1023}`。所以 W 會跳過 realizable 中間點，
也無法到達某些 inclusion covers。所有 mismatch 與逐項證據已保存於
[JSON](../artifacts/c5_weak_quotient/observations.json)，含節點度數、depth 與完整 reduction。
此結果否定兩個具體 order 公式，沒有排除其他 relation-only rule；
一般 weak deletion congruence 仍未證。本輪未新增 Lean。

重現：`python scripts/c5_weak_quotient.py --check`。
驗證：quotient `--check`、`lake build`（8,820 jobs）、文件連結及 whitespace 通過。
停止於此有界分析；不自動擴展到 k=4 或重跑來源全量 audit。

## 前輪理論交付：C5 completion 與 Lean weak-bisimulation bridge（2026-09-16）

報告：[completion 與 weak-bisimulation 信任鏈](c5_completion_weak_bisimulation.md)。
**固定 drawing、同頂點、同有序 C5 的 completion 已有完整紙面證明；
一般 weak-bisimulation bridge 與有限 observable trace equality 已在 Lean 證明。**

completion 先以極大增廣排除不連通與割點，再證 bounded faces 為三角形；
涵蓋 production 的孤立內點、bridges、chords、外圈二度點與 separating triangles。
報告另證 apex-planarity 與存在 disk drawing 的對齊，及 parent 類與
plantri `-P5 -c2 -m2` 的一致性。補邊不要求保持 Σ。

封存 audit 的母圖只商內點置換，因此任意 cell 經固定 boundary 的內點置換
成為保存母圖的 descendant；Σ、W 與全部刪邊路徑在此置換下不變。
**接受紙面 topology、外部 plantri 完備性與封存 Python 計算後，有界結論
可覆蓋全部 k≤3 production cells，含跨 k 比較。** 169,643 仍僅是 audit
實際出現的不同具名圖數，不能改稱全部具名 cells 數量。

Lean：[WeakBisimulation](../Math/WeakBisimulation.lean) 的
`kernel_isWeakBisimulation`、`IsWeakBisimulation.observableTraces_eq`、
`kernel_observableTraces_eq`，以及直接沿用既有 Σ 的 specialization。
它們是顯式 hW 假設下的 kernel theorem；未將有限 audit 或 embedding 放入 axiom。

**精確停止點：** completion 的覆蓋缺口在紙面層已封閉；topology primitives、
plantri 生成完備性、Python／encoding／標號 transport 仍非 Lean 全枚舉證明。
一般 weak deletion congruence conjecture 不變。未跑 k=4、未重跑既有 audit，
未修改 checker 或 132-state catalogue，未處理 K∞=K≤5。
審核見 [新 theorem audit](../artifacts/weak_bisimulation/lean-audit.txt)。
驗證：`lake build`（8,820 jobs）、8 個新 theorem 的 axiom audit、既有公開
定理 audit 與 baseline 逐 byte 比較、本地文件連結與 whitespace 全部通過。
核心 bridge 無 axiom dependency；trace-set equality 僅 `propext`／`Quot.sound`。

以下保存前輪計算與歷史停止點；其中「completion 未證」描述當時狀態。

## 前輪實驗：Full k≤3 weak-deletion congruence audit（2026-09-16）

報告：[完整 weak-deletion audit](c5_weak_deletion_audit.md)。從既有 726 張
plantri triangulated parents 枚舉全部非外圈邊子集，保留所有頂點。
**1,246,132 raw states、169,643 個不同具名圖、6,811,300 transitions、87 個 Σ，
同 Σ 的 W 碰撞為零。** 比較涵蓋跨母圖、全部後代與不同 k。

W 用單邊刪除 DAG DP，並對每個狀態以同 Σ submask strict exits 的 subset-zeta
聚合獨立核對；Σ 以相容賦色交集與完整內點賦色枚舉交叉核對。
每個母圖根再直接枚舉 silent submasks 的出口。沒有枚舉 traces 或逐圖對跑 bisimulation。
全域 W 一致性加紙面匹配引理，給出**此封閉有限域內** ker(Σ) 是 weak bisimulation；
有限 observable trace equality 是 consequence。

**不等同所有 k≤3 cells；completion 仍未證。** 一般 weak deletion congruence
仍是 conjecture，未新增 Lean。A/B 兩因子解釋維持獨立支線，未泛化。

接手：報告 §2–4 → `scripts/c5_weak_deletion_audit.py` →
`artifacts/c5_weak_deletion_audit/observations.json` 的 `sigma_variants`。
下一題可選 k=4 反例搜尋或結構證明；本輪停止於此，未啟動兩者。

```bash
uv run --with networkx==3.5 python scripts/c5_weak_deletion_audit.py --check
lake build
git diff --check
```

驗證通過：完整 checker `--check` 逐 byte 重播、`lake build`（8,819 jobs，
僅既有 lint）、文件連結與 whitespace。沒有背景工作。
本輪 checker、證書與文件隨本次提交發布；以下為歷史停止點。

## 前輪實驗：A/B same-Σ closure 與 weak successors（2026-09-16）

報告：[A/B 的 weak successor 實驗](c5_disk_weak_successors.md)。上一輪已獨立提交
`403e2bd`。本輪只展開 A=`k3-t175`、B=`k3-t180` 的全部非外圈邊子集，維持 k=3。
兩格共 4,096 狀態、22,528 transitions；3,968 個不同具名圖逐一核對完整 relation。

**落在第三分支，但只限這兩張母圖的刪邊域：** 根 silent closure 分別 64／1，
E(A)=E(B)={255,967}；兩格聯集每個同 Σ 狀態都具相同 weak exits，
因此在隱藏 silent 步數與具體刪邊身分的語義下，Σ 等價構成 weak bisimulation。
全部 observable traces 也相同，最長只有兩次 strict 放寬；不只是 depth 2/3 抽查。

共同機制是兩因子：Q=`b0≠b3`，H=`b0,b1,b2,b3 不用滿四色`。
Q iff 保留 chord 03；H iff 保留 A 的四條 spokes／B 的十條非 chord 邊。
公式對每個子集都驗證，weak quotient 為 `Q∩H → Q/H → Ω`。
**未擴到其他母圖、全體 k≤3 或 k≥4；不推論一般 Σ 安全商或 completion。**

接手：新報告 §2–4 → `scripts/c5_disk_weak_successors.py` →
`artifacts/c5_disk_weak_successors/observations.json`。下一個有界問題是其他同 Σ
母圖是否也有共同兩因子分解；本輪停止於 A/B，未啟動該搜尋。

```bash
uv run --with networkx==3.5 python scripts/c5_disk_weak_successors.py --check
lake build
git diff --check
```

驗證通過：新 checker 逐 byte 重播、兩因子公式全子集核對、文件連結與 whitespace、
`lake build`（8,819 jobs，僅既有 lint）。本輪另作獨立 commit；未 push，沒有背景工作。

## 前輪實驗：C5 disk 三角化與單邊刪除（2026-09-16）

報告：[固定 C5 disk 單邊刪除](c5_disk_deletions.md)。plantri 5.8 的
`-P5 -c2 -m2` 生成 k=0..3 的 1、4、14、69 個嵌入同構類；展開固定 boundary
標號並只商內點置換後，共 726 張母圖，枚舉 7,500 次非外圈單邊刪除。
幾何逐面核對；4,906 個圖的完整 relation 以 1,177,440 次 boundary 回溯交叉驗證。

得到 87 個 Σ，均在既有 132-state catalogue 內。**不是所有 k≤3 cells 的枚舉**；
未做多邊刪除、k≥4 或 completion lemma。累積 relation 10→21→51→87，未觀察到飽和。
同 k、同 Σ 的 11,070 對母圖中，k=3 有五組「所有單步後繼」碰撞，但差異
全部只是能否保持原 Σ；嚴格後繼碰撞為零。具體 A=`k3-t175`、B=`k3-t180`
均為 Σ=199，後繼分別為 `{199,255,967}`、`{255,967}`。
這反駁 Σ 決定完整單步後繼，**尚未反駁忽略自環後的 catalogue 合併**，也未證其安全。

接手：新報告 §1、§3 的精確排除範圍 → `scripts/c5_disk_deletions.py` →
`artifacts/c5_disk_deletions/observations.json`。下一個有界問題是上述 A、B 的
保持 Σ 刪邊後繼是否有不同嚴格出口；本輪未啟動多步搜尋。
信任邊界：plantri 生成完備性為外部依賴，Python 幾何與 coloring 為有限計算，未新增 Lean。

```bash
uv run --with networkx==3.5 python scripts/c5_disk_deletions.py --check
lake build
git diff --check
```

驗證通過：新 checker 逐 byte 重播、四份 plantri 輸出重新生成一致、
`lake build`（8,819 jobs，僅既有 lint）、文件連結與 whitespace 檢查。
本輪單邊實驗與先前 §7 三角化說明一併提交；未 push，沒有背景工作。

## 前一支線：新增點／邊的關係影響（2026-09-15）

2026-09-16 補充：[新增點／邊觀察 §7](extension_effects.md#7-拓撲結構三角剖分作為-maximal-constraint-normal-form)
整理三角剖分作為 maximal-constraint normal form 的結構觀點：將內部面統一為三角形，
研究更受限的結構及其平面拼接。可將全圖補成三角剖分，四色存在性足以化約，
但完整邊界關係可能嚴格縮小；三角形面不排除 C5 等長環。
另區分球面三角剖分與固定 C5 disk 的內部三角剖分及其合法操作限制。
本次僅文件整理，未新增 Lean、計算或啟動後續研究；原停止點保留。

使用者指定開啟「加入額外點或邊會對相對關係影響和範圍」研究。
入口：[新增點／邊觀察](extension_effects.md)。先固定有序 C5 的完整染色關係，
完整核對 5 個 chords、32 個單內點鄰居集、1,024 對雙內點鄰居集的未連／連邊圖，
共 2,085 圖、500,400 次整圖延伸查詢；未篩選 disk 合法性。

單內點 6/32 嚴格縮小關係但所有 pair 投影不變；雙內點間加邊 206/1,024
嚴格縮小，其中 105 個 pair 投影仍相同。給出共同 singleton 可用色的精確刪除判準，
以及一般圖無固定影響半徑的紙面構造；本輪新增結論未 Lean 化。
兩個三鄰居點經加邊產生同色強迫的 witness 有 disk 放置障礙，不當成 planar 結果。

接手：新報告 §2–4 → `scripts/extension_effects.py` →
`artifacts/extension_effects/observations.json`。下一步是先有幾何證書、再分類
disk 合法擴張中的 pair forcing 與共享介面；尚未開始該分類或跨圖 Kempe 搜尋。
既有修復介面的停止點保留於下節，不重搜原閉包。

```bash
python scripts/extension_effects.py --check
lake build
lake env lean Math/LocalClosureAudit.lean
git diff --check
```

本輪上述檢查均通過：build 8,819 jobs（僅既有 lint），既有介面定理審計無
sorryAx／native compiler axioms；新報告連結與 whitespace 檢查通過。
沒有新增 Lean 或背景工作；本輪報告、checker 與完整證書隨本次提交發布。

## 原路線停止點：修復介面碰撞與 retained-port 分割（2026-09-15）

詳見 [介面研究報告](c5_repair_interface.md)；[來源修復報告](c5_guard_repair.md)
§3.1、§4.1 已補鄰居歸屬等價式與成本分量數公式，均為紙面推導，未 Lean 化。
研究目標是來源共同介面 I(c) ⇒ 修復後 guard 且 Δχ≤0，先證充分性，再談最小性。

沿用既有 5,952-state 閉包，指定 boundary 型有 600 states／25 個共同色軌道；
19 軌道符合 Q trace `{2,4}`，其中 13 個原 guard 失敗。找到關鍵碰撞 7／17：
完整 Q、位置 2 鄰居色與逐邊 typed cut 相同，修復後 guard 都真，但 χ 成本為
−1／+1。7 正是原 B₂ 有效修復色軌道；兩者只差 cut 外 singleton BC@8。
它切換 retained primal 路徑 `0–8–14` 的存在，並改變 dual owner 分割。
故這份候選介面若接受 7，也會接受不安全的 17，不能單獨保證安全修復。

紙面壓縮引理：primal 只需 root、指定鄰居與 cut 端點的 retained 分割；dual
可略去兩側共同不接觸 cut ports 的 owners，Δκ 不變。兩側分割仍分別抽取，
尚未證共同結構機制或最小資訊，也沒有一般準備保持／後綴成本定理。

接手：新報告 §3–4 → `scripts/c5_repair_interface.py` 的 `port_interface`、
證書 `artifacts/c5_cells/repair_interface.json` 的 `primary_witness` 與 `rows`。
下一題是 retained 路徑對 primal／dual 分割的共同約束，或準備如何強制它；
候選條件必須能處理 singleton-8 反例，不再增加同一色軌道的成功標號。

```bash
uv run --with networkx==3.5 python scripts/c5_repair_interface.py --check
uv run --with networkx==3.5 python scripts/c5_guard_repair.py --check
uv run --with networkx==3.5 python scripts/c5_singleton_preparation.py --check
lake build
git diff --check
```

本輪未新增圖、重搜閉包或新增 Lean；既有 checker／證書保持原樣。
驗證：上述三個 checker 的 `--check`、`lake build`（8,819 jobs，僅既有 lint）、
`git diff --check` 及新檔 whitespace／文件連結檢查通過。沒有背景工作。
文件、checker 與新證書隨本次提交發布。

## 先前停止點：B₂ guard 精確判準與來源修復接口（2026-09-15）

詳見 [guard 修復報告](c5_guard_repair.md)。已補固定 AB@0、AC@4 後綴成功
iff guard 的紙面證明，以及 BC@2 加共同 B/C 角色重命名後的來源集合更新公式。
來源充分條件 P 要求 BC component trace `{2,4}`、位置 2 在預測 W* 中孤立，
以及同一 cut 的 D13 quotient ranks `1→1`、D23 ranks `1→0`。
條件式紙面引理給 `P ⇒ 修復後 guard 且 χ 下降 1`，未 Lean 化。
P 仍分別要求隔離與成本條件，尚未證明更小共同結構會迫使兩者成立。

固定 B₂：72 個原 guard 的充要判準、24 個修復後 guard、168 個後綴步的來源
成本公式均已回放；24/24 失敗來源符合 P。但 72 個準備後完整來源只有 3 個共同
色置換軌道，失敗 24 個恰是同一結構的 24 種標號。不能誇大結構多樣性。

接手：[新報告 §3–6](c5_guard_repair.md#3-修復-guard-的來源集合更新公式)
→ `scripts/c5_guard_repair.py` 的 `repair_source`、`source_cost`。
待攻：由更弱 component／cut／owner 條件同時推出隔離與成本，及準備如何產生
並保持這些條件。沒有一般後綴成本定理或最小資訊定理。範圍仍為固定 B₂，
未擴圖、重搜閉包、改動舊證書或新增 Lean；本輪程式、證書與文件隨本次提交發布。

```bash
uv run --with networkx==3.5 python scripts/c5_guard_repair.py --check
uv run --with networkx==3.5 python scripts/c5_singleton_preparation.py --check
lake build
git diff --check
```

驗證：上述兩個 checker 的 `--check`、`lake build`（僅既有 lint）、
`git diff --check`、新檔 whitespace 與報告連結檢查均通過。沒有背景工作。

以下為先前停止點。

## 先前停止點：Singleton 的等高覆蓋限制與 B₂ 準備策略（2026-09-15）

詳見 [singleton 準備策略](c5_singleton_preparation.md)。既有 χ=2 非 Goal 的
936 個完整狀態形成 20 個等高分量；四度 singleton 直接成功出口只覆蓋兩個
48-state 分量，其餘 840 個不能等高到達該出口。
B₂（含 84、531）恰是一個未覆蓋的 72-state 分量。其 boundary 型
`(A,B,C,A,B)` 要靠單點改色直接成功只能改位置 0 或 4，但固定圖四度 boundary
頂點是 1、3；報告 §3 給純 boundary 紙面證明。

B₂ 的 72/72 起點均可先交換位置 1 的 singleton BD component，χ:2→4；
再用來源 connectivity guard 選擇 2–3 步 χ 不增、不返回 B₂ 的成功後綴。
guard 從 `(A,D,C,A,B)` 的 `S=Comp_AB(0)` 定義
`W=C色頂點 ∪ (A色頂點\S) ∪ (B色頂點∩S)`，要求 2、4 在 G[W] 不連通。
成立則 AB@0、AC@4 必到 singleton-1；此染色引理有紙面證明，未 Lean 化。
48 個直接符合，24 個先做 BC@2 形成 guard。全程高度分別 `2→4→3→2`、
`2→4→3→3→2`，72 條共 240 步全部回放，避開禁用型 `[-1,0,2]`。
後綴規則不查 ID／Goal 表選操作，另以獨立有向最短路核對其長度。

接手：報告 §5–7 → `scripts/c5_singleton_preparation.py` 的 `tail_guard`、
`structural_tail`。待證的是 guard 失敗時 BC@2 能修復它的結構條件，以及大 component
操作 χ 不增的共同來源理由；這兩項目前都是固定 B₂ 證據。
舊 B₂ 已有峰值 3 成功路徑，本輪提供較易描述的峰值 4 策略，不聲稱改善最小峰值。
未擴圖、重搜閉包或新增 Lean；本輪及上一輪程式、證書與報告隨本次交接一併提交。

```bash
uv run --with networkx==3.5 python scripts/c5_singleton_preparation.py --check
uv run --with networkx==3.5 python scripts/c5_local_exit.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_barriers.py --check
lake build
git diff --check
```

新 checker、局部出口 checker、barriers checker 的 `--check`、`lake build`
（僅既有 lint）、新文件連結與 whitespace 檢查通過。沒有待完成驗證或背景工作。
以下均為歷史停止點，以本節為準。

## 先前停止點：四度 boundary singleton 的局部出口（2026-09-15）

詳見 [局部出口報告](c5_local_exit.md)。沿用既有固定圖與閉包，找到更短的 K=4
出口來源條件：boundary `(C,D,C,A,B)` 的位置 3 若 degree=4、鄰居全用 B/C，
直接做 **AD@3、component={3}**，即得 singleton-4。
四條 cut 邊在 dual 中形成 terminal 2 到 terminal 3 的 path。
刪 cut 後，另兩系統各只補一條 terminal 邊與一條內部邊，因此各自 cycle 增量
在 `{-1,0,1}`；D₁₂ 完整保留。從 χ≤2 出發峰值≤4，且不可能是禁用型 `[-1,0,2]`。
報告 §2–3 有 retained-owner 精確公式與一般紙面證明，未 Lean 化。

R 的 48/48 均符合；anchor 為 `3022→1112`，cycles `(1,0,1)→(1,1,2)`。
既有閉包中同一 ordered boundary 型有 384 個來源，96 個通過局部 guard，
全數回放得到上述 cycle 向量；其中另 48 個不屬 R，不宣稱也有峰值必要性。
新引理使用不同操作 AD@3；未證舊 AD@1 引理前提 1–2 推出其完整重接前提 3–4。
新證書 `artifacts/c5_cells/local_exit.json` 保存完整 retained blocks、原始邊與來源 hashes。

接手：報告 §2–5 → `scripts/c5_local_exit.py` 的 `local_source`。
下一缺口是沒有此 singleton 的障礙區域，能否經等高 boundary-root 操作形成它，
或需要另一種局部出口。一般區域可達性、一般 K=4 與 `K∞=K≤5` 仍未證。
未擴圖、未重搜閉包、未新增 Lean；程式、證書與報告隨本次交接一併提交。

```bash
uv run --with networkx==3.5 python scripts/c5_local_exit.py --check
uv run --with networkx==3.5 python scripts/c5_alternative_exit.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_no_comp.py --check
lake build
git diff --check
```

新 checker、替代出口 checker、禁補償 checker 的 `--check`、`lake build`
（僅既有 lint）、新文件連結與 whitespace 檢查通過。沒有待完成驗證或背景工作。
以下各節均為歷史停止點，以本節為準。

## 先前停止點：更換保留系統的替代出口（2026-09-15）

詳見 [替代出口報告](c5_alternative_exit.md)。固定既有 48-state R，對照同一完整
來源 3022 的 BD@4／AD@1；保存原色框、原邊號及兩套完整 retained-block 重接。
AD@1 成功的來源 guard 是位置 3 的鄰居全為 B/C，使其獨自成 AD component，
故位置 1 的 AD component 僅接觸 boundary `{1}`，交換即 singleton-4。
其 cut 恰是保留 D₁₂ 的 `(0,1)` path。另兩系統重接時，舊 D₂₃ cycle 原封轉入
D₁₃，另閉合一個 quotient hexagon 與一個 loop；兩者共用 face 35 的 cut port。
所以 D₂₃ 計數不變卻不是完整保留，最終 cycles `(1,2,1)`、χ=4。

報告 §4 給帶來源 cut／retained 接線前提的替代出口紙面引理，未 Lean 化。
來源 predicate 不讀目標／Goal 表；R 的 48/48 均符合、角色 AD@1 均直接成功。
共同色角色套用在完整來源與全部系統，不分別正規化操作、不按摘要合併狀態。
另外回放每個來源到 3022 的等高路徑，保留較弱的區域策略論述。
「任意禁補償峰值≤4 成功路徑首次離開 R 必為 2→4」由舊封閉證書直接推出。

接手：報告 §3–4 → `scripts/c5_alternative_exit.py` 的 `source_schema`。
待證缺口是更弱的共同 port／retained path 條件能否迫使此接線，及一般等高區域
能否到達它；本輪只證帶明確接口前提的引理，不把它當一般存在性定理。
未擴圖或重搜閉包，沒有新增 Lean。程式、證書與報告隨本次交接一併提交。
證書入口是 `artifacts/c5_cells/alternative_exit.json`：`comparison` 保存 3022 的
兩個出口，`region_checks` 保存來源條件與 48 個實例，`neutral_routes_to_anchor`
保存回到 3022 的路徑；所有 state IDs 均由來源 hashes 綁定至 `strategy_safe.json`。
後續研究需從上述未證缺口續接，不重跑 K=4 成功判定，也不自動擴圖。

```bash
uv run --with networkx==3.5 python scripts/c5_alternative_exit.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_no_comp.py --check
lake build
git diff --check
```

新 checker 與禁補償 checker 的 `--check`、`lake build`（僅既有 lint）、報告連結
及 `git diff --check` 通過。停在此處，沒有背景研究或待完成驗證。
以下「先前停止點」均為歷史；舊接手方向及未提交字樣不是目前待辦。

## 先前停止點：全程禁止補償型升高（2026-09-15）

詳見 [禁補償策略報告](c5_strategy_no_comp.md)。沿用完整 5,952 states 閉包，
從 boundary-root grammar 全部刪除有序 cycle 增量排序為 `[-1,0,2]` 的 984 條有向邊。
K=4 勝集維持 5,112；K=3 從 2,664 減為 2,616，失去 48 states。
從 state 3022 出發的剩餘安全可達集合恰是這 48 states，全 χ=2、無 Goal；
門檻 3 內全部 96 條離開邊都是補償型。因此此類操作在 K=3 對部分起點必要，
在 K=4 可以全程避開。保留勝態的最短路最多分別增加 1／3 步。

B₃ 普通／補償低出口為 168／24，B₂ 為 48／0。舊證書連通性已能推出任一起點
可等高到普通出口，再接不返回的成功後綴；這一推論本身不限制後綴操作。
報告補入「存在一個好出口即可」的弱版紙面引理，以及 XOR cut 保留一組完整
系統的證明；未 Lean 化。新 checker 回放全部 47,616 rooted 邊並核對 preserved system。

接手：報告 §1–2 → `strategy_no_comp.json` 的 `thresholds["3"].witness` 與
`thresholds["4"].policy`。若求 K=4 策略，研究禁補償策略；若求最小峰值，分析
新 48-state 區域的強制出口。這取代先分析舊 24 筆正例的優先順序，不擴新圖。

```bash
uv run --with networkx==3.5 python scripts/c5_strategy_no_comp.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_barriers.py --check
lake build
git diff --check
```

本輪為固定圖 Python 證據；新 checker 與 barriers checker 的 `--check`、
`lake build`（僅既有 lint）、文件連結及 `git diff --check` 通過。
程式、證書與報告隨本次交接一併提交；沒有背景研究或待完成驗證。
完整染色、Goal、seeds 與 component labels 回查 `strategy_safe.json`；
新證書的來源 SHA-256 綁定其索引。先選 K=4 策略或最小峰值方向，再續研究。

以下全部「先前停止點」是歷史；舊下一步與未提交字樣不是目前待辦，
最新接手入口以上節為準。

## 先前停止點：策略障礙區域／必要低谷／cut 計數（2026-09-15）

詳見 [策略障礙報告](c5_strategy_barriers.md)。只用既有 5,952 states 閉包。
state 126 的 χ≤3 分量 B₃ 有 384 states、全為 χ=3、無目標；
192 條升到 4 的出口全部能接上不返回 B₃ 的峰值≤4 成功路徑。
任一起點至多兩步等高後即可走低出口，保存路徑總長≤6。
state 84／531 的 χ≤2 分量 B₂ 有 72 states、全為 χ=2、無目標；
48 條升到 3 的出口均可不返回地成功，至多一步等高、總長≤3。

更強的負結果：247 在 3≤χ≤4 高度帶的分量有 600 states、無目標；
門檻 4 內的 240 條出口只到 120 個 χ=2、κ=3 states。
所以任意峰值≤4 成功歷程都必須先到 2、之後回升至少到 3；不能用跳過低谷的
相同完整出口替換修復。這是完整固定圖 Python 證據，不是一般跨圖定理。

cut 重接紙面計數引理：保留 common retained graph H，收縮後的 multigraph Q
必須保留 loops／parallel edges／isolates；β(H∪A)=β(H)+β(Q)，故
Δcycles=β(Qnew)−β(Qold)。核對 240 低出口及 7 witness transitions；
126→14 由一個平行邊 cycle 變成 loop＋另一個平行邊 cycle。
附有條件式「等高→低出口→不返回成功續接」規範歷程引理的紙面證明，未 Lean 化。
checker `scripts/c5_strategy_barriers.py --check`，證書
`artifacts/c5_cells/strategy_barriers.json`。456 條宏操作路徑共 1,645 步均已回放。
本輪與前輪 checker 的 `--check`、`lake build`（僅既有 lint）、文件連結與
`git diff --check` 通過；兩輪程式、證書與報告隨本次交接一併提交。
下一入口：報告 §3–6、240 低出口中 24 條 `(2,-1,0)` 排列的補償型重接；
研究結構如何保證出口及續接，不自動擴新圖或添加摘要特徵。

### 當時的接手順序與重現（歷史）

1. 先讀 [策略落地](c5_strategy_safe.md) §1、§3，固定圖、escape、boundary-root
   grammar 與 χ 的定義；本路線 χ 是 cycle 總數，和舊消融報告的布林 χ 不同。
2. 再讀 [策略障礙](c5_strategy_barriers.md) §3–5，區分有限出口證書與尚未 Lean 化
   的條件引理。下一題是結構如何保證受控出口和成功續接，並非重跑閉包搜尋。
3. `strategy_barriers.json` 的 `exit_cut_audits` 保存 240 個出口；取三組
   `systems[*].delta` 排序等於 `[-1,0,2]` 的 24 筆，即下一輪補償型候選。
   `source`／`target` 是 `strategy_safe.json` 的 `states` 索引；圖、完整原色染色、
   component、cut 邊號皆可回查。索引綁定證書 hashes，不當作跨版本穩定名稱。
4. 需要重播時執行以下命令；`--check` 不覆寫證書。沒有背景工作或待完成驗證。

```bash
uv run --with networkx==3.5 python scripts/c5_strategy_safe.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_barriers.py --check
lake build
git diff --check
```

以下「先前停止點」均為歷史；其中的下一步、半徑限制與未提交字樣不是目前待辦。
以本節為準；本輪沒有跨圖策略、摘要充分性、介面寬度或五內點代表定理。

## 先前停止點：策略受限成功路徑／完整固定圖閉包（2026-09-15）

詳見 [策略落地報告](c5_strategy_safe.md)。固定 survivor-811 的既有兩個 seeds，
完整 Kempe closure 共 5,952 個原色完整染色、66,720 條 component-labeled 邊；
boundary-root closure 相同，47,616 條邊。全體在 full／boundary-root 規則下均能 escape。
新增複雜度 χ＝三組 dual cycle counts 總和；「每步 χ 不增」只保留 3,168 states，
舊 radius 2 的 106 起點只保留 96。state 126 的 χ=3、最小成功峰值 κ=4，
有 `3→4→4→3` 成功路徑及門檻 3 下的封閉失敗集合證書。
另 504 states 不需超過初始峰值、但仍需途中回升，state 247 是具體 witness。

門檻 4 下，所有 5,112 個初始 χ≤4 的 states 都能留在該集合成功；
舊 corpus 中涵蓋 94/106，其餘初始即超門檻。反向 BFS 產生 rank／policy，
逐狀態驗證下降及失敗補集封閉；NetworkX 獨立核對 components、cycles、全部距離。
checker `scripts/c5_strategy_safe.py --check`，完整證書
`artifacts/c5_cells/strategy_safe.json`。只有固定圖 Python 計算證據，未新增 Lean、
未證跨圖策略／摘要充分性／介面寬度／完整 Σ 小代表結論。
本輪 `--check` 逐 byte 重播、`lake build`（僅既有 lint）、文件連結與
`git diff --check` 通過；未 commit/push。

下一入口：先從報告 §4 的必要升高與回升 witnesses 找 cut 重接機制／替換引理；
不必重找舊區分詞，不自動增加摘要特徵或新圖。舊 radius 2 限制已由本輪使用者
要求落地而擴成此單圖完整閉包，沒有擴 graph catalogue。

## 先前停止點：cycle-count ablation／三步機制（2026-09-15）

詳見 [消融報告](c5_cycle_ablation.md)。固定 radius 2 的 106 染色，移除 cycles：
84 桶、24 對；21 對最短深度 2，3 對最短深度 3（2 對合法 escape，1 對 legality）。
兩對合法三步 witness 是同一個共同換色 pair orbit。選定詞 `AB@0; AC@1; AD@1`，
source boundary `(A,C,D,A,B)`、ψ=true；cycles `(1,1,1)`／`(0,1,2)`。
第一步後 pairings 與六色對 boundary partitions 仍相同，第二步後首次不同；
第三步 singleton-2／singleton-1。NetworkX 獨立檢查全部 931 個較短詞不區分。

新來源 χ 用兩層誘導連通性查詢；在明確兩個 component traces guard 下，
一般三步 `singleton-1 iff ¬χ` 已有紙面證明，尚未 Lean 化，不用平面性或 cycles。
選定 witness 的最後誘導集只差頂點 12／8：12 橋接共同子圖中含 1、4 的分量，
8 只碰含 1 的分量。新 χ 在 22 個染色適用；細化後 87 桶、20 對，仍全有兩步衝突。
cycles 提供額外辨識力，但未證它是任何充分狀態的必要欄位；尚不能用 χ 全面取代。
checker `scripts/c5_cycle_ablation.py --check`、證書
`artifacts/c5_cells/cycle_ablation.json`。三輪 checker、`lake build`、`git diff --check`
通過。停在 radius 2／continuation 深度 3；本輪程式、證書與文件隨本次交接提交。

### 接手順序與下一步

1. 先讀 [消融報告](c5_cycle_ablation.md) §2–5：具體 witness、一般 iff 的完整 guard、
   單頂點橋接機制，以及細化後仍有衝突的限制。
2. 對照 `scripts/c5_cycle_ablation.py` 的 `source_rule` 與 `report`；原始 corpus 在
   `artifacts/c5_cells/behavior_radius2.json`，本輪沒有擴大它。
3. 若續做機制分析，直接從 `cycle_ablation.json` 的
   `refined_residual_pair_indices` 索引 `pairs`，取得剩餘 20 對與各自兩步詞／完整回放；
   不必重新找已完成的三步 witness。先比較共同換色軌道，再追蹤來源連通條件。
4. 若選擇形式驗證，從報告 §3 的一般三步 iff 與 `Math/KempeSurgery.lean` 開始；
   兩步 iff、三步 iff、單頂點加入引理目前都是紙面證明，尚未 Lean 化。

執行 `uv run --with networkx==3.5 python scripts/c5_cycle_ablation.py --check`
可重播本輪並逐 byte 核對證書；不加 `--check` 會覆寫證書，修改程式後需一併更新其 hash。
原色 action labels、完整染色及各自 maximal component 必須保留；`None` 不等於 false。
不依摘要合併 states，不自動擴 radius 3 或新圖。這裡列的是後續入口，沒有背景研究或待完成驗證。

以下「先前停止點」保留歷史敘述；其中的下一步與未提交字樣不是目前待辦，接手以上節為準。

## 先前停止點：固定 predicate 的半徑 2 辨識實驗（2026-09-15）

詳見 [第二輪報告](c5_behavior_radius2.md)。依使用者覆核，先問固定色框 predicate
下是否有非全域換色的同摘要染色可被短 continuation 區分。
同圖半徑 2：106 個完整染色、482 條歷史；基底 100 桶／6 對衝突，固定 ψ
101 桶／5 對，實際色框 ψ 106 桶／0 對。基底 6 對全部屬原反例對的一個共同
全域換色軌道，未發現新機制；細化後無非單點桶，仍無充分性證據。
補驗半徑 1 的基底 15 桶／3 對，以及完整 22 頂點的 B↔C、B↔D 關係。
一般 iff 是已有紙面證明的帶條件策略規則，尚未 Lean 化；仍需完整染色計算。
新 checker `scripts/c5_behavior_radius2.py --check` 與證書
`artifacts/c5_cells/behavior_radius2.json`。兩輪 checker、`lake build` 與
`git diff --check` 通過。停在半徑 2，未 commit/push；下一入口仍是固定摘要的
非單點桶與非換色副本衝突，或另行 Lean 化一般 iff。

## 先前停止點：behavior refinement 第一輪（2026-09-15）

使用者提案已納入 [c5_behavior_refinement.md](c5_behavior_refinement.md)，
實作與紙面證明見 [第一輪報告](c5_behavior_refinement_results.md)。
固定 survivor-811；30 個 boundary-root actions，同步 BFS 深度 2。
原 c/d 完整觀察最短 1 步區分，escape 觀察最短 2 步；指定
`AB@0; BC@2` 已完整重播。一般 source induced-connectivity iff 已有明確
boundary trace 前提與紙面證明，尚未 Lean 化。

兩起點半徑 1 corpus：18 個完整染色、32 條歷史。固定色框 predicate 後仍有
2 對色框外衝突；按實際 boundary 色框實例化 predicate 可分開它們。
結果 18 桶皆 singleton，零剩餘 pairs，**不構成多步充分性證據**。
checker `scripts/c5_behavior_refinement.py --check`；證書
`artifacts/c5_cells/behavior_refinement.json`。沒有 observation-based dedup、
compatibility 剪枝、新圖搜尋或 K∞=K≤5 結論。
下一步：Lean 化一般 iff，再考慮同圖半徑 2 corpus 的非平凡剩餘桶。
新舊 witness checker、`lake build`、文件連結與 `git diff --check` 通過；
本輪成果隨此交接一併提交。

## 先前停止點：Kempe surgery 與 cut 接口引理已 Lean 化（2026-09-15）

新增 [Math/KempeSurgery.lean](../Math/KempeSurgery.lean)（普通證明，無 `native_decide`、
無 `sorry`；審計 `Math/KempeSurgeryAudit.lean`，輸出
`artifacts/c5_cells/kempe-surgery-lean-audit.txt`，全部只依賴 `propext`、`Classical.choice`、
`Quot.sound`）。補掉兩個先前標為「紙面證明，未 Lean 化」的一般圖引理，任意頂點型別，不用平面性：

- **cut 接口的收縮引理**（[c5_cut_interfaces.md §2](c5_cut_interfaces.md)）：
  `quotientGraph H A` 以 `H` 的 connected components 為節點、`A` 邊為弧。
  `reachable_sup_iff_reflTransGen`、`reachable_sup_iff_quotient` 證 `H ⊔ A` 的可達性等於
  quotient 的可達性；`componentEquiv : (H ⊔ A).ConnectedComponent ≃ (quotientGraph H A).ConnectedComponent`。
  孤立分量自動保留（它們就是 quotient 節點）。
- **一次 swap 的六色對更新**（[c5_kempe_connectivity.md §1](c5_kempe_connectivity.md)）：
  `KempeSet G c a b S`（含於 `{a,b}` 頂點、對 `{a,b}` 鄰接封閉，涵蓋單一 component 與
  components 聯集）；`swapOn c a b S`。`swapOn_proper`；`pairGraph_swap_same`（AC 不動）、
  `pairGraph_swap_complementary`（BD 不動）；`pairGraph_swap_mixed`：
  `pairGraph (swapOn c a b S) a d = retained G c a d S ⊔ stars G c b d S`，證明中用到
  properness（`b ∩ S` 內無邊）與封閉性（`b ∩ S` 與 `a \ S` 無邊）；
  `mixed_reachable_iff_quotient` 把兩者接起來。另有 `swapOn_univPair`（全域 transposition ＝
  交換全部 `{a,b}` 頂點，對應 class 對 S₄ 封閉）、`swapOn_comm_of_disjoint`、
  `kempeSet_swapOn`、`swapOn_swapOn`。

**仍是紙面／未 Lean 化**：cut 接口的「目標分量必為 path 或 cycle」（三角化 dual 的度數論證）；
kempe_connectivity §2–3 的 disk separation 與強制接口邊；class 計數的均勻原像論證；
equal-cut witness 的可實現性；所有拓撲信任層。沒有新圖搜尋、沒有改動任何 checker。
驗證：`lake build`（8819 jobs，新檔無警告）、`lake env lean Math/KempeSurgeryAudit.lean`、
`Math/PaperAudit.lean` 已加入 §11 Kempe surgery 條目。未 commit/push。

## 先前停止點：同 cut 長度的合法 disk 重接反例（2026-09-15）

詳見 [c5_equal_cut_witness.md](c5_equal_cut_witness.md)。已在既有 survivor-811
同一 22 頂點 disk 上構造兩個完整染色：同 boundary、T、cycles `(1,1,1)`、
同 `Comp_AB(0)` 規則，cut 長度皆 **21**，目標 αβ pairings 卻為
`(0,4),(1,2)`／`(0,1),(2,4)`，目標 cycles 為 `(1,3,1)`／`(1,2,1)`。
兩 source 都無一步 escape；第一個目標可 BC 到 singleton-4，第二個仍無一步 escape。
另有逐中間相容的 5 步路徑連接兩 source，故也固定同 Kempe class。

**可實現性已具體驗證**：精確有理數座標給出凸五邊形內 37 個三角面，
逐邊無交叉、正面積、不含其他頂點、總面積 `51/2`；報告 §2 給鋪滿 disk 的紙面證明。
完整 proper colorings、maximal components、cut 及 dual 重接均重播，未 Lean 化。
checker `scripts/c5_equal_cut_witness.py --check`；證書保存圖、座標、染色與路徑。
前輪 196 transitions 零衝突結論保留為有限觀察，現在一般 cut 長度充分性已被反例否定。

下一個缺口是各舊 component 切邊數的更強觀察：本例該欄不同，尚未反駁其充分性。
未生成新圖或擴大 catalogue；沒有多步充分 state、最小接口或 K∞=K≤5 證明。
本 checker、兩個 cut 前序 checkers、四個 edge 系列 checkers、`lake build`、
報告連結與 `git diff --check` 通過；Lean 僅既有 lint。使用者已授權將本輪與依賴的
兩輪 cut 成果一併 commit/push。

## 先前停止點：cut 粗觀察的有限比較（2026-09-15）

詳見 [c5_cut_observations.md](c5_cut_observations.md)。完成前輪指定的同批
196 transitions 比較：固定原色 boundary、T、cycles 與色對的基底有 44 個
後繼衝突組；加 cut 長度後 150 組、0 衝突，其中 34 組含不同完整 source 染色。
再加各舊 component 切邊數／原邊數得到 180／186 組，仍 0 衝突。
**未找到 cut 長度不足的反例；也未證一般充分性。**

另保存原 transitions 2、12：同基底、同 `Comp_AC(0)` 選取規則及同 target
boundary，cut 長度 8／4 對應不同 αβ pairing、cycles 與一步相容性。
checker 重播全部合法 actions、588 次接口預測，證書保存全分組及來源 hashes。
接手：本節 → 報告 §1、§4 → `scripts/c5_cut_observations.py`。
下一步可研究同切邊數而不同 retained-port 分區的紙面重接歧義，但需另證
可由合法 disk 染色與 Kempe action 實現；抽象接口歧義本身不夠。
新 checker、原 cut 接口 checker、`lake build`、新報告連結及 `git diff --check`
通過；Lean 僅既有 lint。未新增圖搜尋或 Lean，未 commit/push；前輪未提交檔案保留。

## 先前停止點：同 relation 的 BC 坍縮差異與 cut 接口（2026-09-15）

詳見 [c5_cut_interfaces.md](c5_cut_interfaces.md)。固定前輪 Errera disk，在既有
一步相容／兩步逐中間相容階段中，篩出同原色 boundary、同 T 的 4 個完整 witnesses
與 10 條歷史；source cycles 都為 `(0,0,2)`。統一操作 `Comp_BC(0)`：四列 βγ cycles
皆 2→1，但只有兩列目標仍無一步 escape；另兩列新生 αγ cycle，再 BD `{2}` 即到
singleton-1。嚴格指定舊 component `{0,5,12,14}` 則只在第一列合法。

新增「刪 cut 後 retained components 的 ports／boundary terminals 分區，再加新 cut
邊」的一步重建接口；紙面連通分量引理說明其正確性，未 Lean 化。
checker 在既有 196 transitions 的 588 組 systems 上，預測 pairing／cycle counts
與直接目標重算完全相同。這個接口依賴指定合法 action，大小也未有常數界；
不宣稱能自行列舉下一步 actions 或作為多步充分 state。

接手：本節 → [報告 §1–2、§4](c5_cut_interfaces.md) →
`scripts/c5_cut_interfaces.py` 的 `interfaces/predict`。
證書 `artifacts/c5_cells/cut_interfaces.json` 保存四個比較及原始歷史索引。
下一步僅在同一批 transitions 測 cut 長度／切割次數等粗觀察是否丟失重接結果；
未擴大 catalogue、啟動 polygon grammar 或 safety game。

新接口 checker、四個既有 edge 系列 checkers、`lake build`、新增文件連結與
`git diff --check` 全通過；Lean 僅既有 lint。沒有新增 Lean，未 commit/push。

## 先前停止點：多候選 edge-state 與局部結構坍縮（2026-09-15）

使用者要求實作同時保存多個合法相對關係，並確認「坍縮」指 paths／cycles／區域
在 switch 後重接、合併或消失。詳見 [c5_edge_choices.md](c5_edge_choices.md)。
已實作 `EdgeModel/Branch/Choice`、`switch/condition/split/query/view`；完整染色作
共同見證，原色框架與每條歷史保留，view 分組不合併 witnesses。
固定 Errera 兩個既有起點：一步 20 branches／20 colorings／12 joint rows；
兩步 196／119／53。分欄投影混合會額外造出 8 個兩步不可達 tuples；
同 source pairing 冒用另一 witness 的後繼也有明確負控制。
每步都要求無一步 escape 時，兩步留下 124 branches；只篩最後一步留下 132，
多出的 8 條曾經過不相容中間狀態，證書保留其區別。

**實際結構坍縮**：第一起點先 AB `{0,1,2,9,11,15}`，再局部 BC `{0,5,12,14}`。
後一步保留 αβ、重接另外兩系統，使 βγ cycles 2→1、type-1 regions 4→3，
兩端仍無一步 escape。已排除全域換色造成的 system 名稱置換；完整 edge／vertex
交集矩陣顯示分裂與合併可同時發生，不把數目減少誤寫成刪除完整舊 component。
這否定「結構坍縮必立即打破相容」的局部猜想，未提供全 class invariant。

checker `scripts/c5_edge_choices.py --check`；證書 `artifacts/c5_cells/edge_choices.json`。
本次整理提交範圍：joint incidence、switch traces、多候選 API 的三組 checker／證書與報告，
以及此交接入口。四個 edge 系列 checkers（含既有 `c5_edge_states.py`）、`lake build`、
文件連結與 `git diff --check` 通過；Lean 僅既有 lint。沒有新增 Lean 或新圖搜尋。

**接手順序**：本節 → [choices 報告 §1–4、§6](c5_edge_choices.md) →
`scripts/c5_edge_choices.py` 的 `Choice.switch/condition/view`、`EdgeModel.edge_replay`。
最小輸入是 `edge_choices.json` 頂層 `graph`、`seeds`、`structural_cycle_loss`；
`stages` 的每個 branch 用 `origin` 與 `history` 索引 `transition_table`，可逐步回放。
下一步固定上述局部 BC 重接，對比其他同 source relation 候選的坍縮差異；
保留各自完整 witnesses、原色框架與中間相容條件。完整 witness 後端不是已證有限壓縮 state。

**已完成的輔助入口**：[joint incidence 報告](c5_edge_incidence.md)。三種 incidence
壓縮都分開原 Errera regression，但都仍有 successor collision；不要從舊節的
「尚未執行 incidence」重新開始。那些說明是歷史停止點，最新狀態以本節為準。
**研究停在此處**；未擴大 catalogue／survivor、不啟動 polygon grammar 或 safety game。

## 先前停止點：edge switch 與接口坍縮（2026-09-15）

使用者澄清關注 edge-state 怎麼 switch 和狀態坍縮；詳見
[c5_edge_switches.md](c5_edge_switches.md)。固定 Errera 加五條既有 survivor routes，
六條 traces、14 次 switches，保存完整 cut、三組 components 重接及中間相容狀態。
Errera 內部 CD move 同時切換 βγ 的兩個 cycles，使 S={0,5}→{0}、T={2,10}→{2}、
接口邊 (5,10) 退出接口；boundary pairings 與 cycle counts 不變，仍無一步 escape。
再做 AC{0}、AD{2} 才到 singleton-1。這是實際接口消失，原圖邊未刪除；
指定 component switch 可逆，不是 C5→C3/C4 收縮定理。
已確認的中間狀態標作「實際可實現＋無一步 escape」，不宣稱全 class 封閉。
590 route 的 cycles 可新生再消失，不能以 cycle 數當嚴格下降量。
checker `scripts/c5_edge_switches.py --check`；證書 `artifacts/c5_cells/edge_switches.json`。
新 checker、原 edge checker、既有 incidence 草稿重播、`lake build`、`git diff --check`
通過；Lean 僅既有 lint。沒有新圖搜尋、Lean 修改、commit/push。
下一步沿具體 cut 的 interface 重接規則研究；polygon 壓縮仍需另定義 interface。

## 先前停止點：edge／pairing state 已精確核對，但加 cycle counts 仍不足（2026-09-15）

詳見 [c5_edge_states.md](c5_edge_states.md)。**紙面轉換＋固定圖精確計算，未新增 Lean**。
使用既有 3 個 survivor、120 個 Errera 對齊 controls、132 個 catalogue witnesses；
沒有新圖搜尋。199 個三角化 disk 做 dual audit，56 個非三角化 witness 只做 primal XOR
audit，沒有依染色偷偷補圖。12,301 個染色 representatives、118,690 次 swaps，
其中 109,660 次 dual cut checks、34,053 個 boundary partition checks 全通過。

**精確規則**：交換色對 `{a,b}` 的 component S，令 `k=a xor b`，則只有 cut 邊的
type XOR k；dual cut 是另外兩種 types 的**若干完整 paths/cycles 的聯集**，不一定
只有一條。該 two-type system 的 pairing 保留，另外兩組可能改變。
三組 pairings 加 boundary word 可恢復六個色對的 boundary connectivity，能判斷
一步 escape；五個四色 fibres 的 blockers 已列於新報告 §3。

**不足見證**：固定 Errera disk 上，同圖、同 class、同 ABACD boundary 的兩個染色，
T 完全相同，三組 cycle counts 也同為 `(0,0,2)`，最短 escape 卻為 **3、2**，而且
一步 successor T 集合不同。兩者正由前輪內部 CD component 交換相連。
故 `T=(w,π12,π13,π23)` 與 `T+cycle counts` 都不是 future-sufficient state。
三個 survivor 的五個 aligned 起點皆同 T，escape 第一步均為 AD：保留 π12、改變
π13 和 π23。這只是固定圖觀察，沒有證 five-fibre incompatibility 或 H1–H5。

**下一個有界入口**：先用三組 systems 的 shared-edge／region incidence 或完整
interface relation 區分這對 Errera states，再測同 state 不同後繼。尚未執行此步。
H1 必須量化同一 uncoloured embedded network 的多個染色及其全 class transitions；
跨染色曲線不能疊畫 crossing 後直接判矛盾。dual path 端點位於 boundary 邊內，
`C5→C3+C4` 亦需先定義 interface 壓縮，沒有自動成立的 polygon grammar。
不擴大 catalogue 或 survivor 家族，不重跑先前生成器。

**接手順序**：本節 → [edge 報告 §2–3、§5.2、§6–7](c5_edge_states.md) →
`scripts/c5_edge_states.py` 的 `Dual.systems`／`Dual.state`／`Dual.boundary_partition`。
最小輸入是證書頂層 `same_class_regression`：包含固定 Errera 的兩個完整染色、
連接兩者的 CD component 與獨立有標號 BFS routes；圖的邊／面在
`graphs[name="errera-0"]`。下一輪先增加能區分此對的觀察量，再沿用 `audit_graph`
檢查同 state 的後繼集合；只分開此對尚不等於證明新 state 充分。

重播 `uv run --with networkx==3.5 python scripts/c5_edge_states.py --check`；
證書 `artifacts/c5_cells/edge_states.json`，含五個 fibre obligations、survivor 全 moves、
逐圖 transition hashes、collision 見證及原色框架 escape。新 checker、獨立有標號 BFS、
既有 complementary checker、`lake build` 與 `git diff --check` 均通過；
Lean 僅既有 lint 警告。研究停在上述入口，未執行下一輪 incidence 實驗。

## 先前停止點：高度數 disk 家族——CD 機制不唯一，完整 AB|CD 立方體可以全程存活（2026-09-15）

詳見 [c5_corner_disks.md](c5_corner_disks.md)。**精確有限證書＋紙面小引理，未 Lean 化**：
上節入口 (i) 的回答。固定 seed 生成 2,000 個三角化 C5 disk（`n_int` 11–20，120 次邊翻轉，
無 boundary chord），保留 0、2 內部度數皆 ≥ 4 的 1,318 個；25,288 個 `x₀₂` extensions、
7,750 個對齊 `AB|CD` 立方體，全部沿用前輪 observers 逐狀態重算。

**結果**：(a) 接口層 502 次 CD 翻轉只有 6 次 corner violation；其餘 496 次分成保留接口
208、吞掉接口 182（全部接口邊在被翻轉 component 內 179、端點脫離 3）、打破 blockers 106。
最強狀態出發的 4 次 CD 翻轉全部保留最強條件。「CD 必破接口」「CD 必保 blockers」
都是前輪低度數樣本的產物，**沒有可抽的 CD 引理**。(b) **三個完整立方體 survivor**
（disk 590／811／891，20／22／23 頂點，維度 (0,0)、(0,1)、(0,1)）在所有對齊狀態同時維持
blockers、接口與兩次新生連通；最短 escape 一律從 split 之外開始：`Comp_AD(0)∋4`
（2 步到 singleton-1，兩例）或 `T`（3 步到 singleton-3）。候選局部引理「完整 AB|CD
立方體必在某狀態失敗」**為假**；矛盾（若有）必須用跨 split 的色對與 class 內其他四色
fibres。(c) 8 個不含禁止 singleton 的 Kempe classes 都是 `x₀₂=0` 型，不是候選。

**下一步**：只剩入口 (ii)。固定全圖 `P(G)⊆{0,2}`，在同一 class 內同時使用五個四色
fibres：survivor 顯示第二層必要條件是交換 `Comp_AD(0)∋4`、`T`、`Comp_AC(2)∋3`、`S`
所到的四色 fibre 各自不得有 1 步 escape。先列出每個四色 fibre 的 blockers 條件，
以 survivor 證書中的 `cross_moves` 表為測試資料，看它們在 survivor 上如何被違反。
不要再擴大本家族或換 seed 找更多 survivor，也不要重跑 catalogue。

**接手順序**：本節 → [corner disks 報告 §2–3、§6](c5_corner_disks.md) →
[complementary 報告 §6](c5_complementary_cube.md) → [connectivity 報告 §2–3](c5_kempe_connectivity.md)。
可沿用 `scripts/c5_corner_disks.py` 的 `random_disk`、`cross_moves`、`survivor_detail`。

重播 `python3 scripts/c5_corner_disks.py --check`（約 20 秒），加前六個 checkers、
`git diff --check`。新證書 `artifacts/c5_cells/corner_disks.json`；
無 Lean／production catalogue／前輪證書修改。

## 先前停止點：完整 AB|CD 立方體無 survivor，失敗機制為 corner collapse（2026-09-15）

詳見 [c5_complementary_cube.md](c5_complementary_cube.md)。
**精確有限證書＋紙面推論，未 Lean 化**：固定 `e={0,2}`、`c|C5=(A,B,A,C,D)`，
對齊 `AB|CD` 立方體的自由 bits 恰為內部 AB／CD components（U₀、V₀ 固定＝全域
A/B、C/D 置換），checker 逐 bit 實際交換並與全部有標號 orbit 的 normalize 對照。
每個狀態在其實際染色上重算 blockers、`S`、`T`、接口、兩次新生連通與最短 escape。

**結果**：既有 132 witnesses 的 176 個 `x₀₂` extensions 成 123 個立方體，
全程維持 blockers／blockers＋接口／再加兩次新生連通者為 11／2／**0**
（AB 子立方體 166／20／4／0 與前輪逐項相同）。Errera 三角化 12 個 5 度頂點刪點
×10 個 D₅ 對齊＝120 個 disk、600 個立方體：80／**0**／**0**。
所有 CD bit 造成的接口失敗（corpus 2 次、家族 160 次）皆為同一機制：被翻轉的內部
CD component 含 0 的全部 C 鄰點且不含其 D 鄰點（或 2 的對偶），翻轉後 `S={0}`
或 `T={2}`，接口空，blockers 保留，escape 恰 2。AB bit 只會保留一切或直接打破 blockers。

**真正候選不存在**：`P⊆{0,2}` 且 `x₀₂>0` 由 chord 恆等式強迫五個 x 全正，catalogue
無此 Σ（424、960、1000 有 `P⊆{0,2}` 但 `x₀₂=0`）；全部樣本都是控制例。

**Corner 條件（紙面推論）**：若全圖 `P(G)⊆{0,2}`，每個對齊狀態、每個內部 CD
component V 都須 `N_C(0)⊄V` 或 `N_D(0)∩V≠∅`，且 2 的 D/C 對偶。它是接口引理的直接
後果，且恰好解釋全部觀察到的 CD 失敗；但只涉及 0、2 的鄰域，樣本中 0、2 僅有 2–3 個
內部鄰點，所以是低度數產物，**不是**「CD 必破」定理。成功標準屬 B。

**下一步（(i) 已由上節完成，零 survivor 已被否定）**：不再擴大低度數樣本。(i) 設計 0、2
內部度數 ≥4 且所有對齊狀態滿足 corner 條件的固定 disk，看 CD bit 是否仍破壞接口，
若仍破壞才有新機制可抽成引理；(ii) 改用全圖 `P(G)⊆{0,2}`，把 corner 條件與接口引理
套到同一 class 的五個四色 fibres。不要把兩處的零外推為證明。

**接手順序**：本節 → [complementary 報告 §1–2、§6–8](c5_complementary_cube.md) →
[AB 報告 §1–2](c5_ab_swap_cube.md) → [connectivity 報告 §2–3](c5_kempe_connectivity.md)。
可沿用 `scripts/c5_complementary_cube.py` 的 `aligned_cube`、`observe`、`singleton_distances`。

重播 `python3 scripts/c5_complementary_cube.py --check`（約 1 秒），加前五個 checkers、
`git diff --check`。新證書 `artifacts/c5_cells/complementary_cube.json`；
無 Lean／production catalogue／前輪證書修改。六個 checkers 與 `git diff --check` 全通過。

## 先前停止點：AB 全交換仍可維持阻擋，固定 Errera disk 證書（2026-09-15）

詳見 [c5_ab_swap_cube.md](c5_ab_swap_cube.md)。
**紙面引理＋精確固定圖證書，未 Lean 化**：AB induced components 在任意 AB 交換下
不變；r 個 components 的全部序列恰為 2ʳ 個有標號結果，固定 boundary 顏色框架後
為 2ʳ⁻¹ 個結果。blockers 可寫成共用 component bits 控制的 signed vertex activation。

**局部候選引理已被反例否定**：「初始 blockers／接口／兩次新生連通成立，便能只靠
AB 序列打破它們」。從 Sage 10.6 ErreraGraph 刪舊頂點 0 得到固定 16 頂點 C5 disk；
證書包含重標號、40 邊、25 個定向三角面與 disk 複形檢查。指定染色的 AB components
為 `{0,1,2,9,11,15}`、`{7,12}`；兩個對齊結果皆通過所有上述條件，故任意 AB
序列皆維持。兩條 blockers 都沒有跨兩個狀態的共同固定 path；不能交換 ∀／∃ 量詞。

**仍可逃逸**：先交換內部 CD component `{5,6,8,10,13,14}`，blockers 保留但接口
消失，再依次交換 AC `{0}`、AD `{2}`，得到 singleton-1。全 Kempe BFS 證最短 escape
恰為三步。該圖每個 x=12、每個 y=8，100 個 S₄ orbits 同屬一個 class，
全圖 P 為全部五點，**不是** `P⊆{0,2}` 反例。

既有 132 witnesses 的 176 個 x₀₂ extensions 分成 166 個 AB cubes；其中全程保留
blockers／blockers 加接口／blockers 加兩次新生連通，分別為 20／4／0 個 cubes。
因此新固定控制例也防止把舊樣本的零當成普遍定理。本輪沒有新圖 catalogue 搜尋。

**下一步（已由上節完成）**：固定 complementary split `AB|CD` 的全部獨立交換，
能否也始終維持 blockers 與兩次新生連通？本例四個對齊狀態中恰兩個失敗；
上節在 corpus 與 Errera 刪點家族中都沒有找到 survivor。另一入口是使用全圖 P 假設的額外結構；本輪沒有排除 AB 作為
更完整證明一部分的用途。Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

**接手順序**：本節 → [AB 報告 §1–6](c5_ab_swap_cube.md) →
[connectivity 報告 §1–3](c5_kempe_connectivity.md)。可直接沿用
`scripts/c5_ab_swap_cube.py` 的 `cube(adj, start, ((0,1),(2,3)))` 與 `observe`：
觀察條件為兩條 blockers 加兩次新生連通，接口非空是其必要結果。
先區分「局部條件能否在整個 split orbit 保持」與「全圖 P⊆{0,2} 能否實現」；
本輪只處理前者的 AB 子問題。不要重跑 catalogue，也不要把只交換 boundary
component 誤當成全部獨立交換。此次整理後研究停在此入口，不另開新搜尋。

重播 `python3 scripts/c5_ab_swap_cube.py --check`，加原 connectivity/class/count/screen
四個 checkers、`lake build`、`git diff --check`。新證書
`artifacts/c5_cells/ab_swap_cube.json`；無 Lean／production catalogue／前輪證書修改。
提交範圍為 connectivity surgery 與 AB cube 兩輪的報告、checkers、證書及交接索引。
上述五個 checkers、文件連結、`git diff --check` 與 `lake build` 全通過；
Lean build 僅重播既有 lint 警告。

## 先前停止點：換色 connectivity surgery 與強制 C–D 接口（2026-09-15）

詳見 [c5_kempe_connectivity.md](c5_kempe_connectivity.md)。
**紙面證明，未 Lean 化**：一次 AC component swap 精確保留 AC／BD induced graphs；
其餘四個色對以「刪除被換走的頂點、收縮剩餘 components、加入新色頂點的 stars」
重建。不能先收縮原 components 再刪頂點，因刪除可切斷舊路徑。

在全圖 `P(G)⊆{0,2}`、`c|C5=(A,B,A,C,D)` 下，令
`S=Comp_AC(0)`、`T=Comp_AD(2)`。初始 BC 1↔3／BD 1↔4 blockers 與 disk separation
給 `S∩C5={0}`、`T∩C5={2}`。交換 S 後必新生 AD 2↔4，交換 T 後必新生 AC 0↔3，
否則再一次 swap 即得到禁止的 singleton-1。沿新路徑第一次離開舊 component，推出
**必存在實際內部邊 `E(C∩S,D∩T)≠∅`**；不假定 S、T 不相交。

**computationally verified**：132 個既有 witnesses、1,810 個完整染色 representatives、
16,680 次 component swaps、66,720 次混合色對重建全通過。
固定 8 頂點 witness 935 同時通過兩個新生連通測試：`S={0,6}`、`T={2,7}`、接口邊 67。
它反駁「不相交的交換區域仍會保留彼此的 component」；同時交換舊 S、T 會使邊 67 同色。
此圖全圖 `P={3,4}`，不是反例；改先交換 AB `{0,1,2}`，再交換 AC `{1,6}`，
兩步即得到 singleton-4。證書包含完整染色／邊／定向 disk faces 與最短 escape。

**下一步**：先讀新報告 §1–5。沿包含 boundary `{0,1,2}` 的 AB component 操作，
必要時全域重命名 A/B，重新追蹤兩個 blockers 與接口。更一般可檢查 AB components
的全部獨立交換；尚無定理保證某次必失敗或存在單調下降量。
接口存在本身不造成平面矛盾；Adjacent-singleton lemma 與 K∞=K≤5 仍未證。
不對單一 class 套 exterior／4CT。本輪無新 mask 排除、無新圖搜尋、無 Lean 修改。

重播：`python3 scripts/c5_kempe_connectivity.py --check`，再跑原 class/count/screen
三個 checkers、`lake build` 與 `git diff --check`。新證書
`artifacts/c5_cells/kempe_connectivity.json`。與後續 AB cube 成果一併整理提交；
此節的下一步是歷史停止點，最新接手入口以上節為準。
上述四個 checkers、文件連結、`git diff --check` 與 `lake build` 全部通過；
Lean build 僅重播既有 lint 警告。

## 先前停止點：同一 Kempe class 的計數恆等式與正參數定位（2026-09-15）

詳見 [c5_kempe_class_counts.md](c5_kempe_class_counts.md)。
**紙面證明＋精確有限證書，未 Lean 化**：每個完整四色染色 Kempe class 都滿足
`x_uv+y_u+y_v=L_K`。四個 boundary words 的 signed functional 在 complementary split
的 70 個 noncrossing swap orbits 上皆為零；五次旋轉共 350 個整數等式。
完整 orbit 的 boundary 原像數相同，使此恆等式可限制到任一 class。

若全圖 `P(G)⊆e` 且 `x_e(G)>0`，包含任一 x_e 延伸的 class K 便有
`m_K=x_e(K)>0` 與全部 `x_f(K)>0`。每個 class 都分解為
`x_e(K)t+Σ_{i∈e}y_i(K)F_i`；正參數可定位在同一 class，不依賴文獻 ray 完備性。
其 support 可達性結論也可由原 Kempe screen 得到，本輪不宣稱新增 mask 排除。

驗證：132 個既有 witnesses 的真實 Kempe classes 與完整計數；另用固定 14-vertex disk 圖
驗證 10 個不同 classes，並加入 crossing-chord／缺項負控制。
checker `scripts/c5_kempe_class_counts.py --check`，證書 `artifacts/c5_cells/kempe_class_counts.json`。
沒有大圖枚舉、新 Lean 模組或既有 catalogue 修改。

**下一步**：保留全圖 P(G)⊆e，利用同一 class 內可達的五個四色 fibres，
明確分析換色對其他色對 paths/components 的影響；尚無最終 connectivity 矛盾。
不能對單一 class 套 exterior／4CT，也不能假定它自身是另一張 disk 圖的 relation。
Adjacent-singleton lemma 與 K∞=K≤5 仍未證。

**接手順序與具體起點**：先讀上述 class 報告 §1–3、§5，再讀
[c5_adjacent_singleton_counts.md §4](c5_adjacent_singleton_counts.md#4-可以直接使用的反證起點)。
可用 D₅ 對齊為 `e={0,2}`，選 `c|C5=(A,B,A,C,D)`；缺失 singleton 3、4
強迫 c 中的 B–C 路徑 1↔3 與 B–D 路徑 1↔4。兩路可共享 B 色頂點，
不能直接用交錯端點判矛盾。下一份成果應明列一次換色前後保留／改變的 connectivity，
而不是重跑 catalogue、push screen 或普通單次 pairing。

**重播**：`python3 scripts/c5_kempe_class_counts.py --check`、
`python3 scripts/c5_adjacent_singleton_counts.py --check`、
`python3 scripts/c5_kempe_screen.py --check`；Lean 基線用 `lake build`。
本次三個 checker、文件連結、`git diff --check` 與 `lake build` 全部通過；
Lean build 僅重播既有 lint 警告，本輪未修改 Lean 原始碼。
本次依使用者要求整理、驗證後 commit／push，研究停在此處，未繼續新搜尋。

## 先前停止點：B₅ face 分解確認，單次 gluing 的限制已釐清（2026-09-15）

詳見 [c5_b5_face.md](c5_b5_face.md)，checker `scripts/c5_b5_face.py --check`，
證書 `artifacts/c5_cells/b5_face.json`。本輪未新增 Lean／大圖枚舉。

**computationally verified＋引用 Lemma 6 的 ray 完備性**：從 Dvořák–Lidický Figure 3
轉錄 12 個 5-poles 並直接枚舉邊染色；全部 raw rays 已為 primitive。
`R₅,₁₂=t`，`F₀=R₅,₉`，`F₂=R₅,₇`。兩個 requested faces 恰為
`cone(t,F₀)` 與 `cone(t,F₀,F₂)`，全部 11 個 independent supports 亦成立。
在 `P⊆{0,2},x₀₂>0` 下唯一分解 `n=ct+aF₀+bF₂`，`c=m=x₀₂>0`。

**Fan-trap corollary（引用 Lemma 13.2 的紙面推論）**：independent P 排除 (ii)/(iii)，
每個三色 boundary extension 可產生某個完整 fan family。沒有證明整個 Kempe component
被困在同一 fan；不應把可達 family 寫成 invariant-set 結論。

**gluing 結果**：完整 12×12 pairing 與 10 個 D₅ alignments 已重播。
planar context `Q=R₅,₃` 同時消掉 F₀,F₂，但 gluing 給 **6c>0**，不是 4CT 矛盾。
只有 wheel ray 與 t 正交，而它與每個 fan pairing=6；故對 c>0 且至少一個正 fan，
任何非零 q∈B₅ 都有正 pairing。這排除單一非零 plane 5-pole 的零染色 closure 路線，
不排除需要額外圖結構的多步方法。下一步需超出普通 pairing，才能證 face 上 c=0。
**後續方向／已知缺口**：先提出超出單次 pairing 的圖變換或 bridge 結構引理，
逐項證平面性、count 變換與 bridge 性質；目前尚無此構造。另一入口是同圖不同染色間的
Kempe connectivity 相容性，尚未建立。12-ray 完備性仍依賴文獻，fan corollary 的平行邊
適用性需補論證，拓撲未 Lean 化。詳見報告 §5「後續方向與已知缺口」。
Adjacent-singleton lemma 與 K∞=K5 仍未證。本次使用者要求整理後 commit／push，不另開新搜尋。

## 先前停止點：計數層、XOR 邊字與補完二分法已 Lean 化（2026-09-15）

**proved in Lean**：三個新模組已匯入 `Math.lean`，公理審計
[count-cone-lean-audit.txt](../artifacts/c5_cells/count-cone-lean-audit.txt) 中 31 條定理
全部只依賴 `propext / Classical.choice / Quot.sound`；所有有限檢查是 kernel `decide`，
沒有 `native_decide`、沒有 `sorry`。

- [Math/C5Counts.lean](../Math/C5Counts.lean)（`FiveBoundary.C5Counts`）：chord `j = {j, j+2}`
  與非相鄰 pair 的一一對應；由 inclusion–exclusion 係數 `a₀, a_e` 組成的計數必滿足
  chord total 恆等式（`ofCoefficients_chordTotalConst`）；在恆等式下
  `x_j = m + Σ_{i∉chord j} y_i`、`Σx = 5m + 3Σy`、`slack = −5m`，翻譯後的 Conjecture 9
  `Σx ≤ 3Σy` 等價於 `m ≤ 0`（`conjecture9_iff`）。每個 independent set 含於某條 chord
  （`independent_subset_chord`）。反例保持引理的代數半部 `all_chords_positive`：
  `y ≥ 0`、support ⊆ chord e、`x_e > 0` ⟹ `m = x_e > 0` 且五個 `x` 全正，
  故違反翻譯後的猜想（`counterexample_violates_conjecture9`）。抽象向量
  `N_P = t + Σ_{i∈P} f_i` 對任意 `P` 滿足恆等式、`m = 1`、slack `−5`、support 恰為 `P`。
- [Math/C5ParityWord.lean](../Math/C5ParityWord.lean)（`FiveBoundary.ParityWord`）：`xor4` 為
  Z₂² 加法；邊字 `edgeWord b j = b_j xor b_{j+1}`；translate 是既有 `colorAction` 的特例。
  `eq_of_edgeWord`：base colour 加邊字決定 b；`fiber_eq_translates`／`fiber_card`：
  同邊字的 proper assignments 恰為四個 XOR translates。`extensionCount` 定義為固定
  boundary assignment 的完整染色數，`extensionCount_colorAction` 證色置換不變，故
  `extensionCount_of_edgeWord`：同邊字延伸數相等（文獻的 dual 計數＝我們的固定 assignment
  計數，不乘 4）。`IsParityWord`（無 0、三個非零字母各奇數次）：60 個字、`integrate` 為右逆、
  proper ⟹ parity（`decide` 1024 例），`fiber_partition` 給 240 = 4·60。
  文獻 a₀=(1,1,2,3,1)→singleton-3、b₀=(1,2,1,1,3)→repeated pair {2,4} 均由 `decide` 驗證。
- [Math/NearTriangulation.lean](../Math/NearTriangulation.lean)：任意長度的 n-週期 proper
  cycle colouring，若無 ear（`c i ≠ c (i+2)`）則二週期（`two_periodic_of_no_ear`）、n 為偶數
  （`even_of_no_ear`）、只用兩色且存在 hub 色使所有 cone 三角形 proper
  （`exists_hub_of_no_ear`）；`ear_or_hub` 是 `fill_polygon` 迴圈的二分法，適用於一般長度，
  不只 checker 的 3..9。Euler 計數 `counts`：`3t = 2E − 5` 與 Euler 公式給
  `t = 2k+3`、`E = 3(k+5) − 8`、dual 頂點 `2k+4`；`corollary20_range`：`2k+4 < 30 ↔ k ≤ 12`。

**仍未 Lean 化（拓撲信任層）**：inclusion–exclusion 從 disk graph 產生 `a₀, a_e` 形狀的步驟
（noncrossing partition、disk components 不相交）；block decomposition 與 `Σ(B)=Σ(G)`；
face 結構、平行邊與 `fill_polygon` 的遞迴終止／Euler 特徵；dual graph 與文獻
near-cubic 類別的對應；Conjecture 9 本身與引用的 Corollary 20。Lean 的 `Counts` 只是十個
整數，`ofCoefficients` 是假設而非從圖推出。Adjacent-singleton lemma 與 K∞=K5 仍未證。

驗證：`lake build`（8818 jobs，新檔無警告）、`lake env lean Math/C5CountsAudit.lean`
（含 `decide` 抽查）、`python3 scripts/c5_count_cone_bridge.py --check`、`git diff --check`。
無新枚舉、未改 production／`cells.json`。

## 先前停止點：反例歸約到 near-triangulation／count-cone 猜想（2026-09-15）

詳細證明與來源：[c5_count_cone_bridge.md](c5_count_cone_bridge.md)。

**紙面證明，未 Lean 化**：若 T4 全收且 P independent，選包含 P 的 chord e，保留
repeated-pair e 的一個完整染色。任何同邊界 disk supergraph H 只要保留這個染色，便有
P(H)⊆e、m(H)=x_e(H)>0；計數恆等式重新推出全部 x_f(H)>0。因此 H 仍是反例。
移除 boundary block 外的枝塊，再逐面以 proper ears／二色 residual polygon 加 hub 補完，
可把任意反例轉成 near-triangulation 反例（允許平行邊，可能增加內點）。

**文獻連接**：Dvořák–Lidický, *Coloring count cones of planar graphs*,
[arXiv:1907.04066v2](https://arxiv.org/pdf/1907.04066v2)，Conjecture 9 經 XOR boundary-edge
對應，正是 3Σy≥Σx，等價於 m≤0。這是足以推出本題引理的較強猜想，不能當成已證。
其 Corollary 20（引用的電腦輔助定理，未在本倉庫重播）適用 dual 頂點數 <30；由
dual_vertices=2k+4，排除 k≤12 的 near-triangulation 反例。不能直接推一般 disk 的同大小上界。

**computationally verified**：240→60 的 XOR 四對一映射、十種記號對應、六個線性基底、
11 個 independent supports、132 個舊 witness counts、11 個抽象向量的 slack −5；
長度 3..9 的 1,231 個 polygon color orbits 補完驗證及缺三角形負控制。
新 checker `scripts/c5_count_cone_bridge.py --check`，證書 `artifacts/c5_cells/count_cone_bridge.json`。

**下一步**：在 near-triangulation 中排除 `P⊆e 且 x_e>0`；只需這個特殊 support 分支，
不必先證完整 m≤0 猜想。可利用三角面背景重看 blocking paths；同圖 connectivity 矛盾仍未建立。
Adjacent-singleton lemma 與 K∞=K5 仍未證。無大圖枚舉、未改 production／cells.json。
（代數與邊字部分已於下一輪 Lean 化，見最新停止點。）

## 先前停止點：adjacent-singleton 計數恆等式與必要條件的不足（2026-09-15）

使用者要求找剩餘缺口後，本輪已完成以下研究與紀錄，後續要求 commit／push。
下次由下列 blocking-path connectivity 缺口接續；本次提交不另開新搜尋。詳細結果見
[c5_adjacent_singleton_counts.md](c5_adjacent_singleton_counts.md)。

**紙面證明，未 Lean 化**：對任意 C5 disk cell，令 x_uv 是四色 repeated-pair uv 的延伸數，
y_i 是 singleton-i 的延伸數，則五條 chord 的 x_uv+y_u+y_v 都相同。
證法是 inclusion–exclusion 加上 disk components 的 noncrossing partition；非零 boundary
partition indicators 只有 discrete partition 與五個單 chord partitions。

**computationally verified**：132 個既有 witness 的完整計數均符合；42 個 noncrossing
partitions 的有限部分全檢查。新整數證書給出 11 個 independent supports 的抽象計數向量，
同時滿足恆等式與三個 complementary Kempe splits 的非負整數 orbit 分解。
其構造為 abstract all-four vector t 加上 singleton 位置的 pentagon fan 計數。
非空 independent support 仍通過既有 exterior screen。這些不是 realizing graphs，
證明的是這兩類計數必要條件仍不足以排除候選。

另外補驗 142 個 Kempe+exterior states 的全部 1,420 個 boundary push transitions，仍封閉。
因此反覆這十種 push 並在每一步重新套 exterior，也沒有新的排除力。

**具體下一步**：反證時選相鄰兩個缺失 singleton 位置，利用 T4 選完整染色
(A,B,A,C,D)，得到兩條強制 B–C／B–D blocking paths。它們可在 B 色頂點相交；
缺口是換色後／不同四色 fibers 間的同圖 connectivity 相容性，不能直接宣稱交錯路徑矛盾。
主 Adjacent-singleton lemma 與 K∞=K5 仍未證。

驗證：新 checker `python3 scripts/c5_adjacent_singleton_counts.py --check`、既有 Kempe
checker `--check`、`git diff --check`。證書為 `artifacts/c5_cells/adjacent_singleton_counts.json`。
沒有大圖枚舉、新 Lean 模組或 production catalogue 修改。

## 先前停止點：C5 adjacent-singleton problem（2026-09-15 表述更新）

**研究維持暫停；本次僅更新問題表述。** 核心改為 adjacent-singleton lemma，數字 masks
留在計算證書對照；沒有新搜尋或不可實現性證明。
使用者指定 Dvořák–Swart 的 [A note on extendable sets of colorings and rooted minors,
arXiv:2504.07764v1](https://arxiv.org/html/2504.07764v1) 為後續重要參考。
恢復時優先對照其 §1 的 planar realizability、Kempe constraints 與 reducibility 觀點；
目前只作方向參考，尚未由該文導出 adjacent-singleton lemma 或 K∞=K5。

使用者要求從原猜想找切入點，本輪改做任意大小 cell 的結構必要條件；沒有再枚舉大 k。
完整論證與範圍見 [c5_kempe_screen.md](c5_kempe_screen.md)。

**computationally verified**：1,023 個非空十 bit masks 經平面 Kempe screen 剩 153；再以
與全部已知外側 cell 非空相交（**使用 4CT 和 disk gluing**）剩 142，包含全部既有 132。
差額恰為兩個 D5 orbit：T4 加 singleton support，或加 independent 2-set support；
各五個固定標號 masks，數值見主文件 §4.3 的 computational certificate 對照。

**Adjacent-singleton lemma，UNPROVED**：任意 C5 disk cell，若 T4 ⊆ Σ(G)，則
E(C5[P(G)]) ≠ ∅；P(G) 是可延伸三色 states 的 singleton 位置集合。相鄰兩位置可由不同
完整染色延伸。由 α(C5)=2，反證可統一假設 P(G) independent，再按需要分情況。
一般 cell 不一定全收 T4；這是套用引理的條件分支。此引理配合上述必要條件，有限
檢查恰剩既有 132 keys，因此是一條通往 K∞=K5 的條件式路線。一般 Kempe/disk soundness
仍是紙面論證，尚未 Lean 化；候選引理是實際數學缺口，不是已證結論。

已試 boundary push（五位置、spoke 有／無）共 1,530 個轉移，153 masks 對其封閉，故僅
重複此操作加 Kempe screen 無法繼續排除。下一步宜研究 T4 全收能否與 independent singleton support 共存，以及
不同完整染色間的 connectivity 限制；T4 全收可先推出 boundary 無 chord。

驗證：`python3 scripts/c5_kempe_screen.py --check`、既有 132 witness 的 NetworkX／全染色
checker（零 mismatch）、`git diff --check`。新報告 `artifacts/c5_cells/kempe_screen.json`
保留 obligations、拒絕 witness、hash 與負控制。沒有新 Lean 模組，未改 production／
`cells.json`。使用者後續已要求 commit／push 此輪成果；研究維持暫停，原猜想地位未變。

## 先前停止點：popcount cardinality 與整數 viable 已接通（2026-09-14）

**proved in Lean**：[Math/IntegerViable.lean](../Math/IntegerViable.lean)，已匯入 `Math.lean`。
可執行 `popcount` 使用 `Nat.bitIndices.length`；`popcount_encode` 對任意有限集合證
`popcount (encode M) = M.card`，不受機器 word 寬度限制。AND／右移計數分別等於
intersection／suffix cardinality。整數 Bool `viable` 使用這些計數與五位 numeric attachment。
`viable_encode_iff` 雙向接上集合版；`viable_decode_iff` 處理 n<2^E 的原始整數。
`integer_viable_of_graph`、`integer_rejection_sound`、`viable_reach_iff` 接通圖層
R1+SYM、拒絕可靠性與兩種 DFS 控制模型。詳見 [§15](c5_cell_enumerator.md#15-popcount-與整數-viable2026-09-14)。

驗證：`lake build`、`IntegerViableAudit`（含 257-bit、空 k、未開 block 與 numeric-order
反例的普通 `decide`）、既有 bitmask／viable `--check`、`git diff --check`。
[公理輸出](../artifacts/c5_cells/integer-viable-lean-audit.txt) 無 `sorryAx`／native 公理。
既有 viable 重播仍為 133,181 prefixes、零誤剪／零規格差異；沒有新 catalogue 搜尋。

**尚未認證**：Python `bin(...).count('1')`／迴圈／建表的執行語義、完整 graph／apex、
染色表、planarity oracle 與 scheduler。此次 Bool guard 以有限 `all` 表達同一條件，
沒有形式化 Python 的 early-break 執行。`viable=True` 仍不保證存在完成圖。
$K_\infty=K_5$ 仍是猜想。可接續染色表 AND 語義，或另立 Python 執行 refinement；
平面性仍是獨立缺口。既有修改保留，production／`cells.json` 未改，未 commit／push。

## 先前停止點：bitmask 表示與整數 DFS 對應已 Lean 化（2026-09-14）

本輪自行選題，接續 reduced 搜尋完整性鏈，補 §13 留下的集合／整數表示缺口。
**proved in Lean**：[Math/EdgeMask.lean](../Math/EdgeMask.lean)，已匯入 `Math.lean`。
詳細定理、反例與信任邊界見 [c5_cell_enumerator.md §14](c5_cell_enumerator.md)。

任意有限邊集合：encode 單射、OR 編碼等於冪次和、insert／AND／prefix／右移的精確對應，
以及五位數值擷取等於 `attValue`。整數版與集合版 DFS 在 encode 搬運 guard／oracle 後
由 `reach_iff` 雙向等價；唯一整數 task label 是 `encode M AND ((1 << p)-1)`。
無損有界解碼必須要求 n<2^E：decode 3 8 再 encode 得 0，是不能刪掉此前提的反例。

**computationally verified**：新 bitmask checker 檢查 2,047 masks／22,528 cuts、
5,461 intersection pairs、20 個最高 257-bit 案例；零差異，四項負控制均被拒絕。
既有 production prefix／graph bridge checker 逐 byte replay 通過；沒有新增 catalogue 搜尋。

**下一步／尚未證**：可執行 popcount 與 cardinality 的一般定理，接上整數 `viable`。
Python 執行、完整 graph／apex、染色表語義、planarity oracle 與 scheduler 仍各有缺口；
此次雙向等價僅是兩種 Lean 控制模型。$K_\infty=K_5$ 仍為猜想。

驗證：`lake build`、`EdgeMaskAudit`、bitmask／prefix／graph bridge `--check`、
`git diff --check`。公理輸出 [bitmask-lean-audit.txt](../artifacts/c5_cells/bitmask-lean-audit.txt)
無 `sorryAx`／native 公理。新模組無 warning；既有 warnings 保留。
production、`cells.json` 未改；既有本地修改保留，未 commit／push。

## 先前停止點：DFS 控制轉移與 prefix reachability 已 Lean 化（2026-09-14）

**proved in Lean**：[Math/ReducedDFS.lean](../Math/ReducedDFS.lean)，已匯入 `Math.lean`。
詳細規格見 [c5_cell_enumerator.md §13](c5_cell_enumerator.md)。`Reach` 區分遞迴 node 與迴圈 scan，
包含 `viable` 失敗即 return 的影響：連略過的每個索引都必須通過 guard。
`state_invariant` 證 increasing-index 與固定 prefix；`prefix_reachable`／`mem_candidates`
消除「目標 prefix 已在候選集」前提。`worker_reachable` 到達完整目標；
`split_graph_complete` 接上圖層 R1+SYM、唯一 retained owner 與 terminal recording guard。
包含空 prefix／suffix 與 direct 分支；不要求記錄時 start=E。

**明列前提／仍未證**：目標路徑每次加邊後的 oracle 接受仍是明確前提，未證 planarity oracle。
本輪形式化的是有限集合上的控制可達關係，並非 Python 程式 refinement；
Python bit 操作／建表、graph mutation／完整 boundary-apex representation、染色表與 scheduler
仍未形式化。唯一性是 task label 唯一，不是 scheduler 恰執行一次。$K_\infty=K_5$ 仍為猜想。
下一個可接續缺口是有限集合與 bit 編碼／運算的 refinement；平面性與 scheduler 分開處理。

驗證：`lake build`、`ReducedDFSAudit`、既有 prefix／viable／graph bridge checkers 的 `--check`、
`git diff --check` 通過。新模組無 warning；既有 warnings 保留。
[公理輸出](../artifacts/c5_cells/dfs-lean-audit.txt) 無 `sorryAx`／native 公理。
production replay 仍為 k=3 的 645 tasks、205 張倖存圖；没有新增 catalogue 搜尋。
沒有改 production 或 `cells.json`；本輪與既有本地修改均保留，未 commit／push。

```bash
lake build
lake env lean Math/ReducedDFSAudit.lean
uv run --with rustworkx==0.17.1 python scripts/c5_prefix_check.py --check
uv run --with rustworkx==0.17.1 python scripts/c5_viable_check.py --check
uv run --with rustworkx==0.17.1 python scripts/c5_graph_bridge_check.py --check
git diff --check
```

## 先前停止點：圖層與 incidence／搜尋狀態已接通（2026-09-14）

本輪依使用者指定，完成 degree、attachment mask 的 bridge。詳細規格見
[c5_cell_enumerator.md §12](c5_cell_enumerator.md)。

**proved in Lean**：新 [Math/ReducedGraphBridge.lean](../Math/ReducedGraphBridge.lean)，已匯入
`Math.lean`。對任意 k 具體定義 production interior-edge index 與 `touch`，證邊索引單射、
鄰居與 incident edge 一一對應；`degree_eq_graph`、`attValue_eq_attMask` 把有限集合的 degree／
attachment 值等同於實際圖的 degree／`Sym.attMask`。`survivor_iff` 雙向連接圖層 R1+SYM；
`viable_of_graph`、`graph_rejection_sound`、`retained_graph_owner` 接上 prefix 剪枝與 ownership。

`Represents G M` 精確表示所有 interior edges；`encode G` 與 `represents_encode` 給出具體實例，
`represents_with_chords` 允許任意五個 chord bits。boundary-only adjacency 不在此 representation
內，因此不能由它推完整圖相等或同 Σ。`touch` 包含較晚 blocks 的內點邊，沒有漏算 degree。

**computationally verified**：新 `scripts/c5_graph_bridge_check.py` 核對 k≤2 的 **66,592** 張圖、
**132,096** 個內點觀測：graph↔interior encoding round trip、degree、attachment 全部零差異。
另核對 k=0..12 的 layout，兩項負控制通過。報告 `artifacts/c5_cells/graph_bridge_check.json`。

驗證：`lake build`、新公理審計、新 checker `--check`、既有 viable checker `--check`、
`git diff --check` 通過。新模組無 warning；既有 build warnings 保留。
公理輸出 `artifacts/c5_cells/graph-bridge-lean-audit.txt` 無 `sorryAx`／native 公理。

**仍未證／下一步**：Python shift/popcount／建表執行、DFS reachability、平行 scheduler、
planarity oracle 尚未形式化；`retained_graph_owner` 仍需目標 prefix 已在候選集。
下一個可接續工作是把遞迴搜尋狀態轉移與 prefix reachability 接上此圖層 bridge。
本輪未改 production／`cells.json`、未擴大 catalogue 搜尋、未加強剪枝；$K_\infty=K_5$ 仍為猜想。
本輪及先前本地修改均保留，未 commit／push。

```bash
lake build
lake env lean Math/ReducedGraphBridgeAudit.lean
uv run --with rustworkx==0.17.1 python scripts/c5_graph_bridge_check.py --check
uv run --with rustworkx==0.17.1 python scripts/c5_viable_check.py --check
git diff --check
```

## 先前停止點：`viable` 剪枝可靠性已 Lean 化（2026-09-14）

使用者要求繼續，本輪完成上一個停止點列出的 `viable` soundness。
完整規格、定理與可完成性反例見 [c5_cell_enumerator.md §11](c5_cell_enumerator.md)。

**proved in Lean**：新 [Math/ReducedViable.lean](../Math/ReducedViable.lean)，已匯入 `Math.lean`。
`blockStart` 明確跟隨 production block 大小；`degree_upper` 證目前選中＋尚可選的 degree 上界，
`previous_block_fixed` 證上一個 attachment mask 已定案。`viable_of_survivor` 保證任意 k 的
R1+SYM 完成圖之所有 prefix 都通過有限集合模型的 `Viable`；`rejection_sound` 排除任何合法完成。
`retained_owner` 已銜接上一輪 `covered_iff`，保證候選集中的合法 owner 不被這項過濾丟失。

**computationally verified**：新 `scripts/c5_viable_check.py` 不使用 DFS 或平面性，從 $k=0,1,2$
的完整邊宇宙直接求所有 R1+SYM 圖，再投影各 cut 的確實可完成 prefixes。全部 **133,181** 個
部分狀態與 production 比較，零誤剪、零有限集合規格差異；終端 guard 與 R1+SYM 完整條件一致。
另只檢查 $k=0..12$ 的 block layout，沒有大 k 搜尋。報告 `artifacts/c5_cells/viable_check.json`。

**新觀察**：k=2 有 3,264 個 `viable=True` 但不存在 R1+SYM 完成圖的前綴。首例 `(cut=11,mask=224)`：
$x_0$ 已接 boundary 0、1、2（mask 7）；$x_1$ 的 boundary bit 0 已排除。degree 要求迫使兩內點相連，
且 $x_1$ 至少還需三個 attachment bits，最小 mask 14>7，違反 SYM。這是通過條件保守，不是剪枝錯誤。
production `viable` 不能被當作精確的「是否有完成圖」oracle。

**界線**：Lean 使用明示的有限 incidence table `touch`，還未證它與實際 graph.degree 的 bridge；
Python shift/popcount／建表／DFS reachability／planarity oracle 仍非已形式化。`retained_owner` 保留
「目標 prefix 已在原候選集」的前提。本輪不改 production 或 `cells.json`，沒有新 catalogue 搜尋；
$K_\infty=K_5$ 仍是猜想。前幾輪的本地修改已保留，尚未 commit／push。

重現：

本輪 `lake build`、公理審計、checker `--check` 與 `git diff --check` 均通過；新模組無 warning。
公理輸出 `artifacts/c5_cells/viable-lean-audit.txt` 僅含 `propext`／`Classical.choice`／`Quot.sound`，
沒有 `sorryAx`／native 公理。build 仍有既有 `AttachmentOrder`／`SymRelabel` warnings。

```bash
lake build
lake env lean Math/ReducedViableAudit.lean
uv run --with rustworkx==0.17.1 python scripts/c5_viable_check.py --check
git diff --check
```

**後續方向**：優先補 incidence table／bit 編碼與 graph degree、attachment mask 的 bridge，
使現有 graph 層 R1／SYM 與此次搜尋狀態層直接相接。另一個有具體反例支撐的方向，是把 degree
所需 attachment 數目與 numeric mask 上界結合成更強剪枝；目前僅記錄，未修改 production。

## 先前停止點：prefix 平行切分的唯一歸屬與 production replay（2026-09-14）

使用者要求「繼續下一步」，本輪完成前述 prefix 切分研究。詳細證明與信任邊界在
[c5_cell_enumerator.md §10](c5_cell_enumerator.md)。

**proved in Lean**：[Math/PrefixPartition.lean](../Math/PrefixPartition.lean)，已由 `Math.lean` 匯入。
對任何有限邊集合 $M$、任何 cut $p$，task 的唯一可能標籤是 $M\cap[0,p)$。
`unique_owner`／`owners_equal` 證唯一性；`covered_iff` 精確指出剪枝後覆蓋當且僅當這個 prefix
被保留；`owner_at_end` 處理全邊皆在 prefix 的 direct-record 情況。普通證明，沒有 native finite check。
這是集合分割定理，不是 Python DFS 或 scheduler 的形式化證明。

**紙面程式論證**：`dfs_prefix` 每次進入都 append 候選，不是只 append 最後索引到 cut 的圖。
嚴格遞增的已選索引給每個 label 唯一路徑；§9 的剪枝可靠性保證合法目標的 prefix 被保留。
`prefix<E` 時 parent 完全不 record，全部交 worker；`prefix=E` 時 parent 直接 record，完全不啟動
worker。順帶修正 §9 的「必須到 `start=E` 才記錄」說法：實際 `_record` 在每次 DFS 進入時執行。

**computationally verified**：新 `scripts/c5_prefix_check.py` 比對 actual production 單一 `_dfs`、
逆序同步執行實際 `_task`、真正的雙程序 Pool，保留完整帶標號 mask 多重集、Σ、count、witness。
$k=0,1,2$ 走 direct 分支，倖存圖數 11／11／30；$k=3$ 有 645 個 tasks、205 張倖存圖、61 個
此層倖存 Σ keys，三路逐图一致且每圖只記錄一次。另檢查每次同步 record 的 graph/mask、成功記錄的
完整染色表 AND、每個 task 的 graph 恢復與完成順序無關性；移除有產出 task／重複 task 的負控制均被拒絕。
純集合模型另窮舉 $E=0..9$ 的 55 個 cut 情境、9,217 組 target/cut。

報告 `artifacts/c5_cells/prefix_check.json` 含來源與 `cells.json` hash；`--check` 逐 byte replay。
沒有改 production enumerator 或 `cells.json`，沒有新跑 $k\ge4$。表中是 reduced 倖存者，不能當
nested catalogue 的 $K_k$。Python/pruning/planarity 的完整正確性與 $K_\infty=K_5$ 仍未證明。

重現：

本輪 `lake build`、`PrefixPartitionAudit`、checker `--check` 與 `git diff --check` 均通過；
新模組無 warning，build 仍有既有 `AttachmentOrder`／`SymRelabel` warnings。
公理輸出 `artifacts/c5_cells/prefix-lean-audit.txt` 只有 `propext`／`Classical.choice`／`Quot.sound`，
無 `sorryAx`／native 公理。

```bash
uv run --with rustworkx==0.17.1 python scripts/c5_prefix_check.py --check
lake build
lake env lean Math/PrefixPartitionAudit.lean
git diff --check
```

**下一個明確問題**：把 §9.4 的 `viable` soundness 寫進 Lean——degree 的已選＋尚可選上界，
以及 SYM 前一 block 已定案／目前 block 只能增加的比較。這可接上 `covered_iff` 所保留的 obligation。
本輪只完成 prefix；未開始這段新證明。所有修改仍在本地，未 commit／push。

## 先前停止點：自行選題研究，補齊 SYM 排序定理並修正 checker（2026-09-14）

使用者要求「看一下有什麼方向值得挖並自行開始研究」，因此恢復一輪有界研究。
依目前證據，方向優先序如下：

1. **reduced 搜尋的完整性鏈**：已有 R1 與重標不變性，可逐段消除未形式化環節。
   本輪選定並完成 attachment-mask 搬運與排序代表存在性；同時發現並修正 checker 的語意錯誤。
2. **前綴平行切分是否完整且不重複**：§9 尚未涵蓋 `dfs_prefix` 的覆蓋；下一個明確問題是
   對每個目標邊集合證明它恰屬於一個 prefix task，並核對 prefix 上提前 `_record` 的部分。
   應先做可重驗的有限集合分割模型，再銜接 production；尚未開始。
3. **$K_\infty=K_5$ 的結構性原因**：需要任意大 cell 的 reduction／不可約障礙定理。
   目前有限目錄穩定不足以推出此命題；R2 的一般充分性及 disk replacement 幾何仍是難點。

**proved in Lean**：新 [Math/SymNormalForm.lean](../Math/SymNormalForm.lean)，已由 `Math.lean` 匯入。
`attMask` 以固定 boundary 次序編碼五 bit；`attMask_relabel` 證搬運；`interiorPerm` 明確延伸
內點置換並逐點固定 boundary；`exists_sorted_relabel` 對**任意 $k$**給出非遞增 masks 的重標代表，
且完整 $\Sigma$ 與原圖相等。包含空內部與 mask 相同的情況，不用 native finite check。

**checker 修正與 computationally verified**：SYM 不是 orbit union；正確要求是每個 orbit 至少
保留一個代表。舊報告其實已記錄 k=2 有 31,744 個 split orbits。另 mask 數值排序與 attachment
數目排序互不蘊含，舊 A3 誤查後者；已改查數值排序。A3／A4 的丟失代表以及 A4 規格／production
mismatch 現在會拋錯。重新跑 $k=0,1,2$ 全宇宙，k=2 的 33,792 個 orbit **零丟失**、production
**零 mismatch**；數值／數目排序分歧 14,080 張（numeric-only 3,520；size-only 10,560）。
新報告 `artifacts/c5_cells/sym_check_quick.json`；舊 `sym_check.json` 保留為歷史輸出，不能當新版 A3。

**界線**：本輪完成圖層 SYM 排序存在性，沒有形式化 Python DFS／bit 操作／平行切分，沒有重跑
$k\ge3$ 全宇宙或新 cell 搜尋。`cells.json` 未變；$K_6=K_5$／$K_7=K_5$ 仍為條件式結果，
$K_\infty=K_5$ 仍是猜想。下方舊停止點中的「排序未 Lean 化」與「orbit union」由本節更正。

驗證入口：

本輪 `lake build`、公理審計、quick checker、`git diff --check` 均通過。新模組無 warning；
build 仍有既有 `AttachmentOrder`／`SymRelabel` warnings。公理輸出保存在
`artifacts/sym_relabel/normal-form-lean-audit.txt`，只有 `propext`／`Classical.choice`／`Quot.sound`，
無 `sorryAx`／native 公理。另以記憶體內注入錯誤確認 A3 缺代表、A4 production 不一致會拋錯。

```bash
lake build
lake env lean Math/SymNormalFormAudit.lean
uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/c5_sym_check.py --quick
git diff --check
```

## 先前停止點：SYM 已拆解為「Lean 核心 ＋ 窮舉 checker」（2026-09-13）

使用者要求：證明重新標號 interior vertices 不改變 C5 boundary-colouring feasibility，因此不改變
10-bit Σ key；並核對 production enumerator 的 canonicalization 是否只依賴此等價。
**只做 SYM**：沒碰 R1、R2、$k\ge6$、$K_6=K_5$，也沒改 catalogue 或 `cells.json`。
完整規格、定理表與 checker 覆蓋在 [c5_cell_enumerator.md](c5_cell_enumerator.md) §7。

**proved in Lean（新增 `Math/SymRelabel.lean`，namespace `FiveBoundary.Sym`）**：設 $\pi$ 是固定
boundary 逐點的置換、`relabel π G := G.comap π`，則

$$\Sigma(\texttt{relabel}\,\pi\,G)=\Sigma(G)\qquad(\texttt{Sigma\_relabel}),$$

逐 bit 形式 `sigma_iff_relabel`、cell 座標特例 `Sigma_relabel_interior`、
「兩個固定 boundary 的 relabelling 同 $\Sigma$」`Sigma_relabel_eq`、染色對應
`proper_relabel`（$\mathrm{Proper}(\texttt{relabel}\,\pi\,G)\,c\iff\mathrm{Proper}\,G\,(c\circ\pi^{-1})$）。
**推論**：十 bit 的每一 bit 是 unlabeled 內部的性質，所以同一個 unlabeled 圖的任兩個標號有相同的
10-bit 輸出，reduced enumerator 用它當 key 合法。公理審計
`artifacts/sym_relabel/lean-audit.txt`：這些定理只有 `propext`／`Quot.sound`，沒有 `sorryAx`／native 公理
（`patternOrder_length`／`patternOrder_toFinset` 兩條 list 事實另有 `native_decide` 計算公理）。

**computationally verified（`scripts/c5_sym_check.py` → `artifacts/c5_cells/sym_check.json`）**：
production 的 SYM canonicalization 只依賴這個等價 ——
`interior_perm_maps` 與獨立重寫的 relabel map 相同且生成 $S_k$（`A1`）；
attachment mask 的多重集在 relabelling 下不變（`A2`，$k=3$ 抽驗 5,991,865 次）；
**全宇宙**每張圖都有非遞增 relabelling（`A3`：$k\le3$ 的 $2^5/2^{10}/2^{16}/2^{23}$ 個 graph，
`without_sorted_relabel = 0`；舊 A3 實際查數目排序，見最新更正）；SYM 與規格逐圖相同（`A4`，
舊「orbit union」解讀有誤，見最新停止點）；
R1 倖存者中每個 orbit 至少留一個 SYM 代表（`A4'`）；`cells.json` 的 `canonical_masks` 是 orbit
最大值計數，每 orbit 恰一個（`A5`／`A5'`，$k_{\mathrm{eff}}\le3$ 的 76 個 witness 全過）。

**沒做、也不主張**：
* SYM 的**鴿籠步驟**（每個 unlabeled 圖都有非遞增 mask 代表＝把內點按 mask 排序）與 attachment mask
  的搬運**尚未 Lean 化**，只有 §7.3 的窮舉驗證；`Math/SymRelabel.lean` 明確標示 6.1 的定理不依賴它們。
* $k=4,5$ 的 orbit 檢查沒跑（production `interior_perm_maps` 只建到 $k\le3$；$2^{31}$／$2^{40}$ 不可行）。
* R1／R2 沒動；沒有跑 $k\ge6$；$K_6=K_5$／$K_\infty=K_5$ 的信任層級不變（§6.0 的前提表已按此更新：
  第 2 條拆成 2a「$\Sigma$ 與標號無關」＝已 Lean 化、2b「鴿籠排序」＝未 Lean 化）。
* 既有保留不變：catalogue 不取 D5 商、mask 是帶標號 key、幾何（apex-planarity）不在這條鏈上。

重現：

```bash
lake build && lake env lean Math/SymRelabelAudit.lean          # 公理審計 → artifacts/sym_relabel/lean-audit.txt
uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/c5_sym_check.py --quick          # ~1 min
uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/c5_sym_check.py --k 2 --k 3      # k<=3 全宇宙
```

## 先前停止點：C5 cell 的 10-bit mask ≡ Σ bridge 已對齊（2026-09-13）

使用者要求建立並驗證「`c5_cell_enumerator.py` 的十 bit mask ≡ 規格 $\Sigma$」——只做表示／語意對齊，
不新增數學搜尋結果。規格、production 對照表、逐域覆蓋與信任層級在
[c5_cell_enumerator.md](c5_cell_enumerator.md) §0；checker 是 `scripts/c5_sigma_bridge.py`，
報告 `artifacts/c5_cells/sigma_bridge.json`。

**結果（computationally verified，不是 Lean 定理）**：production 的十 bit 與獨立 reference $\Sigma$ **逐 bit 相等，零 mismatch**。
覆蓋：$k\le3$ 是**全宇宙**（$U(k)$ 的每一個邊子集，$2^5/2^{10}/2^{16}/2^{23}$ 個 graph，含非平面者）；
$k=4$ 走 DFS 接受節點（20,904,415 個，exhaustive）；$k\le5$ catalogue 的 132 個 witness 全過（含空內部、chords-only、$k_{\mathrm{eff}}=1..5$）；
另加 20 個手工極端 case（邊界 $K_4$／$K_5$、孤立內點、內點 $K_4$／$K_5$…）與 60 個隨機 graph。
checker 用三條互相獨立的路線（boundary-first 回溯、逐 orbit 代表元可行性、$4^{5+k}$ 全枚舉）對 production
（production `compat_tables` + `_record`；DFS 模式連 AND 摺疊都跑 production 自己的 `_dfs`，用 spy 掛 `_record` 取 mask）對撞；
S4 orbit 不變性另抽驗 200 節點／$k$，零失敗。

**沒做、也不主張**：沒有 Lean 化 SYM；R1／R2 沒動；沒有跑新的 $k=6,7$ 搜尋，也沒有 $k\ge8$；
$K_6=K_5$／$K_\infty=K_5$ 的信任層級不變（bridge 只覆蓋 $k\le5$ 的 mask 語義，而且 $k=4$ 只覆蓋 enumerator 接受的節點）；
沒有改 catalogue 定義或 D5 商規則；`cells.json` 沒有被改寫（checker 只讀，並在報告裡記 sha256），
132 個 key 與 nested 計數 11／22／52／87／112／132 由 witness 邊集反向重算後完全一致。

重現（`--quick` 是約 20 秒的例行版，寫 `sigma_bridge_quick.json`；完整版寫 `sigma_bridge.json`）：

```bash
uv run --with networkx==3.5 --with rustworkx==0.17.1 python scripts/c5_sigma_bridge.py --quick
uv run --with networkx==3.5 --with rustworkx==0.17.1 python scripts/c5_sigma_bridge.py \
  --cases --product --catalogue --random 60 --all-masks 0 --all-masks 1 --all-masks 2 --all-masks 3 --dfs 2 --dfs 3 --dfs 4
```

## 先前停止點：R1 已 Lean 化

使用者指定目前最該補的 Lean 是 R1（優先級明顯高於 SYM／enumerator bridge／R2）。
已在 `Math/LocalClosure.lean` 證明：密封私有頂點 $\deg(v)\le 3$ 時

\[
\operatorname{Summary}(g,b)\iff\operatorname{Summary}(g-v,b),
\]

並推出 C5 形式 $\Sigma(G)=\Sigma(G-v)$。核心 lemma 是「cardinality $\le 3$ 的顏色集合必有剩餘色」；
`two_step_free` 現在是它的 degree-2 特例。公理審計在 `artifacts/local_closure/lean-audit.txt`，
無 `sorryAx`／native 公理。

$K_6=K_5$、$K_7=K_5$ 現在少掉 R1 這個數學信任缺口；剩下最大的缺口是
「Python reduced search 是否正確實作 R1+SYM」，以及仍未 Lean 化的 SYM。
R2 的染色 replacement 已由既有 `replacement` 保證，disk／planarity 幾何條件仍留在拓撲信任層，不急著整塊 Lean 化。

驗證：`lake build`、`lake env lean Math/LocalClosureAudit.lean`。沒有重跑 $k=6,7$ 搜尋。

## 先前停止點：等待使用者整理數據

使用者要求「先到這」，本輪完成交接後 commit + push，研究暫停。
接手先讀 [討論表示法](state_language.md) → [可重驗觀察表](../artifacts/state_views/examples.md)
→ [局部封環研究](local_closure.md)。等待使用者提供整理後的數據或指定問題，
不要自動開新搜尋、擴充活動面 grammar、研究博弈策略，或繼續下方歷史 fan 5 工作。

目前可用：圖介面分離與完整關係替換的 Lean 證明、固定端點非交叉路徑的摘要定理與有限分類、
多起點分支／接合／預選／強迫的統一表示法，以及同一 C5 的具體觀察表。
一般移動前緣的充分幾何狀態仍未建立；State／Choice 是討論規格，不能當已實作的通用引擎。
所有 proved in Lean、computationally observed 與 conjectured 邊界見各文件。

本輪驗證已完成：`lake build`（新模組無 warning；既有 AttachmentOrder warnings）、
`lake env lean Math/LocalClosureAudit.lean`（輸出在 `artifacts/local_closure/lean-audit.txt`，
無 sorryAx／native 公理）、兩個 Python `--check`、文件連結與 `git diff --check`。
沒有待續的背景研究或待補的數學驗證；後續修改才需依範圍重驗。

重現入口：

```bash
python scripts/local_closure.py --check
python scripts/state_views.py --check
lake build
lake env lean Math/LocalClosureAudit.lean
```

可貼給接手者：

> 先讀 docs/HANDOFF.md 最新停止點、docs/state_language.md、artifacts/state_views/examples.md。
> 我正在整理數據，先使用既有表示法理解接下來提供的材料。研究目前暫停，不自動擴大枚舉、
> 開活動面 grammar 或博弈控制。染色完整關係與幾何合法性分開；Choice 是替代方案，join 是同時約束。

## 2026-09-13 C5 cell 窮舉器：C5 邊界＋密封內部，只暴露 Σ；reduction 跳過 $k=6,7$

使用者問「C5 能不能當子結構：C5 boundary＋內部結構＋外部 attachments，只把內部對邊界的限制往外暴露」，
並要求設計窮舉器。設計與觀察在 [c5_cell_enumerator.md](c5_cell_enumerator.md)。
答案：可以，條件是內部**密封**（不再有未來邊／預染色／共享 frame）且 **C5 在內側是 face**；
染色側由既有 Lean `summary_glue`／`seal_future` 保證無損，幾何側靠「兩個 disk 沿 C5 黏合必平面」（拓撲信任）。
窮舉器分三層：inner（k 個私有頂點的全部邊集，含 chords；DFS＋apex-planarity 剪枝；只以十 bit Σ 去重；`--jobs` 前綴切子樹平行）
→ exposure（D5 對齊、AND、condition、residual automaton、dead prefix、pp 原子）→ outer（另一個 cell／承諾顏色 reader／pp context）。

**Computationally observed：** 精確枚舉 $k\le5$（$2^{40}$，30 workers 17 min，`--check` 零錯）：nested catalogue
$|K_0..K_5|$ = 11／22／52／87／112／132；原 K3 grammar 42 個與五邊形 grammar 87 個 Σ 全在 $K_5$；
允許 chords 後三色 profile 可為 1，profile 2 不再必相鄰；separating C5 的 meet 涵蓋全部 1,023 個非空 mask，
最便宜 BAD 是 chord `[0,2]` ∧ chords `[0,3],[1,3]`（boundary $K_4$），exact $T_4$ 需 $3+3$；residual mask 193 種。

**Reduction（`scripts/c5_cell_reduced.py`）：** R1（內點 degree $\le3$ 可刪）＋SYM（attachment mask 非遞增）當單調剪枝，
把 $k=5$ 從 17 min 壓到 2.6 s、$k=6$ 66 s；$k\le5$ 新 Σ 與精確枚舉逐一相同。R2（長度 $\le5$ 分隔環、inside relation 有較小 disk
實現；自舉自 C3／C4／C5 目錄）在 $k=3,4,5$ 恰好把「Σ 舊」倖存者全部約掉、「Σ 新」倖存者全部不可約。
**$K_6=K_5=K_7=132$，但這是條件式結論（前提見 §7.0）：精確枚舉在 $k\ge6$ 不可行（$2^{50}$、$2^{60}$），
$k=6,7$ 的數字全來自 reduced 搜尋。R1 引理（內點 degree $\le3$ 可刪）現已 Lean 化（`summary_eq_deletePrivate`、
`sigma_eq_delete_private`）；仍依賴 SYM 的鴿籠步驟（未 Lean 化；SYM 的核心「$\Sigma$ 與標號無關」已於 `Math/SymRelabel.lean` 證明，
見上方最新停止點），以及「程式正確實作兩者」（只在 $k\le5$ 以精確枚舉驗證）。
$K_\infty=K_5$ 更弱，仍是 conjectured。**
未做：SYM 的 Lean 化、把 R2 做成生成階段剪枝以攻 $k\ge8$、
nested cell 的 annulus relation、從 strip grammar 自動抽可密封 5-cycle。
（**已補**：C5 enumerator ↔ 10-bit $\Sigma$ 語意 bridge，見上方最新停止點與
[c5_cell_enumerator.md](c5_cell_enumerator.md) §0；那是表示對齊，不是 SYM 或 $K_6=K_5$ 的證明。）

```bash
uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/c5_cell_enumerator.py --k 5 --jobs 30
uv run --with networkx==3.5 python scripts/c5_cell_enumerator.py --check
uv run --with rustworkx==0.17.1 python scripts/c5_cell_reduced.py --k 6 --jobs 30 --r2
```

## 2026-09-13 C5 cell 十 bit mask ↔ Σ bridge（表示對齊）

使用者要求把「`c5_cell_enumerator.py` 的十 bit mask」與「Lean／文件裡的 $\Sigma$」對齊，並回答
「對任意被 checker 接受的 C5 cell graph，production 的十 bit 是否逐 bit 等於規格？」。
完整規格在 [c5_cell_enumerator.md](c5_cell_enumerator.md) §0，checker 是 `scripts/c5_sigma_bridge.py`。

規格要點：cell graph 是 $(k,M)$，$M\subseteq U(k)$（5 chords＋$5k$ attachments＋$\binom k2$ interior 邊，
邊界 C5 不佔 bit）；bit $j$ = 1 ⟺ 第 $j$ 個 pattern（`PATTERN_ORDER`＝`REPS`＝兩個 library 的順序）這個
$S_4$ orbit 有**至少一個**合法內部延伸；$S_4$（全域換色）進 key，$D_5$（邊界重標）不進 key，
只在外部對齊時用——所以 `bits` 是帶標號的 key，132 個 Σ 是 24 個 $D_5$ orbits。

做法：reference 完全照定義重寫（boundary-first 回溯、逐 orbit 代表元可行性、$4^{5+k}$ 全枚舉三條路線），
`PATTERN_ORDER` 與 orbit 代表元也在 checker 內重新推導再與 production／兩個 library 比對；
production 那側在 DFS 模式直接跑 `enumerate_cells`，spy 掛 `_record` 逐節點取 mask。
$k\le3$ 全宇宙（所有邊子集）＋$k=4$ DFS 接受節點＋$k\le5$ 全部 132 個 catalogue witness＋20 個手工極端 case
＋60 個隨機 graph，全部零 mismatch，逐 bit 相等；`cells.json` 未被改寫，catalogue 數字不變。
信任層級：**executable checked／computationally verified（有限域），不是 Lean 證明**，也沒有覆蓋 $k\ge6$。

## 2026-09-13 討論表示法與觀察表

使用者要求先整理表述，方便討論多起點延伸、接合、預選分化與狀態強迫。
統一入口：[state_language.md](state_language.md)，採 `Interface / State / Branch / Choice` 四個物件，
以及 `condition / split / join / forget / query / compat / view` 七個動詞。
明確區分替代選擇 Choice、限制同時成立 join、已證等效才合併的 deduplicate。
這是表示法規格；一般幾何 State／Choice API 尚未實作，不能把候選摘要當已證充分狀態。

[狀態觀察表](../artifacts/state_views/examples.md) 可直接看完整色型、相容矩陣與條件強迫。
`python scripts/state_views.py --check` 以既有 loader 核對 catalog，重算七份狀態、四個接合格，
用全域色置換展開的 labeled rows 重驗交集、條件化與 query，逐 byte 比對文件。
本輪只有表示法文件與觀察表工具，沒有新圖搜尋／Lean 定理；幾何仍分別標示。

## 2026-09-13 局部封環與固定端點接線：第一輪

後續提問：週期／博弈式控制依使用者要求僅記為未來注意事項，見 `local_closure.md` §8，不啟動該研究線。

使用者提出施工邊界內凹、局部封環及有限狀態問題，授權開始研究。
新入口：[local_closure.md](local_closure.md)。原 fan 5 停止點保留為另一研究線，沒有開始 fan 6。

**proved in Lean（普通證明）：** `Math/LocalClosure.lean` 的實際 simple-graph 接合
`summary_glue`、任意 separated graph context 的 `replacement`、正確消去／空關係剪枝、
`relation_count` = $2^{4^k}$、degree-two path 色中性與 hub 的缺色條件，
以及 R1：密封私有頂點 $\deg(v)\le 3$ 時 `summary_eq_deletePrivate`／C5 形式 `sigma_eq_delete_private`。
`Math/LocalWiring.lean` 對 fixed-endpoint pairwise-conflict grammar 證明 forbidden-set
摘要更新封閉、全部未來 context 等價 iff 摘要相等，並實例化交錯 chord grammar。

**computationally observed：** 固定 3／4／5／6 個有序端點的非交叉路徑插入 grammar，
活 residual 1／3／11／45 類（含可達 dead：1／4／12／46）。全 support、轉移與 separator replay。
C4 wheel 封閉中心留下「不能用滿四色」，84→60 個賦色，但所有 pair projections 相同。
P=0–x–2、Q=1–y–3 與共同 T=0–z–2 的四份完整染色關係皆為 84；P+T 可同側，Q+T 有交錯／apex K5 subdivision 障礙。
具体圖著色、座標與 subdivision 檢查已完成；topology implication 未 Lean 化。

重現：`python scripts/local_closure.py --check`、`lake build`、
`lake env lean Math/LocalClosureAudit.lean`；artifact 在 `artifacts/local_closure/`。
**沒有主張**任意 disk patches 或移動前緣的幾何有限 signature。
下一個有意義的擴充是活動面上的 introduce／close／forget，先檢驗新增端點與面資訊的必要性；
不直接擴大枚舉，不把固定端點純插入模型當一般施工模型。

## 2026-09-13 Obstruction／recovery map：$(3,3,3)$ 起的 trap 結構（§9k）

新增 `scripts/stepwise_trap_structure.py` → `artifacts/stepwise/trap_structure.json`（約 3 秒，`--check` 逐 byte 比對），
研究文件 [§9k](stepwise_state_sufficiency.md#9k-obstructionrecovery-map333-起出現的-trap-是什麼在別的形狀能不能穩定找到)。
同 §9j 模型，31 個形狀（原 16 個 + 含 fan-2 列／fan-4 頂列的 15 個）。

**computationally observed**：

- $(3)^n$ 非邊界列全由下一列與左鄰居決定（$\operatorname{comp}$ 規則），自由只在邊界的 repeat／new 兩步。
  forced cone（三個已知鄰居 ⇒ 第四色）是精確的 trap certificate：horizon = cone 第一個碰撞層 − 1，碰撞只有一種型態。
- trap$(h)$ = 剛性 pattern $P_h$（$(3)^{h+2}$ 唯一的 horizon-$h$ orbit，$h+3$ 列）放在列 $r-h-2..r$、$r\in[h+2,n]$，其他列自由：
  $24(n-1-h)2^{n-2-h}=\sum_r 24\cdot2^{n-2-h}$。走一步 = 同一碰撞頂點的 trap$(h-1,r)$。horizon 1 的 echo 規則與 $(3,3,3)$ 的座標規則逐 configuration 驗證。
- 含 fan-2 列的形狀有 trap（$(2,3,3),(3,2,3,3),(2,2,3,3),\ldots$，horizon 到 2），純 cone 不精確；加上**只對內部頂點**的 case split（邊界永不分支）後 31 個形狀全部精確。
- Recovery map：$R=W_\exists\setminus W_\forall$ 在 31 個形狀都不會回到 $W_\forall$；$(3)^n$ 上 $W_\forall$ 兩步都安全、$R$ 的 repeat 留在 $R$、new 必進 $I$（$\rho\equiv1/2$）。
  fan $\ge4$ 的形狀 $W_\forall=\varnothing$、每類 $g=1$。

**沒有主張**：一般 $n$、任意平面圖、環形、Lean。`check_stepwise.py` 已納入 6 個關鍵數字。

## 2026-09-13 兩層 raw configuration 的未來細分（committed-colour 分層 strip）

新增 `scripts/stepwise_layer_refinement.py` → `artifacts/stepwise/layer_refinement.json`（約 4 秒，`--check` 逐 byte 比對），
研究文件 [§9j](stepwise_state_sufficiency.md#9j-兩層-raw-configuration-的未來細分已承諾顏色的分層-strip)。
模型是明確指定的 instantiation：strip grammar 但**所有引入頂點的顏色都已承諾**，層 = $w$ 個引入步驟的頂點，
$w$ 取到恰好兩層局部（$2w\ge\max f-1$ 且某 $f>w+1$，皆 assert）；raw configuration $=(L_{t-1},L_t)$，action = 合法的整個下一層。

**computationally observed（16 個形狀，完整枚舉＋逐深度 Moore refinement＋獨立整圖 replay）**：

- 辨識 behavioural class 的未來深度 $\le2$（兩層局部性的一般論證；第 2 層在 $(3,3),(5),(6),(7),(3^n)$ 等確實需要）。
- 活類 ⇔ constraint map（下兩層每個頂點的禁用色集合）；dead 只有一類。$(3)$：12 類 $=(b_t,\{b_{t-1},u_{t-2}\})$；
  $(3,3)$：A（robust，24 類）／B（viable 但一步致命，24 類）／dead，規則逐類驗證。
- 可延伸性不局部：$(3)^n$ 有 horizon 到 $n-2$ 的 trap（Q2 lookahead 隨深度增長）；strategy core $36\cdot2^{n-1}-24$、robust core $12\cdot2^{n-1}$、
  活類 $12n2^{n-1}$（$n\le6$ 觀察）；fan $\ge4$ 形狀的 robust core 為空，隨機合法走法 100 層存活 0。
- 存在性邊界 residual 的對照曲線：辨識深度 2–5 個邊界步（$(2,3)$ 為 5），沒有兩層局部性。

**沒有主張**：任意平面圖、環形版本、重染、一般 $n$ 的計數律、Lean。`check_stepwise.py` 已納入 8 個關鍵數字。

## 2026-09-12 Lean 補件：strip 圖語義與 residual 類數下界

新增 `Math/StripGraph.lean`（strip 圖、`Extendable`、附 `search_iff`／`verdict_iff` 正確性證明的回溯著色檢查器、
`residual_injective`）、`scripts/export_stepwise.py` → `Math/StepwiseGenerated.lean`（fan 4／5 代表字、
separator、轉移表；純資料、記錄 JSON SHA-256）、`Math/StepwiseReplay.lean`、`Math/StripGraphAudit.lean`。
**proved in Lean**：`fan4_nerode_lower_bound`／`fan5_nerode_lower_bound`——單列 fan 4／5 的真實可延伸語言
至少有 55／97 個右殘餘；全部 1485／4656 組 separator 由已驗證的檢查器重判，不信任 Python DFA。
`fan5_extendable_iff`：長度 $\le7$ 的全部 21,845 個字上，匯出表格的 live 等於 `Extendable`（有限一致性）。
四個重放定理用 `native_decide`；其餘為普通證明。負控制（竄改 separator／live）會失敗。
**沒有主張**：表格是殘餘自動機（上界）、signature 最小性、雙側 437 類、對齊循環證書的 Lean 實例化、
disk embedding。細節與信任邊界見 [研究文件 §9i](stepwise_state_sufficiency.md#9i-leanstrip-圖語義已驗證的著色檢查器與-residual-類數下界)。
重現：`python scripts/export_stepwise.py --check`、`lake build`、`lake env lean Math/StripGraphAudit.lean`
（審計輸出 `artifacts/stepwise/lean-strip-audit.txt`）。

## 歷史：2026-09-12 fan 5 接手入口（目前不自動續作）

**目前主線：fan 5 的雙側接合，不要開始 fan 6。** 先讀本節及下方雙側摘要，
再讀 [研究文件 §9h](stepwise_state_sufficiency.md#9h-fan-5-雙側接合437-個完整-residual成熟部分-25-類)。
單側最小 signature 的前置結果在 §9f–9g；命名與證明邊界在 §9d。

已完成的工作包括：修正獨立換色 quotient 的充分性判準、移除固定 window 檢驗的任意截止、
泛型 Lean 對齊／更新／pumping 定理、fan 4／5 完整單側分類，以及 fan 5 雙側 437 類最小化。
程式與 JSON 證書一併保存；先利用現有分類，不必重跑前六次歷史搜尋。

**接下來可直接做的研究**：把雙側的 425 種無限語言整理成可讀結構族。
其中成熟 A/A 對應的 24 種交替／奇偶語言已解釋，剩餘 401 種尚未完成結構命名。
從 `fan5_bilateral.json` 的 `classes` 開始：每類含 `left/right` 代表、
`left_delta/right_delta`、語言種類及長度 ≤4 真值向量。
`pair_to_class` 將左右組合映到類別；右側 ID 的意義查 `right_states`，
不能直接把右側 ID 當作單側 ID，應使用其 `reversed_word_class`。
候選結構 signature 應在完整 437 類上驗證雙向更新與類別一一對應，不能只拿樣本無碰撞當證明。

**不可遺失的約定**：沿指定方向首次遇色依序命名 b,c,d；左右框架需保留共同顏色對應。
437 是所有有限中央字（含空字）的固定色標分類；若只剩一洞，允許色集合只有 16 種。
各自換色 orbit、固定 gap 長度的輸出、完整 residual，是不同等價關係。
所有 strip 分類為 computationally observed；proved in Lean 的是泛型定理，加上（見上節）strip 圖語義
與 fan 4／5 的 residual 類數下界 55／97。尚無生成 DFA 的 Lean soundness（上界），也沒有 disk embedding 結論。

本輪可重現檢查（Python 只需標準庫；各 `--check` 重算並逐 byte 比對 artifact）：

```bash
python scripts/stepwise_aligned_reference.py --check
python scripts/stepwise_fan4_quotient.py --check
python scripts/stepwise_fan4_signatures.py --check
python scripts/stepwise_fan5_signatures.py --check
python scripts/stepwise_fan5_bilateral.py --check
python scripts/export_stepwise.py --check
lake build
lake env lean Math/StepwiseStateAudit.lean
lake env lean Math/StripGraphAudit.lean
```

Lean 公理審計輸出保存於 `artifacts/stepwise/lean-state-audit.txt`。
`run_repeat_loop`、`pumped_distinction` 不依賴公理；其餘僅列出標準 `Quot.sound`／`propext`。
上述檢查在本輪提交前重驗；未 push。

## 2026-09-12 fan 5 雙側接合完成第一輪

仍限 fan 5，沒有 fan 6。使用者問左右同時參照後授權開始。
**computationally observed**：K(L,R)={X | LXR 可著色} 的完整固定色標分類為 437 類，
由 97 個左 residual ×97 個右逆像集合的全部 9409 組最小化。
右集合與 reversed-R 的單側類有已驗證轉移雙射；左右需保留共同顏色對應。
細分計數 2→31→267→425→437→437；每類長度≤4 的341-bit向量皆不同，
149017 個 bit 全部獨立整圖 replay，另重驗9409組空字接合。
兩端局部更新均封閉且交換；一洞允許色投影有16種，不能把它當完整gap residual。
成熟 A/A 的1296組壓成25類：1128組無解，其餘為24種指定兩色交替＋長度奇偶語言。
一般437類中：空語言1，有限非空11（{ε} 加至多兩個允許色），無限425。
全部類與轉移已保存；一般425種無限語言尚未全部整理成可讀結構族。
左 cbaba、右 ababc／ababd 在各自框架都是 A_d/A_d，卻分別能填 b／任何gap都無解，
示範相對顏色對應不可省略。未新增Lean strip圖語義證明。
詳見 `docs/stepwise_state_sufficiency.md` §9h；`artifacts/stepwise/fan5_bilateral.json`。
重現：`python scripts/stepwise_fan5_bilateral.py --check`。

## 2026-09-12 fan 5 的 97 類完整解剖

使用者要求先完成 fan 5，**不要繼續 fan 6**。
**computationally observed**：97 個固定色標 residual classes =
E 1＋S 4＋P 12＋U_aba 12＋U_cba 24＋A 36＋F 6＋T 1＋dead 1。
配合指定首次遇色框架為 11 種 signature（含 dead）。
F 只保留允許再填一次的無序兩色集合 B，語言 `{ε} ∪ B`；T 的語言 `{ε}`。
四字 `baba`／`caba` 可與真實內部色域態合併；三字 `aba`／`cba` 必須保留為 U。
成熟 cut 用三色時全部是 T；只用兩色時為 A_cd/A_c/A_d。
與 fan 4 相比，多出的 42 個類全屬長度 3／4 的左端暫態，成熟活 signature 仍只有 A 三種及 T。
先前 `acaba`／`cbaba` 的碰撞解成 T／A_d；分類後不必每態都永久保留第四個邊界色。
全部 822 原始狀態的 3288 次結構更新通過；4656 對 separator 的 9312 端點獨立整圖 replay 通過。
未新增 Lean 圖語義證明。詳見 `docs/stepwise_state_sufficiency.md` §9g；
完整分類、cut 變體、轉移與最小性證書：`artifacts/stepwise/fan5_signatures.json`。
重現：`python scripts/stepwise_fan5_signatures.py --check`。

## 2026-09-12 fan 4 完整 signature → fan 5 collision

**computationally observed**：fan 4 完整最小化為 55 個固定色標 residual classes，
由外部首次遇色框架＋8 種 signature（含 dead）表示：E、S、P、A_cd、A_c、A_d、T、dead。
三字 `aba` 與成熟 `(aba,{c,d})` 合併；三字 `cba` 與成熟 `(aba,{c})` 合併，
所以「是否已引入內部點」不是必要狀態欄位。全部 1485 對都有 separator，兩端皆獨立整圖 replay。
移植同一結構 recipe 到 fan 5 自己的 cut，第一個等長 collision 是 `acba` / `dcba`，
同為虛擬 A_c，接 `b` 前收後拒；第一個成熟 collision 是 `acaba` / `cbaba`，
同為 A_d，接 `b` 前拒後收。遺失的是仍將進入下一 fan 的第四個邊界色。
尚未證明補這一欄已是 fan 5 最小表示，尚未接 Lean。
詳見 `docs/stepwise_state_sufficiency.md` §9f；完整分類、轉移、separator 與著色證書：
`artifacts/stepwise/fan4_signatures.json`；重現：
`python scripts/stepwise_fan4_signatures.py --check`。

## 2026-09-12 fan 4 對 fan 3 quotient 續作

**computationally observed**：最短等長成熟共同活歷史對為 `cbaba` / `cbcba`，
fan 3 完整 cut 同為 `(b,a,d)`，fan 4 接同一 `b` 分別接受／拒絕。
fan 4 的四狀態語義為 `(aba,{c,d})`、`(aba,{c})`、`(aba,{d})`、`(cba,{d})`；
最後一種目前可著色，但任何非空延伸都失敗，殘餘語言為 `{ε}`。
已對全部原始可達狀態驗證成熟 cut 分類與局部轉移，並獨立整圖 replay；未接 Lean。
詳見 `docs/stepwise_state_sufficiency.md` §9e；重現：
`python scripts/stepwise_fan4_quotient.py --check`。

## 2026-09-12 最新續作：對齊參照狀態（試跑七）

使用者已明確指定命名規則：固定方向後，以首次遇到其他顏色的次序命名 $b,c,d$，
$\mathrm{dist}(a,b)<\mathrm{dist}(a,c)<\mathrm{dist}(a,d)$。本輪 strip 方向是向已填歷史回看。
**命名規則不等於特徵摘要；反例否定某個摘要，不能宣稱這個命名本身抹掉 identity，或必須改指向別的 occurrence。**

最新有效結論見 [stepwise_state_sufficiency.md §9d–10](stepwise_state_sufficiency.md#9d-指定方向的對齊參照與局部更新試跑七)。
舊試跑六把殘餘關係各自除以換色，沒有保留與參照框架的對齊，故其「充分」結論需修正。
試跑七對狀態與共同後綴採同一框架；fan 3 已有短反例 $1210$ 與 $2010$，再填 2 時一拒一收，
雖然兩者都恰用 $a,b,c$。應保留的是 frontier 被迫為哪個相對色，而不只是是否被迫。

- **computationally observed（完整有限計算）**：六個形狀 $(3),(4),(2,3),(2,4),(2,2,3),(2,2,4)$
  的對齊殘餘自動機，穩態活狀態數 3、4、12、13、28、41；完整局部更新表已保存。
  狀態 = 顏色參照表＋對齊殘餘類，讀新色後 move-to-front 並同步換色殘餘類。
  全特徵池＋window 3 在三個埋藏 fan 3／深層形狀失敗，均有共同後綴和獨立整圖 replay。
- **computationally observed（完整有限計算）**：六個形狀都有共同循環證書排除任意固定 window。
  舊 `finite_range` 的截止 12 已改成迭代至空集或固定點。
- **proved in Lean**：`Math/StepwiseState.lean` 的泛型換色、register 更新與共同循環保持區分定理，普通證明；
  **尚未**把 Python 表格或 strip 圖語義接到 Lean。審計見 `Math/StepwiseStateAudit.lean`。
- **conjectured／未證**：一般深度的 $|Q|$ 無界與二次／指數成長。深度 $d\le3$ 的數據不能證明無界，
  也不能否定固定種類、內容可變的 registers。舊「任何固定容量都不夠」結論撤回。

入口：`scripts/stepwise_aligned_reference.py`、`artifacts/stepwise/aligned_reference.json`。
`python scripts/stepwise_aligned_reference.py --check` 重做全部新計算、獨立整圖 replay 並逐 byte 比對；
`lake build` 與 `lake env lean Math/StepwiseStateAudit.lean` 檢查形式部分。
下一步保持此命名，從對齊 transition 表反推每色應帶的 latent constraint 資訊，
再用完整 closure 驗證候選的局部更新；不再以樣本或獨立 residual orbit 判充分。

下方六次試跑是歷史記錄；涉及無界成長、單 bit 充分或命名抹掉 identity 的敘述以本節與 §9d–10 修正為準。

## 2026-09-12 最新：逐步填色的資訊充分性（前六次歷史記錄）

使用者提出的新研究問題與四次試跑結果都在 [stepwise_state_sufficiency.md](stepwise_state_sufficiency.md)：
第一部分（第 0–6 節）是問題陳述——把逐步四色填色看成決策樹，問哪些資訊足以判定「存在仍可成功的後繼」（Q1）
與「安全剪枝」（Q2），狀態表示 $S(H)$ 的充分性判準是「同狀態、可被 continuation 區分 ⇒ 不充分」；
第二部分（第 7–11 節）是試跑結果與目前能說的話。

| 試跑 | 檢驗場 | 主要結論 | 腳本 → `artifacts/stepwise/` |
|---|---|---|---|
| 一 | C5：87 個 fan-pentagon patch 為內部，同族 × 10 dihedral 對齊為外部，向前填 $b_0..b_4$ | 未填色歷史永遠可完成（4CT）⇒ 判準必須含已承諾顏色；Σ 的所有壓縮被反例否定；window 3 在深度 4 有 75% 接合圖不充分；$B_{in}\lor B_{out}$ 深度 3 抓不到任何死分支 | `stepwise_sufficiency.py` → `first_run.json` |
| 二 | 同上 | 死分支的局部認證：尾端 ≤2 色 0%、尾端 3 色 12.8%、加色數 78%（多為退化）；只靠 $\Sigma_{in}$ 就死 41.8% | `stepwise_local_fail.py` → `local_fail.json` |
| 三 | 同上，Nerode 不可區分 | window 外需 6／4／3 bits；pair 強迫狀態看不到色數；剩一點 5 個關係夠，剩兩點需完整條件投影關係 | `stepwise_window_state.py` → `window_state.json` |
| 四 | 無限長邊界的一段：平移生成 strip（fan 2／3／4） | fan 2 狀態為空；fan 3／4 只需一個 ± bit「剛封閉 fan 的內部頂點是否被強迫」，window 不需要 | `stepwise_strip.py` → `strip.json` |
| 五 | 同上但精確自動機（左端 + 平移不變、Moore 最小化），內部逐列加深，每列一個 fan 值 | 在 fan 列底下加自由列：類數不變；把 fan 列**埋在** $d$ 層自由列下：穩態 Nerode 類數隨 $d$ 成長（fan 3：2,5,9,14；fan 4：3,8,22,63）；沿邊界重複 $Hu^k$ transient+period ≤6 | `stepwise_strip_width.py` → `strip_width.json` |
| 六 | 同上 10 個形狀；候選 = 以 $a$ 為中心的 window + 其他顏色 $b,c,d$ 的**最近出現**（recency 命名）參照 | 任何有界 window 都不充分（精確）；淺層形狀由 2–4 個 run channel（顏色對 + 長度奇偶／精確到 4）決定；$(2,3)$、$(2,2,4)$ 類 nearest／recency 參照不夠，反例顯示參照必須保留遠端顏色 identity 且相關 occurrence 不一定是最近的——一般的遠端參照模型**未被否定** | `stepwise_remote_reference.py` → `remote_reference.json` |

`python scripts/check_stepwise.py --fast`（約 2 分鐘）重跑六個腳本並比對 40 個關鍵數字，目前全部一致；
不加 `--fast` 約 9 分鐘（多跑 $(2,2,2,3),(2,2,2,4),(2,2,3,3)$ 三個慢形狀，其結果已存在 JSON 裡）。
**全部 computationally observed，沒有 Lean 結果。**

第 3 節已改寫成 $S_n=(a_{n-1},a_n,a_{n+1},q_n)$、$q_n$ = 歷史對未來的 Myhill–Nerode 等價類，並加入使用者的兩點：
$a,b,c,d$ 是**四種顏色本身**、$b^\pm,c^\pm,d^\pm$ 不是三個 bit（$b^\pm$ = 顏色 $b$ 在 $\pm$ 方向上一個**相關的**、距離不限的 occurrence 參照，不預設是最近的），以及
「有限作用距離 ≠ 有限狀態」——要找的是有限記憶、無界傳播距離的規則。試跑六檢驗的是它的 nearest-occurrence 具體版本；下一個問題是「參照該指向哪個 occurrence、能否局部更新」。

目前能說的話（文件第 10 節）：判準的 $H$ 必須含顏色；閉環是 C5 退化的原因；約束列緊貼邊界時狀態是常數個 bit（內部頂點強迫狀態），
但約束列埋在自由列底下時狀態是 cut 上的聯合關係、類數隨深度成長——**任何固定容量的狀態對一般深度不充分**（否定「三 bit」讀法，不否定遠端顏色參照）；
沿邊界拉長的歷史在所有 strip 上都塌縮（有限記憶可跨任意距離），無界需求只來自向內加深；C5 上「必定 fail」多半是 meet 層級事實。
下一步候選（第 11 節）：C6–C8 patch 庫、strip 第一列 gadget 沿邊界混合（fan 2／3 週期）、$|Q(d)|$ 成長律（需狀態換色正規化才跑得動 $d\ge4$）、
外部也做成 strip 取乘積、允許 Kempe 換色、Lean 化（strip 自動機可接 `ColorDFA.lean`）。
待釐清 2、3（是否允許換色、$S$ 是否判合法性）未動。

## 2026-09-12 最新：pp-expression 層

使用者接續要求採用 CSP pp-definability 的下一步；已實作小型 JSON pp 公式，
以明確具名自由／存在變數與 EQ、NEQ、catalog 完整 relation 的原子合取求值。
見 [pp_relations.md](pp_relations.md) 與 `scripts/pp_relations.py`。
本輪以 R767 條件查詢、同 C5 投影、R91∩R935 及無解例子驗證；
`scripts/check_pp_relations.py` 的 106 個公式與七個不合法輸入案例通過。
結論是 **computationally observed**，沒有新增 pp 層的 Lean soundness 證明。
原子保留既有 graph／geometry witness 的來源與 hashes；合成幾何仍 unchecked。

公式、結果與獨立 replay 在 `artifacts/pp_relations/`。未重跑原始枚舉，未啟動
雙 C5／一般 transducer 搜尋或 topology completeness。下方「暫停並 commit + push」
是前一階段歷史停止點；使用者已要求將本輪 pp 變更 commit／push。接手先讀新 pp 文件，
再依需求讀下面原有 boundary relation 背景。

## 2026-09-12 新方向：五邊形內部與同一 C5 的條件強迫庫

使用者已啟動新研究：把內部 K3 換成五邊形 12345 加 13、14，結果見
[fan_pentagon.md](fan_pentagon.md)。完整 `2^25` grammar 的獨立 replay 已完成：
174,456 disk-accepted masks、87 exact Σ（含全部原 42、新增 45）；三色 profiles
仍是原 21 種，最少 2 且大小 2 仍相鄰。全 grammar 結論是 **computationally observed**。
新例子 `mask=1116616 / Σbits=767` 接受 216 個 labeled assignments，恰拒絕 01231
的全域換色；`Math/FanPentagon.lean` 有 exact Σ native 證書與普通局部衝突證明。

最新使用者 scope：**先做 generic boundary relation，但本輪只實作／驗證同一個 C5
boundary 上的 pair forcing；pairwise relation 必須由完整 boundary relation 投影得到，
不要反過來用 pair constraints 代表完整狀態。** 見 [boundary_relations.md](boundary_relations.md)。
`Math/BoundaryRelations.lean` 給泛型 full relation / condition / projection / nonvacuous forcing；
`Math/C5PairForcing.lean` 證 R767 與全體 proper C5 所有 pair projections 相同，卻有不同
conditional forcing。Python catalog 收錄 87 個完整 states 及 750 條派生最小條件推論，
來源、幾何 witness 與計算重驗分開保存。不啟動雙 C5 串接、一般 transducer 或任意 n 搜尋。

本輪驗證已完成：完整 `lake build` 通過（8800 jobs；只有既有 `AttachmentOrder` warnings）；
`Math/FanPentagonAudit.lean` 公理審計通過，無 `sorryAx`，實際輸出
`artifacts/fan_pentagon/lean-audit.txt`。泛型 relation 法則沒有 native 依賴；具體 C5
有限反例及 exact Σ 的 native 依賴已標明。Python 完整 grammar replay、211,410 個
條件 pair 查詢、3,828 對 aligned meet、實際 inside/outside union 染色皆通過。
搜尋四份核心輸出與 relation catalog 重建逐 byte 一致。驗證當時的 source／artifact hashes
保存在 `artifacts/boundary_relations/validation.json`；其中 `source_state` 記錄的是提交前的
驗證快照，並非要求工作樹維持未提交。

**本輪停止點：使用者要求先到這，整理交接後 commit + push。研究已暫停，沒有背景程序
或待完成驗證。** 新對話先讀本節、`docs/boundary_relations.md`、`docs/fan_pentagon.md`，
再看 `Math/BoundaryRelations.lean`、`Math/C5PairForcing.lean` 與
`scripts/boundary_relations.py`。先使用現有 catalog 查詢，不自動重跑完整搜尋。

若使用者要求繼續，接續主題是**同一個 C5 上的多條件強迫，以及真實內外 patches
如何共同實現條件**；保留完整 relation 作主狀態與具名 boundary 對齊。可從
R767 的 `b1=b4 ∧ b0≠b2 ⇒ b0=b3`、R91∩R935 才強迫 `b0=b2` 的例子開始。
下一個研究問題尚未指定；不自行啟動雙 C5 串接、一般 transducer、增加頂點搜尋，
也不自動切回先前的 topology completeness 工作。

接手所需操作與證據：

```bash
python scripts/c5_relation_library.py query 767 --given 'b1=b4' --given 'b0!=b2'
python scripts/c5_relation_library.py meet 91 935
```

* 完整 states 與派生規則：`artifacts/boundary_relations/library.json`。
* 真實內外合成圖：`artifacts/boundary_relations/inside_outside.json`。
* 全庫 query／meet replay：`artifacts/boundary_relations/replay.json`。
* 全 grammar 搜尋／重驗：`artifacts/fan_pentagon/summary.json`、`replay.json`。
* Lean 公理界線：`artifacts/fan_pentagon/lean-audit.txt`。

以下 topology completeness 段落是先前工作的停止點；本輪沒有補上 embedding → endpoint order。

## 先前停止點：triangle topology completeness（歷史背景）

先前已啟動 topology completeness，見 [topology_completeness.md](topology_completeness.md)：一般 triangle disk embedding → 分開共用端點 → 切開 annulus → 端點環序一致的紙上論證已落盤。`Math/AttachmentEndpoints.lean` 證明端點環序 → normal form → `AnnulusAccept` 的編譯接口；**沒有證明 embedding → 端點環序，完整 topology completeness 仍 unresolved in Lean**。若日後明確重啟此線，需獨立 embedding 模型與 Jordan／vertex-star splitting／spanning-arc cutting，不要把端點環序作為 embedding 定義或重做 grammar 分類。

**先前一輪的停止紀錄**：未啟動上述拓撲形式化。該輪完整 `lake build` 通過（8797 jobs；新檔無警告，既有 AttachmentOrder warnings 保留）；`lake env lean Math/AutomataAudit.lean` 通過，兩個新定理只有 `propext / Classical.choice / Quot.sound`，實際輸出在 `artifacts/automata/lean-audit.txt`。該輪未重跑枚舉。這不是本輪的接手指令。

## 30 秒摘要

已建立 Lean 的 exact boundary-coloring relation、有限枚舉、gadget relation algebra 與不信任 Python 的證書重驗流程。固定有序 C5 的 Σ 可以無損壓成十個 S4-orbit bits。

已找到 planar、induced-C5、11 頂點／26 邊的 BAD 圖，且 exact Σ 是全部 120 個四色 boundary assignments。但 C5 是 separating cycle，**不是 disk 外邊界**。

目前方向已從擴大 n 的盲目枚舉，改為 primitive exclusion gadgets → relation library → 反向合成 T4 → 研究幾何接線障礙。最新確認：**即使完整 Σ 相同，接上同一 context 的 disk 合法性仍可能不同**。因此 geometry-aware transition 不能只依賴 Σ。

最新階段 **Finite-state synthesis of triangle disk gadgets**（[automata.md](automata.md)）：在固定 triangle grammar 上，染色與幾何都有沿邊界掃描的有限狀態表示。`ColorDFA` 的 exact Σ 語意對每個 attachment word 都是普通 Lean 證明；`GeometryDFA` 只主張 forward soundness（接受 ⇒ 自建 rotation system 通過 Euler／face checker），其 completeness 仍是 topology gap。Nerode 狀態數、42 個 disk states、1,080 個 T4 ordered realizations、Z5 profile 統計皆為 computationally observed，且只限此 grammar。

2026-09-12 最新：attachment geometry 的 cut-necklace normal form 已雙向 Lean 封口；本輪又完成 **incidence 六種 regime 與飽和分支的 cyclic normal form**。`Math/AttachmentSignature.lean` 證 `(E,X,Z)`（shared junction／singleton／空 boundary 數）只可能是 `(1,4,0),(2,2,1),(2,3,0),(3,0,2),(3,1,1),(3,2,0)`。`A=8` 當且僅當 `(E,X,Z)=(3,2,0)`。

`Math/AttachmentSaturated.lean` 普通證明：三種 junction 都出現、各 packet 非空且 Nodup 時，one-turn ⇔ cyclic word 為 `01 · [1]^y · 12 · [2]^z · 20 · [0]^x`。這個 list theorem 不限制 boundary 長度；C5 飽和時再得到 `x+y+z=2`。因此 degree 型 `(4,2,2)`／`(2,3,3)` 的 singleton 配置與環序都已從幾何推得。**續作 `Math/AttachmentGaps.lean` 已完成三 junction 含空 boundary 的雙向環序：`01 · U · 12 · V · 20 · W`，三段各只允許空 packet 或 singleton 1／2／0，保留原空位。C5 時三段總長為 2，singleton 數加空位數為 2。一／兩 junction 的三個 regimes 也已由下段 AttachmentOrder 涵蓋；GeoReject bridge 現已完成（見下段），不要重做環序分支。**

`Math/AttachmentOrder.lean` 已完成一／兩 junction 的三個 regimes（**proved in Lean**）：`one_junction_normalForm` 給出 `(1,4,0)` 的 C5 形式；`two_junction_cyclic_gaps` 與 `two_junction_gap_inventory` 涵蓋 `(2,2,1)`、`(2,3,0)`，保留空 boundary 位置。六種 incidence regimes 的參數化環序均已涵蓋，後續 GeoReject bridge 現已完成（見下段），不要重做環序分支。

**2026-09-12 最新 bridge 已完成（proved in Lean）**：`Math/GeoRejectBridge.lean` 從 normal form 的 fan ≤ 2、共同鄰居 ≤ 1 與 attachment budget 推出 `runOK_rejection_le_three`。`runOK_three_rejection_structure` 證 `|R|=3` 時 degree 型為 `(2,3,3)`，degree 2 的鄰居為 `{t,t+1}`，`R={t+2,t+3,t+4}`。`normalForm_rejection_bound` 直接以 `AttachmentNormalForm` 為前提。另證 `runOK_profile_ge_two` 與 `runOK_two_profile_adjacent`。不需展開十二類 shape、不枚舉 words，也不引用 native profile 檢查。十二類窮盡性仍是 computationally observed，topology completeness 仍 unresolved。詳見 [attachment_normal_form.md](attachment_normal_form.md)。

2026-09-12 bridge 驗證：完整 `lake build` 通過（8796 jobs；新檔無警告，既有 `AttachmentOrder` linter warnings 保留）。`lake env lean Math/AutomataAudit.lean` 通過；新增 12 個定理的公理依賴均為 `propext / Classical.choice / Quot.sound`，沒有 `sorryAx` 或 native 依賴。實際輸出已更新至 `artifacts/automata/lean-audit.txt`。沒有重跑 word 枚舉或 topology 診斷。

## 1. 使用者要求與禁止事項

2026-09-12 新增研究想法（僅記錄、尚未啟動）：[以額外內部點轉接成 C5 interface](c5_interface_idea.md)。研究 C6／C7 是否在指定 continuation grammar 下可經單一 C5 保持語義；區分可逆編碼的十-orbit 容量限制與一般關係式編碼，後者不能僅因來源狀態超過十個就否定。另記錄五點投影漏掉六點染色 obstruction 的診斷例。此想法不取代既定 normal form → GeoReject 工作順序。

核心問題：是否存在小的、composition-preserving boundary quotient，能描述 relevant planar patches；之後才研究 transition system 的 closed SCC。

* 目前研究順序：先刻畫 attachment geometry 的 normal form，再讓 `GeoReject` 成為 corollary；不要把觀察到的十二類當成證明前提。
* 不直接證四色定理，不以四色定理作搜尋 oracle，不假設 boundary-state conjecture。
* 每個找到的候選保留 deterministic certificate；Lean 重算 graph／boundary／coloring claims，不能信任 Python 的 BAD 結論。
* 區分「平面圖中指定 C5」與「C5 是單側 disk 外邊界」。前者可 BAD，不可偷換成後者的反例。
* 區分已證與計算觀察；不可把有限搜尋無反例外推為一般定理。
* 先做 document-first。除非使用者明確 `/graphify`，或文件無法解釋跨檔架構，不自動跑 Graphify。
* 未獲要求不開 sub-agents、不 commit／push。專案已納入 Git；每輪先檢查實際 `git status`，不要沿用早期「全部 untracked」的歷史狀態，也不可將研究產物視為可刪的臨時檔。

## 2. 信任分類

| 標籤 | 專案中的確切意義 |
| --- | --- |
| proved in Lean | 具名 theorem，沒有 `sorry`、`admit`、手寫四色／boundary 猜想公理。多數有限計算用 `native_decide`，額外信任 native compiler 及生成的計算公理。 |
| computationally observed | Python 枚舉完整性、NetworkX planarity／cofacial 測試、搜尋最小性、拓撲診斷。標準拓撲定理提供解釋，但未因此成為本專案的 Lean theorem。 |
| conjectured / unresolved | geometry signature 的充分性、一般接線 grammar、有限 frontier／closure、尚未定義的 closed SCC。不能作為前提。 |

`#print axioms` 的實際輸出放在各 artifact 目錄的 `lean-audit.txt`。此工具鏈產生 `..._native.native_decide.ax_1_1` 等依賴，不能把 native 決定程序說成純 kernel reduction。

五份三角形 pigeonhole 局部衝突證書用 `decide +kernel`；一般 pigeonhole lemma 是普通證明。這不表示全部染色證書都是純 kernel 計算。

## 3. 基本定義與已完成的有限計算

`Color := Fin 4`；有序 boundary 用 injection。一般 restriction-image 定義為 `SigmaAt`，五邊界版為 `Sigma`：所有能延伸成完整 proper coloring 的 boundary assignments。

```text
GOOD := Σ 中存在使用至多三色的 coloring
BAD  := Σ 非空，且不存在使用至多三色的 coloring
T4   := proper C5 assignments 中恰好使用四色者
```

Lean 枚舉結果：

* C5 proper 4-colorings：240；三色 120，四色 120。
* S4 color orbits：10；再允許 D5 位置作用：2。
* 十個 canonical reps：`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`。
* 兩個 S4×D5 reps：`01012 01023`；這是 **coloring 類**，不是只有兩個 patch states。
* 固定 boundary labels、無預染色／外加 list constraints 時，Σ 是 S4-saturated。十-bit encoding 無損且保持 intersection，全部可能 bitsets 的上界是 1024；不宣稱全部可實現。
* 原始 240-bit mask 的 bit i 是 proper tuples 的 lexicographic order，第 0 bit 為最低位；`artifacts/boundary/summary.json` 有完整 raw order。

當兩塊內部不相交、只共享同一個有序 boundary：`Σ(union)=Σ1∩Σ2`。另有 relational composition `∃y, R1(x,y)∧R2(y,z)`、隱藏 terminals、結合律、S4-equivariance。

獨立 D5 canonicalization 不能省略 relative alignment。已有更強反例：`C5+02` 與 `C5+03` 的整個 Σ 互為 reflection，接固定 context `C5+03+13` 後，一個 BAD、一個 GOOD。

## 4. 已完成的圖搜尋與構造

### 第一階段：n=5,6

全部 1,056 個 labeled C5-supergraphs；883 個 planar，250 個 BAD；250 份候選全由 Lean 重驗。最小 `(n,m)` 是 `(5,8)`，含 boundary K4，Σ 有 48 個 coloring。不是 disk patch。

同面測試通過的 223 張圖沒有 BAD；這只涵蓋 n≤6。

### Induced-C5 搜尋

n=5..9 的 planar edge bound 內候選數分別為：

```text
1, 32, 2,047, 258,096, 61,450,327
```

未找到 planar BAD。**n=10 沒有窮舉**。不能宣稱 11 是全域最小頂點數。搜尋是 computationally observed，不是 Lean 的有界完備性定理。

### 11 頂點構造

兩個 8-vertex disk patches 沿完整 C5 黏合，得到 separating-C5 planar BAD。最初 27 邊，刪 `08` 後為 26 邊，Σ 恰為 T4，120 個 coloring。

刪任一 interior vertex／非 boundary 邊不能保持 BAD；這是 deletion-minimal，不是全域 minimum。保留 induced C5 的單邊 contraction 也未給更小 BAD。

資料：`artifacts/construction/`；圖與兩側接線見 [construction.md](construction.md)。`ConstructedAnalysis.minimal_sigma_exact` 等 theorem 連到語意 Σ。

## 5. 目前的 gadget synthesis

Primitive 已驗證：NEQ、以 K5−xy 實現 EQ、K4 frame 排色與強迫第四色。Frame 是相對顏色座標，不是固定紅藍綠黃。共用 frame 與各自隱藏獨立 frame 是不同接線規格：前者可強迫 x=y，後者可接受任何 x,y。

有限 grammar：`有序 induced C5 + 一個內部 K3 + 任意 boundary-to-K3 edges`。

| 項目 | 結果 |
| --- | ---: |
| 接線子集 | 32,768 |
| disk 必要邊數上界內 | 22,819 |
| disk 測試通過 | 7,194 |
| 不同 exact labeled Σ | 42 |
| 單一 component 的 exact T4 | 0 |
| unordered state pairs，含自配對 | 903 |
| intersection 恰為 T4 的 state pairs | 10 |

42 個 state 各保存一個最省邊實現，全部有 Lean exact-relation certificate。十個目標各有完整 graph certificate：五個 26 邊、五個 27 邊，全部 11 頂點、Σ=T4、planar 但 C5 不 cofacial。

最少 26 邊僅限此二元 grammar 的 target synthesis。**幾何測試只涵蓋選出的 state witnesses；未枚舉同 Σ 的全部實現。** 不可將只存最便宜 Σ witness 的優化，未經證明地套用到未來的 disk admissibility 搜尋。

最新決定性最小解的三色模式：

```text
L 接受：01021, 01201
R 接受：01012, 01202, 01212
兩者都接受全部五類四色模式。
```

五份排除證書解釋為「三個相鄰頂點只剩兩色」或「兩個相鄰頂點只剩同一色」。詳見 [gadgets.md](gadgets.md) 及 `artifacts/gadgets/explanation.json`。

`TriangleConstraints.compiled_meaning` 原本只以 `native_decide` 檢查 `leftLinks`／`rightLinks`；`ColorDFA.mem_sigma_triangle` 現在對所有 links 給出普通證明，前者保留為歷史檢查。

**不要混淆兩份 26 邊圖的編號**：`artifacts/construction/minimized.jsonl` 是較早構造；`artifacts/gadgets/bad_certificates.jsonl` 第一行是最新合成解。兩者 exact Σ 都是 T4，但邊集／兩側三色 reps 不同；下節路徑指的是後者。

## 6. 最新進展：非法接線的必要障礙（尚未 Lean 化）

這部分原本只有對話內 read-only 診斷，本交接首次集中落盤。2026-09-11 整理時重新執行確認。**本節的拒絕端證書沒有 Lean topology checker 或 JSON topology certificate。** 接受端（triangle grammar 內的 disk certificate）已於 §7.1 落地，兩者不可混淆。

### 6.1 交錯端點迫使兩塊分居兩側

最新第一張合成圖有兩條完全頂點不相交的路徑：

```text
P = 0–5–2
Q = 1–10–3
boundary order = 0,1,2,3,4
```

端點交錯，因此不能同時嵌入同一側 disk。這是 Jordan separation／cycle-bridge interlacement 障礙，不依賴四色定理。它提供非法的充分證書，也就是合法單側接線的必要排除條件；沒有證明沒有此障礙就一定合法。

十張 target 全有上述形式的證書。依 JSONL 行序 0..9：

| 行 | 0 到 2 的路徑 | 1 到 3 的路徑 |
| --- | --- | --- |
| 0 | 0–5–2 | 1–10–3 |
| 1 | 0–5–6–2 | 1–8–9–3 |
| 2 | 0–5–6–2 | 1–8–10–3 |
| 3 | 0–5–6–2 | 1–8–10–3 |
| 4 | 0–5–2 | 1–10–3 |
| 5 | 0–5–2 | 1–10–3 |
| 6 | 0–5–2 | 1–8–10–3 |
| 7 | 0–5–6–2 | 1–10–3 |
| 8 | 0–5–6–2 | 1–8–10–3 |
| 9 | 0–5–6–2 | 1–8–10–3 |

### 6.2 完整 Σ 也不能決定 disk 接線合法性

取同一個 ordered C5：

```text
P = C5
Q = C5 + {s0,s1,s2}
R = C5 + {t0,t1,t2}，s、t 是不同 interior vertices
```

P、Q、R 各自是 disk patches，Σ 全是 240 個 proper C5 assignments。因為每個 star center 只需避開三個鄰居的顏色，總能選到剩餘色。

但 P∪R 是 disk patch，Q∪R 不是；Q∪R 仍 planar、Σ 仍為全部 240 個。

拓撲原因：若 Q∪R 可以放在 disk 裡，就能在外側加 apex z 鄰接全部 boundary，產生 K3,3 子圖，兩側為 `{s,t,z}` 與 `{0,1,2}`。所以這兩塊不能同側。

這不是 color quotient 壓縮失誤：**即使沒有壓縮，Σ 也未包含此幾何觀察。** 該例可作下一階段 topology-aware congruence 的最小測試之一；尚未證其最小性。

### 6.3 Primitive 的 port 障礙

EQ 圖 K5−xy 自身 planar，但 x,y 不可能同面；若同面便能加 xy 得 K5。K4 frame 的四個 reference ports 也不能同面（加共同 apex 得 K5）。

這些是具體實現的限制，**沒有證明所有 EQ gadget 都不能有同面 ports**。

拓撲背景來源：[MIT：Some Graph Theory，§14.3](https://math.mit.edu/~djk/18.310/Lecture-Notes/some_graph_theory_2007.html)。該引用不是 Lean axiom，也不是搜尋剪枝中的四色定理。

## 7. 建議續作順序

### 7.1 已完成：geometry DFA 作為 topology-certificate 候選（2026-09-11）

在 triangle grammar 內，接受端 certificate 已落地：`GeometryDFA.rotationOf` 從 winding sequence 決定性產生 rotation system，`checkRotation` 驗證鄰居表、每個連通分量 `V − E + F = 2`、C5 為一個 face；`accepted_masks_have_rotation` 以 `native_decide` 對 32,768 個 mask 全部確認，`accept_certificate` 是其 `AnnulusAccept → ∃ run, checker = true` 形式。

* **forward soundness 可形式化**：上述已在 Lean 內。「球面 rotation system 且 C5 facial ⇒ disk embedding」是標準組合拓撲背景，未在 Lean 內證明，與 §6 的 Jordan 障礙同屬 topology 信任範圍。
* **completeness 尚未證明**：自動機拒絕 ⇒ 不存在 disk embedding，沒有證明。
* **`7194 = apex test` 僅為完整有限枚舉觀察**：`accepted_count = 7194`（Lean）與 `scripts/check_automata.py` 的 NetworkX apex-planarity 逐字一致，不因此提升為定理。

§6 的路徑交錯／K3,3 證書仍是 grammar 外的拒絕端證據，尚未 Lean 化。

### 7.2 未開始

1. 把第 6 節路徑／三共同 attachment 證書整理為 deterministic topology-certificate 資料，先讓 Lean 驗證有限組合事實：端點順序、真實邊、內部互不相交、K3,3 模型。
2. 明確定義 disk embedding 或組合 rotation-system 模型，再處理「證書 ⇒ 不能單側」的拓撲 soundness；不能用一個假定的 bridge-conflict 定理把缺口藏起來。
3. 形式化 P/Q/R 同 Σ、不同 context 幾何合法性的例子。染色證明很小，拓撲部分要另列信任範圍。
4. 候選 signature 為 `(Σ, attachments/循環順序, 側別約束或可行 embedding 集合)`；測試 composition congruence，先找反例，不先假設充分。
5. 有明確合法 transition grammar 之後，才研究 closure、有限 frontier 與 SCC。

可先對 bridges 配置 `side∈{inside,outside}`，以交錯／共同 attachment 證書加入 `side_i≠side_j`。這是必要條件方向，不能無條件當作完整判準。

純 intersection transition 已在 `State.lean` 證明單調縮小、互相可達的 exact states 必相同。它不能把 BAD 修成 GOOD（可能縮成 empty），也沒有自動證明哪些 singleton SCC 是 closed。

### 7.3 Z5 現象（觀察，不先當 theorem）

三色 canonical patterns 由唯一色頂點位置索引成 `Z5`（`01012↦4, 01021↦3, 01201↦2, 01202↦1, 01212↦0`）。在 triangle grammar 的 7,194 個 disk-accepted words 上：

* 32 種三色 acceptance subset 實現 21 種；empty 與 singleton 都沒有出現；
* size = 2 只有五個相鄰對 `{t_i, t_{i+1}}`，各 6 個 mask；size ≥ 3 全部實現；
* 十組 T4 target pairs 恰是兩個不相交的實現 profile（5 組相鄰對×相鄰對、5 組相鄰對×補集三元組）。

`GeometryDFA.z5_profiles_checked` 是此 grammar 內的 `native_decide` 檢查，不是 disk patch 的 lemma。

**里程碑「Colour semantics closed」已達成**（`Math/HallTriangle.lean`）：`k3_uncolorable_iff`（Mathlib Hall）→ `reject_iff_hall`：pattern 留有未用色 `d` 時，`¬ Accept (run w b) ↔ PairPinnedToFourth ∨ TripleRestrictedToTwo`，全是普通證明；`regression_guard` 與 `check_automata.py` 只是對 32,768 words 的 regression guard。染色側封口。（`winding ⇒ block` 已於下段證出。）**不要**以「boundary 鄰居是 C5 interval、兩兩交集 ≤ 1」為 geometry lemma 的 statement——這在 1,350 個 accepted words 上是假的（兩內部頂點可共享兩個 boundary 頂點，鄰居集可跳過未接線頂點）；要從 winding 給的「已接線頂點環序上的 block」出發。目標敘述：|R| ≤ 3，且 |R| = 3 只在 degree 型 (2,3,3)、R 為 cyclic 3-interval（目前為觀察；R 現在可寫成 `{u | GeoReject w u}`）。

**2026-09-11 續：`winding ⇒ block` 已證**（`Math/AttachmentBlock.lean`，普通證明，無 native_decide）。`runOK_iff_blocks`：`RunOK w ρ ↔` 弦的三角形位置沿 C5 環讀是某個旋轉下的 `replicate a 0 ++ replicate b 1 ++ replicate c 2`（完整刻畫）。`attachment_block`：`RunOK`、`k ∈ w i`、`k ∈ w j` 時，`i→j` 或 `j→i` 開弧上所有 `m` 都有 `w m ⊆ {k}`。工具是 `stepSum_le_of_sublist`（環和對 sublist 單調）。接著 `Math/GeometryWitness.lean` 把 Hall witness 去色：`GeoReject w u`（只用 `linksOf w k` 是否命中 `u`、`{u+1,u+3}`、`{u+2,u+4}`），`reject_iff_geometry : ¬ Accept (run w b) ↔ GeoReject w u`（任何三色形狀的 b），`threeProfile_eq_geo : threeProfile w = univ.filter (¬ GeoReject w ·)`。**下一步就是 bridge**：從 `RunOK w ρ`（用 `attachment_block`／`runOK_iff_blocks`）證 `#{u | GeoReject w u} ≤ 3` 與 3-interval，兩側都已是純幾何敘述；不要再回頭做 enumeration。

§7.3 的 bridge 最新進度（2026-09-11 續）：`runOK_large_rejection_cases` 已把未封口部分縮到上述四種 degree 型；低 degree 分支由 `runOK_rejection_le_two_of_low_degree` 完成。證明沿用 `stepSum_le_of_sublist`，三個共同鄰居會提供六弦、至少 winding 6 的局部障礙；fan excess 的步數預算給出總 attachment ≤ 8。沒有枚舉 words，沒有使用既有 `z5_profiles_checked` 證明新結論。不要重新做低 degree 分支；最新工作順序已改為先 normal form 幾何分型，再推四型的拒絕 corollary，見下段。完整 bridge 與 topology completeness 仍未證。

**2026-09-11 normal form 續作**：`annulusAccept_iff_normalForm` 與 nondegenerate 版本已證；singleton／shared-junction incidence 公式、pair 唯一性、min-degree ≥ 2 時共同鄰居 ≤ 1 已證。`geoReject_iff_pair_or_opposite` 是第一個以該幾何層為前提的拒絕 corollary。所有新主要定理無 native 依賴。具體參數、雙向證法、具名定理與未解邊界見 [attachment_normal_form.md](attachment_normal_form.md)。

**2026-09-12 bridge 封口**：上述 §7.3 的「下一步」與未封口敘述是歷史進度。現在 `GeoRejectBridge.lean` 已證完整 bound、等號 degree／cyclic interval 結構與 profile corollaries。證明只需 normal form 的 incidence corollaries，未逐型展開環序；一般 disk completeness 與 grammar 外 topology soundness 仍未證。

## 8. 檔案導航

| 檔案 | 接手時看什麼 |
| --- | --- |
| `Math/Boundary.lean`, `Enumeration.lean` | 基本語意、S4／D5、240→10→2 |
| `Math/State.lean` | exact 壓縮、intersection、SCC 限制 |
| `Math/Certificates.lean`, `GeneratedCertificates.lean` | 最早最小 BAD 與 250 份證書 |
| `Math/SplitCertificate.lean` | `edgeCheck_exact`, `splitSigma_exact`；GOOD／BAD／empty 的 exact-relation checker 與 BAD checker |
| `Math/Constructed*.lean` | 較早 11-vertex 構造及 exact T4 |
| `Math/GadgetRelations.lean`, `PrimitiveGadgets.lean` | relation algebra、frame 與 EQ/NEQ 規格 |
| `Math/TriangleConstraints.lean` | pigeonhole 證書、constraints-to-graph 的兩個具體 component 檢查 |
| `Math/GadgetLibrary.lean`, `GadgetTargets.lean`, `GadgetSynthesis.lean` | 42 library witnesses、10 target witnesses、`all_targets_exact` |
| `Math/ColorDFA.lean` | 染色自動機：state invariant、`mem_sigma_triangle`、`splitSigma_triangle`、`acceptedReps_exact`、mask 枚舉 |
| `Math/GeometryDFA.lean` | annulus 自動機、`rotationOf`、`checkRotation`、`accept_certificate`、`accepted_count`、`z5_profiles_checked` |
| `Math/HallTriangle.lean` | `k3_uncolorable_iff`、`reject_iff_hall`、`not_mem_sigma_iff_hall`、具名 witness、regression guard |
| `Math/AttachmentBlock.lean` | `stepSum_le_of_sublist`、`stepSum_mem_iff_blocks`、`runOK_iff_blocks`、`attachment_block`：winding ⇒ block 的普通證明 |
| `Math/GeometryWitness.lean` | `GeoReject`、`reject_iff_geometry`、`threeProfile_eq_geo`：Hall witness 去色，profile 變成 `linksOf` 敘述 |
| `Math/AttachmentBudget.lean` | fan excess ≤ winding、總 attachment ≤ 8、共同 boundary 鄰居 ≤ 2；無 native |
| `Math/GeometryProfile.lean` | 低 degree 時 `|R| ≤ 2`、profile ≥ 3，以及 `|R| ≥ 3` 的四種 degree 型 reduction；無 native |
| `Math/AttachmentNormalForm.lean` | cut-necklace normal form 雙向等價、packet alphabet／junction 唯一性、degree incidence、min-degree ≥ 2 的交集界 ≤ 1；不 import Hall |
| `Math/NormalFormHall.lean` | normal form ⇒ 排除兩個涉及 unique 位置的 triple Hall witnesses |
| `Math/GeoRejectBridge.lean` | 完整 `|R|≤3`、等號 `(2,3,3)` 與 cyclic 3-interval、profile ≥ 2 與等號相鄰對 |
| `Math/AttachmentEndpoints.lean` | 任意 Nodup endpoint packets 加三-block 環序 → normal form → AnnulusAccept；不含拓撲抽取證明 |
| `Math/AttachmentSignature.lean` | packet inventory、六種 incidence regimes、飽和時三 junction 加兩 singleton、兩種 degree 型 |
| `Math/AttachmentGaps.lean` | 三 junction 含空位的雙向 gap normal form；C5 gap 長度與 empty／singleton inventory |
| `Math/AttachmentSaturated.lean` | 三 junction 的 cyclic order、constant gaps、雙向 normal form，以及 C5 飽和時 x+y+z=2 |
| `Math/AttachmentOrder.lean` | 一／兩 junction 的 ordered gaps 雙向 list 定理；一 junction 的 C5 形式、兩 junction 的環序與 empty／singleton inventory |
| `Math/AutomataReplay.lean`, `AutomataAudit.lean` | 42 份 library 證書對自動機的 replay；`#print axioms` |
| `docs/phase1.md`, `construction.md`, `gadgets.md`, `automata.md` | 各階段詳細範圍與結果 |

一般 graph-wiring compiler 的 planar soundness **尚未建立**；不要把 relation 結合律當成 graph embedding 的接線定理。

## 9. 重現與工程注意事項

Lean／mathlib 鎖定 `v4.34.0-rc2`，使用既有 `lake-manifest.json`；不要為接手任務自動 `lake update`。Python 用 `uv run --with networkx==3.5`，不依賴系統 Python 已裝 NetworkX。

```bash
lake build
uv run --with networkx==3.5 python scripts/check_search.py
uv run --with networkx==3.5 python scripts/check_construction.py
uv run --with networkx==3.5 python scripts/check_gadgets.py
lake env lean Math/GadgetAudit.lean
uv run --with networkx==3.5 python scripts/triangle_automata.py
uv run --with networkx==3.5 python scripts/check_automata.py
lake env lean Math/AutomataAudit.lean
```

`triangle_automata.py` 會覆寫 `artifacts/automata/`（含 `nerode_*.json` 的 prefix→class mapping 與未最小化 product states）；兩次執行逐 byte 一致。`Math/GeometryDFA.lean` 的三個 `native_decide` 約需 3–4 分鐘，`HallTriangle.regression_guard` 約 2.5 分鐘。

重建最新合成資料（會覆寫其自己的 generated artifacts）：

```bash
uv run --with networkx==3.5 python scripts/synthesize_gadgets.py
python3 scripts/export_certificates.py --split --relation --namespace FiveBoundary.GadgetLibrary --input artifacts/gadgets/library.jsonl --output Math/GadgetLibrary.lean
python3 scripts/export_certificates.py --split --namespace FiveBoundary.GadgetTargets --input artifacts/gadgets/bad_certificates.jsonl --output Math/GadgetTargets.lean
```

需要只讀拓撲診斷時，可從 JSONL 建圖，分別在 induced subgraphs `{0,2,5,6,7}` 與 `{1,3,8,9,10}` 找 0→2、1→3 路徑，再驗證兩條路徑的 vertex sets 不相交。第 6 節逐行表就是重新執行所得。

性能注意：**不要讓 `native_decide` 枚舉 `Fin 5 → Finset (Fin 3)` 這類 Pi 型別的 `Finset.univ`**（32,768 個函數要數分鐘以上）；改用 `ColorDFA.wordOfMask : ℕ → Word` 對 `Fin 32768` 枚舉，`wordOfMask_surjective`／`wordOfMask_bijective` 已證，可把 mask 結論搬回 `∀ w`。同理 `Accept` 的 `Fin 3 → Color` 枚舉在熱迴圈中用 `acceptB`（`acceptB_iff`）。閉包內的 `let` 若依賴外層參數，會在每次呼叫重算——`rotationOf` 先物化 `rotationTable` 再回傳閉包。

避免直接建立 4^(5+k) 個完整 coloring 的大 Finset；使用已證等價的 split-interior checker。若在 `∀ b` 中重複計算同一 `splitSigma`，應先 `let actual := ...`。要檢查少數 Links 時用 `List.all`，不要透過 `∀ links ∈ list` 讓 native 決定程序枚舉整個 Links 型別。不要同時啟動會寫同一個 `.olean` 的多個 `lake build`。

## 歷史：較早的 C5 catalog 起始訊息（最新入口見文件頂端）

> 請先讀 `/home/ray/math/docs/HANDOFF.md` 最上方最新停止點、`docs/boundary_relations.md` 與 `docs/fan_pentagon.md`。目前已完成內部五邊形加 13、14 的完整搜尋：87 個 exact Σ（原 K3 是 42），以及 generic full boundary relation 和同一有序 C5 上的條件 pair forcing 庫。完整 relation 是唯一主狀態，先套用共同條件、再投影；不得反過來用 pair constraints 代表完整狀態。750 條條件規則、211,410 個 pair 查詢與 3,828 個 aligned meet 已獨立重驗；Lean 已證泛型法則及 pair projections 相同但 conditional forcing 不同的具體反例。普通證明、native finite checks、外部計算／幾何證據分開標示。入口是 `Math/BoundaryRelations.lean`、`Math/C5PairForcing.lean`、`scripts/boundary_relations.py` 和 `scripts/c5_relation_library.py`。使用者要求先暫停並 commit + push，沒有待完成驗證或背景程序。先使用既有 catalog，不自動重跑枚舉；下一個研究問題尚未指定，不自動開雙 C5 串接、一般 transducer、更多頂點搜尋或重啟歷史 topology completeness 工作。
