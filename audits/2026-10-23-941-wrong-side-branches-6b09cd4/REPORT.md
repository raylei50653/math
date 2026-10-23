# 一般 wrong-side：無框附枝與共點原星再收緊

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
保同一 P、任意同 B 路 S、任意同 C 路 L 的全路量詞，不限 Γ8／二內點。

**恰二真交若共 b3=v，B−v 的 b 分量 A 現在一律無 B14 接點，包括 v=q。**
新排除 q 共點而 A 含 c 的子支：同一 B 路可選 Y–q–c 再接 A 的 c→b 路，
Γ 在 q 用兩條 F boundary 邊；q 的所有 F 原面同側，撞兩中心一內一外。
這保留 b≠c 與 W*=q，沒有把完整 B 稱 rootless。

完整共點星還給下列新界。m 是兩中心中 D0 的數目：

| 原共點與適用域 | 新必要度數 |
| --- | --- |
| 恰二真交、私有共同 b3=v | d_G(v)≥6+m |
| 恰二真交、共同 b3=q | d_F(q)≥7+m |
| 上列且兩個 patch b1 都不是 Y | d_F(q)≥9+m |
| 任意真交數、相反側共同 k0=U | d_F(U)≥5+m，d_G(U)≥6+m |

私有 b3 至少三個原色1鄰點；q 因 A 不含 c 至少四個，U 因 C 的框割點
限制亦至少三個。每個 D0 再給一條非色1–非色1原 link 邊。私有點用
完整 cyclic link；q／U 只用 F boundary link 路，沒有誤套完整 cyclic 星。

U 的新條件排除是：C−U 中含 r、e 的兩支不能分別含 V、Y；否則可選
同一 L 經 boundary V–U–Y，再撞兩 patch 的 F 面側。至少一支須避 V/Y，
未把它擅自稱全 rootless。U 五度共 k0、私有 b3 五度等相應子支因此排除。

同一 P[b,c] 必給實際01逃逸段：端點在不同 B−v 分量，內部避 B、K、C，
且投影到同一非 K 的 J−B 分支。這是下一接合義務；未假 P 尾段全在 B。

全稱證明及例外見 [PROOF](PROOF.md)。[certificate v2](certificate-v2.json)／
[checker](check.py)獨立以整數 DP 核12份完整 link 計數、三份 B 刪點圖、
兩份 C 框割點圖及同一01逃逸控制。v2 明寫原中心色，U-link 用1/2/3、
私有 b3／q-link 用0/1/2；初版抽象計數字證書仍保留，未覆寫。
控制不稱941來源；有限校準 `triggered and holds`，來源仍 `not triggered`。

```sh
python3 -B audits/2026-10-23-941-wrong-side-branches-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-wrong-side-branches-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-wrong-side-branches-6b09cd4/check.py --negative
```

[INPUTS](INPUTS.json)記錄先驗上一輪 FINAL_MANIFEST 的91份本線輸出及54份
繼承 authority 相符，再凍結61份輸入；全部原空 fibres／full lifts 保留。
六份正常／seed17／反控制（含前輪checker）、11份破損拒絕與零漂移 receipt
見 [VERIFICATION](VERIFICATION.json)。沒有重算原 caps 或枚舉來源 disk。

下一窄義務是無框 A 的同一01逃逸與全部原星，或 C 的其他割點／01橋。
一般 wrong-side、八配對、941／W7／J1／J2、較小 bad、Lean、matching
仍未由本項全面解決，共同 k≥23 不變。只寫本專屬目錄，未 commit/push。
