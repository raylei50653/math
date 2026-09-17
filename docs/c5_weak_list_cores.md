# 相鄰雙缺失：list-critical cores 與小阻礙分離

2026-09-17。接續 [flow-repair 停止點](c5_weak_flow_repairs.md)。
本輪選出的方向是 **minimal obstruction 的 list-coloring 結構**。
候選 A 一般三出口仍未證，但得到適用於任意大小來源圖的條件式結論：
相應最小阻礙若至多有三個有效內點，就能分離另一個缺失 pattern。
這依賴下述紙面分類及有限模板的 Python／planarity 核對，未形式化到 Lean。

後續：[四內點核心與無界 odd-path 家族](c5_four_vertex_cores.md) 已排除四內點
的雙缺失 minimal core，並指出一般單缺失核心無固定內點上限；以下保存本輪停止點。

## 1. 精確的 list-coloring 翻譯

固定三色 boundary pattern p，以及 inclusion-minimal p-obstruction A。
A 是保留的非外圈邊集；H 是其有效內點誘導圖，忽略孤立內點。
假設來源包含全部 T4，故沒有 boundary chord：每條 chord 都會拒絕某個 T4。
定義 L_p(v) 為四色集扣去 v 的 boundary 鄰居在 p 中使用的顏色。
p 可延拓 iff H 有 proper L_p-coloring。p 未使用的第四色 D 屬於每個 list。

minimality 給出三個一般紙面限制：

1. H 連通。多個有效分量中若一個已不可著色，其他分量的邊可刪。
   沒有內部鄰居的單點也不是阻礙，因為其 list 含 D。
2. 同一內點不能連到兩個 p 同色的 boundary 頂點；否則其中一條 spoke 可刪，
   list 完全不變。
3. 每個有效內點在 C5∪A 的總 degree 至少 4。否則先刪其所有 incident edges，
   由 minimality 延拓剩餘圖，再用最多三個鄰居未使用的色補回該點。

因此 boundary degree 為 t、interior degree 為 d 的內點滿足
`|L_p(v)|=4−t≤d`，而 `d−|L_p(v)|=deg(v)−4`。
degree-list 方法失去直接控制的位置正是總 degree 大於 4 的內點。

## 2. 至多三個有效內點的紙面分類

**引理。** 在 §1 假設下，至多三個有效內點的 A 只可能是：

- 一條內部邊，兩端各連三個 p 顏色互異的 boundary 頂點；兩端 lists 都是 {D}。
- 一個內部三角形，各點連兩個 boundary 頂點；三組 boundary 顏色是同一個
  二元素集合，因此三個 lists 恰為同一組兩色。

證明：一個有效內點不能阻擋 p。兩個內點必相鄰；因每個 list 含 D，
不可著色 iff 兩個 lists 都是 {D}，再由 spoke 不重複性得到第一種。

三個有效內點的連通圖只有 path 或 triangle。path 兩端由最小 degree 限制，
其 lists 都是 {D}。中點若有另一色，path 可著色；若沒有，已有一條邊及其
spokes 構成真子阻礙，違反 minimality。

triangle 的著色等價於三個 lists 有相異代表。由三集合的 Hall 條件及 D 共通，
失敗只可能是兩個 lists 都等於 {D}，或三個 lists 的 union 至多兩色。
前者已有真子邊阻礙。後者若某 list 是 {D}，刪一條適當 spoke 可將它擴成
共同的兩色 list，三角形仍不可著色，亦違反 minimality。
故三個 lists 必恰為同一組兩色。這兩種模板也直接滿足逐邊 minimality。

### 小模板的 disk／T4 篩選與出口推論

保留有序 boundary，只商內點置換，以上模板在五個 p 上共 190 個。
checker 對每個模板核對完整 240-row relation、逐邊 minimality 與 boundary-apex
planarity。35 個是 disk templates；其中 25 個接受全部 T4：5 個 edge、20 個 triangle。
**這 25 個每個都恰好只拒絕其指定 p。** 證書保存全部 190 個，包括排除項目。

這是由 §2 分類窮盡至多三個有效內點的模板，不是由五個舊代表推廣。
信任鏈仍包含 Python、NetworkX planarity 與既有 apex/disk 紙面等價。

**條件式單側出口結論。** 對任意大小的候選 A 來源 G，若某個 minimal
q-obstruction B 至多含三個有效內點，則 B 是 G 的 disk 子圖且接受全部 T4。
由模板核對，Σ(B)=Ω\{q}，故它接受 p；
[critical-core 報告](c5_weak_critical_cores.md) 式 (3) 給出只釋放 p 的 weak exit。
交換 p,q 同理。若只釋放 p 的出口不存在，**每個 minimal q-obstruction
至少有四個有效內點**。不限制來源 G 大小，不假定唯一阻礙，也不推出共同出口。

## 3. 舊代表的機制與失敗的局部化

五個代表的十個 cores 都是 triangle 型；非同面控制的兩個 cores 是 edge 型。
「三角形只能用兩色」與「邊只能用一色」統一在同一個 list-critical 語言下。

缺 singleton-0、singleton-1 的代表有內部三角形 567，其 boundary neighborhoods 是
`N_B(5)={0,1,2}`、`N_B(6)={3,4}`、`N_B(7)={2,3}`。
後兩個 lists 各兩色，第一個非空且至多兩色。Hall 條件給出：拒絕 b iff

`b₂=b₄ 且 b₃∈{b₀,b₁}`。

C5 properness 下這正是兩個相鄰 singleton patterns；另以全部 240 rows 核對。
刪 15 或 05 留下相應的單缺失 triangle core，解釋了兩個單側出口。

把 p₀=(0,1,2,1,2)、p₁=(0,1,2,0,2) 對齊，只改變 boundary 頂點 3。
若限制全部刪邊步驟都在 3 的非外圈 star，strict exit 只有 Ω，找不到單側出口。
五個旋轉代表全部如此。這否定「只在改色頂點的 star 尋找三出口」，
不否定可使用遠處邊與其他 colorings 的一般 flow symmetric-difference 論證。

## 4. degree-four 部分的結構限制

degree-choosability 定理說：連通圖若不是 Gallai tree，就能對每個
滿足 |L(v)|≥deg(v) 的 list assignment 著色。Gallai tree 的每個 block 都是
complete graph 或 odd cycle。標準定理的敘述見 Cranston–Rabern，
[Beyond Degree Choosability](https://arxiv.org/abs/1511.00350) 的摘要。

**推論（紙面，依賴此標準定理）。** 任意 minimal p-obstruction 的總 degree-4
內點所誘導的圖是 Gallai forest。

證明：取任一連通分量 U。刪去所有碰 U 的邊後，由 minimality 將剩餘圖延拓 p，
固定這個外部 coloring。U 每點刪去外部鄰居使用的色後，剩餘 list 大小至少
`4−(4−deg_U(v))=deg_U(v)`。若 U 不是 Gallai tree，degree-choosability 可將
coloring 補回 U，與 A 是 obstruction 矛盾。

尤其，若所有有效內點的總 degree 都為 4，整個 H 必為 Gallai tree。
不是每個 Gallai tree 都是阻礙，也不是都能同面嵌入 C5。
degree≥5 的部分與各 block 在固定 boundary 的可嵌入性仍須處理。

## 5. 小型域外探針：頂點分裂未產生新核心

從一個舊代表的 disk rotation 出發，選內點 v 的 cyclic neighbor list 中兩個
不同位置，切成兩條含共同端點的 arcs；用兩個相連內點分別接兩條 arcs。
這是局部 disk vertex split；另逐圖檢查 boundary-apex planarity。

三個內點共 22 個 choices，所得圖有四個內點。其中 13 個保留來源 relation。
這 13 個各自全部 8,192 個非外圈邊子集以兩種 coloring 算法交叉核對，
合計 106,496 次 subset 檢查；每側仍有唯一 triangle core。
它們全可刪除一個 degree-3 內點還原原圖，只是不影響 relation 的附加部分。
其餘 9 個改變 relation。**此探針未提供非平凡的新候選 A 阻礙。**
這是明確列出的 22 次局部構造，不是 k=4 全圖搜尋。

## 6. 下一個窄問題與驗證

優先研究：**能否存在一個 minimal q-obstruction，同時拒絕相鄰 p、接受全部 T4，
且保持 C5 同面？** 單側出口失敗必然要求這種 core；找到一個仍不等於找到候選 A
反例，因為來源可能另有能分離 p 的 minimal q-obstruction。

至多三個有效內點已排除。下一步先處理四個有效內點，按 degree/list 限制和
Gallai 結構分型，區分全 degree-4 與含 degree≥5 的核心。
若能排除所有大小的這種 core，就得到兩個單側出口；共同出口仍是獨立問題。

產物：[checker](../scripts/c5_weak_list_cores.py)、
[證書](../artifacts/c5_weak_list_cores/observations.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_weak_list_cores.py --check
uv run --with networkx==3.5 python scripts/c5_weak_flow_repairs.py --check
uv run --with networkx==3.5 python scripts/c5_weak_critical_cores.py --check
python scripts/c5_weak_candidates.py --check
python scripts/c5_weak_quotient.py --check
lake build
git diff --check
```

驗證通過：新 checker 與四個既有 checker、`lake build`（8,820 jobs，僅既有 lint）、
三份入口／報告的 136 個本地 file link targets，以及 `git diff --check`。
未新增 Lean theorem，未重播舊全量 deletion audit，未證候選 A 或 K∞=K≤5。
