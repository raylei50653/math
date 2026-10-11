# 更換保留系統的替代出口：3022 與 48-state 區域

2026-09-15。接續 [禁補償策略](c5_strategy_no_comp.md)，只分析既有 survivor-811
閉包中的 R。**一般條件引理為紙面證明，未 Lean 化；48 個實例是 Python 計算證據。**
沒有擴圖、重搜完整閉包或證明一般 K=4 策略。

## 1. 結論與確切缺口

3022 的替代出口可由以下來源構型解釋：

1. boundary 為 `(C,D,C,A,B)`，位置 3 的鄰居全是 B/C，故它獨自構成 AD component。
   因此另一個 AD component `Comp_AD(1)` 的 boundary trace 必為 `{1}`。
2. 此 component 的 cut 是 D₁₂ 的整條 `(0,1)` dual path；交換保留完整 D₁₂。
3. 在同一 cut 的兩張 retained-block 接線圖中，一個 triangle 原封轉移系統，
   另有一個 hexagon 與一個 loop 閉合。後兩者有共同的原始 dual port，並非獨立挑出的增量。

因此操作必得 singleton-4，cycles 由 `(1,0,1)` 變成 `(1,2,1)`。
這給出一條**來源接口充分條件引理**，不使用 Goal 表或目標 cycle counts 當前提。

既有 R 的 48 個來源**全部符合**此條件；這是本輪新增的有限核對，比「等高到一個
好出口」更強，但不是一般引理的必要要求。尚未證明任意同類障礙區域必能到達此構型，
也未證明單憑 boundary trace／保留 pairing 就能推出這套內部接線。

## 2. 同一原色來源的兩個出口

`A/B/C/D=0/1/2/3`，完整來源：

```text
vertices: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21
colors:   C D C A B B C C B A  A  A  D  A  A  C  D  B  D  D  B  D
```

| | BD@4 | AD@1 |
|---|---|---|
| maximal component | `{4,16,19,20,21}` | `{1,9,12,13,14,19,21}` |
| boundary trace | `{4}` | `{1}` |
| boundary 結果 | `(C,D,C,A,D)` | `(C,A,C,A,B)` |
| Goal | singleton-3 | singleton-4 |
| 保留完整系統 | D₁₃ | D₁₂ |
| cut 所在保留 path 的 terminals | `(3,4)` | `(0,1)` |
| cut 長度 | 18 | 21 |
| ordered cycles | `(1,0,1)→(0,0,3)` | `(1,0,1)→(1,2,1)` |

terminal i 位於原始 boundary edge `(i,i+1 mod 5)`，不是 boundary vertex i。
兩個 component 交於 `{19,21}`；兩個 cut 交於原邊 `{36,37,39,43,53}`。
比較使用同一份 vertex、face、edge 編號，沒有分別正規化兩次操作。

```text
BD cut: 1,7,17,18,20,21,22,23,36,37,38,39,42,43,44,48,52,53
AD cut: 0,6,10,11,14,15,16,25,28,29,32,34,36,37,39,40,41,43,53,56,57
```

### 成功的來源理由

位置 3 的鄰居恰為 `{2,4,7,20}`，顏色 `(C,B,C,B)`。沒有 AD 邊能離開位置 3，
所以 `Comp_AD(3)={3}`。boundary 上只有 1、3 使用 AD，故 `Comp_AD(1)∩B={1}`。
合法 swap 只把 boundary 位置 1 的 D 變成 A，立即得到 singleton-4；這個推導不讀
Goal 表、不依賴 cycle 數，也不需要平面性。

dual 端同一事實表現為 D₁₂ 的兩條 paths `(0,1)`、`(2,3)` 分開位置 1、3。
短的 `(2,3)` path 由邊 `{13,18,19,20}` 組成，正是 `δ({3})`。
`Comp_AD(1)` 的 cut 在本例恰好只有另一條 `(0,1)` path，沒有附加 closed dual cycles。
這個 cut 相等是額外核對的來源事實，不能從「存在 `(0,1)` path」逕自推出。

BD 操作則由來源 maximal component 的 trace `{4}` 得 singleton-3。
其 D₁₃ `(3,4)` path 與 AD 操作的 D₁₂ `(0,1)` path，各自隔出不同邊界位置。

## 3. 重接的共同原因：cycle 轉移與一個分岔端口

下表以 Pₙ 表示有 n 條邊的 path，Cₙ 表示有 n 條邊的 cycle；C₁ 是 loop，C₂
是兩條平行邊。**這是收縮 retained blocks 後的 multigraph，不是原始 dual 長度。**
無邊的 isolates 全部保留在證書；表內省略它們。H 是刪除 cut 後的 retained graph。

| 操作／系統 | H 中完整保留 cycles | Qold | Qnew | Δcycles |
|---|---:|---|---|---:|
| BD／D₁₂ | 0 | C₂ + P₅ + P₂ | P₈ + P₁ | −1 |
| BD／D₁₃ | 0 | P₁₈ | P₁₈ | 0 |
| BD／D₂₃ | 1 | P₉ | C₂ + C₅ + P₂ | +2 |
| AD／D₁₂ | 1 | P₂₁ | P₂₁ | 0 |
| AD／D₁₃ | 0 | P₆ + P₅ | C₃ + C₆ + P₁ | +2 |
| AD／D₂₃ | 0 | C₃ + P₇ | C₁ + P₆ + P₄ | 0 |

### AD：哪一個 cycle 移動？哪兩個新閉合？

令 X 為 AD cut 下 D₁₃ 的 retained quotient，Y 為 D₂₃ 的 retained quotient。
每張圖的 block 編號取決於其原始 dual vertices；Xᵢ 和 Yᵢ 並不一律代表相同集合。
完整集合在證書 `comparison[1].systems` 及 `region_checks[*].schema.charts`。

| 結構 | 原 cut 邊號 | block 接線 |
|---|---|---|
| Yold triangle → Xnew triangle | `{11,16,40}` | `2–3–4–2`，兩圖這三個 blocks 的實體集合相同 |
| Xnew hexagon | `{15,28,32,34,56,57}` | `0–5–6–9–8–10–0` |
| Ynew loop | `{39}` | `7–7` |

第一列展開 retained paths 後，兩邊的**完整 cycle 邊集都是**
`{3,11,12,16,40,51}`。所以舊 D₂₃ cycle 的確轉入 D₁₃；不是只因兩個數相等便
把它們視為同一個 cycle。D₂₃ 的最終 cycle 則是另一組邊 `{19,22,38,39}`。

控制後兩列的共同端口是 face 35，即三角面 `(20,7,21)`：

```text
e39 = (7,21),  dual ends (17,35), source type 1 → 2
e57 = (20,21), dual ends (23,35), source type 2 → 1
e38 = (7,20),  dual ends (18,35), type 3，留在 H
```

原來源在這三點的顏色為 `(B,C,D)`；AD swap 只換其中的 21，D→A。
同一 face 上兩條 cut 邊的 type 因而互換，且都以 dual vertex 35 為端點。

在 X 的 H 中，35 屬於 `X₆={6,8,18,35}`，17 屬於 `X₇={7,17,40}`。
在 Y 的 H 中，35、17 卻同屬 `Y₇={7,17,18,35}`。因此：

- e39 在 Xold 是跨 block 的 path 邊，在 Ynew 卻閉合成 loop。
- e57 在 Yold 接向 Y₇，是長 path 的一部分；在 Xnew 接向 X₆，與其他五條
  cut 邊及 retained paths 閉合成 hexagon。

這是「同一 cut 端口，在另一系統有不同 retained owner」造成的兩種閉合。
單憑 face 35 的三色仍不能保證 hexagon：還需要表中其餘 retained 接線。
這也說明 D₂₃ 的 `Δ=0` 不代表該系統保持不動：原 triangle 轉出，新的 loop 補入。

BD 的機制則不同：D₁₂ 的舊平行邊 cycle 被打開；D₂₃ 保留一個舊 cycle，
另閉合平行邊 cycle 與五邊 cycle。它以損失另一系統的一個 cycle 換得總增量 +1。
AD 改保留 D₁₂，保住了該完整系統，總增量因而可以是 +2。
這是兩次重接的精確對照，不聲稱 BD 消失的 cycle 與 AD 新增 cycle 有逐個因果配對。

## 4. 替代出口引理：來源接口充分條件

**紙面引理，未 Lean 化。** 設有限三角化 disk 有 proper 四染色，ordered C5
boundary 是 `(C,D,C,A,B)`，χ 是三個 dual systems 的 cycle 總數。固定同一色框。
假設：

1. 位置 3 的所有鄰居用 B/C。取來源誘導圖的 `S=Comp_AD(1)`、`P=δ(S)`。
2. D₁₂ 有一個 cycle、paths `(0,1)` 與 `(2,3)`，且 P 恰為其 `(0,1)` path。
3. 從來源刪 P 得到的 H₁₃、H₂₃ 都是 forests。保留所有 blocks、ports、terminals，
   以**原 cut 邊身分**接上 type 1 或 type 2 邊，得到 §3 AD 的四張 quotient 圖：
   Xold=P₆+P₅、Xnew=C₃+C₆+P₁、Yold=C₃+P₇、Ynew=C₁+P₆+P₄，外加 isolates。
   這裡「new」只是來源 type XOR 3 選邊的名稱，不要求已知目標染色或其 cycles。
4. Yold 的 triangle 與 Xnew 的 triangle 使用相同原邊與 retained paths；
   Xnew hexagon 的一條邊和 Ynew loop 邊共用一個實體 dual port，該 port 與 loop
   另一端在 H₁₃ 分屬兩塊、在 H₂₃ 同屬一塊，且 loop 邊原屬 Xold。

則交換 S 是合法 boundary-root escape，boundary 變為 `(C,A,C,A,B)`，
cycles 由 `(1,0,1)` 變為 `(1,2,1)`；它不屬指定禁用型 `[-1,0,2]`，一步峰值為 4。

**證明。** 前提 1 給 `Comp_AD(3)={3}`，故 S 的 boundary trace 為 `{1}`。
Kempe component swap 保持 properness，boundary 直接計算得 singleton-4。
cut 不含 type 3，type 1、2 在 P 上互換，非 cut 邊不變；故 D₁₂ 完整保留。
在另兩系統，以來源 type XOR 3 接線正是實際目標系統。H 為 forest，收縮保留
loops、parallel edges、isolates，因此 β(H∪A)=β(Q)。四個 shape 分別給 β=0、2、1、1，
加上保留系統的一個 cycle 得兩個向量與所述峰值。前提 4 同時辨認轉移的完整 cycle
及共用端口的兩次閉合，給出比計數更強的機制敘述。證畢。

前提 4 對數值結論是冗餘的，對本輪要辨認的共同重接機制則有內容。
本引理是偏強的可檢查充分條件，沒有宣稱最小性。**尚未由前提 1–2 推出前提 3–4**；
這正是要進一步抽取／弱化的內部結構缺口，不能把接口判定偽裝成一般存在性證明。

## 5. 此構型在 R 中如何出現

對每個來源，僅用其 boundary 同時指定角色
`A=c(3), B=c(4), C=c(0)=c(2), D=c(1)`。這是一個套在**完整來源及全部系統**上的
共同全域色對應；沒有旋轉 boundary，沒有更換原 vertex／edge 標號，也沒有各自
正規化兩個操作。任意四色置換在 F₂² 上誘導三個非零 edge types 的一致置換，
因此這種角色命名保留 ordered 系統的對應與 χ。

`source_schema(model,c)` 僅讀圖與完整來源，核對 §4 的來源 guards，之後才讀取
轉移表驗證實際目標。R 的 **48/48** 都通過；選擇角色 AD@1 均直接到 singleton-4、
χ=4。這不是將 48 個 ID 再分群：共同解釋是隔離位置 3 的局部鄰色條件，加上
同一 cut 的 coupled retained 接線。

同原色 boundary 的 3022、3529 只差位置 8、14 的 A/B 互換；它們都符合引理。
轉移 triangle 在前者由 cut 邊 `{11,16,40}` 組成，後者為 `{3,12,51}`；兩者展開
都使用完整 cycle `{3,11,12,16,40,51}`。hexagon 邊及 loop 邊保持相同。
所以可以讓 retained triangle 的切割方式改變，同時保留出口機制。
兩個來源有等高 boundary-root 路徑：

```text
3529 --BC@0--> 3978 --AB@0--> 4650 --AC@0--> 3205 --AB@3--> 3022
χ: 2 → 2 → 2 → 2 → 2
```

另保存所有 s∈R 到 3022 的等高路徑並逐步回放，確認反向仍是合法等高操作。
因而即使不採用新增的 48 個直接出口核對，既有證據也足以推出
`s →…→3022 →AD@1→1027`，全程高度 `2→…→2→4`。

R 無 Goal、全 χ=2，且對峰值≤3 的禁補償操作封閉，故任意峰值≤4 的禁補償
成功路徑，第一次離開 R 必是 `2→4`。這個必要性是舊封閉證書的邏輯推論。
本輪另核對門檻 4 下 96 條允許出口均為 `2→4`，不是以此枚舉取代必要性證明。
全程「禁補償」只指排序增量 `[-1,0,2]`，仍允許其他跨系統增減。

## 6. 重現與停止點

- [checker](../scripts/c5_alternative_exit.py)：來源 guards、兩個完整 cut audits、
  共同邊與 port、48 個直接出口、48 條等高路徑。來源 artifacts 與實作 SHA-256 綁定。
- [證書](../artifacts/c5_cells/alternative_exit.json)：保存原始標號與所有 retained blocks，
  不是只存 shape 計數。目標 coloring、cycles、Goal 是**事後獨立回放核對**。

```bash
uv run --with networkx==3.5 python scripts/c5_alternative_exit.py --check
uv run --with networkx==3.5 python scripts/c5_strategy_no_comp.py --check
lake build
git diff --check
```

下一個有界入口：研究 §4 的前提 3–4 能否由更弱的共同 port／retained path 關係推出，
以及何種等高操作保留或形成它；不能只用「χ=2 的無 Goal 區域」保證這套接線。
本輪完成此來源接口引理與固定 R 的核對；一般構型可達性仍未證。

驗證：新 checker 與禁補償 checker 的 `--check`、`lake build`（只有既有 lint）、
報告本地連結及 `git diff --check` 均通過。程式、證書與報告隨本次交接一併提交；
停在上述未證缺口，沒有背景研究或待完成驗證。
