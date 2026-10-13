# 3703：葉點 minor 與三列 palette 的任意長度排除

後續（2026-09-24）：[單側出口接合](c5_single_sided_exit.md) 已完成五目標到
唯一 degree-5／三-spoke minimal core 的分離及條件式出口；一般核心分離仍未證。
下文當輪停止點保留歷史語境。

2026-09-24。接續 [兩葉鏈化約](c5_sector_3703_structure.md)，從乾淨
`3c843a4` 接手。**3703 在指定 sector 圖類內排除。** 更強地，此圖類
不可能同時拒絕索引 3、7、8，無須再使用其餘九列接受條件。

證據層為紙面證明、沿用的外部 degree-list 定理及 Python 局部證書；
未新增 Lean theorem。研究優先序見 [HANDOFF](HANDOFF.md)。

## 1. 前提與結論

K 有 induced C5 外框 Γ=(b0,…,b4) 的 disk embedding；C=K−Γ 非空連通，
每個內點在 K 的完整 degree≤4，b0 恰有兩個不同內鄰點。
令 A(v)=N_K(v)∩Γ，以框索引表示附件。假設同圖拒絕

```
ρ=01201（3），δ=01213（7），η=01231（8）。
```

沿用 [必要結構定理](c5_sector_3703_structure.md#1-命題與精確剩餘問題)：
所有內點完整 degree=4；C 是 bridges／兩兩頂點互斥 triangles 的 block
鏈，兩端均為葉點，葉附件只能為 012／234 或 024／234；b0 第二接點
在鏈內。以下排除兩型，不限制鏈長或 triangle 數。

因此五個目標中剩餘的 3703 也被排除；與
[雙拒絕分類](c5_two_rejection_proof_zh.md) 合成，五目標皆在上述圖類內
排除。這不直接刪除抽象 603 profiles，也未重算固定點或證明主命題。

## 2. 葉點的三附件障礙

**引理。** 若 u 是 C 葉點，A(u)={i,j,k}，則 C−u 不可能同時鄰接
bi、bj、bk。

證明：disk 外加一個鄰接全部 Γ 的 apex h，所得圖仍平面。C−u 非空
連通。如果它鄰接上述三點，取六個連通、非空、互斥 branch sets

```
{u}, {h}, V(C−u)    versus    {bi}, {bj}, {bk}
```

即可得到 K3,3 minor，矛盾。只刪邊／收縮內部連通 branch set，不把
收縮圖當作保持 degree、lists 或 boundary state 的替代圖。

對 024／234，取 u 為 024 葉點。另一葉點提供 b2、b4 接邊，b0 的第二
內鄰點在 C−u 中提供 b0 接邊，立即違反引理。

對 012／234，取 u 為 012 葉點，v 為 234 葉點。C−u 已接 b0、b2，
所以引理迫使

```
所有 w∈C−u 都滿足 1∉A(w)。                         (★)
```

這是同一張來源圖上的全域禁接條件；不是由不同列或不同實現拼接。

## 3. 從 012 葉點起，鏈只能走一步

每列拒絕都給不交的 block-palette 分解：bridge palette 為 singleton，
triangle palette 為二色集；一點的 list 是其所有 incident block palettes
的不交聯集。此為前報告使用的 degree-list 定理之同一依賴。
用三元組依次記錄 ρ、δ、η 的 bridge 顏色。

u 的三列 lists 都是 {3}，故第一條 bridge 的三元組是 **(3,3,3)**。
末端 v 的三元組則是 **(3,0,0)**，故第一條 bridge 不能直接抵達 v。

第一個非葉點若在 triangle 上，該 triangle 的私有點有兩附件；ρ 只用
0、1、2，因此私有點的 list（即 triangle palette）必含 3。這與入橋
的 ρ-palette {3} 重疊，違反不交性。故下一點 x 必是兩條 bridges
之間的 degree_C=2 點，有兩附件。

由 (★) 及三列緊附件表，A(x) 只能為 02、04、23、24、34。其中只有
**02** 的三列 lists 都含入橋顏色 3：

| A | Lρ | Lδ | Lη |
| --- | --- | --- | --- |
| 02 | 13 | 13 | 13 |
| 04 | 23 | 12 | 23 |
| 23 | 13 | 03 | 01 |
| 24 | 03 | 01 | 03 |
| 34 | 23 | 02 | 02 |

所以 A(x)=02，出橋三元組是 **(1,1,1)**。x 用盡第二個 b0 接點，
此後所有點的附件均避開 0、1。此出橋也不能抵達 v，因 (1,1,1)≠(3,0,0)。

## 4. 第二步不可能，無須界定鏈長

若下一點 y 是 bridge 間點，附件只能是 23、24、34。上表中沒有一行
在三列都含 1，故無法容納三元組 (1,1,1) 的入橋。

若 y 是 triangle 的入口割點，令其私有點附件為 P。P 同樣只能是
23、24、34；triangle palette 必等於該私有點的 list，且三列都必避開
入橋顏色 1。

- P=23 的 ρ-list 含 1，矛盾。
- P=24 的 δ-list 含 1，矛盾。
- P=34 的 palettes 是 (23,02,02)。加上入橋色 1，入口割點的 lists
  必為 (123,012,012)。所以其唯一框鄰點 a 的三列色向量必為 **(0,3,3)**。
  然而可用框点 a∈{2,3,4} 的向量依次為 (2,2,2)、(0,1,3)、(1,3,1)，
  沒有符合者。

因此鏈既不能終止，也不能再走一步，矛盾。這證明任意大小的三拒絕
圖不存在，完成 3703 的指定 sector 排除。全程保留三列與同一組實際附件；
沒有把單列縮鏈推成完整十二列或任意 pinning 保持。

## 5. 局部證書與驗證

[程式](../scripts/c5_sector_3703_exclusion.py)／
[JSON 證書](../artifacts/c5_sector_3703_exclusion/observations.json) 保存：

- 56 個 bridge 間點轉移與 33 個 triangle 轉移，皆使用共同實際附件。
- triangle 轉移以直接三點著色獨立核對輸出 singleton root。
- 禁接 b1 且 b0 接點數≤2 後，從 ((3,3,3),1) 可達的狀態恰為自身及
  ((1,1,1),2)，唯一轉移是附件 02；終點 ((3,0,0),2) 不可達。
- 葉附件 012、024 的兩份 K3,3 模型，逐項核對 branch sets 與目標邊。
  模型的 t 代表整個連通 C−u；任意來源圖到此模型的提升由 §2 證明。

有限表是局部算術覆蓋；任意長度排除由 §1–4 的紙面論證完成。
沒有圖生成器、planarity oracle、新 sector 枚舉或 profiles 修改。

```bash
uv run python scripts/c5_sector_3703_exclusion.py --check
uv run python scripts/c5_sector_3703_structure.py --check
uv run python scripts/c5_sector_rejection_lists.py --check
uv run python scripts/c5_sector_terminal_blocks.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

本輪實際驗證詳見 [研究紀錄](history/2026-09-24-3703-exclusion.md)。
沿用前輪 degree-list／結構／雙拒絕紙面證明；未重跑雙拒絕 atlas、舊 K4
standalone、R 系列、603 profiles 或閉包。Lean build 不形式化新排除。

## 6. 停止點

3703 的指定圖類問題已完成；五目標局部不可實現與一般單側出口間的
提升仍需逐一核對假設及候選窮盡性。下一入口是這個邏輯連接，而非重開
兩葉鏈枚舉。R31、一般 degree≥5、共同 pivotal edge、候選 A、一般
weak-deletion congruence 及 `K∞=K≤5` 仍未證；未 commit／push。
