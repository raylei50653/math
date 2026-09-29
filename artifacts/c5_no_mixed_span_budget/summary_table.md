# No-mixed 十五類總表

由 `scripts/c5_no_mixed_span_budget.py` 生成。
原接合含 root 交換方向；支援與查詢只計各報告保存的正向表。
支援／來源排除／target 接受為不同計數單位；必要支援不是來源圖。

| 類型 | 側跨度下界和 | 原接合 | 空正向纖維 | 必要支援 | 原 source 排除 | 保留支援 | 原 target 接受 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A–A | 4 | 88 | 46 | 322 | 0 | 322 | 644 |
| A–B | 4 | 272 | 70 | 560 | 0 | 560 | 1120 |
| A–C | 5 | 192 | 42 | 364 | 340 | 24 | 48 |
| A–D | 6 | 192 | 56 | 212 | 212 | 0 | 0 |
| A–E | 5 | 192 | 60 | 120 | 0 | 120 | 240 |
| B–B | 4 | 236 | 144 | 888 | 0 | 888 | 1776 |
| B–C | 5 | 360 | 80 | 608 | 584 | 24 | 48 |
| B–D | 6 | 360 | 108 | 312 | 312 | 0 | 0 |
| B–E | 5 | 360 | 120 | 144 | 0 | 144 | 288 |
| C–C | 6 | 144 | 36 | 1176 | 1176 | 0 | 0 |
| C–D | 7 | 288 | 72 | 640 | 640 | 0 | 0 |
| C–E | 6 | 288 | 108 | 96 | 96 | 0 | 0 |
| D–D | 8 | 144 | 80 | 352 | 352 | 0 | 0 |
| D–E | 7 | 288 | 120 | 48 | 48 | 0 | 0 |
| E–E | 6 | 144 | 144 | 0 | 0 | 0 | 0 |

總計：`{"edge_saturated_supports": 3624, "inherited_source_exclusions": 3760, "inherited_target_accepts": 4164, "minor_controls": 10872, "necessary_supports": 5842, "new_source_exclusions": 0, "new_target_accepts": 0, "original_ordered_joins": 3548, "over_budget_original_joins": 1848, "retained_supports": 2082, "separated_cells": 7, "source_excluded_cells": 8}`

新推導為紙面必要不等式；本表不新增來源排除或 target 接受。
