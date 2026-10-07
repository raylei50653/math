# 2026-10-07：M3 全新 checkout 還原與驗證

任務：M3。執行完成；**驗收狀態：待補件**。
29項指定命令全部執行，28 PASS、1 FAIL（C44 input audit）。
另重現歷史三項 byte FAIL，並發現 E5 branches 的新文件 provenance FAIL。
沒有新的數學 payload 差異或反例；候選來源、原證書保持原 bytes。

| 基準 | 完整 SHA／位置 |
| --- | --- |
| 受驗 M1 候選 | `ba0b447f09617591d9f2ba81c988f537af771791` |
| main base | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090` |
| 候選 parent | `a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42` |
| 沿用 review head | `a484d4cdaeb069702de0c40acf83bc6a05dea3b3` |
| 全新独立 clone | `/tmp/math-m3-ba0b447`，detached HEAD；無 scratch 交付 clone |
| 新交付 | 本目錄的 fresh audit files；無新 commit SHA，未 commit／push |

範圍依 [任務台帳 M3](../../docs/history/2026-10-07-merge-readiness-tasks.md)
及 [封存說明](../README.md)。本次不代替 M2 紙面稽核或 M4 最終整合／遠端驗收。

## 1. 還原、環境與来源 inventory

以 `git clone --no-local --no-checkout` 建立獨立 clone 後檢出候選。
完整命令、exit、耗時、log hash 見 [setup.json](setup.json)。所有新輸出放本目錄，
不寫入候選来源或原證書。

`restore --artifacts`、`verify --artifacts` 均 exit0：2,540 原路徑、1,460 unique blobs，
逐 byte／SHA256／大小核對通過，採 exclusive 還原，未重生成歷史產物。
`tools/artifacts.py status` exit0、ok=155。工具／封存 metadata 的 SHA256／大小見
[environment.json](environment.json)。

Python 3.14.7；C44／C44′及前序 producer 使用原報告指定 `.venv/bin/python`，
NetworkX 3.5、NumPy 2.4.3、rustworkx 0.17.1；stdlib controls 使用 python3。
Lean／mathlib 鎖定 v4.34.0-rc2；九個 package HEAD 與 manifest 相符，tracked來源乾淨。
獨立複製既有 pinned dependency sources／caches，未複製專案 `.lake/build`；
package caches不與原工作樹共用，三個 symlink 全部解析到 clone 內部。
見 [Lean 環境](lean-environment.json) 及 [symlink 核對](package-symlinks.json)。未 lake update。

前後完整來源 inventory 包含7,190個檔／symlink項、8,442,824,780 file bytes。
新增／刪除／bytes／mode／symlink target 差異全部為零；僅排除 `.git`、`.lake`、
`.venv`、`__pycache__`／pyc 執行快取。
見 [before](sources-before.json.gz)、[after](sources-after.json.gz) 與
[fresh壓縮ledger](fresh-compressions.json)。本次新 inventory 採 deterministic gzip，
保存raw／gzip SHA256與大小並逐byte roundtrip驗證；不改原封存或產物。
最終 clone 的 `git status --porcelain` 為空，HEAD仍是候選；原工作樹僅新增本audit，scratch留存。

## 2. 實際驗證

完整 argv、cwd、顯式環境、exit、秒數及raw logs／SHA256見
[validation.json](validation.json)、[命令台帳](COMMANDS.md) 和個別 `commands/` 紀錄。
嚴格 byte FAIL 不改成 PASS；所有original failure logs保留。

| 檢查 | 結果／範圍 |
| --- | --- |
| 文件 | exit0：572 Markdown、6,698 local links，anchors／index／HANDOFF通過 |
| **全新clone預設DocGraph** | exit0：62 documents、213 relations、5 families；0 errors／notes |
| checkout diff／candidate parent diff | 各exit0；新增候選更動無whitespace診斷 |
| U1 普通／seed17 | 344核心、3,498接回、34,980逐列查詢；target hits=0，逐byte通過 |
| 指定mixed verifier | fresh validation與原檔完整bytes、input hashes、counts相同 |
| D9三份controls，普通／seed17 | 六次exit0；完整輸出逐byte重播，counterexamples=0 |
| C44 input audit | **exit1**；具名metadata差異見下，不修原ledger |
| C44 small／full／full seed17／algorithm | 全exit0；full 9,644 q-orbits、104,507 core deletion witnesses；small含獨立brute gate |
| C44′ screen／two_private／independent，普通／seed17 | 六次exit0；2,416 occurrences／213 cores、125 placements；無Sigma／byte mismatch |
| LC exporter | exit0；179來源與三份輸出逐byte一致；1,597接受witness、4,271刪邊witness、193拒絕列 |
| 顯式主Lean＋LC build | exit0；8,837 jobs、757.303秒；實際command見下 |
| 顯式公理稽核 | exit0；558項、4.470秒；179 positive無native，詳見§3 |

```sh
lake build Math Math.GeneratedExcessTwoCertificates Math.ExcessTwoCertificatesAudit
lake env lean -j 1 Math/ExcessTwoCertificatesAudit.lean
```

分項完整域、判定及信任界線見 [controls](controls-summary.md)、
[C44／C44′](c44-summary.md)、[provenance](provenance-summary.md)。
D9指定三拒絕列的完整來源前提仍 **not triggered**：E4 0/54、E5 0/63、
E6 0/9 source orbits／0/90 transports。已觸發控制維持 `triggered and holds`，
無 `counterexample`；未觸發項不算來源前提驗證。
C44′ compatible core不構造完整933／941來源。

## 3. LC公理與形式化界線

[實際公理結果](lean-axioms-summary.json) 與source中558個 `#print axioms` 名稱／順序逐一對帳，
無sorryAx；179 positive無native公理。
179 rejected及179 valid各依賴其具名rejected的一個 `native_decide` 公理；
S₄ color orbit cover另有一個既有native公理。
Aggregate `all_certificates_valid`有179 native、`all_certificates_sound`有180 native。
Build與獨立公理命令依序執行，沒有另一writer共寫本clone `.olean`。

LC結論限具名literal graphs的soundness、完整關係／刪邊witness及組合rotation／Euler條件，
不證枚舉completeness、軌道互異、任意大小化約或拓撲disk theorem。
LC仍為顯式local target，未接入Math.lean／預設CI，本次沒有遠端LC CI證據。

[Helper控制](axiom-helper-controls-v3.md)使用Oct05舊log，與本次fresh LC log分開。
初版控制harness轉義錯誤及parser誤計aggregate valid均保存；修正後完整基準通過，
缺项／重複／sorryAx／positive native／foreign native負控全拒絕。
Helper不解析額外error文字，正式驗收同時要求上面Lean命令exit0。

## 4. Findings與待補件

**M3-C44-INPUT-AUDIT-001：還原觸發來源存在metadata差異。**
`layers[6]`（NA k9）只有兩個serialized leaves不同：`es_source_present` false→true、
`es_source_hash_matches` null→true。還原檔 `NA_k9_validate.json` 實際SHA256為
`0b08675df72ecd21415d8fb54df567fc2daa7b802df9bc22c97f4cd6f89dc9bb`，符合原預期。
其他serialized欄位相同；見 [C44 finding](c44-summary.md#finding-m3-c44-input-audit-001)。
所需補件：M4列為本候選新增的具名presence／provenance例外及驗收處置，
維持原ledger與本次strict FAIL，不把重算metadata當歷史證書替換。

**M3-PROV-E5-BRANCHES：新文件hash漂移。**
嚴格 `c5_excess_two_e5_branches.py --check` exit1，完整fresh JSON唯一差異為
`/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md`，
`a829d98ebf84a952445e9aebb443cca1b8e0d7129ceaf1a5353b51379f059061`→
`2fe0780d75175f1ccee38a20939eb29f89048a67a82c07fb20afb59ac7680136`。
數學payload全等；[provenance結果](provenance-summary.json)保存精確leaf allowlist与兩端hash。
所需補件：M4獨立列入本候選例外，不擴寫Oct05原三FAIL紀錄，不覆寫原branches證書。

**歷史E4／E5 controls／E4C FAIL保留。** E4差原E3 REPORT bytes/hash、
E5 controls差該REPORT hash、E4C差guide hash；現版guide新增hash值另如實保存。
Fresh比較只容許具名葉差異，其他完整JSON全等，54份E4C controls逐byte相同。
沒有整批忽略provenance；歷史byte FAIL與數學payload相同是兩個不同結論。

**Whitespace：** 相對main整分支 `git diff --check` exit2，原86項vendor／原log診斷
逐byte重現，0新項。原diagnostic raw SHA256仍為
`2868ebd2cf8e43057913481873577faa91a9f85a2df61b408f3b8707a6bad4d3`。
精確六路徑／行號與來源hash見 [whitespace-comparison.json](whitespace-comparison.json)；
candidate parent更動另查exit0，不把新診斷混入舊86項。

## 5. 沿用、未跑與停止點

[依賴inventory](dependency-inventory-v2.json)核對665項，663與Oct05 review一致，
僅guide與mixed-spokes文件改變，受影響E4C／E5 branches已針對重播。
每一來源、producer、local import closure及有限corpus列出實際bytes／SHA256和基準理由。
ES full／seed17搜尋、ES acceptance、ER full／seed17、E3四checkers、E4 control、
E5 local、E6三producer、K′、D8未重跑，沿用同hash原有限證據。
E1／E2／D7、C-W／D6、舊A／B／C、R系列與其他模組獨立公理稽核未重做。

沒有M2新紙面結論、k擴張、source realization或一般定理證明。
U2–U4、其他no-mixed core／single-root例外、E5要求的新證明、三列推廣、ε≥3、
猜想E任意大小、一般出口及K∞=K≤5維持保留。

停止於fresh驗證包與具名findings，待M2／M3驗收後由M4處理例外與最終交付。
未commit／push／建立PR／觸發CI／merge。原scratch交付資料留存；
`/tmp/math-m3-ba0b447` clone／獨立Lean caches及helper controls亦留存，可供核驗。
交付檔案清單與bytes／SHA256見 [BUNDLE_INVENTORY.json](BUNDLE_INVENTORY.json)；
該清單不納入自身hash，避免self-reference。所有交付檔小於1,000,000 bytes。
