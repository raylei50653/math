# 2026-09-28：相鄰雙 root 的唯一共鄰單點化約

接手 HEAD `104c8bc`，起始 main 工作樹乾淨，與本地 origin/main 對齊。
本輪未 commit／push，未開 sub-agents；沒有重新查遠端發布狀態。
以當前 [HANDOFF](../HANDOFF.md) 為準，舊記憶的 record 110 停止點已過時。

## 結果與證據

[報告](../c5_adjacent_degree5_shared_singleton.md) 接續雙 root 完整介面，
固定同一原來源、共鄰點身份、全部接點及共同色框。

1. 單 root 分量的禁色為完整 tuple 關係的精確投影；mixed 分量每欄／每行
   的禁色數不超過對應 root 接點數。消去 unary 分量後，各 root 剩餘色數
   至少為 mixed incidence 數，對每個 boundary row 都成立。
2. 唯一 mixed 分量為共鄰 singleton x 時，令 T 是其 q 兩色 list。
   兩側剩餘色集皆非空且包含於 T，至少一側恰為 T；每個 unary 分量都須
   有 T 外私有色。故每側至多一條 spoke，必要分拆只有 (2)、(3)、(2,1)。
3. 原路徑 r–x–b_i 提供連通外部，沿用三接點 active triangle 與 K5
   抽取排除 (3)，平面來源每側只剩 (2) 或 (2,1)。此步依賴外部
   [degree-list 定理 Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
   本輪已重新核對連通、degree assignment 與 blockwise-uniform 前提。
4. 任意列 β 的拒絕恰為兩側同色 singleton，或 x 的兩色 list 同時包含
   兩側剩餘色集。target 重色使 x 全開後仍有前一種障礙，不能宣稱分離完成。

## 有限控制

[checker](../../scripts/c5_adjacent_degree5_shared_singleton.py) 與
[artifact](../../artifacts/c5_adjacent_degree5_shared_singleton/observations.json)
保存 checker 與直接輸入的 SHA256。

| 核對項目 | 數量 |
| --- | ---: |
| 單側原始容量候選 | 209 |
| 三種 T 的有序兩側代數組合 | 131,043 |
| minimality 關係資料 | 375 |
| (3) 來源排除後的必要資料 | 240 |
| mixed 逐欄／逐行容量 | 各 7,680 |
| unary 精確投影 | 240 |
| 任意列拒絕判準 | 2,250 |
| 一張實際 minimal q-core 的 boundary rows | 240 |
| 該圖逐邊刪後完整 coloring | 25 |
| 原共鄰點路徑 K5 skeletons | 100 |
| 移除 rx 後指定 witness 失效 | 100 |

240 筆是未綁定實際支援／環序的必要代數資料，各有序分拆組合 60 筆。
實際圖控制完整 degree 為 (5,5,4,4,4,4,4,4,4)，但有明示 K5 minor，
不是 disk／T4 正控制。minor skeletons 也不是完整 degree-list 來源。

## 驗證與未重跑範圍

```bash
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_no_spoke_exterior.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新證書生成後逐 byte 重播通過。前序雙 root 介面、三接點、no-spoke 外部
路徑三份 checker 均通過，沿用各自原 artifact，沒有改寫既有分類計數。
`lake build` 通過（8,827 jobs），只有既存 AttachmentOrder／SymRelabel
linter warnings。文件檢查通過 224 份 Markdown／2,598 個本地連結；
DocGraph 通過 35 份 metadata 文件／86 條關係／5 families。
HANDOFF 為 136 行；`git diff --check` 及四份新增檔案的 whitespace／EOF
檢查通過。文件檢查的數字包含本輪 degree-5 導讀後續入口。

沒有重跑唯一 degree-5 的其他完成表、指定 p 大覆蓋、R 系列、雙拒絕
atlas、profiles／閉包、來源圖枚舉或 Lean axiom audit。未新增 Lean theorem；
建置與有限控制不把上述紙面結論提升為 Lean 形式化或來源可實現性。

## 精確停止點

唯一 mixed 共鄰 singleton 的任意大小必要化約已完成。
下一步在兩側 (2)／(2,1) 下保留原 x 的兩個具名 boundary 鄰點與全部
unary 實際支援，處理指定 p 的兩側同色 singleton 障礙：先取 p₁ 的
x 支援 {b1,b4}、p₂ 的 x 支援 {b2,b4}，此時 x 的 target 約束全開。
本子類的 p 分離、較大／多 mixed 分量、一般雙 root、一般出口及主命題仍未證。
