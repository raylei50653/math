# K13／W5 圈秩三主線整合保存核對

2026-10-13。數學採納範圍、完整來源前提、信任分層與 OPEN 邊界見
[整理發布紀錄](../../docs/history/2026-10-13-k13-rank3-publish.md)。
本包保存此次主線重播及發布檢查，不改寫兩份原隔離證書。

## 保存核對

[ORIGINS.json](ORIGINS.json) 記錄兩份固定 BASE 與整合起點。
[IMPORTED.json](IMPORTED.json) 保存248份原 audit 及13份新 archive blobs 的逐檔
SHA256／大小。[verify.py](verify.py) 核對全部原 audit、原 seal 項目、18份
gzip 原共享文件快照、BASE 輸入、舊 ARCHIVE records、17個 K13 追加路徑及13個 blobs。
新的整合 manifest 與白名單由本包獨立保存，不覆寫原 SEAL／DELIVERY。

```bash
python3 tools/audit_archive.py restore --artifacts
python3 -B audits/2026-10-13-k13-rank3-publication/verify.py --check
```

## 主線數學重播

- [K13 結果與命令](validation/k13/results.json)：七項重播全部通過，涵蓋
  normal／seed17、獨立 full lifts、結構負控制、逐 lift 比較、空 fibre 校準與
  736配置／28內側核心的完整覆蓋。306根圖、3,060列、41,021完整 lifts 一致。
- [W5 結果與命令](validation/rank3/results.json)：五項重播全部通過，涵蓋
  normal／seed17、獨立完整關係、K132 membership、16次破損拒絕。
  2,270模板、23,244,800 cells、928,404 A lifts、465,866 G lifts 一致。

全部原 audit 在重播前後逐檔一致；原隔離工作區未修改。
未重跑完整球面生成／小域全邊集枚舉及原74項工具測試；原記錄保留。
外部計算證書重播及新 Lean 形式化未執行。

## 整合檢查

文件連結、audit 連結、正式／全域 DocGraph、`lake build`、儲存政策、
`git diff --check`、新 Git index 還原與原始 bytes 核對，由本包 `validation/`
保存實際命令、退出碼及 stdout／stderr。

- [共享檢查](validation/shared/results.json)：文件659份、8,242個本地連結通過；
  正式 DocGraph 的62份文件、213條 relations、5個 families 通過；
  `lake build` 完成8,831 jobs，僅記既有 Lean 回歸。全域檢查 exit 1，
  62項均為既有 duplicate-ID，ID 集合與原隔離 log 完全相同。
- [audit 連結](validation/shared/audit-links.json)：14份非 frozen Markdown 的
  88個本地連結通過。
- [index 儲存及 whitespace](validation/shared/index-checks.json)：實際 staged
  儲存政策與 `git diff --cached --check` 通過；不 stage 大型原檔的未壓縮副本。
- [新 index 還原](validation/shared/fresh-index.json)：從實際 Git index 匯出
  白名單，在17個封存原路徑尚未還原時保存 verifier 通過；逐 byte 還原這17項後，
  K13 主 checker 及 W5 catalogue checker 通過。

共享 DocGraph 首次正式命令把全域選項放在子命令後，exit 2；修正參數位置後
通過，原 stdout／stderr 保留。新保存 verifier 不作數學枚舉，實際檢查
261份匯入檔案、277項原 seal、33份 frozen inputs、17項封存追加及 gzip 完整性。
最終另建立本包 MANIFEST，再以唯讀核對及新的 staged 匯出確認整合 bytes。
README／HANDOFF 已核對；研究線及用法未變，無需新增摘要。
