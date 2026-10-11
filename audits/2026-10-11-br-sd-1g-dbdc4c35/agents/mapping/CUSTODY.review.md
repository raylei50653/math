# BR-SD-1g：獨立 custody code／mapping-copy 審查

2026-10-11；BASE `dbdc4c35f785519c8e3cb0260807f0d2feb82469`。
本次只核 custody／記錄一致性，不裁定數學證明、來源存在、canonical 採納或遠端狀態。
本 worker 只寫 `agents/mapping/`；isolated I/O probes 只在自己新建的 `/tmp` 目錄運行，
未更動原 audit seal、authority、其他 worker 或共享檔案，未 commit／push。

## 審查範圍與結果

審查 [verify.py](../../verify.py) 與 root [MAPPING](../../MAPPING.md)。
初始已審版本 SHA256
`a8349fa75290063382a29ac8d6c98b2c37949a012e940cad3fedc0670077d44d`；
此 hash 與 [probe 記錄](CUSTODY.probe.json)、[獨立來源核對](CUSTODY.validation.json) 相同。
probe 的 source prerequisites 被顯式 mock，故其 PASS 不冒充 actual audit seal PASS。

| 要求 | 獨立核查 |
| --- | --- |
| 固定原 authority 清單 | INPUTS 原 bytes 的 hardcoded SHA、31 項與 BASE 核對；本 worker 獨立重算通過 |
| 31 frozen／live／git BASE 輸入 | 三者每項 bytes 相等，size／SHA 都相同；實際獨立讀取 31 項通過 |
| 313 old 1a／1c／1e 全量 custody | OLD 原 bytes SHA 固定、恰313筆、恰三原 audit dirs；實際 inventory 的 path／size／SHA／mode／symlink 欄位逐項等於原清單 |
| 三根層文書的 accepted final hashes | code 要求 acceptance scope、OPEN／0 與 PROOF／MAPPING／REPORT 恰三 keys，再逐項比 SHA；第一次本 worker 檢視時最終 ACCEPTANCE 尚未產出，所以未聲稱其 runtime 已通過 |
| audit payload exact inventory | `SEAL.json` 以外全部原 payloads 入表；校驗 exact list／size／SHA／mode，拒絕新增／消失／symlink；isolated controls 實測通過 |
| 外部寫入邊界 | HEAD／origin/main 固定；git porcelain 要求所有可見 dirty records 均為 audit 內未追蹤檔，任何 staged／tracked 變動亦拒绝 |
| recorded checks | nonempty records 的實際／預期 exit codes 必相等，stdout／stderr bytes SHA 必相同；本 worker 先核6筆 preliminary，再核當時22筆 CHECKS 全通過 |
| audit local links | 原 helper 只解析 Markdown prose links／reference definitions；非 authority audit Markdown 的 local target／Markdown anchor 必存在；frozen authority 的歷史相對 link 語境刻意不再檢查 |
| `--seal` exclusive create | `open('x')`，第二次 FileExistsError 且原 SEAL bytes 不變；isolated probe 實測通過 |
| root mapping copy | 從原日期段開始至 EOF，恰等於原 worker 稿把 `../../authority/` 改為 `authority/`；另加 root provenance；實際逐字比較通過 |

## Findings

**CUSTODY-01，已修正。** 初稿沒有固定 INPUTS／OLD 清單 bytes、31／313 數量及三個原
audit dirs；預先移除一整份 old audit 登錄或省略 authority 登錄，會縮小檢查覆蓋而不被拒絕。
root 加了固定原清單 SHA、31／313 及 exact dir set。上述改版已回讀且獨立重算通過。

**CUSTODY-02，要求修正。** 本次所列初始已審版本的 `--check` 未比較 SEAL 的 `claim`，
而 SEAL 自身不在 payload inventory；單改 claim 字串會不影響其餘校驗。
應要求其恰為 `candidate scoped exclusion; no canonical adoption`。
這是 manifest 結論字串的 custody 缺口，不是紙面數學 finding。

## 明確限制

- git status 不觀察 ignored 的外部檔案，也不證明曾寫入再還原的歷史。
  這是工作樹可見狀態界線，不是完整系統 write audit；本次沒有由此宣稱觀察所有歷史 I/O。
- recorded-check hashes 證明已記錄 log bytes 一致；verify 不重跑 commands、也不獨立證明
  log 與 `argv` 的來源真實性。root 原執行紀錄及獨立 checker replay 承擔這部分。
- final acceptance JSON 的 hashes 只核已審 bytes 一致；此工具不是 paper reviewer、
  身分簽章系統或 proof checker。最終 paper acceptance 由獨立 worker 交付。
- exact payload inventory 不包含 mtime／owner／ACL，並不是 filesystem snapshot。
- local-link parser 刻意不是完整 CommonMark／HTML parser；網路連結不抓取，frozen authority
  的歷史連結不改語境。此次 root mapping 的新增相對連結已驗證 copy transform。
- verifier 不取網路遠端 main；root START／END logs 負責 live remote readback。
- SHA manifest 與固定 verifier 是可重播 custody evidence，不自動給來源實現、Lean、
  父身份 closure 或 canonical 採納。

重播 isolated I/O controls：

```sh
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/agents/mapping/custody_probe.py
```

本 worker 的 controls 命令 exit code `0`；actual target source `not triggered`。
此 custody review 保持父身份 **OPEN**、完整 OPEN 身份新增無條件關閉數 **0**。
