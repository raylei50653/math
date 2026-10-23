# 941：Γ8 外側迫四／五私有點，接回 B14 的完整分量交換

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[11個二內點必要型](../2026-10-23-941-gamma8-cells-6b09cd4/REPORT.md)，
固定同一原圖、色框、rotation、完整原stars、有序B14及全fibres／full lifts。

**Γ8恰兩內點時，L／R迫至少4個、O迫至少5個Γ外F私有點。** 圈內τ／ζ
的原共鄰禁止同一對原非邊再有圈外共鄰；四個外側原面與完整link遂迫此界。
加τ／ζ，至少6／7個私有點不在Γ上，未提高原共同k≥23，也未宣稱sharp。

完整rootless M02／N13交換把11型接回固定B14，新增：

- `h=c` 時，d、e均必私有。
- `W*=q` 時，e≠V。
- `d=U,W*=q` 時，兩耳弦皆不存在。

這三項對此Γ8的任意內點數及耳側成立。M交換後再翻同一K，原路
`e–d–r–T–sΓ–x–h` 成為12路；不假設原C／E全部連通性保留。
進一步得到完整M2的ψ12分離義務：h=c迫M2截斷原C的框路；d／e碰框且
原E碰框時，迫M2截斷原E的框路。j=2時分離點全在Γ外；E仍可rootless。

24個端點身分模式剩12個；每份target／02合同有116個必要接合列。
四合同的1,056列保464、排592。**11型全部仍有私有端點分支**，並非464個
完整來源或外側collar實現；ζ五度兩側未排。下一窄義務為完整M2分離集
與四／五外點原stars在同一外側disk的共同接合。

[PROOF](PROOF.md)給完整紙證；[certificate-v2](certificate-v2.json)與
[checker](check.py)獨立重建端點域及88份同圖交換的全部528份局部分量。
原完整fibres、空列及full lifts逐字保管，未重算全部原caps。早期四點證書
保留，新O五點版為exclusive-create。65份authority與219份前輪輸出見
[INPUTS](INPUTS.json)；獨立審查見[REVIEW](REVIEW.md)。

```sh
python3 -B audits/2026-10-23-941-gamma8-exterior-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-exterior-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-exterior-6b09cd4/check.py --negative
```

實際重播／反控制見[VERIFICATION](VERIFICATION.json)。有限域為
`triggered and holds`；完整來源仍`not triggered`。一般wrong-side、Γ8更多
內點、較長Γ、B側、八配對、941／W7／J1／J2及較小bad仍OPEN；無新Lean、
LP或來源枚舉。當前接續由[Kempe導覽](../../docs/c5_kempe_guide.md)維護。
本輪未commit／push。
