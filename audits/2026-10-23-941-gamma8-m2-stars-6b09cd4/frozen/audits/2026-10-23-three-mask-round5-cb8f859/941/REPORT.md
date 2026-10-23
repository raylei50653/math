# 941第五輪：兩份同源四色原面，排五點壓縮

2026-10-23；BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

**新增wrong-side支的共同原面限制，未排初始配對。** 普通短型I、02型13／36，
若指定最後T的原02分量M不在原J−K的B側，第四輪給K內一條C–Q邊。本輪
把原K–B與同一後繼C–Q的兩條完整界面真正接合：後繼界面兩端在原K側外，
卻經K內，所以至少兩次真橫穿；相切不算。

每次真橫穿都在同一原邊的兩個原三角面，給四色patch：

```text
k0∈K∩C，k2∈K∩Q，b3∈B∩Q，b1∈B∩C；
原4圈 k0–k2–b3–b1–k0；
原中心對角 k0–b3 或 k2–b1，另一對角為原非邊。
```

因此至少有兩份不同中心的joint patches。原C3／C4空有界側排它們合併到
至多五個原點：或補成K4，或形成兩條對角均為全域原非邊的原C4。故任兩份
不同橫穿patch合起來至少六個**原點**；不是六私有點。只有各k2必私有；
k0可U、b1可V／Y、b3可q。patch k2不自動認舊Z，b1不自動認R或r。
完整界面／原rotation及原cap反證見[PROOF](PROOF.md)。

同一P最後K出口後的b亦在B∩C外；由同一B的Y→b原13路可指定Q橋W*，
而W*仍可能是boundary q。這適用兩初始03型；以舊R出發的版本另需03型4。
本輪也明確澄清第四輪末句：R與r**不預先識別，可同可異尚未知**，沒有R≠r
引理。K0不全在C、M不自動認L等邊界繼續保留。

[certificate](certificate.json)保全部四份target／02完整前輪記錄、原03兩型、
原01四型、全域inverse、完整七點／原cap lifts與空fibre保管。本輪有限核對
只做8個局部零線四臂配置及20個四／五點同色身份schema：4真橫穿／4相切；
20 schema分為6同中心、10 K4、4無對角C4。沒有來源圖枚舉、LP或有限生存控制。
[INPUTS](INPUTS.json)封28份數學authority，六份routing另存；drift分開。

```sh
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/941/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-three-mask-round5-cb8f859/941/check.py --seed 17
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/941/check.py --negative
```

正常／seed17獨立程序重建一致；16項semantic negatives與外部污染／缺欄證書
均拒絕；immutable drift0，詳[VERIFICATION](VERIFICATION.json)。全稱界面進出及
原C3／C4推論由紙證承擔，有限校準是`triggered and holds`；完整941來源與
wrong-side實際觸發為`not triggered`。

已排的具名子支是wrong-side下「至多一次真橫穿」與「共同patch可壓在至多
五原點」。M在B側及wrong-side一般支均未排，兩target各八配對仍OPEN；一般
941／W7／J1／J2、較小bad與Lean沒有升級。tip、rootless、原X／T／Z五度
兩側、至少六度及03型9無X/R引理均保留。

下一窄義務是兩份patch在同一K–B界面上的次序及共點方式，與原P／B13路的
共同rotation；不能把至少六點誤作完整來源實現。只寫本941目錄，未改前四輪、
shared docs或Git，未commit／push。
