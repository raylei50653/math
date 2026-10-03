# ε=2：t=3 原 triangle 位置的 spoke＋unary 省略核心排除

**後續（2026-10-02）**：[三原 unary 共同扇區排除](c5_excess_two_three_unary.md)
已關閉 t=3 path／tail 分支，連同 triangle 位置完成 t=3 spoke＋unary
省略分支。下文保留當輪證據及停止點。

2026-10-02，基準 `b97b107`，接續工作樹的
[t=2 spoke＋unary 排除](c5_excess_two_spoke_unary.md)、
[three-spoke 原接點保持](c5_941_three_spoke.md)及
[雙 spoke 省略排除](c5_excess_two_double_spoke.md)。目前停止點見
[Kempe 導覽](c5_kempe_guide.md)，實際驗證見
[本輪紀錄](history/2026-10-02-excess-two-three-spoke-unary.md)。

**結論：933／941 的 ε=2、唯一 degree-6 root、t=3 來源，不可能省略
一條原 spoke 及一份原 unary V 後仍拒絕列，且 r 位於剩餘全 degree-4
核心的原 triangle 上。**

這完成前輪指定的 triangle 位置分支。兩 root 色存活本身不足：
11,940 個候選比較中仍留 1,254 個；其中 1,200 個由**同一 binary
省略圖不能拒絕兩列**排除，54 個由既有雙 spoke 省略結論排除。
原 unary 保持任意大小及全部附件；沒有枚舉或替換它。

證據是任意大小紙面接合／共享省略限制及 Python 固定必要域證書。
沿用全 degree-4 分類、外部 degree-list 與原 tail transfer；未新增
Lean theorem。共同下界仍為 ε≥2，未排除 r 位於 path／tail 的情形、
其他 ε=2 分支或一般候選來源。

## 1. 前提、原分量與必要核心

G 是有限簡單圖，B=(b₀,…,b₄) 為指定有序 induced-C₅ disk 外框，
接受全部 T4，完整 Σ 為 933、941 或其整圖 D₅ 像。每條非框邊 e 都有
Σ(G−e)⊋Σ(G)。忽略孤立內點後，H=G−B 連通，
ε=Σ內點(deg_G−4)=2；唯一高 degree 點 r 的完整 degree 為六，其他
內點完整 degree 為四。本輪另明設：

- r 恰有三條原 spokes；其中 e=rb_t 是被省略的具名邊。
- V 是 H−r 的原連通分量，唯一 r 接點為 v；rv 是其唯一 root 邊。
- K=G−V−e 仍拒絕一個 singleton 列 q，且 r 在 K−B 的原 triangle 上。

K 的有效內部連通，全部內點完整 degree 為四。若取 minimal q-core，
內點 degree 至少四迫保留它的全部 incident 邊，再沿內部連通傳播，
故核心等於整張 K。r 在 K 有兩條 spokes、內部 degree 二；原 triangle
寫作 rxy，xy 是原邊。全 degree-4 分類給 K−B−r 是同一原 binary
分量 C₂，接點恰為 (x,y)；原 G−B−r 的分量恰為 C₂、V。

對整張圖共同作一次 D₅ 與 S4 搬運，令 q=q₄=01012。兩個目標的像為

\[
933:\{933,934,940,948,996\},\qquad
941:\{941,949,950,998,1004\}.
\]

由 [three-spoke 報告 §2–3](c5_941_three_spoke.md#2-原-degree-2-root-的完整位置分類)，
無枝 triangle、triangle 加一／兩條 tails、直接 bridge 雙 triangle
涵蓋所有此類 K。縮尾保留原 x、y、xy、r、spokes 及
\(R_{C_2}(b;x,y)\) 對每份 proper b 的完整關係。
V、v、rv 與 V 的全部實際 boundary 附件完全不變。

必要域沿用 36 個未篩 disk 的 T4 全收無枝模型、18 個帶枝 bases、
64 個雙 triangle bases，共 118 個 bases／398 個原 degree-2 triangle
位置。每個位置可接回三種具名 spoke，共 1,194 次接回。
這是已封存的必要域，沒有擴大圖枚舉，也不聲稱全部模型能實現為 disk。

## 2. 四接點精確接合與非空 unary relation

固定任一 proper boundary coloring b，令

\[
S_V(b)=\{d:\text{原 V 可完整延拓 b，且 }v=d\}.
\]

由 [unary slack 引理](c5_excess_two_spoke_unary.md#2-原-v-的-relation-非空不需分類其大小或支援)，
非接點的 boundary lists 至少是內部 degree，v 則多一單位；以 v 為根的
spanning-tree 逆序貪婪染色給 \(S_V(b)\ne\varnothing\)。這沿用全部
原附件，不需要 V 的大小上界或 block 分類。

令 T=K+e，\(\mathcal T(b)=\mathcal R_T(b;r,x,y)\)，且
\(A(b)=\{a:(a,c,d)\in\mathcal T(b)\}\)。完整來源 relation 恰為

\[
\mathcal R_G(b;r,x,y,v)
=\{(a,c,d,h):(a,c,d)\in\mathcal T(b),\ h\in S_V(b),\ a\ne h\}. \tag{1}
\]

每個 tuple 由 T 與**同一原 V** 的完整染色拼接；兩者只共用 B，再
核對 rv。C₂ 從未被兩個 endpoint marginals 取代，各分量亦未獨立換色。
由 (1) 得三種情形：

1. A(b)=∅：T 已拒絕，接回 V 仍拒絕。
2. |A(b)|≥2：任取原 V 染色，都能選異於 v 的 root 色及完整 tuple，故 G 接受。
3. A(b)={a}：G 拒絕**若且唯若** \(S_V(b)=\{a\}\)。

第三項保留整份原一接點 relation，而非只說 V「可能禁止 a」。
不同列的 singleton 要求同時施於同一 V，不能當成可獨立選取的來源。

## 3. 同一省略圖的兩項限制

### 3.1 省略同一 C₂，至多拒絕一列

令 \(L=G-C_2\)。L 保留原 V、全部 V 附件、rv、r 的三條原 spokes
及原 B。r 刪去 rx、ry 後完整 degree 為四，V 的 degrees 不變；內部
\(\{r\}\cup V\) 仍連通，且 L 繼承 disk／T4。

若 L 拒絕任何 singleton 列，上一節相同的 degree-4 飽和傳播迫它自身
為 minimal obstruction；由[全 degree-4 合成](c5_k4_blocks.md#4-合成全-degree-4-的單缺失結論)，
其完整 Σ 只缺該列。因此

\[
\boxed{L=G-C_2\text{ 至多拒絕一個 singleton 列。}} \tag{2}
\]

假設某個目標 mask 迫 (1) 的第三種情形，\(S_V(b)=\{a\}\)。若三條
原 spokes 在 b 的色集合加上 {a} 恰覆蓋四色，則同一 L 拒絕 b。
兩個不同列同時出現此事即違反 (2)。這是固定**同一張省略圖**的跨列
限制；不把兩份不同染色相加，亦不需要跨列 root 色名守恆。

### 3.2 省略兩條原 spokes，必全收

由[雙 spoke 省略排除](c5_excess_two_double_spoke.md#4-必要域的結果及較強的有限觀察)，
在本輪所有候選／唯一 degree-6／ε=2 前提下，任意兩條不同原 spokes
e₁、e₂ 都滿足

\[
\boxed{\Sigma(G-\{e_1,e_2\})=\Omega.} \tag{3}
\]

設只保留原 spoke rb_s，且目標迫 \(S_V(b)=\{a\}\)。令
\(F_{C_2}(b)=\bigcap_{(c,d)\in R_{C_2}(b)}\{c,d\}\)。若

\[
F_{C_2}(b)\cup\{b_s,a\}=\{0,1,2,3\}, \tag{4}
\]

則這份具名雙 spoke 省略圖仍拒絕 b，違反 (3)。Checker 用完整
(r,x,y,v) relation 重算此空纖維，而非只比較 (4) 的色集合。
省略後 tuples 可能超出 T 的 tuples，所以不能直接過濾原 T relation。

原 C₂ 的關係化約同時保持全部 root 不等式的任意子集，故上述判定
對原任意大小 C₂ 仍成立。刪除整份原 C₂ 時，留下的 L 更是未改寫的
原 r、V 與 spokes；兩項推論都保留原省略身份。

## 4. 全表結果與逐項見證

按「已拒絕目標接受列 → 兩 root 色存活 → 同一 C₂ 省略拒絕兩列 →
雙 spoke 省略仍拒絕」的順序分類，每個比較只計一次：

| 排除理由 | 933 的五像 | 941 的五像 |
| --- | ---: | ---: |
| T 已拒絕目標要求接受的列 | 1,556 | 2,703 |
| 兩 root 色迫目標拒絕列接受 | 3,940 | 2,487 |
| 同一 C₂ 省略圖被迫拒絕兩列 | 456 | 744 |
| 具名雙 spoke 省略圖仍拒絕 | 18 | 36 |
| 合計 | 5,970 | 5,970 |
| 剩餘 | 0 | 0 |

其中 1,114 個中間圖 T 接受 T4。前兩項後的 1,254 個剩餘比較正是
兩色存活的適用界線；後兩項以同源省略限制全部關閉。
計數含具名位置及接回重複，不是 graph class 數，也不是 disk 實現數。

每份第三／第四類證書都保存原 V 被迫的 singleton relations、列身份，
及同一 C₂ 頂點集合或具名 spoke pair。四接點算子對最後一欄限制到
原 S_V(b) 才是 (1)；算子中的自由 v 只用來核對全稱接合，不能充當
原 V 的內部染色或一個合法 degree-4 source vertex。

兩份可直接定位的見證（`base_id` 是證書的原零起算索引）如下：

- base 0、r=5、接回 b₂r、目標 934：在 01201、01202 兩列，原 V 都
  被迫有 S_V={3}；三條原 spokes 在 b₀、b₁、b₂，兩列都看見 0、1、2。
  省略同一 C₂={6,7} 後兩列皆拒絕，違反 (2)。
- base 0、r=7、接回 b₄r、目標 948：01212 列迫 S_V={0}。
  省略具名 b₂r、b₄r，只留 b₃r 後，完整四接點 relation 的 v=0
  纖維仍為空，違反 (3)。

這些都只是必要模型的排除見證，不是原 unary 或完整 disk 來源的實現。

## 5. 重播、信任範圍與停止點

[Checker](../scripts/c5_excess_two_three_spoke_unary.py) 與
[artifact](../artifacts/c5_excess_two_three_spoke_unary/observations.json) 保存
具名 bases、原 edges／attachments／ownership、三接點 tuples 與完整
核心染色 witnesses、四接點算子、全部十五種非空 unary relation
接合控制、兩種省略算子及逐候選排除見證。

新 checker 重建 80 個無枝必要 supports（其中 36 個 T4 全收）、驗證
既有帶枝／雙 triangle 的 degree／rotation／q₄-criticality，並重建
全部 398 個標記位置。它核對 3,980 次核心列關係、11,940 次 spoke
接回及四接點算子、179,100 次非空 unary 接合、11,940 次 binary
省略算子及 35,820 次雙 spoke 省略算子，均以完整回溯對照接合式。
核心 witnesses 完整保存；雙 spoke 省略後的每個 tuple 另索引同一
原 C₂ 的完整染色，與原 root／boundary／endpoint 色拼接核對。
未指定的 V 染色由紙面 slack 引理提供。

```bash
python3 scripts/c5_excess_two_three_spoke_unary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_three_spoke_unary.py --check
python3 scripts/c5_941_three_spoke.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

大型證書按 [artifact 政策](../tools/artifacts.py)登錄 manifest 與 producer
依賴；明列 three-spoke 與雙 spoke 證書為輸入，並核對兩者直接 source
hashes。任意大小分類、tail transfer 與 (2)–(3) 是沿用或新增紙面推論，
Python 只證固定必要域；`lake build` 不會將其提升為 Lean theorem。

本輪停止於 t=3 的原 triangle 位置。r 在 path／tail 時，K−r 不再
是同一 binary 分量，不能套用本輪 398 個位置的涵蓋；兩份 unary／
binary 省略、無全 degree-4 真子核心、兩個 degree-5 roots 等亦保留。
沒有提高 ε≥2 下界、證一般候選排除、共同出口或 `K∞=K≤5`。
後續窄入口由 [Kempe 導覽](c5_kempe_guide.md)維護。
