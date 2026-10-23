# 941第五輪：K原星封口與同一外側安全縮減

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接[第四輪](../2026-10-23-941-types-wrong-side-round4-6b09cd4/REPORT.md)，
入口162份前輪最終檔案全驗SHA、零漂移。固定同一原G／F、rotation、
原附件、有序B14、字面φ／ψ、完整原分量、空fibres及full lifts。
新證據只寫四份第五輪exclusive目錄；舊報告／證書保持原bytes。
整合者僅同步相關guide／STATUS路由，未commit／push。

**空M2至少八外點；全部11份Γ8／j=2必要型共同至少八外點。**
**非空七資源的ω只餘N1／N3，K0／K2兩支已排。**

令R為原J−K中含M／N的完整rootless支原點聯集，X為Γ外F私有點，
Z=X∩(R∪V(K))，t=|X\Z|≥1。原鄰點封閉性使任意多旁觀點都不能補R星。
完整論證見[PROOF](PROOF.md)。

- [空M2的七內點封口](../2026-10-23-941-gamma8-empty-k-stars-6b09cd4/REPORT.md)：
  T6／|Z|=6時，完整N六圈與至多七個K點迫所有N原五度，封回同一七內點K6。
  不必先封K點在cap外側的星；舊四候選在同一原外側減7／9點，排整個六資源域。
  因此空支|Z|≥7、|X|≥7+t≥8；T≥8原星直接有|Z|≥D−1≥7。
- [非空K資源的共同N全星](../2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/REPORT.md)：
  七資源／雙五度下重建563份放寬完整N星；44份連通原C/E、39份迫原雙色C4，
  餘480份必要列（K0 300、K2 180，含120份d=U），不是來源實現。
- [本目錄整圖傳送](cap-transfer-certificate.json)：獨立從原星取全共享面，
  排44份C/E及6份非簡單collar，對其餘513份較寬包絡全部給出同一六圈次序下
  的完整圖／面雙射至舊16 cap；480份來源必要列全涵蓋。沿雙射傳送既有34候選，
  原真正接受witness只選一次H，同H三拒絕列全回填、嚴降7–10點。
  故七資源的ω∈K0／K2兩整支排除，ω只餘N1／N3。
- [獨立審查](../2026-10-23-941-gamma8-k-star-review-6b09cd4/REPORT.md)：
  另證空支wheel封口，核完整30邊／18面及完整內點星；審非空原星包絡、
  d=U與U／χ外側例外，並獨立核全部513份整cap雙射。

本輪沒有新造安全填片或縮成支持／pair投影。空支保留完整62個S4 fibres及104 lifts；
非空支保留舊496完整fibres、80空列與1196 full lifts。新整圖雙射傳送的是
完整著色關係。既有34候選安全覆蓋checker本輪正常／seed17重播，仍為16cap、
34候選及同H全列回填；前輪有限證書不自行承擔新來源包絡。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/check.py
python3 -B audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/check.py --negative
python3 -B audits/2026-10-23-941-types-wrong-side-round5-6b09cd4/transfer_caps.py --negative
```

新checker的正常／seed17、語義與外部破壞反控制及舊34候選重播見
[VERIFICATION](VERIFICATION.json)；文件檢查見[DOC_CHECKS](DOC_CHECKS.json)，
來源／路由權限見[REVIEW](REVIEW.md)。正常／seed17、44項新語義及8項外部反控制通過；
正式文件及docs-only DocGraph通過，全樹歷史重複ID仍72。本輪未改Lean或重跑lake build；
第四輪既有建置收據保持凍結，不把它改稱本輪驗證。無新Lean定理。
有限控制為`triggered and holds`，實際完整來源控制仍`not triggered`。

下一窄義務：非空七資源ω∈N1／N3的完整共同原星與同一外側；空支新七資源域
的T6額外資源與T8等號星。一般wrong-side沿無框附枝、同P原01逃逸及其他C割點。
非空至少8、非單M2至少10外點不變；空支及11型共同界由7提高到8。

**11整型、更多Γ內點、長Γ、一般wrong-side、初始八配對、941／W7／J1／J2、
一般較小bad及matching仍OPEN；共同k≥23、W7排38／40不變。**
