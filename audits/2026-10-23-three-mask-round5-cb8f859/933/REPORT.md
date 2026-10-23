# 933第五輪：新k−8換框圖、兩份正16-fibre族與私有長路

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`；2026-10-23。
只寫本 `933/`，不改前四輪／shared docs，不commit／push。

**新原幾何與縮減**：原aR、Rc皆非邊。前者由無對角原C4(a,p,h,R)排除；
後者由原C5(c,b,p,h,R)的空cap／W5兩支排除。故同一原D可作兩次實際共面
識別，得到固定新圖

```
H*=D/(a=R=c), outer=(A,s,v,w,t), k(H*)=k−8。
```

全部原附件、原有序色框映射與parallel suppression逐項保留，沒有新點。
[PROOF.md](PROOF.md)給原面、兩次操作與完整vertex ledger。

H*全部十列完整投影證支持⊆319；第四輪六fibre任一正皆逐點降到同一H*，
故H*非空。**使用原全域最小性**後，其完整支持只能為271、314、319，
三者都迫01021／01201／01231正。沒有得到較小bad。

前兩份被迫正的H*族全部**無任何rxy帽lift**，但仍是真D正fibres；不能由
帽空推D空。本輪只對各18個targets、三split完整wholecomponent orbit作
一次有界測試：01021排D461／482、01201排D470／491，得到兩個同一原D
的**16-fibre OR族各至少一個正**。其餘未排不當成可行或來源，沒有全2461
多輪closure、廣泛圖枚舉或LP。

私有C的同一02|13完整分割另給新joint掛法：nq同掛s-side時，零點j的02
分量必掛a；同掛t-side則必掛c；V唯一crossed行改掛R,L，明確保留。
前兩種非crossed attached支的原02 r–a/c路至少五邊，D段至少三個strict
private點。四種三邊路都被原r rotation及proper C5 cap排除；最短若恰五，
得到真原induced C7，否則奇長≥7。這些長路及crossed支本輪未排。

[certificate.json](certificate.json)含新640份完整n,L,q fibres、全部原bph／
rxy Cartesian full lifts、完整10×2461矩陣、36target的全部三split options及
子集輸出；同時保留第四輪70,144帽fibres、空fibres、全部舊p,h lifts與G/T0/T1
十列同D矩陣。原bph gate精確為n=q iff可回填，且唯一p=L、b=h=第四色。

13份immutable inputs與routing分開見[INPUTS.json](INPUTS.json)。獨立checker
與正常／seed17／semanticnegative回執見[VERIFICATION.json](VERIFICATION.json)。
root另以D-first獨立重建H*矩陣及catalogue分類，沒有import本輪producer。

```
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/933/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round5-cb8f859/933/check.py
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/933/check.py --negative
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/933/independent.py
```

| 權威／控制 | 狀態 |
| --- | --- |
| 純原非邊、兩次共面H*、k−8成本 | conditional paper source theorem |
| 完整關係、552原零與H*三零列、目錄filter | triggered and holds |
| H*三種完整支持及三正列 | conditional consequence using explicit global minimality |
| 兩正族36-target測試、4個新D零列 | triggered and holds；各剩16的OR族未排 |
| 同一私有掛橋支至少五邊原02路 | conditional source theorem；V crossed不適用 |
| 真商圖／回填有限控制 | triggered and holds；完整來源not triggered |
| 完整原r6／933圖／必要系統共同可行 | not triggered／沒有聲稱 |
| 六fibre全空／一般933／實際較小bad／K∞／Lean | 未證／OPEN／未得／OPEN／無新增 |

下一窄義務是同一原D的兩個正16-fibre族、原六正支及掛三橋長02路的共同
source幾何或可回填化約，不能拼獨立見證。早期probe只留非權威診斷；
最終權威為紙證、checker、certificate及唯讀回執。
