# 941：Γ8 六點等號的完整原星迫 U

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
承接[完整 rootless 星](../2026-10-23-941-gamma8-rootless-stars-6b09cd4/REPORT.md)，
仍限普通短型 I、原02型13／36、初始03型4／9、wrong-side `M∉J_B`，
Γ8 嚴格內部恰二原點。固定同一原 G／F、φ／ψ、rotation、完整原 stars、
B14 有序接點、完整 fibres（含空者）及 full lifts；E 可以 rootless。

本輪收緊六點等號，並處理空 M2 六度支的一個框例外：

- **完整 M2 非空、恰六個圈外私有點時，必有 M={T,m}、m∈C、d≠U。**
  前輪 T／m 均五度；本輪完成 m 的原五度 link 三種原色型，其中兩種
  迫另一原 M0 點度三，故排除。剩下一個原 N1 私有點 u，其完整原星
  必含框點 U，原度只可5或6，完整 cyclic link 只留六種。
- **T 五度、m∈E 或 d=U 時，至少七個圈外私有點。**
  完整 M2 非單點及對側分離的原八點界繼續保留。
- **M2 空、T 六度、恰五外點時，也必有原 N1 點 y 鄰 U，且 d≠U。**
  因此 d=U 時 L／R 亦至少六外點；O 的六點界沿用前輪。

U 是框點，不計入圈外私有點數。排除 E 側只用 C≠E，不要求 E 碰框。
完整論證見 [PROOF](PROOF.md)；剩餘六份 u-link 仍需補齊 n、v、兩 K2
出口的完整原星，並接回同一 U 的 F 側有序 link 及其 Y／V 端點。
**這些 link 是必要限制，尚未構成完整外側 disk 或來源實現。**

[producer](produce.py)依紙證獨立列表；[checker](check.py)由原邊及原色／
完整分量、ψ12 側別、m 的非連續 link 禁弦、原非邊共鄰限制重建：

- 66份六點原色型（11型×兩側×三原色型），僅 C 側的 N1／N3 型存留；
  每型六份完整 u-link 必要限制，共66份。
- 22份 d=U 別名控制均無合法完整 u-link。
- 22份空 M2 五點控制；L／R、d≠U 留48份 y-link 必要限制。
  O 的形式 link 標為前輪已排，不作來源 survivor。

```sh
python3 -B audits/2026-10-23-941-gamma8-six-equality-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-six-equality-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-six-equality-6b09cd4/check.py --negative
```

正式 [certificate](certificate.json) 為 exclusive-create；前輪完整證書逐字保留，
未重算全部原 caps。[INPUTS](INPUTS.json) 凍結8份直接輸入、490份前輪檔案
及4份 routing 入口快照；[VERIFICATION](VERIFICATION.json) 記正常／seed17
一致、19項語義及2項外部反控制全部拒絕，前輪正常／seed17／29項反控制
通過，所有凍結輸入與前輪檔案零漂移。有限校準為 `triggered and holds`，
完整來源仍 `not triggered`；沒有新增 LP、Lean、來源枚舉或較小 bad。
論證與傳播核對見 [REVIEW](REVIEW.md)，文件檢查見 [DOC_CHECKS](DOC_CHECKS.json)。

下一窄義務為 **C 側六點型的六份完整 u-link 接回同一 U，並補齊其餘原星**；
另一支為 **空 M2、T 六度、d≠U 的 L／R 五點接合**。
11整型、更多內點、較長 Γ、一般 wrong-side、初始八配對、941／W7／J1／J2、
較小 bad 與 matching 仍 OPEN，共同 k≥23 不變。本輪未 commit／push；
當前接續入口由 [Kempe導覽](../../docs/c5_kempe_guide.md) 維護。
