# Γ8七外點：χ全支無邊與原八內點K6繼承

2026-10-23；exclusive BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
固定同一原 G、F、rotation、字面φ／ψ、有序B14及完整fibres／full lifts。
接續[前輪原面χ](../2026-10-23-941-gamma8-joint-bpaths-6b09cd4/REPORT.md)。

**新χ與含M／N的整個原J−K rootless支無原邊。** χ2若接此支，會使
碰框L02合併或接入rootless支；χ3同理使碰框B13接入。原色相同的
餘格則由proper coloring排除。此論證處理整個完整分量支。

在j=2、M2非空且恰七外點時，既有計數取等迫完整M2={m}及T、m五度。
χ不能補入任何rootless原星，因此原六點域的完整原星仍逐字成立：
M={T,m}、m∈C、d≠U、Uu原邊，並保60份共同rootless原星。

從同一八點(r,T,sΓ,τ,m,n,u,v)的完整原面聯集，仍封出原六圈
(U,p_d,d,ζ,x,p_x)，內恰八點。**兩種χ均嚴格在原cap外側**；每個七外點
來源必含原16份字面cap之一。完整證明及alias／rotation邊界見 [PROOF](PROOF.md)。
χ3能新增B外側原鄰點；前輪B樹及U完整F側B弧不在本輪繼承範圍。

```sh
python3 -B audits/2026-10-23-941-gamma8-chi-seven-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-chi-seven-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-chi-seven-6b09cd4/check.py --negative
```

10份凍結authority零漂移；獨立checker由原邊重建16份14點／33邊／20面disk，
完整31個有序proper六框共496份fibres，含80個空列及1,196份full lifts。
正常／seed17一致、9語義反控制及外部破壞拒絕見 [VERIFICATION](VERIFICATION.json)。
有限控制`triggered and holds`；實際完整來源仍`not triggered`。

本子線的certificate證條件式cap繼承。[本輪共同縮減](../2026-10-23-941-types-wrong-side-round3-6b09cd4/PROOF.md)
另以34份不同實際候選安全覆蓋全部16cap，每cap取4–6份；由一份原接受
witness選一次同候選，全部三拒絕列都回填原外側，完成尺寸嚴降7–10點。
合兩份紙證，**j=2、M2非空的七外點整支已排，故至少八外點**；T五度
完整M2非單點／真的觸發對側完整分離支仍至少九。一般八外點以上、11整型、
更多內點、一般wrong-side及父題仍OPEN。
更強地，令R為同一J−K rootless支的原點聯集，則原鄰點封閉性
`N_G(R)⊆R∪V(K)`。同一原星取等及安全縮減還給
**`|X∩(R∪V(K))|≥7`**，不限制R∪K以外有多少旁觀外點。
令`t=|X\(R∪V(K))|≥1`，更精確為`|X|≥7+t`。因此額外框分量外點
無法補滿原六點儲備。詳見PROOF第6節；儲備至少七點
的原星接合仍OPEN。

共同k≥23不變，無新Lean／LP／一般較小bad；未commit／push。
