# N45-L1C：LOW1 工具、封存與 coverage 獨立稽核

BASE：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。來源交付：
`audits/2026-10-10-n45-s-low1/`；只新增本專屬 audit，不修改 worker、共享文件或其他 audit。

裁決：**接受 final-v4 工具證據 envelope，附一項非阻擋索引 finding**。
本稽核不裁任意大小 paper 論證，不把任何 replay 或 hash agreement 當作數學排除。
數學候選仍交由獨立 paper／前提映射裁決；一般 N2／E 與 Lean 保持 OPEN。
結構化範圍與 finding 見 [獨立裁決](independent-judgment.json)。

## 封存與 inputs

獨立 [checker](checker.py) 只讀實際檔案，自行枚舉 regular files／symlinks，
解析 manifest，重算 SHA256，核對 BASE Git object 和 frozen current pins。
不 import worker code，不執行 `prepare.py`、`seal.py` 或 v2／v3／v4 封存 mutators。
[inputs](inputs.json) 綁原 manifest、receipt、稽核開始時六個 live pins 及父監督封存的初始 strict replay。

| 核對項目 | 實際結果與界線 |
| --- | --- |
| 最終 manifest | `MANIFEST.final-v4.sha256`；SHA256 `7dba2b7df58370838b12c5184e590de4e46e00628db84a204d38db3e139e6292` |
| 完整 payload inventory | 6,049 regular files，5 個 symlink identities；每一項實際內容／target 相同 |
| 最終 exclusions | 僅兩個 top-level files `MANIFEST.final-v4.sha256`、`delivery.json`，與 top-level `seal-final-v4/` |
| receipt metadata | `seal-final-v4/` 恰 10 regular files，逐檔 receipt hash 相同，沒有未綁定 metadata／symlink |
| 舊封存證據 | `seal-checks/`、`seal-final-v2/`、`seal-final-v3/` 各 10 regular files 均納入最終主 manifest |
| nested manifest | 2 份 nested manifests 納入主 manifest；沒有依任意 path component blanket 排除 nested seal dirs |
| BASE 論證來源 | 12 個具名 inputs：BASE Git blob ID、SHA256、archive bytes 均相符 |
| current-work pins | 6 份 frozen current 與指定 SHA256 相符；稽核開始時 6 份 live pins 亦相符 |
| 外部 PDF bytes | worker 留存官方 PDF 和指定 BASE PDF bytes 相同；本稽核只核 bytes，不裁外部定理真偽 |

5 個 symlinks 均在 BASE archive 下，target 為原 `.snapshot`，包括 dangling target 的 identity。
稽核不因 target 是否存在而忽略 symlink。

## 重播與錯資料控制

[checks](checks.json) 封存 actual argv、環境、stdout／stderr hashes 和退出碼；
[controls runner](run_controls.py) 只寫本 audit 的 logs 與 synthetic 錯資料。
一般與 `PYTHONHASHSEED=17` 的獨立 frozen checker actual exit 均為 0，stdout bytes 相同。

| 合成 artifact 負控制 | actual exit 與拒絕階段 |
| --- | --- |
| 同 inventory 的錯 digest | 2；`payload-digests` |
| 刪除一個 manifest path | 2；`payload-inventory` |
| 重複 manifest path | 2；`payload-inventory` |
| `../outside` unsafe path | 2；`payload-inventory` |
| 錯 symlink target | 2；`symlink-identities` |
| receipt 省略一份實際 metadata | 2；`receipt-inventory` |
| receipt 對已存在 metadata 給錯 digest | 2；`receipt-digests` |

七項均核 actual rejection reason，不能只依 exit2 稱 digest 控制通過。
這些是 artifact integrity 負控制，沒有 graph／source counterexample 意義。

worker 最終封存 normal／seed17 actual exit0、bytes 相同；其當時 runs 為 `--payload-only`，
所以 stdout 的 `receipt_checked` 是 false。最終 receipt 另外綁 10 份實際證據。
父監督在新增任何 supervisory／reviewer 目錄之前，重跑 strict normal／seed17：actual exit0、
bytes 相同，且 `receipt_checked` true；原檔 bytes 的本 audit 副本見
[父監督初始 strict evidence](frozen/parent-initial-strict-replays.json)，hash 綁定於 inputs。
父監督 corrupt-manifest actual exit2，stderr 明確是 digest mismatch。

新增 supervisory／reviewer 專屬目錄後，本稽核另跑 worker strict 入口 actual exit2，
理由是 `pre-existing workspace inventory differs`。
這是精確 Git inventory 已新增檔案的預期變化；不能以當前入口失敗否定原封存，
也不能把 frozen checker exit0 報成當前完整工作樹 strict replay exit0。
獨立入口只重查 frozen artifact、BASE inputs 與原 frozen pins，不要求後續採納文件 bytes 不變。

## 舊工具失敗與索引 finding

v1 原 normal／seed17 actual exit2，原因是 manifest string／Path 排序不同。
其 corrupt control 亦停在 inventory，不覆蓋 digest 階段。
v2 原 normal／seed17 actual exit2，誤把四個 nested repositories 的 directory entries 判為 missing files；
v3 原 normal／seed17 actual exit2，把 inline code 的數學式誤讀成 Markdown link。
v2、v3 與 final-v4 的 corrupted manifest 控制才實際到 digest mismatch。
三版 finding、原 verify code、舊 manifest 與 logs 全部仍在 final-v4 主 manifest。
三版舊 REPORT 的 §§1–6 與最終 REPORT **逐字相同**；稽核只確認 retry 沒有改該段 paper bytes。

**L1C-INDEX-01（非阻擋）：** worker `checks.json` 的 `postseal_actual_results` 仍指向
`seal-checks/commands.json`，那份是 v1 失敗紀錄。
真正最終證據是 `delivery.json` 明確綁定、REPORT 正確連結的
`seal-final-v4/commands.json`。應以 final-v4 為當次成功封存入口，保留 v1 FAIL。
本稽核保留 immutable worker，未修這個舊欄位；finding 不改變 final-v4 封存核對的結論。

## Coverage 與保留的 FAIL

worker 初始 Git 清單有 25,895 entries：25,869 regular files hashed、22 symlink identities、
4 個 nested-repository directory entries。四個 nested repos **初始未遞迴 hash**，僅核目錄存在；
不能回溯宣稱其內部 fulltree 零漂移。父監督原 strict 成功只核這個列明範圍。
本獨立 frozen replay不重新宣稱當前 25,895 entries 或全部工作樹內容保持原狀。

本輪沒有建立或執行新 finite source controls，**沒有 trigger 數**；不能寫成 0 觸發或正控制。
沒有新來源實現、Lean、`lake build`，不以本稽核接受工具 envelope 取代 paper 裁決。
LOW incidence2／HIGH／long、一般 N2／E 保持 OPEN。

worker 已封存 fresh BASE `check_docs.py` actual exit1，恰 2 個歷史缺檔；
whole-worktree DocGraph actual exit1，62 個 duplicate-ID error lines。
本 checker 重查對應原 log lines 和計數，沒有重標 PASS 或刪副本。
fresh BASE formal docs／current docs 與 formal DocGraph 原結果另有 exit0，沒有合併全工具 PASS。
歷史 E4 provenance byte replay FAIL 保留，本輪未重跑。

## 交付與停止

[MANIFEST](MANIFEST.sha256) 綁本 audit 的所有 regular payload；
[delivery](delivery.json) 另綁本 audit 的 top-level seal metadata，exact inventory 亦由
[只讀自驗入口](verify.py) 核對，沒有 blanket nested seal exclusion。

```bash
python3 -B audits/2026-10-10-n45-l1c/checker.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-l1c/checker.py
python3 -B audits/2026-10-10-n45-l1c/verify.py
```

只新增本專屬 audit；未修改 shared／worker／其他 audit，未 commit、push、PR、再委派或對外訊息。
停止於工具／封存／coverage 獨立裁決，不選下一 residual，不裁任意大小 paper 或一般命題。
