# 非空 M2 的七儲備：排兩個六度原星支，縮至四類 ω

2026-10-23；exclusive BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接[第三輪](../2026-10-23-941-types-wrong-side-round3-6b09cd4/REPORT.md)指定的
新增 rootless／K 原點完整星。仍保同一原 G／F、rotation、原附件、B14
有序接點、字面框、完整分量、空 fibres 與所有 full lifts。

**非空 M2、|Z|=7 時，完整 M 只能是原邊 Tm，且兩端均原五度。**
這裡 Z 是 Γ 外私有點中位於同一原 rootless 支或 K 的全部原點；χ在Z外。
原 T／m 星只留 `link(m)=(a1,T0,n3,u1,v3)`，其中a=r或sΓ，
`Z={m,n,u,v,p_d,p_x,ω}`。唯一新資源點只可能 N1／N3／K0／K2。

[紙證](PROOF.md) 先由原完整 M2 星排非單點，再排 `(D,dm)=(5,6),(6,5)`：
所有候選都迫額外 M0 點，其完整原度至多三；雙五度的兩個M0型即使
准一個任意 ω 補鄰也至多四。留下兩個反射側的雙五度 N 型。
同輪[一般兩星界](../2026-10-23-941-types-wrong-side-round4-6b09cd4/PROOF.md)
另將完整 |M2|≥2 的整支提高至至少10外點，這裡不重複其證書。

ω=N1／K2 時，完整u-star仍迫 Uu、m∈C、d≠U；ω=N3／K0則保留
兩側。**若ω=N1，它原五度，完整原link只餘 `(d,p_d,U,p_x,w)`，w=n或v**。
這兩份完整原星必須再與同一 n／v／出口／U 的rotation接合，仍OPEN。
沒有把舊60列完整星或16封閉cap套進新增ω的域。

[checker](check.py) 精確列24份T／m同圖原星配置、26份額外M0完整星
包絡、四所有權類的62份必要完整u-link與2份N1-ω完整星。
8份凍結authority bytes／SHA零漂移；原χ-seven的496完整fibres含80空列、
1196 full lifts逐字保留，原u-link完整前史certificate另原樣凍結。
正常、seed17、12項語義反控制及兩項外部破壞拒絕通過，見
[VERIFICATION](VERIFICATION.json)。本輪是原來源必要合同，有限星模型
並非來源可實現證書；程序編譯器與checker共用窮盡器，紙證承擔來源涵蓋。

```sh
python3 -B audits/2026-10-23-941-gamma8-nonempty-resource-stars-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-nonempty-resource-stars-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-nonempty-resource-stars-6b09cd4/check.py --negative
```

非空 M2 仍至少8外點；本子線不排任何11整型，不提高共同k≥23。
一般 wrong-side、完整來源接合與父題仍OPEN；未改共享文件或舊產物，
未commit／push。
