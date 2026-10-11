# Figure 1 的固定 minor 控制

BASE：`4dd11f422c6fa49265a412085116b088786d0344`。程式只用 Python 標準函式庫。正式 PDF Figure 1 的圖形另以實際高解析度影像核對；每次 stretch 將指定 bold edge subdivide **兩次**，不是一次。

本批不枚舉來源圖，只對固定 seeds 指定的有限參數重播：

| 固定種子 | 允許伸長邊 | 每邊 stretch 次數 | 控制數 |
|---|---|---|---:|
| Figure 1 左圖 `D-left` | `s−a0,s−a1,s−a2` | `0,1,2` | 27 |
| Figure 1 中圖 `D-middle` | `s−u0,s−u1,s−u2,u0−a0,u1−a1,u2−a2` | `0,1,2` | 729 |
| Figure 1 右圖 `D-spindle` | 無 bold edge | 不伸長 | 1 |
| complete `K4` | 不適用 | 不伸長 | 1 |

總共 **758** 個。左右 `ai` triangle 的三邊皆為 thin edges，未伸長。沒有對 spindle 或其他邊加入伸長。

`D-left` 與 `D-middle` 的 `K4` branch sets 是全部三臂內點加 `s` 的 connected center bag，以及三個 singleton `a0,a1,a2`。spindle 的具名邊為兩份 diamond：`s−l0,s−l1,l0−l1,l0−l2,l1−l2`，右側以 `r` 同樣接線，另有 `l2−r2`。其四個 bags 是 `{s},{l0},{l1},{l2,r2,r0,r1}`；第四組由原橋及右 diamond 連通，`s−r0` 提供它與第一組的鄰接。

每張固定 `H` 的每個內點 `v`，依 `d_target(v)−d_H(v)` 添加到原有序五環 `b0,…,b4` 的實際 spokes：`s` target degree=5，其他 target degree=4。完整證書逐點保存所有實際附件。然後以同一原 `M` 的前四個 bags 加第五組 `B` 保存 `K5` minor，含每組 spanning tree 及全部十個原邊跨組 witnesses。`H` 的 `K4` 亦保存全部六個 witnesses。重播獨立逐組核對原邊、連通、互斥、complete adjacencies、induced `B=C5`、完整 degrees 及 `H` 二連通。

每個 minor claim 標為 **triggered and holds**。每個原題 disk domain 標為 **not triggered**：已顯式得到原 `M` 的 `K5` minor，所以这些 synthetic degree-completing lifts 非平面。沒有 colouring、β 拒絕、disk realization 或一般 unbounded completeness claim。

生成一次使用 `--write`，output directory 和每個產物檔都採 exclusive create；既有目錄會使生成失敗。`--check --seed 17` 只讀證書，以 seed 17 改變驗證順序。重播前後程式與輸入 JSON hashes 完全相同。實際 Python 為 `3.14.7`，兩次程序 exit code 均為 `0`。argv 使用 subprocess 的 argument array，沒有 shell 字串插值。

```bash
PYTHONDONTWRITEBYTECODE=1 python3 audits/2026-10-11-c5-single-deficit-biconnected-5e7a5ffd/agents/existing_results_overlap/minor_controls.py --check --seed 17
```

三個 in-memory tamper negatives 均為 **triggered and holds**：非原圖 cross edge、互相重疊的 branch sets、錯誤完整 degree metadata，validator 皆拒絕。第三項的拒絕為裸 `AssertionError`，其 log 中訊息字串為空；檢查失敗和無訊息均被完整保留。這些 negatives 沒有改寫原證書。

交付檔案：

- `minor_controls.py`：可重播程式。
- `minor-controls/certificates.json`：全部 758 個完整證書。
- `minor-controls/manifest.json`：BASE、程式及正式 PDF hash、argv、tamper negatives。
- `minor-controls-write.log`：生成 stdout/stderr、argv、exit code。
- `minor-controls-check-seed17.log`：唯讀重播 stdout/stderr、argv、exit code、輸入 hashes 未變紀錄。
- `minor-controls-delivery.json`：以上程式、JSON、logs 的 bytes 及 SHA256。

有限控制與任意 stretch 的紙面構造應分別讀取；758 次通過不是 unbounded proof，也不是原題 disk 來源不存在的單獨證明。
