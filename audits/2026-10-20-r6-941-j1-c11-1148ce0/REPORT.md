# J1 原 W5 三邊路：induced C11 殘支完成排除

2026-10-20；**`d_G(n)≥6` 的具名 induced C11 殘支已排除。**
完整計數的 132 條帶符號等式給

\[
16\bigl(Z_{5093}+Z_{5100}\bigr)=0,
\]

原實際三邊路則給 `Z_5093+Z_5100≥1`，矛盾。所有 n 的額外私有
鄰點與附件均留在同一 F'；不需要刪 n、限制外側大小或另構造較小 bad。
結合前輪 n=5 排除，**J1 原 W5 三邊路整個子支關閉**。一般 J1/J2
最後拒絕、一般同候選較小 bad 與主命題仍 OPEN；沒有新增 Lean 定理。

BASE `1148ce026aaf764e6e2766aebc096eebe193ed13`，初始 tracked worktree
乾淨；證據工作前逐 bytes 凍結 1,240 份輸入，見 [BASE](BASE.md)、
[INPUTS](INPUTS.json) 與[完整來源契約](SOURCE_CONTRACT.md)。
本輪沒有 commit 或 push。

## 1. 精確量詞與同一實際正 fibre

承接[凍結前輪原 W5 報告](frozen/audits/2026-10-20-r6-941-j1-w5-9c36e3c/REPORT.md)
的全部來源前提：原 G 為任意大小簡單 plane C5 disk，原框
`(x,y,a,b,c)`，支持941、全域最小內點數 k 再最大邊數；
原 r 六度，原 p,h,R 完整五度，`N01232(Q1)=0`，原 rotation、
所有私有點、附件與短圈定理。固定 J1 殘餘完整著色中的實際
12 色三邊路 `n–u2–u1–L`。

原七框內部恰 p,h,R，十一個原面與 R 的完整 star 已被前輪確定。
在本輪的 `d_G(n)≥6` 子型，

```
F'=G−{b,p,h,R,x,y,r},
rim(F')=(a,n,u2,u1,L,q,c,s,v,w,t)
```

是實際 induced C11 三角化 disk。n 沒有被刪除；其
`d_G(n)−5≥1` 個額外鄰點及任意大小的其餘原私有圖全部保留。

令 Z_i 為同一 F' 在第 i 個固定正規 rim 色列上的**全部完整著色數**。
實際所選著色限制後恰落在

```
ID 5093: (0,1,2,1,2,3,1,2,0,1,2),
ID 5100: (0,1,2,1,2,3,1,2,1,0,2).
```

所以兩項和正；不要求兩項各自正，也沒有把未刪的必要格當作來源見證。
對其他著色重新量化 u1,u2,R 的色，所有原左／右 cap 都以同一核心
完整著色作 Cartesian product，包含空 fibres。

任意大小來源到有限計數系統的紙面證明見
[同源全稱證明](geometry/PROOF.md)及[獨立 orbit 引理](reduction/ORBIT_LEMMA.md)。

## 2. 從完整交換重數到 132 條守恆等式

全部 proper C11 色軌道有 7,381 格。沿用並重新重播前輪 cap 零值、
完整 R 接回及分量交換所得的 1,430 個零 fibres；其餘 5,951 格只是
已證可能集，不宣稱每格非空。

固定 palette split `{0,1}|{2,3}`，將同一 F' 的全部完整著色依實際
完整分量交換分成 orbits。每個不接框分量的交換都保留，對其邊界
orbit 加入相應 `2^q` 重數。三角化的原面分界 arcs 給出完整接框
分割的必要條件，因而存在同一非負整數向量 β，使

```
A Z = B β.
```

這裡 A 有 22,143 個 half-rows，每列係數是 `8 Z_i`；B 有 36,487 個
完整交換 columns，逐份保留字面重數。兩套不同生成器重建同一完整 family。

一個 B column 只要接觸已證零 fibre 所屬的 half-row，其 β 權重便由
非負性強迫為零。這恰排去 15,693 個 columns，剩 20,794 個。
對剩餘等式，取[完整字面證書](counting/balance-certificate.json)列出的
132 個 half-rows：64 個乘 +1，68 個乘 −1。精確逐項核對得到

```
λ A = −16(e_5093+e_5100),
λ B_j = 0        對全部 20,794 個剩餘 columns。
```

故 `−16(Z_5093+Z_5100)=0`。與 §1 的實際正 fibre 矛盾，
排除此具名原來源。這是同一來源的完整計數守恆，沒有混合不同候選、
不同著色的私有顏色或邊際支援。

另保留[全欄整數證書](geometry/orbit-farkas-certificate.json)：
向 4,290 個已證零 half-rows 各加乘數8，得到等價的

```
16(Z_5093+Z_5100) + Σ_j s_j β_j = 0,    s_j,β_j≥0。
```

它有 15,693 個非零 slack，全部對應上述已強迫為零的 columns，
沒有核心 Z slack。兩種形式獨立重播一致。

**最後證明不使用 signed planar span、任何數值求解器或新的來源正性假設。**
探索階段的數值 infeasible、逾時、求解錯誤及未通過精確化的對偶結果
保留為探索紀錄，均不是此定理的依據。最終 +1/−1 等式由 stdlib
整數 checker 與獨立生成器完全核對。

## 3. 收尾範圍與直接父題

前輪已排除原 n=5；本輪排除所有 n≥6，兩者涵蓋此具名原 W5
三邊路的全部度數型。因此 J1 type III 的同一殘餘完整著色中，
每條實際12色 n–L簡單路皆至少五邊；原「三邊路 W5 例外」不再保留。

未排除 type III 的長路，也未排除 type I。J1 的兩個一般殘餘 fibres、
J2 六項最後拒絕、H4、一般較小 bad 存在性、聯合偶補正值及主命題
均不由本輪完成。

Closure scope：上述任意大小、全部原附件保留的 J1 原 W5 三邊路子支。
Canonical source：本文、[全稱證明](geometry/PROOF.md)、
[132-row checker](counting/balance.py)與[獨立整數核對](review/dual_check.py)。
Updated：Kempe 導覽的原 W5 停止點、直接父題長路義務及 STATUS 索引。
Reviewed-unchanged：舊兩份 REPORT 與 geometry 證據已列入原 OUTPUTS seal，
保留其歷史 bytes；後續狀態由現行導覽及本文銜接。README、HANDOFF 與
跨線主命題未改，因研究線、活躍標記及主命題狀態均未變。
Propagation stop：L2，父題仍 OPEN。

## 4. 重播與證據層

全套唯讀入口：

```
python3 -B audits/2026-10-20-r6-941-j1-c11-1148ce0/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-20-r6-941-j1-c11-1148ce0/check.py
```

最小主證書重播：

```
python3 -B audits/2026-10-20-r6-941-j1-c11-1148ce0/counting/balance.py
```

正常／seed17、竄改負控制、輸入與證據 seal、文件檢查及 build 的實際結果
見 [驗證紀錄](checks.json)。紙面來源語義、有限精確整數證書及 Lean
分開：本輪無新 Lean，`lake build` 不代表本輪拓撲或計數引理已形式化。

有限替換探索與 n=6 展開只作方法紀錄，分別見
[替換範圍](reduction/PROOF.md)、[n=6 探索](geometry/N6_AUXILIARY.md)；
它們的零命中或存活格不承擔本輪來源排除。
目前接續入口見 [Kempe 導覽](../../docs/c5_kempe_guide.md)。
