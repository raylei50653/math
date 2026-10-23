# 941第三輪：χ無邊、七／六外點兩支排除與完整cap縮減

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[第二輪](../2026-10-23-941-types-wrong-side-round2-6b09cd4/REPORT.md)
指定的新χ七／六外點接合。入口253份前輪最終檔案全驗SHA、零漂移。
原 G／F、rotation、有序接點、字面框、原附件、完整分量、空fibres與
full lifts全部保留；四份新exclusive目錄，不改舊證書。

**Γ8嚴格內恰二點時，非空M2的七外點與空M2的六外點兩整支均已排除。**
現非空M2至少8外點，空M2至少7，全11必要型共同至少7。
原T五度且M2非單點、或真的觸發對側完整分離支的9外點界保留。
11整型本身、一般wrong-side與父題仍OPEN，共同k≥23不變。

- [非空M2原星繼承](../2026-10-23-941-gamma8-chi-seven-6b09cd4/REPORT.md)：
  χ2∈L、χ3∈B都與整個原J−K的rootless支無邊。七點等號仍封出原60份
  共同全星及16份八內點K6 cap，χ留在其嚴格外側。χ3會擴充外側B，
  不套舊B樹或U的完整外側link。
- [空M2六外點](../2026-10-23-941-gamma8-chi-six-6b09cd4/REPORT.md)：
  χ無法補N的任何原星，L／R仍封回既有七內點K6，O則原度數容量矛盾。
  既有四候選定理同H四列回填、嚴降7／9點，因此整支排除。
- [八內點cap的新安全縮減](PROOF.md)：34份實際候選，每cap選4–6份，
  各自完整關係包含於原R，聯集恰R。33份為同一六框非交叉弦／識別，
  另一份為五輪加一耳。真正原01232完整witness只選一次H，該同一H的
  三拒絕列全沿原外側商映射回填。完成尺寸嚴降7–10點，排全部16cap。
- [獨立交叉審查](../2026-10-23-941-gamma8-chi-review-6b09cd4/REPORT.md)：
  核χ完整分量所有權、同圖共享面、真η選定的收縮合法性與完整候選覆蓋。
  另一路對全部4096字面六框重核候選關係，與主checker方法分開。

主[checker](check_reduction.py)獨立從原14點邊窮盡每cap的4⁸內賦色，
重建496完整fibres（含80空列）、1196份full lifts；再枚舉34份實際
候選圖／商圖的全部頂點著色。416接受tuple各固定一候選核全部31列，
共12896次同候選全列回填核對。正常、seed17、10項語義及2項外部破壞
反控制見[VERIFICATION](VERIFICATION.json)。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/check_reduction.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/check_reduction.py --seed 17
python3 -B audits/2026-10-23-941-types-wrong-side-round3-6b09cd4/check_reduction.py --negative
```

紙面來源接合與有限完整關係權限見[REVIEW](REVIEW.md)，文件檢查見
[DOC_CHECKS](DOC_CHECKS.json)。有限校準為`triggered and holds`，實際完整
來源控制仍`not triggered`；沒有以有限PASS替代平面／來源／最小性證明。
正式文件索引／導覽與docs-only DocGraph通過；全樹仍有72個歷史重複ID，
未刪改歷史檔案來消除診斷。

下一窄義務更精確：令Z是X中位於同一rootless原支或K的原點，t是其餘
外點數。χ不在Z；非空M2必有|Z|≥7、故|X|≥7+t；空M2／T6則|Z|≥6、
故|X|≥6+t。因此空支七點域在χ之外還須一個ω∈rootless支或K；非空
八點域須接七個此類資源點的原全星，額外L／B點不能補rootless原星。
原圈仍是同一Γ8，不改候選來源或字面色框。

**11整型、更多Γ內點、長Γ、一般wrong-side、初始八配對、941／W7／J1／J2、
一般較小bad、Lean及matching仍OPEN；共同k≥23、W7排38／40不變。**
一般wrong-side沿前輪無框附枝、同P原01逃逸及其他C割點停止點，本輪無新
一般wrong-side排除。未commit／push。
