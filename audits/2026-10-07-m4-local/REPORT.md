# 2026-10-07：M4-L 正式交付整合與本地提交

任務：M4-L。範圍依[原派工](../2026-10-07-merge-supervision/M4_LOCAL.md)。
本輪整合既有 audit／監督驗收與具名例外，只作本地交付；不擴張數學結論。
受驗 U1 已由 M2 驗收，M3 計算／Lean 與兩項新增 provenance 補件由
[監督報告](../2026-10-07-merge-supervision/REPORT.md)驗收；原 strict FAIL 保留。
提交前獨立核對已完成，具名例外保持；最終提交後的獨立核對結果與 SHA
以本輪回報及該 checkout 的 Git 為準。

| 欄位 | 值與用途 |
| --- | --- |
| Input candidate SHA | `ba0b447f09617591d9f2ba81c988f537af771791`；M1／M2／M3 數學來源 |
| Candidate parent | `a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42`；不與 main base 混用 |
| Main base | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`；整分支差異基準 |
| Tested source hashes | 每次 fresh `source-comparison.json`／`tested-sources.json.gz`；原來源及最終 guide 逐欄列出 |
| 最終交付 SHA | 本輪回報或 `git rev-parse HEAD`；外層 seal 不寫入自身 commit hash |
| 數學停止點 | [Kempe 導覽](../../docs/c5_kempe_guide.md)；U2–U4 等保留 |

## 1. 正式納入與原 bytes

明確納入 M2 原 40 檔與 [DELIVERY](../2026-10-07-m2-u1-audit/DELIVERY.json)、
M3 原 264 檔與 [BUNDLE_INVENTORY](../2026-10-07-m3-fresh-checkout/BUNDLE_INVENTORY.json)、
監督原 21 檔與 [SUPERVISION_INVENTORY](../2026-10-07-merge-supervision/SUPERVISION_INVENTORY.json)。
三包共 328 檔（包含三份 manifest），原檔與 manifest 自身的大小／SHA256 均固定於
[original-bundles.json](original-bundles.json)。外層 [DELIVERY](DELIVERY.json)另外列出本輪所有
納入檔的大小／SHA256；排除自身、scratch 與執行 cache，不任意 staging 全工作樹。
原包未增刪、原 bytes／hash 保持；歷史 `/tmp` 路徑與 FAIL 不修改。

M2 原 40 檔 436,019 bytes；M3 原 264 檔 9,784,530 bytes；監督原 21 檔 327,524 bytes。
原 manifest 與 logs 是已交付歷史證據，新增命令均標為「現在重跑」。
原 M2 checker 要求 `HEAD == candidate`，原監督 verifier 要求候選 tracked tree 無更動；
它們的假設保留。整合版本使用[新 verifier](verify.py)逐項核對同一原 bytes，
不宣稱這兩個原 candidate-only helper 在最終交付 HEAD 通過。
原 M3 authoring helper 使用明示 `PYTHONPATH=<repo>/scripts`，不依賴已消失 clone。

## 2. 原證據追回與缺失界線

[追回台帳](evidence-recovery.json)列明搜尋命令、實際 exit、歷史 capture 出處、
可用副本、不可用餘項及 fresh 替代證據。
原 M1／前次監督／M3 的三個指定 `/tmp` 目錄均已不存在。
從歷史 command capture 追回下列兩份原 M1 bytes，切片與原 checksum 相符：

| 原副本 | Bytes | SHA256 |
| --- | ---: | --- |
| [M1 REPORT](recovered-original/m1/REPORT.md) | 15,412 | `88525e181ed89e1e3e28122c9bb6c3f5bc538091bf6e1fb222cdb2121c80a31a` |
| [M1 candidate TSV](recovered-original/m1/candidate-files.tsv) | 1,940 | `46b4fed4672217e4e0c31f5dc0c6a0230ad52626d71b05298a98d9e0be842e2f` |

完整 M1 的 51 檔驗證包、完整原 checksum 清單、其餘 logs／diffstat 與前次監督
完整台帳仍不可用。Recovered REPORT 內六個歷史 `/tmp` 連結仍不可用，原字句不改。
Capture 僅有 19 份完整 checksum entries 及下一份截斷項，不冒稱完整原 manifest。
監督的[新 17-blob 清單](../2026-10-07-merge-supervision/m3-review/m1-package-reconstructed.json)
與候選 immutable Git blobs 重新核對，也與原 TSV 一致；這是 fresh reconstruction／核對，
不替代未追回的原 M1 執行 logs。M3 同候選 fresh 命令與來源快照仍完整保留。

## 3. 五項 strict FAIL 與精確例外

原 29 指定命令：**28 PASS／1 FAIL**；另外四份 provenance strict FAIL，合計五項。
每次新驗證保存實際 strict exit1、source／fresh 大小與 hash、producer hash、
具名 leaf allowlist、完整 JSON differences、其餘 serialized payload 全等及
M3 fresh→最終文件版本 differences。見各次 `strict-failures.json`，不整批忽略 provenance。

| 項目 | 唯一容許的 leaves | 處置 |
| --- | --- | --- |
| C44 input audit | `/layers/6/es_source_present`；`/layers/6/es_source_hash_matches` | `false→true`、`null→true`；原 ES NA_k9 bytes 符合 expected hash。保留原 ledger 與 strict FAIL。 |
| E4 reductions（歷史） | `/sources/artifacts/c5_excess_two_e3/REPORT.md/bytes`、`/sources/artifacts/c5_excess_two_e3/REPORT.md/sha256` | E3 REPORT 原 30,573→現 32,469 bytes；原／fresh hash 明列。歷史 FAIL 保留。 |
| E5 controls（歷史） | `/source_sha256/artifacts/c5_excess_two_e3/REPORT.md` | 同一 E3 REPORT hash；歷史 FAIL 保留。 |
| E4C（歷史＋本輪 guide hash） | `/source_hashes/docs/c5_kempe_guide.md` | 最終 guide 新 hash 另存，不把 M3 fresh hash 混稱本輪重播；54 controls 逐 byte 相同。 |
| E5 branches（M3 新增） | `/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md` | 原 `a829d98e…`→候選／現 `2fe0780d…`；本輪未改此文件，與 M3 fresh 完整 bytes 一致。 |

E3 REPORT 原 hash 為 `6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659`，
現 hash 為 `73ed652a55b159a44eb6da4608f11537efc0d43603128094101ef044a96b2cd3`。
E4C guide 原 hash `bd0502e091973b50a9ec02b8f0d39716cdc3bf5cb7144d4da62df741f57d34b4`，
M3 fresh `7cbad5d926f8d92a3fa2d4c83256833713608adba15d6013d9b413dfbe8d2778`，
本輪最終 guide `ed348ba2540d2cd3e4fadb69e1d65d20429e460f42df20893b7a95fe3b3c1ae0`。
完整兩端 hash 見 fresh ledger；此段 metadata 診斷不是原 strict PASS。

## 4. Whitespace 與工作樹 DocGraph

原整分支有 **86** 項歷史 whitespace 診斷，原 raw bytes 12,380、SHA256
`2868ebd2cf8e43057913481873577faa91a9f85a2df61b408f3b8707a6bad4d3`。
M3 原 raw log 完整保留後，納入該檔本身另產生 **85** 項 trailing-whitespace 診斷；
這是本輪新增的「匯入 immutable 歷史 log」例外，不能說整份 new diff 無診斷。
逐路徑／行號分類見 fresh `whitespace.json`。不修改 vendor／原 logs 消除 FAIL。
新 authoring 檔應為 0 whitespace 診斷；candidate-parent exit0、整合 new diff exit2、
整分支 exit2 與 imported log no-index exit3 分別紀錄。
Fresh raw logs 採 deterministic gzip，保存 raw／gzip hashes 並驗 roundtrip，
不重複引入另一份原 whitespace log 的 diagnostics。

本地原工作樹預設 DocGraph **exit1：62 duplicate-id**，來源為保留的 scratch 交付 clone。
不刪 scratch，不宣稱全工作樹 DocGraph 通過。獨立 checkout 不含 scratch，
須執行預設 DocGraph，不能以排除 scratch 的自訂掃描冒稱預設通過。

## 5. LC 沿用與未跑項

原 M3 完整來源快照有 7,190 entries；本輪只有 STATUS 與 guide 原文件 bytes 改變，
其餘數學來源、producer／import closure、corpus、Lean 來源／設定／生成證書原 bytes
均逐項 hash 核對。新歷史及 audit 為新增輸出。三份原工作樹 permission 差異另列，
其 bytes 相同；獨立 Git checkout 的 mode 由 Git 還原。
[獨立完整核對](independent-integrity.json.gz)與[hash／roundtrip](independent-integrity-hashes.json)
保存原 109 份 Lean 來源／設定／生成證書 hash 核對及原 build／axiom 紀錄。

沿用 M3 顯式 `lake build Math Math.GeneratedExcessTwoCertificates Math.ExcessTwoCertificatesAudit`：
exit0、8,837 jobs、757.303 秒，stdout SHA256
`0cd75c0cc3e67a5a9ea0231e99055270b81e29e166da4c7e1190262f7ce394b1`。
原 `lake env lean -j 1 Math/ExcessTwoCertificatesAudit.lean` exit0，stdout SHA256
`dd976c7b6e533d2a88c6e8795711b7ab3a51d327e5c13aa55358ac8c86cb6c67`。
本輪 **未重跑 build 或 Lean 公理程序**；以具名 source 明示 `--source` 重解析原 log，
558 declarations 與原完整 JSON 相同、無 sorryAx、179 positive 無 native。
Rejected／valid 仍各用具名 native_decide；raw Σ 另有 S₄ cover native 信任。
M3 `.lake` cache 已不可用，沒有交付舊 `.olean` inventory，故不聲稱 `.olean` hash 相同。

本轮未重新執行無 hash 變動的全搜尋、U1／mixed／D9／C44／C44′大重播及其他研究／Lean checks；
沿用 M2／M3 原同來源證據。Guide 變動的 E4C 以及五項 strict／fresh 診斷現在重跑。
沒有新 theorem 或 source realization；有限 compatible core、未觸發 controls、
soundness 不提升為 completeness、disk topology、任意大小或一般出口定理。

## 6. 可攜驗證與正式停止點

先在新的獨立 clone 檢出欲驗 SHA；還原工具只按原 bytes 還原，不重新生成證書。
`--python` 指向已有 pinned NetworkX 3.5 等原研究依賴的 interpreter；不需要原 `/tmp` clone。
`--output` 必須是不存在的新目錄，避免覆寫任何已交付證據。

```sh
python3 tools/audit_archive.py restore --artifacts
python3 tools/audit_archive.py verify --artifacts
python3 audits/2026-10-07-m4-local/seal.py --repo "$PWD" --check
python3 audits/2026-10-07-m4-local/verify.py --repo "$PWD" \
  --source "$PWD/audits/2026-10-07-m3-fresh-checkout" \
  --python /path/to/pinned/python --output /tmp/math-m4-check-fresh --phase checkout
PYTHONPATH="$PWD/scripts" python3 audits/2026-10-07-m3-fresh-checkout/check_bundle.py
python3 audits/2026-10-07-m3-fresh-checkout/check_lean_axioms.py \
  --source "$PWD/Math/ExcessTwoCertificatesAudit.lean" \
  --log "$PWD/audits/2026-10-07-m3-fresh-checkout/logs/lean-axioms.stdout.log" \
  --output /tmp/math-m4-axioms-fresh.json
```

本地提交前要核對獨立 staged-tree checkout 的預設 DocGraph、文件／anchors／index、
新 code syntax、原 manifest／來源 hash、具名 diff 例外與 archive 還原路径。
提交後從真正最終 SHA 的独立 checkout 再驗正式包、source／fresh hashes 與入口。
具體執行 ledger／納入方式見[發布歷史](../../docs/history/2026-10-07-m4-local-delivery.md)。
新 verifier 首次 workspace 執行的 subprocess checks 完成，但終端 metadata 使用
`git write-tree` 嘗試寫唯讀 `.git/index.lock`，內部 exit128／整體 exit1；
[開發紀錄](development-run.json)與原執行碼、全部已完成 logs 保留。
更正新 verifier 為唯讀 `rev-parse`＋staged-diff hash，後續獨立 checkout 驗新版；
不把首次整體失敗改成 PASS。此開發問題未修改原來源／證書。

### 本輪實際提交前驗證

[Checkout setup](checkout-setup/commands.json)記錄 local `--no-local` clone 與 staged-tree
驗證物件 `da152db1494025f6e2c20e201102ba889868d29c`，tree
`92f5e356985d2db65a76521584978b100b726149`；此物件沒有更新主工作樹 branch ref，
不是最後交付 SHA。獨立 checkout 路徑 `/tmp/math-m4-local-independent`，不含 scratch。
[外層執行](precommit-execution/commands.json)及[完整 fresh receipt](precommit-review/verification.json)
保存實際 exit／耗時；[子命令與 raw/gzip hashes](precommit-review/commands.json)可逐項核對。

| 現在重跑項目 | 實際結果 |
| --- | --- |
| Archive restore／verify | 各 exit0；2,540 paths、1,460 unique blobs，原 bytes／hash 全符 |
| Artifact status | exit0；ok=155 |
| 三包原 manifest／來源 | 328 含 manifest 原檔均符合原 hash；7,190 原 entries 除 STATUS／guide 外無 byte 漂移 |
| 新 Python 語法 | 17 檔 AST parse，見[清單](precommit-execution/new-python-syntax.json) |
| 新正式交付 seal | exit0，當次 staged snapshot exact file set／hash；最終 seal 隨納入新紀錄更新 |
| LC 原 log 具名 source 重解析 | exit0；完整 JSON 與 M3 相同；原 build／Lean 公理程序未重跑 |
| 五項 strict 命令 | 五次 exit1，fresh 診斷全部僅具名 allowlist；54 E4C controls byte 全等 |
| 文件／anchors／index／HANDOFF | exit0；573 Markdown、6,712 local links |
| 獨立 checkout 預設 DocGraph | exit0；62 documents、213 relations、5 families；0 errors／notes |
| Candidate-parent／new diff／full branch | exit0／exit2／exit2；原 86＋匯入原 log 85，0 新 authored 診斷 |
| 更正後 portable verifier | exit0；78.147 秒，完整輸出及原數學來源在前後核對中保持 |

[Strict ledger](precommit-review/strict-failures.json)、[source hashes](precommit-review/source-comparison.json)
與[whitespace ledger](precommit-review/whitespace.json)直接列出兩端 hashes、完整差異及精確路徑／行號。
標準 docs checker 不掃 `audits/**`；本輪 audit Markdown 另逐連結／anchor 核對，
唯一六份缺失連結是追回 M1 REPORT 的已披露歷史 `/tmp` 入口。
提交前紀錄納入本地交付；真正最終 SHA 的提交後 receipt 使用新的外部 `/tmp` output，
不自引用已提交 manifest，於本輪回報列出確切 SHA、結果與 logs 位置。
停止於本地最終交付 SHA。**未 push、未建立 PR、未 CI dispatch、未 merge；不宣告可合併。**
U2–U4、其他 no-mixed core、single-root 例外、E5 新證明、三列推廣、ε≥3、
猜想 E 任意大小、一般出口及 `K∞=K≤5` 均保留。M4-R 需另輪驗收與授权。
