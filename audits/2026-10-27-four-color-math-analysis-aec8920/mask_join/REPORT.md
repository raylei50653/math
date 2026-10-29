# 將消元點的四色保留成mask，直接作完整boundary join

2026-10-27。這是獨立桶原型與數學分析，沒有修改主引擎、既有文件或預設。
基底HEAD為`aec8920`，實際檢查及凍結桶來源包含工作樹既有未提交修改，不能歸為純commit行為。

**新意在枚舉前把同一boundary下的x色合併，而不是合法完整指派找到後才壓縮儲存。**
固定同一anchor及free／ready次序，可證明mask前綴是literal前綴沿x座標的精確投影：
延伸嘗試及完成因子查詢次數不增加。全表預建mask仍可能因預處理而退步；
另做按需`known_bits / allowed_bits`原型，避開未查因子的整表掃描。
這些是工作子項的支配關係，沒有總CPU或整體求解加速定理。

## 主引擎目前是否已做

目前[`four_color_constraints.py`](../../../scripts/four_color_constraints.py)的桶流程在1390行選完整因子anchor，
`anchor`／`prefix`都從包含x色的完整列開始，再延伸free座標；每個literal x色分別核對其他因子。
成功後才在約1475行以`table[boundary] |= 1 << color`累積回填mask。
因此已上線的4-bit是**事後完整fibre儲存**；本原型是**枚舉期間的共同支援集合運算**。
當次來源hash與帶行號片段見[小型核對](results.json)及[原碼摘錄](results-current-bucket-excerpt.txt)。

## 精確關係恆等式

消元點為x，所有含x的當前完整因子為`F_i`，其範圍為`{x} ∪ B_i`。
令完整有序邊界S為所有B_i的聯集，當前域為D_v。對完整`b∈∏_{v∈S}D_v`定義

```text
M_i(b|B_i) = {c∈{0,1,2,3} : (x=c, B_i=b|B_i)∈F_i}，
W(b) = D_x ∩ ⋂_i M_i(b|B_i)。
```

集合用四色bitmask表示，集合交恰為bitwise AND；同一B_i列下面的所有x色用OR聚合。
逐色有`c∈W(b) ⇔ c∈D_x 且所有F_i均成立`，所以W正是完整自然join的x-fibre。
完整投影是`{b : W(b)≠∅}`，保留的mask包含全部回填色，缺席b表示空fibre。
空bucket的空交為全色集，故W=D_x；一元因子的B_i為空，仍是有效約束。

所有B_i座標均保留，包含只出現在一張表的私有boundary座標與不同原始欄序。
這不是先各自計算`∃x F_i`再作布林join：後者會混用不同x色。
負控制一側只允許x=0、另一側只允許x=1；各自投影接受16份boundary，正確mask交全空。
所有含x因子、當前域與字面色框須完整；其他不含x因子仍留在外側問題，不能丟掉。

## 固定anchor的逐深度支配

先固定與literal流程相同的anchor a、free順序`y_1,…,y_k`，以及各深度ready因子的順序。
只有因子的全部B_i座標具備時才查詢；它與literal流程的「包括x在內的最後座標具備」是同一時刻。
把同一anchor boundary `u`之下的所有合法x色合併，初始mask為`D_x∩M_a(u)`。

對每個已完成深度d的boundary前綴p，令L_d(p)為literal流程仍存活的x色集合。
mask流程保持的C_d(p)恰等於L_d(p)：初始是anchor的完整fibre；新增一個free色後，
逐一對所有本層ready因子的M_i求交，恰好刪去literal會因同一完整因子而失敗的色。
因此mask前綴存活當且僅當至少一個literal x色前綴存活，拒絕空mask不會漏任何延伸。

每次mask延伸可對應至少一份literal延伸；每份boundary前綴至多合併`q=|D_x|≤4`個literal節點。
對同層ready因子的第j次查詢，mask會執行當且僅當前j−1次後尚有一色；
該色在literal流程也必走到第j次。因此即使兩邊皆short-circuit，mask因子查詢次數仍不增。
此支配比較的是同一前綴樹的節點／查詢集合，不聲稱遍歷時序、有限預算中斷位置相同。

若改用另一份anchor或另一份free次序，這份逐節點對應不能直接套用。
查一次M_i的CPU成本、建索引、mask交集、字典、排序及回填輸出也不包含在節點支配內。

## 工作與空間界；何時預建會退步

令`F_i^D`為按全部當前域過濾後的因子，`r_i=|F_i^D|`，`n_i=|π_{B_i}F_i^D|`。
q>0時`n_i≤r_i≤q n_i`。固定anchor a與其free域乘積P_a，完整延伸的上界由
literal的`r_a P_a`變為mask的`n_a P_a`；少掉的是x重複，最多四色因子，不是消除寬S的指數。
若兩邊均以這些過濾後列數選最小上界，兩個最小值也落在1/q至1倍之間；
目前主引擎用原列數選anchor，本原型為驗支配而固定該選擇，沒有冒稱已最佳選型。

預建每份M_i需掃全部原始輸入列，構造完整B_i key：成本約`Σ_i |F_i|·|scope_i|`，
另有配置與排序；額外索引保存`Σ_i n_i`份key／mask。完整boundary直接查詢上界約m乘延伸上界。
prefix版本的節點上界為`n_a Σ_{d=0}^k ∏_{j=1}^d |D_{y_j}|`，ready因子在自己的深度才核一次。

固定x稀疏anchor反控制：anchor只有一列，另一張同scope因子有1,024列，卻只需查其中一列。
literal只掃1份anchor列、作1次membership；eager-mask先掃1,025列，在線次數完全相同。
若其他表的scope繼續擴大，預掃／直接查詢比例可無界增加；沒有總工作普遍支配。
K₄單一模板每boundary恰一個x色，線上節點亦不減，mask聚合只是額外準備。

## 按需mask：將未查與不允許分開

只聚合anchor。對其他不可變F_i及每份完整有序B_i key，保存`K=known_bits`及`A=allowed_bits`：

```text
不變式：A = M_i(key) ∩ K。
收到當前live色集C：
  只對C \ K中的色c查完整原列(x=c,key)是否屬F_i；把c加入K，成立才加入A；
  回傳C ∩ A。
```

回傳前C的每個色都已在K，故結果恰為`C∩M_i(key)`；K外的未知bit不會被當成不允許。
這維持同一逐深度投影定理。每次真的原列membership miss可對應literal流程在該前綴、
該色、該因子的同一次檢查，所以raw membership次數亦不增加；快取只再減少重查。
若Q_i個不同key曾被問，raw probes亦至多`q Σ_i Q_i`。正／負結果都精確保留。

這避免非anchor因子的整表預掃，但每次仍新增cache查詢、可能儲存、bit操作及key建構。
負key也會占空間，Q_i可大於非空投影n_i，最壞達B_i的域乘積；不能保證比eager更省RAM。
本原型每bucket重建快取；跨桶重用須另含因子身份、revision、owner與欄序契約。
有限容量可安全淘汰已知bit並重查，不能把未查色或超限當成false；整張輸出表仍須原子完成。

## 小型獨立Cartesian核對

[`audit.py`](audit.py)及[原始來源快照](audit.initial.py)在初次結果後保持不變；
[results.json](results.json)的來源hash逐份對上。共142份bucket條件：96份seed固定的任意完整因子，
36份目前主引擎在星、K₄、K₅、固定色五環的實際record，以及10份具名控制。
逐份直接Cartesian定義核4,821份完整fibres，含2,572份空fibre、4,235份合法桶指派；
另核每深度的attempted與surviving前綴色集合、候選／因子查詢／節點／更新支配。
涵蓋固定色、空域／空因子／空bucket、一元因子、不連續ID、欄序及各表私有boundary。

| 控制 | literal延伸／因子查詢 | eager-mask延伸／因子查詢 | demand raw membership |
| --- | ---: | ---: | ---: |
| 原四葉星的四份incident edge因子 | 624／624 | 336／336 | 48 |
| 四色全支援因子 | 1,344／1,344 | 336／336 | 48 |
| 固定x、稀疏anchor及大對照表 | 1／1 | 1／1，但預掃1,025列 | 1，且只掃1列anchor |

[`demand_audit.py`](demand_audit.py)在同142條件獨立核Cartesian、逐深度投影與raw-probe支配。
所有輸出完整mask相等，沒有只比SAT／UNSAT，也沒有只保留一份色見證。

## 真實40例的1,576份凍結桶重播

來源為[前輪prefix-delta完整報告](../../2026-10-27-four-color-method-comparison-aec8920/replay/prefix_delta/report.json)。
逐份核40個完整gzip記錄的hash，以每個record的input_relations、source_domains及有序scope當固定桶。
[`bucket_replay.py`](bucket_replay.py)不執行新的整體求解；[bucket-results.json](bucket-results.json)保存每桶結果。
eager及demand均精確得到同149,040份非空fibres及201,747個色選項；記錄域內另有1,883,563份空fibre。
大桶對照的是已存的完整fibre表及缺席空列契約，沒有另作大型Cartesian窮舉；小型獨立核對另列。

| 累計子項 | literal prefix | eager mask | demand mask |
| --- | ---: | ---: | ---: |
| 輸入列掃描 | 111,844份anchor列 | 219,724份全部輸入列 | 111,844份anchor列 |
| free延伸嘗試（無free時記成功候選） | 663,483 | 422,387 | 422,387 |
| 完成ready因子呼叫 | 1,292,686次原列membership | 887,440次完整mask查詢 | 887,440次支援cache查詢 |
| demand實際原列membership | — | — | 150,390 |
| 非空輸出更新 | 201,747 | 149,040 | 149,040 |

eager的「掃列＋延伸＋mask lookup」假想模型為2,068,013→1,529,551，少26.04%；
但1,576桶有617改善／260同／699增加。這個模型沒把tuple、bit、配置等當成逐項CPU操作。
demand若只數原有的「掃anchor＋延伸＋raw membership」，是2,068,013→684,621，
1,333桶少、243桶同，符合原操作子集支配；**684,621不包含新增支援cache與bit成本**。
不能把它與eager模型直接當完整成本排名。

[demand-results.json](demand-results.json)另列887,440次cache查、887,440次cache存、
887,440次live mask交集、111,844次anchor OR及150,390次新色探測。
本直接原型每次連未改變的cache也回存，尚可優化；其已列成本不能因可優化就當零。
1,142,296個已測色bit命中、71,153份新cache key均為跨桶累計，不是單次峰值或bytes。
沒有量測優化核心的牆鐘、主程序RSS、改算法後的傳播成本或新的有限預算完成率。

## 重播與接續判斷

```bash
python3 -B audits/2026-10-27-four-color-math-analysis-aec8920/mask_join/audit.py --out /tmp/mask-small.json
python3 -B audits/2026-10-27-four-color-math-analysis-aec8920/mask_join/bucket_replay.py --report audits/2026-10-27-four-color-method-comparison-aec8920/replay/prefix_delta/report.json --out /tmp/mask-buckets.json
python3 -B audits/2026-10-27-four-color-math-analysis-aec8920/mask_join/demand_audit.py --frozen-replay audits/2026-10-27-four-color-math-analysis-aec8920/mask_join/bucket-results.json --out /tmp/mask-demand.json
```

輸出檔須尚不存在；原小型audit另外保存當次主引擎片段，不覆寫先前結果。
對本專案，最值得接續的是**固定anchor的demand-mask桶**：有明確完整fibre恆等式、
前綴及raw-read支配，又避開eager整表預掃反例。下一步應在獨立核心實測完整準備／查詢／
cache／bit成本，再決定是否整合及如何計費；目前不因此改主引擎或聲稱一般加速。
這仍是有限精確關係運算，不提供固定寬度、Python形式化或平面四色存在性的額外證明。
