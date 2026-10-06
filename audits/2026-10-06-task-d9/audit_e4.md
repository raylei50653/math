# D₉：E4 非相鄰雙 roots 紙面引理與 NA54 獨立控制

2026-10-06。原文行號均指 `b2ca4520da50c9d2898ac6f8f966ac25df3f9609`
的 [E4 REPORT](../../artifacts/c5_excess_two_e4/REPORT.md)。本附件是獨立稽核；
不修改原報告、producer、歷史證書或原前提，不重開來源搜尋。

**Verdict：指定 E4 紙面引理均 holds。** 未找到新的數學缺口或反例。
原 E4 reductions checker 的兩次 byte-replay FAIL 另行照錄；其差異限於 E3
REPORT 的來源 bytes／SHA，不把 payload 相同寫成歷史 hash 通過。
NA54 只校準實際觸發的通用子步，不補足三列來源或 `(4,4)` core 的實現控制。

## 1. 完整前提、依賴使用與總表

E4:19–36 的來源是有限簡單圖、有序 induced C₅ 的 disk 外面、T4 全收、
每條非框邊對完整有序 Σ critical、ε=2、非相鄰的兩個 degree-5 roots，
其餘有效內點完整 degree 四。指定拒絕列是
`q₀=01212`、`q₁=01202`、`q₃=01021`，indices `(6,4,1)`；
`q₂=01201`、`q₄=01012` 不限定。從這三個拒絕取得有效 H 連通及全 B-touch。
每份 piece 始終是原 `H−{z,w}` 的整個連通分量，不是從 core 或路徑另造的 piece。

| 引理／結論 | 範圍 | verdict | 原文行號與主要理由 |
| --- | --- | --- | --- |
| N-empty-separating | 原 mixed 的 support 空，包含 sole separating mixed | holds | E4:56–72；有原外路時以實際 hubs 排除局部拒絕，沒有外路時無框 appendage 只在一個 root 接合，可由 T4 染色一次共同 S₄ 對齊。兩種情況均與接點邊 criticality 矛盾。 |
| N-theta | disk 中三份不同原 mixed | holds | E4:219–227；三條內部互斥 z–w 原路給 theta，整份第三 piece 被其他兩路的 Jordan cycle 與 B 隔開，故 actual support 空。 |
| N1-22-44 | sole mixed incidences22，指定三拒絕，某拒絕列有兩-root44 core | holds | E4:92–152；實際 core 飽和迫原四點 path／整側兩型；三列迫 terminal 真框邊；每個原整側盾弧至少三，互斥五邊預算矛盾。 |
| N-diagonal | 全 B-touch 的 one-sided degree4 mixed、actual support 含於一條真框邊 | holds | E4:166–185；局部 pin 同色只要求 hub 在 N(C) 交集見一色，輔助 hub 色保留原 lists，故完整 16-pin relation 的四條 diagonal fibres 均有 lift。 |
| N2-short-no-unary | 兩 mixed 皆短、無 unary、N-diagonal 完整前提 | holds | E4:189–192；任何三色 β 的未用色 D 避開所有 spokes，兩 roots 同取 D，兩份完整 piece lifts 可以同框拼回。 |
| N2 side-intersection／預算及殘留 | 兩原 mixed，完整 sides／relations／盾弧 | holds | E4:194–215；全部 mixed 短時拒絕 β 的兩側 domains 互斥；long 與 unary 各收至少二邊，得 ℓ+u≤2；保留完整 off-diagonal joint 及省略身份。 |
| 非相鄰 m≤2 | 原來源全部 mixed，任意 core 型 | holds | E4:219–232；theta 空支援和 N-empty 給來源級矛盾，不需要各列自己的 core。 |
| N3 全排 | m≥3，包含45、54、原55 | holds | E4:229–232、272；刪任一 mixed 仍由另一原 mixed 連 roots，全部 one-sided；原 theta 空支援和 E3 N-empty 排除原 G 本身，故覆蓋全部 core 型。 |
| 原 H 不能 tree（附帶稽核） | ε2、非相鄰雙5、其餘4，H connected | holds | E4:77–84；`s=2k+4`、`E=3k+8` 超過五邊外面 disk 的 `3k+7`，沒有把 core tree 當原 H。 |

只核對外部 prerequisite 的使用：E3 nonadjacent notes:121–163 提供原 degree4
piece 飽和及實際44分類；其中「無 tails／直接 bridge」正是 N1 所需的強前提，
不是從一般 minor 推回的關係不變性。E3 REPORT:96–110 提供 triple-critical；
E4 只取其「刪邊新收三列之一」，沒有把原 G 當每列的 minimal core。
E3 nonadjacent notes:69–89 的盾弧移植明列 H 連通、全 B-touch、degree4 與
原 critical 見證，因而不需要完整 mask 恰為933或941。
E3 nonadjacent notes:165–170 的 ε1／ε0 跨列拒絕限制只用在剩餘 core 身份。

D₈ 的 DG6-1 補表關閉唯一 degree6，並不進入本附件已明定「兩 degree5」
的各引理證明。原 A／B 必要身份表也沒有被當成 E4 的來源窮盡前提。
這次沒有重證上述外部分類，也沒有把它們算作獨立 Python 結果。

## 2. N-empty-separating 逐步

| 步驟 | 原文行號 | 稽核理由 |
| --- | --- | --- |
| 空支援混合 piece 的全部外鄰只有 z、w | 56–60 | piece 是完整 `H−{z,w}` 分量，沒有框附件；不存在第三個有效內部外鄰。 |
| `G−C` connected 時存在原 z–w 路 | 59 | 可經 B，與 sole C 在 H 中 separating 相容；未虛構避開 C 的內部路。 |
| 相同／不同 pins 的原 hub bags | 61–62 | 同色用整條原路；異色沿一條原邊切成兩袋，各連通、互斥、相鄰。只在袋與 N(C) 的交集要求 pin 常色，路內點不需同色。 |
| tightness、minor 與局部接回 | 63 | 拒絕 lists 下每個 C 點在一袋至多有一個外鄰，收縮沒有掉 degree／lists；hub 原則給原 planar 圖的 K₅ 矛盾。只用 minor 排除平面性。 |
| 接點邊不可能 critical | 64 | `G−e` 的新增整圖 coloring 限制到 `G−C`，再接回完整 C，會讓原 G 接受同一列。 |
| `G−C` disconnected 的完整分拆 | 66–67 | 原 H connected，`H−C` 每個分量含 z 或 w，因此至多兩個 root 側；B connected 且 C 無框邊，至少一個 root 側 A 完全不碰 B。 |
| 無框 appendage 的指定 root 配色 | 67–69 | `A∪C` 與外部只在另一 root r 相交。T4 至少給一份原 G coloring，限制到 appendage 後用一次整體 S₄ 把 r 色對齊外部任意 pin。 |
| appendage 非框邊不 critical | 70 | 任一刪邊的新外部 coloring 都能接回完整 appendage；其中確有原接點邊，故不是空的 criticality 反證。 |

這個論證不讀指定三列的字面位置；T4 在分離情況只供一份原 G coloring。
也不對 separating C 使用 one-sided 盾弧。

## 3. N1-22-44 逐步

| 步驟 | 原文行號 | 稽核理由 |
| --- | --- | --- |
| sole mixed 必保留 | 88–90、97–99 | minimal q-core 的有效 H 自己 connected，且保留兩 roots；沒有原 zw，省掉唯一原 mixed 會斷開 roots。 |
| 原 four-point path／附件數 | 97–104 | E3 實際44分類給兩個頂點互斥 root triangles、原直接 bridge、無 tails；degree4 飽和使整個原 C 原樣保留。terminal 各完整兩框附件，中間各一個。 |
| 每側兩種 capacity3 原型 | 106–109 | 44core 每 root 留兩 spokes，原 root5 只差一個 unit。原型只可能原三spokes，或兩spokes加一整份 capacity-one unary；不能把 capacity3 本身當這個分類。 |
| 每 β 原 side 至少有一份 coloring | 111–112 | side 中 root degree3 使 root list 有 strict slack，其他 retained unary 點保持 degree4，connected list-slack 貪婪接回。這是存在某 root 色，不宣稱每個預釘 root 色都可行。 |
| terminal 重色就接回 C | 116–118 | terminal 的兩個不同 actual 框鄰點在 β 同色會合併禁色，產生 strict slack。C connected，所以任意合法 root pins 都可填 C，拼上兩原 side coloring 即原 G 接受。 |
| 三列 cover 全部非相鄰 pair | 120–128 | 02／14 在01021重色，03在01202重色，13／24在01212重色。只需這些指定拒絕，沒有查01201／01012的接受性。 |
| 原 bridge 分兩整側 | 133–138 | `{z,a,b}` 加所有原 z-unary 與對稱 w-side connected、互斥並 cover H；各自 complement connected。盾弧拓撲只需這些條件，故可以向整側收費；沒有向 sole C 收費。 |
| support≥3、若盾長≤2則三個連續點 | 140 | 三spokes側直接≥3，另一型有 unary 的≥3實際支援；全 B-touch 及支援區間使低盾長只能是三點二邊。 |
| unary 型低盾長矛盾 | 142–144 | unary actual support≥3且包含於整側三點，所以正好同一弧；terminal 不在 unary 裡，不能碰其盾弧內點，只能碰兩個非相鄰外端點，違反真框邊。 |
| 三spokes型低盾長矛盾 | 145–149 | 原 root 三spoke star 的三個 disk faces 中，一條 terminal 真框邊只鄰接唯一小三角面。`H−root` connected、避開 B 和star，整塊被困在該面；其所有 B 附件只碰該真框邊兩端。加回 star 全圖至多碰三框點，違反全 B-touch。 |
| 共同五邊矛盾 | 151–152 | 兩個同源、互斥、connected 整側都需≥3盾邊，而實際盾弧邊互斥，得到6≤5矛盾。 |

結論只排除「原 incidences22 且有44core」整型。E4:156–160 保留沒有44core
的22來源以及11／12／21、45／54／原55；稽核未把它擴成 N1 全排。

## 4. N-diagonal 與 N2 逐步

| 步驟 | 原文行號 | 稽核理由 |
| --- | --- | --- |
| 局部 lists 不需外部染色可延拓 | 169–176 | 定理 B 的 list／hub 反證只讀 N(C) 上 pins；收縮後用相異的輔助 hub 色。原外部路上未接 C 的其他顏色不進 lists，故沒有補造 outside coloring。 |
| 三hub／兩hub 的原連通性 | 178–181 | `K=H−C` connected，且全 B-touch 使每個 `B−{h,k}` 點有 K 附件。三點補弧與 K connected，兩種 bags 均互斥、pairwise adjacent，由原框邊及原附件給 adjacency。 |
| bags 中只見指定不同色 | 179–181 | 三hub case 的根色 a 不等於β(h),β(k)；两hub case 合併與根色相同的框端點。所有 N(C) 的外鄰均被覆盖，完整 degree4 的 tightness 可用。 |
| diagonal 是完整共同避色查詢 | 183–185 | 結論是每個 a 的整份 contact tuple 存在一次共同 coloring，包含 shared contact 的單一坐標，不是獨立 contact marginals。 |
| short／no-unary 共同接回 | 189–192 | 三色 β 的唯一未用色 D 避全部 root spokes；沒有 zw，兩 roots 同色合法。兩 mixed 互為不同原分量且沒有其他跨分量邊，故整份 lifts 可同 β／D 拼回。 |
| rejected β 的側交集 | 194–195 | 若 a 同時在 E_z、E_w，所有 unary 因子和 spokes 可避 a，再由每個 short mixed 的 diagonal lift 接回，矛盾。只給必要條件，未推定 off-diagonal 充分性。 |
| long／unary budget | 199–211 | m2時所有原 pieces one-sided；long support 的純盾弧下界二，unary 的 critical 見證及全 B-touch 給二。盾弧互斥，得 ℓ+u≤2；short pair收恰一，singleton收零，並保留實際盾長總和。 |
| 殘留接口與跨列 core 身份 | 212–215、240–261 | 原44省一11mixed；45／54省原單側unit；55就是原 G。ε1或ε0的列限制套同一原省略圖本身，沒有舊「省略必Ω」filter；整 tuple、ordered contacts、全部 fibres及lifts持續保留。 |

短支援 diagonal 的 full-B-touch 是必要環境前提。NA54 中24圖只碰四框點，
不把這些圖對該引理的缺失前提算成反例或成功觸發。

## 5. N-theta、m≤2 與 N3 逐步

| 步驟 | 原文行號 | 稽核理由 |
| --- | --- | --- |
| 原三路及 theta | 221 | 各 mixed connected 且觸兩 roots，所以有內部在該整份 piece 的simple z–w路。三份原 pieces互斥，路径內部互斥且避 B。 |
| 含整段 B 的互補區 | 222–223 | disk 外面 B 與 theta不交且connected，全部落在同一 theta互補區；其邊界是两路形成的Jordan cycle。第三路內點在远離 B 的有界側。 |
| 整份第三 piece 被隔離 | 225–227 | roots不在 piece，另兩路位於不同原 pieces；第三原 piece connected且不碰Jordan cycle，所以不是只把所選路當piece，其全部頂點都在同一有界側。 |
| actual 框附件不可能 | 226–227 | 任何第三 piece 到 B 的原附件邊都需穿越cycle，與原 disk embedding 矛盾。 |
| 來源級排除全部 cores | 229–232 | m≥3時每份 piece刪掉後仍有另一原mixed連roots，N-empty 的原外路版本適用。空支援piece的contact不critical，已矛盾原 G，無需另分45／54／55。 |

這裡只使用指定 C₅ 為 disk 外面的平面嵌入。Minor僅作不平面反證；沒有宣稱
boundary pattern、T4、完整 Σ、R_C 或 fibres 在minor下保持。

## 6. NA54 獨立 checker 與 trigger 統計

[audit_e4_controls.py](audit_e4_controls.py) 僅讀 E4C 54個具名代表的
`id, vertices, edges, rotation`。沒有import原 E4／E4C／ES checker的decision
logic，也不讀來源的lemma判定、Σ、degree、piece、support、colouring或core輸出。
所有來源bytes SHA另記入[e4_controls.json](e4_controls.json)。

獨立重算simple／induced-frame、degree、H／piece連通性、原rotation dart faces、
Euler=2及C₅外面，MRV四色DFS算同一字面色框的完整local lifts、contact tuples、
每列16有序pin fibres；再用獨立整圖DFS逐個pin核對完整join。
逐非框刪邊的新列附整圖witness。每個實際拒絕列的全部 inclusion-minimal qcores
由全刪邊遞迴加degree<4剝離重算，每份保留邊附qcritical witness；剝離有四種色
可貪婪接回，且不會剝掉任何degree≥4的minimal拒絕core。
從recorded rotation限制到同一實際子圖，重新抽盾弧，沒有另挑canonical embedding。

| 基礎獨立重算 | 實際數量 |
| --- | ---: |
| k6／k7／k8／k9代表 | 3／2／22／27 |
| `(m,u)` | `(1,0):1`、`(1,1):4`、`(1,2):30`、`(2,1):19` |
| full-B-touch／四框touch | 30／24 |
| 原 pieces／one-sided pieces | 156／121 |
| 完整contact tuples | 7373 |
| 原非框刪邊／新增列witness | 1289／1385 |
| 完整joint與整圖DFS的pin查詢 | 54×10×16＝8640 |
| 全部實際拒絕列／全部minimal qcores | 60／60，每列唯一 |
| qcore型 | 55:48、45:10、54:2、44:0、root省略:0 |

下表圖數的三種狀態與JSON完全一致；多piece／多pin不充當多張控制。

| 判定 | triggered and holds | not triggered | counterexample | 實際限制 |
| --- | ---: | ---: | ---: | --- |
| N-empty-separating | 0 | 54 | 0 | 無空actual support的mixed。 |
| N-empty外路hub | 0 | 54 | 0 | 無空支援加原外路的實例。 |
| N-empty appendage | 0 | 54 | 0 | 無空支援分離appendage。 |
| N-theta | 0 | 54 | 0 | 全部m1或m2，沒有三branch antecedent。 |
| N1-22-44原path步驟 | 0 | 54 | 0 | 沒有兩root44 minimal qcore。 |
| N1-22-44三列排除 | 0 | 54 | 0 | 沒有44core，也沒有三列同拒。 |
| N1-44 retained-mixed／triangle身份 | 0 | 54 | 0 | 沒有兩root44 core。 |
| N-diagonal | 11 | 43 | 0 | 22份原mixed、10列×4 diagonal pins，共880個nonempty完整fibres。 |
| N2-short-no-unary | 0 | 54 | 0 | 全部m2圖都有一份unary。 |
| N2拒絕列側交集 | 11 | 43 | 0 | 全部short且full-B-touch的11圖；每個實際拒絕β側domains互斥。 |
| N2共同盾弧budget | 11 | 43 | 0 | full-B-touch的m2實例才套unary下界。 |
| 非相鄰m≤2必要條件 | 54 | 0 | 0 | 全部圖直接數得m≤2；不是N-theta反證前提的校準。 |
| N3來源排除前提 | 0 | 54 | 0 | m≥3沒有實例。 |
| 完整contact join | 54 | 0 | 0 | 每個β／pin的join與獨立整圖DFS相等，保留全部fibres。 |
| 原degree4 piece飽和 | 54 | 0 | 0 | 全部minimal qcores原piece全取或全不取，原incident edges不變。 |
| 指定三列同拒前提 | 0 | 54 | 0 | 沒有一圖同拒indices `(6,4,1)`。 |

所有列counterexample明確為零。禁型前提零觸發是控制覆蓋限制，不是成功實驗，
更不證任意大小來源不存在。NA54的原Σ、Q與source原位一起保留；沒有獨立D₅
或S₄正規化不同分量，也沒有拿AD圖頂替非相鄰前提。

## 7. 重播、historical FAIL 與停止点

獨立checker只需stdlib；正式稽核目錄的重播是：

```bash
python3 audits/2026-10-06-task-d9/audit_e4_controls.py --check
PYTHONHASHSEED=17 python3 audits/2026-10-06-task-d9/audit_e4_controls.py --check
```

若在稽核目錄外執行相同copy，可明示 `--root REPO --output /path/e4_controls.json`
再加 `--check`；新建output用exclusive-create，`--check`只讀逐byte核對。
實際命令／exit／stdout與stderrSHA見validation；不把未執行項寫成通過。

| 原 E4 checker | default exit | seed17 exit | stdout byte相同 | 說明 |
| --- | ---: | ---: | --- | --- |
| `python3 scripts/c5_excess_two_e4_reductions.py --check` | 1 | 1 | 是，兩者空stdout | `Exact E4 artifact replay failed.`，保留原歷史FAIL。 |
| `uv run --with networkx==3.5 python scripts/c5_excess_two_e4_control.py --check` | 0 | 0 | 是 | 原202stored representatives及19attempts仍未找到當時要求的NA控制。 |

原reductions artifact SHA為
`5b9d97d2a19d36776cd0617531023756889813bc44c108ec67bf6dca1ec1fb40`；
用當前原producer重算SHA為
`3a78b89f29b8fc37ea8fff477ceb0e8956a2d25977b3f75f529fe5aadc525425`。
差異只有 `/sources/artifacts/c5_excess_two_e3/REPORT.md/bytes` 的
30573→32469，以及該來源SHA
`6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659`→
`73ed652a55b159a44eb6da4608f11537efc0d43603128094101ef044a96b2cd3`。
去來源provenance後完整semantic payload相同；這個診斷重用原build，與本附件的
独立lemma checker不同。原artifact與原歷史bytes未改寫。

本附件沒有新gap reproduction，因為沒有發現E4指定紙面引理的缺口。
停止於逐步paper verdict及NA54固定控制；N1／N2剩餘、ε≥3、無界來源realizability、
一般出口與K∞=K≤5仍未證。外部Gallai／degree-list及Jordan證明、固定Python
證據、disk拓撲／來源實現、Lean層分開；沒有四色定理oracle，也沒有Lean build。
