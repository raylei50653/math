# DocGraph

輕量文件關係網：從 Markdown front matter 的 `docgraph:` 區塊產生 family 分組、
relation 反向索引、dependency closure 與 D2 圖。目的是減少文件孤島，不是文件治理。
只用 Python 標準函式庫；核心不含任何 repository 專屬語義，可直接複製到其他專案。

## Metadata

```yaml
---
docgraph:
  id: c5.single-spoke-root-conservation   # 必填；stable logical ID，與路徑無關
  family: [c5, c5.single-spoke]           # 選填；分組，不代表順序或依賴
  requires: [c5.single-spoke-branch-minor]  # 選填；確實存在的前置條件
  derives_from: []                        # 選填；結果由另一結果推導
  related: []                             # 選填；值得互相發現，允許 cycle
---
```

只有 `id` 必填。只寫一個方向：`required_by`、`derived_by`、反向 `related`、
family 成員與 ancestors/descendants 都由工具推導，不要人工維護。其他 list 欄位
（如 `verified_by`、`formalized_by`、`supersedes`）視為擴充 relation，target 可為外部
名稱，不檢查也不進入 DAG。解析器只讀 `docgraph:` 區塊，支援純量、block list
與 flow list 的 YAML 子集。

## 指令

```bash
python3 tools/docgraph check [-v] [--strict]   # 驗證；-v 列出資訊性提示
python3 tools/docgraph build [--svg]           # 寫 .docgraph/（JSON、D2、每份文件的局部圖）
python3 tools/docgraph show <id>               # 局部關係
python3 tools/docgraph family [<name>] [-r]    # 家族成員；無名稱時列出所有 family
python3 tools/docgraph render [--view relation|family|dependency] [--root <id> --depth N] [-o FILE|-] [--svg]
python3 tools/docgraph suggest [<id>]          # 由 Markdown 連結提出候選 relation，只輸出
python3 -m unittest discover tools/docgraph/tests
```

共用選項：`--repo`（預設 git top level）、`--include GLOB`（可重複；預設掃所有
非隱藏目錄的 `*.md`）、`--out`（預設 `.docgraph/`，已加入 `.gitignore`）。
`--svg` 需要 PATH 上有 [d2](https://d2lang.com)；沒有時只寫 `.d2`。

## Validation

失敗（exit 1）只限資料錯誤：metadata 無法解析、duplicate ID、`requires`／
`derives_from`／`related` 指向不存在的 ID、`requires`＋`derives_from` 投影有 cycle。
沒有 family、沒有 relation、孤立文件都合法；`unconnected`、`single-member-family`、
`superseded-target` 只是資訊提示，僅在 `--strict` 時失敗。

工具從不修改 Markdown，也不依檔名、資料夾、時間、Git history 或文字連結建立
relation；連結只出現在 `suggest` 的候選清單中。D2 為產物，不是 source of truth。

## 圖的方向

邊依宣告方向繪製（A requires B 畫成 A → B），relation／dependency view 使用
`direction: up`，所以前置文件在上方。family view 每個 family 一個容器，
同屬多個 family 的文件在各容器各出現一次。
