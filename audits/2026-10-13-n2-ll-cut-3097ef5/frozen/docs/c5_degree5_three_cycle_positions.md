# 三環共用點鏈：全部接點位置與保留標記的奇環目標

文件整理（2026-09-23），R28：完整 list 接合保留；[R29–R30](c5_degree5_middle_cycle_minors.md) 已完成中間不同二接點排除，[R31](c5_degree5_same_terminal_triangles.md) 僅完成同末端不同二接點正常形。
系列定位見 [degree-5／R 系列導讀](c5_degree5_guide.md)，研究優先序見
[HANDOFF](HANDOFF.md)。下文「下一步／未解／未提交」保留當輪語境；
歷次驗證與發布見 [研究歷史](STATUS_HISTORY.md)，不代表本次重新驗證。

2026-09-18，R28。接手 HEAD `e14874d` 與未提交 R24–R27。
沿用三-spoke、唯一 degree-5 點 z、其餘 degree-4、fixed-q minimal
obstruction 的設定。研究 J1–J2–J3 共用點鏈，兩共用點 r12≠r23，
各環為任意奇環。本輪為**紙面 list 介面＋Python 固定域控制**；
沒有新增圖層 minor、minimality／disk 排除或 Lean theorem。

## 1. 接點位置與不能直接消去的末端環

共用點已有四條環邊，不能另接臂、spoke 或 bridge。刪去 cluster 的
環邊後，每個外部樹分量至多碰 cluster 一點，否則會產生額外 block。
兩條從 z 進入分量的路徑因而分成：

| 位置 | 本輪處理 |
| --- | --- |
| 兩個不同私有點 | 同末端環、分處兩末端、末端與中間、同中間環 |
| 同一私有點會合 | 末端或中間的帶標記閉路徑介面 |
| 在 cluster 外先會合 | cluster 整體在不含 z 接點的單 bridge 旁支 |

第三型沿用 [R13 §2](c5_degree5_triangle_components.md#2-不含保留接點的單-bridge-外枝可消去)：
該外枝不要求是樹，minimality 給其 bridge root 唯一強迫色；可化為
實際同色 spoke 或 D 葉，回到既有樹排除。本輪未重跑該來源 minor 控制。

但一個**共用點末端環**不是單 bridge 旁支。其對共用點交回至少二色
root 集；共同私有 palette T 時恰為 U\T。因此不能直接刪掉該環，
也不能把它當成一個 singleton forcer。證書保存具體 list 控制：

```
J1=[U,{2,3},{2,3}], J2=[U,U,{0,1}], J3=[U,{2,3},{2,3}].
```

原接合不可著色；刪掉 J1 對 r12 的限制後可著色。這只是反駁直接
刪環／singleton 替換，沒有排除其他保留二色限制的圖層化約。

## 2. 所有接點位置共用的精確判準

固定 z=a，先扣除兩臂末端 singleton 訊息；非 singleton 不扣色。
不同接點原 list 為三色，同點接入原 list 為 U，故所有私有有效
lists 仍至少二色；兩個共用點的原 list 為 U。

令末端環完整 root 集為 E1(a)、E3(a)，中間環兩共用點的完整
有序關係為 R2(a)。中間環若有接點，**R2 也隨 a 變動**。精確接合是

```
Q(a) = R2(a) ∩ (E1(a) × E3(a)).
```

由 [R23 root 剛性](c5_degree5_shared_cycle_roots.md#1-一般奇環在自由-root-的二色剛性)，
|E1|、|E3|≥2。把這兩個集合當成中間環端點 lists，套用奇環
至少二色 list 判準，可得 Q(a)=∅ iff 存在二色 S，使

```
J2 全部私有有效 lists = S，E1(a)=E3(a)=S，
亦即 J1、J3 全部私有有效 lists = T=U\S。
```

所以 **T–S–T 剛性不要求兩臂分處末端環**。D 被拒絕即固定交替
palettes；此推論保持共同端點色框，沒有把有序關係改成獨立投影。

兩個不同接點時，至少存在一個未標記的末端私有點，固定 T 與 S。
每個標記點原 list 是其 palette P 加一個 c∉P，D 列臂輸出 {c}。
其他列要再拒絕，必須再次輸出該指定 singleton；R20 的反向唯一性
強迫輸入仍是 D。因此所有不同接點位置都有 **完整 F={D}**。

## 3. 同點會合必須保留完整禁色集

令標記點 p 所屬 palette 為 P（末端為 T，中間為 S）。先移除兩臂，
把 p 的 list 放寬成 U，其餘維持交替 palettes。此 gadget 對 p 的
完整 root 集恰為 **U\P**：若 p∈P，原來的 obstruction 仍拒絕；
對每個 c∉P，將 p 放寬為 P∪{c} 打破交替剛性，必有著色，且該
著色不能令 p∈P，所以必使用 c。

設兩臂末端訊息為 M1(a)、M2(a)，δ(M) 在 M 是 singleton 時等於 M，
否則為空。則

```
a∈F iff (U\P) \ (δ(M1(a)) ∪ δ(M2(a))) = ∅。
```

兩條臂與 p 因此給出一條在 p 帶二色 list U\P 的閉路徑。不能各自
只保留 D 列而縮臂；可能另一個 a 交換兩個 singleton 的角色，亦被拒絕。
證書保存含 D 的雙拒絕反向控制；這些不符合 F={D} 的 list 配置不是
minimal q-obstruction 候選。後續圖層工作應沿用帶標記閉色序列規則。

例如 S={0,3}、T={1,2}、p 在末端 triangle；其 intrinsic root 是
{0,3}。一臂含一個 list={0,3} 的內點，另一臂零長，z=0 或 3 時
兩臂都恰禁用 {0,3}，故 F={0,3}。這是完整四列檢查必要性的具體控制。

## 4. 保留接點的有限 list 目標

每個末端環保留共用點與所有接點，補到三個點；中間環保留兩個
共用點與所有接點。若中間環至多一個接點，補到三個點即可。
**若中間環有兩個不同接點，須保留四個不同標記，原環長至少五，
再保留任一其他私有點，得到 C5。** 三點 triangle 無法分別保留這
四點；這是此保留標記、只縮環方案的限制，不是任意化約的不可能定理。

所有保留點依原循環次序排列，lists 及臂 profile 沿用；同點型仍保留
單一 p。目標為 (C3,C3,C3)，或兩臂同中間不同點時的 (C3,C5,C3)。
每個環任意子集替換都保持四列可延拓布林值：未標記點始終是固定
palette，保留全部標記，且仍有末端 palette 錨點。因此 §2 的交替
判準在來源與目標對每個 a 等價。同點型也保持 §3 的完整 F。

這裡**不要求 Q(a) 本身保持**；證書另存有序關係變化的控制。
尚未建立這些新位置的 boundary 固定 branch sets、degrees、刪邊
著色及拓撲合成，不能把本節 list 目標視為已完成來源 minor。

## 5. 有限控制、重播與下一步

[checker](../scripts/c5_degree5_three_cycle_positions.py)、
[certificate](../artifacts/c5_degree5_three_cycle_positions/observations.json)。
三個 triangles 的五個私有 lists 各取全部 11 種至少二色集合，逐一
以獨立圖回溯核對精確接合與交替剛性。條件化控制採環長
(3,3,3)、(5,5,5)、(5,7,9)，中間共用點的全部位置、全部無序接點對
（可重複）、六個 palettes 及 R20 所有 D 相容 arm profiles。
profile 對在每組接點上有序，故不同臂分派皆涵蓋；同點交換也保留。
逐組核對四種 z 色與八種縮環子集；triangle 條件化列另用圖回溯核對。
同點型另精確求放寬 p 後的 root 集。一般任意長度結論由 §2–4 承擔，
不是把有限長度控制當成枚舉證明。數字與本輪核對範圍見 [STATUS 歷史 §32](STATUS_HISTORY.md#32-r28-三環鏈全部接點位置介面)。

```bash
uv run python scripts/c5_degree5_three_cycle_positions.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_three_cycle_minors.py --check
lake build
git diff --check
```

下一步優先處理**兩個不同接點都在中間環的 C3–C5–C3 正常形**：
枚舉兩共用點與兩接點在 C5 上的循環位置、建立實際 attachments／臂
接線，核對 degrees、四列 F={D}、逐邊刪除著色，再求非 disk 證書或
具體障礙。R26 三個 triangles 的覆蓋不能直接涵蓋此 pentagon。
其他新位置的圖層排除、環間 bridge 型、一般三環與 `K∞=K≤5` 仍開放。

後續 [R29](c5_degree5_middle_pentagon.md) 已完成上述 C3–C5–C3 正常形
的全部實際接線、四列、刪邊著色與非 disk 證書；[R30](c5_degree5_middle_cycle_minors.md)
再補完此型任意長來源 minors 及拓撲回接。沒有將本報告 list 縮環直接
視為圖層 minor。[R31](c5_degree5_same_terminal_triangles.md) 另完成
同末端不同二接點正常形，此型任意長來源 minors 仍是目前缺口。
