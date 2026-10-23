# 941第六輪：N1／N3完整共同原星與空支七資源

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接[第五輪](../2026-10-23-941-types-wrong-side-round5-6b09cd4/REPORT.md)，
入口202份前輪最終檔案全驗SHA、零漂移。固定同一原G／F、rotation、原附件、
有序B14、字面φ／ψ、完整原分量、空fibres及full lifts。
新證據只寫四份第六輪exclusive目錄；整合者同步相關guide／STATUS。
未commit／push。

**非空M2七資源整支排除，至少九外點；空支T八度至少十外點。**
**空支及全部11型共同界仍八外點，非單M2至少十外點不變。**

令R為原J−K中含M／N的完整rootless支原點聯集，X為Γ外F私有點，
Z=X∩(R∪V(K))，t=|X\Z|≥1。任意多旁觀點均不能補R原星。
完整整合論證見[PROOF](PROOF.md)。

- [非空N1／N3共同全星](../2026-10-23-941-gamma8-n-stars-6b09cd4/REPORT.md)：
  N1以u、ω三個原共鄰直接排除；N3由唯一N1接點、同一K路及n/u/v/a完整
  cyclic links排除，分別處理u五度／六度與d=U。合第五輪K0／K2，得|Z|≥8、
  |X|≥8+t≥9。331份未封ω必要星只作校準，不是來源實現或來源涵蓋證明。
- [空支原輪與七資源](../2026-10-23-941-gamma8-empty-seven-6b09cd4/REPORT.md)：
  D條T-link邊迫D個不同原02面點，得|Z|≥2D−7、|X|≥2D−6；d=U再加一。
  T8七／八資源均排，至少十外點。七資源只餘T6，兩新點各在同一N或K；
  兩K只餘d≠U、一K0一K2的K8 collar，度數型為一七度或兩六度。
  兩N、一N一K與K8安全替換仍OPEN，未提高全部空支下界。
- [獨立審查](../2026-10-23-941-gamma8-n7-review-6b09cd4/REPORT.md)：
  另證輪面點注入、N1三共鄰，逐支核N3短證，並獨立從331列補完整ω星。
  沒有把U的F-link或未知K外側尾弧封成完整原星。

非空完整496個fibres／80空列／1196份full lifts保持凍結；
空支舊K6完整62個fibres／24空列／104份lifts另獨立重算。
21份K8抽象全星控制核34邊／20共享面，沒有K8縮減或來源實現聲稱。
舊K6四候選的真正接受witness仍只選一次H、同H三拒絕列回填。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-round6-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-round6-6b09cd4/check.py
python3 -B audits/2026-10-23-941-types-wrong-side-round6-6b09cd4/check.py --negative
```

正常／seed17、39項語義與9項外部破壞反控制通過，見[VERIFICATION](VERIFICATION.json)；
正式文件及docs-only DocGraph通過，全樹歷史重複ID仍72，分見[DOC_CHECKS](DOC_CHECKS.json)。
權限、來源涵蓋與路由核對見[REVIEW](REVIEW.md)。本輪沒有新Lean或重跑lake build。
有限控制為`triggered and holds`，實際完整來源控制仍`not triggered`。

下一窄義務：空M2／T6／七資源的一K一N、兩N完整共同原星，及K0+K2的
K8完整關係與同H安全替換；非空接新八資源域。當前停止點見
[Kempe導覽](../../docs/c5_kempe_guide.md)。

**11整型、更多Γ內點、長Γ、一般wrong-side、初始八配對、941／W7／J1／J2、
一般較小bad及matching仍OPEN；共同k≥23、W7排38／40不變。**
