# 941：Γ8 六外點的同 U 原星接口

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[六點等號](../2026-10-23-941-gamma8-six-equality-6b09cd4/REPORT.md)，
仍限普通短型I、原02型13／36、初始03型4／9、wrong-side及Γ8內恰二點。
同一原G／F、字面框、原rotation、完整分量與stars、有序B14、全部fibres
含空列及full lifts保留；E可rootless。

新增三個相連結果，紙證見 [PROOF](PROOF.md)：

- **M2非空且恰六外點時，六份u-link只餘三形。** 同一n、v、r、sΓ完整
  原星有60份必要限制（L16／R32／O12）；R保額外nx原邊分支。兩K2出口都
  鄰U，完整星餘弧必是同一完整B樹內的有序路。
- **完整B只餘原3點W*與q，迫W*≠q、原VW*邊、YW*非邊及e≠Y。**
  完整B恰是共唯一z∈{e,h,c}的兩星樹，唯一原V→Y路是V–W*–z–q–Y四邊。
  保e=V、h=c及Erootless別名後有6份完整B必要圖。因此W*=q或e=Y的六外點
  等號已排，M2非空時這兩子支至少七外點；11整型均仍未排。
- **接回同一U的F側有序link。** Y端必直接接一出口，V端只可V／V–W*／
  V–W*–e；兩出口間N弧由同一60列決定。兩出口的全部其餘鄰點只在同一B，
  其完整B路仍須共同接上同一U弧，尚未完成外側disk。

B兩星引理也適用M2空、T六度的五外點等號；本輪60列完整星表只屬M2非空
六外點支，未冒充空支的完整接合。

```sh
python3 -B audits/2026-10-23-941-gamma8-u-link-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-u-link-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-u-link-6b09cd4/check.py --negative
```

[INPUTS](INPUTS.json)凍結8份直接authority；[producer](produce.py)與
[checker](check.py)以公式／原邊重建兩種方式獨立核60份完整星及6份B樹。
[certificate](certificate.json)整份保留前輪證書；[VERIFICATION](VERIFICATION.json)
記正常、seed17、14項語義反控制、外部損壞證書及零輸入漂移。
有限校準為`triggered and holds`；來源仍`not triggered`。

**下一窄義務：同一60列原星、同一6份B樹、同一U有序弧，完成兩出口的
共同B-path及其餘原星／完整分量。** 未新增來源、LP、Lean、較小bad或matching；
11整型、一般wrong-side及較長Γ仍OPEN，共同k≥23不變。只寫本專屬目錄，
未改共享docs或舊audit，未commit／push。
