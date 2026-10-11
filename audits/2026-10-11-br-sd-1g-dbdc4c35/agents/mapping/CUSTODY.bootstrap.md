# BR-SD-1g custody：首次 seal 的 planned-link bootstrap 回讀

2026-10-11；BASE `dbdc4c35f785519c8e3cb0260807f0d2feb82469`。
[前次 final review](CUSTODY.final.md) 與所有原 probe／review bytes 均保留。
本次只審 [verify.py](../../verify.py) 的 bootstrap patch，最終 SHA256：
`cb818a3d7430b48df7d098c7beb38e597aa197fae2665a8cd9d93f73ada5bcc0`。

**Bootstrap patch 通過，沒有新增 custody 阻斷 finding。**
REPORT 已接受的 bytes 連向預定 SEAL，首次 creation 前該 target 尚不存在。
現在 `prerequisites(allow_pending_seal=False)` 保持預設嚴格檢查；main 只在 `--seal`
傳 True。唯一豁免是不存在的 target 恰為本 audit 的 SEAL 且無 fragment；
其他缺少 local links／anchors 不被豁免，`--check` 不准 missing seal。
所有固定 authority／old manifest、accepted paper hashes、log digests 及 write-boundary checks
都仍在該 link exception 之前照常執行；exclusive `open('x')` 與 claim／key validation 未改。

本 worker 實際執行 read-only preseal prerequisites，不 mock，紀錄於
[CUSTODY.bootstrap.json](CUSTODY.bootstrap.json)：31 frozen／live／git BASE inputs、
313 原 audit files、22 recorded checks 與 existing audit links 全通過；
缺少 SEAL 時預設 strict prerequisites 仍以該 missing local link 拒絕。
命令 exit code `0`，沒有建立 SEAL、沒有改 accepted PROOF／MAPPING／REPORT。

```sh
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/agents/mapping/custody_bootstrap_probe.py
```

既有 `custody_probe.py`／`custody_probe_final.py` 的 mock 綁定前次已審 API，
保留為該版本的歷史 I/O controls；本次 read-only probe 是新 signature 的重播入口。
正式 root seal／seal check 仍由 root 執行；本次不是 mathematical acceptance 或來源實現。
其餘已記錄 custody 限制保持。actual source `not triggered`、父身份 **OPEN**、
完整 OPEN 身份新增無條件關閉數 **0**。

本 worker 完成本檔及 probe／JSON 後重新凍結全部 `agents/mapping/`，不再寫入。
