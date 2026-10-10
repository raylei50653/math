# N45-J：χ=0 兩 mixed 的完整 joint 與逐欄容量校準

任務狀態：**執行者完成，待監督端交叉驗收**。交付的是獨立工具與固定控制校準；
没有新增 N2 來源排除，也尚未驗收 N45-S／N45-U 的新命題。

BASE／實際輸入 HEAD 均為 `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
獨立 detached worktree：`/tmp/math-n45-j-dc8e9aa7`，建立後及驗證完成時均無工作樹修改。
輸出只在 `/home/ray/developer/ai/math/audits/2026-10-09-n45-j/`。
未 commit、push、開 PR、發外部訊息或再委派。

## 1. 交付、輸入與獨立性

- [checker.py](checker.py)：標準庫獨立 checker，從原邊重建完整 pieces／contacts／relations。
- [inputs.json](inputs.json)：BASE、HEAD、66 個實讀檔案的原路徑、凍結路徑及 SHA256。
- [checks.json](checks.json)：命令、exit、seed、logs、未跑項及零漂移核對。
- [inventory.json](results/inventory.json)：54 圖原邊重建的 metadata、19 圖 N2 固定清單及 N1 校準清單。
- [certificate.json](results/certificate.json)：完整 local tuples／全部 piece lifts／16 fibres、原圖及 derivative 的逐 pair 整圖 lifts、容量、原刪邊與 root-deletion 見證。
- [coverage.json](results/coverage.json)：分域計數、12 個 N1 45／54 occurrences 的 β-minimality witnesses。
- [具名原圖介面範例](source_examples/NA7-0002-named-root-swap.json)及[介面證書](source-example-results/certificate.json)：原 NA7-0002 只重新命名頂點並交換有序 roots，沒有搜尋新圖。
- [verify.py](verify.py)：重播、只讀與拒絕覆寫核對；[TASK.md](TASK.md)保存未提交的派工指令。
- [MANIFEST.sha256](MANIFEST.sha256)：交付檔案 hash；不是交付 commit SHA。

來源依賴讀 BASE 版本：[E4 §6](frozen/artifacts/c5_excess_two_e4/REPORT.md#6-完整原-relation-的參數化交付與-core-身份)、
[E4C §1–2](frozen/artifacts/c5_excess_two_e4c/REPORT.md#1-來源精確前提與證據層)、
[Phase B §3.2](frozen/docs/c5_phase_b_common_lemmas.md#32-b-c2任意两自由roots的條件逐欄容量定理)
及[原 capacity checker](frozen/scripts/c5_phase_b_controls.py)。
HANDOFF、STATUS、DOCUMENTATION 及任務共用來源也全部保留 BASE bytes。
原工作樹 STATUS／guide 已有派工修改，未混進凍結研究輸入。

沒有 import 或執行原 checker 的決策邏輯。原 JSON 的邊、頂點與 rotation 是輸入；
預存 pieces、tuples、fibres、joins、derivatives 與結論在重建完成後才作比較。
54 圖只做原邊／拓撲 inventory；完整染色校準限下列 19 個 N2 圖及另外 6 個 N1 圖。
12 個 45／54 occurrences 是既存 core 的選取，不是重開 minimal-core 枚舉。

## 2. 有限量詞、方法與結果

共同有限域 `D₂` 是 inventory 的 19 個 `N2_selected` 原圖。
每圖根序為 `(5,6)`、框序為 `(0,1,2,3,4)`，χ=0，兩 roots 完整 degree5，
其餘有效內點完整 degree4；`H−{5,6}` 恰兩 mixed，另有一 unary。
框列 `C` 是 cells indices 0–9 的十個 canonical proper rows，依序為
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
所有主張均固定同一原圖、字面框列及原 contacts；沒有獨立搬運 pieces。

### N45-J-C01：完整原 relation 與整圖 oracle 相等

**量詞／結論：** 對每個 `G∈D₂`、`β∈C`、有序 `(a,b)∈{0,1,2,3}²`，
從原完整 tuples 得到的
`J_G=(E_z×E_w)∩A_P∩A_Q` 接受該 pair，當且僅當直接原邊回溯可染整圖。
每個非空 pair 保存 tuple-join 與 direct oracle 各一份 full graph lift；空 fibre 明存 `null`。
每個 `R_P(β)` 保存全部 contact tuples 及每 tuple 的全部原 P lifts。
每份原 mixed 的 16 個 fibres 包含全部 diagonal；沒有刪同色 pins。

**依賴／前提：** 原有限邊集、同一框色、互斥完整分量、ordered distinct contacts；
shared contact 只佔一個座標。全圖 oracle 只讀原邊和 pins，不讀 local relation。
E4 §6 是介面語義依賴；保存結果不用作計算決策。

| N2 原圖項目 | 核對結果 |
| --- | ---: |
| 原圖／框列／root-pair queries | 19／190／3040 |
| 非空／空整圖 fibres | 882／2158 |
| local contact tuples／全部 piece lifts | 2362／2534 |
| 所有 pieces 的 local pin fibres／空 local fibres | 9120／1066 |
| 原 mixed／有 shared contacts 的原 mixed | 38／38 |
| 預存完整 tuples、全部 lifts、16 fibres、join 及 E 比較 | 全相等 |

原支援、實際框附件、ownership、contacts、原內邊與 bridges 從邊重建。
原 rotation 保存，獨立 face walk 驗 sphere Euler 與唯一 C5 外面；one-sided 與
原 shield edges 也從原圖 rotation 重建並與保存資料比較。shield 不参与染色替換。

**證據層／未涵蓋：** 有限 Python；不是任意大小完備性、來源實現或 Lean theorem。
普通及 seed17 重播結果為 **triggered and holds**，counterexample 0。

### N45-J-C02：原單位省略查詢精確且 mixed relation 不變

**量詞／结論：** 對 `G∈D₂` 的每條原 spoke 及每份原 root incidence=1 unary U，
對全部 `β∈C` 和全部 16 pairs，精確重建 `X=G−e` 或 `X=G−V(U)`，
原兩 mixed 的完整 `R_P,R_Q` 直接沿用，join 與 X 的獨立原邊回溯逐 pair 相等。
spoke 只移除該原不等式；unary 是整份原分量省略，未改成新頂點或 singleton 禁色。
被省略 unary 的完整原 relation、所有原 lifts、attachments 與 support 仍在原圖證書內。
每列 `F_U` 由完整 relation 計算，容許空；capacity-one 不預設 `|F_U|=1`。

| N2 derivative 項目 | 結果 |
| --- | ---: |
| 原 spoke／整份單接點 unary 省略 | 47／7 |
| derivatives／框列／root-pair queries | 54／540／8640 |
| degree-(4,5)／(5,4) | 29／25 |
| 非空／空整圖 fibres | 3440／5200 |
| 完整 Σ=1023／拒絕列 | 54／0 |

**全部前提／依賴：** C01 的同圖完整 relation；省略 incidence 恰一且 retained nonroots
完整 degree4。程式逐 derivative 重算 degrees、ε及刪除邊集，ε全為1。
未預填 X 的 Σ-critical；也沒有在此對 X 作同 Σ minimalization 或引用 E2 排除。

**證據層／未涵蓋：** 有限 Python，triggered and holds；不是 N2 45／54 minimal-core
來源控制，因為本域 derivative 全收。保存的 19 個原拒絕列 core degree payload
全為55，僅重算其邊給出的 degree，未重新宣稱已枚舉所有 minimal cores。

### N45-J-C03：χ=0 的 B-C2 逐欄容量

**量詞：** 對上述每份原圖／derivative、每個 β、两个 root 方向 `(r,s)`，
僅在完整 join 拒絕且 `E_s≠∅` 時，對每個 `b∈E_s` 核

`D^u+O^u+δ+o+λ=deg_X(r)−4`，χ=0，`A=E_r`。

**全部前提／依賴：** 原完整 nonroot degree4、同一 β 的完整 fibres、原 incidence 計數，
每份 unary 局部 relation 非空；沒有其他自由 roots 或未填的外部限制。
`G_C(b)` 是由完整 fibre 的空性得到的原 mixed 禁色欄；逐 C 核
`|G_C(b)|≤k_C^r`，並核 `A⊆⋃G_C(b)`、全部五項非負及等式。
spokes 每條分開計 singleton 因子，重色不能先去重 incidence。
依賴 Phase B §3.2 紙面語義；Python 是固定實例核對，未證新任意大小命題。

| 域 | triggered and holds：逐欄 | not triggered：方向 | 右值 |
| --- | ---: | ---: | --- |
| N2 原 G | 74 | 342 | 74 次均為1 |
| N2 unit derivatives | 0 | 1080 | 全接受，0／1 等式前提未觸發 |
| 另列 N1 原 G | 24 | 96 | 24 次均為1 |
| 另列 N1 unit derivatives | 36 | 456 | 降度側0：12次；另一側1：24次 |

**計數單位：** triggered 計每個 b 的 column；not triggered 計每個 `(β,r,s)` 方向，
兩者不能當成同一分母。缺失前提逐項記在證書；接受列記 `complete join rejects beta` 缺失，
若 E_s 空也另記。這批没有以空 E_s 補充任何容量觸發。

N1 校準只使用既存 12 個 45／54 core occurrences：6 份原圖、8 次 spoke 與4次整 unary
省略，10份45、2份54。它們各自恰等於一個原 unit derivative；全部 β-minimality
由每條保留非框邊刪除的 full lift 獨立核實。另重算這6圖的所有原 units，共24份
derivatives／240列／3840 pair queries；N1 原圖另計60列／960queries。
**這些統計始終標 N1；不補充 N2 45／54 的來源 coverage。**

**證據層／未涵蓋：** 有限 Python，counterexample 0；任意大小等式論證仍由 Phase B
原紙面承擔。沒有混合不同 β 的容量，也不相加跨列見證。

### N45-J-C04：完整 tuples 與 shared identity 的實際碰撞控制

**量詞／結論：** 僅對 D₂ 原資料逐 piece-row／pair 作診斷，沒有改 relation：
480 個 piece-row 的座標 marginals 乘積包含原 R_P 沒有的 tuple；602 個 mixed
piece-row-pair 允許兩側各自選一個 tuple，卻沒有單一完整 tuple 同時滿足兩側。
全部602個保存了同一原 shared contact 及兩個互不相容 tuple indices。

具名控制 `NA7-0002 / β=01012 / P0={7,9} / pins=(1,2)`：

- 原 contacts：z 接9，w接7及9，shared contact9只一座標；原 bridge=79，附件07、09、17。
- contact order `(7,9)`；完整 R 為 `{(2,1),(2,3),(3,1),(3,2)}`，每 tuple 的全 P lift 即該 tuple。
- z單獨可選 `(2,3)`，w單獨可選 `(3,1)`；兩者在原頂點9的顏色不同，不能拼接。
- 完整 `(1,2)` fibre 空，整圖 direct oracle 同樣空；當列 `E_z={1,2}`、`E_w={0,2,3}`，
  所以此 pair 亦實際通過原 side 限制。

**依賴／證據層：** C01 保存的實際原 relation／full lifts；有限 Python。
這是投影替換的 **counterexample control**，並非 B-C2 反例、目標來源反例或新 disk 構造。
原圖 Σ959，完整933／941與指定三列前提均未觸發。沒有以人工 relation 偽造 disk 反例。

## 3. 精確來源 coverage 與 OPEN 邊界

19 個原圖都實際滿足：有限簡單 induced-C5 disk、T4全收、每條非框邊 Σ-critical、ε2、
非相鄰完整 degree5 roots、其餘有效內點degree4、m=2，且兩份原 root-deletion 全收。
Σ-critical 用全部原非框刪邊的新列及 full witnesses 核對；root-deletion 另重算。

原完整 masks 為 `959×3,1021×4,1015×4,1007×2,1022×6`。
每圖另核整框的10個 D5 搬運，**没有一份完整 mask 是933／941或其整圖像**。
指定三列 q0(index6)、q1(index4)、q3(index1)全拒絕的前提也都未觸發。
每圖完整 source coverage 因此均為 **not triggered**，具名缺失字段為
`complete_933_941_or_whole_D5_image` 及 `specified_triple_rejected`。

N2 的45／54 source/minimal-core occurrence：**0；缺控制**。
tooling 的有限核對不推出一般 N2 来源不存在，不建立任意大小枚舉完備性，
不重開 U1–U4、原55排除或猜想E；S／U新命題保持未驗。

下一個最小義務：S／U若返回具名原圖及完整原邊／ordered frame／roots／原 rotation，
使用 §4 介面凍結該輸入，增量重算 joint、原 units、完整 source 前提與容量。
若仍没有目標 N2 45／54控制，降度側右值0的 N2 實例 coverage保持缺控制；
不能借 N1 的12次正校準關閉該義務。

## 4. 重播與具名原圖增量介面

從 canonical research root 執行，兩次固定重播只讀：

```sh
python3 -B audits/2026-10-09-n45-j/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-j/checker.py --check
```

可追加 `--live-base /tmp/math-n45-j-dc8e9aa7` 核獨立 BASE 原檔案 bytes；實跑的兩次固定
重播均帶此選項。凍結快照足以獨立重播，無須保留 /tmp worktree。
`--check` 逐 byte 比較完整證書並核輸入 SHA256；不覆寫舊 JSON。
生成先 exclusive-create 新輸出目錄；目錄存在立即 exit1，沒有先算再覆寫。

具名輸入 JSON 只需 `id, vertices, edges, frame, roots`；frame與roots均有序，
頂點可為整數或字串。原圖必須χ=0、兩degree5 roots，其餘有效內點degree4；
孤立內點需在介面外明確忽略。附原 `rotation` 才能核 disk；未附則 disk 標not triggered。
不需要任何預算、tuples、join、minimal-core等預存決策字段。

```sh
python3 -B audits/2026-10-09-n45-j/checker.py --source /path/to/named-original-graph.json --out audits/2026-10-09-n45-j/new-source-output
python3 -B audits/2026-10-09-n45-j/checker.py --check --source /path/to/named-original-graph.json --out audits/2026-10-09-n45-j/new-source-output
```

路徑是供接手者替換的參數，非已存在或已核的 S／U 控制。
生成保存原輸入 payload／hash、完整relations及所有units；任意大小可能昂貴，但不搜尋新圖族。
輸出可辨新增輸入的完整來源前提是否觸發，**不宣稱枚舉每列全部 minimal cores**；
如 S／U需驗特定新 core，仍須另附原 core 邊集與 β-minimality 證書。

## 5. 驗證、findings 與修改邊界

| 實跑 | exit／結果 |
| --- | --- |
| 獨立 checker 固定生成 | 0；exclusive-create |
| 固定普通／PYTHONHASHSEED=17重播 | 0／0；[普通log](logs/fixed-normal.log)、[seed17 log](logs/fixed-seed17.log) |
| 具名root交換範例生成、普通／seed17重播 | 0、0／0；[普通log](logs/source-normal.log)、[seed17 log](logs/source-seed17.log) |
| 具名root交換的完整relation轉置 | 160個原圖pairs相等；同原圖derivative另核640queries |
| 已存在輸出目錄再生成 | 預期exit1；[拒絕覆寫log](logs/exclusive-create-refusal.log) |
| 故意改壞新比較副本的coverage數字 | 預期exit1，`certificate byte/payload drift: coverage.json`；[log](logs/corrupted-certificate-refusal.log) |
| ordinary／seed17／負控制前後 bytes與mtime | 75個輸入／證據檔案全部相同 |
| 獨立 BASE 原輸入 | 66個實讀檔案零byte漂移；worktree仍乾淨 |

`negative-replay/` 是明確標記的拒絕校準副本；coverage只有一個查詢數字被故意加1。
它引用原證書只讀，沒有改壞或覆寫任何 frozen input／results。

**N45-J-F01（介面使用限制，已保存重現）：** §2 C04 的共享頂點碰撞迫整 tuple 同時存在；
若下游用兩側 marginals／兩個不同 lifts拼接，會在 NA7-0002 的具名pair得到假接受。
影響是省略查詢與來源延拓的正確性；所需做法是保原 shared coordinate、同一完整tuple及full lift。
此 finding 不指控原 checker，原保存joint在此次比較全部相等。

未跑 Lean／lake build／axioms audit（無新Lean）、E3／E4／E4C／ES／ER／U1–U4大枚舉、
S／U新命題核對及全repo文件檢查，理由在checks.json。
沒有將未跑項列PASS；沒有借 lake build宣稱紙面或拓撲已形式化。

共同 guide／STATUS／HANDOFF／舊artifacts均未修改，L1採納交由監督端處理。
canonical worktree原有STATUS、guide及派工文件保留；同時出現的N45-A／S／U目錄屬其他任務。
本任務修改清單完全在本audit目录，詳见MANIFEST.sha256。
最終Git狀態及交付檔案hash另存delivery.json；未提交，無交付commit SHA。
