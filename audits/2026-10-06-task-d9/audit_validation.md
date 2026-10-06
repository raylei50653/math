# D₉：重播、不變性與信任範圍

2026-10-06；所有被稽核行號與 bytes 固定於
`b2ca4520da50c9d2898ac6f8f966ac25df3f9609`。
來源 worktree `/home/ray/developer/ai/math-task-d9`，branch `task-d9-audit`。

## 1. 稽核界線

依 [DOCUMENTATION](../../docs/DOCUMENTATION.md) 的信任分層，紙面推導、
引用的 degree-list／Gallai／Jordan／K₅ 不可平面性、固定 Python 控制、
外框 disk 可實現性、Lean 各自記錄。此輪只查外部前提在 E4–E6 的實際使用，
不重證 E3、D₈ 的 DG6-1 補表或原 A／B 必要表。

每個 argument 保留同一原圖、原 piece 的全部頂點、原 contacts、實際框附件、
ownership、rotation、完整 tuple／lift 與共同色框。Minor 只用於原圖非平面反證，
不宣稱保留 Σ、T4、全部 boundary patterns 或原 graph class。
q₂、q₄ 的接受性只在明列的精確 941／933／940／932 分支中使用；
proper predecessor 的 Ω 身份只在已證的個別入口使用。

獨立 checker 不 import producer 的決策程式；从 raw edges 与 rotation 重算。
原 producer 的 `build` 只在 [歷史重播差異診斷](inspect_original_replay.py) 中重用，
此檔明列 `independent_lemma_checker=false`，不能冒充獨立證明。
沒有四色定理 oracle，沒有大枚舉、Lean build 或新增 Lean theorem。

## 2. 原 checker 的 default／seed17 重播

這裡 default 指不設定 `PYTHONHASHSEED` 的 `--check`，不是會建立產物的 generation mode。
各歷史 report 指定 stdlib `python3` 或共用 Python 3.14／NetworkX 3.5；
本輪 stdlib 沿用 `python3`，NetworkX 三個 checker 以
`uv run --with networkx==3.5 python` 執行。E4–E6 report 沒有指定其他 uv 套件。
每份普通命令另以 `PYTHONHASHSEED=17` 執行一次，單 worker；
原 checker 的命令、exit、stdout／stderr log SHA256 見 [validation](validation.json)。

| checker | default exit | seed17 exit | stdout 相同 | 解釋 |
| --- | ---: | ---: | --- | --- |
| E4 reductions | **1** | **1** | 是 | 原 artifact byte FAIL；只差 E3 REPORT 的 provenance |
| E4 control | 0 | 0 | 是 | 202 stored representatives／19 fixed attempts；原控制搜尋本來沒有 NA 正控制 |
| E5 controls | **1** | **1** | 是 | 原 artifact byte FAIL；只差 E3 REPORT 的 provenance |
| E5 local | 0 | 0 | 是 | 原局部算術重播 |
| E5 branches | 0 | 0 | 是 | 原四分支、共同 D₅ 搬運與完整 guard 重播 |
| E6 reductions | 0 | 0 | 是 | 原字面算術、兩種四路外面示例重播 |
| E6 controls | 0 | 0 | 是 | 原 9 AD orbit／90 D₅ images 重播 |
| E6 local controls | 0 | 0 | 是 | 原局部機制重播 |

16 命令為 12 個 exit0、4 個歷史 exit1；八對 stdout 皆相同。
stdout 相同包含兩組失敗命令的空 stdout，不能將其解讀為 checker 通過。
沒有覆寫或重新封存舊 artifact。

## 3. D9-P1：歷史 provenance FAIL 的最小重現及影響

```bash
python3 scripts/c5_excess_two_e4_reductions.py --check
python3 scripts/c5_excess_two_e5_controls.py --check
python3 audits/2026-10-06-task-d9/inspect_original_replay.py
```

前兩條實際 exit1；最後一條產生 audit 目錄中的 fresh replay 與
[逐欄差異](historical_replay_differences.json)，不改原證書。
兩份原資料都記錄 E3 REPORT SHA
`6d385639c565e2dd08eb61d7835f5fbfec29cd7c467ce8e5abba1dfc2e39e659`；
在 b2ca452 該檔 SHA 為
`73ed652a55b159a44eb6da4608f11537efc0d43603128094101ef044a96b2cd3`。
E4 另記錄 bytes 30573，現為 32469。

| artifact | 原 SHA256 | fresh replay SHA256 | 移除單一 provenance 欄位後 |
| --- | --- | --- | --- |
| E4 reductions | `5b9d97d2a19d36776cd0617531023756889813bc44c108ec67bf6dca1ec1fb40` | `3a78b89f29b8fc37ea8fff477ceb0e8956a2d25977b3f75f529fe5aadc525425` | 全部 payload 相同 |
| E5 controls | `988b6d4b799594107c99ef6037d9bd4a7128a88d3f3810a9f04b7dcfc7d6dabf` | `34581ff2e1974dd44cd1c184f320bb9b2076829432cc90cee96d64afe5d37a1b` | 全部 payload 相同 |

E4 只差 `/sources/artifacts/c5_excess_two_e3/REPORT.md/{bytes,sha256}`，
E5 只差 `/source_sha256/artifacts/c5_excess_two_e3/REPORT.md`；
所有其他 provenance 值也相同。
影響是嚴格 byte/provenance 重播無法標記 PASS；不是新數學反例，
不影響本輪逐步紙面 verdict 或獨立控制結果。

## 4. D9-R1：封存還原 preflight 缺口

```bash
python3 tools/audit_archive.py restore --artifacts
```

實際 exit1，完整 [stderr](logs/archive_restore.stderr.log) 保存：
`No archived bytes for manifest artifact: artifacts/c5_excess_two_e3/degree6.json`。
`tools/audit_archive.py:182–193` 先核對全部 blob、再預查全部 MANIFEST artifacts；
這個 error 發生在任何還原写入之前。
另查 MANIFEST 缺檔，其中未封存 SHA 的還有
`artifacts/c5_excess_two_finite_search/NA_k9_validate.json`、
`artifacts/c5_kempe_diagonal_transport/assignments.jsonl`、
`artifacts/c5_kempe_diagonal_transport/bounded_realization.json`。

本次需要的 54 NA／9 AD 原 orbit、E4C 的 54 份 controls、E3 的紙面與 D₈ 補表皆已 tracked。
唯一缺少的實際原 checker 輸入是 E1 `observations.json`；
[restore-required](run_validation.py) 對它獨立核對 compressed blob SHA／大小及
uncompressed MANIFEST SHA／大小，僅用 `xb` 還原缺檔。
其 SHA `23a92b56f325bd4bd496d7e8dfb14714d8481618253f88243df4cb7916ca999e`、
1125356 bytes 與原記錄一致，見 [restore record](required_restore.json)。
此檔是 gitignored runtime，未修改 existing tracked file。

影響：repo 的全域 `restore --artifacts` 無法完成；本輪必要 controls 與八份 checker
皆可讀取，不需重建缺少的 E3 degree6／ES aggregate／K′ runtime。
本輪只檢查 D₈ 補表在 E3 degree6 prerequisite 的引用，沒有宣稱重跑該外部補表。

## 5. 文件／whitespace／不變性

`python3 scripts/check_docs.py` 實際 exit1，只出現 D₈ 已記錄的兩個 known missing paths：

- `docs/c5_open_leaf_ledger.md:78` 引用的 `audits/2026-10-04-task-d5/c4/scope_ledger.json`。
- `docs/history/2026-10-04-task-d2-integration-audit.md:39` 引用的 `audits/2026-10-04-task-d2/integration_doc_changes.diff`。

兩個問題與本輪紙面推導無關；未更動原文件、未虛造替代檔來消除 error。
全域 checker 本來不掃 audits，另檢查本 audit 的相對連結、實際引用的 heading anchor 與新增文本 whitespace。
`git diff --check` 和 `git diff --cached --check` 均須照實記錄；
新檔在 staged 前不能只憑 empty tracked diff 宣稱檔案已查。
既有 tracked 普通文件逐 SHA 核對見 [invariance](invariance.json) 與
[baseline](baseline_sha256.json)。

此輪只完成指定引理的獨立 audit；G1–G4、N1／N2、J6 m≤2 的原來源殘留仍保留。
有限控制的零反例不提升成任意大小定理，不推得 ε≥3、一般出口或 K∞=K≤5。
