# 獨立短審：固定 K6 完整關係與18份換補控制

2026-10-23；審查 [integration PROOF §§2–3](../2026-10-23-941-types-wrong-side-6b09cd4/PROOF.md)
與 [check_cap_relation.py](../2026-10-23-941-types-wrong-side-6b09cd4/check_cap_relation.py)，
正式證書為 CAP_RELATION-v2.json。結論：**此固定圖／填片域的有限結論可採**。
未發現 relation 方向、字面框正規化或換補安全性界線的錯誤。

- 六圈 proper words 對同一全域 S4 作 restricted-growth 正規化，31列覆蓋
  全部字面色框軌道；內點 lifts 仍逐原頂點保留四色，未再個別正規化。
  checker 先窮盡所有4⁷內點賦色再過濾內邊與接框邊，264個內邊合法賦色
  沒有漏失。原 cap 的框內無額外弦，而六框 proper 條件已核全部框邊。
  逐 fibre 和完整 tuple 比對證書，確得兩核心各19非空／12空／52 lifts。
  L/R 宣稱的是同一有序框的**支援相等**；未錯升為全 inner-tuple relation
  或原 B14／C5 完整 Σ 相等。
- 六邊形有9條可能弦；三條互不交叉弦正好重建14個三角化。只有偶／奇
  中央三角形兩份滿足 `R_new⊆R_old`。此方向正是無條件 backfill 所需的
  邊界可延拓包含。每個空三角化均至少加入一條同色端點弦，故原交替二色
  框全被拒絕；兩份包含安全者也無法沿用這個 frozen witness。
- W6 的可延拓條件確是六框最多用三色；兩個 W4 的條件是原直徑兩端異色，
  且每個四框最多用三色。兩個中心之間沒有額外邊或其他共用內點，所以
  checker 以兩個條件的同框交集計算正確。所得 W6 三列洩漏、三份雙 W4
  各四列洩漏，皆否定這些填片的**無條件**完整 backfill 包含。
- 紙證沒有據此排除另外的填片或來源，也保留同一外側相容限制下的替換。
  特別「丟失原交替 witness」不等於證明改填片後所有 accepted witnesses
  都空；新的 accepted witness 能否與同一外側接合仍需另證。此精確停止
  點與正文最後義務一致，沒有從18份固定失敗推一般較小 bad 不存在。
- 新定稿 v2 凍結含有向原面的 cap 輸入；checker 先核 frozen SHA 及 live
  同一檔字節。v1 因新增面欄造成 hash fail 的歷史證書與失敗記錄仍留存，
  未把失敗改成成功或覆寫舊證書。

我實際重播正式 checker 的 normal、seed17 及 negative，皆 PASS；四項破損
（刪空 fibre、刪完整 lift、換框序、改 input hash）均拒絕。這次短審沒有
拓展填片搜尋，也沒有重稽核上游完整來源鏈。K6 cap 的原有界側與 full-star
覆蓋另見 [empty-M2 交叉審查](REVIEW_EMPTY_M2.md)。完整來源仍
`not triggered`，替換與嚴格較小 bad 尚未建立。
