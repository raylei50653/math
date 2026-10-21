# 探索檔的權威界線

`discovery.py`／`discovery.json` 是第一輪只翻Y缺側完整分量的局部診斷。
`discovery-orbit.json` 保留後續在同一原完整partition內翻全部boundary-touch
components的探索結果；`discovery-free.json`另把Y設為boundary-free控制。
它們不由正式checker讀取，也不作來源排除的單獨authority。

正式數學來源為 `BASE.json`／`frozen/`；排除短證為 `PROOF.md`；完整數據的
可重播authority為 `check.py`／`certificate.json`。後者獨立重建全部250份
分支、完整同E strip/cap kernels及固定單分量G01021 witness。
