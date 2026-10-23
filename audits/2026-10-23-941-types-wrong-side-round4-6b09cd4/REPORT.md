# 941第四輪：新增rootless／K資源點的完整原星

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[第三輪](../2026-10-23-941-types-wrong-side-round3-6b09cd4/REPORT.md)，
入口173份前輪最終檔案全驗SHA、零漂移。保同一原G／F、rotation、
原附件、有序B14、字面φ／ψ、全部完整分量、空fibres及full lifts。
四份新exclusive目錄；舊證書及報告不改，未commit／push。

**完整M2非單點現至少十外點；最小資源域的新ω身份已收緊。**
仍限原Γ8嚴格內恰兩點的11份必要型；非空M2至少8外點、空M2至少7、
全11型共同至少7及全域k≥23不變，沒有新增11整型排除。

令R為同一原J−K中含M／N的完整rootless支原點聯集，X為Γ外F私有點，
`Z=X∩(R∪V(K))`、`t=|X\Z|≥1`。χ∉Z，所有Z外點對R無邊。

- [兩個完整M2原星](PROOF.md)：任取不同m,m'∈M2，沿同一原非邊的
  共鄰上界扣除兩星交集，得`|Z|≥|M2|+d(m)+d(m')−3≥|M2|+7`。
  故非單M2至少九資源、十外點；不需T五度或對側分離前提。
  更強地，非空M2且|Z|≤8時，R不能另有完整02分量。
- [非空M2七資源原星](../2026-10-23-941-gamma8-nonempty-resource-stars-6b09cd4/REPORT.md)：
  |Z|=7迫完整M={T,m}、T與m均原五度，m-link只餘原(1,3)型。
  `Z={m,n3,u1,v3,p_d2,p_x2,ω}`，額外ω只能為N1／N3／K0／K2；
  一般仍保m∈C或E。若ω∈N1或K2，完整u-link仍迫原Uu、m∈C及d≠U；
  N1另迫兩份具名ω五度星。N3／K0可失去U強迫，全部四類都不能沿用
  舊60列或16cap，仍須共同接合新增ω星與N星。
- [空M2六資源原星](../2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/REPORT.md)：
  T六度且|Z|=6時，`Z={a3,y1,b3,p_d2,p_x2,ω}`。
  排新增其他rootless分量及ω∈N1；ω∈N3的全部五份部分共同原星也無法
  接成ω的完整cyclic star。因此**ω只能是原K0或K2**，不能再補N原點。
  任意多Z外旁觀點均不能繞過此R原星限制。
- [獨立交叉審查](../2026-10-23-941-gamma8-resource-review-6b09cd4/REPORT.md)：
  核R原鄰點封閉性、U／q／E例外、兩M2原星交集及兩支新ω的全稱
  來源包絡；有限算術／link控制與原來源紙證分開。

本目錄[checker](check.py)獨立核21份完整M2圈鄰點集合對與1,432份
圈外集合賦值的精確極小值。它只證固定域計數控制；原度任意增大的
延伸由符號不等式承擔。兩個子checker另從原十點邊／完整T、m星重建
必要完整links，沒有用新局部關係取代舊完整fibres或full lifts。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-round4-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-round4-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-types-wrong-side-round4-6b09cd4/check.py --negative
```

全部本輪checker的正常／seed17重播、語義及外部破壞反控制見
[VERIFICATION](VERIFICATION.json)；來源／文件傳播邊界見[REVIEW](REVIEW.md)。
[Lean既有專案建置](BUILD_RECEIPT.json)通過8832 jobs，有原有linter警告，
沒有新增Lean定理。文件檢查見[DOC_CHECKS](DOC_CHECKS.json)：正式文件
索引／導覽及docs-only DocGraph通過；全樹歷史重複ID仍72。
有限控制為`triggered and holds`，實際完整來源控制仍`not triggered`。
本輪沒有新增較小候選H或另一份完整cap安全縮減。

下一窄義務：空支先接ω∈K0／K2的完整原星及同一原外側；非空七資源支
接N1／N3／K0／K2如何改變n、u、v與U兩出口原面。一般wrong-side的
無框附枝、同P原01逃逸及其他C割點仍沿前輪停止點。

**11整型、更多Γ內點、長Γ、一般wrong-side、初始八配對、941／W7／J1／J2、
一般較小bad、Lean及matching仍OPEN；共同k≥23、W7排38／40不變。**
