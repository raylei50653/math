# 3703：三拒絕的兩葉 triangle 鏈化約

文件導引（2026-09-23）：本報告為目前 3703 必要結構的證據入口，
3703 仍未排除；研究優先序與接手約定見 [HANDOFF](HANDOFF.md)。
本輪成果的整合發布與實際驗證範圍見
[發布紀錄](STATUS_HISTORY.md#75-3703-鏈化約整合發布)。
下文「本輪／未 commit／push」指 2026-09-22 研究當時，不代表即時 Git 狀態。

2026-09-22。由乾淨 `f5b42d4` 接手；沿用 [五目標](c5_sector_targets.md)
的十二列及 [雙拒絕分類](c5_two_rejection_proof_zh.md) 的 sector 圖類。
本輪得到任意大小的**必要結構**，尚未排除 3703。證據層為紙面證明、
外部 degree-list 定理與局部 Python/minor 證書；未新增 Lean theorem。

整合發布見 [STATUS §75](STATUS.md#75-3703-鏈化約整合發布)；文末「未
commit／push」保留為研究輪歷史，當前提交／遠端狀態以 Git 為準。

## 1. 命題與精確剩餘問題

K 有 induced 外框 Γ=(b0,…,b4) 的 disk embedding，C=K−Γ 非空連通，
內點完整 degree≤4，b0 恰有兩個不同內鄰點。以下附件用框索引表示，
`A(v)=N_K(v)∩Γ`。假設同一張圖拒絕三列

```
ρ=01201（索引 3），δ=01213（7），η=01231（8）。
```

**必要結構定理。** C 的所有點完整 degree=4；C 的 block-cut tree 是路徑，
兩端 blocks 都是 bridges。每個 block 為 bridge 或 triangle，triangles
兩兩頂點互斥。C 恰有兩個葉點，它們的附件（不計兩端方向）只能為

```
{0,1,2} 與 {2,3,4}，或
{0,2,4} 與 {2,3,4}。
```

因此 b0 的兩接點恰有一個是 C 葉點，另一個是鏈內的非葉點。
三列拒絕已自動使 α=01212 接受；但仍須在**相同完整圖**驗其餘
接受列，尤其兩個額外開口列 00102、01210。第一葉對自動接受 00102，
第二葉對自動接受 01210，另一開口列尚未解決。

未限制 triangle 數或 bridge 長度；不把此链化約當成有限狀態充分性。
下一入口是兩種葉對、第二個 b0 接點的實際位置，以及三列各自的
block palettes 聯立。沿用具名 attachments，不作獨立 root 邊際相乘。

## 2. 三列緊 lists 與附件表

對 β∈{ρ,δ,η}，`Lβ(v)=U\β(A(v))` 滿足 `|Lβ(v)|≥deg_C(v)`。
沿用連通生成樹貪婪餘量論證：拒絕迫使每點完整 degree=4、所有 lists
緊，且 β 在每個實際附件集上單射。C 不可能只有一點，因 b0 有兩個
不同內鄰點。

由 degree-list 定理，C 是 Gallai tree，各列分別有不交的 block palettes。
只用普通圖（全正邊）情形；來源是
[Schweser–Stiebitz Lemmas 2.2、2.4](https://arxiv.org/html/1507.04569v1)，
本輪重新核對原文。三列的 palette 分解不能互相替換。平面性排除 K5，
目前 blocks 只可能為 bridges、odd cycles、K4。

全部可能的二／三附件如下；大括號內是可用色。

| A | Lρ | Lδ | Lη |
| --- | --- | --- | --- |
| 01 | 23 | 23 | 23 |
| 02 | 13 | 13 | 13 |
| 04 | 23 | 12 | 23 |
| 12 | 03 | 03 | 03 |
| 23 | 13 | 03 | 01 |
| 24 | 03 | 01 | 03 |
| 34 | 23 | 02 | 02 |
| 012 | 3 | 3 | 3 |
| 024 | 3 | 1 | 3 |
| 234 | 3 | 0 | 0 |

空附件及五種單附件都合格；沒有四附件。單附件的三列色向量也兩兩不同。
特別地，表中二附件的**三列 list 向量**各異。因此同一 odd-cycle block
的全部非割點（以下稱私有點）必有同一個實際二附件 P：每列的私有 list
都是該 block 的共同 palette，再用表的單射性。這對非末端 block 也成立。

## 3. 排除所有 K4 blocks，不另假設 minimality

K4 的每個點已有三條 block 邊，完整 degree=4 使它恰有一條外接邊。
外接若非 spoke，必是 C 的 bridge；不同 K4 點的 bridge 外側分量互斥。
每個外側分量都必接到 Γ：在 block-cut tree 向外走到末端 block，取其
私有點 y；`deg_C(y)≤3`，完整 degree=4，故 A(y) 非空。若外側只有
一點，該點本身即 C 葉點，也有附件。

所以 K4 四點各有一條除起點外避開 K4、通至 Γ 的路徑，四路內部互斥。
保留四點為 singleton，將 Γ 與四路的內部合為第五個連通 branch set，
即得 K5 minor。這沿用 [K4 報告 §3](c5_k4_blocks.md#3-不需正常形枚舉的-k5-minor)
的拓撲構造；本輪以 Gallai 結構／完整度數證明各外側有附件，**不借用該
舊報告的 minimality 前提**。此 minor 只排除平面性，不保持 boundary state。

## 4. 所有末端 blocks 都是 bridges

先排除 C 只有一個 block。若為 odd cycle，§2 使所有點附件都是同一對，
b0 的內鄰點數只能是 0 或圈長，不能為 2。若為單邊，兩端三列都是
singleton lists；三列皆拒絕使两端 list 向量相同，故附件相同。兩端再加
外部 apex h，與共同的三個框鄰點構成 K3,3。K4 已排除。

故 C 有多個 blocks。令 B 為末端 odd cycle，x 是唯一割點。其私有點都
有同一二附件 P={i,j}。

若圈長≥5，至少有三個私有點。把圈沿循環次序分成三個連通段，各含一個
私有點；三段兩兩相鄰。另取 `{i}` 與 `{h,j}`，得到 K5 minor。
這一構造實際上排除**任何有至少三個私有點的 odd-cycle block**。

只剩 B=xuvx。若 0∉P，b0 的內鄰點不在 u,v；C 的連通性給出從 x 經
B 外到 b0 的路徑 Z（容許直接 spoke）。此時有 K3,3 branch sets

```
{u}, {v}, {h,b0}∪int(Z)    versus    {i}, {j}, {x}。
```

若 0∈P，u,v 已用盡 b0 的兩個接點。取另一個末端 block：K4、長奇環及
不含 b0 附件的末端 triangle 已排除；另一個含 b0 的末端 triangle 也會
超過兩接點。因此另一末端必為 bridge，其葉點因不能接 b0，只能取
附件 234。選 `k∈{2,3,4}\P`，從 x 沿 B 外走到該葉點再到 bk，得到 Z。
把上述第三 branch set 改為 `{h,bk}∪int(Z)`，仍得 K3,3。

故末端 odd cycles 全部排除，block-cut tree 的葉節點全是末端 bridges，
一一對應 C 的葉點。

## 5. 葉點恰有兩個，block-cut tree 是鏈

由 §2，葉點附件只能是 012、024、234。若兩個葉點附件相同，將它們
與 h 作一側、共同三個框點作另一側，得到 K3,3；每一類至多一個。

三類也不能同時存在。令 v 是 024 葉點；`C−v` 連通，且另兩葉點使它
同時鄰接 b0、b2、b4。因此

```
{v}, {h}, V(C−v)    versus    {b0}, {b2}, {b4}
```

是 K3,3 minor。故至多兩個葉點；有限非平凡 block-cut tree 至少有兩個
葉節點，故恰兩個。只有兩個葉節點的樹是路徑。

每個非末端 block 恰含兩個割點。所以任何長度≥5 的 odd cycle 至少有
三個私有點，被 §4 的 K5 minor 排除；只剩 bridges 與 triangles。
每個 triangle 恰有一個私有點，其 ρ-list 含全框未使用的色 3，故其
ρ-palette 含 3。若兩個 triangles 共用割點，兩 palettes 在該點重疊，
違反不交分解。因此 triangles 兩兩頂點互斥，中間有非空 bridge 鏈。

## 6. 排除兩葉附件 012／024

假设兩葉 u,v 分別取 012、024，b0 的兩接點便恰是 u,v。沿 block 鏈，
每遇 triangle，就以其兩割點間的直接邊走過，得到 u–v 簡單路徑 P。
每個未在 P 上的 triangle 私有點 w 收縮到該 triangle 的任一割點。
triangles 互斥，這些收縮不識別 P 上不同點，也不動 Γ；結果內部恰為 P。
這只用於拓撲，沒有宣稱保持 lists 或完整 Σ。

對收縮後每個路徑點 p，令 `S(p)⊆{1,2,3,4}` 為非 b0 框附件。
兩端分別是 12、24；每個中間點的 S 非空：原 bridge 間的點有兩附件，
triangle 割點有一附件。若有 triangle，吸收私有點的割點之 S 至少有
兩個元素；若沒有 triangle 但有中間點，該點原有兩附件。

由 [strip 次序引理](c5_two_rejection_proof_zh.md#5-平面附件的次序引理)，
P 的某個方向必滿足 `max S_i≤min S_(i+1)`。只有 12→24 的方向可能，
而兩端使每個中間 S 都必為 `{2}`。只要存在中間點，上一段就給矛盾。
因此 C 只能是單邊 uv；但 δ 下两端 lists 分別為 `{3}`、`{1}`，可以染色，
仍矛盾。此葉對在任意 bridge 長度／triangle 數下排除。

剩餘葉對恰為 §1 的兩種。它們都含 234 葉點，該點在 α 下有 list 餘量，
所以 α 自動接受。012 葉點使 00102 有餘量；024 葉點使 01210 有餘量。
這只解除相應接受測試，並未證明另一開口列接受或拒絕。

## 7. 證書、核對範圍與停止點

[程式](../scripts/c5_sector_3703_structure.py)／
[JSON](../artifacts/c5_sector_3703_structure/observations.json) 不用 NetworkX、
不呼叫 planarity oracle、不枚舉新 sector 圖、不修改任何舊 artifacts。

- 完整列出 32 個框子集中的三列緊附件；逐列核對單／二／三附件向量單射。
- C3 的 49、C5 的 2,401 組私有二附件，以完整 root 色集計算，各僅七組
  同時有三列二色禁集，均為共同附件。K4 的 125 組單附件僅五組共同型。
- 保存 207 份實際邊／連通互斥 branch sets；逐份驗目標 K5 或 K3,3
  的全部邊。其中長圈控制遍歷 C5/C7 的三個標記私有點，任意長度由 §4
  的分段構造證明；模型中的外部路徑不冒充完整 sector 實現。
- 另驗 K4 四出口的全部 625 種框端點選擇，包括端點重合；保存十份代表。
- 同圖負控制為單邊、附件 012／024：完整十二位 mask=3831，拒絕 3、8
  卻接受 7。緊附件條件本身不能推得三拒絕。

```bash
uv run python scripts/c5_sector_3703_structure.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
uv run python scripts/c5_sector_terminal_blocks.py --check
lake build
git diff --check
```

本輪重播以上三份 checker 與 Lean build；strip 的一般紙面引理沿用已核對
報告，本輪未重跑雙拒絕 atlas／strip 窮舉；K4 舊 standalone、其他 sector
及 R 系列未重跑。新 checker 只驗局部表與所存 minors，任意大小的分類
依賴 §2–6 紙面接合及外部 degree-list 定理。Lean build 不形式化新結論。

**停止點：** 兩種葉對的實際 triangle/bridge 鏈，b0 第二接點在鏈內。
尚未界定 triangle 數或收縮任意 bridge 長度；尤其不能只保留 ρ 的 list
語義後推論 δ、η 或開口列。3703、一般 degree-5、R31、共同出口及
`K∞=K≤5` 仍未解；603 profiles／固定點不變，未 commit／push。
