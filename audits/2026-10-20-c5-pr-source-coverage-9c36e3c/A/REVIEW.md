# A：P/R 文法來源覆蓋的量詞、等價與計數反控制

2026-10-20。獨立審核 BASE `9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。
本審核讀共用 frozen，不修改來源文件；另由 `git show BASE:path` 凍結
原 cell 定義／有限枚舉報告與 `cells.json`，雜湊見
[additional-inputs.json](additional-inputs.json)。

**結論**：一般 disk 的「同一個 F/C 文法代表保持全部 P/R 未來四列支援」
與「同一個代表保持完整十列支援」完全等價。前者沒有把來源覆蓋義務變弱。
它等價於所有來源的支援都屬於 `K132`。若沿用既有有限
`K≤5=K132` 的 catalogue authority，這正是 `K∞=K≤5`。
相對地，若把「支援」改成「固定字面著色計數」或完整 fibres 雙射，
一般來源覆蓋已由本節的內部葉點 disk **反駁**；不是同一個 OPEN 命題。

## 1. 固定 source contract

來源域 `D` 是 frozen [實圖語義報告](../frozen/audits/2026-10-19-c5-pr-disk-semantics-ed59843/REPORT.md)
§1 的有限簡單平面 disk 圖，外框為五個相異點組成的有序
`B=(b0,b1,b2,b3,b4)`，其餘點、邊在內部，允許內側 chords。
不加 induced、near-triangulation、critical、度數或 r6 附件條件。
每次 P/R 皆在目前外框進行，字串由左至右作用。

十列固定為：

```text
i:    0     1     2     3     4     5     6     7     8     9
row: 01012 01021 01023 01201 01202 01203 01212 01213 01231 01232
```

`F_G(alpha)` 是同一張 G、同一字面外框 alpha 的全部 proper 四色染色；
空 fibres 也保留。`n_i(G)` 是固定 canonical 字面指派的延拓數，
`s_i(G)=1[n_i(G)>0]`，`Sigma(G)=(s_0,...,s_9)`。
這裡的「完整十列」指十個支援 bits 全部保留，並非保留十個 fibres 的所有成員。

四列觀察是 tuple `O(s)=(s9,s1,s4,s6)`；每個 tuple 的四項共同求於同一來源。
本審核不把它換成單一布林 predicate
`s9 and not s1 and not s4 and not s6`，也不只問 exact-319 reachability。
那些較弱觀察有別的等價關係，不能套用下面的充要條件。

文法 `Gamma={F,C}{P,R}*` 使用 frozen 明定的實圖種子與操作。
`F` 是五點 fan（邊界加 `b0b2,b0b3`），`C` 是無弦五圈。
兩者內點數均為零；P 的成本是一個內點，R 成本為零。
同標號 comparisons 不先作各自獨立 D5 canonicalization。

## 2. 兩來源的四列全部未來行為充要條件

對任意 `G,H in D`，定義

```text
G ≡O H  iff  for every w in {P,R}*, O(Sigma(wG)) = O(Sigma(wH)).
```

所有字串都合法，故沒有把未定義操作當拒絕的 partial-language 問題。
實圖語義給同一來源完整 fibres 的轉移，取支援後得確定性 Boolean P/R。
因此 `Sigma(G)=Sigma(H)` 蘊含 `G ≡O H`。

反向只需三個共同後綴，皆從同一初始來源及原有序框的副本執行。
將 `RR, PRR, RRR` 的四列結果分別記為 `a,b,c`，分量從 1 起算。
frozen 三探測恆等式為

```text
a = (s2,s4,s0,s1)
b = (s5,s9,s7,s3 OR s8)
c = (s8,s6,s1,s3)

s = (a3,a4,a1,c4,a2,b1,c2,b3,c1,b2).
```

每個原 bit 都是直接讀取的座標；沒有由不同候選的 marginal 拼接。
若全部未來觀察相等，這三個觀察相等，逆公式遂給 `Sigma(G)=Sigma(H)`。
故

```text
G ≡O H
  iff the three probes RR/PRR/RRR agree
  iff Sigma(G)=Sigma(H).
```

這是任意大小 disk 的圖層命題，不須先假設 `Sigma(G)` 屬於 K132，
也適用於形式零支援。它使用 frozen 任意大小操作語義及代數恆等式；
不是由有限 132 態的分割數字外推。

以固定字面計數替代支援，將上式的 OR 換成加法，同一逆公式也直接成立：

```text
all future four-count tuples agree iff n(G)=n(H).
```

所以 counts 與 support 各自有完整解碼，但兩種代表問題不可互換。

## 3. 來源覆蓋與 K∞ 的精確量詞

令 `K_Gamma={Sigma(H):H in Gamma}`，
`K∞={Sigma(G):G in D}`；此定義先不排除可能的零支援。
文法圖皆是合法 disk，故 `K_Gamma subseteq K∞`。
frozen 文法閉包及圖語義給 `K_Gamma=K132`。
對**每一張固定來源 G**：

```text
exists H in Gamma, for all w, O(Sigma(wG))=O(Sigma(wH))
iff exists H in Gamma, Sigma(G)=Sigma(H)
iff Sigma(G) in K132.
```

而一般來源覆蓋是

```text
for all G in D, exists H in Gamma, for all w, ...
iff K∞ subseteq K132
iff K∞=K132.
```

`H` 可以依 G 選擇，但必須先選定，不能隨後綴 w、觀察座標、
或 accepted/rejected row 改換候選。較弱的 `for all w, exists H_w`
不是此來源覆蓋命題，也不能供應同一候選的完整十列。

frozen 文法最小成本資料另外給每個 K132 支援一個不超過五內點的 F/C 代表。
因此上面的 H 可加上 `interior(H)≤5` 而不改變充要條件。
這是**文法內支援代表成本**，不是原來源的完整 fibres、內面形狀、
原頂點身份、attachment 或 matching witness 的保持定理。
只有原來源多於五內點時才自動得到 strict vertex decrease；
接回附加結構的成本及較強 source contract 仍須另證。

對指定較窄來源族 `R subseteq D`，同樣的定理只給
`coverage(R) iff {Sigma(G):G in R} subseteq K132`。
這個局部覆蓋可能比一般 `K∞=K132` 弱，不能把 r6 的量詞改成任意 disk，
也不能從一般域的反控制推定其滿足 r6 額外前提。

## 4. 與 K≤5 的連接：分開有限 authority

原 [cell 窮舉器文件](frozen/docs/c5_cell_enumerator.md) §3 記錄
`k≤5` 精確枚舉得到 132 個 keys；文件把 catalogue 數字列為
computationally observed，沒有宣稱 catalogue 的 Lean 證書。
§0.5 明確區分 witness replay 與重新掃描 `2^40` 全部邊子集。
因此 frozen atlas 的「132 個已知 witness」本身只證一個下界，
不能單獨充當 `K≤5` 的完備上界。

本輪 [checker](check_contract.py) 僅重核：

1. BASE 保存的 `cells.json` keys 與文法 `model.states` 逐項相同，共 132 個。
2. 兩者使用同一十列順序，0 與 932 都不在清單。
3. 葉點例完整字面 fibres、實圖局部 P/R 編譯、下面的整數障礙。

本輪沒有重跑五內點 graph enumeration，也沒有把 saved keys 的相等
升格為獨立的 catalogue completeness proof。
**沿用原 bounded census 的 `K≤5=K132` identification 時**，
§3 的一般支援覆蓋與 `K∞=K≤5` 等價。
不使用該 identification 時，無條件的本輪化約停在 `K∞=K132`；
文法至多五內點 representatives 仍給 `K132 subseteq K≤5`。

## 5. 不使用 4CT 時的零來源與 932 界線

本審核沒有使用 frozen Kempe/exterior 報告的 4CT 外側排除。
因為 P/R 矩陣非負，零支援在兩操作下仍為零；文法狀態沒有零。
因此一個零支援 disk 若存在，就是一般文法覆蓋的反例，不能在定義中默默刪掉。
若另限制為已知可四色染的來源 `D+`，§3 改成 `K∞+ subseteq K132`；
這個限制版沒有解決原 `D` 中非空性的義務。

實際上，把任意有限平面圖放入 C5 內側作私有分量，就得到此一般 disk 域的來源；
一般來源覆蓋會推出該平面圖可四色染。這只是量詞強度的提醒，
不是本輪採用 4CT 的證明。

932 是非空形式支援，且不在 K132；它也沒有被本輪排除。
frozen 外側 wheel 加 4CT 的排除屬另一條明示前提的證據。
同樣地，933／941 十個固定標號 masks 的一般來源未由觀察解碼、
文法零可達或支援代表成本所排除。

## 6. 計數與完整 fibre 覆蓋的一般反例

取有序無弦 C5，在其內側添一個新點 x，只連邊 `xb0`。
這是 §1 域的合法連通簡單 disk 圖，記為 L。
每個 proper 字面外框都有恰好三個完整延伸：x 可取除 b0 色外的三色。
故

```text
Sigma(L)=1023=Sigma(C),
n(L)=(3,3,3,3,3,3,3,3,3,3),
n(C)=(1,1,1,1,1,1,1,1,1,1).
```

這不只反駁「C 是 count 代表」；L **不存在任何** F/C 文法 count 代表。
理由如下。固定 P 前的任意整數向量 x，令 `y=M_P x`。
由實際局部賦色可直接讀出

```text
y1 = x3+x8,   y3 = x1+x8,   y8 = x1+x3,
y1+y3+y8 = 2(x1+x3+x8).
```

因此每個 P 輸出的這三項之和必為偶數。若某文法字含 P，
取其最後一個 P；之後只有 R。常向量 `(3,...,3)` 在所有 R 下不變，
故最後 P 的輸出也必為 `(3,...,3)`，但三項和為 9，矛盾。
若文法字沒有 P，只有 F/C 種子及旋轉，計數均為 0/1，
也不是目標向量。故不存在同十列計數的文法圖。

§2 的 count 解碼遂給：沒有任何文法圖能保 L 的全部 P/R 未來四列計數。
逐字面完整 fibres 的雙射必保 cardinality，故也不存在這種文法代表。
這個反例沒有否定 P/R **操作本身**的完整 fibre 雙射；
否定的是從任意原來源到某個文法來源的另一種雙射。

對任意正整數 m，在 b0 附 m 個互異私有葉點，同一論證給
`n=(3^m,...,3^m)`。三項和仍為奇數；因此得到任意多內點的反例族。
它不滿足 near-triangulation、最低度數或 r6 額外前提，
不得把這個一般域的反例跨域使用。

這也說明支援代表不會自動供應原完整 lifts 或內部 Kempe 結構。
三角面插點的自然 restriction/unique-extension 雙射則是另一個可證子類；
inverse-P/I 幾何、任意大小的該子類與幾何反控制由 C 審核處理。

## 7. 重播及停止點

```bash
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/A/check_contract.py --check
```

[contract_controls.json](contract_controls.json) 保存 L 的十份 canonical fibres，
每份列出全部三個六頂點字面染色；並對全部 240 份 proper 字面外框核對恰三個延伸。
P/R 從新舊外框實際色值編譯，再比 frozen 矩陣；整數 parity
按矩陣係數恒等式核對，不以抽樣有限整數向量取代證明。
`--check` 只讀，`--write` 排他建立輸出，不覆寫。

**已完成**：一般來源的支援等價化約、有限 catalogue authority 分離、
量詞／零來源／932 保留、一般 count 與 fibre 代表覆蓋的反例。

**OPEN**：一般 `K∞=K132`（在既有 bounded authority 下即 `K∞=K≤5`）、
指定剩餘 r6 的實圖文法代表或成功／更小 bad 化約。
沒有新增 Lean theorem、文獻新穎性判定或任意大小來源排除。
