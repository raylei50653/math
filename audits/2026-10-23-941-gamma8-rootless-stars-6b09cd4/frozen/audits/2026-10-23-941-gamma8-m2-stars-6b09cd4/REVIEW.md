# 量詞、原星與分離集：本輪自審

2026-10-23；本輪未使用 sub-agents；此檔是主作者的證明自審，沒有宣稱
另有獨立 reviewer。producer／checker 使用不同固定域重建與連通演算法。

對[PROOF](PROOF.md)逐項核對：

- T 五度是新增前提，不把結論用到 T≥6、j≥3 或較長 Γ。T 私有且完整
  原星在 F，因此外側 link 恰有兩點，且次序與 rTa、TsΓb 原面相符。
- 原 C≠E 是同一 ψ12 的完整分量分離；M2 鄰 sΓ 必在 E，鄰 r 必在 C。
  只用此判斷新取 link 點的避開性，未假設 M2 僅有 T 的鄰點。
- 外側四面點可重複的兩種情形分開處理；L／B 的 u=a、R／A 的 b=c₀
  均另取真正不同的第四點。O 的 u,c₀ 四種色別均有第五點，非套對稱。
- sΓ 間隙點：b,c₀原色均2所以必有中間點；所有 sΓ 鄰點私有；r,sΓ
  禁圈外共鄰排 u,a；ψ12 原邊排該點落 M2∩C。
- r 間隙點：r 唯一可能非私有鄰點為 U。只插 U 仍不能接 M2 點 a，
  故另有私有點；若該點在 M2，原邊把它放在 C。保留 U 的框例外。
- x／d 接續點：N3 與 B1 不可鄰；原面迫 N1 或 K2，從而私有且不在 M2。
  d=U 時由 u 私有保完整原星，未假定 U 的 F link 是完整 cyclic link。
- w 嚴格圈外：均沿 Γ 外側角選取；Γ 完整誘導圖及內耳側別禁止另一
  Γ 點佔該外側位置。無外耳的 j=2 假設在此保留。
- 完整分離集非空：h=c 對 C 無額外前提；另一方向必需穩定 C 框點及
  E 碰框。E rootless 時不推另一個分離點，不把 {v} 當完整 cut。
- 保護點與整個所需 M2∩C／E 不交，故另取 v 可加一；沒有把本已在
  四面點或第五點中的 m 再計一次。
- 完整前輪證書逐字保留；104列只代表已知面的必要限制。沒有宣稱外側
  其他原星已完成，也未把分支索引／局部分量 PASS 當來源實現。

Propagation：

- Updated：[Kempe導覽](../../docs/c5_kempe_guide.md)頁首、近期里程碑與
  Γ8停止點；[STATUS](../../docs/STATUS.md)增加短索引。條件外側界及下一
  窄義務有實質收緊。
- Reviewed-unchanged：前輪 reports／proofs／完整證書與所有輸出保留；
  外耳2／4／6、一般外側4／5、端點464列、ζ五度兩側及11整型均不改。
  HANDOFF、共通語言、932／933、W7 38／40、J1／J2及共同 k≥23不變。
- Remaining OPEN：T 五度且 m 在所需分離側的完整接合、T≥6、完整外側
  disk、更多內點、較長 Γ、一般 wrong-side、完整來源及較小bad。
- Propagation stop：L1。條件義務加強未關閉父來源題，不升級跨線摘要。

實際重播與反控制見[VERIFICATION](VERIFICATION.json)，正式文件及 scoped
DocGraph 見[DOC_CHECKS](DOC_CHECKS.json)。全樹 DocGraph 未重跑，不宣稱全樹 PASS。
