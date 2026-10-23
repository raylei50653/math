# χ 原分量與密封 cap 的獨立交叉審查

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
保同一原 G／F、rotation、有序 B14、完整分量、空 fibres 與 full lifts。

**新 χ 對 J−K 中含 M 的完整 rootless 支全無原邊。** 原2 χ 還對整個 K
無邊；原3 χ 的未知 K 附件仍保留。這使七／六外點等號中的舊 rootless
完整原星及密封 cap 原樣繼承，無需先補 χ 或 B 的全部外側星。

[PROOF](PROOF.md)審查兩條繼承：非空七外點的16份八內點 cap，及空支
六外點的兩份七內點 cap。原3 χ 可擴充 B，所以沒有繼承舊六份 B 樹及
完整 U-link 的額外假設。空支沿用既有四候選單向縮減；非空新候選族另由
本輪主線提供完整關係安全性。本審查另記識別候選接未知外側時，必由真正
接受 witness 排原邊收縮成迴圈，以及所有平行邊、原 C5 與尺寸帳。

[第二份獨立 checker](check_cover.py)按弦等式與hub可用色，逐一核4096份
字面六框；主線34候選各自安全且逐cap聯集覆蓋，14724份字面回填及
7167744份同一固定候選跨列檢查通過，尺寸嚴降7／8／9／10點。
正常／seed17一致、四種候選損壞全拒絕。紙審亦確認 reservoir 計數可保留
任意多個 rootless 支外旁觀點：非空 M2 至少8外點、空支至少7外點。

[獨立 checker](check.py)核18份 cap 的共同面定向、完整內點圈 link、框點
路 link、全部實際面與單一有序邊界；另逐邊核原存1196份 full lifts，保
496列及80空 fibres。十份凍結原輸入零漂移，正常與seed17一致、四種損壞
均拒絕，見 [VERIFICATION](VERIFICATION.json)。有限域 `triggered and holds`；
具名完整來源仍 `not triggered`，沒有以拓樸控制 PASS 推來源排除。

```sh
python3 -B audits/2026-10-23-941-gamma8-chi-review-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-chi-review-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-chi-review-6b09cd4/check.py --negative
```

全部11整型、更多內點、一般 wrong-side 與父題仍 OPEN；共同 k≥23 不變。
只寫本 exclusive 目錄，未 commit／push。
