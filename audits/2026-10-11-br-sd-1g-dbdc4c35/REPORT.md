# BR-SD-1g：双原旁支精確排除候選交付

2026-10-11；實際研究 commit 基準 `dbdc4c35f785519c8e3cb0260807f0d2feb82469`。
起始 HEAD／origin/main／遠端 main 三者相同、工作樹乾淨。
結束前回讀仍為此基準，index 空，工作樹只新增本專屬 audit。
[START](logs/START.json) 與 [完整命令紀錄](logs/CHECKS.json) 保存實際 argv／stdout／stderr／exit。
沒有 commit、push、merge 或 canonical 採納。

**結論：在完整原來源合同下，BR-SD-1g 指定雙旁支子域有任意大小的紙面
candidate scoped exclusion。** W1 真的破壞 J1 triangle 的 private-witness 身份，
W2 的部分接點真的破壞原 terminal lemma 前提；这些失效沒有提供 actual source 反例。
新矛盾保同一原 M／β／T／D，在 S 側完整 block incidence tree 交替追色。
完整 N45-S-NOU-LS-PAIR 父身份維持 **OPEN**；**完整 OPEN 身份新增無條件關閉數為 0**。

## 1. 精確量詞、完整合同與證據入口

[PROOF§1](PROOF.md#1-完整原來源合同與固定量詞) 保留 N45 canonical §1／§2.11
及 BR-SD-1a／1c／1e 的全部原身份：同一 finite simple ordered induced-C5 disk G、
完整 Σ933／941 或共同整圖 D5 像、ε=2、逐非框邊 critical 及全部原 witnesses；
不相鄰原 degree5 r/s、其他有效原點完整度4、U=0、L long、S actual 同一真框邊 pair；
M=X=G−e、只省略 r 唯一原 B-spoke、M 自身同 proper 三色 β minimal 且拒絕及
所有 retained-edge full witnesses；M 中 s 度5其他有效點4、p/q 及 s 三 spokes 全保；
sole C、r split22、三原奇環單原 bridge、兩原可零長外臂、全部合法具名重合；
完整原邊、附件、ownership、rotation／embedding、字面色框、relations／fibres 含空及 full lifts。

形狀量詞僅為 J1 triangle `(r,a1,x1)`，任意奇長≥3的 J2/J3、任意 h/ℓ≥0，
恰兩份有限非空 connected off-skeleton 原 W1/W2，唯一接點分別是 x1 與原
`x2∈J3∪q-arm`；W1 屬完整原 L、W2 屬完整原 S，無其他接線、s-contact 或第三份旁支。
包含首接入 m1/m2=1或2、所有原 q=a3／a3=v 重合；超 degree 的位置先結構排除。
不研究其他 core、一般多旁支、R31 minor 或 ε≥3。

沒有 actual source 提交；所有 degree／attachment 列是對同一假想原候選的必要條件。
沒有向已 degree4 的舊來源增邊，沒有為旁支刪原附件。
[MAPPING](MAPPING.md) 由独立 [mapping 原稿](agents/mapping/MAPPING.review.md) 適配根層連結，
保存逐原點 ownership、全附件等式、所有臂／接點／重合及各第一矛盾。

## 2. 既有前提逐項裁決與新證明

| 路線／子型 | 完整前提稽核與裁決 |
| --- | --- |
| 1e 双 private witnesses | x1 是 C 割點、屬 J1 與 W1 首 block；J1 triangle 無替代的非割點非 s-contact witness。J2 原 witness 仍保持，因此不能直接套完整旧 1e 路線 |
| 1c terminal，x2=v／a3且 a3≠v | degree 合法時 m2=1/k=0；J3 接入位置與 off-cycle 臂鄰居前提均保持，直接由既有 terminal lemma 排除 |
| x2=a3=v | 零／正 q 臂均有 d0+t=4；非空 W2 使完整 degree≥5，第一矛盾是原度數 |
| 普通 J3 點接 W2 | 新第三接入位置違完整 terminal 前提；triangle 可耗盡唯一 J3 witness；較長環有替代點時仍可重用短證明，MAPPING§6逐列記錄 |
| 正長 q／臂內點接 W2 | 原「只有 path 鄰居」前提失效；若還保 J3 witness 且接點不在原短證明讀取的首點／末端，舊逐點矛盾仍直接保存，不列作新 OPEN |
| 其餘完整原候選 | 由下述同一 S 側 T/D 交替 incidence 矛盾排除 |

完整 lists 使用原 M **全部**鄰居：
`L^D(y)=Col−(β(N_B^M(y))∪({D} if sy∈E(M) else ∅))`。
原 `4=d_C+k+t` 給 `|L^D|≥d_C`；完整 C coloring 的存在，當且僅當同一 M 有
完整 β／s=D 延拓。ignored 原孤立座標的允許色因子也全部接回，不把投影誤寫為一對一。
M 自己拒絕 β，故連通 C 不可著色。

依 [外部 Gallai degree-list 刻畫](external/SOURCE.md)，各點完整 list 為 incident palettes
聯集、相交 blocks palettes 互斥。S actual pair 的異色為 A/B，β 第三已用色 T、未用色 D。
未改 J2 witness 在 S、有兩原 pair 附件且只屬 J2，迫 `P_J2={T,D}`。
S−q 所有 lists 都含 T/D，q 含 T、禁 D。
q 的 T-only palette 走到另一原點後須有另一份 D-only palette，反覆交替。
J2 同時含兩色，阻止此路徑退出 S 進入 L；完整 block–vertex incidence 是有限樹，
每次都不回頭，故不可能永遠延續。非割點沒有下一 block 時，當場就是缺色矛盾。
完整任意大小論證在 [PROOF§3–5](PROOF.md#3-原全部鄰居的-degree-lists-與完整延拓)。

W1 首 bridge 可合法含 D，首 odd cycle 可含 T/D，而 J1 不含 D。
第一個失效舊推論 `D∈L(x1)⇒D∈P_J1` 明示保留局部 `counterexample`；
本證明以 S 追色完成，沒有硬把 D 由割點傳回 J1，也沒有 blocks 獨立色重命名。

## 3. 獨立審查與 findings

三個 worker 分開寫 mapping／paper／controls，root 寫主證明與 custody。

| 審查入口 | finding 與處置 |
| --- | --- |
| [mapping 原稿](agents/mapping/MAPPING.review.md)、[validation](agents/mapping/MAPPING.validation.json) | 31 frozen inputs 的 size／SHA 通過；逐原點 degree／ownership／附件、J2 唯一 S 出口及 T/D 同色映射相容，無來源映射阻斷 finding |
| [paper initial](agents/paper/REVIEW.initial.md)、[proof-v1](agents/paper/REVIEW.proof-v1.md)、[最終 REVIEW](agents/paper/REVIEW.md) | 独立核 full 原合同、Gallai ≥前提、J2 barrier、finite-tree 追色、所有命名重合。首次精度 finding 是 ignored 原座標被投影後非一對一；PROOF§3 已改成存在 iff 加完整 lifts 乘積，初版 review 保留 |
| [controls REPORT](agents/controls/REPORT.md) | 最早 generation 的「應拒絕 β」assertion 錯誤，exit1／traceback保留；修正為六圖接受 β，完成重播及負輸入拒絕 |
| [custody review](agents/mapping/CUSTODY.review.md)、[final](agents/mapping/CUSTODY.final.md) | preseal manifest 不能只信可縮小的清單；verify 已固定起始兩份 manifest SHA、31/313數與 exact 三舊 audit dirs，防刪項繞過覆蓋。另固定 seal claim 及 metadata keys，避免改成超範圍宣稱。兩 findings已修正，12項隔離controls exit0；實際root seal由root執行。Custody只核bytes／紀錄，不代替紙面或重跑所有歷史commands |

最終 [ACCEPTANCE](agents/paper/ACCEPTANCE.json) 對回 PROOF／MAPPING／REPORT 的精確 hashes。
早期 review 不被冒充最終 bytes 接受；所有早期 findings／failed generations 保留。
正式採納不在本輪授權範圍。

## 4. Finite controls：量詞與触發分層

六份固定 synthetic 图均三 triangle，覆盖 p/q 零／正長、W1 佔 J1 唯一 witness、
W2 接普通 J3／v／a3／臂內點／q，以及 m2=1/2。
完整 C/M lifts 數為 `64,224,32,144,32,96`，全部 M 都接受 β，完整 compatible palettes 都為0。
另外保存各 G 同 β full lifts、每個原邊／附件及全部16個 ordered p/q fibres 含空。
primary 完整 backtracking 與独立 domain-propagation solver 重建結果相同。

| 控制命題 | 標籤與精確意義 |
| --- | --- |
| 固定圖完整 degree／synthetic actual pair／ownership、J2 witness、C/M完整延拓、有限 palette 搜尋 | `triggered and holds`，僅六份具名小圖 |
| 把 W1 接在 J1 唯一 witness仍稱其 preservation；cutpoint D ⇒ J1／每份 palette D | `counterexample`，只反駁局部保持／推論，不是 actual source |
| 任意旁支首 block 一定含 D | `counterexample`：首 bridge A、leaf cycle T/D；原 W2 點 degree4 合法，root displayed list 只为 branch-side，非完整來源 |
| 已滿 degree4 增旁支、刪原附件修 degree、錯 actual pair、a3=v 飽和 | `triggered and holds`，檢出具名第一原身份／degree矛盾 |
| 拒絕與局部度數自動給 M minimality、marginals 自動給 full lifts | `counterexample`，独立 synthetic 反例及完整 tuples 保留 |
| 完整 actual disk／Σ／逐邊 critical／原所有 witnesses／M 自身同 β minimal拒絕來源 | `not triggered`；actual target source count=0 |
| 任意大小排除、Lean、新 canonical 採納 | finite controls 不承擔；前者由紙面與獨立 review，後兩者未新增 |

normal 與 `PYTHONHASHSEED=17` 產出 certificate bytes 完全相同：
SHA256 `3d44eb24c360a22e2757bca8e29c695560420fe6f6c9766f6449ec6a7034a1a6`。
`--seed 17` 只改 search traversal metadata，排序後完整數學內容相同；不把其不同 metadata hash 說成 byte-equal。
full M tuple 損壞、malformed JSON、只刪 fibre 裡一份完整 lift 三種负輸入由 primary／independent
全部拒絕，預期與實際 exit 都1。原輸入及失败 stdout／stderr 全保留。

## 5. 修改清單、custody 與檢查入口

全部新增檔案都在 `audits/2026-10-11-br-sd-1g-dbdc4c35/`；沒有任何 tracked diff或 staged檔案。
完整 paths／sizes／modes／SHA256 由 [SEAL](SEAL.json) 的 payload 清單提供。

| 新增範圍 | 內容 |
| --- | --- |
| 根層 BASE／TASK／PROOF／MAPPING／REPORT／verify.py／seal_negative.py／SEAL.json | 精確任務、紙面、映射、分層裁決與可重播 custody／負控制入口 |
| authority/ | 31份 BASE immutable 原輸入、INPUTS.json、三舊 audits 313檔完整 OLD-CUSTODY.json |
| external/ | 凍結及 fresh-download 作者 PDF、來源版本、FETCH hash比較 |
| agents/mapping/ | 原 mapping、其輸入驗證與 custody code review |
| agents/paper/ | initial／初版精度 finding、最終独立 REVIEW／ACCEPTANCE exact hashes |
| agents/controls/ | 两 checker、完整與負证書、normal／seed17 logs、failed generations、原前版 gzip、HASHES／REPORT |
| logs/ | 起始 Git及22项实际 root commands 的 outputs／exit codes／digests |

31份 authority 每份同时比对 frozen bytes、BASE git blob 与原 live path。
三舊 audits 全部313檔核 paths／bytes／size／mode／symlink及完整目录枚舉，零 drift；
不仅核它们各自 seal 的部分 payload。外部新下載與原凍結 PDF逐 byte相同。
verify 固定起始 manifest SHA，final seal 再封存所有 payload hashes（SEAL 自己以清單 digest驗證）。
Git邊界核 tracked及未忽略 untracked；全檔 custody覆盖三舊 audit 与新 audit，
没有聲稱可追溯任意工作區 ignored檔的历史寫入。

以下命令由 root 實際重播；[CHECKS](logs/CHECKS.json) 保存22項 records。

| 實際檢查 | Exit code |
| --- | --- |
| `python3 -B audits/2026-10-11-br-sd-1a-0f181045/verify.py --check` | 0 |
| `python3 -B audits/2026-10-11-br-sd-1c-fd6e1112/verify.py --check` | 0 |
| `python3 -B audits/2026-10-11-br-sd-1e-337d018b/verify.py --check` | 0 |
| `python3 -B scripts/check_docs.py` | 0；602 Markdown／7412 links |
| `python3 -B tools/docgraph --include 'docs/**/*.md' check` | 0；62 documents／213 relations、0 errors／notes |
| `git diff --check` | 0；tracked diff空，专属未追蹤 payload另由 custody核 |
| primary normal、PYTHONHASHSEED=17及 traversal seed17；independent normal／seed17 | 全0；完整 argv在 CHECKS |
| primary／independent 各三種 corrupted certificates | 全1；預期 rejection |
| Git HEAD／origin/main／remote main、status、index回讀 | 全0；refs同BASE、只本 audit 未追踪 |

最終封存入口（从 repo 根，首次 `--seal` exclusive-create，不可覆寫）：

```sh
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/verify.py --seal
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/verify.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/verify.py --check
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/seal_negative.py
```

`--check` 完全唯讀，核 custody／精確 review hashes／22項既錄 checks及新 audit local links；
它不重新證明 Gallai、任意大小紙面定理，也不把 source finite `not triggered` 升成已觸發。
損壞 seal可用 `--check --seal-path /tmp/...json` 验负控制，不改原 seal或payload。
seal_negative 使用 memory file descriptors，逐項測試 claim／extra metadata／payload hash／
遺漏payload及再次seal的預期exit1，核seal bytes完全不變，不產生未封存的磁碟輸出。
最終 seal／normal／seed17及 seal負控制的實際 execution 結果在交付時回報。

## 6. Residual 與正式採納義務

| 身份／義務 | 本輪裁決 |
| --- | --- |
| 此§1 exact BR-SD-1g 双原旁支完整合同 | 紙面 candidate scoped exclusion；獨立 final review 对精確bytes驗收，正式採納待後續授權 |
| degree／support已違合同的分支及原 terminal前提保持配置 | 各按第一矛盾或既有局部排除記錄，不列新 OPEN |
| actual target source realization／完整來源finite驗證 | 未提交，`not triggered`；不聲稱存在或完成來源證書 |
| Lean | 沒有新增 theorem 或 build驗收 |
| 完整 N45-S-NOU-LS-PAIR、其他split22／非split22、其他三環形狀、多旁支、R31 | OPEN；此候選不關父身份 |
| 其他45／54／55、無45／54、一般 N45／N2／E、ε≥3、一般出口／主命題／K∞=K≤5 | OPEN；没有扩大範圍 |

既採 LOW／HIGH／LONG／U及1a／1c／1e均不重開，也不改其原證書、seal、负控制或失敗紀錄。
本輪精確紙面域內無剩餘 proof obligation；正式採納與上層文件傳播尚未授權，
不直接修改 N45 canonical、degree-5 guide、interfaces、STATUS 或 HANDOFF。
**父身份 OPEN；完整 OPEN 身份新增無條件關閉數＝0。**
