# 2026-10-30：Zarankiewicz 旋轉與超額重播

權威論證：[旋轉與超額報告](../../docs/zarankiewicz_rotation_excess.md)。
此目錄包含固定輸入與精確有限重播；沒有一般不可避免性或低交叉畫法證書。

| 檔案 | 來源及範圍 |
| --- | --- |
| [integer_tensor.json](integer_tensor.json) | 共同二元端點對張量；C=79；未含獨立原邊匹配、旋轉或嵌入 |
| [integer_replay.json](integer_replay.json) | 全部 proper 子集下界、奇×奇奇偶、雙側 S/P/H 及所有 Rt 通過 |
| [rotation_lift.json](rotation_lift.json) | 上述固定張量兩側均無三元方向旋轉提升；含四鄰點四星局部證書 |
| [rotation_budget.json](rotation_budget.json) | 明列四星旋轉的 antisum21、必要超額至少1；寬鬆 pseudo-tight 模型 UNSAT |
| [planarization.json](planarization.json) | 七份實際來源正控制、四份負控制及同來源兩側超額核對 |
| `planar_K2_*.json`、`straight_K*.json` | 完整來源包；straight 包另保留產生來源的整數座標 |

重播及更新固定輸出：

```bash
python3 scripts/zarankiewicz_integer_replay.py --output audits/2026-10-30-zarankiewicz-rotation-excess/integer_replay.json
python3 scripts/zarankiewicz_rotation_lift.py --output audits/2026-10-30-zarankiewicz-rotation-excess/rotation_lift.json
python3 scripts/zarankiewicz_rotation_budget.py --output audits/2026-10-30-zarankiewicz-rotation-excess/rotation_budget.json
python3 scripts/zarankiewicz_planarization.py --write-controls audits/2026-10-30-zarankiewicz-rotation-excess
```

整數張量的存在與其旋轉提升失敗可以同時成立。
旋轉、tight 或 pseudo-tight 的必要模型通過也不代表已有完整畫法。
