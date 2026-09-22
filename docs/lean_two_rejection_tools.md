# 雙拒絕證明的 Lean 共用工具

2026-09-22。對照 [雙拒絕分類](c5_two_rejection_proof_zh.md)。
本輪補上 [TwoRejectionTools.lean](../Math/TwoRejectionTools.lean)，沿用
`ForcingLists.ListColorable` 與 `RootInterfaces` 的同圖共同著色語義。
這是一般引理層；**完整 disk 分類仍是紙面證明**。不以外部定理的
`axiom` 或 `sorry` 假裝完成形式化。

## 定理對照

下列名稱均位於 `FiveBoundary.TwoRejectionTools`。

| 紙面步驟 | Lean 定理 | 精確輸入與結果 |
| --- | --- | --- |
| §1 貪婪法 | `listColorable_of_removable` | 有限圖的每個非空頂點子集，都有一點在子集內的鄰點數小於 list 大小，則可 list 著色；以刪點歸納真正構造著色 |
| §1 嚴格餘量 | `listColorable_of_connected_slack` | 連通有限圖、每點 list 大小至少為鄰點數、一點嚴格大於，即可著色；由 walk 證明每個不含該點的非空子集都有外出邊 |
| §1 拒絕迫緊 | `lists_tight_of_rejection` | 同一連通 degree-list 問題不可染，則每點 list 大小恰為鄰點數 |
| §1 度數／附件 | `tight_of_no_slack` | 明確輸入完整度數上界、框色 image 大小及 list 補集大小，推出完整度數 4、list 緊、框色 image 與實際附件等大 |
| §2 兩端口計數 | `two_port_count` | 非空分量集合滿足 `2 × 分量數 + Σ excess = 2` 時，恰一個分量且各 excess 為零；森林身分與 port 恆等式仍須另證 |
| §5 strip 寬度 | `interval_width_sum` | 任意長自然數區間序列，已知各區間合法且前右端不超過後左端，推出寬度和不超過首尾跨度 |
| §6–7 路徑大小 | `path_size_bounds` | `n≥2` 下，旁支寬度界推出 `n=2`；或 `n≤3` 加偶數性推出 `n=2` |
| §6 刪葉矛盾 | `not_two_singleton_rejections` | 同一可染核心、同一 lists 與 root，不可能拒絕兩個不同的 singleton 葉色；明確保留核心可染前提 |
| §6–7 框列比較 | `boundary_lists_eq` | 兩框列在每個實際附件上相同，則整個內圖 lists 相同；沒有合併框點 2／4 |

`two_port_count` 的 `excess` 是每個樹分量內所有 block 的
`|V(B)|−2` 總和，不是已形式化的 block-cut forest。`interval_width_sum`
只處理已給定的次序，沒有把 planarity 偷換成自然數不等式。
`not_two_singleton_rejections` 使用既有完整 contact relation 的禁色語義，
其葉接合意義由 `RootInterfaces.mem_forbidden_single_iff` 給出；
不能將兩個不同圖的 root 集代入同一前提。

## 未完成的形式化依賴

1. 實際 boundary attachments 到完整度數／補集基數的圖層連接，以及 image
   等基數到框色單射的接線實例化。
2. 外部 degree-list 不可染圖的 Gallai block 分解及共同 palettes 定理。
3. 從實際 block-cut tree 建立 D、證 forest／port 恆等式，抽出唯一交替橋鏈
   並導出偶數路徑。
4. 末端 odd-cycle／K4 的具名 disk 拓撲排除，以及旁支唯一性。
5. Jordan strip 次序、旁支收縮保框與實際附件聯集；刪葉後圖的連通性及
   list 餘量，才能套用本輪貪婪法。
6. 把以上連成唯一二內點分類、十二列簽章 1855 與四目標排除的 Lean 定理。

這些缺口未用條件式「分類定理」或未證公理掩蓋。3703、R31、共同出口
及 `K∞=K≤5` 的研究停止點不變。

## 重播與信任

```bash
lake build
lake env lean Math/TwoRejectionToolsAudit.lean
uv run --with networkx==3.6.1 python scripts/c5_two_rejection_audit.py --check
uv run python scripts/c5_sector_terminal_blocks.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
git diff --check
```

[Audit](../Math/TwoRejectionToolsAudit.lean) 逐一列出新增定理的 axioms。
Lean 工具與原 Python atlas 重播分開：後者仍信任 NetworkX 3.6.1 的
atlas／planarity，不能證任意大小分類。未改寫舊證書、603 profiles 或固定點。
