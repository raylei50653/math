# BR-SD-1g-ADOPT：獨立採納審查

日期：2026-10-11。Repository：`raylei50653/math`。
固定 base／起始 HEAD／main：`c15a635e17d4be814e19aeeeeb765f3d6024099a`。
原研究 base：`dbdc4c35f785519c8e3cb0260807f0d2feb82469`，兩者不得混用。

目標：不預設原證明正確，獨立判定 BR-SD-1g candidate scoped exclusion 是否具備正式接受的完整精確子域紙面證明。
可用裁決只有 ACCEPTABLE／NEEDS REPAIR／REJECTED；ACCEPTABLE 僅準備回寫提案，不執行正式採納。

## 固定輸入與審查分工

- 原 [PROOF](../2026-10-11-br-sd-1g-dbdc4c35/PROOF.md)、[MAPPING](../2026-10-11-br-sd-1g-dbdc4c35/MAPPING.md)、[REPORT](../2026-10-11-br-sd-1g-dbdc4c35/REPORT.md)、[SEAL](../2026-10-11-br-sd-1g-dbdc4c35/SEAL.json)。
- 原 [paper REVIEW](../2026-10-11-br-sd-1g-dbdc4c35/agents/paper/REVIEW.md)、[ACCEPTANCE](../2026-10-11-br-sd-1g-dbdc4c35/agents/paper/ACCEPTANCE.json)、publication [PRECHECKS](../2026-10-11-br-sd-1g-publication/PRECHECKS.json)。
- [N45 canonical](../../docs/c5_excess_two_nonadjacent_unit_core45.md) §1／§2.11，已採納 BR-SD-1a／1c／1e；既有權威文件全部唯讀。
- `/root/proof` 重新重建 degree lists、完整延拓、Gallai 前提及 J2／有限樹矛盾；不先讀原 paper review。
- `/root/mapping` 重建完整同一原來源量詞、degree／attachment 表、臂與重合及既有引理適用性。
- `/root/custody` 核原 160 檔、publication 6 檔、31 authority、313 舊 frozen 檔、seals、tracked/index bytes 與實際 verifier 重播。
- Root 重播有限控制，另寫獨立固定測例驗證、整合裁決及提案；另一 reviewer 核最终 payload bytes。

## 必須驗證的命題

完整同一 G／M／β／Σ933／941／ε=2、非相鄰 degree5 roots、其餘有效 degree4、U=0、L long、S short 且 actual 真框邊 pair、M 自身同 β minimal 且拒絕、split22／三原奇環／單原 bridge、兩旁支唯一接點與原 ownership／attachments、所有合法零長臂及 a3=v 重合、全部 witnesses／relations／空 fibres／full lifts。

獨立重建 `L^D` 的全鄰居定義、逐點 degree 下界、C coloring 與 M 同 β／s=D 完整延拓的存在 iff、ignored 原坐標的完整因子、外部 Gallai theorem 的全前提與 palettes。獨立核 J2 witness、`P_J2={T,D}`、唯一 S–L 接口、q 起始 block、T/D 交替留 S、不回頭 incidence walk、非割點／leaf／triangle／K4／任意有限 W2。

禁止推論 `D∈L(x1) ⇒ D∈P_J1`。必要容量不是 actual source realization；六份 synthetic fixtures 不承擔任意大小量詞。

## 驗證及寫入边界

實際重播 publication `verify.py --check --require-tracked` 正常／`PYTHONHASHSEED=17`；原 verifier 能力／基準差異須如實記錄，不修改它。重播 primary／independent finite controls 與負控制，執行 `scripts/check_docs.py`、`tools/docgraph --include 'docs/**/*.md' check`、`git diff --check`。保留 argv、環境、stdout／stderr、exit code。

只新增本目錄。原 BR-SD-1g 160 檔、publication companion 6 檔、31 authority、313 舊 frozen 檔、全部既有 seal、canonical、STATUS、HANDOFF 不改。
所有 tracked 文件的起始 bytes／symlink target／mode／index blob 由 [WORKSPACE_BEFORE](inputs/WORKSPACE_BEFORE.json) 記錄；終局逐項核對。
不 commit、push、merge 或正式採納；交付保留 untracked audit，owner 另行授權。

任何裁決下，完整 `N45-S-NOU-LS-PAIR` 父身份 OPEN；完整 OPEN 身份新增無條件關閉數 0。
其他 split22／非 split22、多旁支、其他三環、R31、ε≥3、一般 N45／N2／E、`K∞=K≤5` 不升級。
