# M1：本地交付包與候選凍結回報

任務：M1。狀態：完成本地交付，待使用者驗收。2026-10-07。

候選完整 SHA：`ba0b447f09617591d9f2ba81c988f537af771791`。分支：`integrate-kprime-e3`。
base（本地 `origin/main`，且為 merge-base）：`2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`。
直接 parent／接手 HEAD：`a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42`。
候選 tree：`d30db40215a2abaf154c51363ae4f0471427bfa4`。
本地遠端追蹤 ref `origin/integrate-kprime-e3`：`1d026ee949d07a5b20bd60ec2f1e6d4329341cdf`；候選較其 ahead 13。

已建立一個本地提交；未 push、未建立 PR、未執行 merge。M2／M3／M4未啟動。
17個交付檔案依任務單以明確路徑 staging；保留接手時全部原 bytes，沒有改寫來源、報告、生成器或歷史產物。
任務台帳中的初始狀態與「未 commit」保留其建立當時語境；本份回報記錄此次M1執行結果。
本驗證回報及logs保存在本地 `/tmp`，不屬候選提交；候選本體可直接由完整SHA檢出。

**範圍及證據層。** 交付現有C44″更正、唯一mixed指定稽核，以及完整Σ=933／941或整圖D₅像的ε=2相鄰no-mixed兩-root44身份U1排除。
U1仍是指定前提下的紙面化約＋固定必要域Python證書；本次整理不構成M2獨立紙面稽核或M3新checkout驗收。
上游Gallai／degree-list分類及有限拓撲／NetworkX信任界線保留。沒有新增Lean定理、來源實現構造或一般定理。
U2–U4、no-mixed其他core、單-root例外、(4,5)/(5,4)/(5,5)、E5新證明、三列推廣、ε≥3、猜想E任意大小、一般出口與K∞=K≤5均保留。

**納入檔案。** 8份既有tracked修訂＋9份新檔；17份候選blob均與接手bytes及下表hash／大小一致。

| 狀態 | 路徑 | bytes | SHA256 |
| --- | --- | ---: | --- |
| M | [README.md](/home/ray/developer/ai/math/README.md) | 10411 | `55acccaf6a80d6d0f1710d1316cd836f4372ffb583421beb4b3ec3bf8dd31d1c` |
| M | [artifacts/c5_excess_two_c44pp/REPORT.md](/home/ray/developer/ai/math/artifacts/c5_excess_two_c44pp/REPORT.md) | 21727 | `6baa1dff6f1a280b5e05c272b9f16a46b38a16f026ab969288281e8e5d891179` |
| A | [artifacts/c5_excess_two_no_mixed_core44/observations.json](/home/ray/developer/ai/math/artifacts/c5_excess_two_no_mixed_core44/observations.json) | 992965 | `e2b74cc9516d2131b1ad53e98558d4a0131172a5d98e3fd828814ede9a795097` |
| A | [audits/2026-10-07-c44pp-mixed-audit/REPORT.md](/home/ray/developer/ai/math/audits/2026-10-07-c44pp-mixed-audit/REPORT.md) | 7433 | `81b83315dde45b8add60f4c70caec5eef84a206f20351cbc4969b8899ef55636` |
| A | [audits/2026-10-07-c44pp-mixed-audit/validation.json](/home/ray/developer/ai/math/audits/2026-10-07-c44pp-mixed-audit/validation.json) | 6858 | `08b7ec78ca8d2a3527b6adfb55312c2a48614410aedbc9a39d0b7c341376a50b` |
| A | [audits/2026-10-07-c44pp-mixed-audit/verify.py](/home/ray/developer/ai/math/audits/2026-10-07-c44pp-mixed-audit/verify.py) | 26691 | `7a1329bd3f5c6ee79735a5954fd15dc30434d7e3ca07ec30fed7cad65d82824e` |
| M | [docs/STATUS.md](/home/ray/developer/ai/math/docs/STATUS.md) | 131682 | `2f1fa35c5df2d62695b307dc2e4494b92f6508b4465b783a7910753f3ddadb6f` |
| M | [docs/c5_excess_two_mixed_core_spoke_unary.md](/home/ray/developer/ai/math/docs/c5_excess_two_mixed_core_spoke_unary.md) | 11957 | `2ec389e9f58669d84dbd7308018c3770956af588a42954b3b1844f804da4ed7a` |
| M | [docs/c5_excess_two_mixed_core_spokes.md](/home/ray/developer/ai/math/docs/c5_excess_two_mixed_core_spokes.md) | 13065 | `2fe0780d75175f1ccee38a20939eb29f89048a67a82c07fb20afb59ac7680136` |
| M | [docs/c5_excess_two_mixed_core_two_unary.md](/home/ray/developer/ai/math/docs/c5_excess_two_mixed_core_two_unary.md) | 13056 | `f7378979203061ac5743af1d962d12fbe61a8ffbcd37aaa1a3b206ee6bc95c3c` |
| M | [docs/c5_excess_two_mixed_omission.md](/home/ray/developer/ai/math/docs/c5_excess_two_mixed_omission.md) | 13620 | `27a974285e24ef8fe300b42a76cd35c6b835bb97a46a6cc5218a4d01008598d3` |
| A | [docs/c5_excess_two_no_mixed_core44.md](/home/ray/developer/ai/math/docs/c5_excess_two_no_mixed_core44.md) | 8880 | `ab3dcd2ff66ec3a2508f91d74991d8f04fa7f9446c2addf5430d5e1b5f798dab` |
| M | [docs/c5_kempe_guide.md](/home/ray/developer/ai/math/docs/c5_kempe_guide.md) | 38140 | `7cbad5d926f8d92a3fa2d4c83256833713608adba15d6013d9b413dfbe8d2778` |
| A | [docs/history/2026-10-07-c44pp-integration-review.md](/home/ray/developer/ai/math/docs/history/2026-10-07-c44pp-integration-review.md) | 4753 | `660592e2d2d2b80ce5cea74fcfb833bb61378ba1232cb16c24ac59d0b8039b0e` |
| A | [docs/history/2026-10-07-merge-readiness-tasks.md](/home/ray/developer/ai/math/docs/history/2026-10-07-merge-readiness-tasks.md) | 10543 | `d2c1d612fb9549faa409b2dc89728f71c86ed66428900b6cf532057fbbbcf290` |
| A | [docs/history/2026-10-07-no-mixed-core44.md](/home/ray/developer/ai/math/docs/history/2026-10-07-no-mixed-core44.md) | 3912 | `4e7f611b356e03eafe79358336dc4146e4f19f90a3d0e9bf153bf854555c6602` |
| A | [scripts/c5_excess_two_no_mixed_core44.py](/home/ray/developer/ai/math/scripts/c5_excess_two_no_mixed_core44.py) | 7222 | `f5534863c0fa6779cd00f9cb304d8a3565cbaed239e7f1eb7276b356b0ceadc1` |

U1 `observations.json`：992,965 bytes，低於`tools/artifacts.py`的1,000,000 bytes門檻；直接納入Git，未變更MANIFEST或.gitignore。

**來源inventory。** mixed validation的19份唯一依賴、verifier及U1 checker合計21項；與原記錄hash完全相符，且M1前後零byte漂移。
其中U1的兩份來源為原mixed_omission artifact及新增U1 checker；前者亦包含於mixed依賴。
下表「tracked」只指候選Git tree；未追蹤的大型原artifact本次讀取本地已存在bytes，封存還原留待M3。

| 來源 | bytes | SHA256 | tracked |
| --- | ---: | --- | --- |
| [artifacts/c5_excess_two_mixed_core_spoke_unary/observations.json](/home/ray/developer/ai/math/artifacts/c5_excess_two_mixed_core_spoke_unary/observations.json) | 189362323 | `79f83e8191f865a7264f977c2e743220756c0fe26fe6c9f4626d44ec289c1ef6` | no |
| [artifacts/c5_excess_two_mixed_core_spokes/observations.json](/home/ray/developer/ai/math/artifacts/c5_excess_two_mixed_core_spokes/observations.json) | 113696727 | `0ae4dee743d75d2a0b74650204ff2fa730fd45010f0fd3f295796460d564283f` | no |
| [artifacts/c5_excess_two_mixed_core_two_unary/observations.json](/home/ray/developer/ai/math/artifacts/c5_excess_two_mixed_core_two_unary/observations.json) | 107665331 | `69ff8d64ea254498f5e38bc2cf49c6b9b66fe39a1ec5d8a9c25db2ef6b402a8d` | no |
| [artifacts/c5_excess_two_mixed_omission/observations.json](/home/ray/developer/ai/math/artifacts/c5_excess_two_mixed_omission/observations.json) | 56106614 | `ded2ff09f1fba01426d801bfda0d975e9c52b5e89554538d9d963f5656db98cc` | no |
| [artifacts/c5_odd_join_cores/observations.json](/home/ray/developer/ai/math/artifacts/c5_odd_join_cores/observations.json) | 870869 | `f0e9727fea16b39baff3ff885bdb060296b4b0920048e567751a5f7831d899e2` | yes |
| [artifacts/c5_tree_cores/observations.json](/home/ray/developer/ai/math/artifacts/c5_tree_cores/observations.json) | 8668398 | `a6e80eb52b27c004856323a93be9b2f816789a66951d273a1778870777c70ba0` | no |
| [artifacts/c5_triangle_branches/observations.json](/home/ray/developer/ai/math/artifacts/c5_triangle_branches/observations.json) | 165867 | `8cfa0382908cb2ab81b177fcbf81a3ca62f4ad4163a206db5be5f4325a700e3f` | yes |
| [artifacts/c5_triangle_path_reduction/observations.json](/home/ray/developer/ai/math/artifacts/c5_triangle_path_reduction/observations.json) | 414223 | `2689b6fc7e08d91c4ea1ff112b801f50dbcbaffa98f42aad3924360bde897c7e` | yes |
| [artifacts/c5_two_triangle_blocks/observations.json](/home/ray/developer/ai/math/artifacts/c5_two_triangle_blocks/observations.json) | 1058824 | `b7181f8e2c926d00118f46643cc51b97e004a271b217975ae449dba01eb1702b` | no |
| [audits/2026-10-07-c44pp-mixed-audit/verify.py](/home/ray/developer/ai/math/audits/2026-10-07-c44pp-mixed-audit/verify.py) | 26691 | `7a1329bd3f5c6ee79735a5954fd15dc30434d7e3ca07ec30fed7cad65d82824e` | yes |
| [scripts/c5_941_three_spoke.py](/home/ray/developer/ai/math/scripts/c5_941_three_spoke.py) | 10702 | `32c9456ea70278a0df74960e4a042bad7b325ba00db17bc17149c7dcb8198dc8` | yes |
| [scripts/c5_941_two_spoke.py](/home/ray/developer/ai/math/scripts/c5_941_two_spoke.py) | 15359 | `6fff4d1d66ae7e43adaf9170387aead624baf284ff733dc7c360237e35419e0b` | yes |
| [scripts/c5_excess_two_mixed_core_spoke_unary.py](/home/ray/developer/ai/math/scripts/c5_excess_two_mixed_core_spoke_unary.py) | 26095 | `79b034fb125e8a450b2285fe44163d9445708bee1bf39259de09daf3b51b05ec` | yes |
| [scripts/c5_excess_two_mixed_core_spokes.py](/home/ray/developer/ai/math/scripts/c5_excess_two_mixed_core_spokes.py) | 22306 | `42e0406ef944d100346ff0b1a2316a8b8995ccf0a14d48c41e343ed26f44295c` | yes |
| [scripts/c5_excess_two_mixed_core_two_unary.py](/home/ray/developer/ai/math/scripts/c5_excess_two_mixed_core_two_unary.py) | 25715 | `691051425da07af8c95e98b1c35e97c9830a9d5b27b3d427c6e01e3e9e0e8964` | yes |
| [scripts/c5_excess_two_mixed_omission.py](/home/ray/developer/ai/math/scripts/c5_excess_two_mixed_omission.py) | 34135 | `6f43b60aff7e2521ae2aca3bfa28d7f2667283c31ccff126d5d969dfad4432a4` | yes |
| [scripts/c5_excess_two_no_mixed_core44.py](/home/ray/developer/ai/math/scripts/c5_excess_two_no_mixed_core44.py) | 7222 | `f5534863c0fa6779cd00f9cb304d8a3565cbaed239e7f1eb7276b356b0ceadc1` | yes |
| [scripts/c5_excess_two_path_edge.py](/home/ray/developer/ai/math/scripts/c5_excess_two_path_edge.py) | 11575 | `9df1411e75619d2ab185a8ea1767a0bab895ac0463157fed99aaea6b9914bc43` | yes |
| [scripts/c5_excess_two_triangle_edge.py](/home/ray/developer/ai/math/scripts/c5_excess_two_triangle_edge.py) | 22044 | `ba11313b8a10c429fccccacce5adf76ebe7562a372316a56a3d8f5010b738572` | yes |
| [scripts/c5_independent_support_capacity.py](/home/ray/developer/ai/math/scripts/c5_independent_support_capacity.py) | 12297 | `272b8acfd02fc2a4b807b253cc290d254f809f788ac37b55a8e0094566647d4a` | yes |
| [scripts/c5_odd_join_cores.py](/home/ray/developer/ai/math/scripts/c5_odd_join_cores.py) | 13126 | `182c47543113ede6916593446b7c58646ec34f406c7fbfded22b3ee0919aeedb` | yes |

**Diffstat。**

本次候選相對parent：17 files changed, 1424 insertions(+), 31 deletions(-)。
候選相對base main：1047 files changed, 1830825 insertions(+), 70 deletions(-)。此數字含分支前序既有成果，並非全部都是本次M1新增。
完整逐檔main diffstat：[main-diffstat.txt](/tmp/math-m1-2026-10-07-t05hjm31/main-diffstat.txt)；本次提交：[candidate-diffstat.txt](/tmp/math-m1-2026-10-07-t05hjm31/candidate-diffstat.txt)。

**實際檢查。**

| 命令／檢查 | exit | 結果／限制 |
| --- | ---: | --- |
| `python3 scripts/check_docs.py` | 0 | 572 Markdown、6698 local links；anchors／index／HANDOFF通過 |
| `python3 tools/artifacts.py status` | 0 | `ok=155`；未rebuild或record |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | 0 | 62 documents／213 relations／5 families、0 errors |
| `python3 tools/docgraph check` | 1 | 62 duplicate-id，全部來自`docs/`與`scratch/task-c44-delivery/repository/docs/`的既有副本；維持FAIL，未刪原scratch |
| `python3 scripts/c5_excess_two_no_mixed_core44.py --check` | 0 | 344 cores／3498 restorations／34980 independent row checks／target_hits=0；与原證書bytes一致 |
| 標準函式庫檢查17檔尾空白／末尾LF，2 Python ast.parse＋compile，2 JSON parse | 0 | PASS，未執行新Python模組、未寫入cache |
| 原記錄source_sha256／input_sha256與實際來源比對 | 0 | 21項全部相符 |
| `git diff --cached --check` | 0 | staging後全17檔PASS，涵蓋全部9新增檔 |
| `git diff --check` | 0 | staging後沒有tracked未納入差異；接手差異已保存 |
| `git show --format= --check HEAD` | 0 | 候選提交patch whitespace PASS |
| 提交後候選blob／工作樹bytes／原input及受保護檔核對 | 0 | 17 blobs、21 sources、5 protected files零byte漂移 |
| excluded scratch inventory核對 | 0 | 11192 files、路徑及大小零漂移；未宣稱全部scratch逐byte hash稽核 |

U1四類域仍為160／64／56／64 cores及1440／576／458／1024 restorations；未縮減完整域或把子型重播當全域。
全部命令、exit、耗時、stdout／stderr路徑與SHA256見[checks.json](/tmp/math-m1-2026-10-07-t05hjm31/checks.json)。
語法／whitespace細目見[syntax-whitespace.json](/tmp/math-m1-2026-10-07-t05hjm31/syntax-whitespace.json)；提交前後核對見[candidate-verification.json](/tmp/math-m1-2026-10-07-t05hjm31/candidate-verification.json)。

**未跑項與沿用理由。**

- 未跑U1 seed17、mixed verifier重播、D9 controls、C44／C44′重播及LC exporter；M1只凍結既有交付，這些已由任務单明列給M3。普通U1只作M1必要域與既有bytes一致性的本地重播。
- 未做全新checkout、audit_archive restore／verify、lake build、顯式LC target或#print axioms；均留待M3，未把本次文件／PythonPASS當Lean或還原PASS。
- 未重跑ES／ER搜尋、前序E3–E6、上游拓撲枚舉或四個mixed原producer；不開新研究輪。歷史E4／E5／E4C byte FAIL保持原記錄，不作本次PASS。
- 未重驗整分支whitespace；本次只驗17檔staged diff與候選提交patch。全分支vendor／歷史logs診斷仍由M3另查，不沿用未執行的例外結論。
- 未刷新PR／CI或GitHub保護規則；M1沒有遠端驗收。

**未納入資料及保留狀態。**

| 路徑 | 檔案數 | bytes（含子目錄） |
| --- | ---: | ---: |
| `scratch/er` | 1 | 308784 |
| `scratch/task-c44-delivery/repository` | 11189 | 489123056 |
| `scratch/task-c44-delivery/delivery.json` | 1 | 939 |
| `scratch/task-c44-delivery/task-c44-cores.bundle` | 1 | 421658 |
| `audits/2026-10-07-c44pp-mixed-audit/__pycache__/verify.cpython-314.pyc`（ignored） | 1 | 53878 |

完整逐檔excluded inventory：[excluded-scratch-inventory.tsv](/tmp/math-m1-2026-10-07-t05hjm31/excluded-scratch-inventory.tsv)。
Scratch資料全部保留；已排除clone、bundle、交付暫存與plantri可執行檔。新驗證輸出只寫`/tmp`，未納入候選。
HANDOFF、DOCUMENTATION、.gitignore、artifacts/MANIFEST.json、audits/ARCHIVE.json均維持接手hash。
候選完成後tracked工作樹乾淨、staging空；`git status --short --branch`僅列ahead13及`?? scratch/`，不宣稱全工作樹clean。

**findings及即時遠端限制。** 指定交付範圍未發現M1阻斷，未執行M2任意大小論證独立稽核。
正式docs的DocGraph PASS與全工作樹的62 duplicate-id FAIL分開；fresh checkout的預設DocGraph仍須由M3驗收。
21項原source hashes相符、候選17檔與input零byte漂移；未改寫歷史provenance失敗。未在M1重新判定D9控制的trigger分類。
只讀`git ls-remote origin refs/heads/main refs/heads/integrate-kprime-e3` exit128：環境DNS無法解析github.com。
因此上面main與tracking SHA是本地已存在refs，與任務單接手SHA相同；未聲稱本次確認即時遠端HEAD或CI。此限制不影響M1本地候選凍結。
Sandbox對.git原為read-only，首次git add exit128；依已授權M1經escalation成功完成明確17路徑git add與git commit。未收到auto-review拒絕。

**下一個驗收入口。** M2／M3可由本候選完整SHA建立各自獨立checkout；本次停止於M1本地交付。
