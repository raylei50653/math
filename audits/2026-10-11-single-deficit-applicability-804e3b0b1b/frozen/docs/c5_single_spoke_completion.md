---
docgraph:
  id: c5.single-spoke-completion
  family:
    - c5
    - c5.single-spoke
  requires:
    - c5.single-spoke-cores
    - c5.two-spoke-nonadjacent
---
# Single-spoke：外部雙路徑 completion 與指定列分離

後續（2026-09-27）：[旁支 K5 minor](c5_single_spoke_branch_minor.md) 已證
指定 (01,04,1234)、禁 3 者二接點分支的 p₁ 延拓；114 筆現為 64 筆
兩列已證、50 個指定查詢未決。下文保留原輪次結論及數字。

後續（2026-09-27）：[bridge 路徑化約](c5_single_spoke_bridge_path.md) 已證
下文未決入口若拒絕 p₁，兩接點間必是奇數 bridge 路徑，全部 b3 接線
位於旁支；尚未排除，62／52 的查詢統計不變。

2026-09-27。接續 [single-spoke 必要支援化約](c5_single_spoke_cores.md)，
沿用 [非相鄰 two-spoke 的 degree-4 completion](c5_two_spoke_nonadjacent.md#3-the-pb-completion-preserves-the-actual-pentagon-component)。
研究優先序見 [HANDOFF](HANDOFF.md)。

**結果：** 交接指定的 s=0、(S₁,S₂,S₃)=(01,04,234)、C₃ 二接點型
也接受 p₂=01212，因此此支援型的三種接點角色均接受 p₁、p₂。
相同引理及既有反射可套用到原表其他具名配置：114 筆中，已證兩列延拓
由 40 筆增至 **62 筆**；20 筆只證 p₁、32 筆只證 p₂，兩列皆未決由 8 降至 0。
共新增 30 個具名配置／查詢的接受結論；剩下 52 個指定查詢未決。
19 種必要支援型沒有刪減，不宣稱它們皆可實現，也未完成全部 (2,1,1)。

## 1. 前提與保留的完整關係

沿用原報告的 finite simple induced-C5 disk 圖 G、q=01012、連通有效內點 H、
edge-minimal q-obstruction、唯一完整 degree-5 點 z 及其唯一 spoke zb_s。
其餘內點完整 degree=4，H−z 的接點分拆是 (2,1,1)。支援表另假設接受 T4。
記 U={0,1,2,3}、p₁=01021、p₂=01212；各分量的 R_C(b)、F_C(b)
與共同 z 色接合式均維持 [R10](c5_degree5_interfaces.md#1-設定與完整介面) 定義。

下面引理本身不需 T4，也不需重做支援分類。指定二接點分量 C 及原有序
接點 (u,v)，假設：

1. 實際支援 S_C⊆{1,2,3,4}，故 C 不碰 b0；F_C(q) 為 {0} 或 {3}。
2. 在同一來源中，存在兩條 z–b1、z–b4 簡單路徑，除了 z 之外互不相交；
   內點皆在 H−C−{z}，不經其他 boundary 點。原 spoke 可作長度一的路徑。

**外部雙路徑引理：** 在上述前提下，`F_C(p₂)∩{0,3}=∅`。
這是對完整分量關係的禁色投影結論，不宣稱 R_C(p₂) 是兩個 marginals 的乘積。
也不宣稱 F_C(p₂) 全空；1、2 是否被禁不由本引理判定。

## 2. 從實際路徑得到 degree-4 disk completion

若 C 在 p₂ 下禁 0 或 3，因其所有 boundary 鄰點只見 1、2，交換 0、3
保持整個 C 的 list-colorings，故兩色同時被禁。R_C(p₂) 非空，且只有兩個
接點，故 |F_C(p₂)|≤2，得到

```
F_C(p₂)={0,3}，R_C(p₂)={(0,3),(3,0)}。
```

第二式使用 R10 的逐接點解除引理，不能只從兩個座標的投影推得。
第一式已足以作下面的 completion。

保留原 C5、全部 C、C 的每條實際 boundary 邊、兩條原 z-contact 邊，
以及前提中的兩條外部路徑。刪除其他邊點。各路徑只保留通往 boundary 的
最後一邊，將其餘邊向 z 收縮；若路徑是 spoke 則不收縮。所得 K 的 z
branch set 是原 z 與兩路徑的所有內點，五個 boundary branch sets 均為
原 singleton。不同路徑內點不交，且不碰 C，所以沒有合併任何 C 點或接點。

K 恰含新增的兩條 spokes zb1、zb4；這些邊來自原路徑的最後一邊，
不是任意在 disk 上另畫的邊。全部操作是來源 embedding 的刪除／內部收縮，
保持 C5 外框與原環序。C 的內部、中間 bridges、實際 attachments 和兩個
具名 tuple 座標完全保留。因此 K 中 C 的 R_C(q)、R_C(p₂) 就是原關係。
不需要、也沒有宣稱這個 minor 保留整張 G 的 boundary 關係。

K 滿足既有 degree-4 分類的全部條件：

- 每個 C 點仍有完整 degree=4；z 現有兩條 spokes 與兩個接點，degree=4。
- 內部 C∪{z} 連通並含 cycle：C 內一條 u–v 路徑加 zu、zv 即可。
- p₂ 的 z 可用色是 {0,3}，恰被 C 禁止，所以 K 拒絕 p₂。
- K 是 minimal p₂-obstruction。刪除 incident-to-C 的任一邊，R10 解除
  所有禁色；刪除任一 z spoke 則釋放 1 或 2，該色不在 F_C(p₂)。
- p₂ 的 singleton 是 b0，K 中沒有任何內點鄰接它。C5 induced 性不變。

因此 [未接 singleton 的有環 degree-4 引理](c5_two_spoke_split_support.md#2-a-useful-consequence-of-the-existing-degree-four-classification)
作用於這張實際 K，且不需要 K 接受 T4。K 的**實際內部**只可能是 triangle，
或兩個 vertex-disjoint triangles 加一條直接 bridge，沒有任意長尾巴。
z 的內部 degree=2，故它在其中一個 triangle 上且不是 bridge 端點。

保留 z 與兩個有序接點後，C 的兩種形式恰為：

```
z=5，(u,v)=(6,7)。
C={6,7}，E(C)={67}；或
C={6,7,8,9,10}，E(C)={67,68,89,8-10,9-10}。
```

這是任意大小來源先經已證結構定理所得的完整 cover，不是由小圖實驗猜測。
每個點的 boundary degree 由完整 degree=4 決定，attachments 都在 {1,2,3,4}。
既有非相鄰 two-spoke 證書的 **36+3,456=3,492** 個接線已完整覆蓋它們；
沒有任何一項同時有 F_C(q)∈{{0},{3}} 與 F_C(p₂)={0,3}。矛盾，完成引理。
兩種接點次序均由完整 tuples 的座標搬運涵蓋，沒有分別任選端點 coloring。

## 3. 指定入口與其他支援配置的套用

在原入口 s=0、(S₁,S₂,S₃)=(01,04,234) 中，C=C₃ 是二接點。
在 C₁ 內從其原接點到一個實際 b1 鄰點取路徑，在 C₂ 內到一個實際 b4
鄰點取路徑，並各加原 z-contact 邊與末端 boundary 邊。兩分量本來不交，
因此得到引理要求的兩條路徑；無需縮短或分類 C₁、C₂。

C₁、C₂ 在 p₂ 的完整關係由支援上的相容色置換搬運，禁色仍分別是 1、2。
新引理給 C₃ 不禁 3，故可以取 **z=3**，並在三個原分量分別選一份避開
3 的完整 tuple 與其內部 coloring，再依 R10 拼接。這證 p₂ 延拓到原 G。
p₁ 沿用原支援表已證的結論。

對其他配置，checker 只使用以下可重播的充分條件，不臆造額外連通性：

- 路徑若是 spoke，須有 s=1 或 s=4 且端點相符；
- 否則從一個**其他分量**的原接點出發，終點必屬該分量的實際支援；
- 兩條非 spoke 路徑使用不同分量，故內點確實互不相交。

證書所存的是「哪個實際分量提供哪條路徑」的必要來源資料；來源圖未知時
不把它冒稱為逐點 path certificate。從連通分量到路徑的存在性由以上紙面
論證承擔。若此條件不通過，只保留未決，不據此斷言沒有外部路徑。

## 4. p₁ 僅由既有反射搬運

沿用 ρ=(3,2,1,0,4)、π=(0 1)、(Tb)_i=π(b_ρ(i))，以及既有 Lean
`contactRelation_transport`、`forbidden_transport`。反射同一來源、實際
attachments、路徑與 embedding，接點保持其原具名座標。Tq=q，且

```
T(p₁)=21010=(0 2)p₂。
```

若反射後的分量及外部路徑符合 §1，先在反射來源套用 p₂ 引理，排除
其 F(p₂) 中的 0、3，再以全域色置換 (0 2) 得 F(Tp₁) 不含 2、3。
最後用 π 的完整關係搬運回原來源；π 固定 2、3，故原 F_C(p₁) 不含
2、3。沒有重新枚舉反射側的圖或 completion。

三個原代表 s=0、1、4 的具名配置仍全部保留；s=3、2 只由原反射搬運，
兩個指定查詢同時隨之搬運，不另建立獨立支援 catalogue。

## 5. 有限表、驗證與停止點

[新 checker](../scripts/c5_single_spoke_completion.py) 與
[certificate](../artifacts/c5_single_spoke_completion/observations.json)
以原 114 筆具名配置為輸入。保留已知分量禁色與原來未知禁色上界，僅在
上述引理適用時，從二接點分量的上界移去 p₂ 的 {0,3} 或 p₁ 的 {2,3}。
未被三個上界聯集覆蓋的可用 z 色，給原圖延拓的充分條件。

| 已證查詢 | 原表 | 本輪 |
| --- | ---: | ---: |
| p₁、p₂ 都延拓 | 40 | 62 |
| 只證 p₁ | 32 | 20 |
| 只證 p₂ | 34 | 32 |
| 兩列皆未決 | 8 | 0 |

「只證」不代表另一列被拒絕。共新增 30 個接受查詢；每筆記錄來源 index、
具名支援、原 slit-disk 次序、路徑分量身份、是否反射、修正上界及保證 z 色。
另保存 19 型按禁色角色整理的新表，並核對交換兩個單接點分量的名字不改結果。
原支援 artifact 與原 3,492 項 completion artifact 均保持原樣；新證書保存
輸入 SHA256，重算全部繼承接線的 q／p₂ 完整 tuples 及反向座標關係。

證據層：**任意大小紙面路徑／minor 論證＋既有 degree-4 結構定理與外部
degree-list 定理＋Python 有限重播**。反射沿用既有 Lean 普通證明；
本輪未新增 Lean theorem，degree-4 結構、disk completion 與新分離尚未 Lean 化。

```bash
python3 scripts/c5_single_spoke_completion.py --check
python3 scripts/c5_single_spoke_cores.py --check
python3 scripts/c5_two_spoke_nonadjacent.py --check
python3 scripts/c5_two_spoke_reflection.py --check
lake build
python3 scripts/check_docs.py
git diff --check
```

實際驗證範圍見 [研究紀錄](history/2026-09-27-single-spoke-completion.md)。

**下一個窄入口：** s=0、(S₁,S₂,S₃)=(01,04,1234)，C₃ 為二接點。
本輪已證 p₂。若 p₁ 仍拒絕，C₁、C₂ 在 p₁ 均只禁 1，z 可用 {1,2,3}；
故必有 F_C₃(p₁)={2,3}，逐接點解除給 R_C₃(p₁)={(2,3),(3,2)}。
同一來源仍有 F_C₃(q)={3}。這次 C₃ 實際碰到 p₁ 的 singleton b3，
不能再引用未接 singleton 引理排除所有尾巴；須保留此實際接線另作化約。

其餘 52 個查詢、t=1 的其他分拆、t=0、degree≥6、多 degree-5、一般核心
存在性、一般單側／共同出口與 K∞=K≤5 仍未證。此處不更新一般出口定理
的適用核心，也不重開已完成的 t=2 分類、R31 或一般圖枚舉。
