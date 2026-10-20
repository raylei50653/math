# 獨立審查與採納邊界

固定 BASE `13dc5ff163045c85b5c82dde438eb5f275dab999`；三組只在各自
獨立子目錄工作，原證據未改。root 綜合原契約與紙面證明後採納下列範圍。

* **原 c 四度／四弦分支排除：採納。** A 證明三角化互補色對分量引理，
  完整重建10798個必要交換欄及每輪空格。C 不匯入 A/model，以兩側
  cyclic side-run 的集合分割另行生成全部 family；全部 columns SHA、
  每輪每格 witness 與原 alpha 空係數逐項一致。
* **q>=6、core 度數、短圈 pocket：採納。** B 回到原雙低 p,q 定理，
  核對原 h=ell 身份及最小性。C 以獨立 Catalan 遞迴核對35條 chord、
  全部空填片與 W5 例外，並人工核實 bounded side 與所有 core incident
  邊確實在 pocket。與 A 合成後得到 c>=5、D10 induced。
* **兩個新計數恆等式：採納。** A 在完整44維必要空間的 basis 上精確
  檢查；C 另用獨立完整 cap 投影、C8交換 family 及有理 constraint
  row-span 消去核對，沒有重用 A 的 nullspace basis。
* **完整回填及風險負控制：採納於明列範圍。** C 獨立枚舉完整字面
  core／cap 與120份商圖局部介面，保存 Q2 a=q 分支、空 fibres、重數，
  並檢查跨候選、跨著色、來源正值及完成成本的錯誤控制。
* **較小圖比較：採納合法性與必要投影。** B/C 核對左右共面洞、原框及
  全部完成成本；C 另重建兩控制的576份右側／雙側完整十列計數。
  這些比較沒有排除一般 allK 控制。

具體獨立程式、完整比較及 reviewer 的紙面審核見
[C/REVIEW.md](C/REVIEW.md)、[B/REVIEW_RIGHT.md](B/REVIEW_RIGHT.md)。
正常／seed17 重播、輸入與輸出 SHA、實際工程結果見 [checks.json](checks.json)。

**不採納主目標已完成、嚴格較小 bad 已構造、一般 allK 已排除、來源實現
已取得或新增 Lean theorem 的宣稱。** 剩餘量化義務與三個接受分支在
[主證明](PROOF.md)及 [主報告](REPORT.md)明列 OPEN。

文件傳播：更新直接 Kempe 導覽與 STATUS；核對 README／HANDOFF 的入口、
研究線及活躍標記未變，依現行治理保留。其他父題 OPEN 未改變，傳播停於
直接來源／導覽層。舊 audit、舊來源定理與舊證書原始位元組保持。
