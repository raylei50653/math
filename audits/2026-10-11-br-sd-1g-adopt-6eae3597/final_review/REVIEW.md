# BR-SD-1g-ADOPT：最終 payload 獨立 bytes 審查

2026-10-11；reviewer `/root/proof`；固定 base／HEAD／main
`c15a635e17d4be814e19aeeeeb765f3d6024099a`。

**裁決：接受最終 audit payload bytes；ACCEPTABLE；阻斷 finding 0。**
正式採納未執行；父身份 OPEN；新增完整 OPEN 無條件關閉數 0。
本接受以最後另行生成的 [ACCEPTANCE](ACCEPTANCE.json) 完整 path／SHA／size／mode 清單為準，
不是只接受幾份摘要。Root 於 freeze 訊號後停止 payload 寫入；本 reviewer 只新增本
`final_review/`，完成本 review 及實際命令紀錄後才產生 acceptance，之後停止 payload 寫入。

## 1. 數學、原來源與量詞

已逐段核對 root [TASK](../TASK.md)、[REVIEW](../REVIEW.md)、
[MAPPING_REVIEW](../MAPPING_REVIEW.md)、[ADOPTION_DECISION](../ADOPTION_DECISION.md)、
[CANONICAL_DELTA_PROPOSAL](../CANONICAL_DELTA_PROPOSAL.md)、[REPORT](../REPORT.md) 和
[CHECKS](../CHECKS.json)，以及 proof／mapping／custody worker 原始證據。

本 reviewer 先前直接重建原證明，沒有借用原 paper REVIEW／ACCEPTANCE 的結論；
[完整獨立 proof review](../agents/proof/REVIEW.md) 的原 lists、所有鄰居、degree inequality、
完整 C／M assignments 雙射及 ignored 原坐標非空 factors、外部 Gallai 完整前提、
J2 private witness／`P_J2={T,D}`、S–L 唯一接口與有限最長 incidence path 矛盾，
與 root 最終文字一致。新證明不使用 `D∈L(x1)⇒D∈P_J1`；此失效步驟保留 counterexample。
「T-only」只指對固定 T/D pair 恰含 T，沒有偷改成 singleton palette。

提案八項保留原七項全部完整來源前提，明寫 **S short**，沒有因短證明使用較少前提而擴大量詞：
同一 finite simple ordered induced-C5 disk G、完整 Σ933／941 或整圖共同 D5 像、ε2、
G critical 與原 witnesses、非相鄰 degree5 roots／其餘有效 degree4、原 U0／L long、
actual 同一真框邊 pair、只刪 r 唯一原 spoke、M=X 自身同 β minimal 且拒絕與自己的
完整 witnesses、sole C／split22、J1 指定 triangle／任意奇長 J2/J3／唯一原 uv／兩原臂、
兩 finite nonempty connected Wi 唯一接點與原 ownership、原 degree／attachments、
所有合法零臂及 a3=v、原 rotation／具名 contacts／完整 relations／空 fibres／full lifts。
來源容量只作必要條件；沒有聲稱 source realization。
Triangle、K4、leaf block、非割點和任意有限 W2 由紙面樹論證處理；沒有從六圖推出任意大小。

N45§2.11 插入位置、§2 候選新增列與§3精確 subset 的建議保持完整合同參考和父 OPEN，
既採 1a／1c／1e 範圍保持。逐檔同步提案沒有現在執行回寫。
實際 `docs/HANDOFF.md` 是17行薄導覽，已連 degree5／Kempe guide；root 判定只更新 guide、
HANDOFF 無需改 bytes 有據，不沿用 mapping 初步「也同步」的未精查建議。

## 2. Finite controls 的獨立性及實際結果

逐行核 [fresh checker](../controls/independent_finite.py)，其只讀原 fixture 資料，
不 import 原 primary／independent checker 或 theorem code。它以 MRV 枚舉完整 assignments，
重新查原附件／lists／degree，核完整 C/M/G tuples 與全部16 ordered p/q fibres（含空），
以 BFS fundamental-cycle edge 合併重建 blocks，核全原 vertex incidence tree 和完整 palette search。
此重建不是原 Tarjan 實作的直接引用。

[新證書](../controls/CERTIFICATE.json) 保存六個具名 synthetic fixtures：
C/M counts 為64／224／32／144／32／96；它們均接受 β，完整原 source contract
`not triggered`。另有一份 fixed extended fixture 保 B-only 孤點和真正 free 孤點的原坐標，
12倍 full-lift factor／768完整 tuples，投影非雙射。
Triangle／odd-cycle5／K4 及其 incident bridge 的局部 palettes／walk，
缺 J2 barrier、額外 s-contact 及 x1 路由負控制均明標有限局部機制，
沒有被當成原 source、一般 Gallai theorem 或 Lean。

Root 原 primary／原 independent／新 independent 各三項 corrupt tuple、malformed JSON、
fibre 缺完整 lift 的負控制均保 actual exit1 和 stderr；沒有「只查 marginals」。
本 reviewer 在 freeze 後重新執行 fresh normal／seed17，均 exit0、stdout 完全相同，
證書比對 digest `21ae34afd5a76e8fdf78bb8dde6628cca49ecfd76c8de3cdec1294dc19063584`。
這些通過只校準其固定具名測例。Actual source 仍 not triggered，未新增 Lean theorem。

## 3. Custody、publication 與 command ledger

完整原160檔、publication6檔、authority31項、三份舊 audit filesystem313檔均有獨立
immutable 重核。313 是89＋115＋109個 filesystem files；其中309 tracked與4既有ignored
local-only certificates 分列，沒有把未追蹤證書稱為 published。
全工作區15743 tracked entries 的 bytes／原 symlink target／mode／index blobs 亦保持。
本 reviewer freeze 後的 independent immutable replay exit0，再確認上述範圍與完整 paths；
boundary replay 和 git diff check exit0，只存在本新 audit 未追蹤，tracked／staged diff 空。

Publication `verify.py --check --require-tracked` normal／seed17 **實際各 exit1**，
歷史 whitelist 不接受新授權目錄；原 fresh checker **實際 exit1** 因 HEAD 與歷史 BASE 不同。
Root 最終 report／decision 沒有把它們寫作 PASS。Independent adapter 的 normal／seed17 exit0
是本輪另行完整重核，不改原 checker／manifest／historical evidence。

Root CHECKS 固定21個 current command receipts（12個 exit0、9個 expected negative exit1），
另保留 precheck-v1 actual1／expected0，直到 precheck-v2 actual0／expected0 已實際產生。
原始 v1、bootstrap snapshot failures、proof 錯路徑 query、custody 313 tracked 初版失敗、
工具 snapshots／failed probes 都仍在 full payload。錯誤結果沒有被重命名成成功。
Docs602／links7412、docgraph62／relations213／errors0／notes0、git diff check 的實際 exit0
與其 receipts 相符；後者只檢 tracked diff，新 audit 的 local links／anchors／md及py尾空白
另由新 checker 逐檔驗證。

Freeze 後本 reviewer 的六項 read-only replays全部 exit0：
precheck、fresh finite normal、fresh finite seed17、independent immutable、diff check、
boundary readback。Actual argv／env／cwd／start／finish／stdout／stderr／exit和digests保留在
[RUNS](RUNS.json)，所有 stderr 空。Precheck核 tracked15743／原160／publication6／authority31／
old313及當時89條 links；此數是該命令當時實際結果，不冒充後來新增本 review 的 link總數。

## 4. 最終新工具 bytes、修復與封存設計

已讀 [原工具審查](../agents/custody/ROOT_TOOL_REVIEW.md) 與 freeze 後新增的
[ROOT_TOOL_FINAL_UPDATE](../agents/custody/ROOT_TOOL_FINAL_UPDATE.md)，再逐行核當前 root tools。
先前工具審查的舊 verify hash 與最後 delta 的新 hash 有明確區別；最後 delta 已接受
receipt digest、retained-failure／superseding v2 block 與 aggregation，
沒有把舊 code acceptance 冒充對新 bytes 的接受。

本 reviewer 接受的最終重點 hashes：

| Payload | SHA256 |
| --- | --- |
| verify.py | `be7f8e24ee350c3fdece9cdce2ca5ee9367ad5ad7712cfdc99c8a0c611efcac8` |
| record_check.py | `1e90e58f0d27b93d79dc73d8b0f81b7382224758ac5b5600ba256ba74fddfe9b` |
| aggregate_checks.py | `1cf053f33bc15fa094eb8ea1a1348bc996dada1699849bd1c1ee9d58c71ed4a6` |
| seal_negative.py | `96eac77c46d1d3a09e088216601fccf5567778745f20f54d5d8f39bb99e7d0ab` |
| ROOT_TOOL_FINAL_UPDATE.md | `9873a6b7efde8403ebb5842039b53ca5ccf221f2addb446d488a69c08a01aef6` |
| REPORT.md | `068dfd2c78c234c75332dac547abff3b5f61a9b73024c7cdf19f7c8dc5aadfc5` |
| CHECKS.json | `b96563bb44bb145d5d9b7aaf71ad9c4baec461fb426b1b8a730f3cf6b4cb73cb` |

Verifier 逐項核 full workspace、immutable adapter、actual receipts、完整 accepted inventory、
local links和完整 seal object。主 inventory 固定所有 payload path／SHA／size／mode，
只排除 SEAL／DELIVERY envelopes 與獨立固定白名單 postseal；acceptance另只排除自己。
所有 retained worker logs／old tool copies／negative probes仍在 inventory。任意 audit symlink拒絕。

Logger在執行前拒絕 stale receipt或logs、dangling output symlink、logs directory symlink／escape；
修復前後 probes保留，不把 logger collision 當數學證明。
Seal／delivery exclusive-create，envelope mode固定644；sealed check沒有本 audit 寫入。
Postseal 只能是五個具名 commands 的receipt／stdout／stderr與 reviewer readback 共16檔，
各命令 argv／env／exit0／paths及output JSON另受精確合同，不因任意 expected1而放行。
Delivery再固定 SEAL bytes與 postseal 清單；final require-delivery 不放行缺少實際資料。

最後 `seal_negative.py` 只放寬 reseal 拒絕理由為建立 DELIVERY前的
`File exists` 或 DELIVERY後的 `delivery exists before seal`；
兩者仍必須 actual exit1，並逐byte確認原 SEAL未改。這使最後封存後可重播負控制，
沒有弱化六種 altered-seal 各須特定 seal-corruption 拒絕的要求。

## 5. 精確接受與未完成義務

本最終 review 接受 root 固定後的完整 payload，沒有剩餘阻斷 finding。
[原始文檔讀取 receipts](COMMANDS.json)保留初讀及freeze後delta的实际stdout／stderr／exit。
Root report對尚未建立的 SEAL／DELIVERY／postseal 結果明寫交付門檻，而非預填成功exit；
此處沒有冒充尚未執行的封存結果。

接續只准 root 生成 prescribed SEAL／postseal紀錄、獨立 sealed-byte readback與 DELIVERY，
完成正常／seed17 final require-delivery read-only 驗證。封存前接受不代替這些後續義務。
正式採納、canonical／STATUS等回寫仍須 owner 另行批准；未 commit／push／merge。

完整 N45-S-NOU-LS-PAIR父身份和其餘split22／非split22、多旁支、其他三環／更多環、
R31、ε≥3、一般N45／N2／E與K∞=K≤5仍 OPEN。新增完整 OPEN 無條件關閉數0。
Actual source not triggered；無新增 Lean；沒有一般 closure 或 source realization。

