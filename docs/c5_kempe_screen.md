# 從 Kempe 必要條件切入 K∞ = K5

2026-09-14。此次目標是任意大小 cell 的結構限制，沒有再枚舉大 k。

**結果：原猜想可集中到兩個尚未排除的 D5 orbit。** 這是紙面必要性論證搭配外部有限檢查，
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

例如 932 是五個四色 patterns 的集合 T4；它與 wheel 的 91（三色五種全收）不相交。
其餘十個全部存活，故只反覆測已知外側 cell 已無法再進一步。

## 4. 集中後的候選引理（UNPROVED）

令 T4 是 C5 的五個四色 patterns，P(G) 是可延伸的三色 patterns 的 singleton 位置集合。
每個三色 C5 pattern 的色重數為 (2,2,1)，因此 singleton 位置給出唯一標記。

> 對任意 C5 disk cell G，若 T4 ⊆ Σ(G)，則 |P(G)|≥2；若 |P(G)|=2，這兩個位置在 C5 上相鄰。

尚未被排除的 masks 恰為這條引理的兩類反例：

| 類型 | D5 代表 | 全部固定標號 masks | 代表的 P |
| --- | ---: | --- | --- |
| T4 加一個三色 pattern | 933 | 933, 934, 940, 948, 996 | {4} |
| T4 加兩個不相鄰的三色 patterns | 941 | 941, 949, 950, 998, 1004 | {4,2} |

代表的實際 patterns：

- 933 = T4 ∪ {01012}。
- 941 = T4 ∪ {01012, 01201}。
- T4 = {01023, 01203, 01213, 01231, 01232}，bit mask 為 932。

此引理是所有有限 disk cells 上的命題，不是已知 catalogue 的經驗規則。它對既有 132 個
keys 全部成立；合併 §2–3 的必要條件後，通過者恰等於這 132 個 keys。

**條件式推導**：假設此引理成立，任意 G 由 4CT 得非空 Σ，由 §2 得 Kempe 條件，由 §3 得
外側相容；有限檢查再給 Σ(G) 等於某個已有至多五內點 witness 的 key。故 K∞⊆K5；反向包含
由定義成立。整條上界不需要逐圖縮減，也不需要證明每張大圖都有 R1／R2 configuration。
但目前這仍是一條待證路線：候選引理、拓撲 bridge、有限分類認證各有工作。

**下一步宜先攻這兩個代表的不可實現性。** 假設一張 disk 圖同時接受 T4 的全部五種，並且
三色 support 分別恰為 {4} 或 {4,2}，找出跨不同完整染色的 connectivity 限制。此次單個
pattern／split 的 existential partitions 已無法排除它們，不能再宣稱相同的檢查足夠。

可先利用一個紙面簡化：T4 全收意味 boundary 無 chord。每條 C5 chord 的兩端，都能在某個
四色 pattern 中成為唯一重複色的一對；該 pattern 就會被 chord 禁止。因此這兩個代表可
限制在 induced-C5 disk 圖研究，但不能假設整張內部圖已是 triangulation。

較早 triangle/fan grammar 的 profile 結論可用來找證明靈感，不能直接搬到任意 disk。
尤其一般 cell 已有不相鄰二元 profile（例如 429）；不能刪去 T4 全收的前提。

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
