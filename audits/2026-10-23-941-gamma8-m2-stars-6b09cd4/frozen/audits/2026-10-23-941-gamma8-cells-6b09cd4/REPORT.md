# 941：Γ8外耳迫2／4／6內點，二內點收成11共同型

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[同一P／B13原圈](../2026-10-23-941-p-b13-6b09cd4/REPORT.md)，只追普通短型I、
02型13／36的wrong-side且共同Γ恰長8。原圖、色框、rotation、完整stars與
全fibres／full lifts保留；未排初始八配對。

**Γ8有0／1／2個外耳時，至少有2／4／6個私有內點。** 外耳加圈使h或e
成為F私有點，完整原度數迫三個Γ內鄰；雙外耳用原非邊最多兩共同鄰及已有
共鄰W*再收緊。一般外耳仍保留，不能宣稱耳必在圈內。

若Γ8恰兩內點，外耳全排；內點必為原3的τ∈N∩Q與原2的ζ∈K∩Q。
扣四個實際面strip後，原六圈只餘L／R／O三核心，配兩耳presence共12份，
排O雙內耳（ζ度四且有禁C4），得**11份完整有序十點局部必要型**。
不是11份完整941來源；Γ外的原stars與固定B14仍未接完。

同一圖的KB／CQ、KB／EQ、KN／CQ、KN／EQ四種joint patch共用ζ，各在
Γ內恰一中心。16個中心D選擇排KN雙D1的四份與全D0的一份，恰餘11份。
ζ五度四型的C／C外兩側各保兩型；不以五度排除。T五度時，其唯一原2鄰
與另一原3鄰都必在Γ外，仍保兩種外側link次序。

完整論證見[PROOF](PROOF.md)，[certificate](certificate.json)與[checker](check.py)
保11份原面、兩內點完整原star、φ／ψ同圖交換及兩個字面boundary的完整
二點fibres。獨立固定域1,365份邊子集與12候選重建相符；此核對只涵蓋具名
Γ8二內點合同。53份authority及138份前輪輸出保管見[INPUTS](INPUTS.json)。

```sh
python3 -B audits/2026-10-23-941-gamma8-cells-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-cells-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-cells-6b09cd4/check.py --negative
```

實際重播及反控制見[VERIFICATION](VERIFICATION.json)，獨立審查及文件傳播
見[REVIEW](REVIEW.md)。完整來源仍`not triggered`；有限固定域為
`triggered and holds`，全稱外耳／覆蓋為紙證。沒有新Lean、LP或較小bad，
共同k≥23不變。W*=q及所有圈外附件例外保留。

下一窄義務是11型與同一Γ外原stars／B14接合，或j≥3（有外耳至少4／6）；
一般wrong-side、B側、八配對及941／W7／J1／J2仍OPEN。接續由
[Kempe導覽](../../docs/c5_kempe_guide.md)維護。未commit／push。
