# 球面覆蓋的外部與實作依賴

2026-10-13，獨立唯讀稽核。新證明採用完整 19／20／21 點最小度五球面域，
不繼承原 K13 的 h 分支紙面縮減。

## 官方來源核對

- [plantri guide](https://users.cecs.anu.edu.au/~bdm/plantri/plantri-guide.txt)：
  `-m5` 為預設三連通最小度五球面三角剖分；`-c5` 另限五連通。
- [minimum-five 原論文](https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf)：
  Theorems 1、3 及修正後 Theorem 2 處理完整構造，包括分離三／四環。
  使用結構生成／縮減、Barnette–Butler 與 canonical construction path，
  不以四色定理或四色可約配置作前提。
- [plantri 生成綜述](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf)：
  §2、Figures 6–7 說明 min4 與 min5 全域。Table 1 在 20／21 點的全域
  計數 73／192 不同於五連通域 71／187；與本輪域相符，但數量吻合不代替完備性。

保留生成定理、C 實作與執行證據三層，未宣稱 Lean 認證或工具實作無誤已形式化。

## 已核對的實作

K13/K14/K15 凍結的 plantri `min5_dispatch` 把未指定 connectivity 預設為 3，
進 `scanmin5`，包含分離四環及三環；未設定 `-c5`。
min4 第二路的 `min5_filter.c` 只定義完成輸出階段的 `FILTER`／`SUMMARY`，
按全部點 degree≥5 過濾，不改遞迴生成分支。

三個 primary checker 都遍歷每張輸入球面圖的每個五度 root。K13 的額外
collar assertions 全部通過；沒有條件不符即跳過來源的分支。K14/K15 同樣
没有按 h 或 mask 剪枝。保存根圖明確包括 h=0,1,2。

## 本輪實際重播

primary 三份 `check.py --check` 均重新計算全部 fibres 並與既有證書比較，
4,021 根圖、40,210 列、845,866 full lifts 全部通過。
獨立 reviewer 另完成：

```bash
python3 -B audits/2026-10-13-k13-collar-50d5474/independent/check.py --check
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/compare.py
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/compare.py
```

三者均 PASS；未重跑兩路圖生成。生成的完備性與來源仍採納既有凍結 plantri
及既有雙路生成紀錄。沒有修改任何原球面證書。
