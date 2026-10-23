# 941：Γ8 空 M2 五外點縮為兩份完整 cap

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[六點等號原星](../2026-10-23-941-gamma8-six-equality-6b09cd4/REPORT.md)
的空 M2、T 六度、d≠U、L／R 恰五個圈外私有點分支。
固定同一原圖／rotation／字面框、完整原分量、空 fibres 與 full lifts；
U 保框例外，E 起初允 rootless。

- 前輪每核心六份完整 y-link，補齊同一 a、b 原星後，**L／R 各只餘一份**。
  a,b,y、r,sΓ 皆迫五度；連原 τ，共六個 N13 點全五度，T 六度。
- 完整 K02 恰原六圈 `(d,p_d,U,p_x,x,ζ)`，內恰七點；
  L／R 各四份耳身分共八份必要全星列，均成13點、30邊原 cap。
  兩個字面 K6 框的完整 fibres 各恰四個 lifts，正好完整 M／N 原交換，
  其餘16,380內賦色全空。
- U 的 F 側 link 迫包含連續弧 L 的 `p_d–y–b–p_x` 或 R 的
  `p_d–a–y–p_x`，允整體反向；**未假定 U 有完整 F cyclic link**。
- 同源完整 M 交換迫 E rootless、h≠c。完整 B13 另迫原 VW* 邊、
  W*≠q、e≠Y；唯一出口 z∈{c,e,h}，最短原13路恰 V–W*–z–q–Y。
  d,h,W* 均私有，e 只餘私有或 V。

完整來源論證見 [PROOF](PROOF.md)，精確 cap 見 [K6_CAPS](K6_CAPS.json)。
[producer](produce.py)按紙證 exclusive-create [certificate](certificate.json)；
[checker](check.py)獨立重建66份 y-link 的共同完整 a／b 星、8份 r／s 星、
40份 B13 出口列及16份完整字面 fibres，共64 lifts、262,080空賦色。

```sh
python3 -B audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-empty-m2-6b09cd4/check.py --negative
```

[INPUTS](INPUTS.json) 凍結9份直接 authority 與3份 routing 入口快照。
正常／seed17／語義及外部破壞反控制與零漂移 receipt 見
[VERIFICATION](VERIFICATION.json)。前輪完整 certificate（含原空 fibres
與 full lifts）逐字保留；沒有重算全部原 caps。

有限校準 `triggered and holds`；完整來源仍 `not triggered`。
這八列未補成同一完整外側 disk，**11整型未排**；本輪亦未排最後的
空 M2 五點分支。下一窄義務為同一 K6 cap 的完整外側／唯一 B13 出口與
U/F 側原 link、完整 B14 stars 接合。更多內點、較長 Γ、一般 wrong-side、
初始八配對、941／W7／J1／J2、真正較小 bad、Lean 與 matching 仍 OPEN，
共同 k≥23 不變。只寫本 exclusive 目錄，未 commit／push。
