# B：P/R 形式支援轉移與反向來源覆蓋的障礙

BASE：`9c36e3c4789dfec07d60ec4e042f0bafe17451d1`。本工作僅寫 B 目錄。
輸入是 audit 的 frozen v0.2 certificate、disk semantics 報告及 screen 定義；
不讀浮動的 catalogue、不枚舉一般圖、不用 exterior/4CT 篩選。

**主要結論：933／941 的所有 D5 對齊一遇 P 就進 K132，之後永遠在 K132；
這不給原來源的反向文法覆蓋。932 不滿足「任何 P 立即抹掉 outlier」：
`932 --P--> 63 --R--> 459`，而 `P(459)=459`。**

## 1. 精確域、局部重建與權限

令 \(U=\{0,\ldots,1023\}\)，十 bit 依序為
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
以下所有集合及量詞首先都是 **形式支援 masks**，含空 mask 0。
令 \(T_w\) 表示由左至右執行字串 \(w\in\{P,R\}^*\)。

[checker](check_transition_obstruction.py) 從如下接線獨立枚舉字面局部染色：

- 舊邊為 `01,12,23,34,40`。
- P 加新點 5 與邊 `50,51,54`，新有序框為 `(5,1,2,3,4)`；
  固定新框的一列，枚舉唯一未固定的舊點 0 之四種顏色。
- R 保留舊圖，新有序框為 `(4,0,1,2,3)`。

各列經全色盤一致正規化後所得整數矩陣，再與 frozen v0.2 矩陣比對，
沒有以附件轉移表定義接線結果。從有弦 `02,03` 的五邊形直接讀得 F 種子 960，
以新編譯矩陣求閉包，得到恰 132 態，再與附件逐態逐邊比較；
加 C 種子 1023 後閉包相同。以下記此閉包為 K。

任意實際 disk 的 P/R 圖層合法性與完整 fibre 雙射，由 frozen
[disk semantics 報告](../frozen/audits/2026-10-19-c5-pr-disk-semantics-ed59843/REPORT.md)
承擔；本 checker 只獨立核對局部編譯及有限代數。
若 G 確是該報告的 disk，則可代入 \(\Sigma(G)\)；
**並未因此聲稱 U、下列21個 extra masks 或其中任何 outlier 有實圖來源。**
這裡沒有來源減小、實際附件接回、較強論文來源前提或 Lean 證明。

## 2. 全 1024 態的前像與吸收

| 有限事實 | P | R |
| --- | ---: | ---: |
| 像大小 | 640 | 1024 |
| \(T^{-1}(K)\) 大小 | 256 | 132 |
| K 外一步進 K | 124 | 0 |
| K 內一步離開 K | 0 | 0 |

P 的非空前像 fibres 有 512 個大小 1、128 個大小 4。
每個四前像 fibre 只在原 mask 的座標 `{1,3,8}` 不同：
這三座標至少兩個為 1 的四種情況有相同 P 像；其餘七座標完全相同。
這是 Boolean 支援損失，沒有聲稱整數計數的 P 矩陣不可逆。

因此，對所有 \(m\in K,w\in\{P,R\}^*\)，\(T_w(m)\in K\)。
但 \(P(m)\in K\Rightarrow m\in K\) 在 U 上為假；
一個明確 witness 是 \(941\notin K\)、\(P(941)=447\in K\)。
更強地，`P(941)=P(935)=P(943)=447`，而 `935,943∈K`：
對所有共同後綴 v，三者在先做 P 之後的完整支援相同。
這僅是形式反例，不能當作未知 disk outlier 的實現證明。

還可完整算得：對每個 \(m\ne0\)，存在有限字串 w 令 \(T_w(m)\in K\)。
最少 P 次數分布如下；證書逐態保存一個達到最小 P 次數的有限字串。

| 最少 P 次數 | 0 | 1 | 2 | 3 | 4 |
| --- | ---: | ---: | ---: | ---: | ---: |
| masks 數 | 132 | 355 | 386 | 135 | 15 |

checker 另逐邊驗證 `d(s)≤cost(op)+d(T_op(s))`，在 K 上 d=0；
此不等式沿任意到 K 的路徑 telescoping 給下界，所附 witness 給同值上界。
所以這裡的最少成本並非只有一次搜尋輸出的標籤。

0 對兩字母皆自環、不能進 K。非空 basin 恰 1023 的成本結論是
\(\forall m\ne0\,\exists w,\ |w|_P\le4,\ T_w(m)\in K\)。
此外，本模型還有下面的共同字串結論；兩者都沒有給任意字串均會成功
或原來源覆蓋。若代入非空的實圖支援，最多4次 P 的 pointwise 結果只會添
至多4個 collar 頂點，改變目前外框；不保存原色框、不減小原來源。

### 2.1 固定17次 P 的共同外側 collar

令

\[
W=RRR(PPR)^4P(PRP)^4.
\]

此字串有28個字母、17個 P；[補充證書](universal_collar.json)
保存每個前綴作用於十個 singleton masks 的完整軌跡，
終態十個都為1023。P/R 是 Boolean 矩陣作用，保存聯集，
故每個非空 mask（singleton 的非空聯集）亦滿足

\[
\boxed{\forall m\in U\setminus\{0\},\quad T_W(m)=1023.}
\]

[補充 checker](check_universal_collar.py) 同時直接重播全部1023個非空 masks，
並核對兩個字母在全1024 masks 上的聯集保持性。
沒有最短共同字串或最少17次 P 的宣稱。
較直覺的 `(PR)^n` 並不成功：十個 singleton 的像向量在 n=10 起進入
4-cycle，始終有未到1023的分量；補充證書保存 n=0..14 的完整負控制。

對任意具有**非空**完整支援的合法 disk G，frozen P/R 雙射遂給出實圖
`W(G)` 的支援恰為1023，且內點數比 G 增加17。
這裡並不使用4CT保證 G 的支援非空，也不保存 G 的原外框。
共同外側 collar 能消除全部非空形式支援的差異，正好顯示
「往前加工後支援有文法代表」無法自行提供原來源的覆蓋或排除。

## 3. 933／941：精確的任意字串定理

| m | P(m) | R(m) |
| --- | ---: | ---: |
| 933 | 191 | 996 |
| 934 | 319 | 933 |
| 940 | 319 | 934 |
| 948 | 575 | 940 |
| 996 | 127 | 948 |
| 941 | 447 | 998 |
| 949 | 703 | 1004 |
| 950 | 831 | 941 |
| 998 | 383 | 949 |
| 1004 | 383 | 950 |

表的前五列為 D5(933)、後五列為 D5(941)；十個 P 像全在 K，
兩個 R 軌道各在自身內且與 K 不交。故精確量詞為

\[
\forall m\in D_5(933)\cup D_5(941),\quad
\forall w\in\{P,R\}^*,\qquad
T_w(m)\in K\ \Longleftrightarrow\ w\text{ 含至少一個 P}.
\]

證明只需按第一個 P 分割字串 `w=R^aPv`：
`R^a(m)` 仍在同一軌道，P 後進 K，再用 §2 的 K 前向封閉。
無 P 的字串只是 R 軌道，仍不在 K。
這是任意有限字串的結論，不是測到某個長度的經驗。
任意 boundary 位置的帶 spoke push 可由旋轉前後共軛實現，
所以換 push 位置亦不能恢復已丟掉的這項支援區別。

## 4. 932：六個 K 外態與一個 K 吸收狀態

`D5(932)={932}`。從 932 可達的 K 外態恰為六個；
將所有 K 態合併為吸收符號 K，得到精確 quotient：

| 狀態 | P | R |
| --- | --- | --- |
| 932 | 63 | 932 |
| 63 | K（942） | 459 |
| 459 | 459 | 599 |
| 599 | K（1016） | 249 |
| 249 | K（967） | 858 |
| 858 | 858 | 63 |
| K | K | K |

若 w 沒有 P，終態為 932。
否則唯一分割 `w=R^aPv`，第一個 P 後從 63 開始，
其 R cycle 依 residue `0,1,2,3,4` 為
`63,459,599,249,858`。

對 v 中任一個 P，計算它之前在 v 中出現的 R 總數 modulo 5：

- 若有一個 P 的此 residue 屬於 `{0,2,3}`，則終態在 K。
- 若所有 P 的此 residue 都屬於 `{1,4}`（也包括 v 沒有 P），則終態在 K 外。

理由是在首次進 K 之前，P 在 residue 1、4 自環，故 R 的累計數正好記錄狀態；
首次在 residue 0、2、3 執行 P 即進 K，之後無法離開。
這描述了所有有限字串，包括任意多個 P：
`PP` 進 K，但對所有 \(n\ge0\)，`PRP^n` 的終態都等於 459。
因此不存在僅以「已執行多少次 P」保證進 K 的統一門檻。

## 5. no4ct 額外軌道的範圍

frozen screen 文件的純 Kempe 必要條件接受 153 個非空 masks，
其 K 外差集有 **21 個 masks、5 個 D5 軌道**；
不能把未用 4CT 的範圍簡寫成只有 932／933／941 的 11 個 masks。
本證書保存這五個報告中列出的軌道及其全部 P/R 邊：

| 代表 | 軌道 |
| --- | --- |
| 7 | 7, 56, 193, 266, 592 |
| 63 | 63, 249, 459, 599, 858 |
| 932 | 932 |
| 933 | 933, 934, 940, 948, 996 |
| 941 | 941, 949, 950, 998, 1004 |

這 21 態加 K 對 P/R 封閉。額外的 7 軌道之 P 邊為
`7→424∈K,56→774∈K,193→193,266→266,592→592`。
本 checker 從局部接線重算這些邊，但沒有把先前 Kempe 紙面 soundness
或該 screen 的分割完整性重新標成自身已證的圖論定理。
本輪不使用 screen 的 exterior 部分。

## 6. 能推與不能推

假設有一實際合法 disk G 的完整支援屬於 D5(933) 或 D5(941)，
§3 可以推出每個含 P 的字串所造 disk，其支援有 F/C 文法代表。
這個條件句並不推出 G 自己有文法代表：
原支援在 K 外，且 forward support transition 的前像確實有 K 外候選。
要證一般來源覆蓋，仍須獨立證明原來源不落在這些 K 外完整支援，
或提供來源層逆向構造／歸納與完整接回證明。

對「完整支援相同」的代表要求，任意 mask 在 K 外便不可能等於某個 K 代表。
對保留所有共同後綴四列觀察的代表要求，frozen disk semantics 的三探測可恢復
原十列支援，所以也不能用先 P 後的支援碰撞偷換為原來源行為相同。
這不是已經建出 disk counterexample；只是明確指出有限轉移閉包不能補足的量詞。

## 7. 證書與重播

- [完整可讀證書](transition_obstruction.json)：所有 1024 條雙後繼、
  K、P/R 全部非空前像、124 個一步進 K 的外部 masks、21 態表、
  932 quotient、全部1023非空支援的最小 P 成本與 witness。
- [正常生成](normal.log)、[只讀重播](check.log)、
  [seed17 重播](seed17.log)：皆 exit 0，canonical certificate SHA256
  `c5a128a4de09fece8f3dd42d90372c4af49b3fe476a1d3a242f48c0b43a06349`。
- [污染證書](polluted_transition_obstruction.json) 將
  `932_outside_quotient.932.P` 偷改為 K；
  [污染控制](pollution_control.log) exit 1，明確報 `Certificate mismatch`。
  污染副本與失敗輸出均保留，未覆寫正常證據。
- 全邊成本不等式加入後的 [rank 重播](rank_check.log) 仍 exit 0，
  原 transition certificate bytes 及 SHA 不變。
- 固定共同 collar 的 [正常生成](collar_normal.log)、
  [只讀重播](collar_check.log)、[seed17](collar_seed17.log) 皆 exit 0；
  SHA256 為 `f776a67219bc023157ee1a034f9ebcf6478613b6c1f110737d32db4690a8e224`。
  [污染副本](polluted_universal_collar.json) 偷改 singleton 1 的終態為1022，
  [污染控制](collar_pollution_control.log) exit 1，副本與失敗輸出均保留。

從 repo root：

```bash
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_transition_obstruction.py --check
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_transition_obstruction.py --check --seed 17
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_transition_obstruction.py --check --certificate audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/polluted_transition_obstruction.json
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_universal_collar.py --check
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_universal_collar.py --check --seed 17
python3 -B audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/check_universal_collar.py --check --certificate audits/2026-10-20-c5-pr-source-coverage-9c36e3c/B/polluted_universal_collar.json
```

第三、六條預期非零退出。`--check` 僅讀檔；生成模式用 `open("x")`，
預設證書已存在時拒絕覆寫。seed17 只打亂內部全域 mask 遍歷順序，
不更改正規輸出；不是額外圖樣本或不同證明域。
