# 2026-09-28：共鄰端點 K2 的 w 側兩條 spoke、實際支援與雙列分離

接手 main@104c8bcccb32486dbddd7d23183c47b0c7282526，保留前輪全部尚未提交
的 singleton／mixed K2 成果。依 HANDOFF 處理共鄰端點型 t_w=2、(1)
的 18 筆原必要資料。未 commit／push，未開 sub-agents，未重啟大圖枚舉。

## 結果與證明界線

[報告](../c5_adjacent_degree5_mixed_edge_shared_t2.md) 先給任意大小的來源化約。
C_z 禁色非空、容量二，原 z–u–B 外部 hub 排除 K4，degree-list 緊性
與 Gallai 葉塊迫使 actual support 至少見兩個 q 色。C_w 恰禁 {3}，
支援穩定子迫使見三個 q 色。外部依賴為
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，本輪核對原文。

原 diamond 的四點各有避開其餘 diamond 的 B 路徑，因此其外面必為
z–w–u–v–z，chord zu 在內側；原 unary 均在外側。六單位次序為
C_z、perm(C_w,s_h,s_d)、u、v 或反向，C_z 保留兩個有序接點。
跨度為至少 1、2、1，總和≤5；兩條 w-spokes 與 u 是原零跨度單位。
沒有把 u 誤當兩條 boundary spokes，也沒有把 actual support 填成整弧。

| 證書項目 | 結果 |
| --- | ---: |
| 原 t_w=2、(1) 關係資料 | 18 |
| 兩條 w-spokes 落點不同的幾何配置 | 280 |
| 有相容支援／無相容支援的原關係資料 | 8／10 |
| q 必要支援資料／不同六支援配置 | 38／30 |
| 使用的原局部 K2 支援 | 12／28 |
| 指定 target 查詢／未決 | 76／0 |
| target 完整禁色集合候選接合 | 202，全部接受 |
| 反射支援／反射 target 查詢 | 38／76 |
| 原局部見證的共同色框核對 | 4,848 |
| 每份 C_z 的具名接點方向 | 2 |

幾何域由遞增區間與獨立 cyclic hull masks／w 區塊區間兩種算法核對。
跨列相容時搬運整個原關係；不相容時保留容量及支援穩定子的完整 F 上界。
每組候選都保存同一 (z,w,u,v) witness，直接檢查包含 chord zu 的全部
原局部接線，並由 root 不在完整 F 中推出原 unary 的完整 tuple 存在。
沒有選取獨立的端點 marginals，也沒有將局部 witness 當成任意來源的顯式著色。

本型 **必接受 p₁=01021、p₂=01212，不需 T4**。38 筆均作雙列檢查，
沒有先用 T4 或雙禁色 K5 排除難項；未證這些必要資料 disk 可實現。
10 筆原關係的支援集合為空，是此子型的必要支援矛盾，未改寫前輪表。
原 306／288 筆、9,312 q schemas 與 28 組局部 K2 支援證書保持原內容。

README、STATUS、HANDOFF、degree-5 導讀、介面及前序報告均接上新入口。
條件式單側出口新增第八類，明用來源雙缺失與刪邊繼承才推出完整
Σ(M)=Ω∖{q}。一般出口及主命題仍未證，沒有新增 Lean theorem。

## 驗證

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

五份 checker 已通過，新 JSON／Markdown 表逐 byte 重播相同。
`lake build` 通過（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 247 份 Markdown／2,775 個本地連結；DocGraph 通過 43 份
metadata 文件／117 條關係／5 families，零錯誤。HANDOFF 維持 149 行。
`git diff --check` 通過；新增五份 source／報告／歷史／JSON／表另核對
trailing whitespace 與 EOF，全通過。Lean 建置沒有形式化本輪新論證。

沿用且未重跑：各一接點 mixed K2／四環次序、singleton 同側／12／34／40、
三接點與唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、抽象 profiles／
閉包、Lean axiom audit 與來源圖枚舉；沒有修改它們的 checker 或證書。

## 精確停止點

t_w=2、(1) 完成任意大小支援化約與雙列分離。下一窄型為
**t_w=1、(2) 的 36 筆**：保留兩份二接點完整關係、原 diamond 外側環序
與 w-spoke，再使用飽和雙禁色的原 bridge／逐塊 actual supports。
其餘 w 分拆、其他 mixed、一般雙 root、degree≥6、非相鄰 roots 及一般
單側／共同出口仍保留；優先序只見 [HANDOFF](../HANDOFF.md)。
