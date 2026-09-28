# 唯一 mixed K2：原四環外側次序的來源排除

此表重播必要資料的排除；任意大小來源覆蓋見證明報告，不是來源圖枚舉。

| (一色側 t, 分拆, 兩色側 t, 分拆) | 原資料數 | 最小總跨度 | 排除 |
| --- | ---: | ---: | --- |
| `(0, (1, 1, 1), 0, (2, 1))` | 144 | 9 | perimeter_excess |
| `(0, (1, 1, 1), 1, (2,))` | 72 | 8 | perimeter_excess |
| `(0, (2, 1), 0, (2, 1))` | 72 | 7 | perimeter_excess |
| `(0, (2, 1), 1, (2,))` | 36 | 6 | perimeter_excess |
| `(1, (1, 1), 0, (2, 1))` | 96 | 8 | perimeter_excess |
| `(1, (1, 1), 1, (2,))` | 48 | 7 | perimeter_excess |
| `(1, (2,), 0, (2, 1))` | 48 | 6 | perimeter_excess |
| `(1, (2,), 1, (2,))` | 24 | 5 | saturated_order_conflict |
| `(2, (1,), 0, (2, 1))` | 24 | 7 | perimeter_excess |
| `(2, (1,), 1, (2,))` | 12 | 6 | perimeter_excess |

## 飽和後的六種 q 相容大側支援

ps、pl 分別為一色側、兩色側的原 mixed 端點；原 z/w/u/v 身份見 JSON。

| 幾何 ID | Cs | ps | pl | Cl | 缺色 d,e | 矛盾 |
| ---: | --- | --- | --- | --- | --- | --- |
| 4 | 04 | 01 | 12 | 234 | 2,2 | equal_missing_colors |
| 5 | 12 | 01 | 04 | 234 | 2,1 | small_support_misses_residual |
| 6 | 01 | 12 | 23 | 034 | 2,2 | equal_missing_colors |
| 7 | 23 | 12 | 01 | 034 | 2,2 | equal_missing_colors |
| 8 | 12 | 23 | 34 | 014 | 2,0 | small_support_misses_residual |
| 9 | 34 | 23 | 12 | 014 | 2,2 | equal_missing_colors |
