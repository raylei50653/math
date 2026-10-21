# W7 專用 CPU 算子

`w7_operator.py` + `kernels.cpp` 實作固定模型的 `A=[D;Q_selected]` 與其
adjoint，不建立 D 或 Q 的稀疏矩陣。所有原 state、half-row、X 欄編號保留。
首次使用由本機 `g++` 編譯；只需 NumPy，轉成 SciPy `LinearOperator` 時才需 SciPy。
編譯旗標不含 `fast-math`；浮點結果仍須接受一般累加誤差。

```python
from w7_operator import W7Operator

op = W7Operator(backend="direct", positive=tuple(range(10)))
workspace = op.workspace()
ax = op.matvec(x)                    # 長度 122626
aty = op.rmatvec(y)                  # 長度 307197
op.matvec_into(x, ax, workspace)     # 迭代時重用緩衝區
op.rmatvec_into(y, aty, workspace)
z = op.recover_z(x)                  # live state 原順序；D x=0 時才相容
linear_op = op.aslinearoperator()
```

`positive=()` 只取 D；`positive=(9,)` 只加 target；也可指定任意不重複、
有序的正量列。`reference="mindeg"` 與 `"h2"` 都支援。每個 reference
沿用原程式將其餘兩個 half-row 依 encoded order 排序的規則。

兩個後端提供相同 API：

- `direct`：編譯後的單位係數 gather sums，forward 使用 C 的 CSR 索引，
  adjoint 使用其原 CSC 索引；省去浮點係數及顯式 D/Q。
- `template`：333 種非空形狀共用局部 CSR/CSC，批次 gather、相加、scatter；
  數值索引陣列較小。每個實例仍保有獨立變數。

本機完整十列的 float64 測速如下，詳 [normal.json](normal.json)；獨立測速的
正向＋轉置總加速約為 direct 1.44 倍、template 1.26 倍，見
[wrapper-review.json](../algebra/wrapper-review.json)。這些只量測算子呼叫。

| 模式 | 正向 median | 轉置 median | 兩方向數值陣列 |
| --- | ---: | ---: | ---: |
| SciPy CSR | 3.17 ms | 2.61 ms | 115.4 MB |
| 專用 direct | 2.33 ms | 1.57 ms | 36.4 MB |
| 專用 template | 2.56 ms | 2.20 ms | 8.17 MB |

MB 採十進位；native 額外 workspace 分別約 1.47／2.83 MB。上表排除 Python
及編譯器／共享函式庫開銷，沒有把陣列比值當作整體 RSS 或求解加速比。

forward 先算 `h=Cx`，再產生每個 state 的兩個差分及
`Q_l x=sum_s P_l[s] h_ref(s)`。adjoint 先將差分與正量列回填至同一組
half-rows，再算 `C^T h`。因此 Q 的尺度是 `2PZ`；原正量下界仍為 2。

`*_into` 會拒絕錯誤長度、非 float64 輸出、唯讀輸出、過小緩衝區及記憶體重疊。
同時呼叫時，每次使用獨立 workspace。算子初始化核對凍結 cache／模板 SHA256
以及全部 scatter 座標恰出現一次。

從 repository root 重播：

```bash
audits/2026-10-20-w7-count-opt-d5b8a86/py -B \
  audits/2026-10-21-w7-reuse-d5b8a86/specialized/check.py --benchmark
PYTHONHASHSEED=17 audits/2026-10-20-w7-count-opt-d5b8a86/py -B \
  audits/2026-10-21-w7-reuse-d5b8a86/specialized/check.py --seed 17
```

核對涵蓋兩後端 × 兩 reference × 四種正量選擇、整數精確相等、一般浮點誤差、
adjoint、Z 回復、`LinearOperator` 及污染／格式反控制。測速為單執行緒 CPU
float64，7 批、每批 25 次；兩側都配置一份輸出，native workspace 重用。
setup 另計。數值陣列 bytes 不等於程序 RSS。

現有 HiGHS、OR-Tools PDLP、cuOpt 包裝都要求顯式稀疏陣列；本算子可直接用於
殘差、pricing 或接受 matvec callback 的迭代法。此交付沒有改寫既有求解器。
任何數值解仍須轉成原座標整數證書，交既有 independent checker 核對。

已用 [run_pdhg.py](run_pdhg.py) 實跑一次 60 秒可行性修整，全部十項正量皆保留。
13207 次迭代、約 220 次／秒；最佳抽查殘差從 2.99e-8 降至 2.60e-9，
但 X>1e-9 的欄數由 170466 增至約 262687。這仍是數值點，沒有精確證書。
[結果](runs/feasibility-60s/result.json) 及 vectors.npz 保留最佳與最終點。
若另行重跑，必須使用新的 `--name`，不覆寫本次輸出：

```bash
audits/2026-10-20-w7-count-opt-d5b8a86/py -B \
  audits/2026-10-21-w7-reuse-d5b8a86/specialized/run_pdhg.py \
  --name NEW_EXCLUSIVE_NAME --seconds 60
```
