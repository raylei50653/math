# 2026-09-29：Root degree 超額預算、樹引理與 136 份入口的支援覆蓋

後續提交整理與驗證沿用範圍見 [發布核對](2026-09-29-root-degree-excess-publish.md)；下文保留研究當輪語境。

接手 `/home/ray/developer/ai/math`，HEAD=`30a2e59`，初始工作樹乾淨。
讀 HANDOFF、STATUS 及 Git 狀態後，核對使用者提出的上層結構，
再推進指定 no-mixed t_z=2,(2)、t_w=1,(2,1) 的 136 份入口。
未開 sub-agents、Graphify 或大圖枚舉；未 commit／push。

## 理論與證據邊界

[預算報告](../c5_root_degree_excess.md) 補齊精確消去、source spokes
異色、F⊆A、一般 root 的 |E_r|≤deg_Q(r)，包括 Q 單點的證明。
得到 D+O+κ=degree−4 及總超額公式。樹上 edge-minimal list obstruction
等價於 incident 邊標色互異且其聯集恰為 E_r，故樹骨架 κ=0。
還記錄逐列的完整半樹關係遞迴；不把 q 的 singleton 搬成 p 的 spoke。

兩個主引理為初等任意大小紙面證明。一般骨架全部 κ=0 的 Gallai
推論另依外部定理，本輪核對 Dvořák Theorem 10。三層工作假設 A／B／C
仍未證成，也未新增 Lean theorem。

[樹 checker](../../scripts/c5_root_degree_excess.py) 以完整半樹遞迴
對照直接 literal colorings oracle，重建 233,744 份 list assignments，
恰有 113 份 edge-minimal 拒絕。每份保存邊標色及逐邊刪除染色，
另獨立枚舉 proper edge labels 核對反向。原 149 份側預算全核對；
118 份平面必要側型含 94 份 (D,O,κ)=(1,0,0)、24 份 (0,1,0)。
此為 list 控制，不是 C5 原圖窮盡。

## 原 136 份資料與新的停止點

[支援報告](../c5_adjacent_degree5_no_mixed_t2_t1.md)、
[checker](../../scripts/c5_adjacent_degree5_no_mixed_t2_t1.py)、
[JSON](../../artifacts/c5_adjacent_degree5_no_mixed_t2_t1/observations.json) 及
[表格](../../artifacts/c5_adjacent_degree5_no_mixed_t2_t1/support_table.md)
保存三份原分量、五接點、三條 root-spokes、zw 與共同色框。
每側 (D,O,κ)=(1,0,0)；w 的二接點 C_w 缺額一，單接點 D_w 飽和。

兩種獨立幾何算法同得 3,150 份實際支援／placements。原 136 份
中 66 份有支援，產生 560 份必要支援；70 份原參數型纖維空，
包括原首項 sides=(133,91)。原 IDs、SHA、全部原資料保留。
兩份 pair 的完整 95-schema 表、支援穩定子、singleton 的整份 relation、
具名 root rotations 均保存；沒有把 D_w 壓成 spoke。

1,120 個 target 中，724 個以完整關係搬運關閉，278 個以搬運加容量
上界關閉，合計 1,002。其餘 118 個查詢有 146 組失敗候選：
empty_z 60、empty_w 68、same_singleton 18；本輪沒有兩側同時空的候選。
442 份為 A/A、59 份 ?/A、59 份 A/?；1,120 次字面共同反射核對。
560 份支援未另做來源排除，沒有新增 minor 證書或出口類別。

下一窄入口是 record 14／p₁：原子表 ID=42、原 retained-join ID=3192、
原 sides=(137,118)，B_z=04、B_w=3，支援 (01,123,34)，c=3。
source F 為 ({1},{0},{2})；p₁ 的 F_z=F_D={1} 精確，唯一失敗候選
是 F_w={0,3} 導致 E_w=∅。保留 D_w 的 34 支援及原路徑，研究
同一 C_w 的 singleton／pair 拒絕證書相容性。p₂ 已接受。
必要支援沒有來源實現保證；全分拆／root 樹分離與主命題仍開放。

## 實際驗證

新兩層先生成，再 `--check` 逐 byte 重算。以下五個 checker 均通過，
原 no-mixed、t=2 及 interfaces artifacts 保持原 bytes。
`lake build` 通過（8,827 jobs），只見原 SymRelabel／AttachmentOrder
style／unused simp warnings；未新增 Lean 檔。

```bash
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

文件檢查通過（287 份 Markdown、3,105 個本地連結）；DocGraph 通過
（56 documents、177 relations、5 families，0 errors／notes），
`git diff --check` 及新增 source／報告的空白檢查通過，HANDOFF 為 149 行。
未重跑 t=2 bridge／endpoints／path-palettes，其他 singleton／唯一
degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、profiles／閉包及 Lean
axiom audit。已完成 t=2 的 644 個延拓沿用原報告及發布紀錄，
本輪 t=2 checker 重播的是支援／容量基層，輸出的 512 並未取代最終 644。
