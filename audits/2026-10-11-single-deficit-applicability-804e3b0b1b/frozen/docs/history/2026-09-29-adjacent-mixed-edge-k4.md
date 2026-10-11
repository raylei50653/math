# 2026-09-29：唯一 mixed K2 四 incidence 型，原 K4 與實際外部路徑

接手 main@c178cf1，工作目錄為專案根目錄；保留全部既有
未提交成果。先讀 HANDOFF、STATUS、文件規則，推進使用者指定的
P*ᶻ=P*ʷ={u,v}。未重開大圖枚舉、未使用 Graphify、未開 sub-agents、
未 commit／push。

## 結果與來源論證

[報告](../c5_adjacent_degree5_mixed_edge_k4.md) 完成此型的**一般平面來源
排除**。原 zw、uv、zu、zv、wu、wv 已形成 K4；u、v 各保留一條
boundary 邊，z、w 各有兩條離開 K4 的原邊。

關鍵補點是 boundary-free unary 的完整改色引理：由刪 zw 的染色
取得 C∪{r} 的完整染色，再整體置換 C 的顏色以配合另一份刪邊染色
的 r，便可接回任一 C-root 被刪邊；這違反 q-minimality。因此每份
unary 都有實際 boundary 附件。z、w 各取一條原外部路徑到 B，
B 加路徑內點給 K5 的第五組；其餘四組為原 K4 的四個 singleton。
所有十條鄰接都來自原邊。無需 T4、degree-list 定理或 disk 環序。

此任意大小結論為初等紙面證明。Python 只核對固定接回控制、選取
子圖、真正非平面 minimal q-core 及九組具名接線覆蓋；沒有由有限
路徑長度外推定理，未新增 Lean theorem，沒有獨立第二審稿者。

| 證書層 | 數目 |
| --- | ---: |
| boundary-free unary 固定圖 | 5 |
| 完整分量接回／共同色框置換接回 | 384／2,304 |
| 原 K4 與實際外部路徑選取子圖 | 270 |
| 刪原 K4／所選路徑邊使指定 witness 失效 | 3,420 |
| 把原 u 重複放進外部 branch set 的負控制 | 270 |
| 真正 degree=(5,5,4,…) 非平面 minimal q-core | 1 |
| 該原圖逐邊 q-染色見證 | 22 |
| 具名 K2 接線／整圖重新命名後代表 | 9／4 |
| target 查詢 | 0 |

新報告、checker、JSON、路徑表、研究紀錄均已加入。README、STATUS、
HANDOFF、介面／degree-5 導讀、前序通知與出口第八類已接上。
唯一 mixed K2 的全部接線完成：各一接點異端、同端點及四 incidence
三型作來源排除；可存在的 disk 來源可整圖重新命名成 zu、zv、wu，
再用前序雙列結果。完整 Σ 的接合仍須來源雙缺失與刪邊繼承。
既有正常形、支援與關係證書未改寫；沒有新增空的出口類別。

## 驗證

以下八個 checker 已實際通過，JSON／Markdown 重播 byte-identical。
`lake build` 通過 8,827 jobs，僅既有 AttachmentOrder／SymRelabel lint
warnings；本輪沒有 Lean 變更，build 不代表新改色／minor 論證已形式化。
文件檢查通過，HANDOFF 147 行；DocGraph 為 49 份 metadata 文件、
146 條關係、5 families，0 errors／0 notes。`git diff --check` 通過。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_k4.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_same_endpoint.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪未重跑其餘 shared-endpoint w 分拆／singleton 子類、唯一 degree-5
完成表、雙拒絕 atlas、R 系列大覆蓋、profiles／閉包及 Lean axiom audit。
前序指定雙列結果沿用各自已記錄的驗證，沒有宣稱本輪重驗全庫。

停止於唯一 mixed K2 全接線接回出口。下一窄入口為相鄰雙 root 的
無 mixed 型：先核對完整 residual E_z(q)=E_w(q)={c}，再處理兩側
飽和禁色與逐邊 minimality；原 zw、原 unary 身份、實際支援及完整
有序關係均須保留。一般單側／共同出口與 K∞=K≤5 仍未證。
