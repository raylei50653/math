# C8 共同 gadget 推進：五內點純 cap 完備界線與同圖計數控制

2026-10-13。Git BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。
本輪接續使用者指定的未提交 generalization 包；直接輸入凍結自當時工作樹，
不是把未提交報告宣稱已存在於 BASE commit。詳見 [INPUTS](INPUTS.json)。
全部新工作只在本隔離包；前兩份未提交 audit 與共享文件保留。

**主要新結論：在明列 plantri 完備性依賴下，任何至多五私人內點的簡單
平面 C8 cap，都不能與原八份必要上界 U 形成空交集。**
前輪的 2,274 份指定族無排除，現已提升為整個五點純 cap 域的無排除。
這是一項方法的精確界線，沒有新增來源排除，也不賦予八份 U 可實現性。
一般 `K∞=K≤5`、無界 932／933／941 仍 OPEN。

## 1. 契約與精確全稱範圍

沿用全域最小目錄外 C5 來源的 k，原 induced C8 內圖 H 有 k 個總頂點。
既有下降引理保證所有至多 k+5 點的 loopless planar 圖可四色。
故對外接 h≤5 私人點的 cap F，實際來源必有

\[
\Sigma_C(H)\cap\Sigma_C(F)\ne\varnothing.
\]

但目前只知道 `Σ_C(H)⊆U`，因此直接排除 U 需要 `U∩Σ_C(F)=∅`。
本輪證明這種**單份純 cap 的上界空交策略**在五點預算內無法成功。
並沒有證 `Σ_C(H)=U`，也沒有將 `U∩Σ_C(F)≠∅` 當作真正來源的存在證據。

八份 U 逐名取自 frozen no4ct 結果：c04/c07/c15/c18/c20/c30-941、
c15/c18-933。保留全部 274 個原 literal C8 rows、原接點順序、空 fibres
及完整私人指派；全部 D8 搬運都同時搬完整 row 與邊界對應。

## 2. 從任意 cap 到完整有限域

[紙面增廣引理](theory/PROOF.md)證明：任意簡單 disk cap 可在同一頂點集、
同一外圈上補邊成三角剖分。這涵蓋內部孤點、橋及不連通圖；補邊只縮小
完整關係，所以一份拒絕 cap 必給一份拒絕三角剖分。
該證明也核對三角化 disk 的二點割集只能是外圈 chord 的端點，與生成器
的類別限制完全對接。

使用 frozen plantri 5.8 的 `-aP8c2m2 n`，n=8..13，生成含外框弦與
邊界二度點的完整 embedded disk 類別；生成器完整性仍是外部程式依賴，
不是本輪新證的枚舉定理。[逐份結果與來源](search/REPORT.md)如下：

| 私人點 h | embedded 同構類 |
| ---: | ---: |
| 0 | 12 |
| 1 | 91 |
| 2 | 685 |
| 3 | 5,051 |
| 4 | 38,078 |
| 5 | 290,595 |
| 合計 | 334,512 |

每份檢查全部 16 種原邊界對齊，得到 5,352,192 份帶重複的對齊與
42,817,536 個 cap／query 測試。每次都檢查實際 rotation、原邊與完整染色。

| 原必要殘留 | 全純 cap 域的最小交集 |
| --- | ---: |
| c04-941、c07-941 | 2 |
| 其餘六項 | 4 |

保存 91,656,288 個完整 fibres，其中 76,526,879 個為空，以及全部
26,145,720 份 full lifts。壓縮 tuple 用每私人點兩 bits、原名字順序
編碼；counts 只用來分隔 fibres，不用計數取代完整 tuples。

[第二套 checker](independent_check.py)不 import producer：producer 對各
boundary row 搜索私人延伸；獨立版先枚舉所有 proper 私人指派，再以
boundary bitsets 分派到全部原列。逐 fibre 比較 counts 與**完整 tuple
集合**，並獨立搬運八份 U；正常與 seed17 通過，破損 count／tuple 被拒。
這覆核全部已生成圖的內容，不獨立證明 plantri 沒有漏圖。

## 3. 共同等式與不等式比純 cap 多出的範圍

本輪也把外側 chord 標為 equality scaffold 或 inequality edge，
同時收縮所有 equality chords。逐份檢查原 C8 邊及所有 inequality
邊都不成 loop；全部操作在同一 exterior disk 內實現。
若 h 個新增點、識別淨省 d 個原點，使用的預算是 `k+h−d≤k+5`。
不同 gadget 的成功列沒有被合併。

第一族是所有 polygon dissections 加可選 face hubs，覆蓋 15,766 份
合法共同 gadget（另拒 8,652 份 loop 構造），3,284 份不同完整關係。
[v2 完整證書](quotients/certificate.v2.json.gz)保存 4,319,884 個 fibres、
578,038 份 full lifts；[獨立 checker](theory/signed_check.py)以另一種
面分解重建族，再由具名商圖 DFS 核對全部 tuples。v1 為先前 discovery
快照，保留作過程證據，正式重播使用 v2。

這族沒有排除 U；c15/c18-933 的最小交集降為一列，給相應的必要正性。
下一族在同一 h≤5 完整三角剖分域中允許任意相鄰私人點，並對每條 boundary
chord 選 Eq 或 Diff。共 2,599,458 份合法簽名，全 16 種原邊界對齊下
仍無排除；最小交集依查詢順序為 `2,2,1,3,1,2,3,2`，已在零私人點
層達到。[signed 結果](search/SIGNED_RESULTS.json)保存各層統計；
其 204,250,566 份同列私人 full lifts 全保存。用每 row 的 Eq-signature
索引還原 712,251,492 個 signed fibres（643,620,314 空），不相符簽名的
cell 明確為空。[獨立覆核](review/SIGNED_VERIFICATION.json)以私人指派
枚舉及 equality transitive closure 比較全部 tuples、簽名與
332,730,624 份 query／對齊查詢。兩個 933 查詢各有四個 forced rows：
`c15-933: [19,33,188,249]`、`c18-933: [44,67,157,188]`，都是固定
原列索引；具名 full-lift witnesses 保存在 search 子包。
兩族都是明列的 simultaneous quotient 家族，不能冒稱覆蓋所有
`a−d≤5` 的可能 gadget、其他原面上的限制或來源特有識別。

## 4. 同一計數向量與完整 Kempe 軌道

[共同計數報告](review/COUNT_REVIEW.md)重新對最新八份 U 給精確證書，
包括 c15/c20-941 在舊 count 證書之後各被刪去的兩列。
每份新向量在其 U 上全正、U 外為零，符合 equality span、十列 collar
transfer 及既有支援 Kempe 必要條件。

另證一個同圖必要條件：固定互補色對 01|23，實際全圖染色分解為完整的
component-flip 軌道；各 boundary row 的 multiplicity 必由相同軌道
共同提供。保留 G8 軌道權重後，得到 821 維 state 上、1,552 個完整
boundary flip-orbit 欄生成的非負有理錐。八份 U 仍各有精確非負分解，
並由四份實際 disk 圖直接全 lifts 對照。未聲稱此錐相對既有條件嚴格更強。

因 x 在 U 全正，對任何與 U 相交的 gadget relation R，都有
`sum_{p∈R}x_p>0`；真正 cap 計數則加各 row 的正 orbit 權重及 cap lift
數，結論相同。因此**同一份數值 x**能同時滿足本輪全部非空不等式。
這沒有把 `∀gadget∃row` 換成 `∃row∀gadget`，也沒有構造一份來源 H。
新增條件仍可能刪去其他數值向量；本輪只證未造成不可行或縮小最大支援 U。

## 5. 可重用紙面縮減與下一個確切缺口

[四度点完整計數分解](theory/PROOF.md)保留 cap 內四度點 v 的原鄰環
u0u1u2u3。逐份原 lift 有

\[
4-|\psi(N(v))|=[u0=u2]+[u1=u3],\qquad
x_F(p)=x_{Q02}(p)+x_{Q13}(p).
\]

每個 Q 分支先刪 v，再識別一對對角點；原邊成 loop 的分支為零。
兩等式同時成立時保留重數二。非零分支的同圖總頂點恰為 `k+h−2`，
兩個原 boundary pins 合併時仍保存它們到商圖的原名字映射。
它提供完整計數的可用縮減，沒有把商後邊界當作新的 simple C8。

另得到一個精確識別上界：在 C_b 的同一空側，對原環作 noncrossing
independent partition，若識別淨省 d 點，則

\[
d\le\lfloor b/2\rfloor-1.
\]

證明取 block 內的 chord forest；其 d 條弦切出 d+1 個面，每面至少含
兩條原環邊。因此 C8 有 `d≤3`。全部 scaffold 收縮後，尚存 a 個新點
的共同預算是 `a≤5+d≤8`。這只限在同一 exterior disk 識別原 C8 pins，
不限制其他原 H 點的識別，也未證本輪 signed grammar 完備覆蓋這個域。

本輪結論改變了下一步選擇：繼續找一份五內點純 cap 來直接拒絕原 U，
已在明列生成器依賴下用盡。真正未覆蓋的是更一般的共同識別／附加限制
（特別是收縮後仍有六至八個新點的合法 gadget），
或使用同一原 H 的 actual faces、degree、separator 與完整 lifts 證出
比 U 更小的必要關係或計數矛盾。已測共同 gadget 的非空性本身還不夠。

## 6. 證據層與發布邊界

- 紙面：同點集 cap 三角化、二點割集介面、四度點逐 lift 計數分解、
  exterior 識別淨省界，
  固定互補色對的完整交換錐必要條件。
- 有限：完整五內點純 cap 域、明列共同 quotient 家族、八份精確計數
  證書；generator 依賴、完整 fibres 及破損控制各自列出。
- 原來源：八項全部仍保留；没有 source realization 或新排除。
- Lean：沒有新增形式化；不以舊 `lake build` 代表本輪結果。
- 共享文件與 Git：只寫本包，沒有 commit／push，未重播未修改的共享
  DocGraph／Lean／外部球面證書。已核對本包連結、whitespace 及輸入漂移。

具體命令、實際出口碼與 custody 見 [VERIFICATION](VERIFICATION.json)。
本包不是一般主命題 closure；下一輪應從上述未覆蓋義務接續。
