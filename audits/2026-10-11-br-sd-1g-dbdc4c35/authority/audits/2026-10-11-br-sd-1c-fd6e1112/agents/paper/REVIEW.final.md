# BR-SD-1c：最終 PROOF 的獨立驗收

日期：2026-10-11。Reviewer：paper worker。研究 BASE：`fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`。
最終審查輸入：父端 `PROOF.md`，SHA256
`e3f88f1a01c12b6c428b829e215ee33d59185fa7dbd57f3c56548277867d23d5`。
原先審查輸入完整保存在 `PROOF.reviewed-v1.md`，其 SHA256 仍恰為
`649ad89d0f05de602ee29c13a2aba02eb1f2d72ec0edd4672b802e3d81288a25`。
原 REVIEW.md 不覆寫。

判定：**接受最終精確 one-W 任意大小來源排除與明列前提的可重用局部引理。**
沒有阻止其交付的紙面缺口。Canonical 採納仍由 owner 另行裁決。

## 修正核對

重讀最終全文，並與已審版本逐行 diff。只有以下兩處精確補充：

1. §3，74–75：effective-H 若省略原孤立自由內點，按同一原 M 的自由 Col 因子
   填回其完整 full-lift 坐標。這保存原全圖 assignment，不影響 degree-list 或任何 palette 推論。
   該補充只指原孤立**自由**點，不把有實際邊的點當成任意可填的因子。
2. §6，129–133：原 q 臂的每條邊明列為 C bridge；a 以外每個臂點只能有該臂的
   C 鄰居，正長時 terminal q 的 dC=1、內部臂點 dC=2。這完整修補原 REVIEW.md
   唯一的局部引理前提精度 finding。

因此最終§6的零／一邊／長臂三類，每個 degree 與 list 等式都由明列前提供給。
J3 私有點實際 list {T,D} 的推導仍取自完整原 degree4 與 actual S edge-pair support；
不是合成 list 反推 disk 實現。a3=v、任意奇環長及任意 q 臂長均包含。

## 主結論與證據界線

最終結论只指 `N45-S-NOU-LS-PAIR` split22 原共 r／三環／uv／p-q 臂骨架，
多一份實際 pendant W 接在 J1 或 J2，完整保原來源 degree、contacts、附件、β、ownership、
rotation、Σ witnesses 與完整 relations／fibres／full lifts 的候選來源家族。
r 接 W 由完整度數排除；其餘位置由 degree-list 拒絕及 untouched actual pair-supported
J3/q 臂矛盾排除。W 的任意有限大小不被 finite controls 承擔。

可重用局部引理亦接受，但它的实际附件 pair、原 odd-cycle 私有點、唯一 s-contact、
原 simple bridge 臂、末端度數與不額外接入條件必須逐項核回來源。
§7 的 abstract routing counterexample 只反駁錯誤 D 傳遞推論；撤 actual pair，未提供
disk embedding／完整 Σ，故不構成本 scoped source theorem 的反例。

本次接受沒有確認 actual target source 存在、一般 Gallai trees、一般 N45、R31、55、
ε≥3、主命題或 Lean。Formal 依賴仍為先前已重讀的 Dvořák Theorem 10／blockwise uniform；
原 SOURCE 的 frozen hash 與 paper evidence 層不變。
父端 REPORT 尚未交付，本次精確驗收只綁定上述 PROOF bytes，不稱已審 REPORT。

本 worker 只新增本目錄 REVIEW.final.md，原審查／舊封存／canonical source 不修改。
