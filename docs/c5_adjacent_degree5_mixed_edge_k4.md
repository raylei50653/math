---
docgraph:
  id: c5.adjacent-degree5-mixed-edge-k4
  family:
    - c5
    - c5.degree5
  derives_from:
    - c5.adjacent-degree5-interfaces
  related:
    - c5.adjacent-degree5-mixed-edge-same-endpoint
    - c5.adjacent-degree5-mixed-edge-order
    - c5.adjacent-degree5-mixed-edge-shared-t0-singles
    - c5.single-sided-exit
---
# 唯一 mixed K2 四 incidence 型：原 K4 與實際外部路徑

後續（2026-09-29）：[無 mixed 型](c5_adjacent_degree5_no_mixed.md) 已完成
同色 singleton residual、飽和禁色與逐邊 minimality；平面來源每側
只剩四型，指定雙列分離仍保留。本文 K2 排除及原證書保持。

2026-09-29，接手 main@c178cf1 與既有未提交研究成果。
**P*ᶻ=P*ʷ={u,v} 的 planar minimal q-core 不存在。**
原 z、w、u、v 已形成 K4；q-minimality 排除不碰 boundary 的 unary
分量，因而四點都有避開其餘 K4 頂點的實際外框路徑。連通外框加上
這些路徑的內點，給出 K5 的第五個 branch set。

這是任意大小的初等紙面改色／minor 證明，**不需 T4、degree-list 外部
定理或 disk 環序，target 查詢為零**。Python 保存固定圖與來源 minor
控制，未新增 Lean theorem。與前序三型合併後，唯一 mixed 原 K2 的
全部九組具名接線均已處理；一般雙 root、單側／共同出口及 K∞=K≤5
仍未證。研究優先序只見 [HANDOFF](HANDOFF.md)。

## 1. 同一來源與四條外部方向

G 有限簡單，B=(b0,…,b4) 是 induced C5，H 是非空連通有效內部。
固定 U={0,1,2,3} 與 q=01012，G 拒絕 q，刪任一非框邊後接受 q。
有序相鄰 roots z、w 完整 degree=5，其餘有效內點完整 degree=4。
H−{z,w} 的唯一 mixed **原分量**恰為 C*={u,v}，原 root incidences
為 zu、zv、wu、wv。連同原 zw、uv，Q=G[{z,w,u,v}] 是真正的 K4。

u、v 各有三個 Q 內鄰點，且 C* 沒有其他內點，因此各有恰一條
boundary 邊 ub_i、vb_j，允許 i=j。每個 root 在 Q 內也有三個鄰點，
故各有恰兩條離開 Q 的原邊；它們是 root-spokes 或通往該 root 的
unary 原分量。唯一 mixed 假設在此確保這些分量不接另一個 root。

全程保留同一 G、原分量身份、實際邊、具名 boundary 及共同色框。
本型沒有前輪 v 的三條 boundary 邊，亦不沿用前輪三角形環序。

## 2. 不碰 boundary 的 unary 不可能出現在 minimal core

**原分量引理。** 在 §1 的 minimality 與刪 zw 可延拓前提下，每個
unary 原分量 C 都有 N_B(C)≠∅。此引理不需平面性或 degree 條件。

假設 C 只接 r∈{z,w} 且 N_B(C)=∅。取原 incidence e=rx，x∈C。
令 g 為 G−zw 的一份完整 q-染色；因 zw 不屬 G[C∪{r}]，g 在該
子圖上的限制已是完整 proper coloring，沒有任何邊被刪除。
令 f 為 G−e 的一份完整 q-染色。選擇一個全色置換 σ∈S4，使
σ(g(r))=f(r)，並定義

\[
h(v)=\begin{cases}
\sigma(g(v)),&v\in C,\\
f(v),&v\notin C.
\end{cases}
\tag{1}
\]

所有 C 內邊及 C–r 邊在 g 中原本皆 proper；整份 C 的顏色一起置換，
又在唯一共同 root r 對齊，所以 h 亦滿足這些邊，包括 e。
C 沒有 boundary 邊、不接另一 root、沒有通往其他原分量的邊；C 外
的 f 完全保留，q 也沒有改變。故 h 是 G 的 q-染色，矛盾。證畢。

這是對同一來源的兩份完整刪邊染色作接合，沒有假設 f=g，亦未把 C
的接點拆開。σ 僅作用於待接回的整份 C，與外部固定的 r 色相合；
不是給相互共用頂點的兩份關係各自獨立換色。
刪 zw 的見證不可省略：不碰 boundary 的圖仍可能不可四色著色；
單靠「全色對稱」不足以宣稱該分量能接受每個 root 色。

## 3. 原外部路徑給 K5

對 r=z、w 任選一條離開 Q 的原邊。如果它是 rb_k，就取長度一的
P_r。否則它通往 unary 原分量 C_r；由 §2 取 C_r 的實際 boundary
附件，沿 C_r 內的一條簡單路徑接到該附件，得到原 r–B 路徑 P_r。
其內點全部在 C_r，避開 Q 及 B。z、w 的這兩個 unary 分量若存在，
必為不同原分量，故兩路徑內部不相交；boundary 端點可以重合。

令

\[
O=V(B)\cup\bigl(V(P_z)\setminus\{z\}\bigr)
       \cup\bigl(V(P_w)\setminus\{w\}\bigr).
\tag{2}
\]

O 由原 B 與兩條接入 B 的截尾路徑組成，連通且避開 Q。五個 branch
sets 為

\[
\{z\},\quad\{w\},\quad\{u\},\quad\{v\},\quad O.
\tag{3}
\]

前四組的六條鄰接恰為原 K4 邊。P_z、P_w 的第一條原邊分別給
z–O、w–O；ub_i、vb_j 分別給 u–O、v–O。因此 (3) 非空、連通、
互不相交，且具有全部十條鄰接，是 **原圖的 K5 minor**。G 不平面。

本論證只選原邊與路徑，未補邊，未將 root–u–B 假稱為避開 Q 的
外部路徑，也未更改著色問題後再搬回原來源。各 root 未選的另一條
外部邊可不納入 minor 子圖，原來源的完整 degree 仍保持為五。
沒有用到 boundary 的環序；故排除一般平面來源，當然也排除 disk
來源。C5／q 的具體形式屬研究前提，這一步只使用 B 連通。

## 4. 唯一 mixed 原 K2 的接線覆蓋與出口

mixed 要求 P*ᶻ、P*ʷ 都非空，因此各自只能是 {u}、{v}、{u,v}，
共九組具名接線。下表的 root／端點置換都作用於**整張來源圖**及其
附件、原分量、contact orders；boundary 與顏色不動。z、w 完整 degree
相同，u、v 亦相同，這些重新命名保留全部前提與 boundary relation。

| 代表 P*ᶻ、P*ʷ | 具名接線數 | 已完成結果 |
| --- | ---: | --- |
| {u}、{v} | 2 | [原四環次序](c5_adjacent_degree5_mixed_edge_order.md)：disk 來源排除，不需 T4 |
| {u}、{u} | 2 | [同端點原 v-star](c5_adjacent_degree5_mixed_edge_same_endpoint.md)：disk 來源排除，不需 T4 |
| {u,v}、{u} | 4 | [共鄰端點完整化約](c5_adjacent_degree5_mixed_edge_shared.md) 及[全部五型完成](c5_adjacent_degree5_mixed_edge_shared_t0_singles.md)：來源排除或指定雙列延拓，不需 T4 |
| {u,v}、{u,v} | 1 | 本文原 K4＋實際外部路徑：planar 來源排除，不需 T4 |

因此 [條件式出口第八類](c5_single_sided_exit.md) 可寫成「唯一 mixed
原分量為 K2」，不再限制 root incidence 接線。可存在的 disk 來源
必可整圖重新命名成第三列，再套用已證的 p₁、p₂ 分離；其餘三列
是來源排除，不能計作 target 接受。完整 Σ=Ω∖{q} 的接合仍須來源
雙缺失與刪邊繼承，並非由兩列延拓單獨推出。

此九組是唯一 mixed K2 的**接線覆蓋**，不是九份圖實現；不涵蓋無
mixed、較大 mixed、多 mixed 或不相鄰 roots。前序 finite necessary
tables 也沒有因此成為 disk 可實現性證書。

## 5. 可重播證書與界線

[Checker](../scripts/c5_adjacent_degree5_mixed_edge_k4.py)、
[JSON](../artifacts/c5_adjacent_degree5_mixed_edge_k4/observations.json) 與
[原路徑表](../artifacts/c5_adjacent_degree5_mixed_edge_k4/source_minor_table.md)
保存直接工具輸入的 SHA256，分開記錄：

- 五個不碰 boundary 的 unary 固定圖：384 次完整分量接回與 2,304
  次共同色框置換接回，逐次核對外部染色保持及被刪原邊恢復。
  另存不可著色的 root＋K4，說明刪 zw 見證的必要性。
- 270 份原 K4／外部路徑選取子圖：u、v 的全部 25 組 boundary 附件，
  對應兩 root 的指定 offset 端點，以及五組四路共端點控制；各配
  z、w 路徑長度 1、2、4 的九組。保存全部 branch sets 與十條原邊
  鄰接；不是任意 boundary placement 的窮舉，也不是 degree/list 實現。
- 刪除每份 witness 的任一 K4 邊或所選外部路徑邊，3,420 次均使
  **該份 witness**失效；270 次將 u 錯放入 O 的重疊負控制亦全失效。
  沒有宣稱刪邊後整張圖平面。
- 一張真正 degree=(5,5,4,…) 的 minimal q-core：原 K4 加兩份各
  二接點的 unary K2，u、v 同接 b4，其他四內點各接 b0、b1。
  q 拒絕，22 條非框邊皆存刪後完整 q-染色；原 K5 witness 證其
  **不平面**。這驗證平面假設有作用，不是 disk／T4 正控制。
- 九組具名 root incidence 的完整覆蓋與全來源重新命名映射。
  target 查詢為零，沒有重開支援／正常形或大圖枚舉。

任意大小的 §2–3 由紙面證明給出，有限控制不取代來源路徑存在證明。
本輪未使用 degree-list 外部定理；§4 整合前序結果時，仍保留那些
報告原有的外部 degree-list／Jordan 證據層。沒有獨立第二審稿者，
未新增 Lean theorem，`lake build` 不表示本輪改色／minor 已形式化。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_k4.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_same_endpoint.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及省略範圍見 [本輪紀錄](history/2026-09-29-adjacent-mixed-edge-k4.md)。
唯一 mixed K2 的四種接線代表均完成。下一窄入口為**無 mixed**：
先由完整關係接合及刪 zw 的見證核對 E_z(q)=E_w(q)={c}，再保留
兩側原 unary 關係、實際 boundary 支援與原 zw 推進。一般分離仍保留。
