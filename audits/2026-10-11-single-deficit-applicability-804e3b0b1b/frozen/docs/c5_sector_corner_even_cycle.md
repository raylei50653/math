# 3903：第一種 corner 次序的偶圈排除與單步正控制

後續狀態（2026-09-23）：[雙拒絕分類](c5_two_rejection_proof_zh.md) 已在
induced-C5 disk、非空連通內部、內點完整 degree≤4、b0 恰兩個不同內鄰點
的圖類內排除 3903。本文正文保留當輪結論與停止點；閱讀順序及證據界線見
[3903 系列導讀](c5_sector_3903_guide.md)。
非空交集的兩種 corner 次序已由 [偶圈報告](c5_sector_corner_even_cycle.md)
與 [末端 block 報告](c5_sector_terminal_blocks.md) 完成排除；
空交集另見 [空分支末端報告](c5_sector_empty_terminal.md)。

本報告保留研究當輪狀態；三輪整合與發布重播範圍見
[STATUS §63](STATUS.md#63-3903-三輪成果整合與發布)。

2026-09-21，接續尚未提交的 [飽和入口分離集](c5_sector_corner_gates.md)。
**若非空葉點分支具有第一種次序 `1,4,b,r,p,q`，則內部 C 含至少
六邊的簡單偶圈，因而每個開口框列均可延拓。這排除它作為 3903
sector；本分支只剩第二種次序 `1,4,r,p,q,b`。**

同時保存一張所有內點完整 degree=4、真正 disk 的 **397→330 單步
正控制**，其開口簽章是 4095。故不附加拒絕列的「一般 397→330
不可能」已被否定；不能再將它當成待證的一般排除命題。
3903、空交集分支與主命題仍未解，603 profiles 沒有刪除。

## 1. 從兩個交點抽取內部偶圈

沿用前報告的 G,c,S,c′、J=G−{0,w}、S′ 及具名 p,q,r,b。
原 C 連通，所有內點完整 degree≤4，c′ 是在同一 S 上交換。
只取舊 13 路徑 **R:4→r** 與新 02 路徑 **P:3→p**；它們在 J
中頂點互斥，且各自沒有其他框點。已知 wp、wr 是原 G 的邊。

在 S′ 中取從 b 到 {1,2} 的簡單路徑 γ，**到第一個框點便停止**。
於是 γ 除末端外全在 C。第一種指定 corner 次序使 γ 與 R、P
都必相交，無論末端是 1 或 2。這裡沿用前報告的同一 embedding
交錯論證，允許 b 本身是交點。

沿 γ 依次列出所有與 R∪P 的交點。因兩種類型都出現，可選取其中
相鄰而類型不同的一對，記 R 側為 t₃、P 側為 t₂。將兩點間的
γ 子路徑定向成 **M:t₃→t₂**。因此 M 的內部避開 R∪P。
不需要假設所有交點只有兩個，亦不預設 R、P 在整條 γ 上的先後。

取 R 從 t₃ 到 r 的後綴並接上 rw，得到 A₃:t₃→w；取 P 從 t₂
到 p 的後綴並接上 pw，得到 A₂:t₂→w。三條路徑只在具名末端
相交，且都不含框點：R/P 的框端點在所取後綴之前，w 是內點，
M 又在 γ 首次碰框之前。因此 **M∪A₂∪A₃ 是 C 內的簡單圈**。

其三段長度分別為正偶數：

| 路徑 | 同一染色中的交替色 | 兩端顏色 |
| --- | --- | --- |
| M | 舊 0/1 | c(t₃)=c(t₂)=1 |
| A₃ | 舊 1/3 | c(t₃)=c(w)=1 |
| A₂ | 新 0/2 | c′(t₂)=c′(w)=0 |

交點的顏色由 S′ 與兩色路徑的交集決定。三個端點 t₃,t₂,w 互異，
每段至少兩條邊，故圈長是 **至少 6 的偶數**。不同列使用舊／新
染色只是判斷同一實際路徑的長度奇偶，不是把不同圖的路徑拼接。
此抽取不使用舊 12 路徑 U 或新 13 的 2/4 分離。

## 2. 偶圈迫使所有開口列可延拓

一條簡單圈全部位於同一個 block。若 C 是 Gallai tree，這個 block
只能是 clique 或奇圈。奇圈 block 不含偶圈；而 Δ(C)≤4 使任何
clique block 至多五點，不可能包含上述至少六點的圈。因此 **C
不是 Gallai tree**。

現在任取一個在保留框路徑 1–2–3–4 上 proper 的四色列 β，令

```
Lβ(v) = {0,1,2,3} \ {β(x) : x∈N_G(v)∩Γ}，v∈C。
|Lβ(v)| ≥ 4 − |N_G(v)∩Γ| ≥ deg_C(v)。
```

由 C 連通及 degree-choosability 定理，C 可從這些 lists 著色，故 β
可延拓到 G。標準定理沿用 [list-critical 基礎 §4](c5_weak_list_cores.md#4-degree-four-部分的結構限制)，
並重新核對 [Cranston–Rabern 摘要](https://arxiv.org/abs/1511.00350)
的敘述：連通非 Gallai tree 是 degree-choosable。

**結論：此條件分支接受全部 19 個正規化開口列，十二位簽章必為
4095，而非 3903。** 3903 要求拒絕的 `01212`、`01213` 都會被接受。
這不依賴 minimality，也不需先證 T4；degree≤4 已足夠。
它是針對此分支的完整開口列結論，不是任意圖的 Σ 壓縮定理。

## 3. 為何不能只排除單步：具體 disk 正控制

先直接構造 11 內點 seed，沒有按內點數搜尋圖。除框點 0,…,4 外，
內點為 w,b,a,t₃,c,t₂,d,q,r,p,x。所有邊恰為下列路徑邊的聯集：

```
1–2–3–4
0–w–p
0–b–a–t₃–c–t₂–d–1
1–q–w–r–t₃–x–4
3–t₂–p–1
```

旧框列為 01021，內點顏色如下；此處頂點名 c 與染色函數 c 依上下文區分。

| 顏色 | 內點 |
| --- | --- |
| 0 | a,c,d |
| 1 | w,b,t₃,t₂ |
| 2 | p |
| 3 | q,r,x |

S 是含 0 的完整 01 分量，包含 0,1,2,w,b,a,t₃,c,t₂,d。
交換後精確得到 profile 330，交換前為 397；核對的是全部六份框分割。
在新 02 刪 1 後，N(0)∩B₃={w}；刪 1 的確切斷 S 中 0、2。
新 13 分離 2、4，兩個飽和 stars 是 t₂、t₃。實際抽出的偶圈為

```
t₃–c–t₂–p–w–r–t₃。
```

### 補齊 degree=4

seed 中 p 的 degree 為 3，先在邊 1p 旁加入舊色 0 內點 u，以及
pu、u1。所得 12 內點圖有八個 degree-2 內點，其餘皆 degree 4。

對每個 degree-2 內點 v，掛上一個「八面體的一條邊細分為 v」的
單點接合 gadget：新增六點，完整三部圖 K₂,₂,₂ 刪一條跨部邊 xy，
再加 xv、vy。新六點度數均為 4，v 恰增加兩條邊。此 gadget 可在
v 的小鄰域內接入，沒有新增原頂點間的路徑。

給定 v 的任意顏色，三個二點部各用其餘三色，便有 proper 延拓。
八份 gadget 之後得到 **60 內點**的固定圖；內部仍連通，每個內點
完整 degree=4，deg_G(0)=2，K=G+{01,04} 的框圈 induced 且為 disk。
這是明確度數補全，沒有枚舉更大圖。

checker 重新計算全圖的 maximal S，而非假定 S 沒有新增頂點；
交換後再次逐項核對 397→330、B₃、飽和分離集及新 13 分離。
三個階段各保存 apex rotation，刪 0,w 後由原刪邊定位六個指定
corners，直接驗出次序 `1,4,b,r,p,q`；不只查六點是否共面。

正控制接受全部 19 列，每列都有完整 degree-4 圖的明示染色證書。
因此它**不是 3903 的實現或反例**，也不是 minimal obstruction。
它否定的是漏掉跨列拒絕条件的單步排除目標，與 §2 的一般結論一致。

## 4. 重播、信任界線與停止點

[checker](../scripts/c5_sector_transition_control.py)、
[JSON](../artifacts/c5_sector_transition_control/observations.json) 保存：

- 11／12／60 內點三個固定圖、完整染色、maximal S、六組框分割；
- 三份 apex rotations、繼承 J 的面 walk 與指定 corner 入邊；
- 19 份完整開口列延拓、八個單點 degree 補全與四色局部控制；
- 八種指定邊細分的偶圈控制，圈長 6、8、10、12。

最後一項只驗 §1 較弱的偶圈前提；細分 P 的控制可能不再具有來源
profile 397，不能宣稱細分保持完整 transition。未枚舉多步交換歷史。

生成三份 rotations 使用 NetworkX 3.5；重播直接驗 rotations／Euler
條件、圖邊及指定 corners，不調用 planarity oracle。19 份染色在明確
12 內點圖上找出，再按 gadget 公式延拓；重播只查實際染色，不做搜尋。
另在禁用 planarity 與 coloring 搜尋的環境重播成功。

一般偶圈引理是紙面證明；從非 Gallai 到任意 list 延拓依賴外部
標準定理，未 Lean 化。有限正控制及細分核對不代替這兩項一般證明。

**下一問只剩第二種次序 `1,4,r,p,q,b`（於此非空分支與 3903 假設下）。**
保留 S′−{1} 切斷 b、2 的情形；尋找另一個內部非 Gallai block，或
在 Gallai block／list 條件下利用 3903 拒絕列。不能繼續把新 13 分離
本身當成第一種次序的矛盾來源。空交集分支仍開放。

非空 ≥8、總體 ≥6 下界不變；沒有最小正控制或 3903 可達性結論。
603 profiles 沿用、零刪除、未重算固定點；一般 3903、R31、共同出口
及 `K∞=K≤5` 仍未證。未 commit／push。

```bash
uv run --with networkx==3.5 python scripts/c5_sector_transition_control.py --check
uv run python scripts/c5_sector_corner_gates.py --check
uv run python scripts/c5_sector_leaf_corners.py --check
lake build
git diff --check
```
