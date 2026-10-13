# 2026-10-11：BR-SD-1b canonical 採納與 residual 對帳

本輪只採納／對帳已獨立驗證的 BR-SD-1a 精確子域；沒有新增數學證明、來源搜尋或完整 N45 closure。
起始 actual HEAD、origin/main 與 `git ls-remote origin refs/heads/main` 均為
`fc3d3d8b4c5b8e6378268edb5cd3f04b50940b5a`，工作樹乾淨。
BR-SD-1a 的執行 HEAD `0f181045…` 與 source BASE `4dd11f4…` 是原 audit provenance，
不是本輪發布基準。原 REPORT 的未 commit／push 語句保留稽核時點；後續
[PUBLICATION](../../audits/2026-10-11-br-sd-1a-0f181045/PUBLICATION.md) 與
[發布 commit](https://github.com/raylei50653/math/commit/fc3d3d8b4c5b8e6378268edb5cd3f04b50940b5a) 說明 audit 已發布。
採納審查交付時，文件 diff 留在工作樹供 owner 審查；該階段沒有 commit、push、merge 或 GitHub 回覆。

## 採納審查與證據界線

Canonical Source： [N45§2.11](../c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)。
Evidence：原 [REPORT](../../audits/2026-10-11-br-sd-1a-0f181045/REPORT.md)、
[PROOF](../../audits/2026-10-11-br-sd-1a-0f181045/PROOF.md)、
[逐前提 MAPPING](../../audits/2026-10-11-br-sd-1a-0f181045/agents/mapping/MAPPING.md)。
本輪父端與唯讀獨立核對均未發現阻止精確採納的前提映射或證明缺口。

| 原身份核對 | 採納邊界 |
| --- | --- |
| 原 G／Σ | N45§1 的同一 ordered induced-C₅ disk、完整 Σ933／941 或整圖 D₅ 像、ε=2、原非相鄰 degree5 roots，原逐邊 Σ witnesses 全保留 |
| 省略身份 | exact-S、原 U=0、一 long L／一真框邊 pair-support short S；僅省略 r 唯一原 boundary spoke，X=M=G−e |
| M 合同 | 自己是同一 literal proper 三色 β 的 inclusion-minimal 拒絕 core，retained 邊同 β full witnesses；s 唯一完整 degree5，其餘有效內點4 |
| C 合同 | 實際 sole C、原 p/q 與 s 三 spokes 全留、r-contact split22；恰三原奇環、J1/J2 共用 r、J3 不交、唯一環間原 bridge uv、末端各一原外臂、無其他 blocks／旁支 |
| 同源資料／量詞 | actual contacts、attachments/supports、ownership、rotation、boundary assignments、完整 relations／fibres／full lifts 全留；任意奇環長≥3及外臂長≥0，不獨立換色框 |

| 四步紙面核對 | 結果 |
| --- | --- |
| 原 M 拒絕 ⇒ C 不可 L^D 著色 | 完整原度4給 degree-list 下界；D 未用使 s=D 合法；C 著色與原 β 沿全部原邊接合即違反 M 拒絕 |
| J1/J2 的具名 witnesses | w1∈J1−{r,a1}、w2∈J2−{r,u}；奇環至少三點，無旁支與末端 contacts 保兩點非割點／非 s-contact，含零長臂 |
| 兩份 lists 保同一 D | 全部 C 鄰居恰本環兩鄰點，其他原 M 鄰居恰兩個 B 附件；同一 β 未使用 D |
| Gallai palettes 矛盾 | 非割點 list 等於本環 palette；相交 J1/J2 palettes 必互斥，卻都含同一 D |

正式外部數學依賴是 [Dvořák 作者講義 Theorem10 與 blockwise-uniform 定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪核對凍結全文／第6頁圖像與作者原 PDF；[SOURCE](../../audits/2026-10-11-br-sd-1a-0f181045/external/SOURCE.md)
保存下載及 hash。這是有定理與證明的講義，不標成期刊論文或 Lean theorem。
任意大小推論由封存 PROOF 承擔；有限31,296列、三份 synthetic M、normal／seed17及負控制
沿用原 REPORT 的校準紀錄，本輪未重跑 controls。校準為 `triggered and holds`；撤 D 負控制
不滿足來源 list 合同。Actual target source 未提交，`not triggered`，沒有完整来源反例或新來源實現。
Seal verifier 只核 bytes，不以其 PASS 取代紙面審查；沒有新增 Lean theorem。

保留原精度 finding：a3≠v 未假定，不能從私有錨點推 H_M 二連通。
直接 D 矛盾不依 SD-A、H_M 二連通、T4 定位或 uv→R27；四 component queries、target β-minimality
及舊 minor 路線沒有在本輪補完。Canonical 採納段落與前段二連通應用分清合同。

## Residual coverage

| 來源身份／義務 | 狀態 |
| --- | --- |
| BR-SD-1a 精確 split22／共用 r 雙環／三環單 bridge 無旁支，任意環與外臂長 | Scoped exclusion |
| 完整 N45-S-NOU-LS-PAIR；無 U、long／pair-short 其他 splits 及 split22 其他形狀 | OPEN |
| 其他 bridge-separated 三環、旁支、接點位置、更多環、一般非二連通來源及完整兩 long 身份 | OPEN |
| R31 同末端不同二接點的任意長來源 minor | OPEN |
| 其他 45／54、原 55、無 45／54 來源 | OPEN |
| 一般 N2／E、ε≥3、一般單側／共同出口、主命題及 K∞=K≤5 | OPEN |

**完整 OPEN 身份新增無條件關閉數仍為 0。**
既有 LOW／HIGH／LONG 及 U 的排除合同與覆蓋不重開；subset 不提升為父身份 closure。

## 文件傳播核對

依即時 [GitHub Issue #4](https://github.com/raylei50653/math/issues/4) 與 [DOCUMENTATION](../DOCUMENTATION.md)
的 L0/L1/L2/L3、closure 與反向引用規則，以 ordinary file search 核直接 consumers。
文件足以說明關係，未使用 Graphify；沒有新增 registry 或治理框架。

Updated：N45 頁首／採納表／§2.11／§3 的精確採納與 residual；degree-5 guide§4 的停止點與
BR-SD-1c 候選義務；degree-5 interfaces§7 的舊「待採納」接續；Kempe guide 對應狀態列／§3；
STATUS 的 BR-SD-1a 直接索引、N45 條目、degree-5 短狀態及本紀錄索引。
本紀錄保存當輪核對與驗證，不另建現況總帳。

Reviewed-unchanged：N45§1及既有 LOW／HIGH／LONG／U；degree-5 interfaces§7 的 SD-A 定理與
四 component queries 語義；degree-5 guide 的 R9–R31 表與 R31 任意長來源義務；
[Phase B 共通引理§2.1](../c5_phase_b_common_lemmas.md) 的 B-S0 前提及
無 U long／兩 long 父身份 OPEN，均未受此 subset 採納改變。原 audit、certificates、hashes、
negative controls、失敗代次及既有歷史文件保持原 bytes；STATUS 歷史條目的「待獨立封存」保留當輪語境。

Remaining OPEN：上表所有父身份與未涵蓋義務。
Propagation stop：L2；直接 consumers 的舊停止點需更正，父身份與上層一般結論仍 OPEN。
研究線／tags／全域路由未變，不展開 L3；README、HANDOFF、全域 synthesis 不修改。

## 驗證命令與實際結果

| 本輪命令 | Exit code | 實際範圍／結果 |
| --- | --- | --- |
| `python3 tools/audit_archive.py restore` | 0 | 2,425 paths、1,494 unique blobs；既有 bytes 不覆寫，只按 archive 還原 |
| `python3 -B audits/2026-10-11-br-sd-1a-0f181045/verify.py --check` | 0 | 65 sealed payloads、14 authority inputs 與指定 Git blobs 核回；actual_head 欄是原 0f181045 provenance |
| `python3 scripts/check_docs.py` | 0 | 600 Markdown、7,353 本地連結，anchors／index／HANDOFF 核回 |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | 0 | 62 documents、213 relations、5 families，0 errors／0 notes |
| `git diff --check` | 0 | 本輪 diff whitespace 通過 |

額外只讀 custody 核對 exit0：前後65,234個既有 audit 檔案（排除 Python cache），
regular files 共10,780,527,468 bytes；SHA256／size／mode 與 symlink targets 無變更、無缺檔，
本次 restore 未新增路徑。原 frozen audits、證書、hash、負控制及歷史失敗紀錄保持不變。
交付前 HEAD／origin/main／遠端 main 再讀仍同為 fc3d3d8，Git index 無 diff；
工作樹只有五份 live docs 變更及本份新增歷史紀錄，沒有其他寫入。
未執行：BR-SD-1a `--live` 固定 HEAD=0f181045，發布與採納後不適用；原 verifier 不改寫。
未重跑全庫 DocGraph、R／N45 大枚舉、大型 certificates、finite controls、來源搜尋或 `lake build`。
本輪未修改 Lean，既有 Lean 建置不能取代此紙面核對；formal docs 檢查不聲稱全工作樹 DocGraph PASS。

## BR-SD-1c 候選研究義務

目前候選入口由 [degree-5 guide§4](../c5_degree5_guide.md#4-r31-保留缺口與重播入口) 維護。
在保留同一原 G／β／完整 degree／contacts／ownership／完整關係的條件下，先限定含具名旁支
或另一種 Gallai block 接線的子域，判定兩個非割點、非 s-contact 的原 witnesses 是否仍存在，
或另證同一 D 必進入相交 blocks 的兩個 palettes。旁支破壞 witness 選取時，保留具名障礙與
原資料，再尋 palette 傳遞論證；有限 controls 不能替代無界證明。本輪未直接實作此推廣。

## 採納文件發布階段

採納審查完成後，owner 明確授權「整理後 commit + push」。本階段只發布 N45 canonical、
degree-5 guide／interfaces、Kempe guide、STATUS 及本紀錄，共六份相連文件。
原 audit／proof／certificates／hash／負控制與 archive 不變；沒有新數學採納或 Lean 宣稱。
發布前重跑上述五項命令；commit／push 結果以實際 Git commit、origin/main 與遠端 main
回讀及工作樹狀態為準。前述未提交／fc3d3d8／工作樹欄位保留原採納審查時點。
