# 五度輪的跨原邊 Kempe 缺陷搬運

2026-10-13。接續 [共面正規形](c5_cofacial_normal_form.md)、
[完整外圈](c5_neartri_boundary_collar.md) 及 [全內部五輪](c5_degree5_link_reductions.md)。
完整合同、證明及有限控制見
[隔離報告](../audits/2026-10-13-cross-edge-kempe-19209f4c/REPORT.md)；
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。

本輪證明五度中心的不同原邊 J_e 之間有保留完整外部染色的精確雙射，
並得到相鄰五度中心的共同缺陷搬運及全域計數恆等式。
**933／941 的一般排除與 K∞=K≤5 仍 OPEN。**

## 1. 逐邊存在式與可共用的資料

沿用同一原圖 G、固定原外框 B、同一色集及全部十列四格
J_e(p;[s≠t],[u≠v])。既有最小來源引理是：若 e 的 opposite pair 至少一端
在內部，且 J_e(01232;1,0) 非空，則某個原拒絕列 p 有 J_e(p;0,0) 完整 lift。
固定同一接受列染色可同時觸發多條邊，但結論仍是 ∀e∃p_e∃f_e。
它不聲稱 Kempe 交換把原接受列染色送到這些拒絕列染色。

不同原邊 e≠d 的單邊缺陷完整 lifts 必不相同：一份使 e 單色，另一份在保留的
原邊 e 上必 proper。因此共同資料必須透過明確限制或搬運取得。

## 2. 五條 spokes 的完整雙射

令 v 為五度內點，原循環鄰點 U=(u0,…,u4)，五個 vu_i u_(i+1) 為實際三角面；
H=G-v，e_i=vu_i。
下標模五。對每一列 p 定義完整 H fibres：

- A_i：U 用四色，唯一重色對是 u_(i−1)=u_(i+1)。
- T_i：U 用三色，唯一 singleton 位於 u_i。

十份 fibres 兩兩不交且覆蓋 H 的全部完整 p-lifts。令 ρ_v 刪去中心值，則

\[
\begin{aligned}
\rho_v J_{e_i}(p;0,0)&=A_i,\\
\rho_v J_{e_i}(p;0,1)&=A_{i+2}\dot\cup A_{i+3}\dot\cup T_i,\\
\rho_v J_{e_i}(p;1,0)&=T_{i+2}\dot\cup T_{i+3},\\
\rho_v J_{e_i}(p;1,1)&=T_{i-1}\dot\cup T_i\dot\cup T_{i+1}.
\end{aligned}
\]

每式都是完整 lifts 的雙射：缺陷中心取 u_i 色，proper 中心取 U 的唯一缺色。
證明只用 proper C5 的重數型 (2,1,1,1)／(2,2,1)，不需最小性或 4CT。

若 p 被 G 拒絕，T_i 全空。每份 J_ei(p;0,0) 完整 lift 因而唯一配出其他兩條
spokes 的 J_e(i+2)(p;0,1)、J_e(i+3)(p;0,1) lifts；三份只改中心顏色。
這是真正同一外部染色的跨邊約束，並非各自非空的 marginals。

寫 N_i^{ab}=|J_ei(p;a,b)|，得到

\[
|T_i|=N_i^{01}-N_{i+2}^{00}-N_{i+3}^{00}\ge0,
\qquad |\mathcal C_G(p)|=\sum_iN_i^{01}-2\sum_iN_i^{00}.
\]

若相鄰五度中心 v,w 共用原邊 e，拒絕列上的 J_e(p;0,1) 同時是兩端各兩份
00 fibres 的不交聯集之雙射像。經**同一**中間 lift 合成，得到只可能改動 v,w
的跨中心雙射。相鄰五度中心的存在本輪未證。
令 m5(e) 為原邊的五度內點端數，只對接觸五度內點的原邊求和，則全圖另有

\[
\sum_e m5(e)(N_e^{01}-2N_e^{00})=n_5|\mathcal C_G(p)|.
\]

## 3. 同一 lift 的路徑限制與條件排除

在 A_i 的同一完整 H lift 中，rim 色依序為 (a,b,c,d,b)，四個色互異。
對 rim 次序中不相鄰的 singleton pairs (u_i,u_(i+2))、(u_i,u_(i+3))，若 p 被 G 拒絕，
每對必在同一二色分量，或其兩個不同分量都碰到原 B。
否則交換不碰 B 的那個分量，把 U 降為三色，再補中心便得到被拒絕的 p 延伸。

此條件是「一次保持原框不變的單分量 Kempe 交換後補中心」的精確充要 escape
判準。若能在最小 933／941 來源的任一強制 witness 中迫出一次 escape，便可
排除該來源；目前兩者均至少九個五度點及全內部 W5 尚未供應這個缺失前提。
若相關色對在 B 至多出現一個頂點，拒絕進一步強制真正的端點間二色路徑。

使用固定 BASE 已有的九／八下界，就能同步一個拒絕列到至少三個五度中心及三條不同原邊：
固定同一 01232 lift 的 2n5 個觸發 incidence，再按四／三個拒絕列作鴿籠計數。
三個中心各供應至少三條 p 缺陷 spokes，扣掉至多三條重複原邊，
更迫同一 p 至少有六條不同原邊的單邊缺陷（00 或 01）；仍不識別那些完整染色。
並行的[外圈後續](c5_neartri_boundary_collar.md)提高度數界，不影響本輪以較弱前提的推導。

## 4. 反控制、重播與信任邊界

完整有限控制、正常／seed17 重播及破損證書檢查見
[驗證紀錄](../audits/2026-10-13-cross-edge-kempe-19209f4c/VERIFICATION.md)。
具名 near-triangulation `triangulated_03` 有全內部 induced W5；同一拒絕列
01212 在四條 spokes 各有 00 witness，但四份 H 限制兩兩不同。
這完整反駁「同列的多份 00 witnesses 可視為同一 H lift」的廣義命題。
該圖不是 933／941 最小來源。

```bash
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/controls/check_cross_edge.py --check
python3 -B audits/2026-10-13-cross-edge-kempe-19209f4c/review/catalogue_check.py
```

紙面雙射及單步引理為一般定理；有限控制只驗證明列圖域。
最小來源適用性沿用上游紙面／目錄／外部依賴，實際 target 為 `not triggered`。
沒有新增 Lean theorem。一般多步 Kempe 軌道 escape、來源排除及普遍同步仍 OPEN。
