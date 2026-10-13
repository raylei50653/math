# 2026-10-07：M4-L audit 整合與本地交付

本輪依 [M4-L 派工](../../audits/2026-10-07-merge-supervision/M4_LOCAL.md)，
整合 M2／M3 與監督補件，限定本地提交。
完整例外、追回證據、來源 hash、portable 命令與未跑項見
[M4-L 報告](../../audits/2026-10-07-m4-local/REPORT.md)。
現行數學停止點維持 [Kempe 導覽](../c5_kempe_guide.md)，
沒有新的研究線或結論，HANDOFF 與 README 不作逐輪修改。

| 欄位 | 內容 |
| --- | --- |
| 受驗候選 | `ba0b447f09617591d9f2ba81c988f537af771791` |
| 候選 parent | `a1ca89db9c04c6e65ba0b1cb0928df9e8c163e42` |
| main 基準 | `2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090` |
| Tested source hashes | Fresh `source-comparison.json` 與 `tested-sources.json.gz`，不以最終 commit SHA 代替原來源 hash |
| 最終交付 SHA | 本轮回報及即時 `git rev-parse HEAD`；manifest 不自引用 commit hash |
| 外層交付清單 | [DELIVERY](../../audits/2026-10-07-m4-local/DELIVERY.json)，包括原三 manifest 自身 |

原 M2 40＋DELIVERY、M3 264＋inventory、監督 21＋inventory 共 328 檔按原 bytes 纳入。
原 29 指定 checks 維持 28 PASS／1 FAIL；另四 provenance strict FAIL，五項各限具名
leaf 診斷。新 guide wording 引起 E4C hash 再漂移，必须用本輪 fresh 輸出單獨核對。
原 86 whitespace 與新增匯入歷史 raw log 的 85 診斷分開，原 bytes 不改。
工作樹 scratch 造成的預設 DocGraph 62 duplicate-id 保留為工作樹限度；
正式 scratch-free 獨立 checkout 才能驗預設 DocGraph。

原 M1 REPORT／candidate TSV 兩份追回並核對原 checksum；其餘原 M1 51 檔包、
前次監督台帳與原 M3 cache 不可用。17 immutable candidate blobs 的新清單
及 M3 同候選 fresh 記錄均另以 fresh 核對標示，不冒充原缺失 logs。
原数学／Lean source、設定與生成證書未改，沿用 M3 build／558 公理原 logs；
本輪只重新解析具名公理 log，未重新 build，未比較不存在的原 `.olean` inventory。

提交前獨立 staged-tree checkout 驗證物件為 `da152db1494025f6e2c20e201102ba889868d29c`，
不是 final delivery SHA；archive restore／verify、17 份新 Python syntax、文件與
預設 DocGraph 均通過。更正後 portable verifier exit0；五份 strict FAIL 與
171 whitespace 的具名例外原樣保存，0 新 authored 診斷。
Actual argv／exit／raw 與 gzip hashes 見[執行紀錄](../../audits/2026-10-07-m4-local/precommit-execution/commands.json)
與[完整驗證](../../audits/2026-10-07-m4-local/precommit-review/verification.json)。
首次 workspace wrapper 的唯讀 Git metadata 開發失敗仍保存；最終 verifier 使用唯讀 metadata。
本輪最终提交後 exact SHA 的獨立 checkout receipt 使用新的外部 `/tmp` output，
確切 SHA 與 logs 在本輪回報中逐欄給出；未將暫存驗證物件混称 final。
未 push／PR／CI dispatch／merge，不宣告可合併；M4-R 是後續獨立任務。
