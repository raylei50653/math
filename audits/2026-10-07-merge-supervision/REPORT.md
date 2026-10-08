# 2026-10-07：M3監督補件與M4派工

受驗候選：`ba0b447f09617591d9f2ba81c988f537af771791`。
main基準：`2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090`。
直接parent：`a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42`。

**監督判定：M3計算／Lean證據及兩項新增provenance診斷已驗收，附明列byte例外。**
原[M3報告](../2026-10-07-m3-fresh-checkout/REPORT.md)的「待補件」保留其交付語境，
原29項指定命令仍為28 PASS／1 FAIL；另有四份provenance strict FAIL。
本補件不把任何原FAIL轉為PASS，也不宣稱所有strict checks均通過。
M1／M2依本對話前次驗收仍為已驗收；M4本地整合可啟動，最終可合併判定仍待M4。

## 本輪獨立核對

[監督重播程式](verify_m3.py)只新增fresh輸出，未更動候選、原產物或M2／M3交付。
結果見[review.json](m3-review/review.json)，實際命令、預期exit及logs見
[commands.json](m3-review/commands.json)。

| 核對 | 結果／限度 |
| --- | --- |
| M3原manifest | 264份檔案、9784530 bytes均符合原hash；seal檢查PASS |
| 原命令／logs | 57份command records、114份raw logs符合hash；29項指定判定與原records一致 |
| fresh來源快照 | 7190份前後entries全同；gzip／raw hash、零增刪／變動均吻合 |
| 候選Git blobs | 4650份tracked檔／symlink與fresh快照一致；目前tracked工作樹未改 |
| LC公理 | 重新解析原fresh log，558項與具名source對帳；無sorryAx、179 positive無native，結果完整JSON與M3摘要相同 |
| LC build | 採認已驗hash的顯式build exit0／8837 jobs紀錄；監督端未重跑757秒build |
| C44 input audit | 新目錄獨立in-memory重算，僅兩個presence leaves不同；原strict FAIL亦重現 |
| E5 branches | 新目錄獨立in-memory重算，與M3 fresh完整bytes一致；僅一個文件hash不同；原strict FAIL亦重現 |
| 歷史provenance | E4／E5 controls／E4C完整JSON各只差原明列leaf；54份E4C控制逐byte相同 |
| 歷史whitespace | 原86項diagnostics raw bytes相同；未修vendor或原logs |
| audit authoring | 以明示PYTHONPATH執行原M3 bundle檢查PASS，不依賴消失的/tmp clone |

公理拒絕／valid仍含具名native_decide，rawΣ另含S₄ cover的native信任。
本補件不證搜尋completeness、拓撲disk、任意大小定理或來源實現。

## 兩項新增例外的驗收處置

| finding | 完整差異 | 處置 |
| --- | --- | --- |
| M3-C44-INPUT-AUDIT-001 | `/layers/6/es_source_present`: false→true；`/layers/6/es_source_hash_matches`: null→true | 原ES NA_k9還原檔SHA符合預期；其餘serialized欄位全等。接受為還原造成的具名presence例外，保留原input_audit與strict FAIL。 |
| M3-PROV-E5-BRANCHES | `/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md`的原／現hash不同 | 現文件hash與候選Git blob一致，完整fresh payload其餘欄位全等。接受為單份文件provenance例外，保留原branches及strict FAIL，與舊三FAIL分列。 |

精確兩端hash、全JSON差異與處置在review.json；重算檔分別為
[C44](m3-review/c44-recomputed.json)、[E5 branches](m3-review/e5-branches-recomputed.json)。
只有完全符合該具名leaf集合的差異可沿用此判定；M4增加其他差異時必須重新診斷。
原來源存在／不存在的歷史狀態不以現在重算metadata改寫。

## /tmp證據留存與可攜性

本輪確認以下原路徑現在不可用：

- `/tmp/math-m1-2026-10-07-t05hjm31`：M1原回報及logs。
- `/tmp/math-merge-supervision-2026-10-07-cai23oac`：前次M1／M2監督台帳及重播輸出。
- `/tmp/math-m3-ba0b447`：M3執行時的獨立clone／Lean caches。

M2及M3正式audit包仍完整留在workspace；M3原logs及來源快照已核驗，
clone消失不改變已交付logs的結果，但不能宣稱現在仍能打開該clone／cache。
M1候選17檔已从immutable Git重建[新清單](m3-review/m1-package-reconstructed.json)，
這是fresh reconstruction，不是恢復原M1回報或51份歷史驗證檔。
M4須先查是否有原證據副本；若沒有，就記錄「原暫存不可用」，引用M3同候選fresh證據
及新的逐blob核對，不能捏造舊logs或宣稱原完整包已封存。

原M3 helper有執行當時的absolute/tmp路徑。原bytes保留；本輪以
`PYTHONPATH=<repo>/scripts`執行check_bundle，以顯式`--source`重驗axioms。
正式新驗證入口應用顯式repo／source／output參數，不修改舊命令的cwd歷史。

本輪可重播入口，output必須是尚不存在的新目錄：

```sh
PYTHONDONTWRITEBYTECODE=1 python3 audits/2026-10-07-merge-supervision/verify_m3.py \
  --repo /home/ray/developer/ai/math \
  --output /tmp/math-m3-supervisor-fresh-output
```

repo必須檢出受驗候選SHA，並有原已還原輸入與M3交付包；此命令不重跑Lean。
候選來源／前提變更後，本判定不能當作新版本已驗收。

## 管理狀態與下一步

| 任務 | 監督狀態 |
| --- | --- |
| M1 | 已驗收本地候選交付；原/tmp驗證包目前不可用，正式包留存由M4處置 |
| M2 | 前次已驗收；指定前提紙面與完整必要域有限證書，上游信任保留 |
| M3 | 本補件驗收完成，附兩项新增byte例外及歷史FAIL；不是全strict PASS |
| M4-L | 可發布：[本地整合任務](M4_LOCAL.md) |
| M4-R | 等M4-L驗收：[遠端發布／PR／CI任務](M4_REMOTE.md) |

本輪未commit／push／建立PR／觸發CI／merge。未修改tracked候選或M2／M3原包。
