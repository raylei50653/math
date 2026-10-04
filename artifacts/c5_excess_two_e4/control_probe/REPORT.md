# E4 補充：非相鄰雙 degree-5 的有限正控制探查

基準 `integrate-kprime-e3 @ 2ac279b`；worktree
`/home/ray/developer/ai/math-task-e4`。本探查只新增本目錄的 source、JSON 與
報告，不改既有 checker／報告，不 commit／push。使用指定共用 `.venv`。

**結果：未找到符合全部控制前提的圖。** 這只是四個具名 interior 模板的
有限構造失敗，不能寫成任意大小、任意 nonadjacent interior 的不存在定理。
因此本探查沒有提供可用於檢驗 E4 無三列中間引理的非相鄰正控制。

| 具名模板 | 變動範圍 | 命名接法 | Disk | T4 全收 | Σ-edge-minimal |
| --- | --- | ---: | ---: | ---: | ---: |
| Split951：兩個原 binary triangle hubs，以 sole mixed singleton 連接 | 原 binary attachments 固定為 `6→01,9→04,7→12,8→23`；`z=5,w=10,x=11` 各枚舉全部二 spokes | 1,000 | 7 | 7 | 0 |
| A：四 private，`H=K₂,₂`，兩 mixed singletons | 非相鄰 `z=5,w=6` 各三 spokes，`7,8` 各二 spokes，所有框 subsets | 10,000 | 0 | 0 | 0 |
| B：A 的兩 roots 各加一份固定原 binary triangle | 原兩 binary attachments 同上；roots 各一 spoke，兩 mixed 各二 spokes | 2,500 | 0 | 0 | 0 |
| C：`K₂,₃+xy`，一份 `(2,2)` mixed binary 加一份 `(1,1)` mixed singleton | `z=5,w=6,t=9` 各二 spokes，`x=7,y=8` 各一 spoke，全部框 subsets | 25,000 | 0 | 0 | 0 |

四個模板均在建圖時逐點驗：兩 roots 非相鄰且完整 degree 5，其他 private
完整 degree 4，ε=2，框上只有 C₅ 五邊。Disk 以加暫時框 apex 的平面檢查
篩選，再移除 apex，保存原圖 rotation、全部 faces 與指定 C₅ 外面。所有
interiors 連通，且固定或變動 spokes 碰齊框，移除 apex 後的指定面亦實際核對。

完整 Σ 用有限 MRV 四色回溯計算十份框代表，並用一次共同 S₄ 展開全部
字面接受框列；這是對固定有限圖的精確染色，沒有四色定理 oracle。

Split951 的七張 disk 全接受 T4，Σ 分別是 `1015`（兩張）、`959`（兩張）、
`1023`（三張）；每張至少有一條非框非critical 邊，尤其兩條 sole mixed
連接 `5–11,10–11` 均非critical。這七张的完整原邊、degree、Σ、完整接受框
relation、代表延拓、全部非框刪邊 Σ／新增列 witnesses 與 rotation 均保存在
[split_hub_probe.json](split_hub_probe.json)。它們不能充作要求 Σ-edge-minimal
的正控制，也不能據其 T4 性質冒稱已驗該完整前提下的無列引理。

其他三个模板的 disk 數為零，尚未到 Σ／criticality 篩選階段；完整固定
interior 與變動 spoke 定義分别保存在 [m2_probe.json](m2_probe.json) 和
[m2_binary_probe.json](m2_binary_probe.json)。零值计数若未由 Counter 輸出欄位，
以本表的零值明示。沒有擴大到其他 interior 或對單一具名 relation 分支進行
來源分類。

三個 sources 都提供 `--check`，新 JSON 使用 `open('xb')` exclusive-create。
三條生成、三條普通 `--check`、三條 `PYTHONHASHSEED=17 --check` 全部 exit 0；
`git diff --check` exit 0。命令、實際輸出與 source SHA-256 保存於
[validation.json](validation.json)。主 E4 的 `check_docs`／DocGraph 由任務整合
檢查，這份控制探查沒有另作可替代的全 repo 驗證。

重播：

```sh
PYTHONDONTWRITEBYTECODE=1 /home/ray/developer/ai/math/.venv/bin/python artifacts/c5_excess_two_e4/control_probe/split_hub_probe.py --check
PYTHONDONTWRITEBYTECODE=1 /home/ray/developer/ai/math/.venv/bin/python artifacts/c5_excess_two_e4/control_probe/m2_probe.py --check
PYTHONDONTWRITEBYTECODE=1 /home/ray/developer/ai/math/.venv/bin/python artifacts/c5_excess_two_e4/control_probe/m2_binary_probe.py --check
```

具體限制：未搜索任意 private 數或所有 interior 拓撲；沒有一般不可實現性
證明；沒有找到滿足 E3 三列前提的候選反例。E4 若保留無三列紙面引理，應
照實明列缺少要求的非相鄰實現控制，不能把既有相鄰 935 或 degree-6 的 951
控制當作同一前提的替代。
