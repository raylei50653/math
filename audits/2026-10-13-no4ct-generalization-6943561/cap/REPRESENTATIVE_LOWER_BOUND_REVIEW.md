# C_(4t) 五點代表限制：獨立紙面覆核

2026-10-13。覆核 scope_review 提出的 family；本文件只檢查其幾何及
完整 boundary relation 的 counting 下界，不以有限搜尋代替證明。

令 t≥1，具名外框按 `(a_i,b_i,c_i,d_i)`、`i=1,...,t` 排列成 C_(4t)。
每段加弦 `d_i a_i`，在所切下的四點 face 內加私人 hub h_i 並接四點。
t=1 時 `d_1a_1` 已是原外框邊；t≥2 時各段弦 noncrossing，所切下的
四點 faces 互不相交。因此此圖是合法 C_(4t) disk，有 t 個內點。

固定 literal 色框 0,1,2,3。每段可選

\[
P=(0,2,0,1),\qquad Q=(0,1,3,1).
\]

各 P 段令 hub=3，各 Q 段令 hub=2，便得全部 `2^t` 個 rows 的完整延伸。
段間外框邊的色值恒為 1–0。相反，只要某段變成 `(0,2,3,1)`，
其 hub 同時看到四色，該完整 boundary row 就不能延伸。

令 R 是任意保留全部具名 boundary relation 的代表，內點數為 m；
它可以有原 family 沒有的 boundary chords，甚至不要求平面。
每個接受 row 各選一份完整內點 assignment。若 `2^t>4^m`，
兩個不同接受 rows u,v 會共用同一內點 assignment z。
取它們不同的一段；其中一列給 b_i=2，另一列給 c_i=3。
保留 a_i=0、d_i=1，把這兩個值一起放進混合 row w，其餘座標任取
u 或 v 的對應值。

**額外 boundary chords 不會破壞這次混合。** 在全部接受 family 中，各點
可用值的 domains 是

\[
A_i=\{0\},\quad B_i=\{1,2\},\quad
C_i=\{0,3\},\quad D_i=\{1\}.
\]

R 的每條 boundary–boundary edge 兩端 domains 必不相交：
若兩端在不同段，各段 choice 獨立，任何共同色都能在同一接受 row 出現；
若兩端在同段，兩個變動點 b_i,c_i 的 domains 已不交，
其餘情況至少一端固定，共同色也在某接受 row 同時出現。
兩種情形都與該 row 在 R 可延伸矛盾。
所以**任何**逐座標 domains 混合仍符合 R 全部 boundary edges。

對 boundary–internal edge，混合端點的色值來自 u 或 v，兩列均與 z
相容，所以仍 proper。internal–internal edges 由同一 z 保證 proper。
故 `(w,z)` 是 R 的完整染色；但原 family 在指定段為 `(0,2,3,1)`，
不能延伸，矛盾。結論是每個內點 assignment 至多支持一個接受 row，故

\[
\boxed{4^m\ge2^t,\qquad m\ge\lceil t/2\rceil.}
\]

t=11 的 C44 disk 已迫任何保完整具名 boundary relation 的代表至少六內點。
因此「任意邊界長度都有至多五內點代表」是假的，且所需代表大小隨邊界
長度無界。這不反駁 cap 的相對最小性 hitting 定理，也不回答固定 C8
是否有統一五內點代表。推導不需要四色定理或任何來源不可染假設。
