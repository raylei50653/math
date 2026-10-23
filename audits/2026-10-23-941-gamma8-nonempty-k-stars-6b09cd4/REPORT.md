# 非空七資源ω∈K：完整N星縮至480份共同必要列

2026-10-23；exclusive BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接[第四輪非空七資源](../2026-10-23-941-gamma8-nonempty-resource-stars-6b09cd4/REPORT.md)，
仍保同一原G／F、原rotation、原附件、有序B14、字面φ／ψ、完整分量、
空fibres及全部full lifts。

**ω∈K0／K2時，七份同圖完整T、m、u、n、v、r、sΓ原星有563份放寬列；
原來源反證排83份，餘480份必要列（K0有300、K2有180）。**
K0仍保d=U的120列；K2仍迫m∈C及d≠U。44份K0列因ω連通ψ12的C／E而排，
39份K2列因交叉出口原邊形成雙色禁C4而排。

[紙證](PROOF.md)以R原鄰點封閉性證完整N星包絡，逐星累加同一圖的全部
原面邊；沒有用舊60列覆蓋新增ω。K原星則保留Z外B／其他rootless支的任意
13鄰點，逐列輸出既定原面弧、完整K02連通要求及同一U的F側有序link接口。
它們仍須共同定向／接合，並非來源實現。

[checker](check.py)重建全部563列及83份拒絕理由，8份凍結authority零漂移，
整份上輪certificate逐字保留。正常／seed17、12項語義反控制及外部破壞拒絕
見[VERIFICATION](VERIFICATION.json)。producer與checker共用窮盡器，紙證
承擔原來源涵蓋；`explore.json`為給共同collar審查的凍結563列交換檔。

```sh
python3 -B audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-nonempty-k-stars-6b09cd4/check.py --negative
```

此子證書不單獨排K0／K2來源；下游必核同一完整cap及共享原面後才能傳送
既有安全縮減。11整型、一般wrong-side、完整原外側、真正較小bad、Lean及
matching仍OPEN，共同k≥23不變。未改共享文件或舊產物，未commit／push。
