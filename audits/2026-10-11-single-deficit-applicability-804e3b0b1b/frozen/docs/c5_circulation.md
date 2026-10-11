# C5 十態計數的循環流：六維、153 支撐與十二個生成元

2026-09-27。來源為使用者提出的五點有向圖重述；本輪從專案原始資料獨立核對，
並補上任意非負整數向量的 split-wise orbit 分解推論。
接續 [計數恆等式](c5_adjacent_singleton_counts.md)、[Kempe screen](c5_kempe_screen.md)、
[邊位置對座標](c5_edge_pair_coordinates.md) 與 [B₅ face](c5_b5_face.md)。
研究優先序仍見 [HANDOFF](HANDOFF.md)，本報告不替換 record 110 的主線入口。

**完成範圍**：chord-total 恆等式與循環流的紙面代數等價；全部 1,023 個非空 masks
與既有 Boolean screen 的有限等價；十二循環的完整分類及既有十二射線對照；
36 份有限 orbit 分解推出任意非負整數解皆通過三個 splits 各自的整數計數條件。
沒有新增平面可實現性排除、一般 m≤0、adjacent-singleton lemma 或 K∞=K≤5 證明。
本輪未新增 Lean theorem。

## 1. 座標、固定賦色與輔助圖

固定有序邊界 v₀,…,v₄，下標模 5。Yᵢ 是 singleton 位於 vᵢ 的三色 boundary
pattern 的延伸數；Xᵢ 是唯一重複色對為 {vᵢ,vᵢ₋₂} 的四色 pattern 的延伸數。
每個數都是**一份固定色名 boundary assignment** 的內部延伸數，不是 S4 軌道總數。
沿用 `cells.json` 的十 bit 次序，不重編既有 masks：

| i | Xᵢ pattern／bit | Yᵢ pattern／bit |
| --- | --- | --- |
| 0 | 01203／5 | 01212／6 |
| 1 | 01231／8 | 01202／4 |
| 2 | 01023／2 | 01201／3 |
| 3 | 01213／7 | 01021／1 |
| 4 | 01232／9 | 01012／0 |

[C5Counts.lean](../Math/C5Counts.lean) 的 `x j` 使用 chord {j,j+2}，因此這裡
Xᵢ = `x (i−2)`；Yᵢ 的編號相同。這個換標號須保留，不能直接把兩份 x 索引視為相等。

定義五點輔助有向圖 D：Xᵢ 放在 i→i+2，Yᵢ 放在 i→i−1。每個無序點對恰有
一條有向邊，底圖是 K5。D 的邊代表 boundary patterns；D 不是來源 disk 圖、
dual 圖、來源 minor 或完整染色的 Kempe 可達圖。

## 2. 恆等式等價守恆與六維

令 Lᵢ=Xᵢ+Yᵢ+Yᵢ₋₂。頂點 i 的流出減流入為

\[
X_i+Y_i-X_{i-2}-Y_{i+1}=L_i-L_{i-2}.
\]

因此 Lᵢ 全相等就有流守恆。反之，模 5 反覆減 2 走遍全部位置，所以流守恆
使所有 Lᵢ 相等。此等價在整數、有理數、實數上都成立；加上逐座標非負即得到
相應的非負循環流錐。

D 的 incidence matrix 有 5 行、10 列，秩為 4。直接理由是五行和為零，
而行相依係數在每條邊兩端都相等，底圖連通迫使五個係數全相等。
故循環流空間維數為 10−4=6。全十座標為 1 的向量嚴格為正且守恆，
所以非負錐的相對維數也為 6。checker 另以有理數 RREF 核對兩組方程的行空間相同。

這是邊界**計數空間**的維數，與內點數無關；不是來源圖的 cycle rank。
任意 disk 計數滿足 chord-total 的 topology／inclusion–exclusion 前提，
沿用 [既有紙面證明](c5_adjacent_singleton_counts.md)。

## 3. 十二個循環的完整分類與整數分解

非零非負循環流的每條正邊都在正支撐內的有向環上：若 u→v 無返回 u 的路徑，
令 S 為從 v 可達的點集。沒有正邊離開 S，卻有 u→v 正流入；對 S 加總守恆即矛盾。
取簡單有向環，減去環上的最小正流量，至少消掉一條正邊，且保持非負及守恆。
迭代便終止。整數輸入時每次減量為正整數，故得到單位循環的非負整數組合。

分類不必依賴外部 polyhedral ray-completeness 定理。D 無 loops 或雙向點對，
簡單環長 k 只能是 3、4、5。若含 a 條 X、b 條 Y，則 k=a+b，且閉合要求

\[
2a-b=3a-k\equiv0\pmod5.
\]

- k=3 只能 a=1：唯一 X 邊決定其後兩條 Y，共五環。
- k=4 只能 a=3：唯一 Y 邊決定其後三條 X，共五環。
- k=5 只能 a=0 或 5：純 Y 與純 X 各一環。

這些候選都直接給出不同頂點的閉環，因此十二項窮盡。
令 Tᵢ 的非零座標為 Xᵢ,Yᵢ₊₁,Yᵢ₊₂；Fᵢ 的非零座標為 Yᵢ 及
所有 i∉{j,j−2} 的 Xⱼ；t、W 分別為純 X、純 Y。所有列出的座標皆為 1。
十二者生成全部非負實數循環流，亦生成全部非負整數循環流；每個單位簡單環
不能再拆成兩個非零整數循環流，故這也是整數解的最小生成集。

由 Lᵢ=L 及 m=L−ΣYᵢ，

\[
5m=\sum_iX_i-3\sum_iY_i.
\]

| 生成元 | 數量 | 每單位 m | 既有 B₅ 編號 |
| --- | ---: | ---: | --- |
| Tᵢ：一 X、二 Y | 5 | −1 | T₀,…,T₄ 對應 R₅,₅、R₅,₄、R₅,₃、R₅,₂、R₅,₁ |
| Fᵢ：三 X、一 Y | 5 | 0 | F₀,…,F₄ 對應 R₅,₉、R₅,₈、R₅,₇、R₅,₆、R₅,₁₀ |
| t：五 X | 1 | 1 | R₅,₁₂ |
| W：五 Y | 1 | −3 | R₅,₁₁ |

checker 重算既有 Figure 3 轉錄 5-poles 的邊染色計數，與十二單位循環逐座標相等，
亦比對原 [B₅ 證書](../artifacts/c5_cells/b5_face.json)。此處重新證出的完整性是
**本頁循環流錐**的完整性；文獻 B₅ 的定義及與圖來源的橋接仍見原報告。
不同循環分解可以有不同係數，但總 m 永遠為
λₜ−Σᵢλ_Tᵢ−3λ_W。計數向量的分解沒有給出來源圖的 patch 分解。

## 4. 精確支撐與 153 個 Boolean 通過者

一個 edge set 是某個非負循環流的精確支撐，當且僅當它的每條邊都在此集合
內的有向環上。必要性見 §3；充分性是把包含於集合內的所有簡單環之單位流相加，
每條保留邊皆得到正整數流。故實數可行與整數可行在支撐層完全相同。

checker 按既有 pattern 次序對全部 1,024 masks 比較三個判定：

1. 包含於 mask 的簡單循環之聯集恰等於 mask。
2. 每條 u→v 均有 mask 內的 v→u 返回路徑。
3. 原 `c5_kempe_screen.obligations`／`failure` 的 noncrossing partition screen。

全部相同。零 mask 對應零流並通過 screen；非空 1,023 項中 **153 通過、870 拒絕**。
證書為每個通過者保存整數流及循環分解；每個拒絕者保存一條流入封閉可達集的邊，
以及原 screen 的失敗 obligation。這個固定域等價沒有聲稱是任意有向圖的 Kempe 定理。

因此單加本頁線性恆等式及非負性，不能從既有 153 個候選再刪除任何支撐。
本輪沒有改寫 exterior screen、production catalogue 或既有 142／132 的差額。

## 5. 更強推論：三個 splits 的整數計數條件也不再收緊

把十座標向量 N 提升成 240 個固定色名 proper assignments 上的向量
\(\widetilde N(b)=N_{\operatorname{normalize}(b)}\)。不乘 24；每個 assignment
分別使用它所屬 pattern 的同一延伸數。

對 [既有計數 checker](../scripts/c5_adjacent_singleton_counts.py) 的每個 complementary
split，它生成 70 個 noncrossing boundary swap orbits O，附起始 assignment 及
component partition。本輪對每個單位循環 C 取所有滿足
O⊆supp(\(\widetilde C\)) 的 orbits，逐一核對

\[
\widetilde C=\sum_{O\subseteq\operatorname{supp}(\widetilde C)}\mathbf1_O.
\]

每個被選 orbit 的權重恰為 1。每個 split 下，Tᵢ 用 12 個 orbits、Fᵢ 用 16 個，
t 與 W 各用 20 個。**12×3=36 份分解，每份全部 240 座標完全相等**，不是浮點 LP 判定。

**推論**：任意滿足 chord-total 恆等式的非負整數向量 N，皆通過三個 splits
各自的非負整數 orbit 分解要求。證明：§3 給 N=Σ_C a_C C，a_C 為非負整數；
對每個 split，把上述 12 份有限分解乘 a_C 再相加，即得 N 的該 split 分解。
有限基底由 Python 證書核對，對任意大小整數係數的推廣是此紙面加法論證。

這比只比較 153 個 supports 更強：在已滿足恆等式的非負整數計數向量內，
**三套分開要求的此種 orbit 分解不能再增加排除力**。
但權重並未被認證為某張圖內部 components 的計數；也未將三個 splits 的
orbits 配成同一完整染色空間。這不是所有更強 Kempe 訊息都無效的結論。

## 6. 獨立 singleton 支撐的唯一分解與剩餘問題

令 P={i:Yᵢ>0} 是 C5 的獨立集。Tᵢ 需要相鄰 Yᵢ₊₁、Yᵢ₊₂，W 需要全部五個 Y，
因此它們不可能出現在此非負分解中。Fᵢ 只可能在 i∈P 時出現。故

\[
N=m\,t+\sum_{i\in P}Y_iF_i,\qquad m\ge0.
\]

唯一性由 Y 座標讀出每個 fan 係數，再由 m 或一個包含 P 的 chord 讀出 t 係數。
因 α(C5)=2，每個 independent P 都包含於某 {i,i−2}；該座標有 Xᵢ=m。
若再全收 T4，則 Xᵢ>0，故 m>0。checker 核對全部 11 個 independent P 的允許循環
與可讀取 t 係數的 X 座標。這接回 [既有特殊支撐面](c5_b5_face.md)，未新增排除。

一般 m≤0 的強目標，可表述成星形正貢獻受負循環補償；但在這個特殊分支，
負循環根本不能出現。剩餘精確問題是：**為何 m>0 的星形加獨立位置 fans
不能來自同一張 planar disk 的染色空間？**尚無證明。

純 t 已由 exterior wheel＋4CT 排除：兩側精確支撐互不相交，黏合後卻應有平面
四色染色。這一步明確使用 4CT；本頁流守恆或整數 orbit 分解不會排除純 t。
一般 m≤0 的來源猜想及 near-triangulation 化約仍見 [count-cone bridge](c5_count_cone_bridge.md)。
本輪沒有調查該猜想的後續文獻，也不把這個等價重述宣稱為文獻首創。

## 7. 證書、重播與信任界線

- [核對程式](../scripts/c5_circulation_audit.py)
- [完整 JSON 證書](../artifacts/c5_cells/circulation_audit.json)
- [當輪整理與驗證紀錄](history/2026-09-27-circulation.md)

```bash
python3 scripts/c5_circulation_audit.py --check
python3 scripts/c5_kempe_screen.py --check
python3 scripts/c5_b5_face.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 不帶 `--check` 時寫入 JSON；帶參數時重算並逐 byte 比對。證書保存
來源 hashes、座標表、有理數行空間、十二循環、全部 masks 的見證、36 份 orbit
分解及其 partition witnesses、十一個獨立支撐面。負控制包含破壞單一計數、
星形刪一邊，以及通過代數 screen 但與 wheel 支撐互斥的純 t。

新一般敘述屬紙面循環流論證＋固定域 Python 證書；既有 Lean 計數代數仍可沿用，
但本頁新等價、循環分類及 orbit 覆蓋均未 Lean 化。`lake build` 僅驗證既有 Lean 整合。
未重跑大圖 catalogue、degree-5/R 系列、record 110 surgery 或全策略閉包。
