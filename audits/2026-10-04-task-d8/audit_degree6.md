# D₈ 子稽核：E3 §4 唯一 degree-6 的 26 分拆與單橋 carrier

基準 `2ac279b`；獨立 worktree `/home/ray/developer/ai/math-task-d8`。
本子稽核只新增本目錄的檔案；未修改既有 checker、REPORT、notes 或 artifact。
以下行號均指本基準 tracked 檔案；JSON 用欄位路徑定位。

**總 verdict：有缺口但可補。** 26 分拆中，24 格確認成立；
`t=1,(4,1)` 與 `t=1,(3,2)` 的原新證書只覆盖 spoke=b₀，未覆蓋固定
三列座標下另外兩個相對 spoke 軌道。這是原有限域覆蓋缺口 DG6-1，
不是找到可實現反例；本稽核補算全部五個 spoke 的同一必要域均空，
已給出具體補證資料。E3 §4.1 的單橋 carrier 各步確認成立，
沒有發現需要 q₂／q₄ 接受性或「省略必 Ω」的偷換。

本判定沿用既有 paper 的 degree-list 與實際全 degree-4 分類，
沒有重新證明其全部歷史內容；Python 有限重算不代替任意大小／disk 論證。

## 1. 共用前提與列身份

| 核對 | verdict | 具體理由／位置 |
| --- | --- | --- |
| 固定三拒絕列、T4、另兩 singleton 自由 | 成立 | `scripts/c5_excess_two_e3_degree6.py:32–39` 重算十列；ACCEPT={2,5,7,8,9} 恰 T4，REJECT={1,4,6} 恰 q₃,q₁,q₀。SELECT 不含0、3。`solve:213–230` 只在 SELECT 上建立變數与 coverage；没有 full-mask equality。 |
| 無舊三份省略全收 screen | 成立 | `solve:209–304` 沒有測 spoke∪F_A、spoke∪F_C、F_A∪F_C 各自不得覆蓋 U；artifact 明列 `original_omission_full_acceptance_screen=false`。`degree6_notes.md:17,33,37` 正確保留 951 原 binary omissions 非 Ω 的界線。 |
| 完整 R_C 的 root 避色投影 | 成立 | E3 REPORT:177–182；對非空 R_C，a 可避開整份原 contacts，恰 a∉∩_tuple set(tuple)。同一 root pin 下每份分量各取完整 tuple 再接回。沒有對一般 binary relation 取 endpoint marginals。 |
| 原 criticality 私有見證／至少二邊盾弧 | 成立 | E3 REPORT:172–175；`degree6_notes.md:11–13`；`c5_excess_two_no_spoke_complete.md:65–101`，`c5_short_support_singleton.md:27–62,64–150`。刪原 contact 邊的新完整染色使 root 色在這份 C 被禁而其他因子放行；E3 triple-critical 可把見證選在三列之一。full-B touch 給同一圖、避開 C 的外路徑；短支援 hub 反證使 fixed support span≥2。共同 annulus/slit lifts 开框邊段互斥，故 ≥3 份 C 需要6>5。 |
| t≥4 排除 | 成立 | 四個不同原 boundary 鄰點可在一份 T4 中看齊四色，直接阻斷 r；没有 singleton 角色需求。参照 `c5_excess_one_subcovers.md:177–178`，E3 REPORT:191。 |
| 由空有限必要域到來源排除 | 有缺口但可補 | 局部 envelope profiles、support-family 全24置換與原 path/pendant-bag 引理均是來源必要条件；但 t1 建域遗漏相对 spoke 位置，见 §4 DG6-1。其餘有限幾何域覆盖见各格。 |

## 2. 全 26 分拆逐格 verdict

E3 主表为 REPORT:184–195；逐工具表为 `degree6_notes.md:23–37`，逐分拆表为:43–60。
下表只列原三列加 T4 所需的最后出口，没有移植旧 exact-mask 零解结论。

| t | 原接點分拆 | verdict | 具体理由／引用 |
| ---: | --- | --- | --- |
| 0 | (6) | 成立 | 任取 q₀，F_C=U。四 root pins 的 tight palettes 共用 τ，六 contacts 飽和为兩原 K₄ 加直接 bridge；原五 branch sets 給 K₅。`c5_excess_two_no_spoke_complete.md:104–141` 明確只需一拒絕列，不用 C 外部 spoke 或 exact Σ。 |
| 0 | (5,1) | 成立 | 另一原因子提供 root-to-B hub；五接點任選三禁色的 active-tree/tether K₅ 使容量≤2，unary≤1，q₀ 的四色覆盖不可能。`c5_excess_two_no_spoke_complete.md:156–168`。 |
| 0 | (4,2) | 成立 | 同一原 binary pair path 及 actual support family／兩框弧 K₅；四接點只用容量2而没有冒充 binary。`finite_interfaces:328–333` 包含固定 Q 坐標下20份旋轉/ownership幾何，artifact `summary/t0_(4,2)`=20几何、54 nodes、0余项。 |
| 0 | (3,3) | 成立 | 两份 ternary 各容量≤1，任取 q₀ 的四 root 色不能全覆盖。`c5_excess_two_no_spoke_complete.md:156–170`。 |
| 0 | (4,1,1) | 成立 | 三份固定原盾弧各≥2，6>5；不使用额外列身份或 profiles。E3 REPORT:172–175；本页 §1。 |
| 0 | (3,2,1) | 成立 | 同上三原盾弧预算。 |
| 0 | (3,1,1,1) | 成立 | 四原盾弧预算至少8>5。 |
| 0 | (2,2,2) | 成立 | 三原盾弧预算。 |
| 0 | (2,2,1,1) | 成立 | 四原盾弧预算。 |
| 0 | (2,1,1,1,1) | 成立 | 五原盾弧预算至少10>5。 |
| 0 | (1,1,1,1,1,1) | 成立 | 六原盾弧预算至少12>5。 |
| 1 | (5) | 成立 | 原 spoke 的 selected criticality 完整见证迫同一 F_C=U−{spoke色}；三拒絕 palettes 的五葉 active tree 只能正 C₅ 或三 triangles。原 spoke、实际 tethers 给 K₅。`c5_excess_two_five_contact.md:24–54,58–102,104–156`，对任意原 spoke 位置成立。 |
| 1 | (4,1) | 有缺口但可補 | 四接點容量2、unary D守恒与共同-D fixed pendant bags 的局部论证成立；原有限表只算 spoke0（DG6-1）。正式 artifact 10几何、32 nodes；本稽核全5 spoke共50几何、157 nodes均空。`checker:326–327,334`；本页 §4。 |
| 1 | (3,2) | 有缺口但可補 | ternary容量1/D守恒、binary原pair path/首桥/actual-support K₅成立；原有限表同样只算 spoke0（DG6-1）。正式 artifact 10几何、18 nodes；本稽核全5 spoke共50几何、92 nodes均空。`checker:326–327,335`；本页 §4。 |
| 1 | (3,1,1) | 成立 | 三原盾弧预算。 |
| 1 | (2,2,1) | 成立 | 三原盾弧预算。 |
| 1 | (2,1,1,1) | 成立 | 四原盾弧预算。 |
| 1 | (1,1,1,1,1) | 成立 | 五原盾弧预算。 |
| 2 | (4) | 成立 | 同色spokes拒絕列需三禁色，四接點K₅矛盾；异色时每个指定拒絕pair含D，原共同active forest给两fixed末端袋，actual support family不能在同一sector并排。`c5_excess_two_two_spoke_four.md:48–101,137–160`；`finite_interfaces:336–337`覆盖全部10 spoke pairs×2sector=20几何，40 nodes，空。 |
| 2 | (3,1) | 成立 | ternary/unary各容量1，加同一原envelope相等型及完整root覆盖。`finite_interfaces:338–339`全部10 spoke pairs的40原ownership几何，44 nodes，空。不施 Drole、不施省略全收。 |
| 2 | (2,2) | 成立 | 全部40具名几何；原pair path/first-bridge必要条件留下两ownership互换弱控制，然后 §3 carrier排除。`checker:340–348`，artifact198 nodes，2弱控制，最终0；没有旧三个Ω screens。 |
| 2 | (2,1,1) | 成立 | 三原盾弧预算。 |
| 2 | (1,1,1,1) | 成立 | 四原盾弧预算。 |
| 3 | (3) | 成立 | ternary容量1；三拒絕singleton位置0、1、3使S={0,1,3}才可能全部虹彩，但q₀在S上为011，需至少两禁色。`finite_interfaces:350–357`全部10 spoke sets保存一指定拒絕列容量反证。 |
| 3 | (2,1) | 成立 | 扇区(1,1,3)放不下兩份span≥2；(1,2,2)各长区一份，共10具名ownership几何。T4已把全部同源profile压到至多一个拒絕，故三指定拒絕不可能。`c5_excess_two_three_spoke_complete.md:77–120`；本checker:342–343重新三列域539 nodes空。 |
| 3 | (1,1,1) | 成立 | 三原盾弧预算。 |

只需 E3 前提的沿用局部引理包括：四接點三禁色K₅、ternary容量1、
unary/ternary非空禁色的D身份守恒、binary pair的同一原奇数bridge path、
首桥same-row共用β、兩框弧K₅和兩fixed pendant bags。
它们的使用均不要求 q₂／q₄ 接受；但凡完整十列歷史producer的目标比较、
旧省略Ω结论或另外两个 singleton 的接受位，均没有纳入此次新 solve。

## 3. §4.1 單橋 carrier 逐行／逐步核對

| 原文步驟 | verdict | 核對與理由 |
| --- | --- | --- |
| REPORT:199–210 的两弱控制和同框F表 | 成立 | artifact `pre_carrier_weaker_abstract_controls[0/1]`确是spokes02、短envelope012、长2340，只交换两个原ownership；八列完整F profiles中的指定三列逐值等于REPORT表。0、3仍未加入。 |
| :212 K的complete degree／连通 | 成立 | 删除短原C_s只减少r的两原contact边，deg_K(r)=4；其他保留內点只在长C_l或r，C_s与其无边，仍degree4。H_K={r}∪C_l连通。B原induced C₅和disk嵌入保持；T4是删子图的单调继承。 |
| :213 K拒q₁ | 成立 | spokes在q₁禁{0,2}，原长factorF_l(q₁)={1,D}，同框root投影为空。无需对另外两列作假设。 |
| :214 K自身q₁-core | 成立 | 取包含B的minimal q₁ obstruction M⊆K。任一内点deg_M≥4，否则删该点的q₁着色可贪婪补回。K每个保留内点degree4，所以M出现的任一内点保留其全部原incident边、原邻点；沿连通H_K传播得到M=K。故K的每条非框边都q₁-critical。所谓“完整Σ只缺q₁”是T4+all-degree4分类/E2 ε=0的推论，不是偷偷假设q₂/q₄接受；此句在后续只需minimal-q₁并未额外使用exactΣ。 |
| :215 singleton unattached、cycle | 成立 | q₁的singleton是b₁，long actual attachments⊆2340且r spokes02，所以K无内点接b₁。长C_l的两不同原contacts x,y和其内部原simple path，加rx,ry，形成K中原cycle；r内部degree2。 |
| :216–218 cyclic lemma适用与原xy | 成立 | `c5_two_spoke_split_support.md:69–98`要求minimal singleton obstruction、allcomplete degree4、connected interior、cycle、unattached singleton，以上逐项满足；不需T4。实际H_K只能triangle，或两不交triangles加direct bridge，无tails。r内部degree2且在cycle，故处于triangle而不能是bridge endpoint；其两个原contacts就是该triangle另外两点，确有原xy。原q₁ pair path lemma（`c5_single_spoke_two_two.md:127–140`）使xy为C_l中的原bridge，所以切xy后分成两实际bags，非relation-preserving minor。 |
| :220–224 exact E及q₁ pair | 成立 | 删除原bridge xy后bags不交，各只有一个原r-contact。整C_l的原relation恰由两bag完整染色、接回xy异色构成；对固定r=a，原bag contact色正好E_x−{a}、E_y−{a}。F={1,D}对应拒1和拒D；两边各有接点slack而非空，于是拒1迫两剩余域都是{D}，拒D迫都是{1}，故E_x=E_y={1,D}。这是single bridge exact join，不是任意binary的marginals乘积。 |
| :226–228 两tight assignments | 成立 | q₁和q₀都禁root1，所以对同一完整C_l可选两份不可染degree assignments，两者tight且有Gallai palettes。每个off-path noncontact point无r边；两个框列都未使用D，故D均在其原list里。即便boundary其他色改变，也不改变这个D位元。 |
| :229–232 rooted剥叶唯一D bits | 成立 | 将每bag block tree以原contact为根。对非根v写Σ_{K∋v}d_K=1_[D∈L(v)]，同点palette互斥。最深block取parent以外原点v，先从v方程扣已解children的D bits，即唯一解该parent block的d_K。每一步所用v都不是原r-contact；因此两列同右端、同children，解出完全相同off-path D bits。接点direct boundary也无D，所以原exact E的D位元相同；q₁的E含D便得q₀的E也含D。袋若只是contact singleton，没有off-path block，D直接留在E，亦覆盖。 |
| :234–238 最后D∈F_l(q₀) | 成立 | q₀拒root1，D在两E中；若E_x−{1}有d≠D，便与y色D异色，完整bag着色可接回；反之同理。因此两个remaining sets均为{D}，E_x,E_y各仅可能{D}或{1,D}。扣rootD后各为空或{1}，原xy仍不可染，故D∈F_l(q₀)，矛盾于F_l(q₀)={1}。没有声称两份E都必须是pair。 |
| :240–242 任意大小与有限表界线 | 成立（单桥子型） | 一般大小来自cited actual-degree4分类和rooted palette归纳；192个set queries只确认最后exact单桥代数。不能把该192表当作topology或palette存在性证明。原(i)总体完成仍应附DG6-1覆盖限定。 |

Gallai使用的外部前提另在本次打开[Dvořák原讲义](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
确认：Lemma7需connected degree assignment并拒絕，推出tight；Theorem10同条件
给Gallai及blockwise-uniform palettes。没有额外exactΣ或逐列minimal条件。

**独立固定原结构控制。** `degree6_fixed_shapes.py`不import任何repo checker。
它在cyclic lemma给出的triangle及两triangles/direct bridge上保留r=5、
contacts(6,7)、spokes02，枚举long envelope2340内全部complete-degree4
boundary附件：36+3456+3456=6948份（两种具名bridge endpoint都算）。
没有施disk或T4筛选，所以是覆盖真实控制的放宽域。
1040份有exact F_l(q₁)={1,D}；其中100份在q₀还拒root1，
全部同时禁D，exact q₀ singleton{1}从未出现。
每种形状保留一份原图、actual attachments、两列完整ordered relations和exact bag E。
普通／seed17 `--check`均exit0。该有限probe辅助核对carrier，未取代paper cyclic lemma。

## 4. DG6-1：t=1 固定spoke与固定Q不能同时任意正規化

**最小复现。** 查看新checker的`finite_interfaces:326–327,334–335`：

```python
one_spoke = ... # slit coordinates 0,...,5, where 0 and 5 both mean original b0
solve((0,), s, (2,1), fourbags=0, Drole=1, ...)
solve((0,), s, (2,1), paths=(0,), Drole=1, ...)
```

全文件同时固定REJECT={1,4,6} (`checker:34–39`)，即原Q={0,1,3}；
artifact两组的全部`original_spokes`也都是[0]。
`degree6_notes.md:21`虽正确要求D₅同时搬原列／spokes／attachments／ownership，
但此两个新必要域只搬了几何切口，没有枚举相应拒絕列轨道。
固定Q={0,1,3}的D₅ stabilizer仅identity和i↦1−i(mod5)，
spoke位置軌道为{0,1}、{2,4}、{3}。因此原spoke=b₂或b₃没有
保持同一三列的变换可送到b₀；两格的新10查询不能宣称覆盖所有来源。

**影响。** `degree6_notes.md:29–30,51`和E3 REPORT:187,240的
“t1两表全排／(i)完成”缺这两轨道的正式有限证书。
这不影响任意原spoke的(5) active-tree排除、>=3因子盾弧预算、
t=0/2/3各格或§4.1 carrier；也不证明degree6反例存在。
在原交付证书层，(i)完成需要附这个缺口限定；不能继续写成原checker
已独立覆盖全部26格而无补充。数学结论不需因为carrier推翻而撤回：
下述audit补表已经支持直接修补。

**具体补证方向／附加重算。** 保持REJECT字面三列不动，对每s=0,...,4
把同一10份slit geometries的全部原envelope位置一起加s(mod5)，
把原spoke改为(s,)，仍保留factor ownership，再运行完全相同solve；
或者保留spoke0并同时枚举三列的D₅像。无需q₂／q₄精确角色，
无需新增來源枚举或省略Ω filter。
本子稽核在独立脚本`degree6_t1_spoke_coverage.py`做第一种补算：

| 原spoke | (4,1) 几何／nodes／remaining | (3,2) 几何／nodes／remaining |
| ---: | --- | --- |
| 0 | 10 / 32 / 0 | 10 / 18 / 0 |
| 1 | 10 / 31 / 0 | 10 / 19 / 0 |
| 2 | 10 / 30 / 0 | 10 / 18 / 0 |
| 3 | 10 / 34 / 0 | 10 / 19 / 0 |
| 4 | 10 / 30 / 0 | 10 / 18 / 0 |

总100份同框查询、249 nodes、0 remaining；其中80份是原artifact缺少的
spoke≠0查询。普通／seed17 `--check`均exit0，结果完整保存于
`degree6_t1_spoke_coverage.json`。脚本import unchanged checker的finite helper，
与完全独立的carrier fixed-shape probe证据层不同，明列此依赖。

## 5. artifact对照与重播导航

| artifact路径 | 本次对照 |
| --- | --- |
| `required_accepted_row_indices` / `required_rejected_row_indices` / `unspecified_three_color_row_indices` | [2,5,7,8,9] / [1,4,6] / [0,3]，无额外接受位。 |
| `summary` | t0(4,2):20/54；t1(4,1):10/32；t1(3,2):10/18；t2(4):20/40；t2(3,1):40/44；t2(2,2):40/198；t3(2,1):10/539；t3(3):10spoke sets。全部剩余0，t2弱控制2；t1 coverage缺口另列DG6-1。 |
| `pre_carrier_weaker_abstract_controls` | 两份原ownership互换，q₃/q₁/q₀ F表逐值吻合REPORT:203–207。 |
| `carrier_edge_controls` | 192份完整exact parent query，包含E={D}控制，没有错误强迫E都等于pair。 |
| `positive_controls.records[0]` | 951原r=5，两binary contacts(6,9)、(7,8)都为原singleedge；pair-D reference rows分别[1,3]、[0,6]，全部5个singleton的carrier检查通过。此处控制读全部十列，包括q₂/q₄，属观察而非排除前提。 |
| `positive_controls.records[1]` | 935是两degree5 roots，unique-degree6介面不适用；共同degree／H连通／full-B／spokes≤3通过，没有被排除。 |

四个E3/K′普通和seed17的整体十命令重播由总稽核者运行，
本子稽核不重复把它们算成自己的独立检查。
新增两脚本的生成／`--check`／seed17实测exit与输出在
[degree6_validation.json](degree6_validation.json)。

```text
/home/ray/developer/ai/math/.venv/bin/python audits/2026-10-04-task-d8/degree6_fixed_shapes.py --check
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python audits/2026-10-04-task-d8/degree6_fixed_shapes.py --check
/home/ray/developer/ai/math/.venv/bin/python audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.py --check
PYTHONHASHSEED=17 /home/ray/developer/ai/math/.venv/bin/python audits/2026-10-04-task-d8/degree6_t1_spoke_coverage.py --check
```
