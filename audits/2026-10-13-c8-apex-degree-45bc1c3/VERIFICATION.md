# 驗證與可重播命令

本包驗收使用 Python 標準庫，無浮點容差或 LP 狀態作接受標準。
[verification.json](verification.json) 與 [validation](validation/) 保存全部 stdout／stderr。

```bash
python3 -B audits/2026-10-13-c8-apex-degree-45bc1c3/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-apex-degree-45bc1c3/check.py --check
python3 -B audits/2026-10-13-c8-apex-degree-45bc1c3/controls.py
python3 -B audits/2026-10-13-c8-apex-degree-45bc1c3/verify.py
```

正常與 seed17 重播均 PASS：八個原查詢、四十份具名 apex 假設，38 份
完整支援刪除證書與兩份完整有理分離證書。每次先驗證全部七份 frozen
輸入 SHA256／大小；它們已逐一與 BASE Git object 位元組核對。
獨立 reviewer 自行遍歷 literal contexts 與 4^8 boundary assignments，
分別驗證支援、兩份 dual 及原 transfer，皆 PASS。
[獨立紙面審查](review/REVIEW.md) 不依賴 discovery 或主 checker 的生成器。

三個破壞控制均按預期拒絕：改具名 apex 位置、將不等式乘數改為負、
刪除一項 normalizer 係數。控制只改臨時目錄，保留原證書。
W8 的全部 732 個合法 literal 七點 context 驗证新計數引理；另有原
度數四邊界點的明列三角化圖，完整延伸數為 `(1,0,0)`，反駁任意放寬
度數三前提。這是 weakened-claim 反例，不是實際最小目標來源。

可選 SciPy discovery 只發現兩份 dual：

```bash
/home/ray/.cache/uv/archive-v0/3XJ9zwHiKOnoDAN7/bin/python \
  audits/2026-10-13-c8-apex-degree-45bc1c3/discover.py \
  --output-dir /tmp/c8-apex-discovery-replay
```

本次 discovery 重播生成位元組相同證書，雜湊見
[discovery-replay.json](discovery-replay.json)。系統 Python 不需 SciPy。
初始 generated interface 無 Git blob 的情形與改以完整 literal transfer
重算的處理，見 [發現紀錄](discovery_failure_01.txt)。

本輪 root 再驗 exact checker PASS，保留 [root-check.stdout](validation/root-check.stdout)。
與並行 W5 包共同完成的文件／Lean 驗證集中在鄰包：

* [一般文件連結](../2026-10-13-w5-rank3-essential-45bc1c3/logs/docs.log)：PASS，651 檔／8148 連結。
* [正式文件 DocGraph](../2026-10-13-w5-rank3-essential-45bc1c3/logs/docgraph-formal.log)：PASS，62 文件／213 關係。
* [全樹 DocGraph](../2026-10-13-w5-rank3-essential-45bc1c3/logs/docgraph-full.log)：FAIL，62 項既有 duplicate-ID，未修改舊歷史證據。
* [lake build](../2026-10-13-w5-rank3-essential-45bc1c3/logs/lake-build.log)：PASS，8831 jobs。這是既有 Lean 回歸，不是新增引理形式化。

root 接入 [C8 正式入口](../../docs/c5_c8_apex_degree.md)、完整外圈限制、
Kempe 導覽與 STATUS；本 subtask 只寫這個 exclusive audit。
沒有 commit、push、PR 或 Issue。此包的完整檔案雜湊見 [MANIFEST.json](MANIFEST.json)。
