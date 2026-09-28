---
docgraph:
  id: c5.single-spoke-two-two-minor
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-two-two
    - c5.single-spoke-branch-palettes
  related:
    - c5.dual-path-surgery
---
# Single-spoke (2,2)：路徑塊支援守恆與 record 110 的來源 K5 排除

後續（2026-09-28）：[外部路徑接合](c5_single_spoke_two_two_external.md) 已排除
record 104；相鄰支援對的同一 K5 引理再排除 210 筆，現剩 144 筆／72 型，
其中 54 筆雙列已證。下文與本頁 artifact 保留先前 26 排除、354 剩餘的當輪數字。

2026-09-28。接續 [(2,2) 必要分類](c5_single_spoke_two_two.md) 的 record 110，
研究優先序見 [HANDOFF](HANDOFF.md)。

**record 110 已排除。** 雙禁色原 bridge 路徑的每個連通旁支塊，其 residual
二色集合都受實際支援的換色穩定子保持。對 s=0、F_C(q)={1,2} 且 C 不接 b1
的來源，每塊都必碰 b3、b4；相鄰兩塊與其餘原路徑、spoke 及 C5 框邊給 K5 minor。
這也排除 record 119，並直接涵蓋原表 **26 筆／13 個交換分量名字後的型**。
原 380 筆 T4 保留項剩 **354 筆／177 型**，104 筆雙列已證的數目不變。

證據為任意大小紙面證明、沿用外部 degree-list 定理及 Python 局部／minor
證書；未新增 Lean theorem。未證其餘 (2,2) 可實現性或完整出口分離。

## 1. 前提與完整來源資料

沿用原分類 §1–3：G 是有限簡單 induced-C5 disk 圖，外框 B=(b0,…,b4)，
有效 H 連通；G 是 edge-minimal q=01012 obstruction。唯一完整 degree-5
點 z 只有 spoke zb0，其餘內點完整 degree=4；H−z 分成兩個二接點分量。
取其中一份 C，保留其原有序接點 (u,v)、全部 boundary 接線、原 bridges
和完整 R_C(q)。假設 F_C(q)={1,2}，且 actual support S_C 不含 1。

完整關係為 R_C(q)={(1,2),(2,1)}。同圖 (q,z=1)、(q,z=2) 的兩份 tight
拒絕 lists 與 block palettes，依原分類的外部 degree-list／K4-free 結構。
原分類 §3 給唯一路徑 P=(x0=u,…,xℓ=v)，ℓ≥1 為奇數，每條邊都是 C
的原 bridge；每個路徑點都不直接接 q 色 1、2 的 boundary 頂點。
此處不另要求 G 接受 T4；只有套入原 T4 保留表時才使用該表的篩選。

從 C 刪掉 P 的所有邊，令 W_j 為含 x_j 的連通分量。原 bridges 保證 W_j
兩兩不交；它保留 x_j 的全部旁支，且不含其他路徑點或另一原接點。
T_j 是 W_j **所有**頂點的實際 boundary 支援，包含 x_j 自己的接線。
沒有把 C 的完整關係替換成獨立接點邊際，也沒有合併另一個分量。

## 2. 路徑塊 residual 的穩定子引理

以下先以任意雙禁色 F={a,d} 表述；仍使用原分類的雙禁色 bridge 化約。
對每個 W_j，令 D_j=q(A(x_j)) 為 root 自己的 boundary 色集合，Q_j 為
全部路徑外 incident blocks 在 x_j 的 palettes 聯集。

兩份 z=a、z=d 證書的路徑外 palettes 相同：這些 rooted branches 的非
root 頂點沒有 z 邊，也沒有其他接點，lists 完全相同。沿有限 block tree
由葉向 root，任一 block 的 palette 由非 root 頂點扣除已知後代 palettes
唯一決定；這正是 [rooted palette 唯一性](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)。
此唯一性不需要指定 root 的 list，亦不斷言任意 lists 都存在證書。

在路徑內點，扣除 Q_j 後的 residual 是 {a,d}；在端點，兩份 residual
分別是 {d}、{a}。原 boundary lists 及 incident palette 的不交性因此給

\[
\boxed{D_j\cup Q_j=U\setminus\{a,d\}.}
\]

端點也適用：設 E=U\(D_j∪Q_j)，則兩份 residual 為 E\{a}={d}、
E\{d}={a}，合起來迫使 E={a,d}。這一步保留原接點的 z 色，未把端點
誤當路徑內點。D_j 與 Q_j 不交，因 palettes 包含於原 lists。

若色置換 π 固定 q(T_j) 中的每一色，則它保持所有非 root lists。
換色後的 branch palettes 由上述唯一性仍是原 palettes，因此 πQ_j=Q_j；
root 的 boundary 色也給 πD_j=D_j。故

\[
\boxed{\pi\{a,d\}=\{a,d\}\quad
\text{對每個逐色固定 }q(T_j)\text{ 的 }\pi.}
\]

這是**每一塊 W_j** 的必要條件，強於只對整份 S_C 做穩定子檢查。
推論不需要把 residual 稱為完整 rooted coloring relation，亦不刪除旁支。

在 q=01012 下，色 3 沒有出現在 boundary。若 3∉F，則 F 的每個色 c
必出現在 q(T_j)：否則 (c 3) 固定所有局部支援色，卻移動 F。若 3∈F，
同理 U\F 的每個色都必出現，否則交換它與 3。反向亦成立：這兩個所需
色都已固定時，其二色補集也保持。因此 q 下穩定子條件恰為

\[
F\subseteq q(T_j)\ (3\notin F),\qquad
U\setminus F\subseteq q(T_j)\ (3\in F).
\]

這個引理仍只使用同一來源的拒絕證書，沒有假設 T_j 可任意選取。

## 3. 實際 b3、b4 支援與五個 branch sets

回到 F={1,2} 且 1∉S_C。前節迫使每個 q(T_j) 都含色 1、2。
C 不碰 b1，故色 1 只能由 b3 供應；色 2 只能由 b4 供應。因此

\[
\boxed{\{3,4\}\subseteq T_j\quad\text{對每個 }j.}
\]

b0、b2 的額外實際接線不影響推論，所有旁支大小及 odd-cycle blocks
均保留。W_j 到 b3、b4 的兩條路徑可以共用內點；只需要 W_j 自身連通。

任取 P 的一條原邊 xy=x_(i−1)x_i，取 A=W_(i−1)、D=W_i。
P 加 zu、zv 是 simple cycle J。J−{x,y} 是含 z 的非空連通路徑；
ℓ=1 時它就是 {z}。定義五個 branch sets

\[
A,\quad D,\quad
Z=(V(J)\setminus\{x,y\})\cup\{b0,b1,b2\},\quad
X=\{b3\},\quad Y=\{b4\}.
\]

它們兩兩不交，且各自連通；Z 由原 spoke zb0 與框邊 b0b1、b1b2 接成。
全部十條鄰接皆來自原 G：

| branch-set pair | 原邊 witness |
| --- | --- |
| A–D | xy |
| A–Z、D–Z | J 上 x、y 各自另一條 cycle 邊 |
| A–X、D–X | 兩塊各自的實際 b3 接線 |
| A–Y、D–Y | 兩塊各自的實際 b4 接線 |
| Z–X | b2b3 |
| Z–Y | b0b4 |
| X–Y | b3b4 |

故原圖有 K5 minor，與平面性矛盾。論證對 P 的每條邊都成立，不只奇數位置；
奇數長度是來源化約的既有結果，minor 抽取本身不需要選邊 parity。
另一分量及它的全部原接線仍留在 G；非平面 witness 可以不使用它。
這是排除來源的 minor，沒有宣稱收縮後保留完整 boundary 著色關係。

特別地，record 110 的 C0 支援 34、record 119 的 C0 支援 034 都滿足前提。
因而不必先完成 [dual 有序重接](c5_dual_path_surgery.md) 的共同切口矛盾。
該報告的一步公式與同圖反例仍有效；本頁並未解決有限可迭代 state 問題。

## 4. 原表套用與證書範圍

[新 checker](../scripts/c5_single_spoke_two_two_minor.py) 讀取原
[(2,2) JSON](../artifacts/c5_single_spoke_two_two/observations.json)，只對
s=0、有分量 F_C(q)={1,2} 且 1∉S_C 的保留表項套用 §3。排除 IDs 為

```
110 111 116 117 119 120 125 126 130 131 132 133 134
348 351 352 353 354 355 356 357 358 367 368 369 370
```

後 13 筆是交換分量名字，不是新拓撲。反射側 s=3 僅沿用原表中保存的
完整關係反射搬運，沒有另枚舉，也不把它重複計入三代表的 26 筆。

| p₁ / p₂ | A/A | A/? | ?/A | ?/? | A/R | R/? | ?/R | R/R |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 排除後保留 | 104 | 58 | 60 | 114 | 6 | 0 | 12 | 0 |

R 仍指條件式強迫拒絕，不代表存在來源。這次已去除全部 R/R 表項，沒有
證明其餘 354 筆可實現，也未把來源排除計作新增 p 延拓。

[新 JSON 證書](../artifacts/c5_single_spoke_two_two_minor/observations.json) 保存：

- 48 個端點／內點 residual 聯集控制；六份 F 的全部直接色與旁支聯集。
- 192 個「六種 F × 32 個局部 actual supports」穩定子檢查，使用全部
  24 色置換；失敗者保留一份實際違反置換。
- 256 份 K5 抽取控制：P 長 1、3、5、7 的每條邊，兩端各四種 tether
  形狀（直接、分開 bridges、共同 cycle、共用 trunk），保留原邊、五個
  branch sets、全部十條鄰接與連通／不交核對。
- 缺 spoke、缺 tether、branch sets 重疊三個負控制，皆必被拒絕。
- 26 份原表項的完整副本（含 ordered relation schema IDs、全部 slit lifts、
  contact words、原 targets 及反射資料）、354 個剩餘 IDs 與輸入 SHA256。

這些拓撲 skeletons **不是**完整 degree-4 來源、list 實現或來源圖 cover。
任意大小成立的理由是 §2 的 block-tree 歸納與 §3 的具名連通集合抽取。
原必要表與舊證書均保留原內容；本證書是有明確來源的後續排除層。

## 5. 重播、信任界線與停止點

```bash
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 不帶 `--check` 時寫入新 JSON；帶參數時重算並逐 byte 比對。
當輪執行與未重跑的範圍見 [研究紀錄](history/2026-09-28-two-two-minor.md)。
兩輪成果的整合重播與發布範圍見 [發布紀錄](history/2026-09-28-two-two-publication.md)。
未新增 Lean theorem；build 不形式化上述 palette 歸納或 K5 抽取。

下一個窄入口為原表 record 104：s=0，(S0,S1)=(01234,04)，
(F0,F1)=({1,2},{1,3})。§2 使 C1 的每個路徑塊都接 b0、b4，但 spoke
落在這兩個框點之一，§3 的 Z 不能原樣使用。下一步保留 C0 的實際
z–boundary 路徑，研究能否把剩餘 J 接至補弧 b1–b2–b3，形成新的五個
互不相交 branch sets；本輪尚未建立或登記該排除。
其餘 (2,2)、(3,1)/(4)、t=0、高 degree／多 degree-5、一般核心存在性、
一般單側／共同出口與 K∞=K≤5 仍未證。
