# BR-SD-1g custody 最終回讀

2026-10-11；BASE `dbdc4c35f785519c8e3cb0260807f0d2feb82469`。
前次 [CUSTODY.review](CUSTODY.review.md)、probe 與 validation 原檔保留，未覆寫。
本回讀的 [verify.py](../../verify.py) SHA256 為
`b371bd7769f52a2cb7301872685a7d9af607aeca679679a6b18d2dc34d350595`。

**CUSTODY-01 與 CUSTODY-02 均已修正，沒有未處理的 custody 阻斷 finding。**

- CUSTODY-01：固定初始 INPUTS／OLD manifest SHA、31／313 項及恰三個 old audit dirs；
  前次已實際獨立核全部 frozen／live／git BASE 輸入與原 custody inventory。
- CUSTODY-02：新增固定 `CLAIM`，`--check` 必比較該值；並新增 exact `SEAL_KEYS`。
  本次回讀已確認 claim drift／額外 metadata fields 被拒絕，`--seal` 使用固定 claim。
- root MAPPING body 的獨立原稿／相對 authority 連結 transform 再次通過。

最終 isolated controls 記於 [CUSTODY.probe.final.json](CUSTODY.probe.final.json)，
共12項，命令 exit code `0`：exclusive first-create／第二次拒絕且不覆寫、正常 inventory、
bytes drift、新增 payload、mode drift、symlink、恢復 inventory、mapping copy、
claim drift、額外 keys、恢復固定 claim／keys。

```sh
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/agents/mapping/custody_probe_final.py
```

所有 I/O probes 明示 mock source prerequisites，僅使用自己新建的 `/tmp`；
因此本次不聲稱 actual root `--seal`／`--check` 已執行，正式 seal 由 root 後續完成。
最終 paper accepted hashes、recorded checks 與 root payload inventory 仍須實際 verification。

[前次 review](CUSTODY.review.md) 的限制仍適用：git status 不觀察 ignored 外部檔案或
寫後還原歷史；recorded logs 的 hash checks 不重跑 commands；link helper 非完整
CommonMark parser；無網路遠端查詢；沒有 owner／ACL／mtime filesystem snapshot；
custody 不是來源／proof／Lean／canonical 採納驗證。

本 worker 現凍結全部 `agents/mapping/` 產物，不再寫入。
actual source `not triggered`，父身份 **OPEN**，完整 OPEN 身份新增無條件關閉數 **0**。
