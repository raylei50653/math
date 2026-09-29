# D–E 五正跨度與飽和原路徑來源排除

全部必要支援全 source K5；0 target 查詢。必要表不宣稱 disk 實現。

| ID | 原 join | Cz / Dz / Cw / Dw / Ew | 飽和原分量 |
| ---: | ---: | --- | --- |
| 0 | 432 | 01 / 04 / 12 / 23 / 34 | Cz, Dz |
| 1 | 434 | 01 / 04 / 12 / 23 / 34 | Cz, Dz |
| 2 | 433 | 01 / 04 / 12 / 34 / 23 | Cz, Dz |
| 3 | 435 | 01 / 04 / 12 / 34 / 23 | Cz, Dz |
| 4 | 432 | 01 / 04 / 23 / 12 / 34 | Cz, Dz |
| 5 | 434 | 01 / 04 / 23 / 12 / 34 | Cz, Dz |
| 6 | 433 | 01 / 04 / 23 / 34 / 12 | Cz, Dz |
| 7 | 435 | 01 / 04 / 23 / 34 / 12 | Cz, Dz |
| 8 | 436 | 01 / 04 / 34 / 12 / 23 | Cz, Dz |
| 9 | 437 | 01 / 04 / 34 / 12 / 23 | Cz, Dz |
| 10 | 436 | 01 / 04 / 34 / 23 / 12 | Cz, Dz |
| 11 | 437 | 01 / 04 / 34 / 23 / 12 | Cz, Dz |
| 12 | 626 | 04 / 01 / 12 / 23 / 34 | Cz, Dz |
| 13 | 628 | 04 / 01 / 12 / 23 / 34 | Cz, Dz |
| 14 | 627 | 04 / 01 / 12 / 34 / 23 | Cz, Dz |
| 15 | 629 | 04 / 01 / 12 / 34 / 23 | Cz, Dz |
| 16 | 626 | 04 / 01 / 23 / 12 / 34 | Cz, Dz |
| 17 | 628 | 04 / 01 / 23 / 12 / 34 | Cz, Dz |
| 18 | 627 | 04 / 01 / 23 / 34 / 12 | Cz, Dz |
| 19 | 629 | 04 / 01 / 23 / 34 / 12 | Cz, Dz |
| 20 | 630 | 04 / 01 / 34 / 12 / 23 | Cz, Dz |
| 21 | 631 | 04 / 01 / 34 / 12 / 23 | Cz, Dz |
| 22 | 630 | 04 / 01 / 34 / 23 / 12 | Cz, Dz |
| 23 | 631 | 04 / 01 / 34 / 23 / 12 | Cz, Dz |
| 24 | 499 | 23 / 34 / 01 / 04 / 12 | Cz, Dz |
| 25 | 501 | 23 / 34 / 01 / 04 / 12 | Cz, Dz |
| 26 | 498 | 23 / 34 / 01 / 12 / 04 | Cz, Dz |
| 27 | 500 | 23 / 34 / 01 / 12 / 04 | Cz, Dz |
| 28 | 502 | 23 / 34 / 04 / 01 / 12 | Cz, Dz |
| 29 | 503 | 23 / 34 / 04 / 01 / 12 | Cz, Dz |
| 30 | 502 | 23 / 34 / 04 / 12 / 01 | Cz, Dz |
| 31 | 503 | 23 / 34 / 04 / 12 / 01 | Cz, Dz |
| 32 | 498 | 23 / 34 / 12 / 01 / 04 | Cz, Dz |
| 33 | 500 | 23 / 34 / 12 / 01 / 04 | Cz, Dz |
| 34 | 499 | 23 / 34 / 12 / 04 / 01 | Cz, Dz |
| 35 | 501 | 23 / 34 / 12 / 04 / 01 | Cz, Dz |
| 36 | 981 | 34 / 23 / 01 / 04 / 12 | Cz, Dz |
| 37 | 983 | 34 / 23 / 01 / 04 / 12 | Cz, Dz |
| 38 | 980 | 34 / 23 / 01 / 12 / 04 | Cz, Dz |
| 39 | 982 | 34 / 23 / 01 / 12 / 04 | Cz, Dz |
| 40 | 984 | 34 / 23 / 04 / 01 / 12 | Cz, Dz |
| 41 | 985 | 34 / 23 / 04 / 01 / 12 | Cz, Dz |
| 42 | 984 | 34 / 23 / 04 / 12 / 01 | Cz, Dz |
| 43 | 985 | 34 / 23 / 04 / 12 / 01 | Cz, Dz |
| 44 | 980 | 34 / 23 / 12 / 01 / 04 | Cz, Dz |
| 45 | 982 | 34 / 23 / 12 / 01 / 04 | Cz, Dz |
| 46 | 981 | 34 / 23 / 12 / 04 / 01 | Cz, Dz |
| 47 | 983 | 34 / 23 / 12 / 04 / 01 | Cz, Dz |

## 原 ID 纖維

| 原 join | 支援數 | 分類 |
| ---: | ---: | --- |
| 432 | 2 | source_K5_excluded |
| 433 | 2 | source_K5_excluded |
| 434 | 2 | source_K5_excluded |
| 435 | 2 | source_K5_excluded |
| 436 | 2 | source_K5_excluded |
| 437 | 2 | source_K5_excluded |
| 468 | 0 | no_compatible_disk_support |
| 469 | 0 | no_compatible_disk_support |
| 470 | 0 | no_compatible_disk_support |
| 471 | 0 | no_compatible_disk_support |
| 472 | 0 | no_compatible_disk_support |
| 473 | 0 | no_compatible_disk_support |
| 498 | 2 | source_K5_excluded |
| 499 | 2 | source_K5_excluded |
| 500 | 2 | source_K5_excluded |
| 501 | 2 | source_K5_excluded |
| 502 | 2 | source_K5_excluded |
| 503 | 2 | source_K5_excluded |
| 534 | 0 | no_compatible_disk_support |
| 535 | 0 | no_compatible_disk_support |
| 536 | 0 | no_compatible_disk_support |
| 537 | 0 | no_compatible_disk_support |
| 538 | 0 | no_compatible_disk_support |
| 539 | 0 | no_compatible_disk_support |
| 626 | 2 | source_K5_excluded |
| 627 | 2 | source_K5_excluded |
| 628 | 2 | source_K5_excluded |
| 629 | 2 | source_K5_excluded |
| 630 | 2 | source_K5_excluded |
| 631 | 2 | source_K5_excluded |
| 662 | 0 | no_compatible_disk_support |
| 663 | 0 | no_compatible_disk_support |
| 664 | 0 | no_compatible_disk_support |
| 665 | 0 | no_compatible_disk_support |
| 666 | 0 | no_compatible_disk_support |
| 667 | 0 | no_compatible_disk_support |
| 688 | 0 | no_compatible_disk_support |
| 689 | 0 | no_compatible_disk_support |
| 690 | 0 | no_compatible_disk_support |
| 691 | 0 | no_compatible_disk_support |
| 692 | 0 | no_compatible_disk_support |
| 693 | 0 | no_compatible_disk_support |
| 724 | 0 | no_compatible_disk_support |
| 725 | 0 | no_compatible_disk_support |
| 726 | 0 | no_compatible_disk_support |
| 727 | 0 | no_compatible_disk_support |
| 728 | 0 | no_compatible_disk_support |
| 729 | 0 | no_compatible_disk_support |
| 806 | 0 | no_compatible_disk_support |
| 807 | 0 | no_compatible_disk_support |
| 808 | 0 | no_compatible_disk_support |
| 809 | 0 | no_compatible_disk_support |
| 810 | 0 | no_compatible_disk_support |
| 811 | 0 | no_compatible_disk_support |
| 836 | 0 | no_compatible_disk_support |
| 837 | 0 | no_compatible_disk_support |
| 838 | 0 | no_compatible_disk_support |
| 839 | 0 | no_compatible_disk_support |
| 840 | 0 | no_compatible_disk_support |
| 841 | 0 | no_compatible_disk_support |
| 862 | 0 | no_compatible_disk_support |
| 863 | 0 | no_compatible_disk_support |
| 864 | 0 | no_compatible_disk_support |
| 865 | 0 | no_compatible_disk_support |
| 866 | 0 | no_compatible_disk_support |
| 867 | 0 | no_compatible_disk_support |
| 892 | 0 | no_compatible_disk_support |
| 893 | 0 | no_compatible_disk_support |
| 894 | 0 | no_compatible_disk_support |
| 895 | 0 | no_compatible_disk_support |
| 896 | 0 | no_compatible_disk_support |
| 897 | 0 | no_compatible_disk_support |
| 980 | 2 | source_K5_excluded |
| 981 | 2 | source_K5_excluded |
| 982 | 2 | source_K5_excluded |
| 983 | 2 | source_K5_excluded |
| 984 | 2 | source_K5_excluded |
| 985 | 2 | source_K5_excluded |
| 1016 | 0 | no_compatible_disk_support |
| 1017 | 0 | no_compatible_disk_support |
| 1018 | 0 | no_compatible_disk_support |
| 1019 | 0 | no_compatible_disk_support |
| 1020 | 0 | no_compatible_disk_support |
| 1021 | 0 | no_compatible_disk_support |
| 1052 | 0 | no_compatible_disk_support |
| 1053 | 0 | no_compatible_disk_support |
| 1054 | 0 | no_compatible_disk_support |
| 1055 | 0 | no_compatible_disk_support |
| 1056 | 0 | no_compatible_disk_support |
| 1057 | 0 | no_compatible_disk_support |
| 1078 | 0 | no_compatible_disk_support |
| 1079 | 0 | no_compatible_disk_support |
| 1080 | 0 | no_compatible_disk_support |
| 1081 | 0 | no_compatible_disk_support |
| 1082 | 0 | no_compatible_disk_support |
| 1083 | 0 | no_compatible_disk_support |
| 1160 | 0 | no_compatible_disk_support |
| 1161 | 0 | no_compatible_disk_support |
| 1162 | 0 | no_compatible_disk_support |
| 1163 | 0 | no_compatible_disk_support |
| 1164 | 0 | no_compatible_disk_support |
| 1165 | 0 | no_compatible_disk_support |
| 1190 | 0 | no_compatible_disk_support |
| 1191 | 0 | no_compatible_disk_support |
| 1192 | 0 | no_compatible_disk_support |
| 1193 | 0 | no_compatible_disk_support |
| 1194 | 0 | no_compatible_disk_support |
| 1195 | 0 | no_compatible_disk_support |
| 1220 | 0 | no_compatible_disk_support |
| 1221 | 0 | no_compatible_disk_support |
| 1222 | 0 | no_compatible_disk_support |
| 1223 | 0 | no_compatible_disk_support |
| 1224 | 0 | no_compatible_disk_support |
| 1225 | 0 | no_compatible_disk_support |
| 1246 | 0 | no_compatible_disk_support |
| 1247 | 0 | no_compatible_disk_support |
| 1248 | 0 | no_compatible_disk_support |
| 1249 | 0 | no_compatible_disk_support |
| 1250 | 0 | no_compatible_disk_support |
| 1251 | 0 | no_compatible_disk_support |
| 1324 | 0 | no_compatible_disk_support |
| 1325 | 0 | no_compatible_disk_support |
| 1326 | 0 | no_compatible_disk_support |
| 1327 | 0 | no_compatible_disk_support |
| 1328 | 0 | no_compatible_disk_support |
| 1329 | 0 | no_compatible_disk_support |
| 1350 | 0 | no_compatible_disk_support |
| 1351 | 0 | no_compatible_disk_support |
| 1352 | 0 | no_compatible_disk_support |
| 1353 | 0 | no_compatible_disk_support |
| 1354 | 0 | no_compatible_disk_support |
| 1355 | 0 | no_compatible_disk_support |
| 1376 | 0 | no_compatible_disk_support |
| 1377 | 0 | no_compatible_disk_support |
| 1378 | 0 | no_compatible_disk_support |
| 1379 | 0 | no_compatible_disk_support |
| 1380 | 0 | no_compatible_disk_support |
| 1381 | 0 | no_compatible_disk_support |
| 1402 | 0 | no_compatible_disk_support |
| 1403 | 0 | no_compatible_disk_support |
| 1404 | 0 | no_compatible_disk_support |
| 1405 | 0 | no_compatible_disk_support |
| 1406 | 0 | no_compatible_disk_support |
| 1407 | 0 | no_compatible_disk_support |

[完整證書](observations.json)；[前提與證明](../../docs/c5_adjacent_degree5_no_mixed_de.md)。
