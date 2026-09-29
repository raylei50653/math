# C–E 五正跨度與飽和原路徑來源排除

全部必要支援全 source K5；0 target 查詢。必要表不宣稱 disk 實現。

| ID | 原 join | Cz / Dz / Cw / Dw / Ew | 飽和原分量 |
| ---: | ---: | --- | --- |
| 0 | 104 | 01 / 04 / 12 / 23 / 34 | Dz |
| 1 | 106 | 01 / 04 / 12 / 23 / 34 | Dz |
| 2 | 366 | 01 / 04 / 12 / 23 / 34 | Cz |
| 3 | 368 | 01 / 04 / 12 / 23 / 34 | Cz |
| 4 | 105 | 01 / 04 / 12 / 34 / 23 | Dz |
| 5 | 107 | 01 / 04 / 12 / 34 / 23 | Dz |
| 6 | 367 | 01 / 04 / 12 / 34 / 23 | Cz |
| 7 | 369 | 01 / 04 / 12 / 34 / 23 | Cz |
| 8 | 104 | 01 / 04 / 23 / 12 / 34 | Dz |
| 9 | 106 | 01 / 04 / 23 / 12 / 34 | Dz |
| 10 | 366 | 01 / 04 / 23 / 12 / 34 | Cz |
| 11 | 368 | 01 / 04 / 23 / 12 / 34 | Cz |
| 12 | 105 | 01 / 04 / 23 / 34 / 12 | Dz |
| 13 | 107 | 01 / 04 / 23 / 34 / 12 | Dz |
| 14 | 367 | 01 / 04 / 23 / 34 / 12 | Cz |
| 15 | 369 | 01 / 04 / 23 / 34 / 12 | Cz |
| 16 | 108 | 01 / 04 / 34 / 12 / 23 | Dz |
| 17 | 109 | 01 / 04 / 34 / 12 / 23 | Dz |
| 18 | 370 | 01 / 04 / 34 / 12 / 23 | Cz |
| 19 | 371 | 01 / 04 / 34 / 12 / 23 | Cz |
| 20 | 108 | 01 / 04 / 34 / 23 / 12 | Dz |
| 21 | 109 | 01 / 04 / 34 / 23 / 12 | Dz |
| 22 | 370 | 01 / 04 / 34 / 23 / 12 | Cz |
| 23 | 371 | 01 / 04 / 34 / 23 / 12 | Cz |
| 24 | 196 | 04 / 01 / 12 / 23 / 34 | Dz |
| 25 | 198 | 04 / 01 / 12 / 23 / 34 | Dz |
| 26 | 564 | 04 / 01 / 12 / 23 / 34 | Cz |
| 27 | 566 | 04 / 01 / 12 / 23 / 34 | Cz |
| 28 | 197 | 04 / 01 / 12 / 34 / 23 | Dz |
| 29 | 199 | 04 / 01 / 12 / 34 / 23 | Dz |
| 30 | 565 | 04 / 01 / 12 / 34 / 23 | Cz |
| 31 | 567 | 04 / 01 / 12 / 34 / 23 | Cz |
| 32 | 196 | 04 / 01 / 23 / 12 / 34 | Dz |
| 33 | 198 | 04 / 01 / 23 / 12 / 34 | Dz |
| 34 | 564 | 04 / 01 / 23 / 12 / 34 | Cz |
| 35 | 566 | 04 / 01 / 23 / 12 / 34 | Cz |
| 36 | 197 | 04 / 01 / 23 / 34 / 12 | Dz |
| 37 | 199 | 04 / 01 / 23 / 34 / 12 | Dz |
| 38 | 565 | 04 / 01 / 23 / 34 / 12 | Cz |
| 39 | 567 | 04 / 01 / 23 / 34 / 12 | Cz |
| 40 | 200 | 04 / 01 / 34 / 12 / 23 | Dz |
| 41 | 201 | 04 / 01 / 34 / 12 / 23 | Dz |
| 42 | 568 | 04 / 01 / 34 / 12 / 23 | Cz |
| 43 | 569 | 04 / 01 / 34 / 12 / 23 | Cz |
| 44 | 200 | 04 / 01 / 34 / 23 / 12 | Dz |
| 45 | 201 | 04 / 01 / 34 / 23 / 12 | Dz |
| 46 | 568 | 04 / 01 / 34 / 23 / 12 | Cz |
| 47 | 569 | 04 / 01 / 34 / 23 / 12 | Cz |
| 48 | 13 | 23 / 34 / 01 / 04 / 12 | Dz |
| 49 | 15 | 23 / 34 / 01 / 04 / 12 | Dz |
| 50 | 367 | 23 / 34 / 01 / 04 / 12 | Cz |
| 51 | 369 | 23 / 34 / 01 / 04 / 12 | Cz |
| 52 | 12 | 23 / 34 / 01 / 12 / 04 | Dz |
| 53 | 14 | 23 / 34 / 01 / 12 / 04 | Dz |
| 54 | 366 | 23 / 34 / 01 / 12 / 04 | Cz |
| 55 | 368 | 23 / 34 / 01 / 12 / 04 | Cz |
| 56 | 16 | 23 / 34 / 04 / 01 / 12 | Dz |
| 57 | 17 | 23 / 34 / 04 / 01 / 12 | Dz |
| 58 | 370 | 23 / 34 / 04 / 01 / 12 | Cz |
| 59 | 371 | 23 / 34 / 04 / 01 / 12 | Cz |
| 60 | 16 | 23 / 34 / 04 / 12 / 01 | Dz |
| 61 | 17 | 23 / 34 / 04 / 12 / 01 | Dz |
| 62 | 370 | 23 / 34 / 04 / 12 / 01 | Cz |
| 63 | 371 | 23 / 34 / 04 / 12 / 01 | Cz |
| 64 | 12 | 23 / 34 / 12 / 01 / 04 | Dz |
| 65 | 14 | 23 / 34 / 12 / 01 / 04 | Dz |
| 66 | 366 | 23 / 34 / 12 / 01 / 04 | Cz |
| 67 | 368 | 23 / 34 / 12 / 01 / 04 | Cz |
| 68 | 13 | 23 / 34 / 12 / 04 / 01 | Dz |
| 69 | 15 | 23 / 34 / 12 / 04 / 01 | Dz |
| 70 | 367 | 23 / 34 / 12 / 04 / 01 | Cz |
| 71 | 369 | 23 / 34 / 12 / 04 / 01 | Cz |
| 72 | 197 | 34 / 23 / 01 / 04 / 12 | Dz |
| 73 | 199 | 34 / 23 / 01 / 04 / 12 | Dz |
| 74 | 919 | 34 / 23 / 01 / 04 / 12 | Cz |
| 75 | 921 | 34 / 23 / 01 / 04 / 12 | Cz |
| 76 | 196 | 34 / 23 / 01 / 12 / 04 | Dz |
| 77 | 198 | 34 / 23 / 01 / 12 / 04 | Dz |
| 78 | 918 | 34 / 23 / 01 / 12 / 04 | Cz |
| 79 | 920 | 34 / 23 / 01 / 12 / 04 | Cz |
| 80 | 200 | 34 / 23 / 04 / 01 / 12 | Dz |
| 81 | 201 | 34 / 23 / 04 / 01 / 12 | Dz |
| 82 | 922 | 34 / 23 / 04 / 01 / 12 | Cz |
| 83 | 923 | 34 / 23 / 04 / 01 / 12 | Cz |
| 84 | 200 | 34 / 23 / 04 / 12 / 01 | Dz |
| 85 | 201 | 34 / 23 / 04 / 12 / 01 | Dz |
| 86 | 922 | 34 / 23 / 04 / 12 / 01 | Cz |
| 87 | 923 | 34 / 23 / 04 / 12 / 01 | Cz |
| 88 | 196 | 34 / 23 / 12 / 01 / 04 | Dz |
| 89 | 198 | 34 / 23 / 12 / 01 / 04 | Dz |
| 90 | 918 | 34 / 23 / 12 / 01 / 04 | Cz |
| 91 | 920 | 34 / 23 / 12 / 01 / 04 | Cz |
| 92 | 197 | 34 / 23 / 12 / 04 / 01 | Dz |
| 93 | 199 | 34 / 23 / 12 / 04 / 01 | Dz |
| 94 | 919 | 34 / 23 / 12 / 04 / 01 | Cz |
| 95 | 921 | 34 / 23 / 12 / 04 / 01 | Cz |

## 原 ID 纖維

| 原 join | 支援數 | 分類 |
| ---: | ---: | --- |
| 12 | 2 | source_K5_excluded |
| 13 | 2 | source_K5_excluded |
| 14 | 2 | source_K5_excluded |
| 15 | 2 | source_K5_excluded |
| 16 | 2 | source_K5_excluded |
| 17 | 2 | source_K5_excluded |
| 48 | 0 | no_compatible_disk_support |
| 49 | 0 | no_compatible_disk_support |
| 50 | 0 | no_compatible_disk_support |
| 51 | 0 | no_compatible_disk_support |
| 52 | 0 | no_compatible_disk_support |
| 53 | 0 | no_compatible_disk_support |
| 78 | 0 | no_compatible_disk_support |
| 79 | 0 | no_compatible_disk_support |
| 80 | 0 | no_compatible_disk_support |
| 81 | 0 | no_compatible_disk_support |
| 82 | 0 | no_compatible_disk_support |
| 83 | 0 | no_compatible_disk_support |
| 104 | 2 | source_K5_excluded |
| 105 | 2 | source_K5_excluded |
| 106 | 2 | source_K5_excluded |
| 107 | 2 | source_K5_excluded |
| 108 | 2 | source_K5_excluded |
| 109 | 2 | source_K5_excluded |
| 140 | 0 | no_compatible_disk_support |
| 141 | 0 | no_compatible_disk_support |
| 142 | 0 | no_compatible_disk_support |
| 143 | 0 | no_compatible_disk_support |
| 144 | 0 | no_compatible_disk_support |
| 145 | 0 | no_compatible_disk_support |
| 170 | 0 | no_compatible_disk_support |
| 171 | 0 | no_compatible_disk_support |
| 172 | 0 | no_compatible_disk_support |
| 173 | 0 | no_compatible_disk_support |
| 174 | 0 | no_compatible_disk_support |
| 175 | 0 | no_compatible_disk_support |
| 196 | 4 | source_K5_excluded |
| 197 | 4 | source_K5_excluded |
| 198 | 4 | source_K5_excluded |
| 199 | 4 | source_K5_excluded |
| 200 | 4 | source_K5_excluded |
| 201 | 4 | source_K5_excluded |
| 232 | 0 | no_compatible_disk_support |
| 233 | 0 | no_compatible_disk_support |
| 234 | 0 | no_compatible_disk_support |
| 235 | 0 | no_compatible_disk_support |
| 236 | 0 | no_compatible_disk_support |
| 237 | 0 | no_compatible_disk_support |
| 258 | 0 | no_compatible_disk_support |
| 259 | 0 | no_compatible_disk_support |
| 260 | 0 | no_compatible_disk_support |
| 261 | 0 | no_compatible_disk_support |
| 262 | 0 | no_compatible_disk_support |
| 263 | 0 | no_compatible_disk_support |
| 284 | 0 | no_compatible_disk_support |
| 285 | 0 | no_compatible_disk_support |
| 286 | 0 | no_compatible_disk_support |
| 287 | 0 | no_compatible_disk_support |
| 288 | 0 | no_compatible_disk_support |
| 289 | 0 | no_compatible_disk_support |
| 314 | 0 | no_compatible_disk_support |
| 315 | 0 | no_compatible_disk_support |
| 316 | 0 | no_compatible_disk_support |
| 317 | 0 | no_compatible_disk_support |
| 318 | 0 | no_compatible_disk_support |
| 319 | 0 | no_compatible_disk_support |
| 340 | 0 | no_compatible_disk_support |
| 341 | 0 | no_compatible_disk_support |
| 342 | 0 | no_compatible_disk_support |
| 343 | 0 | no_compatible_disk_support |
| 344 | 0 | no_compatible_disk_support |
| 345 | 0 | no_compatible_disk_support |
| 366 | 4 | source_K5_excluded |
| 367 | 4 | source_K5_excluded |
| 368 | 4 | source_K5_excluded |
| 369 | 4 | source_K5_excluded |
| 370 | 4 | source_K5_excluded |
| 371 | 4 | source_K5_excluded |
| 402 | 0 | no_compatible_disk_support |
| 403 | 0 | no_compatible_disk_support |
| 404 | 0 | no_compatible_disk_support |
| 405 | 0 | no_compatible_disk_support |
| 406 | 0 | no_compatible_disk_support |
| 407 | 0 | no_compatible_disk_support |
| 564 | 2 | source_K5_excluded |
| 565 | 2 | source_K5_excluded |
| 566 | 2 | source_K5_excluded |
| 567 | 2 | source_K5_excluded |
| 568 | 2 | source_K5_excluded |
| 569 | 2 | source_K5_excluded |
| 600 | 0 | no_compatible_disk_support |
| 601 | 0 | no_compatible_disk_support |
| 602 | 0 | no_compatible_disk_support |
| 603 | 0 | no_compatible_disk_support |
| 604 | 0 | no_compatible_disk_support |
| 605 | 0 | no_compatible_disk_support |
| 750 | 0 | no_compatible_disk_support |
| 751 | 0 | no_compatible_disk_support |
| 752 | 0 | no_compatible_disk_support |
| 753 | 0 | no_compatible_disk_support |
| 754 | 0 | no_compatible_disk_support |
| 755 | 0 | no_compatible_disk_support |
| 780 | 0 | no_compatible_disk_support |
| 781 | 0 | no_compatible_disk_support |
| 782 | 0 | no_compatible_disk_support |
| 783 | 0 | no_compatible_disk_support |
| 784 | 0 | no_compatible_disk_support |
| 785 | 0 | no_compatible_disk_support |
| 918 | 2 | source_K5_excluded |
| 919 | 2 | source_K5_excluded |
| 920 | 2 | source_K5_excluded |
| 921 | 2 | source_K5_excluded |
| 922 | 2 | source_K5_excluded |
| 923 | 2 | source_K5_excluded |
| 954 | 0 | no_compatible_disk_support |
| 955 | 0 | no_compatible_disk_support |
| 956 | 0 | no_compatible_disk_support |
| 957 | 0 | no_compatible_disk_support |
| 958 | 0 | no_compatible_disk_support |
| 959 | 0 | no_compatible_disk_support |
| 1104 | 0 | no_compatible_disk_support |
| 1105 | 0 | no_compatible_disk_support |
| 1106 | 0 | no_compatible_disk_support |
| 1107 | 0 | no_compatible_disk_support |
| 1108 | 0 | no_compatible_disk_support |
| 1109 | 0 | no_compatible_disk_support |
| 1134 | 0 | no_compatible_disk_support |
| 1135 | 0 | no_compatible_disk_support |
| 1136 | 0 | no_compatible_disk_support |
| 1137 | 0 | no_compatible_disk_support |
| 1138 | 0 | no_compatible_disk_support |
| 1139 | 0 | no_compatible_disk_support |
| 1272 | 0 | no_compatible_disk_support |
| 1273 | 0 | no_compatible_disk_support |
| 1274 | 0 | no_compatible_disk_support |
| 1275 | 0 | no_compatible_disk_support |
| 1276 | 0 | no_compatible_disk_support |
| 1277 | 0 | no_compatible_disk_support |
| 1298 | 0 | no_compatible_disk_support |
| 1299 | 0 | no_compatible_disk_support |
| 1300 | 0 | no_compatible_disk_support |
| 1301 | 0 | no_compatible_disk_support |
| 1302 | 0 | no_compatible_disk_support |
| 1303 | 0 | no_compatible_disk_support |

[完整證書](observations.json)；[前提與證明](../../docs/c5_adjacent_degree5_no_mixed_ce.md)。
