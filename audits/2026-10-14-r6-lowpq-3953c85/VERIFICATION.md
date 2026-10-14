# 驗證範圍與重播

BASE `3953c85e334b96533e44652df065640f5463715a`。
新證明及文件只在 `/home/ray/developer/ai/math-r6-lowpq-3953c85` 工作樹。
主工作樹與遠端發布狀態獨立核對；本輪沒有 commit／push。

## 紙面與固定算術

- [r6 證明](r6/PROOF.md)：兩張原實際面的合法共同識別、k−5 cap 預算、
  完整 fibre 聯集非空及 ell-v／ell-w 非邊；任意大小部分由紙面論證負責。
- [原內圈證明](h18/PROOF.md)：induced collar、私人圖連通無葉與圈秩≥2、
  精確 incidence 等式及 k≤27⇒h≤12；有限算術不認證這些拓撲步驟。
- [獨立幾何審查](review/GEOMETRY.md)逐項核對上述原邊、旋轉、量詞與來源域。
- [主局部色表](r6/check.py)的正常及 seed17 重播通過，破壞一份真實 cap lift
  的負控制被拒；[receipts](r6/logs/receipts.json)保存完整命令與雜湊。
- [獨立原邊核算](validation/direct_joint.py)不 import 主 checker，逐份比對
  全部210個 proper 色軌道與6048份標記 full lifts，正常與 seed17 輸出完全相同；
  見 [獨立 receipt](validation/independent-receipt.json)。另一份
  [獨立核算](review/independent_caps.py)另從舊 transfer 表比對。
- [計數 checker](h18/check.py)從 C–P 邊數與私人 degree 總和獨立重建等式；
  正常及 seed17 通過，44條跨界邊被改成43的負控制被拒；見
  [receipts](h18/receipts.json)。881／765／698列分別是非負邊、連通必要式、
  圈秩至少二的整數鬆弛，不是實際圖或來源實現。

## 只讀重播入口

從隔離工作樹根目錄執行：

```sh
python3 -B audits/2026-10-14-r6-lowpq-3953c85/check_inputs.py
python3 -B audits/2026-10-14-r6-lowpq-3953c85/r6/check.py --check
python3 -B audits/2026-10-14-r6-lowpq-3953c85/h18/check.py --check
```

以 `PYTHONHASHSEED=17` 重跑後兩項可核對固定色列與整數順序。
`--write` 是 exclusive-create 的產生模式，不是只讀重播。

## 整合檢查與歷史檔案補齊

[整合重播](validation/final-checks.json)確認23份 frozen inputs 全等於 exact BASE，
現行不可變數學輸入亦無漂移；正常／seed17 custody 通過，破壞 SHA256 的
負控制被拒。整合者再跑 r6 與 h18 的只讀 checker 均通過。

正式 docs DocGraph 通過：97 documents、383 relations、0 errors。
`git diff --check` 通過。第一次 `check_docs.py` 因新工作樹缺少9個歷史
目標而報23條連結錯誤，原 log 保留。按 [補齊清單](validation/archive-hydration.json)
恢復5份經雜湊驗證的 tracked archive blob，並複製4份主工作樹已有但 ignored
的歷史文件作連結核對；後四份不是本輪數學 authority，也不聲稱屬 BASE。
僅查 archive 的初次補齊在找不到一個 local-only key 時失敗，紀錄亦保留。
[補齊後重播](validation/hydrated-doc-checks.json)通過：686 Markdown files、8950 local links。

Whole-tree DocGraph 仍失敗，70項診斷；與主工作樹相比
[錯誤鍵完全相同](validation/docgraph-comparison.json)，沒有新增錯誤類目。
各工作樹的 frozen／scratch occurrence 清單不同，本輪新增的 frozen C4
副本亦如實保留；不能把正式 docs 通過寫成 whole-tree 通過。

## 保留的歷史與界線

舊 BASE 報告、證書、271／314／319 計數模型與 frozen inputs 原樣保留。
本輪的 [h≤13 初稿](h18/PROOF-h13-initial.md)、
[探索與編輯失敗紀錄](h18/EXPLORATION.md)亦保留，由現行 h≤12 證明承接。
沒有重跑 plantri、大型來源枚舉、外部論文計算或 Lean build；沒有新增 Lean theorem。
一般 K≤22／k≥23、高 p,q 條件 k≥28 及所有未關閉來源保持原範圍。
