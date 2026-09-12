# 內部五邊形加 1–3、1–4：第一輪完整研究

2026-09-12。使用者指定替換內部 K3；外部仍是固定有序、induced C5。
後續同一 C5 上的條件強迫庫見 [boundary_relations.md](boundary_relations.md)。

## 結果與信任分類

**Computationally observed：** 這個替換增加 exact Σ 的表達能力，但本 grammar
仍沒有只接受零個或一個三色模式的 disk patch。

| 項目 | 原內部 K3 | 內部五邊形加兩條對角線 |
| --- | ---: | ---: |
| 任意 attachments | 32,768 | 33,554,432 |
| apex-planarity 接受 | 7,194 | 174,456 |
| 不同 ordered / labeled exact Σ | 42 | 87 |
| 三色 acceptance subsets | 21 | 21，相同集合 |
| 最少接受三色模式數 | 2 | 2 |
| 接受恰兩個三色模式時 | Z5 相鄰對 | 仍全為 Z5 相鄰對 |
| Σ=T4 / 非空 BAD / 空 Σ | 0 / 0 / 0 | 0 / 0 / 0 |

87 個狀態包含全部原 42 個，新增 45 個。依三色 profile 大小分類：

| profile 大小 | 原 K3 exact states | 新 grammar exact states | 新 grammar 接線數 |
| --- | ---: | ---: | ---: |
| 2 | 5 | 5 | 460 |
| 3 | 15 | 30 | 2,820 |
| 4 | 15 | 35 | 10,190 |
| 5 | 7 | 17 | 160,986 |

**Proved in Lean：** `Math/FanPentagon.lean` 的單一新例子有 exact full Σ
證書，接受 216 個完整 labeled boundary assignments；接受全部三色邊界染色，
恰拒絕 01231 的 24 個全域換色。exact Σ 使用 `native_decide`，包含原生編譯信任。
`available_exact`、`each_triangle_feasible` 使用 `decide +kernel`；
`lists_incompatible` 和 `two_colour_obstruction` 是普通證明。

**Conjectured / unresolved：** 一般 fan / outerplanar interior 的三色 profile
下界與相鄰性是否有統一結構證明。此處的 87 狀態窮盡性、全 grammar 無 BAD、
disk topology 都沒有 Lean 定理；不外推至任意內部圖。

## 固定 grammar 與完整性檢查

外部頂點為 `b0..b4 = 0..4`。內部使用者標號 `1..5` 對應 graph vertices
`5..9`，邊是 `12,23,34,45,51,13,14`。每條 `(u,v)` attachment 的 bit
為 `5*u+(v-5)`。沒有增加外部邊界對角線，也沒有將內部限定在某個預設環序的嵌入。

搜尋器對 graph 加 apex 10，接到全部 boundary vertices，以平面性測試 cofacial C5。
DFS 按 bit 遞增加邊；遇 nonplanar prefix，剪掉其所有高 bit supersets。
輸出 174,456 個接受 mask 與 319,584 個拒絕 prefix。

獨立 checker 將低位固定 prefix 反轉成整數區間，證實區間互不重疊、沒有缺口，
恰覆蓋全部 `2^25` masks；再用 NetworkX 重驗每一個接受 mask 和拒絕 prefix。
搜尋使用 Rustworkx 0.17.1 的 [Left–Right planarity test](https://www.rustworkx.org/apiref/rustworkx.is_planar.html)，
重驗使用 NetworkX 3.5 的獨立實作，但兩者屬同一類演算法，並非獨立拓撲證明。
apex cofacial 測試的拓撲解釋仍是外部數學信任邊界。

染色搜尋沿 attachments 交集過濾 96 個合法內部 assignment bitsets。
獨立 checker 從所有 `4^5` assignments 重建合法內部染色，逐一驗證所有接受 mask 的
十-bit Σ，並對每個 state witness 重驗完整 240 個 labeled boundary assignments。
87 個 witness 都附 apex rotation；刪 apex 後另驗 C5 確為 face。

每個 Σ 只選 `(attachment 數, mask)` 最小的 witness 供展示；完整接受 masks 都保留。
這不是允許未來幾何 composition 只保留一個 Σ witness 的證明。

## 最簡單的新例子：只拒絕一類四色模式

`mask=1116616`、`sigma_bits=767`，10 頂點、19 邊、7 attachments：

| 內部使用者標號 | 相接的外部 boundary vertices |
| --- | --- |
| 1 | b4 |
| 2 | b1, b2, b3 |
| 3 | b1 |
| 4 | b0, b1 |
| 5 | 無 |

固定被拒絕的邊界模式 `(b0,b1,b2,b3,b4)=(0,1,2,3,1)`，可用色為：

| 內部點 | 可用色 |
| --- | --- |
| 1 | {0,2,3} |
| 2 | {0} |
| 3 | {0,2,3} |
| 4 | {2,3} |
| 5 | {0,1,2,3} |

點 2 被迫取 0。三角形 123 使點 1、3 分別取 2、3；點 4 同時鄰接 1、3，
卻只剩 {2,3}，因此無色可選。

三個三角形**分別**可染，例如按各自順序取：123 → `(2,0,3)`、
134 → `(0,2,3)`、145 → `(0,2,1)`；這些 witness 對共用頂點的選色不一致。
所以不能先各自隱藏共用頂點，再只交集三個「可染」布林答案。
本例的衝突其實已發生於前兩個三角形；第三個三角形的點 5 沒有 attachments，
永遠可選一個不同於點 1、4 的色。這是本例的簡化，不是所有 87 states 的縮減定理。

換成 boundary pair 語言，本例在 proper C5 上等價於：

```
b1 != b4  OR  b0 = b2  OR  b0 = b3
```

例如 `b1=b4 AND b0!=b2` 會強迫 `b0=b3`。單獨投影每對點看不到這條
三項共同限制；詳見 [條件強迫庫](boundary_relations.md)。

## 檔案與重現

* `scripts/fan_pentagon.py`：完整搜尋，約數秒。
* `scripts/check_fan_pentagon.py`：獨立 coverage / 染色 / 幾何 replay。
* `artifacts/fan_pentagon/summary.json`、`replay.json`：結果與輸入 hash。
* `disk_rows.bin`：按 mask 排序的 `<IH` records（uint32 mask、uint16 Σ）。
* `nonplanar_frontier.bin`：按 mask 排序的 `<I` prefix masks。
* `states.json`：87 個 exact Σ、最小 witness 與 apex rotation。
* `Math/FanPentagon.lean`、`Math/FanPentagonAudit.lean`：單例染色證書與公理審計。

```bash
uv run --with rustworkx==0.17.1 --with networkx==3.5 python scripts/fan_pentagon.py
uv run --with numpy==2.4.3 --with networkx==3.5 python scripts/check_fan_pentagon.py
lake build
lake env lean Math/FanPentagonAudit.lean
```

本輪不新增 native 全 grammar 證書、不嘗試證一般 topology completeness，也不擴大 n。
