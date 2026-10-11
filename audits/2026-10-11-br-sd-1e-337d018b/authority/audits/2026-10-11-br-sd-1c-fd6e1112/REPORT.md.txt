# BR-SD-1c：單一原旁支的 scoped exclusion

2026-10-11。**結論：指定原來源域不可能存在，任意大小紙面證明已完成並經獨立審查。**
這是本專屬 audit 的 candidate scoped exclusion，canonical 採納另行裁決。
沒有改動共享 canonical source、BR-SD-1a／1b、既有 LOW／HIGH／LONG／U，沒有 commit／push／外部發文。

工作目錄 `/home/ray/developer/ai/math`；來源 BASE 與 actual HEAD 均為
`fd6e1112e6f5e9fd23c50d2f3b5d2ef874954d69`；起始工作樹乾淨。
唯一輸出為本目錄 `audits/2026-10-11-br-sd-1c-fd6e1112/`。

## 精確命題與結果

保留 [BASE N45§1及§2.11完整來源合同](../../docs/c5_excess_two_nonadjacent_unit_core45.md)：
ordered induced-C5 disk 原 G、完整 Σ933／941 或共同整圖 D5 像、ε2、自己的逐邊 Σ witnesses；
非相鄰原 degree5 roots r/s、其他有效原內點4、無原 U、原 L long／S actual support 恰真框邊兩端；
exact-S 只删原 r 唯一 spoke，`X=M=G−e` 自己拒絕同一 proper literal 三色 β、自己同 β minimal，
保其 retained-edge witnesses；M 只有 s degree5、其他有效內點完整度4，s 恰原 p/q contacts及三 spokes；
同一 `C=H_M−s={r}∪L∪S` 為 sole connected component，r split22。

保留原任意奇長 J1/J2/J3、`J1∩J2={r}`、原 J2–J3 bridge uv、原 p/q 末端外臂
（各任意非負長，允許 a3=v）；所有 ordered/shared contacts、實際 attachments/supports、
ownership、rotation、全部原邊、literal 四色框、完整 relations／fibres／full lifts 均保留。
唯一形狀放寬：允許**一份來源自己的有限非空 pendant branch W**只接在 J1 或 J2 的
具名 x，無其他新增 s-contact、cross edge 或骨架接入位置。不是對一張已 degree4 的舊圖任意增邊。
W 的附件及 blocks 必由候選原來源供給；不宣稱抽象 W 是合法 disk source。

此完整精確合同不能同時成立。**本輪涵蓋所有單一 W 的 x 位置、triangle 例外、任意環長、
原 p/q 臂長與有限 W 大小**；完整 `N45-S-NOU-LS-PAIR` 仍 OPEN。

## 任意大小證明的核心

[PROOF](PROOF.md)／[MAPPING](MAPPING.md) 保存完整合同與逐原點推導：

1. r 已由四條原 cycle 邊飽和，接任何非空 W 即違完整 degree4，直接結構排除。
   a1/u 只容第一 W bridge；其他私有點最多容兩條 W incident 邊。degree 可行不證來源實現。
2. 原 M 邊定義 `L^D(y)=Col−β(N_B^M(y))−({D} if sy原邊 else ∅)`；
   完整度4給逐點 `|L^D(y)|≥d_C(y)`。若 C 可染，和原 β、s=D 沿全部原邊接成 M 完整染色，
   與拒絕矛盾。因此 C 不可著色，正式 Gallai 刻畫給 incident palettes 的互斥聯集。
3. 長奇環或旁支接在原已排除錨點時，J1/J2 的非割點、非 s-contact witnesses 仍存在。
   唯一可能耗盡 witness 的是 triangle 第三點 x 被旁支佔用。J2 例外仍由未動 J3 與 uv route 迫 D 回 J2。
4. J1 triangle 例外的泛用 D-routing 不成立。但**原 S 的 actual pair support**等於全部 B 鄰点集合，
   只含同一真框邊两端。以 T 記第三個 β 色，原 J3 私有非 contact 點完整 degree4 強制
   兩附件恰 pair，故 `P_J3={T,D}`。q 臂零長時 q 禁 D；長1時 q list={T}；
   長≥2時第一 off-cycle 臂點 list={T,D}。正長臂的首 bridge palette 非空且包含於該 list，
   在 a3 與 J3 palette 相交，卻必互斥。三類涵蓋全部原長度，且不受 W 在 J1/J2 的接入影響。

因此得到可重用的**原 pair-supported 奇環／唯一 s-contact 外臂局部排除引理**。
必要前提包含原附件範圍、未被佔用的私有環點、bridge 臂、臂端點無其他 C 邊。
這個局部引理比「cutpoint list 有 D 就傳給原環」精確；後一推論有保存的 counterexample。
本輪使用的正式外部依賴是 [Dvořák Theorem 10／blockwise-uniform 定義，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
版本與凍結 hash 見 [SOURCE](external/SOURCE.md)。紙面證明不依 SD-A、H 二連通、R27 minor 或 T4 定位。

## 獨立審查與保留精度 finding

三個隔離 workers 分別保存來源 [原 mapping](agents/mapping/MAPPING.md)、
[獨立紙面推導](agents/paper/PAPER.md)、[有限控制](agents/controls/REPORT.v2.md)。
mapping 與 paper 都獨立對回 raw support 定義、原 S 身份及 q 臂各長度。
paper 先重推論證，再逐段核父端 PROOF，原審查見 [REVIEW](agents/paper/REVIEW.md)。

唯一精度 finding：獨立可重用引理也須明列正長臂 q 是 C 末端，不能只排除臂「內點」的額外邊。
主 one-W 合同原已保證此前提；最終 PROOF 將其明写，並明列 effective-H 忽略的原自由孤點
在 full-lift 接合時保留其自由因子。原受審版本保存在 [PROOF.reviewed-v1](PROOF.reviewed-v1.md)，
舊 REVIEW 未覆寫。修訂後紙面接受見 [REVIEW.final](agents/paper/REVIEW.final.md)；
其受審 bytes 另存 [PROOF.reviewed-v2](PROOF.reviewed-v2.md)。
最終僅將 controls 導航轉到修正負控制原色誤記的 REPORT.v2，
精確最終 PROOF 及本 REPORT 的接受審查見 [REVIEW.final-v2](agents/paper/REVIEW.final-v2.md)。
沒有遺留主命題內的紙面缺口；這不構成 canonical 採納。

## 最小有限控制與反例範圍

只用四張固定的具名 C（各10點12邊），沒有增加任何來源／列表域枚舉。
[證書](agents/controls/certificate.normal.json) 保完整原 G/M/C 頂點／邊、所有實際 synthetic 附件、
lists、重建 blocks／cutpoints、完整四種 C-query tuples、全部 contact fibres（含空 fibres）、
完整 M/G β lifts。四 C-query 暫不施加 s–B spokes；M/G 全圖查詢保全部原邊，兩種語義分清。

| 固定控制 | 完整 M-β lifts | coverage／界線 |
| --- | ---: | --- |
| J1 在原 a1 接 W，兩原 private witnesses 保留，S pair 保留 | 54 | `triggered and holds`：同源 degree/list 校準，β 接受 |
| J1 triangle 唯一 private x 接 W，S pair 保留 | 12 | `triggered and holds`：必要 pair-support 機制校準，β 接受 |
| J2 triangle 唯一 private w 接 W | 48 | `triggered and holds`：D-routing 校準；terminal W leaf 的三附件不滿 actual S pair |
| J1 triangle x 接 W，D 全落 W bridge，撤 actual S pair | 0 | `counterexample`：只反駁無条件 cutpoint→cycle D 傳遞；S 使用三框點 |
| actual disk、拒絕 β、完整 Σ／minimality／原合同 | 無提交 | `not triggered`；沒有新 source realization 或完整來源反例 |

前三個 synthetic M 都接受 β；第四個拒絕但違 S 的真 edge-pair support。
四者均沒有宣稱 disk embedding／rotation、完整 source Σ 或本輪完整合同成立。
負控制 exact palettes 見 PROOF§7；其完整 D fibre 為空不是 source exclusion 證據。

正常與 seed17 證書 byte-equal，均87402 bytes，SHA256
`0b2193d4d13f715272f78f3df2431aca915efd2dd77f60ef52de3549d230906a`。
checker 全重算正常／seed17 均exit0，損壞全點 coloring tuple 預期exit1；所有原代次與負控制保留。
[independent_edges.py](agents/controls/independent_edges.py) 另用固定頂點序回溯，直接由 M 原邊
重建附件／lists／全部四 queries與 M/G lifts，逐完整 tuple 集合核對，不 import 原 checker／block solver。
其 normal／seed17 重播及損壞證書負控制由 controls REPORT.v2／raw logs 保存。
controls 原 REPORT 對損壞前色值誤記0，實際是1→9；REPORT.v2只更正文字，
原 REPORT、證書及負控制均保存，沒有改寫失敗代次。
有限校準與原邊重播不承担無界量詞；無界結論由 PROOF 承担。

## authority、重播與操作邊界

[authority.json](authority.json) 凍結17份指定／直接使用的 authority files，各 exact bytes
均等於 BASE Git blobs；保存原 BR-SD-1a 89個檔案的原地 SHA256 custody。
原作者 PDF 重下載與旧 frozen PDF byte-equal；即時 Issue #4 body/comments snapshot 只讀保存。
最終 [seal-v1.json](seal-v1.json) 綁定本輪 immutable payloads；
[verify.py](verify.py) 的 frozen check 核 payloads、authority copies 與 BASE blobs，
`--live` 另核 current HEAD、authority／舊 BR-SD-1a 零漂移、Git tracked/index 零 diff及 exclusive 新輸出。
seal 只核 bytes，不決定數學結論。

從 repo root read-only 重播：

```sh
python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/verify.py --check --live
python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/independent_edges.py --certificate audits/2026-10-11-br-sd-1c-fd6e1112/agents/controls/certificate.normal.json
```

本輪執行的文件檢查見 [docs-checks](docs-checks.json)：
`python3 -B scripts/check_docs.py` exit0（600 Markdown、7353 local links）；
`python3 -B tools/docgraph --include 'docs/**/*.md' check` exit0（62 docs、213 relations、0 errors）；
`git diff --check` exit0。這些既有正式文件檢查不掃本新 audit 的 links 或驗證數學。
本 audit 的本地導航及 final custody／seal 檢查另見 [validation](validation.json)。
全工作樹 DocGraph、舊大枚舉／BR-SD-1a controls、Lean build 均未重跑。

## 文件治理與剩餘範圍

已只讀核 [DOCUMENTATION](../../docs/DOCUMENTATION.md) 及即時 [Issue #4](https://github.com/raylei50653/math/issues/4)。
本輪 user 明確限定新 audit、canonical 採納另行裁決，故執行核對並把待採納結果保存在此，
沒有為傳播規則更動共享 canonical source。

Updated：僅新 audit 的 PROOF／REPORT／MAPPING、獨立審查與必要控制。
Reviewed-unchanged：degree-5 guide§4、STATUS 的 N45／BR-SD-1a 條目、N45§1／§2.11／§3、
degree-5 interfaces§2／§7及 BR-SD-1b residual；仍描述已採1a及父域 OPEN。
採納候選1c後可加精確 one-W subset，現時不升格已採狀態。
Propagation stop：本 audit L0；L1與直接父 residual 已核，採納／canonical 傳播留 owner 裁決。
沒有一般路由或跨線語義變動，不展開 L3；document-first 足夠，未用 Graphify。

Remaining OPEN：完整 N45-S-NOU-LS-PAIR、其他 splits／split22形狀、J3／q 臂也被旁支佔用、
其他三環接線／更多旁支／一般 Gallai trees／一般非二連通來源、R31、其他45/54／55、ε≥3、
一般 N45／N2／E、一般出口及主命題。
**完整 OPEN 身份新增無條件關閉數0；沒有新 Lean theorem、actual source 或發布採納。**
