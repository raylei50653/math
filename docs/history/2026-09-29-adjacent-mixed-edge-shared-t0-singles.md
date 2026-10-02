# 2026-09-29：共鄰端點 K2 的 t_w=0、(1,1,1)，六跨度來源排除

接手 main@c178cf1，工作目錄為專案根目錄；保留前兩輪
t_w=1、(1,1) 與 t_w=0、(2,1) 尚未提交的 checker、證書與文件變更。
先讀 HANDOFF、STATUS、文件規則與前輪完整論證，沿原 108 筆正常形
推進；未重開大圖枚舉、未使用 Graphify、未開 sub-agents、未 commit／push。

## 結果與證據層

[報告](../c5_adjacent_degree5_mixed_edge_shared_t0_singles.md) 保留原 diamond
zw、wu、uv、vz、zu，C_z 的兩個具名接點與 w 的三份不同單接點分量。
每份 unary 支援至少見兩個 q 色；三份 w 禁色恰分割 U∖{e}，所以
有一份禁 {3}，其 actual support 必看見全部三個 q 色。
原 diamond 外側 annulus 的同序支援給總跨度≤5，但四份 unary 加 v
需要至少 1+(1+1+2)+1=6，故整型任意大小來源不存在。

| 項目 | 結果 |
| --- | ---: |
| 原正常形 ID／完整記錄綁定 | 108 |
| 最小所需跨度／框周長 | 6／5 |
| 來源排除／保留必要支援 | 108／0 |
| 空的原正常形纖維 | 108 |
| 獨立無次序五單位 hull packings | 120 |
| 兩算法共同的同序幾何／placements | 60／60 |
| 原正常形與幾何逐筆接合 | 6,480，全矛盾 |
| 原正常形／幾何反射 | 108／60 |
| 三份具名 w 分量排列對照 | 648 |
| 共同色框 q 接合核對 | 2,592 |
| target 查詢 | 0，不計為接受查詢 |
| 新 pair K5 排除／T4 使用 | 0／否 |

紙面任意大小論證＋外部 degree-list 定理＋Python 有限證書；未新增
Lean theorem，也沒有獨立第二審稿者。支援下界仍用已有局部 K4-free
論證及原 r–u–b_i 外部 hub，不將「不用 pair K5」誤寫成不需平面性。
本輪重讀 Dvořák Lemma 7／Theorem 10 第 5–6 頁；web 讀取逾時後，
下載同一 [原始 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
並用 pdftotext 核對。有限幾何不是可實現的 degree/list disk 來源。

原 shared JSON SHA256 保持
`6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`。
本輪新增 checker／JSON／逐筆排除表／報告，接上 README、STATUS、
HANDOFF、前序通知與出口第八類。四份前序證書因文件通知刷新
inputs_sha256；與編輯前快照去除此欄後逐欄完全相同，所有變更雜湊
均只指向 docs。原有限數學資料與前兩輪未提交成果保留。

## 驗證

下列十一個 checker 均已實際執行通過，JSON／Markdown byte-identical。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 已完成 8,827 jobs，只有既有 AttachmentOrder／SymRelabel
lint warnings；它不形式化本輪拓撲證明。DocGraph 已核對 47 份 metadata
文件、136 條關係、5 families，0 errors／0 notes。
文件檢查通過：260 份 Markdown、2,890 個本地連結；HANDOFF 恰 150 行。
`git diff --check` 通過。前序四份證書只更新文件雜湊，數學資料完全相同。

未重跑其他相鄰 mixed／singleton 子類、唯一 degree-5 完成表、雙拒絕
atlas、R 系列大覆蓋、抽象 profiles／閉包及 Lean axiom audit；本輪不是
全庫研究重驗。

## 停止點

zu、zv、wu 接線的五種 w 正常形已全完成，出口第八類移除 w-spoke
及分拆限制。完整 Σ(M)=Ω∖{q} 仍另用來源雙缺失與刪邊繼承。
下一窄入口為唯一 mixed K2 的 P*ᶻ=P*ʷ={u}，兩 root 都只接 u、v 有
三個 boundary 附件；先重推完整 tuples 與逐邊 minimality，本輪未推進
這份新接線。一般單側／共同出口及 K∞=K≤5 仍未證。
