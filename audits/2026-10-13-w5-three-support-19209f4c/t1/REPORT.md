# W3-TRANSPORT：固定五輪中心所需的具名三色 support

2026-10-13。本檔是父隔離包的獨立紙面核對，不修改共用文件。
凍結來源由 [`../INPUTS.json`](../INPUTS.json) 指定，BASE 為
`19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
使用者已指示暫不追查「T1」名稱；本檔以新的明確標籤陳述，**不宣稱找到了
某份原 T1 證明**。

結論是：對固定、原位接回的五輪中心，三色具名 support 相等確實足夠；
它還恰好等價於存在保持全部十個 pins 的雙向 full-lift 對照。
這項充分性已明載於凍結的
[`review/THEORY.md` 第 6 節](../../2026-10-12-w5-marked-relation-e299ae98/review/THEORY.md)；
本檔將必要性、對照的精確意義、不能推出的事項分開核對。
**這並未構造任意來源的 r≤6 代表。**

## 1. 介面與適用範圍

令 A、A' 為有限簡單 plane annulus 圖，邊界為同一有序具名
`B=(b0,...,b4)` 與 `U=(u0,...,u4)`。兩環不交，U 的原邊為 C5。
兩圖均須在同一 annulus 槽位合法嵌入；其 B/U 方向、原附件所在側及所有
保留 ports 的旋轉次序必須一致。私人頂點可不同。

保留 A 的原完整邊表、旋轉、attachments、ownership 及 fibres 供追溯；
A' 的內部修改另給合法記錄。支援關係相等本身不會證明這些幾何條件。
本 theorem 只比較已通過這些條件的兩張圖。

固定色集 `C={0,1,2,3}`，只許**全圖共同**更名顏色。對任意 proper B 色列 β、
完整具名五元组 τ，令

\[
J_A(\beta,\tau)=\{\eta:\eta\text{ 為 A 的完整 proper 染色},
\ \eta(B)=\beta,\ \eta(U)=\tau\},
\]

\[
R_A^3=\{(\beta,\tau):J_A(\beta,\tau)\ne\varnothing,
\ |\operatorname{im}\tau|=3\}.
\]

三色指 **U 所用色數恰為三**；不是 β 也只能用三色，不是 τ 的獨立標準化，
不是三個色名的 unordered set，也不是每個 pin 的個別 support。
對十個既定 β 代表核對時，τ 仍保留原四個色名。

proper C5 的 τ 恰有 240 個：120 個三色、120 個四色。三色型為 `(2,2,1)`，
可由單色位置的五選擇及三個色名的 `4·3·2` 選擇計數。
所以 W3 條件每張圖比較 `10·120=1,200` 個具名 cells。
證據可仍保存全部 `10·1024=10,240` cells，包括 improper τ 及所有空格；
放寬比較義務不表示刪掉來源證據。

在 U 的空內盤補入 v 及全部五條原位 spokes，得 `G=A+v`、`G'=A'+v`。
當且僅當 τ 用三色時可接中心，而且中心色唯一：

\[
c(\tau)=C\setminus\operatorname{im}\tau.
\]

此式右側是單元素集；以下也以 c(τ) 表示其唯一元素。

## 2. W3-TRANSPORT 定理及雙向證明

以下兩項等價：

1. `R_A^3 = R_A'^3`。
2. 在 G 與 G' 的全部完整染色之間，存在一個兩側皆 total 的關係 T，
   使每個被配對的完整染色在全部 B/U pins 上逐點相同。

「兩側皆 total」指每份 G 染色至少配對一份 G' 染色，且每份 G' 染色至少
配對一份 G 染色。不要求單值或雙射，也不要求兩圖私人點可識別。
中心色自動相同。

**1 ⇒ 2。** 對每個共同非空三色 cell，放入其完整 fibres 的 Cartesian product：

\[
T=\bigcup_{(\beta,\tau)\in R_A^3}
\{((\eta,c(\tau)),(\eta',c(\tau))):
\eta\in J_A(\beta,\tau),\ \eta'\in J_{A'}(\beta,\tau)\}.
\]

每份 G 完整染色限制於 A 得到一個非空三色 cell；由 support 相等，該 cell
在 A' 有至少一份完整 lift，且相同 c(τ) 可補中心。故 T 在 G 側 total。
反向同理，故 T 在 G' 側也 total。每一個配對使用**同一** `(β,τ)`，
没有拼接兩個不同商圖中僅各自存在的 witnesses。

**2 ⇒ 1。** 若 `(β,τ)∈R_A^3`，取任意該 cell 的完整 lift，補唯一中心色即得
G 染色。T 的 total 性供應一份相同 B/U 顏色的 G' 染色；限制於 A' 即證
`(β,τ)∈R_A'^3`。交換 A、A' 得反向包含。

**有限構造性。** 若需要兩個單值演算法，可固定每圖的原頂點順序與色序，
枚舉指定 cell 的所有完整染色並選字典序最小者。前向、反向各用此規則。
它們保持 pins 及中心色，但通常不是互逆函數。上式完整關係 T 則涵蓋每一份
原、新 full lift。只存一份 representative lift 可以驗證 support 的非空性，
不能無損還原其他原始 lifts；來源完整 fibres 仍須保存。

**幾何 glue。** 在相同方向的 U 空內盤補相同中心和 spokes，不產生穿越；
B 仍為外框。任何未修改的框外 context，只經保留 pins 接入時，可保留原
context 染色，因為每個對照逐 pin 相同。這是具名 equality 的用途。
若 context 接在舊私人點，該點必須先升格為保留 pin；本 theorem 不會自動
保存被遺忘的附件。

## 3. 對十二內點界的確切推論

若 A' 在 B/U 之外有 r 個私人點，則 G' 的內點數是

\[
|U|+r+1=6+r.
\]

因此 `r≤6` 且 W3-TRANSPORT 的幾何、關係前提全成立時，G' 至多十二內點，
並有 `Σ(G')=Σ(G)`。使用凍結來源所列 `K≤12=K≤5=K132`，便可排除該
最小目錄外來源。這是條件推論，代表存在性仍是另一本質義務。

此 proof 不用最小性、933／941、edge-critical 或 N2 身份。
那些來源特有結構只能用來**建立代表或其 W3 等式**，不能由本 transport
theorem 反推出。

## 4. 真正只保 Σ 時的最弱條件，以及它不保留的資料

定義三色 support 的外框投影

\[
P_A^3=\{\beta:\exists\tau\ (\beta,\tau)\in R_A^3\}.
\]

因中心的上述 characterization，有精確等式 `Σ(A+v)=P_A^3`。
因此，若交付只要求兩圖具有同一外框 Σ，最弱且必要充分的關係條件是
`P_A^3=P_A'^3`。這可產生只保 B 的雙向 full-lift 對照；它容許改變 U 色列，
故不符合第 2 節逐 B/U pin 保持的對照。

**具名反控制。** 令 P 為 pentagonal prism annulus：B、U 兩環及五條 `bi ui`。
令 D0 再加五條 `b(i+1) ui`，下標 mod 5。每條新邊位於各自 prism 四邊面，
故兩者有同一合法 annulus 槽位，均無私人點。

`Σ(P+v)=Σ(D0+v)=1023`，但 `R_P^3≠R_D0^3`。例如

```
beta = 01012
tau  = 10103
v    = 2
```

是 P+v 的完整染色；在 D0 中新邊 `b1 u0` 兩端都是 1，該 named cell 為空。
D0+v 對十個 β 皆有一份完整 lift；[`summary.json`](summary.json) 列出十份，
[`certificate.json.gz`](certificate.json.gz) 保存所有 full lifts 和空 cells。
這個反例證明只憑補中心後的外框 bits 不能推出 marked W3 equality。
它不是最小目錄外來源。

更弱的 `Σ(A)=Σ(A')` 連固定 wheel 的 Σ 都不能保證。有限控制沿用已知的
同一具名 prism 與 D1：D1 把 D0 的第一條對角線 `b1 u0` 改成 `b0 u1`。
兩者 `Σ(A)=1023`，補中心後 prism 仍為 1023，D1 為 831；D1 丟失
`01212`、`01213`。本檔直接重算，而非重做已排除的零新頂點正聯集方案。

## 5. Support 與計數的精確分界

在 P 的第一個 annular 四邊面，新增私人點 x，連到原相鄰點 `b0,u0`。
原邊 `b0u0` 保留，x 放在該邊旁的同一面內。得 annulus P+。
每份 P 染色在 b0、u0 的色不同，因此 x 恰有兩個選擇：

\[
R_P=R_{P+},\qquad |J_{P+}(\beta,\tau)|=2|J_P(\beta,\tau)|.
\]

刪除 x 給一個二對一的完整 restriction；反向任選兩個剩餘色之一。
它紙面證明 fibre 計數相等並非 transport 的必要條件，同時給全 fibres
保留時的完整對照。四個控制圖的數據如下。

| annulus | 全 A lifts | 三色 named cells | 全 A+v lifts | Σ(A+v) |
| --- | ---: | ---: | ---: | ---: |
| P | 670 | 340 | 340 | 1023 |
| P+ | 1340 | 340 | 680 | 1023 |
| D0 | 50 | 20 | 20 | 1023 |
| D1 | 47 | 23 | 23 | 831 |

所有計數均遍歷十個既定 β；P+ 的私人點是 10，而中心另外附加在最後。
這是本檔明示的頂點順序，不與舊證書把 v 固定為 10 的順序混用。

## 6. Arbitrary context 與 universal claim 的界線

W3 equality 足以支援所有**仍包含這個五輪中心、且只透過保留 pins 接入**的
其他 context，因所有可用 τ 已被中心限制為三色。它不提供四色 cells 的任何
等式；若拿走中心或換成允許四色 τ 的內部圖，這個 proof 不再適用。

本檔不宣稱已構造一對 plane annuli，恰好 W3 equality 成立而四色 support
不同；也不宣稱各種未加 pins 的合法平面 context 能分辨每一種 formal cell。
上面的確切必要性只針對「存在保持每個 B/U pin 的 total 對照」，沒有把
抽象 relation separation 偷換成 plane gadget realization。

既有「只用原 U、加邊、非交叉識別、零新頂點」普遍正聯集 no-go 不在本輪
重證。本 theorem 既不違反也不繞過該結果：它允許改動整个 annulus，仍必須
另交付一張合法代表及完整的關係證明。

## 7. 重播與證據層次

[`check.py`](check.py) 使用標準 Python，自行建四份 literal annuli 的 oriented
faces、rotation、edge ownership，核對每條 dart 恰出現一次、反 dart 存在及
Euler 等式。其枚舉保存四圖全部 40,960 cells，包括所有空格和 full lifts。
輪心重建另與直接對 G 做 DFS 的完整染色集合逐份相等。

```bash
python3 -B audits/2026-10-13-w5-three-support-19209f4c/t1/check.py
```

預設唯讀重播，與固定壓縮 certificate 及 summary 的 bytes 比較。
`--write` 只允許輸出尚不存在時建立證據，拒絕覆寫。

| 層次 | 結果 |
| --- | --- |
| W3-TRANSPORT 等價、投影 characterization、內點計數 | 紙面 `triggered and holds` |
| 四個 literal synthetic annuli | 40,960 cells 全枚舉，`triggered and holds` |
| 從輪圖外框 Σ 推出 marked W3 equality | `counterexample`：P 與 D0 |
| 從 annulus 外框 Σ 推出輪圖 Σ | `counterexample`：P 與 D1 |
| 實際最小目錄外 933／941 來源 | `not triggered` |
| 任意／條件性 r≤6 代表存在性 | 本子任務未解決 |
| Lean、外部大枚舉與上游 K≤12 定理 | 未新增、未重跑 |

所有普遍結論均由第 2–3 節紙面證明；四圖控制不提升為所有 annuli 的結論。
