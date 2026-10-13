# 2026-09-27：single-spoke 覆蓋、支援與接點次序

研究報告：[single-spoke cores](../c5_single_spoke_cores.md)。
本輪先以紙面證明任意大小的必要條件，再產生有限支援證書，沒有一般圖枚舉。

- 四種接點分拆的三色不可刪減覆蓋；二接點雙禁色的完整關係、單禁色的
  95 個必要關係 schema；反射直接沿用任意 contact type 的 Lean transport。
- slit-disk 的接點區塊及實際支援順序，允許共用框點及切口兩副本；
  K4-free Gallai 分量的外部至少兩色。這些是紙面必要條件，未 Lean 化。
- (2,1,1) 只分析 s=0、1、4，留下 4、3、12 種按禁色命名的支援型。
  114 個具名配置中，40 個兩個 p 延拓，32 個只證 p₁，34 個只證 p₂，
  8 個兩列未決。接點數限制的缺色交換對單／二接點給不同結論。
- 16 個 R10 既有 (2,2) 來源作控制，3,840 個來源 boundary rows，
  7,680 個完整分量關係反射、240 份逐邊 q 著色；皆不接受 T4。
  它們不提供 (2,1,1) 的可實現性。沒有重新生成或改寫 R10 證書。

停止點：s=0、(S₁,S₂,S₃)=(01,04,234)，禁 3 者為二接點。
p₁ 已延拓；p₂ 若拒絕，必有 R_C₃(p₂)={(0,3),(3,0)}，與 q 的
F_C₃(q)={3} 同圖共存。下一步分析實際接線／palette 與環序；不另枚舉反射側。

實際驗證：

- `python3 scripts/c5_single_spoke_cores.py --check`：通過，重算與 JSON 逐 byte 相同。
- `python3 scripts/c5_two_spoke_reflection.py --check`：通過，沿用反射及既有來源控制。
- `lake build`：通過（8,826 jobs）；只有既有 AttachmentOrder／SymRelabel linter warnings。
- `lake env lean Math/TwoSpokeReflectionAudit.lean`：通過；普通定理僅列既有
  `propext`、`Classical.choice`、`Quot.sound`。
- `python3 scripts/check_docs.py` 與 `git diff --check`：通過。

上述 build／audit 不代表本輪紙面支援或 disk 拓撲已形式化。
未重跑一般 graph catalog、603 profiles、固定點、
R 系列大型覆蓋或全 t=2 排除；沒有新增 Lean theorem。未 commit／push。
