# 完全二分圖交叉數導覽

## 研究概況與閱讀入口

Zarankiewicz 公式給出完全二分圖的標準畫法交叉數。
這條研究線詢問能否用與完整外側相容的局部重畫，配合低交叉候選的不可避免性，另建下界論證。
[局部重畫報告](../../archive/reports/crossing/zarankiewicz_local_redrawing.md)從整星複製的實際交叉帳目出發，
說明雙星與三星改善條件、奇數最小反例的缺額限制，以及計數鬆弛為何還缺實際畫法。
[旋轉與超額接續](../../archive/reports/crossing/zarankiewicz_rotation_excess.md)將旋轉距離轉為可用交叉超額，
用共同標籤的相容性迫出額外成本；一份完整整數計數候選雖通過全部所列奇偶及重畫條件，
仍被小型旋轉阻礙排除，具體說明計數與畫法之間尚有來源條件。

文獻的兩交叉 K₃,₄ 本身已最優，使用它必須加入足夠的外側條件。
本路線的不可避免性尚未證明；新近完整證明及形式化的外部紀錄，與本地證據分開列於報告。
接續問題是以同一份平面化畫法的旋轉和交叉順序，迫出有完整外側證書的改善。
接手先依[工作次序與驗收](#接續工作與驗收)將完整循環排列條件接回共同張量，再檢查必要超額是否超過低交叉預算；
[精確停止點與重播](../../archive/reports/crossing/zarankiewicz_rotation_excess.md#重播精確停止點與接續)保留當輪完整證據；
目前採納結論與 OPEN 查[活躍結論](../CONCLUSIONS.md#獨立的完全二分圖交叉數研究)，本頁維護接續工作。

## 接續工作與驗收

2026-10-30 整理，沿用[來源報告的下一個窄問題](../../archive/reports/crossing/zarankiewicz_rotation_excess.md#重播精確停止點與接續)。
依序增加必要條件，每層都保留同一份候選來源及完整標籤。

1. **共同張量與兩側旋轉。** 把 TL 的完整循環排列條件接回整數張量，
   同時保存兩側全部旋轉與標籤對應。先重播既存 `C=79` 張量的旋轉排除及正控制，
   再辨識仍存活的共同候選；固定張量被拒不當作所有張量均被拒。
2. **超額與覆蓋。** 對每份共同候選核 EB／ER／EP，使用該候選實際迫出的
   non-pseudo-tight 四點族計算整數覆蓋成本，與同一低交叉預算比較。
   抽象四點族控制只有在證明由共同來源迫出後，才可用作一般下界。
3. **完整畫法。** 預算仍可行者才補原交叉邊匹配、每條原邊的交叉順序與完整平面化，
   由既存 checker 核兩側及外側相容性。每份重畫改善都須有同一外側的完整證書。

驗收可為一份新的共同來源排除及其完整證書，或更一般的可證必要超額界。
要收尾完整下界，仍須覆蓋全部目標低交叉畫法；有限放鬆通過、搜尋無命中或單一候選被拒均不足。
外部完整證明及形式化沿原報告分列，不提升本地證據範圍。

## 查證與重播

- [完整前提與紙面推導](../../archive/reports/crossing/zarankiewicz_local_redrawing.md#畫法與外側契約)
- [整星複製與雙星條件](../../archive/reports/crossing/zarankiewicz_local_redrawing.md#完整雙星重畫)
- [同時替換多星](../../archive/reports/crossing/zarankiewicz_local_redrawing.md#同時替換多星與三星條件)
- [最小反例及偶數缺額](../../archive/reports/crossing/zarankiewicz_local_redrawing.md#最小反例的奇偶與缺額)
- [分數控制與來源缺口](../../archive/reports/crossing/zarankiewicz_local_redrawing.md#計數鬆弛還缺實際畫法)
- [外部形式化範圍](../../archive/reports/crossing/zarankiewicz_local_redrawing.md#外部完整證明與形式化)
- [精確算術腳本](../../../scripts/zarankiewicz_redraw_bounds.py)
- [超額預算與非 pseudo-tight 覆蓋](../../archive/reports/crossing/zarankiewicz_rotation_excess.md#從非-pseudo-tight-子集到整數覆蓋)
- [共同整數殘餘與旋轉排除](../../archive/reports/crossing/zarankiewicz_rotation_excess.md#完整整數計數殘餘及其旋轉排除)
- [完整來源平面化驗證](../../archive/reports/crossing/zarankiewicz_rotation_excess.md#完整交叉來源的平面化驗證)
