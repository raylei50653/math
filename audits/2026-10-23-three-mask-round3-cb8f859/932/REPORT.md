# 932 round3：距四雙接點只餘單一pair的一／二點

**新定理：在同一全域最小no4ct、完整932、h=4的全部二十份原C9合同中，
所有距四雙接點只能使用同一種原pair；這個pair至多兩個原中心，若有兩個
則必有原邊相連。** 每份collar因此只餘19份必要接觸模板，共380份。
單pair及無距四接點的來源仍OPEN；共同k≥23不變。

[來源合同](SOURCE_CONTRACT.md)、[任意大小短紙證](paper/PROOF.md)、
[完整幾何證書](certificate.json)、[獨立唯讀checker](check.py)。
BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

九種距四pair的36對中，27對在原C上四端點交錯，兩個原二邊路被Jordan
分離排除；其餘9對共享端點，另外兩端相鄰，圍成同一原C5 pocket。
空cap只有一條可能對角線，無法完成三角剖分；W5中心卻有三個原C contacts，
撞第二輪定理。相同pair的兩條路圍出空原C4 lens，只能以原中心邊作對角線；
三條路的最外兩條則圍入中間中心，直接撞C4 cap空。這些是任意內側大小
原來源的共同嵌入限制，不是有限圖控制替代來源排除。

單pair分出的原C6／C7 cells另有完整full-fibre雙射。不同色原anchors下，
一中心／兩中心都給兩個outer products之和，僅rank≤2；同色anchors僅rank≤3。
本輪沒有套用rank-one rectangle，沒有新增C9 row deletion或較小bad。

兩張具名有向disk控制具一／二中心，嚴格內點12／13。逐邊側別、完整link、
degree、contacts、原邊面第三點及所有C3／C4／C5 caps均核對。它們沒有原B、
完整932、全域最小性，完整來源狀態為`not triggered`。full-lift接合控制為
`triggered and holds`：不同／同色anchors的全部1220／1260份fibres（含空）
及直接whole full tuples完全相等。兩控制分別核4772／7544份whole lifts。
同一literal frame的真實count minors行列式為+16／−16，rank-one誤用是具體
`counterexample`。

獨立checker不import producer，重建全部位置／cap阻礙並核20份原case完整SHA、
真名與19模板。原820列、十列annulus fibres及full lifts照凍結authority
完整保留；沒有重播外部C4 census、舊180份刪除或廣泛圖枚舉。
18份immutable輸入及六份routing入場快照見[ledger](INPUTS.json)。正常／
seed17唯讀重播、11項語義負控制及drift0見[VERIFICATION.json](VERIFICATION.json)。

```bash
python3 -B audits/2026-10-23-three-mask-round3-cb8f859/932/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round3-cb8f859/932/check.py --check --negative
```

下一窄義務是單pair原C6／C7的兩sector完整共同實現或可回填化約；不能將
兩個獨立可行cell拼為來源。一般932、h≥5、smaller bad、K∞及新Lean仍OPEN。
不改前兩輪／共享文件，不commit／push。
