# C5 adjacent-singleton problem：從 Kempe 必要條件切入 K∞ = K5

2026-09-14；2026-09-15 更新結構性問題表述。此次目標是任意大小 cell 的結構限制，沒有再枚舉大 k。

**後續（2026-10-02）**：[四容量子覆蓋共享](c5_excess_one_subcovers.md) 已證
933 的 ε≥2，並將 941 的 ε=1 收窄到單 binary 原分量及 t=1、2、3。
兩候選的一般來源仍未排除，既有 screen artifact 未更改。

前輪 [933／941 容量與跨度下界](c5_independent_support_capacity.md)
對固定完整 Σ 的 edge-minimal disk sources 證 ε≥1、cores 兩兩共用高 degree
root，並建立 mixed 條件容量及 unary 六跨度禁形。未證候選必含禁形，
933／941 仍未排除；沒有新圖枚舉。目前停止點見 [Kempe 導覽](c5_kempe_guide.md)。

**計數路線續作**：[反例歸約到 near-triangulation 與 count-cone 猜想](c5_count_cone_bridge.md)。
一般反例可保留一個關鍵完整染色補完；T4 全收由計數恆等式重新推出。
引用文獻可排除內點 ≤12 的 near-triangulation 反例，一般引理仍未證。

**結果：原猜想可集中到 singleton support 是否必含一條 boundary 邊的問題。** 這是紙面必要性論證搭配外部有限檢查，
不是新 Lean 定理，也尚未證明原猜想。外側檢查明確使用四色定理（4CT）；若希望整條路線不依賴
4CT，必須另外證明該步，不能拿本結果反過來當作 4CT 的無循環證明。

## 1. 定義與實際結果

沿用 [cell 定義](c5_cell_enumerator.md#1-答案可以條件是密封與c5-在內側是-face)：有限簡單圖，
有序 C5 暴露為 disk 邊界，其他頂點私有，允许內側 chords。K5 表示至多五個內點可實現的完整
十 bit 關係集合，不是 complete graph。所有 bit 使用 `cells.json` 的固定 `pattern_order`。

| 篩選 | 剩餘 masks | 與既有 K5 的差額 |
| --- | ---: | ---: |
| 全部非空十 bit masks | 1,023 | 891 |
| 平面 Kempe 必要條件 | 153 | 21 |
| 再要求與每個已知外側 cell 非空相交（使用 4CT） | 142 | 10 |
| **假設** §4 尚未證明的引理 | 132 | 0 |

132 個既有 witness 以原獨立 checker 重播：NetworkX apex-planarity 與 brute-force 染色均通過。
這驗證的是已知實現；任意大圖的上界仍需要結構論證。新 checker 枚舉的是 1,023 個關係，沒有
跑 graph DFS，沒有依賴 K6／K7 搜尋完整性。

## 2. Kempe 必要性：為何與內點數量無關

固定一個能延伸的 boundary pattern b，選一個完整四色染色 c。把四色分為兩對，例如
{0,1} 與 {2,3}。考慮兩個雙色 induced subgraphs 的 connected components。

1. 每個碰到 boundary 的 component 給一個 boundary block。兩組 component 的 blocks 合起來
   分割五個 boundary 位置；沒有碰到 boundary 的 components 不影響以下觀測。
2. 同一 block 的 boundary 顏色必須在同一色對內。boundary 邊若兩端在同一色對，兩端必屬
   同一 component。
3. 這個分割必須 noncrossing：不能存在依環序排列的 a,b,c,d，使 a,c 屬一個 block，b,d 屬
   另一個 block。否則兩個 vertex-disjoint connected subgraphs 在 disk 中連接交錯端點，
   違反平面分離性。**此為紙面 disk 拓撲引理，未 Lean 化。**
4. 可獨立對任意多個 components 交換其兩種顏色；跨色對的邊仍連接不同色對，故完整染色仍
   proper。得到的所有 boundary patterns 都必須仍屬 Σ。

因此，對每個 b∈Σ 和三種 complementary splits，**至少存在**一個符合 1–3 的分割，其所有
block-swap 結果均在 Σ。不是要求所有抽象分割都可實現；不同 split 的分割也沒有被本檢查
認證為可同時來自同一完整染色。

`scripts/c5_kempe_screen.py` 枚舉上述分割，生成每個 pattern／split 的可選 orbit masks，
再檢查 `∃ orbit, orbit ⊆ Σ`。所有拒絕均在 JSON 留下 pattern、split 與可選 orbit 證據。

重要負控制：刪掉 noncrossing 條件後，1,023 個非空 masks **全部通過**。單純使用換色、而
不使用 disk 幾何，在這個抽象層上沒有排除力。

## 3. 外側 cell 測試

對任意真實 cell G 與已知 cell H，兩個 disk 沿相同有序 C5 黏合是平面圖。4CT 保證 union
可染色；限制回 boundary，得到 Σ(G)∩Σ(H)≠∅。這裡用完整十 bit 關係，沒有 pair projection
或獨立重命名 boundary。已知 catalogue 對 D5 封閉，測所有 132 個固定標號 keys 已包含對齊。

21 個 Kempe 額外 masks 中有 11 個被這條排除。JSON 對每個被排除的 mask 記錄一個
`exterior_rejections[mask]`，即與它相交為空的具體已知 witness key。

例如五個四色 patterns 的集合 T4 與 wheel 的關係（三色五種全收）不相交。
其餘十個全部存活，故只反覆測已知外側 cell 已無法再進一步。

## 4. C5 adjacent-singleton problem（UNPROVED）

固定有序 boundary C5 = (v₀,v₁,v₂,v₃,v₄)。令 T4 是全部五個四色 boundary states；
每個 state 由唯一同色的非相鄰頂點對標記。令

\[
P(G)=\{i\in V(C_5):\text{singleton 位於 }v_i\text{ 的三色 boundary state 可延伸}\}.
\]

每個三色 C5 pattern 的色重數為 (2,2,1)，singleton 位置唯一決定其 S4 orbit；
色名本身沒有意義。

> **Adjacent-singleton lemma（候選，未證）**：對任意有限 planar disk cell G，
> \[
> T_4\subseteq\Sigma(G)\quad\Longrightarrow\quad E(C_5[P(G)])\ne\varnothing.
> \]
>
> For a planar disk cell G with boundary C5, does extension of all five four-colour boundary
> states force the three-colour singleton support P(G) to contain an edge of C5?

結論表示存在相鄰 i,j，使 singleton-i state 和 singleton-j state 各自可延伸；
兩個延伸可以是完全不同的完整染色。這是 extension space 中兩個 boundary fibers 非空，
不是要求同一染色同時具有兩個 singleton 位置。

因為 α(C5)=2，此結論等價於 |P(G)|≥2，且恰好兩點時相鄰。
反證的統一起點是 **T4 ⊆ Σ(G)，且 P(G) 是 C5 的獨立集**；只有證明需要時才按大小分情況。
空集已由外側 wheel 配合 4CT 排除：wheel 恰接受全部三色 states，與 T4 不相交。
剩下 singleton 與 independent 2-set，是同一結構性反例的兩種大小。

### 4.1 與 K∞=K5 的條件式關係

此引理是所有有限 disk cells 上的命題，不是已知 catalogue 的經驗規則。它對既有 132 個
keys 全部成立；合併 §2–3 的必要條件後，通過者恰等於這 132 個 keys。

**條件式推導**：假設此引理成立，任意 G 由 4CT 得非空 Σ，由 §2 得 Kempe 條件，由 §3 得
外側相容。一般 disk cell 不一定滿足 T4 ⊆ Σ(G)：有限分類中，不全收 T4 的倖存關係已在 K5；
全收 T4 的分支再用 adjacent-singleton lemma，排除獨立 support 的額外候選。
有限檢查於是給 Σ(G) 等於某個已有至多五內點 witness 的 key。故 K∞⊆K5；反向包含由定義成立。
整條上界不需要逐圖縮減，也不需要證明每張大圖都有 R1／R2 configuration。
但目前這仍是一條待證路線：候選引理、拓撲 bridge、有限分類認證各有工作。

### 4.2 證明方向與範圍

直接研究 T4 全收與 independent singleton support 能否共存，找出跨不同完整染色的
connectivity 限制。此次單個 pattern／split 的 existential partitions 已無法排除剩餘候選。
這提示可研究不同 extension colorings 間的相容性，但不表示已證明所有單一染色 Kempe
論證都不可能成功，也未證明延伸空間本身的 Kempe connectivity。

可先利用一個紙面簡化：T4 全收意味 boundary 無 chord。每條 C5 chord 的兩端，都能在某個
四色 pattern 中成為唯一重複色的一對；該 pattern 就會被 chord 禁止。因此可限制在
induced-C5 disk 圖研究，但不能假設整張內部圖已是 triangulation。

較早 triangle/fan grammar 的 profile 結論可用來找證明靈感，不能直接搬到任意 disk。
尤其一般 cell 已有不相鄰二元 profile；不能刪去 T4 全收的前提。

### 4.3 Computational certificate 對照

數字 masks 僅作固定 pattern order 下的證書索引；數學問題使用上面的 support 表述。

| independent P 的形狀 | D5 代表 | 全部固定標號 masks | 代表的 P | 狀態 |
| --- | ---: | --- | --- | --- |
| 空集 | 932 | 932 | ∅ | exterior wheel + 4CT 排除 |
| 一個點 | 933 | 933, 934, 940, 948, 996 | {4} | 尚未排除 |
| 兩個不相鄰點 | 941 | 941, 949, 950, 998, 1004 | {4,2} | 尚未排除 |

- T4 = {01023, 01203, 01213, 01231, 01232}，bit mask 為 932。
- 933 = T4 ∪ {01012}；941 = T4 ∪ {01012, 01201}。
- 外側 wheel 的 mask 為 91；不滿足 T4 全收但具有不相鄰二元 profile 的既有例子為 429。

**2026-09-15 後續**：[計數層與剩餘缺口](c5_adjacent_singleton_counts.md) 推出
x_uv+y_u+y_v 為常數的紙面計數恆等式，並給出仍通過恆等式與 Kempe orbit 整數分解的
abstract independent-support vectors。另確認加入 exterior 後的 142-state push 閉包。
這些是新必要條件與其不足的證據；主引理未證。

## 5. 已試過、沒有縮小的局部操作

把 boundary v 換成新頂點 v'，連 v' 到原 v 的兩個 boundary 鄰居，並選擇是否連 v'–v。
保留原 C5 邊，讓原 v 成為 private；這是在兩邊 boundary arc 的外側附上一個 disk，故
新圖仍有有序 C5 邊界。完整關係是對原 v 的顏色存在量化，`push` 直接算其十 bit 輸出。

153 個 Kempe masks × 五個位置 × 兩種 spoke 選擇，共 1,530 個轉移，全仍在 153 個之內。
132 個已知 keys 的 1,320 個轉移也全在 K5。因此這十種操作的任意有限重複，配合**僅此
Kempe screen**，不會排除新的 masks。沒有宣稱涵蓋一般 annulus、所有 context，或將
外側測試加入轉移後的全閉包。

## 6. 重播與信任範圍

```bash
python3 scripts/c5_kempe_screen.py --check
uv run --with networkx==3.5 python scripts/c5_cell_enumerator.py --check
git diff --check
```

[報告](../artifacts/c5_cells/kempe_screen.json) 記錄 catalogue 與新 script 的 SHA-256、完整
30 組 obligations、全部 Kempe 拒絕證據、11 個外側 witness、兩個剩餘 orbits。`--check`
逐 byte 比對；分割生成另以 restricted-growth words 獨立核對 n≤5 的全部 Bell 分割。

未新增 Lean 模組，未變更 production enumerator／`cells.json`。使用者後續已要求 commit／push 此輪成果。
K∞=K5 仍是猜想；「假設候選引理後剩 132」不可標成實現性證明。

**重要參考（使用者於 2026-09-14 指定）**：Dvořák–Swart 的 [A note on extendable sets of colorings and rooted minors,
§1](https://arxiv.org/html/2504.07764v1) 明確指出 planar realizable coloring sets 必須滿足
Kempe-chain constraints。本輪以此為方向背景；153／142／兩類剩餘 masks 是本倉庫新計算，
並非引用該文定理。該文的一般 rooted-minor 結果沒有證出這裡的 C5 分類。

使用者要求本輪先停在這裡。恢復研究時優先對照該文 §1 的 planar realizability、
Kempe constraints 與 reducibility 觀點，再評估對剩餘兩個 orbit 的用途。
