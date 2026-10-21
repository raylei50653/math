# Profile 0／1：原完整第二層的幾何接續

BASE `13e51db3ec3d8d7ec7eeef60167afdc19ad956c4`；[紙證](PROOF.md)。

**仍未排除剩餘兩型。** 本項在同一原 W7 證明新必要結構：第二層
`W=N_G(C7)\(C7∪{R})` 恰是一個 induced 原簡單圈 S，全部原 H 點
彼此不同，且每個 H 點在任何著色前已恰有一個 C7 接點。

Profile 0 的完整有序 S 為
`(p,a,reverse(H_n),z1,H1,z2,H2,z3,H3,z4,H4,z5,H_L,q)`，長度8+K，
有界側恰 C7 與 R 共八原內點。它是保留全部更外附件的真完整接合界面。
原 a–q 外側 link 因而是 induced 簡單路；既有反向12色障礙 y 必在同一份
完整 `K12(P)` 中，給 K≥1、|S|≥9。

Profile 1 的 z1=a，界面為 `(p,a,H1,z2,H2,z3,H3,z4,H4,z5,H_L,q)`，
長度7+K，同樣恰八原內點；其反色障礙給 K≥1、|S|≥8。

並給出完整 S fibre 的精確七列表公式：固定同一 σ，原 C7 每點只可用其
所有 S 鄰點未用的色，且共同避開原 R 色、沿 C7 相鄰異色。全部 lifts
逐份對應504個未受列表限制的內輪候選，包含空 fibre，適用任意 H 長度。

尚缺排除一般 K≥1 來源的矛盾，或具名合法較小 patch 的完整 S 支援相等
證明。沒有構造替代圖、聲稱完整941來源實現、跑 LP 或新增 Lean。

[checker](check.py)核對凍結輸入、全部十四種 C7 接觸的所有不交點對，
及兩型49個局部符號 collar 的面拼接；任意大小原來源的 topology 由紙證承擔。
另在兩型 K=0 collar 全部365個 proper S 色置換類，獨立回溯核對公式的
完整 lift 數；局部控制不觸發完整941來源前提。
normal 與 seed17 加 `-O` 重播相同，兩份 marginal 接合負控保留；見 [runs](runs/normal.log)。
