# 獨立交叉審：六外點 u-link 的完整 U／K2 接口

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
只審[最終 u-link 紙證](../2026-10-23-941-gamma8-u-link-6b09cd4/PROOF.md)
第2、4、5節及其60份必要原星列，不改該目錄。
[REVIEW_U_LINK_INPUTS](REVIEW_U_LINK_INPUTS.json) 凍結所審 PROOF/check/certificate
的逐字 snapshot、SHA256及獨立唯讀重播；正常 checker 通過，L16／R32／O12，
6份完整 B13 樹，8份直接 authority 零漂移。

未發現最終稿在這個具名域內的新增缺口：

- n,v,r,sΓ 均私有且原13在同一 rootless N；完整星包絡只保 U 框例外。
  完整 m/T/u link 同時封滿；checker 逐點加面後再次核全部已滿星的原邊、
  非連續禁弦與共鄰限制，未將獨立星拼成一列。R 的 nx 選擇同時改 n、sΓ
  兩份 link，L/O 沿圈內共同鄰點排該邊，故60列保同一原圖與原 rotation。
- p_d,p_x 的原0鄰點確為 d/U、x/U；M 的0點不可接 K，其他框0點由完整
  K 的唯一框接點 U 排除。所有 N 鄰點已由同列完整原星封滿。
- 原框仍有兩個非 B 的 rooted13分量，不能只用私有點窮盡略掉。初稿缺少
  明文引用；最終第4節已明引原 U,V,anchor,Y 交錯給的完整 K 對兩分量
  反相交禁鄰，第5節亦保該條。故剩餘鄰點確只能在同一完整 B 樹。
- p 出口完整 link 的其餘弧必為非空簡單 B13 路；U、d/x同原0，不能空弧
  直接相接。最低度與同 link 禁弦條件保留；文稿沒有稱兩出口可獨立取路。
- U 只用原 F 側 V→Y link；其原2鄰點只有兩個出口。已封滿 N 弧與兩出口
  之間不容另插原13分量；其餘弧由同一 K 反相交禁鄰及私有點窮盡落在 B。
  ψ12 排 Uh/Uc，原03 gate 排 Uq；故 B 鄰點只可 V,Y,W*,e。
  完整 B 的 YW* 非邊使 Y 臂只有 Y，V 臂正好 V、V-W*、V-W*-e，
  e=V 時刪第三臂。保兩出口順序，不把 Γ 的 orientation 擅自對應到 B14。

6份 B 樹及60列原星未共同解出兩出口 B-path fibres；完整原框 stars、
外側 disk 與實際來源仍 `not triggered`。本審查支持已寫出的必要接口，
不提供11型排除、一般 wrong-side、較小 bad、Lean 或 matching 證明。
