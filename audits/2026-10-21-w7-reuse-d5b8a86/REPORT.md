# W7 可復用結構與專用算子

2026-10-21；BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`。
已找到可精確重用的局部結構，並實作編譯後的 CPU 正向／轉置算子。
本輪只寫入本目錄；[BASE.json](BASE.json) 記錄工作前既有 dirty 狀態與輸入 SHA256。
同一來源、完整 fibres、全部原附件及十個共同正量的數學合同沿用
[原模型](../2026-10-20-w7-count-cone-d5b8a86/MODEL.md)。既有必要錐維持 OPEN。

## 可直接使用的專用算子

[w7_operator.py](specialized/w7_operator.py) 呼叫 [C++ 核心](specialized/kernels.cpp)，
提供 `matvec/rmatvec`、重用 workspace 的 `*_into`、`recover_z` 與 SciPy
`LinearOperator`；[用法與重播](specialized/README.md)。完整模型
`A=[D;Q_0;…;Q_9]` 大小為 122626×307197，不必建立顯式 D/Q。

原座標與 reference 規則完整保留。`direct` 後端共用 C 的單位係數求和；
`template` 後端共用相同局部形狀的 CSR/CSC，將 gather、批次相加與 scatter
移入編譯核心。兩者的 half-row 結果再融合每個 state 的差分與正量行。
adjoint 使用對應的反向回填與 C 轉置。

完整 wrapper 的測速見 [normal.json](specialized/normal.json)：單執行緒 CPU
float64、7×25 次取 median，setup 另計；兩側均配置輸出，native 重用 workspace。
實際時間依本機與執行負載而變；數值陣列儲存量另列，不當作 RSS。
這組測速未包含求解；下節另列專用算子上的 60 秒數值迭代，沒有求解器整體加速比。
本機正向／轉置分別為 SciPy 3.17／2.61 ms、direct 2.33／1.57 ms、template
2.56／2.20 ms。獨立測速合計加速約 direct 1.44 倍、template 1.26 倍。
數值陣列兩方向共用量分別為 SciPy 115.4 MB、direct 36.4 MB、template
8.17 MB；native 額外 workspace 分別約 1.47／2.83 MB。

兩後端、兩 reference、空／target／重排三列／完整十列共 16 組，均核對整數
forward、transpose、adjoint 與 Z 回復；一般浮點結果以誤差界核對。
污染 column map 會造成比較失敗；錯誤長度、複數輸入、錯誤輸出型別、唯讀輸出、
過小／重疊 workspace 及重複／bool 正量編號均被拒絕。
[獨立審查](review/SPECIALIZED_OPERATOR.md) 釘死 Q 的尺度及 adjoint 合同。

## 實際 60 秒可行性修整

[run_pdhg.py](specialized/run_pdhg.py) 使用 `direct` 算子執行
`min 0, DX=0, QX≥2, X≥0` 的對角預條件 PDHG。從既有 all-cu-pdlp 的原 X
接續，dual 初始化零；原 `min ΣX` 的 dual 不挪用。以 `B=|L|C≥|A|` 的
行列和給安全步長，無需建立 D/Q；其縮放後算子範數至多 eta=0.99。

[完整結果](specialized/runs/feasibility-60s/result.json)：60.00 秒共 13207 次迭代，
約 220 次／秒。全部保存為數值探索，既有必要錐維持 OPEN。

| 量測 | 原近似點 | 最佳抽查點 | 最終點 |
| --- | ---: | ---: | ---: |
| 最大方程／正性殘差 | 2.9883e-8 | 2.5968e-9 | 4.5236e-9 |
| 正量下界違反 | 6.41e-11 | 0 | 0 |
| X>1e-9 的欄數 | 170466 | 262687 | 262415 |

最佳抽查殘差降低約 11.5 倍；在固定五秒觀測間隔以外未宣稱全程最優。
最終平衡 L2 由 9.78e-7 降至 6.43e-8。`vectors.npz` 同時保留原座標的
final X、best X、final dual 與 reference；input.json 記錄 warm/source SHA。
這是可行性修整，sum X 由 15452.44250 略增至 15452.44787，不是目標值改善。
密度明顯增加，未化解精確證書需要的稀疏／基底問題；沒有因浮點殘差很小而
輸出可行／不可行裁定。本次只跑一輪，未延長或重啟求解。
由[顯式 A 獨立重算](review/trial-review.json)確認步長界、各項殘差及完整輸入 SHA。

## 六種模板與 335 種受限形狀

每個交換欄保留 rim 的 binary palette membership。將相鄰同 palette 的強制
交替段收縮，只剩偶數個 runs；局部欄族依 2、4、…、12 段分成六種。
原始 428506 次生成只需 5033 種模板欄，透過字面 phase、palette word 與
原 state／column map 展開。這是局部係數共用，沒有合併獨立 X 變數。

全部 199290 個 half-rows 與 307197 個存活欄逐項重建；原始完整生成的
ordered SHA256 也相同。加入目前零 fibres 後，4095 個 palette words
只有 335 種 live-row masks，333 種非空。相同局部形狀只需快取 696389 個
incidence entries，原展開為 4264208 個，重用率約 6.12 倍。
這個比例不是總記憶體或執行時間的加速比。

[模板報告](templates/REPORT.md)、[完整映射與核對結果](templates/report.json)
及 [獨立重建](review/REPORT.md) 保留所有原座標與空 fibres。
先前純 Python/SciPy 批次版本在公平 float64 比較中較慢；專用編譯核心避免其
多次 Python 呼叫。整數／浮點係數混用的早期測速不採作速度證據。

## 可供下一步消元的精確秩結構

| Runs | 模板 rows | 模板 columns | 精確有理 rank |
| --- | ---: | ---: | ---: |
| 2 | 1 | 1 | 1 |
| 4 | 4 | 4 | 3 |
| 6 | 16 | 20 | 10 |
| 8 | 64 | 112 | 35 |
| 10 | 256 | 672 | 126 |
| 12 | 1024 | 4224 | 462 |

每個欄是 binary phase 空間中一個 affine subspace 的指示向量，同一 subgroup
的所有 cosets 都出現。其 Walsh span 恰由 subgroup annihilator 的 characters
組成；取所有 subgroup 的頻率聯集給出上下界相同的精確 rank。
[獨立整數變換與 character 重建](algebra/rank_review.json) 及
[直接由欄支援證明](review/fourier-review.json) 分別核對，沒有浮點 rank 閾值。

未裁切的 C block-diagonal rank 為 106470。對每個存活 block 再取
`min(live rows, live columns, universal rank)` 加總，得
`rank(C_live) ≤ 103787`。因 `D=L C_live`，122616 個 D 方程至少有
**18829 條相依（15.36%）**；加十個正量列後 rank 至多 103797。
這尚未選出全域獨立方程組或重建矩陣，不能任意刪除這個數量的方程。

重要的接合條件：變換後 X 側為零的頻率仍要求共享 Z 的對應組合為零。
只保留模板 rank 個方程而丟掉這些 Z 限制會放寬原模型。即使消去局部 X，
原非負條件也必須保留；各 palette block 不能各自選一份 Z。
此時才可安全建立局部／全域消元或 matrix-free 迭代器。

## 其他已量測結構與停止點

[代數核對](algebra/REPORT.md)：完整 D 沒有可直接合併的比例行／欄，
incidence 只有一個連通分量。原 C 有重複 half-row sums，可證 5913 個 state
相等；但消去 Z 後只少 43 條差分，nnz 少約 0.49%，不足解釋主要消元瓶頸。
既有 equitable partition 為離散，仍容許本輪精確局部模板共用。

下一個窄工作是建立共享 Z 線性限制的全域獨立基底及重建圖，量測其稀疏度後
再決定是否用於求解。本輪專用算子已可用於殘差、完整欄定價與接受 callback
的數值迭代；目前三個 solver 包裝都要求顯式 sparse arrays，未替換其內部算法。

本輪沒有新 primal／dual 證書，未排除嚴格 only-R／W7，也未建立原來源。
112 接觸型額外限制仍未加入；一般 J1/J2、較小 bad 與主命題均未推進。
沒有 Lean 修改，未重跑 `lake build` 或無關研究證書；未修改共享 docs，未 commit/push。
