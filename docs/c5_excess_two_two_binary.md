# ε=2：t=2、(2,2) 的原 binary 省略分支排除

**後續（2026-10-03）**：[t=2、(2,1,1) 兩份原 unary 省略](c5_excess_two_two_unary.md)
已完成本輪留下的下一窄題；該型後由
[短支援引理的共同推論](c5_excess_two_single_spoke_complete.md#4-結論證據層與停止點)
作整型排除。下文保留本輪 (2,2) 的結論與驗證，現況由導覽維護。

2026-10-02，基準 `bbd900a`，接續工作樹的
[t=3 binary 省略](c5_excess_two_binary_omission.md)。目前接手點見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[研究紀錄](history/2026-10-02-excess-two-two-binary.md)。

**結論：933／941 的固定完整 Σ、edge-minimal C₅ disk 來源，若 ε=2、
唯一 degree-6 root r、t=2，且 H−r 的原接點分拆為 (2,2)，則省略
任一整份原 binary 後必接受全部十列。**

任意大小涵蓋沿用原接點 tail transfer 與全 degree-4 分類；新增證據是
紙面完整接合、明確 apex K₃,₃ subdivision 及 Python 固定域證書。
未新增 Lean theorem。沒有排除整份 (2,2)、其餘 ε=2 或一般候選來源；
兩候選的共同下界仍為 ε≥2。

## 1. 完整前提及同一原五接點關係

G 有限簡單，指定有序 induced-C₅ 外框 B=(b₀,…,b₄) 是 disk 邊界，
完整 Σ 為 933、941 或其整圖 D₅ 像；每條非框邊 e 均有
Σ(G−e)⊋Σ(G)。有效內部 H 連通，r 的完整 degree 六，其餘內點完整
degree 四。r 的兩條原 spokes 為 rb_s、rb_t；H−r 恰有兩份原連通
分量 A、C，原有序接點分別是 (x,y)、(u,v)，四點互異。
所有原附件、ownership、root 邊與內部邊保持。

固定 proper boundary coloring b，原二接點完整 relations 記作
R_A(b;x,y)、R_C(b;u,v)。刪除 r 後，各分量接點有 slack；生成樹
逆序貪婪染色使兩份 relation 在全部十列都非空，見
[容量報告](c5_independent_support_capacity.md#2-任意-root-的完整條件介面包含-mixed)。
精確五接點關係是

\[
\mathcal R_G(b;r,x,y,u,v)=
\{(a,c,d,e,f):(c,d)\in R_A(b),\ (e,f)\in R_C(b),
\ a\notin\{b_s,b_t,c,d,e,f\}\}. \tag{1}
\]

每個 tuple 分別取同一 b 下兩份原分量的完整染色，檢查四條 root 邊後
拼接。令 F_A=∩_{(c,d)∈R_A}{c,d}，F_C 同理；兩者大小至多二。
式 (1) 在 r 的精確投影為 U∖({b_s,b_t}∪F_A∪F_C)。此投影只供
固定 root 接線查詢，不是取代完整 binary relation 的一般 state。

## 2. 第一份省略核心及必要列限制

反設 K=G−C 拒絕 q。其有效內部連通且完整 degree 全為四。
minimal q-core 的 degree-4 飽和沿內部傳播，迫它等於整張 K。
由[全 degree-4 分類](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，
Σ(K)=Ω∖{q}。在原 A 內取 x–y 路徑，連同 rx、ry 給經 r 的 cycle；
分類迫 r 位於原 triangle rxy，xy 為原邊，r 的內部 degree 二。

對整張圖共同作 D₅／S4 搬運，把 q 對齊 q₄=01012（十列索引 0）。
其後不獨立正規化 A、C。原 triangle／tails／雙 triangle 的位置分類
及有序 (x,y) relation 保持，正是
[941 three-spoke 報告 §2–3](c5_941_three_spoke.md#2-原-degree-2-root-的完整位置分類)：
118 個 bases／398 個具名原 r 位置。這裡使用原兩-spoke 核心，
不使用該報告新增第三條 spoke 的接回圖。

無枝 triangle 有 36 個 T4 全收必要 bases，尚未篩 disk；帶枝與直接
bridge 雙 triangle 分別有 18、64 個 bases，附原 apex rotations。
尾枝化約保持全部 proper b 的原 R_A，故式 (1) 在接上任意原 C 時
仍保持。縮減只在各自原分量內進行，不把兩份支持獨立拼成來源。

同一原圖另有兩個必要限制：

1. L=G−A 也是連通、全 degree-4、T4 全收的 disk 圖。若拒絕任一列，
   飽和傳播及分類使其完整 Σ 恰缺該列；故它至多拒絕一列。
2. 由[雙 spoke 排除](c5_excess_two_double_spoke.md)，G−{rb_s,rb_t}
   全收，故每列 F_A∪F_C≠U。

對每個標記核心、兩候選各五像及十列，checker 放寬枚舉全部
|F_C|≤2 的集合，保留式 (1) 的目標接受性及上述第二項。若某列
每個剩餘 F_C 都使 {b_s,b_t}∪F_C=U，稱該列迫 L 拒絕。
兩列同時迫拒絕即違反第一項。跨列獨立選 F_C 是必要域放寬，
不宣稱那些集合有同圖實現。

## 3. 無枝核心的明確 disk 障礙

36 個無枝必要 bases 中，12 個有兩個 triangle 頂點 p、q 共用同一
對原框鄰點 {a,b}。第三 triangle 頂點 z 有另一框鄰點 c∉{a,b}。
在外框外加 apex w 及五條 wb_i。若原核心是 disk，此 apex 圖必平面。
但它有 K₃,₃ subdivision：左右分支點分別為 {a,b,z}、{p,q,w}，
八條連接是原單邊，最後 z–w 用原路徑 z–c–w。

九條路徑的內部互斥，唯一內點 c 不是分支點。Checker 逐條核對原邊、
六個不同分支點及內部互斥；不依賴 planarity oracle。這只排除已明示
的 12 個無枝必要 bases，沒有宣稱其餘必要模型或最後接合圖可實現。

## 4. 第二份原核心必須共用框點、spokes 與色框

必要限制後剩 90 個比較，全屬無枝 triangle；§3 排除其中 54 個。
其餘 36 個均為 941 比較，且每個恰有一列 q' 迫 L=G−A 拒絕。
因此 L 自己也是全 degree-4 minimal q'-core，r 在原 triangle ruv 上；
**原 C** 也可套用同一任意大小分類及有序接點保持化約。

對第二份核心保存其 source base／root ID、完整 (u,v) relation、全部
原附件與一個明示 D₅ 框點映射 π。只容許同時滿足：

- π 把第二核心的兩個 spoke 端點映到第一核心的同一具名 {s,t}；
- 固定當前 q'，拉回 b↦q'(π(b)) 後的 canonical row 正是 q₄。

對每一當前列 b，先拉回 b∘π，再共同換回字面色名，輸出完整 R_C；
沒有逐分量自行重命名色。兩個縮減可在原 A、C 內分別進行，因它們
只共用 B、r 且所有介面保持，式 (1) 對兩個縮減同時成立。

36 個比較中，24 個在全部 398 個位置及十個 D₅ 映射中無相容第二
核心；其餘 12 個共有 2,376 個具名接合，全不等於目標 Σ。
Checker 以原完整 relations 計算十列，並對每個接合的第一個目標差異列，
獨立從兩核心的原邊建圖回溯，核對完整 (r,x,y,u,v) relation。
每個非空 tuple 保存全圖染色 witness；空 relation 由完整回溯核對。
它們是分類必要核心的接合控制，不是新增來源圖枚舉。

## 5. 證書與數字

[Checker](../scripts/c5_excess_two_two_binary.py)及
[artifact](../artifacts/c5_excess_two_two_binary/observations.json)保存 source hashes、
具名第一核心索引、必要列選項、K₃,₃ 九路徑、第二核心索引及 D₅ 映射、
差異列完整五接點 relation 與逐 tuple 完整染色。第二核心的新內點
依原 binary 頂點順序另編號，只識別字面 B、r；兩份 ownership 不混合。
原附件、rotations 及全部十列 relations 由已 hash 的來源 artifact 取得，
checker 重新由原邊核對 398 個位置及其十列，不只相信保存的 flags。

| 第一階段原因 | 933 五像 | 941 五像 |
| --- | ---: | ---: |
| 原核心已拒絕目標須接受的 q₄ | 398 | 796 |
| 某列無必要 F_C 選項 | 364 | 273 |
| 同一 L 被迫拒絕至少兩列 | 1,198 | 861 |
| 原核心的 apex K₃,₃ | 30 | 24 |
| 被迫分類第二原核心 | 0 | 36 |
| 合計 | 1,990 | 1,990 |

2,376 次接合的完整 Σ 為 886、1002 各 36 次，1006、1014 各 1,152 次；
全無目標。計數含具名重複，不是新的 class 數。故反設不成立，得到

\[
\boxed{\Sigma(G-A)=\Sigma(G-C)=\Omega.}
\]

## 6. 重播、停止點及證據界線

```bash
python3 scripts/c5_excess_two_two_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_binary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
python3 scripts/c5_941_three_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪完成指定 t=2、(2,2) binary 省略分支。連同雙 spoke 結果，該型的
容量二省略全收；若來源仍存在，其 minimal rejected-row core 須有
高 degree 點。理由是 G−r 在每列可染色，所以拒絕核心必含 r；任何
被保留的其他內點原 degree 已是四，飽和沿原 A 或 C 傳播，迫整份分量
及全部原接線保留。因此要把 r 的 degree 從六降到四，只能省略一份
完整 binary 或兩條原 spokes，兩者已排除。

未排除整份 (2,2)，未提高 ε≥2，未證一般出口或 K∞=K≤5。
其餘 t=2 分拆、其他 t 及兩個 degree-5 roots（含 mixed）仍保留；
下一窄入口由導覽維護。

外部 degree-list 定理、全 degree-4 結構及任意長 tail transfer 沿用
依賴報告。Python 負責固定必要域及原邊證書，紙面負責任意大小涵蓋；
`lake build` 通過不表示新拓撲或接合排除已 Lean 化。
