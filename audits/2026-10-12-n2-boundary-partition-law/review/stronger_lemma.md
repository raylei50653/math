# 更強 unary 全色出口候選的停止點

2026-10-12；只讀同一 [BASE](../BASE.json)。這份 note 區分 local 反控制與 full disk
source，沒有採納尚未證明的更強定理。

候選「每份 k≤3、三點支援 unary 必有某指定列全部 owner colors 接受」在已有局部
前提下是 **counterexample**。已保存控制 tailtriangle entry34 的原頂點
`7,8,9,10,11`，原 triangle `7–8–9–7`，tail `7–10–11`，owner contacts
`8,9,11`，附件 `7:0,8:2,9:2,10:01,11:12`，有

\[
F_U(q_0)=F_U(q_1)=\{0\},\qquad F_U(q_3)=\{2,3\}.
\]

獨立直接遍歷所有 `4^5` 原 tuple（每列四 owner pins），逐 tuple 與保存 probe 相同。
其 count vectors 為 `q0/q1=(0,8,16,4)`，`q3=(8,4,0,0)`。
例子也否定 `F_U⊆unused(support)`：在 Diff rows，used 色0 forbidden。

**但此例不能反駁 full disk source 的更強候選。** 把三个 contacts 接同一實際 owner
5 後，以下五 bags 是原 K5 minor：

\[
\{8\},\quad\{9\},\quad\{7\},\quad\{5,10,11\},\quad B.
\]

前三袋由原 triangle 兩兩相鄰。第四袋沿 `5–11–10` 連通，經 owner contacts 接
8、9，經 `10–7` 接7。原 B 連通，經原附件接前三袋及第四袋。各袋互斥，十對
鄰接全存在；已按原邊直接核回 bags 連通及十對鄰接。
這個 minor 其實適用任何同 owner 的原 tailtriangle 型：triangle 每點按 degree 四
都有一條框附件，tail 外部 hub接三個 triangle點且碰 B。

因此此例的正確界線是 local 反控制，並非 full disk／Σ-critical 原來源反例。
完整來源更強的全色出口候選未在本 note 證成或否定；當輪已採納的是
U-USED-ONE＋source容量得到 `k_U=2`，並由共同橋接規律排七模板。
不得從少量 exemplars 全符合、或十個 local 控制非平面，推稱來源全面 closure。
