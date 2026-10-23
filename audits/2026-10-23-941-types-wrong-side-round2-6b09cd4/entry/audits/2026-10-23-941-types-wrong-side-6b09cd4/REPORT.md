# 941：11整型的完整星接合與一般 wrong-side 接續

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
承接[六點等號](../2026-10-23-941-gamma8-six-equality-6b09cd4/REPORT.md)，
三名 agent 分別推完整 M2 六外點、空 M2 五外點與任意長 Γ，另作相互紙證
審查。保同一原 G／F、rotation、字面框、有序 B14、原附件、完整分量、
全部空 fibres 與 full lifts；沒有逐列換候選或拼接不同 palette 見證。

本輪得到三個相連增量：

- [M2非空六外點](../2026-10-23-941-gamma8-u-link-6b09cd4/REPORT.md)：
  六份 u-link 收為三形；同一 n／v／r／sΓ 的完整原星共60份必要限制。
  兩個 K2 出口都鄰同一 U，餘星必接同一完整 B13 樹的有序路；U 的
  F 側 V→Y link 亦收成明確接口。W*=q 或 e=Y 的六點等號已排，故這兩
  子支至少七外點。一般六外點接合及全部11整型仍 OPEN。
- [M2空、T六度五外點](../2026-10-23-941-gamma8-empty-m2-6b09cd4/REPORT.md)：
  L／R 各只餘一份共同 y／a／b 完整原星，合8份耳身分列；完整 K02
  迫原六圈，內恰七點，N13 六圈全五度、T六度。原字面框及整 K 換後
  各恰四個完整 lifts。E 必 rootless；同原外側接合仍 OPEN。
- [一般 wrong-side](../2026-10-23-941-wrong-side-general-6b09cd4/REPORT.md)：
  任意 Γ 長度／內點數的共 k0／b1 升為全 C 路割點，共01邊必是 C 原橋，
  共13邊只能是同一最後 C 橋。恰二真交的共同 b3 隔開完整 B 的 B∩C 與 b；
  **b=c 時此共 b3 子支已排**，亦涵蓋 h=c⇒b=c 的情形。b≠c 的共 b3、
  C 割點、兩 patch 不共點及四次以上仍 OPEN。

兩個 Γ8 等號支還共同迫 W* 私有、原 VW* 邊、YW* 非邊及 e≠Y；完整
B13 為兩個原3星共唯一 z∈{e,h,c}，唯一 V→Y 原路是四邊
V–W*–z–q–Y。別名按同一原點集合處理，六點支保 h=c，空支已排 h=c。
完整同源論證分別見三份報告；root 的共同接口核對見 [PROOF](PROOF.md)。

root 另以新 K6 cap 的全部有序 proper 六框作獨立直接核對：31個同框 S4
類中各19非空、12空，逐列保完整52份 lifts。14份空六邊形三角化、W6及
三份雙W4均未給安全且保原交替框的通用替換覆蓋；此為窄域控制，沒有
構造較小 bad。完整表 [v2](CAP_RELATION-v2.json)及 [CAP_VERIFICATION](CAP_VERIFICATION.json)
保留空列、full lifts、正常／seed17一致與4項破損拒絕；未重算全部舊 cap。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-6b09cd4/check_cap_relation.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-6b09cd4/check_cap_relation.py --seed 17
python3 -B audits/2026-10-23-941-types-wrong-side-6b09cd4/check_cap_relation.py --negative
```

三份子報告各附 checker、exclusive-create certificate、正常／seed17／負控制
與凍結 hashes；本輪重播與交叉審查索引見 [REVIEW](REVIEW.md)，原入口及
數學輸入快照見 [INPUTS](INPUTS.json)。完整來源仍 `not triggered`，有限
校準為 `triggered and holds`；紙證子支排除不由固定控制的 PASS 推出。

下一個窄義務：六外點須在同一60列、同一6份 B 樹及同一 U 有序弧上完成
兩出口共同 B-path；五外點須將 K6 的19列完整關係接回同一原外側與 B14，
保同一 accepted witness 及全部 backfill。一般長 Γ 須處理剩餘 C 割點與
b≠c 的無框 B 附枝。當前排程由 [Kempe導覽](../../docs/c5_kempe_guide.md)維護。

**11整型、更多內點、一般 wrong-side、初始八配對、941／W7／J1／J2、
嚴格較小 bad、matching 及新 Lean 仍 OPEN；共同 k≥23 不變。**
本輪未 commit／push，既有未提交研究產物保留。
