# Disk embedding 到 AnnulusAccept

2026-09-12。目標是現有 triangle grammar 的 topology completeness。

**狀態：拓撲部分以下給出紙上證明，依賴標準 Jordan–Schoenflies／曲面切割事實，尚未 Lean 化。** `Math/AttachmentEndpoints.lean` 的端點環序編譯步驟是 **proved in Lean**。因此專案的完整 topology completeness 仍為 **unresolved in Lean**；不能以本文件取代形式化證明。

## 精確範圍

令 `G(w)` 是 `triangleEdges (linksOf w)`：外圈是固定有序 induced C5
`b₀ b₁ b₂ b₃ b₄ b₀`，其餘頂點是完整三角形 `t₀ t₁ t₂`，並有恰好
`k ∈ w i` 的邊 `bᵢtₖ`。圖是 simple graph。

這裡的合法 disk embedding 指有限圖的拓撲實現到閉 disk 的 embedding：

* 頂點互異，各邊為 simple arc，不同邊只可在共同頂點相交。
* C5 的整個像恰為 disk 邊界，標號沿邊界按 `0,1,2,3,4` 排列。
* 其餘頂點及所有非 C5 邊的相對內部都在 disk 內部。

不預設 straight-line、fan order、winding、necklace、degree 下界或連通性。
`AnnulusAccept` 接受的是 attachment word，故目標不是對任意 disk patch
直接套用此 predicate。較大的合法 patch 若含此 C5 和一個不相交的 K3，
可以限制到這八個頂點及上述邊後套用；這不表示 grammar 表示了整個較大 patch。

欲證：

```text
G(w) 具有上述 disk embedding
  → 可抽取五個無重複 endpoint packets F i
  → 存在 o,n,a,b,c，使 (flatten F |> map (pos o)).rotate n = 0^a 1^b 2^c
  → AttachmentNormalForm w
  → AnnulusAccept w.
```

前兩個箭頭需要拓撲。後兩個箭頭已在 Lean 中。

## 1. 三角形外側確實是一個 annulus

嵌入的 K3 是 disk 內部的一條 Jordan curve `T`。取其不包含外邊界的閉
Jordan disk `D_T`。Jordan–Schoenflies 給出 `D \ int D_T` 為 annulus。

每條 attachment 的開弧避開 `T`，且靠近其 boundary 端點時位於 `T` 的
外側。開弧連通，故整條開弧都在同一側；它不可能先走入三角形內部再接到
`tₖ`。這一步從一般 embedding 推出單側性，沒有把單側性藏在 word 定義裡。

## 2. 將共用端點分成不同 slots

在兩個邊界的有限個頂點附近取互不相交的局部半 disk，將邊界略向 annulus
內推，再截短 attachment。得到一個較小 annulus 及一族 proper simple arcs：
每條連接兩個不同 boundary components，所有端點互異，所有弧互不相交。

局部邊界選在 vertex-star 的 regular neighborhood 內；不能直接選任意
Euclidean 小圓，因為原始 topological arc 可能反覆穿過小圓。
對 polygonal embedding 這是直接的有限局部構造；對一般 topological embedding
需要平面有限 vertex-star 的局部標準化／regular-neighborhood 結果。
這是待形式化的獨立拓撲步驟，不能當作 packet 欄位的假設後宣稱已處理一般 embedding。

外側 slots 沿原 C5 順序分成五段 `F₀,…,F₄`；沒有 attachment 的頂點留下
空段。段內順序由嵌入讀出，尚未假設它是 `fan`。

內側 slots 沿三角形順序分成三段，各段所有 label 都是同一 `k`。
這是因為每個 `tₖ` 只有一個朝向 annulus 的局部 sector。讀環方向選成與外圈
`0,1,2,3,4` 相容；從 `t₀` 起內圈只可能是 `t₀,t₁,t₂` 或 `t₀,t₂,t₁`，
恰好對應 `pos true`／`pos false`。兩個邊界作為定向曲面的 induced boundary
orientation 相反；此處比較的是繞洞的同方向環序，不是兩個 induced orientations。

每條邊只有一個 slot；simplicity 保證每個 `Fᵢ` 的 inner labels 無重複，
且 `(Fᵢ).toFinset = w i`。不同 boundary packets 可以包含同一 inner label。

## 3. Annulus 端點環序引理

**紙上引理。** 一個 annulus 內有限族兩兩不相交、端點互異的 proper arcs，
每條都連接不同邊界，則以弧的身分標記端點時，兩側端點的循環順序相同
（使用上節的方向約定）。

證明如下。

1. 沒有弧時結論為空環序；只有一條弧時直接成立。
2. 否則選其中一條 `e`，沿 `e` 切開 annulus。連接不同邊界的 proper arc
   是 spanning arc，切開後得到一個 disk。此事實對繞洞的弧同樣成立，
   不需要先假設 `e` 是徑向線段或 winding number 為零。
3. 新 disk 的邊界由外側端點區間、`e` 的一份副本、內側端點區間、另一份
   副本依序組成。其餘弧沒有碰到切線，仍是 disk 中互不相交的 proper arcs。
4. 在 disk 中，兩條 proper arcs 不可能有交錯端點：第一條弧加上一段邊界
   形成 Jordan curve，交錯的另一對端點位於不同側，第二條弧必須穿過第一條。
5. 將兩側區間都按繞洞同方向讀取。若兩條弧在這兩份線性次序中的先後相反，
   它們在整個 disk 邊界上就有交錯端點。因此端點匹配沒有任何 inversion。
6. 沒有 inversion 的有限雙射保持整個線性次序。黏回兩份 `e`，即得原來的
   循環次序相同。

這裡先以**邊的身分**比較 slots，再忘掉身分只保留 inner label。
若一開始只比較 label，重複 label 會遮蔽錯誤匹配。

本引理及上述應用是此文件的推導；參考資料提供所用的基礎曲面拓撲，
不是已在 Lean 中存在的 annulus-order 定理。

## 4. 編譯成既有 grammar

套用引理後，外側串列 `F₀ ++ ⋯ ++ F₄` 的 normalized inner labels，與
內側串列有相同循環順序。內側串列正是 `0^a ++ 1^b ++ 2^c`；故存在
一個 rotation `n` 使它們相等。

保留 `F₀` 的固定起點和全部五個 packet，令 widths 為它們的長度，將上式
反向旋轉，就得到 `NecklaceCuts`。每個 packet 的 Nodup 給出 `Valid`，
對 label 取集合給出原來的 `w`。

這正是新增的 **proved in Lean** 定理：

```lean
normalForm_of_endpoint_order (w : Word) (F : Fin 5 → List (Fin 3))
  (hn : ∀ i, (F i).Nodup)
  (hw : ∀ i, (F i).toFinset = w i)
  (o : Bool) (n a b c : ℕ)
  (horder : (((List.ofFn F).flatten).map (pos o)).rotate n = necklace a b c)
  : AttachmentNormalForm w
```

`annulusAccept_of_endpoint_order` 再套 `annulusAccept_iff_normalForm`。
它沒有假設 packet 是 fan，也沒有假設 `RunOK`；局部 fan reconstruction
由既有 `NecklaceCuts.accept` 負責。這是拓撲抽取結果的編譯接口，
**本身沒有證明 noncrossing arcs ⇒ horder**。

## 5. 退化情形與信任邊界

* 零 attachment：五個 packet 全空，`a=b=c=n=0`。圖有兩個 components，
  不需要假設 connected，也不需要選切線。
* 只有一種 inner label：只有一個非空 block；grammar 的 cyclic step sum 為 0。
* 兩種 label 或三種 label：允許零長 block，沿內圈讀取全部端點一次；
  既有 necklace theorem 給出 cyclic step sum 為 3。
* 單個 boundary vertex 接三個 inner vertices：保留三個 distinct slots，
  不用預先排除 triple packet 或假設 min-degree ≥ 2。
* 共用端點：第 2 節局部分開；不把原來的共端點弧錯當成 endpoints-distinct。
* 任意共同繞洞／Dehn twist：切開實際的一條弧，證明不使用弧的 metric shape。
  `RunOK` 的 label step sum 不是原嵌入中每條弧的整數 winding number。
* boundary labels、空位置和相對對齊全數保留；不做獨立 D5 quotient。

若要聲稱 **proved in Lean 的 topology completeness**，仍須完成：

1. 獨立的 graph disk embedding 定義（不能定義成 `AnnulusAccept`、normal form
   或附帶 `horder` 的 structure）。
2. 從該定義證明 triangle separation、vertex-star slot splitting，並保存邊身分、
   packet 完整性與局部順序。
3. 證明 spanning-arc 切割及 disk 交錯端點障礙，導出第 3 節的環序引理。
4. 將抽出的資料交給已證的 `annulusAccept_of_endpoint_order`。

本輪沒有引入 topology axiom、`sorry`、假定的 bridge-conflict theorem，
也沒有以 7,194 個 masks 的外部一致性取代上述步驟。

## 拓撲背景與驗證

Jordan–Schoenflies、一般曲線與 polygonal 模型的區分可見
[Arnaud de Mesmay, GEOMGRAPHS, §1.1](https://monge.univ-eiffel.fr/~demesma/LectureNotesMPRI.pdf)。
曲面分類及 embedding 的 rotation 表示背景可見
[Mohar–Thomassen, Graphs on Surfaces, Chapter 3](https://www.sfu.ca/~mohar/Book/Ch3.html)。
這些背景尚未成為本專案的 Lean theorem；上述 slot splitting 和切割 lemma
也仍須在所選 embedding 模型中明確證明。

驗證：`lake build` 通過（8797 jobs，新檔無警告；既有 AttachmentOrder warnings 保留）；
`lake env lean Math/AutomataAudit.lean` 通過。
新兩個定理的公理依賴均只有 `propext / Classical.choice / Quot.sound`，
沒有 `sorryAx` 或 native 依賴；實際輸出列在 `artifacts/automata/lean-audit.txt`。
