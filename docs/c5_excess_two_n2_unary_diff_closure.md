---
docgraph:
  id: c5.excess-two-n2-unary-diff-closure
  family: [c5, c5.excess-two, c5.n2]
  requires:
    - c5.excess-two-arc-size-bound
  derives_from:
    - c5.excess-two-n2-diagonal-three-row
    - c5.excess-two-n2-partition-rule
---
# N2 原55：兩接線 unary 的全色出口與含 U 子情形排除

**後續（2026-10-13，BASE 243a125）**：[N2-BRIDGE](c5_excess_two_n2_bridge.md)
另排932，完成原E4完整三列來源契約的N2；E-ARC2仍OPEN，未新增Lean證明。
以下各輪證明與停止點保留當時語境。

**後續（2026-10-13，BASE 3097ef5）**：[同來源 LL-CUT+diag](c5_excess_two_n2_ll_cut.md)
已排指定完整Σ契約的最後 `(2,0)`，九格全覆蓋；基本LL-CUT未獨立證成。
LL-CUT當輪未涵蓋的原E4三列N2，後由上述N2-BRIDGE排除；E-ARC2仍OPEN。
下文保留原輪證明、有限控制及停止點。

**最新後續（2026-10-13）**：[一long來源排除](c5_excess_two_n2_one_long_closure.md)
以任意長末端block的原K₅及固定root完整外側接回，關閉完整原55 `(1,0)`。
合既有含U覆蓋，九格八格、完整目標只剩 `(2,0)`；父N2／E-ARC2仍OPEN。
以下舊日期的剩餘表與證據保留當輪語境。

2026-10-12。基準 HEAD `8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`，
包含前輪尚未提交的[接口分割成果](c5_excess_two_n2_partition_rule.md)。
十八份精確工作樹輸入與 SHA 見
[BASE](../audits/2026-10-12-n2-two-contact-unary/BASE.json)。
目前停止點見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。

**完整 N2 原55 的 `(ℓ,u)=(1,1)` 子情形已排除，不限制 long 的大小或接線數。**
新局部引理證：兩接線 unary U 的實際支援為連續三點 `A=(a,b,c)` 時，
任一在 A 上三色互異的 proper 原框列，U 接受每個 owner 色並有完整 lift。
原 U 的任意 block-tree 先由原附件容量化約為五種原形狀；唯一可能拒絕的
六點形含明確原圖 K₅ minor，違平面性。最後使用同一列、同一實際 owner pin 接回。

與既有 `(0,1)`、u=2 排除合成，完整目標 N2 的原55只剩 **u=0**，
H 因而二連通；含 long 的剩餘參數情形為 `(1,0)`、`(2,0)`。
九格仍七格已有覆蓋，因第二 relation 格仍含 `(1,0)`。
一般原55／N2／E-ARC2 保持 **OPEN**。

證據層是任意大小紙面證明＋沿用外部 degree-list 輸入＋独立審查；
固定完整 fibres 作校準，完整 target `not triggered`，没有新 Lean theorem。

## 1. 完整來源與局部引理前提

來源沿用[三列 diagonal §1](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)：
有限簡單 induced-C₅ disk、有序原 B、完整 Σ933／941 或整圖共同 D₅ 像、
T4 全收、每條非框邊 Σ-critical、ε=2、連通 full-B-touch 的有效 H；
恰兩個非相鄰完整 degree5 roots，其餘有效內點完整 degree4；
H−{r,s} 恰兩份原 mixed，其餘 unary，原 pieces one-sided。
共同搬運原整圖後固定 `I={0,1,3}`、`q₀=01212`、`q₁=01202`、`q₃=01021`。
原 contacts／ownership／實際附件／rotation／bridges／旁支／完整 relations、
空 fibres、完整 lifts 與自由孤立座標因子全保留。

局部引理 U2-DIFF-ALL 使用：U 連通且恰接同一 owner 兩次、不接另一 root，
每點完整 degree4；blocks 為 bridges／奇環，多 block 的每 leaf 有私有 contact，
每奇環至多一個普通私有點；每點框附件至多相鄰兩點；actual support 恰為 A；
H 內度二點的框邊附件單射；原 G 平面。
這些是[原55骨架](c5_excess_two_arc_size_bound.md)及既有來源結論。

拒絕 pin 的 degree lists 緊，且由 incident Gallai block palettes 互斥合成，
沿用已採納的 Dvořák 2018 Lemma 7／Theorem 10；本輪沒有新增外部定理。
新五形推導、Diff 出口及原 minor 是本輪紙面證明。

## 2. 任意大小的原五形與 Diff 出口

兩 contacts 使多 block 的 block-cut tree 恰有兩 leaves，contacts 都是兩個
leaf 的私有點，沒有 contact 割點。每個奇環的割點外分支各需不同私有 contact，
加至多一個普通私有點，迫所有奇環都是 triangles。
每個 triangle 的普通私有點、每個 bridge leaf 的 contact 端、每個兩 bridge
之間的普通割點都是 H 內度二點，恰附原框邊。A 中只有 ab、bc 兩條框邊，
附件單射給至多兩個這種原點，完整覆蓋任意長 block chain：

| 原 U | 頂點數 | Diff 列拒絕的障礙 |
| --- | ---: | --- |
| 單 bridge | 2 | 已用 owner 色產生 strict slack；第四色給兩個不同 singleton lists |
| 單 triangle | 3 | 同一 palette 迫兩 contacts 都附同一原框端，actual support 只剩一條邊 |
| triangle 加一 bridge | 4 | 同一原割點的 bridge／triangle palettes 重色 |
| 兩 triangles 共享割點 | 5 | 兩個 cycle palettes 在原割點共同包含第四色 |
| 兩 triangles 由一 bridge 連接 | 6 | 拒絕迫精確原附件，其原圖含 K₅ minor |

這是由任意大小 block tree 得到的原圖窮盡，沒有替換來源或設定搜尋 cutoff。
leaf triangle 只含一個 contact 的情形已保留，不能誤套未用色 D 的特殊計數。
逐形 palette 證明見 [完整紙面稿](../audits/2026-10-12-n2-two-contact-unary/paper/REPORT.md)。

六點形保留原 triangles `p₁z₁w₁`、`p₂z₂w₂`，原 bridge `w₁w₂`，
contacts `p₁,p₂` owned by r。Diff 拒絕迫 owner 色恰為 q(b)，框附件恰為

`p₁→a、z₁→ab、w₁→a、w₂→c、z₂→bc、p₂→c`。

原 K₅ 的五 bags 是
`{a}、{p₁}、{z₁}、{w₁}、{b,r,p₂,z₂,w₂}`。
前四形成原 K₄；第五以第二 triangle、rp₂、bz₂ 連通，四條 cross edges
是 ab、p₁r、z₁b、w₁w₂。所有十對鄰接都是原邊，因此違平面性。
minor 只否定原平面來源，不要求收縮後保 Σ。

故任一 proper q，只要 `q(a),q(b),q(c)` 互異，便有 **`F_U(q)=∅`**。
局部定理允許 q 在 A 外使用第四色。

## 3. 同列來源接回與精確 closure

[接口報告 §6](c5_excess_two_n2_partition_rule.md#6-已用色禁色規律與原七模板的統一排除)
已由共同容量與三列出口排除 k_U=3；完整 `(1,1)` 因此有 k_U=2 及三點弧 A。
每個原三點弧在 I 均有 Diff 列：012／401 可取 q₀，123 可取 q₁，
234 可取 q₃，340 可取 q₀。

固定其中一份原拒絕列 qᵢ。原 `G−U` 已全收，取其一份完整外部染色 ψ。
新引理對這份染色的實際 owner 色 ψ(r) 給 U 的完整 tuple。
按原頂點順序接回；全部交界都仍是原 B／owner，相同 pins 覆蓋全部原邊，
得到原 G 的完整 lift，違原拒絕。這亦與同列容量要求 `|F_U(q_i)|=1` 矛盾。
沒有拼接不同列，沒有獨立正規化框，沒有假設 long 的高接點 diagonal escape。

**Closure scope：** 完整上述來源契約下的原55 `(1,1)`；
加既有含 U 覆蓋後，完整目標原55必 u=0、H 二連通。
**Remaining OPEN：** `(1,0)`、`(2,0)` 的同列完整 joint／來源矛盾，
N1／相鄰／單-root例外、契約外 N2、一般 E-ARC2、一般出口及 `K∞=K≤5`。
九格仍七格；沒有新增 Δ 門檻或來源大小下界。

## 4. 獨立審查、完整控制與重播

[獨立審查](../audits/2026-10-12-n2-two-contact-unary/review/REPORT.md)
逐量詞核對任意 block 長度、私有／割點 contacts、palette 分支、原 minor
及同列全圖接回。[另一份重建](../audits/2026-10-12-n2-two-contact-unary/joint/REPORT.md)
保存內部 bridge 可與 owner 同色的更正，避免把非平面 barbell 誤判為局部全接。

[checker](../audits/2026-10-12-n2-two-contact-unary/controls/checker.py)
對五形的 1,050 份具名附件配置，獨立以原邊 DFS 和全 tuple 篩選核對
42,000 owner cells，保留十列全部 168,000 ambient ordered pins cells、
3,880 空 cells 及 2,119,000 完整 tuples。
[證書](../audits/2026-10-12-n2-two-contact-unary/controls/observations.json.gz)
以確定性 gzip 保存全部原 relations，解壓為 35,291,724 bytes。
唯一十份可拒絕 Diff 的控制恰是兩種方向乘五原弧的非平面 barbell；
其五 bags 的連通性、互斥與十條原 cross/clique witnesses 均重算。

1,040 份局部出口控制 `triggered and holds`；十份 barbell 是撤去平面前提的
`counterexample`，並有原 K₅；完整 N2 target **`not triggered`**。
有限附件校準不承擔無界分類或來源排除，沒有整圖來源枚舉。

```bash
python3 -B audits/2026-10-12-n2-two-contact-unary/controls/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-n2-two-contact-unary/controls/checker.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

實際檢查與刪去一份完整 lift 的負控制見
[verification](../audits/2026-10-12-n2-two-contact-unary/verification.json)。
沿用前輪容量／N45／44／SD-A 的採納信任鏈，未重跑全部上游證書或 ES／ER 搜尋。
既有 Lean build 不形式化這份新紙面證明。沒有 commit 或 push。
