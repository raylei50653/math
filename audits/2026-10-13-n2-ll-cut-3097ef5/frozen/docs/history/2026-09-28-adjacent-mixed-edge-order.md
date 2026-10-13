# 2026-09-28：原四環外側次序排除唯一 mixed K2 各一接點型

接手 main@104c8bcccb32486dbddd7d23183c47b0c7282526，保留前輪 singleton
與 mixed K2 的未提交成果。從 HANDOFF 的一色側 t=2、(1) 入手，先證
原四環外側的任意大小支援次序，再建立有限 checker。未 commit／push，
未開 sub-agents，未重啟圖 catalogue 或唯一 degree-5 枚舉。

## 結果與證據界線

[證明報告](../c5_adjacent_degree5_mixed_edge_order.md) 給來源排除：
有限簡單 induced-C5 disk、q=01012、edge-minimal q-obstruction，恰兩個
相鄰完整 degree-5 roots z、w，其餘內點 degree=4；唯一 mixed 原分量
為 uv，root incidence 恰為 zu、wv。**此來源不存在，不需 T4。**
原 K2 端點共鄰兩 root 等其他 incidence 不在此定理範圍內。

原四環內側空，外側 annulus 使每個 unary 分量及 u、v 的實際支援
各佔同序的框弧；總跨度≤5。F={3} 的支援見全部三個 q 色，至少佔
兩段。原定 t=2 型兩側各有一份 F={3}，加 u、v 得 2+2+1+1>5，
故其 36 筆抽象資料全排除。其餘正常形同樣受此界限。

前輪 576 筆中，552 筆超周長；只餘兩側各一條 spoke、各一份二接點
分量的 24 筆。周長飽和使支援跨度恰為 1,1,1,2。大側 C_l 見三色，
其支援只可能 234、340、401；配合原四環正反序共六型。四型的 mixed
缺色相同，另兩型的一色側 C_s 未見其 residual 色 2，均矛盾。

任意大小覆蓋來自紙面 Jordan／支援論證；Gallai、tight degree lists
及前輪原路徑 K5 沿用外部 degree-list 定理，本輪核對 Dvořák 講義
Lemma 7／Theorem 10。Python 只核對固定域、原 ID 接合與有限幾何；
沒有新增 Lean theorem，`lake build` 不形式化新拓撲證明。

| 證書項目 | 結果 |
| --- | ---: |
| 前輪平面必要資料／本輪全部排除 | 576／576 |
| 周長超限／飽和次序矛盾 | 552／24 |
| 原定一色側 t=2、(1) 的抽象資料 | 36，全部涵蓋 |
| 四單位 cyclic hull 的獨立框邊 mask 幾何 | 360 |
| 原四環飽和次序幾何／大側 q 相容幾何 | 10／6 |
| 剩餘 24 筆逐幾何核對 | 240，全部矛盾 |
| 反射原資料／反射幾何 | 576／10 |
| t=2 放寬四支援域／通過環序 | 3,240／0 |

3,240 是兩份九種 {3} 支援乘四十組具名 mixed 支援；不是完整來源
枚舉，也不與 576 筆乘成圖數。原 816／576 證書不改寫，新 JSON 保存
原 ID、原 z/w/u/v 身份與分量禁色、spoke 候選、二接點方向及直接輸入
SHA256。共享框點可作相鄰單位的共同端點，另有總跨度五的正控制。

README、STATUS、HANDOFF、degree-5 導讀及介面／出口報告均接上新成果。
單側出口 §5 的失敗核心限制排除此接線型；既有七類定理無須增加空的
第八類。一般單側／共同出口、一般雙 root 與主命題仍未證。

## 驗證

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

五份 checker 已全通過；新 JSON／Markdown 表逐 byte 重播相同。
`lake build` 通過（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 241 份 Markdown／2,731 個本地連結；DocGraph 通過 41 份
metadata 文件／108 條關係／5 families，零錯誤。HANDOFF 保持 150 行。
`git diff --check` 與五份新增檔案的 trailing whitespace／EOF 檢查通過。

沿用且未重跑：no-spoke 支援表 checker（本輪獨立重算四單位幾何）、
singleton 同側／三份長弧 checker、唯一 degree-5 完成表、雙拒絕 atlas、
R 系列大覆蓋、抽象 profiles／閉包、圖枚舉與 Lean axiom audit。

## 精確停止點

唯一 mixed 原 K2 各一接點型已完成 disk 來源排除。下一窄入口為唯一
mixed K2 的共鄰端點接線 P*ᶻ={u,v}、P*ʷ={u}；先保留共鄰 u 的同一
身份，重推完整 ordered tuples／mixed 關係與逐邊 minimality。
不能沿用各一接點的禁對公式，亦不能假設兩端各有兩條 boundary 邊。
其他較大／多 mixed、無 mixed、非相鄰雙 root、degree≥6 及一般出口
仍保留。當前優先序只見 [HANDOFF](../HANDOFF.md)。
