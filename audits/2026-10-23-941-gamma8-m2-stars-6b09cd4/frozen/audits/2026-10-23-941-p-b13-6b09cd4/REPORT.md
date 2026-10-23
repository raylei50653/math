# 941：同一 P／B13 接合排六點型，分開兩個 k2

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`，接續
[上一輪](../2026-10-23-941-patch-order-6b09cd4/REPORT.md)原路標記。
固定同一原圖／色框／完整K交換，限普通短型I、02型13／36的wrong-side。

**恰二真交的六點共u⁻–Z型已排，現在兩patch合至少七原點，且k2必不同。**
新增的同一P最後C橋r–T位於Ω內，給β上原01標記p，不能塞入原共02的兩面
短段。這個排除涵蓋全部D0／D1中心選擇，未排初始八配對。

同一P[r,b]、同一B13最後C橋e–W*後的尾路，在首次相交h截取，再以C內
r→e路閉合，給原Jordan偶圈Γ≥8。Γ保留兩橋，與β只共p及B橋中點n；
Γ內外各有奇數個真交。原實際兩面patch的k2嚴格跟隨中心側別，而Γ沒有
K2點。因此一般wrong-side已迫兩個不同私有K2∩Q點，其中至少一個不同於
指定Z；不能把新點也當成具有Z標記鄰點的橋。

恰二真交若僅共一點，只能是：C內所有r→e路必經的k0、同樣的b1（e為
端點例外）、或固定B子路上的b3。若共b3且雙03中心，原度數至少七。
這些剩餘型未排。此wrong-side下另新證r≠e，03型4時R≠r；沒有先假定身份。

β含p的Ω內子弧至少經8個不同原面，加中心兩側共至少10面；不是面整個在
Ω內。Γ的T兩側各有私有原3鄰點，故不是空cap。最短Γ8的20個非圈點對
只餘兩條三角耳弦x–W*、d–W*；兩弦及內側私有點尚未排。

[PROOF](PROOF.md)保留完整論證與前提；[certificate v2](certificate-v2.json)及
[checker](check.py)只校準固定局部合同。n可為boundary Yq中點、W*=q、
b=c、B路Y–q–c、兩原路多次共點、h早於最後K出口均保留。沒有來源圖枚舉、
LP、新Lean或較小bad。44份authority與63份前輪輸出保管見[INPUTS](INPUTS.json)。

```sh
python3 -B audits/2026-10-23-941-p-b13-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-p-b13-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-p-b13-6b09cd4/check.py --negative
```

實際重播及反控制見[VERIFICATION](VERIFICATION.json)，獨立審查與文件傳播
見[REVIEW](REVIEW.md)。原完整fibres／full lifts逐字保留，本輪只重播沿用的
局部checker；固定校準為`triggered and holds`，完整來源為`not triggered`。

下一窄義務是Γ8兩耳弦及T內側原3點，或較長Γ的具名C割點／B路共點；
一般wrong-side與B側、八配對及941／W7／J1／J2仍OPEN。
接續由[Kempe導覽](../../docs/c5_kempe_guide.md)維護。本輪未commit／push。
