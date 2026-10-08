# E3：唯一 degree-6 分支的三列移植與補洞

本頁是任務 E3 的研究附件；主報告由整合者負責。只新增檔案，不修改歷史工具、共用文件或原 artifacts，不 commit／push。

**結論：分支 (i) 完成。** 只使用指定 ordered induced-C5 disk、T4 全收、自身 Sigma-critical、有效 degree 約定、epsilon=2，以及 singleton 位置 0、1、3 三列拒絕。沒有假定 Q 恰為三點，也沒有假定其餘三色列接受。Checker 的所有必要域只 filter row indices 1、4、6 為拒絕，2、5、7、8、9 為接受；0、3 不受限。

## 1. 前提、一般介面與控制

十列的順序直接由所有 proper literal C5 rows 作共同 S4 正規化重算：q0=01212 是 index6，q1=01202 是 index4，q3=01021 是 index1。未指定的 q4=01012、q2=01201 是 indices0、3。

E2 §2 從本題來源推出有效 degree>=4、H 非空連通、拒絕兩列時碰齊 B；故唯一 degree6 root r 以外都 degree4。每份 H-r 原分量有非空原有序 contact relation（contact slack 逆序貪婪），令 F 為完整 tuples 的顏色集合之交。精確 root projection 是 U 減去原 spoke 顏色和各原 F 的聯集；它只描述這個同 root 避色查詢，沒有拆掉原 relations。

Sigma-critical 原 contact 邊的刪邊完整染色給该原分量的 private forbidden-color witness。沿同一圖取避開該分量的 r-to-B 原路徑，短支援 hub 論證使每份原分量的盾弧至少二邊；共同原盾弧邊互斥，故分量至多兩份。T4 使每個內點原 spokes 至多三。這些工具不需要三列假設本身，只需已有兩拒絕列的 full-B touch 或對應的明列外路徑。

[新 checker](../../scripts/c5_excess_two_e3_degree6.py)讀取同任務的[exact E1 controls](positive_control_inputs.json)，從原邊枚舉完整 literal colorings，重算 Sigma=951、935。951 的 r=5、spokes=34、兩個原 binary 是 C69 與 C78；兩份完整十列 ordered relations、tuples 的原 full-color witnesses、原附件及精確 root joint 都保存於 [degree6.json](degree6.json)。兩份 binary 都適用 §4 的 single-edge D carrier 引理，並實際通過全部五個 singleton rows 的檢查。935 有兩個 degree5 roots，故 unique-root 介面前提不適用；共同 degree、H 連通、full-B touch、spokes<=3 均通過。兩張控制都不滿足指定三列拒絕。

原來源不能無條件套「省略任一 binary 後全收」：951 的 C69、C78 原省略圖分別有 Sigma=959、1015（由整合者的 control checker 實際驗證）。新 checker 完全刪除了歷史 t2 binary producer 的這個 screen。

## 2. 原工具的移植性

下表的精確列是 canonical 941 frame；原 D5 搬運必同時搬原列、contacts、attachments、component ownership，不能固定 mask 再只搬局部 incidence。

| 原工具／原身份 | 紙面局部內容 | 原末端證書的形狀依賴 | E3 實際使用 |
| --- | --- | --- | --- |
| t0 (6)，單份 C、六原 contacts、兩 K4 的原 bridge | 四個 root pins 對同一拒絕列、共同 tau、六葉飽和給原 K5 | 只需任一拒絕列 | 直接移植；可選 q0 index6 |
| t0 (5,1)、(3,3)，每份具名原因子 | 另一原分量給外部 hub；F5<=2、F3<=1；不能覆蓋四 root 色 | 只需任一拒絕列 | 直接移植；可選 q0 index6 |
| t0 (4,2)，C4 與 V2 的原 ownership、同一 binary 原 path bags | 同框 envelope profiles、同一 pair path、共同 actual-support family 與兩框弧原 K5 | 舊 200 queries 對完整十列精確 mask；941 額外接受 indices0、3，933 額外接受 index0 | 新 20 份三列必要查询全排，54 DFS nodes；不用舊精確 mask 或 omitted-full 限制 |
| t1 (5)，唯一 spoke rb_s、C 的五原 contacts | rb_s criticality witness 迫同一 C 的三禁色；五葉 active tree／原 tethers K5 | 私有色見證可在任何原拒絕列；不需其它三色列接受 | 直接移植；不把見證列固定為某個額外接受／拒絕身份 |
| t1 (4,1)，C4、W1 與原 spoke 切口，兩原末端袋各一 contact | 容量 2+1、unary D role、共同-D active forest、兩固定末端袋不得並排 | 舊 216 profiles 是精確十列結果；各拒絕 C4 pair 含 D 是輸出，不能提前假設 | 新 10 份三列查询全排，32 nodes；D guard 顯式保留；只有 indices1、4、6 用於共同-D 末端袋 |
| t1 (3,2)，A2、C3 與原 binary bridge path | ternary 容量一及 D role；binary 同一原 path support family／兩框弧 K5 | 舊 100 queries filter 完整 mask | 新 10 份三列查询全排，18 nodes；指定三列均保留同一原 factor 身份 |
| t2 (4)，同一 C4、兩原 spokes、原扇區及固定末端袋 | 任一指定拒絕列 spoke 同色就需三禁色；否則三列都迫 C4 pair 包含 D，末端袋次序矛盾 | 舊 200 exact-mask queries 的局部證明實際只用拒絕列 | 新 20 原 spoke-sector 配置，40 nodes，全排；所有拒絕比較都是 indices1、4、6 |
| t2 (3,1)，C3、U1 同扇區支援／ownership | 兩容量各一及同原局部 equality-class profile | 舊 107296 十列 profiles final only compare exact masks | 新 40 具名幾何必要域、44 nodes 全排；沒有使用精確 accepted extras |
| t2 (2,2)，A2、C2 兩原接點對、兩原 spokes | pair path；singleton 首橋兩端共用 beta，跨列 beta 各自獨立 | 舊 script solve 的三份「all omissions accept every row」screens，及 full-mask 比較，都不可直接套 | 新 screen 全部移除；三列域先剩兩份 abstract controls，§4 single-edge carrier 補洞，40 geometries、198 nodes 全排 |
| t3 (2,1)，C2、U1、三原 spokes | 每份 span>=2，扇區 1/2/2、兩原局部 profile | 舊 T4 survivors 已至多缺一列，強於 exact-mask 排除 | 直接移植概念；新 10 幾何、539 nodes 三列必要域獨立重算為零 |
| t3 (3)，C3、三原 spoke positions S | 每列 F3<=1；拒絕 singleton-j 迫 spokes rainbow、j in S | 941 三位置 0/1/3 迫 S=Q，而 q0 在 S 重色；933 舊寫法用四列但此處不需第四列 | 三列足夠；新十 S 各保存一份 indices1/4/6 的原拒絕 row 容量反證 |
| 所有 >=3 原分量的分拆 | 每份 fixed original shield length>=2，共同互斥 | 僅以來源 full-B touch／private witness 使用舊 933/941 前提 | 直接 2+2+2>5，毋須 profiles／省略 core 表 |
| 原 double-spoke 省略 rb_s,rb_t；spoke+unary 省略 rb_s,V；binary 省略 C2；two-unary 省略 U,V | 全 degree4 飽和、原 q-core、接點保持 transfer 是一般局部工具 | 原最終「省略後全收」是完整 source target 的十列必要比較；canonical 941 包含 indices0、3 的額外接受身份，933 包含 index0；原 q4-aligned first/second core 保留 original base/root IDs 才能接合 | E3 不引用這些全收結論；保留它們為精確 mask 工具，原 rb_s/rb_t/V/C2/U identities 不冒充本輪一般省略身份 |

歷史省略工具詳細入口：[double-spoke](../../docs/c5_excess_two_double_spoke.md)、[spoke+unary](../../docs/c5_excess_two_spoke_unary.md)、[t3 binary](../../docs/c5_excess_two_binary_omission.md)、[t2 binary](../../docs/c5_excess_two_two_binary.md)、[two-unary](../../docs/c5_excess_two_two_unary.md)、[t1 binary](../../docs/c5_excess_two_single_spoke_binary.md)、[t1 two-unary](../../docs/c5_excess_two_single_spoke_two_unary.md)。本輪沒有讀舊「0 target hits」當一般來源排除，也沒有重新跑其 398 原 root positions 或 3497 open keys。

## 3. 全部分拆表

| t | 原接點分拆 | 三列前提下的排除 |
| --- | --- | --- |
| 0 | (6) | 飽和兩原 K4、原 bridge、六 contacts 的 K5；只需 q0 拒絕 |
| 0 | (5,1) | 任一拒絕列的 forbidden capacity<=2+1<4 |
| 0 | (4,2) | 新三列同源 palette/path support 域為空 |
| 0 | (3,3) | 任一拒絕列的 forbidden capacity<=1+1<4 |
| 0 | (4,1,1),(3,2,1),(3,1,1,1),(2,2,2),(2,2,1,1),(2,1,1,1,1),(1,1,1,1,1,1) | >=3 原盾弧，至少六框邊 |
| 1 | (5) | 原 spoke 私有色 witness 的五葉 active-tree 原 K5 |
| 1 | (4,1),(3,2) | 新三列同源有限必要域為空；四接點不當成 binary |
| 1 | (3,1,1),(2,2,1),(2,1,1,1),(1,1,1,1,1) | >=3 原盾弧 |
| 2 | (4),(3,1) | 新三列同源原 sector/profile／末端袋域為空 |
| 2 | (2,2) | 原 pair path／first-bridge screens 加 §4 carrier 論證 |
| 2 | (2,1,1),(1,1,1,1) | >=3 原盾弧 |
| 3 | (3) | 三列 spokes rainbow 位置容量矛盾 |
| 3 | (2,1) | 新三列同源原 sector/profile 域為空 |
| 3 | (1,1,1) | >=3 原盾弧 |

合計 t0 的11份、t1 的7份、t2 的5份、t3 的3份＝26種整數分拆。t>=4 與 T4 全收矛盾。本表是紙面任意大小化約與有限必要末端的合成，不是任意大小圖搜尋。

## 4. t2 (2,2) 的新 common carrier 補洞

只保留三列＋T4、同一原 binary pair path／first-bridge 及 full relation 的同框 equivariance，不套任何「省略全收」，較弱必要域剩兩份，只差原 A、C ownership。共同座標為 spokes02，短 A envelope012、長 C envelope2340；原 tuple／支持位置都一起搬運。兩份 abstract necessary controls 保存完整八列 forbidden profiles，未指定 indices0、3，不聲稱 disk source 可實現。

在 q1=01202(index4) 有 F_A={D}、F_C={1,D}。原 K=G-A 是連通 all-degree4 圖，繼承 T4 和 disk，拒絕 q1。任取 minimal q1-core，在 K 的 degree4 飽和沿 H_K 傳播，得到整張 K，所以 K 自身 q1-critical。K 的 r 有兩原 contacts x,y、兩 spokes02，C 連通使 r 位於 cycle。K 不碰 singleton b1（C actual support 包含於2340、r spokes02）。[Unattached-singleton cyclic lemma](../../docs/c5_two_spoke_split_support.md#2-a-useful-consequence-of-the-existing-degree-four-classification) 因而使原 H_K 恰為 triangle 或兩 disjoint triangles 加直接 bridge。兩型都令 C 的原 contacts x,y 相鄰。q1 pair 原-path 定理進一步確定 xy 是 C 的一條原 bridge，接點間原 path 長度恰一。

切 xy 得兩份固定原 bags W_x、W_y；每袋只含自己那個原 root contact，其餘私有點不接 r。E_x(q)、E_y(q) 是在該原 bag 內、尚未扣原 root 色的 **exact attainable contact-color query**，而不是一個 palette 上界或 endpoint marginal。原 q1 pair lemma 給 E_x(q1)=E_y(q1)={1,D}。

較弱域另在 q0=01212(index6) 迫 F_C(q0)={1}。固定兩列共同 root pin 1，兩份 C-degree assignments 都不可著色而 tight，Gallai block palettes 存在。在每個 off-path private point，兩列的 boundary 都不使用 D、又沒有 r attachment，所以兩列的 list-D membership 均為1。沿同一原 rooted block tree，從 leaf 向 contact 剝 terminal blocks：在 private vertex 由 list-D bit 定 block-D bit，在 cutpoint 先扣孩子 blocks 的 D bits 再定 parent bit；逐步唯一。兩列的全部 off-path palette-D bits 相同；direct boundary attachments 也不用 D。因此 D 仍在 exact E_x(q0)、E_y(q0) 中。

對單條原 bridge xy，拒絕 root=1 意味 E_x(q0)減去{1}與E_y(q0)減去{1} 都是 singleton {D}：任一集合若還有另一色，與另一邊 D 配成異色就能完整延拓。**不能由此說兩份 E 都等於 {1,D}**，它們也可能是 {D}。但扣 root=D 後，各份 exact query 只剩空或 {1}，因此 xy 仍不可染，原 C 也禁 D。與 F_C(q0)={1} 矛盾。

此 carrier 原理不依賴 epsilon 或三列本身：任何一條原 contact-path edge、兩份可重用 exact rooted bags、共同未用色 D、pair witness 與一個 non-D singleton witness 都不相容。新 checker 對所有包含 D 的非空 E_x,E_y 及三個 non-D root pins 作192份精確 edge queries，特別保存 E={D} 的控制；951 的兩份原 binary 在實际十列完整 relations 中也都通過這條引理。935 不具該 unary-binary 原接點前提，明列為不適用。

## 5. 新有限證書與執行

新必要域全部是由先行紙面 root／shield／Gallai／actual-core 引理導出的至多20／40個原扇區或弧配置，以及 palette/color-permutation 類；不是來源圖或既有逐 key 葉。共同框色固定，所有 support-family 都直接核對全部24置換。其他 accepted singleton rows從未加入 Boolean constraints；full-mask equality 從未使用。

實際成功命令與 exit code：

```text
python3 scripts/c5_excess_two_e3_degree6.py                 exit 0
python3 scripts/c5_excess_two_e3_degree6.py --check         exit 0
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_e3_degree6.py --check  exit 0
```

三輪摘要完全相同；生成的 degree6.json 是2,027,696 bytes。第一次生成嘗試 exit1，原因是讀新的 controls input 時把欄位 sigma_mask 寫成 sigma；沒有產物寫入。一次跨檔案系統 rename 修正嘗試亦 exit1（EXDEV），原 failed source 保留 `/tmp/e3_degree6_failed_attempt_20261004.py`，之後以 exclusive-create 在空缺的 canonical path 新建修正版，沒有覆寫原資料。上述最終三輪均成功。全域 check_docs、docgraph、diff checks 由 E3 整合者執行列入主報告。

外部 degree-list／Gallai 來源是 Dvorak 的 [List coloring and Gallai trees, Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，沿用 E2 所讀版本；本 checker 不是外部定理的 formal proof。沒有新 Lean theorem／lake build，沒有 4CT oracle、planarity oracle 或大枚舉。本頁完成 (i)，雙 degree5 roots 的 (ii) 由另外兩份工作負責；不宣稱整個 E3 已完成。
