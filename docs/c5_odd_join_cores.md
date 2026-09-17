# 整個 odd-join 家族的單缺失分離

2026-09-17。接續 [四內點與無界 odd-path 家族](c5_four_vertex_cores.md)。
本輪處理交接提出的整個 `K2 ∨ C_(2m+1)` quotient 家族，得到任意長度的
條件式分離結論；不只是上一輪可反覆伸長的某一個例子。
證明由紙面 minor 化約、固定大小拓撲證書與路徑著色組成，尚未 Lean 化。

後續：[degree-4 樹核心](c5_tree_cores.md) 已處理任意大小的全 degree-4 內部樹，
包含 odd-join 之外的兩-run 路徑家族；下一個窄問題改為含 cycle block 的核心。

## 1. 結論及適用範圍

令 G 是以有序 C5 為外圈的 disk graph，接受全部 T4。
固定三色 singleton pattern q，假設 G 的非外圈邊集是 inclusion-minimal
q-obstruction；忽略孤立內點。把三個 boundary q 色類各識別成一點，
所得簡單圖若是 `K2 ∨ C_(2m+1)`，m≥1，則

`Σ(G) = Ω \ {q}`。

這是**紙面化約加可重播有限證書的條件式一般結論**，不稱為純紙面分類或
Lean theorem。尤其沒有宣稱任意 minimal obstruction 都有此 quotient。
boundary 同色識別只用於著色與圖形分型，完全不要求識別保存平面性。

對候選 A 的含義：任意大小來源的某側只要有一個此型 minimal obstruction，
就存在相應的單側 weak exit。若單側出口失敗，該側每個 minimal obstruction
不但至少五個有效內點，而且都不屬於此 odd-join 家族。
共同 pivotal edge 與一般三出口命題仍未證。

## 2. Boundary triangle 的位置只有兩型

沿用 [list-core 化約](c5_weak_list_cores.md)：T4 排除 boundary chords；
minimality 排除同一內點連到兩個 q 同色的 boundary 頂點。
因此從 quotient 拆回原圖時，每條 boundary-color／內點邊恰好選該色類的
一個 boundary 頂點，不會漏掉額外的重複 spoke。
三個 boundary 色類在 quotient 中構成 triangle。

令奇環長度為 ℓ≥5，兩個 hubs 為 h₀,h₁。奇環沒有 triangle，故只有：

| 型態 | Boundary triangle | 有效內點結構 |
| --- | --- | --- |
| I | h₀、h₁、一個環點 | 偶數點路徑 P_(ℓ−1)；每點各接兩個 hub 色類，兩端再接第三色類 |
| II | 一個 hub、兩個相鄰環點 | 一個內部 hub 加奇數點路徑 P_(ℓ−2)；hub 接全部路徑點與三個 boundary 色類，路徑各點接 boundary hub 色類，兩端另接相應環端色類 |

將 q 經 boundary rotation 與顏色置換固定成 `01012`，不損一般性。
枚舉三個色類放入 boundary triangle 的位置，僅商交換 hubs（I）或反向讀環（II），
即覆蓋所有 lifts；不商有序 C5。ℓ=3 時 quotient 是 K5，所有 triangle 等價，
另列十六個二內點 lifts。

## 3. Disk 強迫路徑中段 attachments 恆定

「中段」不包括路徑的兩端。型 I 的每個中段點有兩條 boundary spokes；
型 II 的每個中段點有一條 boundary spoke，以及到內部 hub 的邊。

**有限拓撲事實：**

1. 型 I、ℓ=5：384 個 lifts 中，256 個的兩個中段點有不同 boundary neighborhoods；
   全部非 disk。
2. 型 II、ℓ=6：272 個 lifts 中，128 個的兩個中段點有不同 boundary neighbors；
   全部非 disk。這裡的偶環只是拓撲測試，沒有稱它為 q-obstruction。

每個排除項目都保存 boundary-apex 圖中的 K5 或 K3,3 subdivision。
checker 逐條追蹤分支間路徑，確認真實邊、內部頂點互不相交與完整目標接線；
不只保存 planarity 布林值。接受端保存並核對球面 rotation 的 darts 與 Euler 式。
有限模板覆蓋仍依賴 Python，disk/apex 及 subdivision 排除的拓撲意義屬紙面。

**任意長度的 minor 化約：** 假設中段 attachments 不恆定，保留路徑兩端及
任意兩個 attachments 不同的中段點。刪掉未保留點的 spokes，型 II 也刪其
到內部 hub 的邊；把四個保留點之間的路段收縮成邊。
原有 boundary C5、兩端的額外 spokes、型 II 的 hub 及其 boundary spokes
全部保留。得到的正是上述型 I 四內點 lift 或型 II 五內點 lift。
可把路徑分成四個互不相交、各含一個保留點的連通 branch sets，因此這是
真正的 minor operation，不是同色 boundary 識別。

若原圖有 disk drawing，在外側加 apex 後得到平面圖，以上刪除／收縮仍平面，
與有限 subdivision 證書矛盾。因此所有中段點有相同 attachments。
型 II、ℓ=5 僅一個中段點，結論自動成立。

## 4. 恆定中段可以縮短，且保存完整 relation

固定任意 proper boundary coloring b；型 II 再固定內部 hub 的顏色。
所有中段點的可用色相同，記為 S：

- 型 I：排除兩個共同 boundary 鄰居的顏色。
- 型 II：排除共同 boundary 鄰居及內部 hub 的顏色。

所以 |S|≥2，即使兩個被排除顏色恰好相同也成立。
固定路徑兩端的顏色 x,y，二者**不必在 S 中**。有 r 個中段點時：

| | r 為奇數，r≥1 | r 為偶數，r≥2 |
| --- | --- | --- |
| S 有兩色 | 不可延拓 iff `{x,y}=S` | 不可延拓 iff `x=y∈S` |
| S 至少三色 | 永遠可延拓 | 永遠可延拓 |

|S|=2 時沿路交替即得公式，端點不在 S 時相應限制消失。
|S|≥3 時，r=1 可避開 x,y；r=2 可先選避開 x 的色，再避開它及 y。
任何已有中段著色均能將一個中段點 s 替換成 `s,t,s`（t∈S、t≠s），
增加兩點。因此兩個基底覆蓋所有 r。
checker 另核對全部十一個 |S|≥2 的四色子集、全部十六組 x,y、r=1,…,6，
以及相應 Boolean transfer 的平方穩定式；無界長度來自上述歸納。

型 I 的 r=ℓ−3 為偶數，可縮成 r=2；型 II 的 r=ℓ−4 為奇數，可縮成 r=1。
縮圖都只有四個有效內點。保留相同端點與 spokes，收縮中段路徑給出 disk minor；
上述公式則另外證明完整 relation 相等。**不是把一般 edge contraction
誤當作 relation-preserving operation。** 型 II 對 hub 顏色取存在量詞即可。

兩型縮圖的所有 disk lifts 共十六個，八個接受全部 T4，這八個都恰好只拒絕 q。
這裡固定 q 且只商所述 quotient automorphisms，數字不是上一輪的一百模板數。
ℓ=3 的十六個 lifts 有六個 disk、兩個 disk/T4，也都只拒絕 q。
完整 240-row relation 用兩種 coloring 算法核對；每個 disk 基底另檢查所有
非外圈邊對 q 的 criticality。這完成 §1 的有限基底。

## 5. 同面假設確實必要

型 I、ℓ=5 的 lifts 有 192 個接受全部 T4，其中 23 個同時缺失多個 singleton；
型 II 對應為 60 個中的 4 個。它們全部非 disk。
證書保存第一個具體控制，完整 relation 為 1020，即同時缺 singleton-4、singleton-3。
其非外圈邊為

```
05, 06, 07, 16, 17, 28, 35, 38, 45, 48, 56, 67, 78.
```

在 q 下它仍是 minimal obstruction：quotient `K2 ∨ C5` 對所有可刪邊
edge-critical，且每條 spoke 對應唯一 quotient edge。這也可由 checker 的
q 單刪檢查重播。此控制只說明不能移除 disk 假設，不是候選 A 反例。

另從十六個四內點 disk 基底分別增加 2、4、8 個中段點，得到 48 個較長 lifts；
獨立回溯核對全部 240 boundary rows 與 disk planarity，均與縮圖相同。
這是對化約的跨長度檢查，任意長度結論仍由 §3–4 論證負責。

## 6. 下一個值得挖的缺口

此族已有任意長度的縮減，繼續增加奇環長度不會帶來新障礙。
下一步宜研究 **不屬於 odd-join 的 minimal quotient**，而非一般 k=5 全圖枚舉：
先用 degree-4 Gallai 部分與 degree≥5 內點之間的接線，找出下一種可能的
critical quotient；優先尋找同時拒絕另一個 singleton、但接受 T4 的最小機制，
再問其 boundary lifts 能否 disk。若從既有非同面控制出發，必須保存完整
boundary 接線，不能只看抽象 quotient 的可著色性。

另一路是共同 pivotal edge；本輪沒有將它化約成 odd-join 分離問題。
沒有新增 Lean theorem、沒有證一般候選 A 或 K∞=K≤5，沒有重跑全量 deletion audit。

產物：[checker](../scripts/c5_odd_join_cores.py)、
[有限證書](../artifacts/c5_odd_join_cores/observations.json)。

```bash
uv run --with networkx==3.5 python scripts/c5_odd_join_cores.py --check
uv run --with networkx==3.5 python scripts/c5_four_vertex_cores.py --check
uv run --with networkx==3.5 python scripts/c5_weak_list_cores.py --check
lake build
git diff --check
```

驗證通過：新 checker 逐 byte 重播、four-vertex 與 list-core checkers、
`lake build`（8,820 jobs，僅既有 lint）、四份入口／報告的 144 個本地連結，
以及 whitespace 檢查。本輪產物與 odd-join／tree／triangle 三輪成果一併納入本次發布提交。
