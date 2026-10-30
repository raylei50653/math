# 十三內點完整外圈與 W5 私人圈秩至少四整理發布

2026-10-13。使用者提供兩份隔離研究回覆後，授權整理並 commit + push。
兩包皆固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`；整合起點為
`5211a92178dffd9d7cd3f883a19d8a3f03932d07`。主線其後的 Cell／K₄ 成果保留，
兩份原研究沒有使用它們作前提。

## 採納範圍

- [K13-COLLAR](../archive/reports/c5/structure/c5_k13_collar.md)：一般有序 disk-C₅ 完整關係
  `K≤13=K≤5=K132`；目錄外來源至少十四內點。h=4 的41份根圖（含兩份有弦圖）、
  h=5 的4份根圖（均兩條內弦）全部 Σ=1023；h=6／7 由紙面普遍排除並與
  完備分類吻合。全域最小來源化約、外部 Brinkmann–McKay 生成完備性定理、
  C 實作及完整有限證書分層；不是僅由零觸發外推。
- [W5 contractible 圈秩三](../archive/reports/c5/structure/c5_w5_private_rank3_contractible.md)：在全部
  目錄外 disk-C₅ 圖中先最小化內點、再最大化邊數取 G。任取合法全內部
  induced W5，固定原中心 v、原循環 U、外框 B、十 pins 及原輪面，令
  `P=V(G)\(B∪U∪{v})`，則 `ρ(G[P])≥4`。contractible 的 c=1／c=2
  分支完整排除，接既有 essential 排除完成圈秩三。2,162＋108 份必要模板的
  八種完整 Σ 均在 K132，直接排除來源；沒有聲稱縮減代表或 R³ 保存。

W5 證明獨立從 k≥13、r≥7 開始；整合後 K13 可另給未來來源 k≥14、r≥8，
不改原分類域、模板數或證書。一般 h≥4 並未採納；C₈ 八項更大來源、
`K≤14`、圈秩≥4 的一般縮減、小 annulus／R³ 代表、E-ARC2 及
`K∞=K≤5` 仍 OPEN。未新增 Lean theorem，未重播 Dvořák–Lidický 外部計算證書。

## 原證據保存與本次驗證

兩份原隔離 audit 的248份非快取檔案保持原 bytes，包括 frozen inputs、
完整關係／空 fibres／full lifts、原 seal、成功與失敗紀錄。
K13 的17個原路徑及13個 gzip blobs 追加到既有 ARCHIVE；整合前的全部
files／blobs records 不變。新 checkout 先依[封存還原說明](../../audits/README.md)還原。
原 seal 另涉及18份共享文件，這些原版本以 deterministic gzip 保存於
publication 的 `source-docs/`；當前正式文件採納兩份成果並保持並行主線內容。

原 K13 seal／delivery checker 和 W5 verify 的 HEAD、空 index、整份共享文件
條件只適用原隔離工作區。保留其原程式及 manifest，發布後使用
[整合保存核對](../../audits/2026-10-13-k13-rank3-publication/verify.py)，
核對原 audit、全部原 seal 項目、原文件快照、BASE bytes、封存追加及新的整合 manifest。

本次在主線重新執行 K13 主 normal／seed17、獨立全部 lifts、結構負控制、
主證書逐 lift 比較、空 fibre 校準及完整內側覆蓋；306份根圖、3,060列及
41,021份完整 lifts 全一致。W5 主 normal／seed17、獨立完整 checker、
K132 membership 與負控制亦重播通過：2,270模板、23,244,800 cells、
928,404 A lifts、465,866 G lifts 及16次破損拒絕。兩包重播前後原檔 hashes 不變。

未重新執行完整球面生成、11,284,042份 min4 生成或小域全邊集校準；
沿用兩份原生成及74項原工具測試證據。此次文件、正式／全域 DocGraph、
儲存政策、Lean 回歸、白名單及 Git index 還原，以
[發布核對紀錄](../../audits/2026-10-13-k13-rank3-publication/REPORT.md)與各 log 為準。
原全域 DocGraph 的62項 duplicate-ID 失敗保留。

## 文件傳播與停止點

Closure scope：十三內點全部 disk-C₅ 關係，以及完整最小來源任取合法 W5 的圈秩三。
Updated：兩份正式入口、cofacial／degree／collar／C₈ 直接 consumers、
W5 父題／單環／雙環／essential／五輪交付入口、Kempe 導覽、STATUS、封存入口。
Reviewed-unchanged：README／HANDOFF 的入口與研究線未變；歷史快照維持日期語境，
State／common-language／synthesis 不接管本次停止點。
Remaining OPEN：上述十四內點以上、一般缩減及父命題義務。
Propagation stop：L2；完整最小來源的下界不等於一般主命題完成。

只提交兩包及相連白名單。推送後核對 HEAD、origin/main、遠端 main 相等；
具體提交 SHA 與工作樹狀態以即時 Git 及本次回覆為準。
