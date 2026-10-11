# BR-SD-1g 正式採納：獨立數學、合同及最終 bytes 審查

2026-10-11；reviewer `/root/proof`。固定採納基準
`c15a635e17d4be814e19aeeeeb765f3d6024099a`。
Owner 後續批准精確採納、必要文件同步及通過檢查後的 main commit／push；
本 reviewer 只寫本新 audit 的 `proof/`，不改文件、舊證據或 Git 狀態。

**裁決 ACCEPTABLE；數學／原來源合同／最終工具及新 payload 沒有阻斷 finding。**
完整父身份 OPEN；actual source `not triggered`；新 Lean theorem 0；
新增完整 OPEN 無條件關閉 0。本接受不宣稱尚未發生的 seal、commit、push 或遠端讀回成功。

## 1. 獨立來源與八項合同

原 [PROOF](../../2026-10-11-br-sd-1g-dbdc4c35/PROOF.md) 的 §§3–5 已由本 reviewer
重新推導，當時沒有沿用原 paper reviewer 的結論。完整推導、外部原來源核對及所有角落
保存在已封 [獨立 proof review](../../2026-10-11-br-sd-1g-adopt-6eae3597/agents/proof/REVIEW.md)。
本輪把實際 [canonical](../../../docs/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)
及五個直接文件逐份對回已封 [八項提案](../../2026-10-11-br-sd-1g-adopt-6eae3597/CANONICAL_DELTA_PROPOSAL.md)，
沒有重寫原 candidate 或為取得接受而修改歷史證明。

| 項 | canonical 保留的精確合同 |
| --- | --- |
| 1 | 任意有限簡單原 G、ordered induced-C5 disk、完整有序 Σ933／941 或整份具名資料的 D5 像、ε2、G 自己全部 witnesses、有效 H 連通、非相鄰原 degree5 roots、其他有效點完整 degree4，以及 §1 的原 full B-touch／one-sided／非空 support。 |
| 2 | 完整原 L/S mixed、U0、L long、S **short**；actual S 聯集恰同一真框邊 pair，Wi 附件計入原 owner 的完整 support。 |
| 3 | 只刪 r 唯一原 spoke，M 與 G 同原 vertices；X=M，M 自己對同一 literal 三色 β minimal 且拒絕，M 自己全部 retained-edge witnesses 保留。 |
| 4 | M 的原完整 degrees、s 的原三 spokes 及有序相異 p∈L／q∈S、sole C、r split22／C 度4／M 無 spoke；45／54 只作整份 roles／資料共同搬運。 |
| 5 | 指定 J1 triangle(r,a1,x1)、任意奇長 J2/J3、唯一原 uv bridge；任意 h/ℓ≥0 的原 simple bridge arms，含 p=a1、q=a3、a3=v，正臂原互斥及無額外骨架邊。 |
| 6 | 恰兩個任意有限非空 connected off-skeleton 原 Wi，唯一骨架接點 x1／x2∈J3∪q-arm；保全部原接入邊及內邊、所有合法接入 multiplicities，沒有第二接口、相互邊、額外 s-contact、第三旁支或 cross edge。 |
| 7 | W1/W2 原 ownership L/S、各原骨架 ownership、所有原 A(y)、C 逐點完整 degree 式、actual S 聯集恰 pair、L 不受 pair 兩點限制；保全部合法 x2／mi／重合，不能刪原附件以容納旁支。 |
| 8 | 全部原坐標、具名／有序／共用 contacts、附件／support、ownership、bridges、rotation／disk embedding、literal Col／β、G/M 各自 witnesses、完整 relations、空 fibres、full lifts，及 effective-H 忽略原坐標的允許色因子。 |

canonical 的八項正文逐項覆蓋提案，摘要沒有取代合同。五份同步文件明確路由完整正文；
沒有把 degree 容量或六份 fixtures 宣称為來源實現。任意大小有限 Wi、所有零臂及合法重合
仍由紙面量詞承擔，沒有新增拓撲正常形或枚舉量詞。

## 2. 紙面推論在回寫後仍完整

對每個原 y∈C，從所有原鄰居定義
`L^D(y)=Col∖(β(A(y))∪{D:sy∈E(M)})`。
`d_C(y)+|A(y)|+1[sy∈E(M)]=4` 及可能重複的附件色給 `|L^D(y)|≥d_C(y)`；
沒有把不等式先誤作 tight equality。C 的 list assignment 與同一 M／β／s=D 的全延拓
有相同存在性。完整 assignment 還須乘上每個被 effective-H 忽略的原內圖孤立點因子；
B-only 點因子為 `Col∖β(A(z))` 且含 D，真正無附件孤立點有整份 Col。
canonical 明說投影忘坐標不宣稱 bijective，沒有遺失 full-lift factors。

M 自己拒絕 β 給 C 不可 list-coloring。外部定理適用於有限連通簡單 C 及完整
degree assignment，無二連通前提。每個 maximal block 的合法 clique／odd-cycle palette、
橋大小1、奇環大小2、Kn 大小 n−1、原點 incident-union 及共享原點 palette disjointness
均保留。原審查已從 [Dvořák 作者 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
核定義及 Theorem10，fresh PDF SHA
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`；
本輪延用該已封版本，不作新的未核外部主張。

原 w2∈J2−{r,u} 始終存在，包括 J2 triangle，未受任一 Wi 影響且不是割點或 s-contact。
其 C 度2／完整 degree4 及 actual pair 附件給 `P_J2={T,D}`。
S−q 的各原 list 均含同一 T,D，q 含 T 而禁 D。q 的 incident-union 給含 T 不含 D
的 block；exclusive 是只就 T/D 而言，palette 可另含 A/B。

exclusive block 不可能碰 J2 的任一原點，包括 r，否則與 `{T,D}` 違反 disjointness。
S 到 L 的唯一接口經 J2／r，故步行始終留原 S。每個 block 有另一原點可作出口；
其 list 需要缺色，incident-union 提供不同 block，disjointness 保另一色 exclusive。
block／vertex 都換節點。完整 all-vertex incidence 圖是有限 block-cut tree 加非割點葉；
不回頭 walk 無重點，不能重遇 q。取有限最長可行路徑，仍能再延伸兩條 incidence 邊而矛盾，
沒有無限選擇的隱藏前提。非割點／leaf 缺色即矛盾，triangle／K4 都有不同出口；
任意有限 W2、零臂及 a3=v 不改变此步。

這條證明容許 D 由 W1 提供給 x1，不使用失效推論
`D∈L^D(x1)⇒D∈P_J1`，也不借用 1c terminal lemma、二連通、SD-A 或 R31 minor。

## 3. 文件 diff 及狀態邊界

[原始讀取](READS.json) 與 [最終重新讀取](final-reads/READS.json) 保存全部實際命令、
stdout／stderr／exit；最終 snapshot 包含 canonical／四 guide-status 文件的整份 diff、
新 history、TASK／REPORT／manifest、CHECKS、兩位 worker review 及所有新工具。
[獨立唯讀檢查](final-checks/CHECKS.json) 的 normative、docs、diff、raw-evidence 核對均 exit0。

§1、§2.1–2.10、既有 §2.11（SD-A 與採納 1a／1c／1e）逐字未變。
HANDOFF／STATUS_HISTORY／README 逐字未變。HANDOFF 實際17行 thin routing 已足夠；
STATUS 索引新 history，沒有回寫歷史快照或當輪候選語境。
變更只限 [AUTHORIZATION](../AUTHORIZATION.json) 的五份既有文件加一份新 history；
六份最終 bytes／mode 與 [ADOPTION_MANIFEST](../ADOPTION_MANIFEST.json) 及
[mapping final records](../mapping/FINAL_DOCS.json) 一致。

完整 N45-S-NOU-LS-PAIR、未涵蓋 split22／非 split22、兩／多旁支、其他三環／更多環／
一般 Gallai 接線、R31、其他45／54／55身份、ε≥3、一般 N45／N2／E、一般出口及
K∞=K≤5 均不升級。source NOT TRIGGERED；lake build 沒有新增 Lean theorem。

## 4. 新工具的獨立 code review

新 [verify.py](../verify.py) 不 import／mock 歷史 verifier；其 stdlib custody 重建獨立檢查
BASE ancestry、main、15743 BASE entries 的 HEAD／index／work bytes／modes、精確 M/A 白名單。
只有五份已批准 live authority 可對新 manifest；原31 frozen authority 及原 research blobs 不變。
原研究160、publication6、舊 filesystem313（309 tracked＋4 local-only）及 sealed review281
完整 paths／bytes／modes／envelopes 都另固定。四份 local-only 不能被 promote 為 tracked。

即使尚未 require-tracked，只要新 history 已存在於 HEAD／index，就須對回 approved bytes／mode。
final require-tracked 強制六份文件及兩個新增 audit 的完整 HEAD／index coverage，不能用 working
tree 的正確內容遮住已 stage／commit 的錯誤。此檢查承認 owner 批准的 descendant HEAD；
不把歷史 exact-base whitelist 的 exit1 冒稱成功。

唯一寫入分支是取得 final acceptance 後 exclusive-create 新 SEAL；其他模式唯讀。
final acceptance 綁六份 documents 及所有新 payload（只排自己／未來 seal），seal 再包含 acceptance。
完整 exact object／hash／size／mode／inventory 核對；沒有可追加 payload 的 postseal 排除。
`--validate-manifests` 只作具名 memory 控制，不能代替 final acceptance 或 require-tracked。

record_check 保留 actual argv／cwd／environment／exit／stdout／stderr 及 raw receipt hash，
拒絕 symlink logs、parent escape、既有 final acceptance／seal；unique folder 不覆蓋舊結果。
aggregate 不修改原 receipts，兩個 retained failures 保 actual1／expected0，要求同 argv 成功重播。
normative_readback 比較字面段落；其 readback 已由本 reviewer 獨立重播成功。
logger_controls 在 repo 外 disposable tree 執行，negative_controls 只用 memfds；
後者先 positive exit0，再要求9次具體錯誤理由的 negative exit1，且核 protected bytes 不變。

本 reviewer 發現的 logger boundary 與兩個 manifest harness reason 字串問題已在 root freeze 前修好；
最終 code 已重讀。初次 logger fixture 本身漏建 logs parent 的 raw exit1／harness v1仍保留，
其後同 argv exit0。沒有為修工具去改歷史 seal 或 original checker。

| 最終新工具 | SHA256 |
| --- | --- |
| verify.py | `a070b3401c6680392deef65a091c07a17566251dcbf604d09ac3367d7d044af7` |
| record_check.py | `bdf3271c0b9e6ad5f7cc02cdb412577704357ee1f7dc8eceeb845672d2dddefc` |
| aggregate_checks.py | `8efc4804dbefbb6c6f5f1a8a30428741beb50ca50e3eea468088106a344484fa` |
| negative_controls.py | `cd22f5cf8afa21b74b9dcd348cc1262ec5e37cf7f352b9cba7e3358b33e09028` |
| logger_controls.py | `1cab5d8d36561fa5d5f94d7f08f215c17e8c0db54b06ab5317467309b2b6fcc4` |
| normative_readback.py | `235c17fa7cc4f0af6aafedc445718857968f1461834529888dd44a786b579e59` |

## 5. 最終證據及接受接口

[CHECKS](../CHECKS.json) 的35項 current commands＝22項 exit0＋13項 expected exit1；
另2項 retained actual1／expected0及同 argv 成功重播。所有 stdout／stderr／raw receipt hashes
與原欄位已由本 reviewer 跨核。五對 normal／seed17 stdout 一致，包含新 adapter。
九個 solver corruption controls 只校準證書拒絕；四次歷史 publication exit1 與獨立 adapter exit0分開。
新 manifest controls 的 positive0＋九項 negative1、protected bytes unchanged，以及 logger
positive0／三项預期2均有實際完整紀錄。有限 controls 只支持各具名 synthetic fixtures。

本 reviewer 的 normative、docs（603Markdown／7446local links）、git diff --check及 evidence
跨核均實際 exit0。root 的 DocGraph／lake build／finite／custody結果由原 receipt 支持；
未因其成功推來源實現或新增 Lean。一次誤用 `tools/` 路徑的 read failure另保存於
[原始失敗](RETAINED_READ_FAILURE.json)，隨後已重新讀正確工具，並非 proof finding。

發出 acceptance 前再核本 audit 的最後唯讀 precheck 原始收據及完整 inventory。
acceptance 的 schema、六份 document rows、所有 payload rows及 canonical bundle SHA
由已審查新 helper 的公開純函數生成，寫入後本 reviewer 停止 payload 寫入。
root 尚須實際 seal、唯讀 normal／seed17 sealed checks、stage／commit／push、require-tracked
與 HEAD／origin/main／remote main 相等讀回；所有後續 receipts 在 repo 外，不改已接受 bundle。

**最終 reviewable 範圍 ACCEPTABLE，blocking findings＝0；完整父 OPEN、source not triggered、
新 Lean theorem 0、新完整 OPEN 無條件關閉0。**
