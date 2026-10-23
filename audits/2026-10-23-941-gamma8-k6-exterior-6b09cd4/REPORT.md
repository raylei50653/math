# 941：空 M2 五外點等號已排，Γ8二內點全11型至少六外點

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續前輪空 M2、T六度、恰五外點的同一 K6 七內點 cap。
**已完成此五點等號的條件來源排除，故該支 |X|≥6。** 合前輪非空 M2
六點界及空 M2／T≥8 的七點界，Γ8 嚴格內部恰兩點的全部11型現共同
至少六個圈外私有點；完整11型仍未排，全域 k≥23 不變。

四份局部候選為偶／奇中央三角填片、偶／奇三接點共同識別。它們各自的
完整六框關係都包含於原 cap，聯集恰覆蓋全部19份非空框，保12份空列。
對同一原 G 的一個實際01232完整 witness，只選一次涵蓋它的候選 H；
此同一 H 的三拒絕列全能拉回原外側並補回七點，完成較小目錄外反證。
三角填片少7內點，識別候選少9；原有序 C5 保留，沒有未計完成成本。

[PROOF](PROOF.md)逐一核平面空 disk 的Y樹收縮、無原迴圈、平行邊簡化、
U原為C5內點的ownership、商圖著色拉回與同候選量詞。
直接 authority 已凍結，前輪相關32檔 [final-manifest重播](PREDECESSOR_HASH_REPLAY.json)
零漂移。原完整 cap／空 fibres／全部 full lifts 逐字保留；沒有重跑舊原星、
14填片、W6或雙W4探索。

[producer](produce.py)用紙面關係產生 [certificate](certificate.json)；
[checker](check.py)獨立從四份實際小圖／商圖的完整著色重建候選關係，
逐一核31個全框及4⁶=4096份字面 tuple，再把所有舊 lifts 依同一逆 S4
搬回原13點逐邊重播。四候選各8／8／5／5份框，字面各192／192／108／108。

```sh
python3 -B audits/2026-10-23-941-gamma8-k6-exterior-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-k6-exterior-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-k6-exterior-6b09cd4/check.py --negative
```

正常／seed17及語義／外部破壞反控制見 [VERIFICATION](VERIFICATION.json)。
有限覆蓋 `triggered and holds`；具名實際 source instance 仍 `not triggered`。
紙面五點來源排除與有限校準分開，未宣稱補成實際外側或新一般定理。
空 M2 六點同源接合、11整型、更多內點、較長Γ、一般wrong-side、初始八配對、
941／W7／J1／J2、Lean、matching及一般較小bad仍 OPEN。未 commit／push。

同輪 [原 z4–V 面的新私有點 χ](../2026-10-23-941-gamma8-joint-bpaths-6b09cd4/PROOF.md)
另給五點等號的獨立短證，且把非空 M2 的六外點等號也排除；其紙證核查見
[REVIEW_FACE_POINT](REVIEW_FACE_POINT.md)。本目錄保留四候選縮減為可重用的
獨立來源排除，χ 不在本 checker 的有限檢驗範圍。
