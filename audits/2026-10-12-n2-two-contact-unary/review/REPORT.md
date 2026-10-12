# 兩接線 unary 全 owner Diff 出口的獨立紙面審查

2026-10-12。封存權威為 [BASE](../BASE.json) 的十八份逐份 SHA 輸入，基準
HEAD `8b76dcc82adabba679e7b0d2ef6dbe6eb9cc37f3`。本作者只寫這份新報告；
没有改共享文件、凍結輸入、舊證書或 remote。本次先自行重建原 block 計數與
palettes，再讀 [作者 paper](../paper/REPORT.md)、[另份 joint 推導](../joint/REPORT.md)
及 [固定控制程式](../controls/checker.py)。

**裁決：在明列的完整原來源契約及已採納信任鏈內，採納 U2-DIFF-ALL，並採納
完整原55 `(ℓ,u)=(1,1)` 子域排除。** 原55的 `(1,0)`、`(2,0)`，完整 N2、
E-ARC2 及契約外例外仍 OPEN。任意大小結論由紙面證明承擔；有限校準沒有觸發
完整 target，不承擔來源全排。沒有新增外部定理或 Lean theorem。

## 1. 核對的原圖契約與信任鏈

完整来源沿用凍結 `c5_excess_two_n2_diagonal_three_row.md` §1：同一有限簡單
induced-C₅ disk、有序 B、完整 Σ933／941 或整圖共同 D₅ 像、T4 全收、全部
非框邊 Σ-critical、ε=2、有效 H 連通且 full B-touch、非相鄰原 degree5
roots r,s；其餘有效內點完整 degree4；恰兩份原 mixed，其餘 unary，pieces
one-sided。原 ordered/shared contacts、owner、attachments、rotation、bridges、
旁支、完整 relations、空 fibres 及原完整 tuples 均保留。

本次新局部證明只使用作者 paper §1 的五項來源前提：原 U 連通、恰兩條
owner incidences、每點完整 degree4；blocks 是 bridges／奇環、每 leaf block
有私有 contact、每奇環至多一個普通私有點；actual support 恰為三點弧
`A=(a,b,c)`；每點框附件至多相鄰兩點；原 H 內度二的框邊附件單射；原 G
平面。五形分類與 minor 都沒有假設尚未證明的 E-ARC2。

凍結 partition report §6 的推論 U3 提供完整 `(1,1)` 的 `k_U=2`；盾弧
結論提供 `S_U=A`。不可染 degree assignment 的 tightness 及 block palettes
互斥聯集，沿用已採納 Dvořák 2018 Lemma 7／Theorem 10 信任鏈。本次没有
重作全部上游證明，也沒有把五形分類或原 K₅ minor 歸稱外部定理原文。

## 2. 任意大小五形分類：接點與原 cutpoints 無遺漏

Simple unary 恰兩條 owner incidences，故是兩個不同原 contact。Singleton
至多一 owner 邊及兩框邊，完整 degree 不足四。

對任一原奇環 K，每個 K 上的 U 割點都可在一個環外分支取到 leaf 私有
contact；各分支互斥，所取 contacts 與 K 的私有 contacts 亦互斥。至多一個
普通私有點給 `|K|≤1+k_U=3`，所以所有原奇環恰為 triangles。

多 block 的 block-cut tree 至少兩 leaves，每 leaf 都要不同私有 contact。
兩 contacts 因此恰在兩個 terminal blocks 的私有點；所有 cutpoints 和
interior blocks 都沒有 contact。有限 tree 恰兩 leaves 是 path。這一步
明確排除 contact 在 cutpoint 的可能，不從色列或有限圖樣假定它不存在。
每個 terminal triangle 的兩私有點恰為一 contact、一普通點；interior
triangle 恰有兩割點及一普通私有點。單 triangle 另有兩 contacts、一普通點。

每個 triangle 的普通私有點是 H 內度二；每個 leaf bridge 的 contact 端是
H 內度二；每個 bridge–bridge 普通割點亦是 H 內度二。它們的原框附件
恰為一條框邊，且只能是 `ab` 或 `bc`。附件單射給總數至多二。

因此：無 triangle 的 chain 全部點都是 H 內度二，只能是單 bridge；一個
triangle 若在內部，加兩個 leaf bridge contacts 已超容量，故只能是單
triangle 或 triangle 加一條末端 bridge；兩個 triangles 已用完容量，
不能有 bridge leaf 或 bridge–bridge 割點，故只能共享割點或由單 bridge
連接。三個以上 triangles 本身即超容量。這五形窮盡任意 block-chain 長度，
沒有搜尋大小界、原圖縮短或 relation 替換。

特別核對：本次是全部 owner pins，leaf triangle 可以只有一個 contact。
未用色 pin 拒絕時的較強 leaf 計數不能移用到這裡；作者保留了這個分支。

## 3. 同一 Diff 列的完整 palette 核對

固定同一原 q，令 `x=q(a),y=q(b),z=q(c)` 互異，D 是未在 A 上使用的第四色。
q 在 A 外可用 D；局部 argument 只讀 actual support。對任一 owner 色 d，
若原完整 U fibre 空，則所有 degree lists tight，原橋／triangle palettes
大小分別一／二，且在同一原割點上互斥。

普通 triangle 點若附原框邊 e，cycle palette 恰是 `[4]∖q(e)`。
同環私有 contact 的唯一框附件 h 使 `{d,q(h)}=q(e)`。這是從原 degree 和
空完整 fibre 推出的集合相等，沒有把原附件換成色數 marginals。

五形逐一核對如下：

1. 單 bridge 的兩附件邊不同，恰為 `ab,bc`。d 在支援已用色中時，某端有
   root／框外鄰同色的 strict slack，故全部 U 可染；d=D 時兩 singleton
   lists 恰 `{z}`、`{x}`，直接可染。
2. 單 triangle 的兩 contacts 都必附到其普通點附件邊 e 的同一原端點：
   Diff 在具名 A 上單射，使兩 contact 的相同所需框色確定同一原點。
   全支援遂包含於 e，違 actual support 恰三點。
3. Triangle 加 bridge 的兩 H 內度二附件 e,f 不同，恰 `ab,bc`。按 e=ab
   的方向記名，triangle contact 迫 d∈{x,y}，bridge leaf tight 迫
   d∉{y,z}，所以 d=x、bridge palette={D}。Cycle palette={z,D}，在原
   割點與 bridge 共 D，違互斥。反方向完全相同。
4. 共享割點的兩 triangle palettes 恰 `{z,D}`、`{x,D}`，在同一原割點
   重複 D，不可能互斥，與 owner pin 無關。
5. 單 bridge 連接的兩 triangles 是唯一保留的**局部**拒絕形：兩 contacts
   迫 d∈q(ab)∩q(bc)={y}；bridge palette 亦只能是 {y}。所以 d 和
   bridge 色可以相同，因為 bridge 端點沒有 root 邊。兩 contacts 及兩
   bridge 端點的實際附件由 Diff 單射各自迫到原 a 或 c，恰是作者 paper
   §3.5 的六點 attachment table。這一形不能僅靠局部 degree-list 前提排。

本作者自行重建時也先找到了第五形的精確局部拒絕：它在所有 proper 弧列
恰禁止 owner 取 `q(b)`，包括 Eq 和 Diff。根作者及 unary 作者隨後提供其
K₅ bags 建議；本次獨立核對全部 bags 和原邊。對這個結構的採納不是聲稱
局部 F 空，而是下節直接否定它的原平面來源。

## 4. 精確原 K₅：所有 bags 互斥、連通及十對鄰接

保留作者 paper 的原 labels：triangles `p₁z₁w₁`、`p₂z₂w₂`，bridge
`w₁w₂`，owner contacts `p₁,p₂`。被 Diff 拒絕所迫原附件為

`p₁→a, z₁→ab, w₁→a; w₂→c, z₂→bc, p₂→c`。

取五個原 bags：`{a}`、`{p₁}`、`{z₁}`、`{w₁}`、
`X={b,r,p₂,z₂,w₂}`。前四個 singleton 的六對鄰接是原 triangle 的三條
邊及 a 到這三點的三條原附件。X 由第二 triangle、原 `rp₂`、原 `bz₂`
連通；與前四 bags 互斥。其四條 cross edges 分別是

`ab, p₁r, z₁b, w₁w₂`。

十對全有原鄰接，全部 bags 非空且連通，因此這就是原 G 的 K₅ minor，
違原 disk 平面性。反方向只換同一原圖中哪個 triangular leaf 作第一側，
不重新標準化原框、不變動 owner、不增加新接口邊。Minor 只否定原 G
平面，不聲稱收縮後保存 Σ 或完整 relations。

於是第五形也不能在原平面來源拒絕，採納

`q|A 三色互異 ⇒ F_U(q)=∅`，對每一個 owner pin 都有全部原 U 的完整 lift。

## 5. 完整 `(1,1)` 的同列、同實際 pin 接回

未變的指定三列 `q₀=01212,q₁=01202,q₃=01021` 在五個原三點弧
`012,123,234,340,401` 的 Diff sets 分別是
`{0,1},{1,3},{3},{0,3},{0,1}`，均非空。

故對同一原 A 選一個原指定 Diff 列 qᵢ。在同一原 U，U2-DIFF-ALL 給
`F_U(q_i)=∅`，直接違凍結推論 UL 的同列 singleton 禁色。亦可只用採納的
`k_U=2` 與三點支援結論，將最後一步完整接回原圖：

完整來源的原非框邊全刪釋放／分量刪除全收給 `G−U` 在這份同一 qᵢ
有完整外部染色 ψ。保留 ψ 的原框、兩 roots、所有原 spokes、其餘 pieces
及它的 actual owner 色 d=ψ(r)。本定理在這個實際 d 給 U 的完整 tuple。
U 所有外鄰恰在原 B 和 owner r，故接口值逐具名點一致；按原頂點順序
拼回後覆盖原 G 全部邊，所有自由孤立座標的原四色因子亦保留。

這是一份同列、同 pin 的完整 G lift，違原 qᵢ 拒絕。没有把 U 的某列出口
與 long 的另一列出口相乘，也没有把分別正規化的 components 當共同框列。
高接點 long 即使原 diagonal mask 是 I，亦由這份原 `G−U` 染色保留其完整
lift；最後接回沒有使用一般 long diagonal 或 off-diagonal 出口定理。

因此採納完整原55 `(ℓ,u)=(1,1)` 來源排除，無須限制 long 接線或頂點數。
這是該參數子域的 closure，不能升格為整個原55、N2 或 E-ARC2 closure。

## 6. 固定 checker 語義與證據邊界

本次逐函式審讀 `controls/checker.py`，核對以下語義；实际重播由根作者
本 audit receipt 記錄，本報告没有另外把未執行的重播列為通過：

- 固定五個導出的原 skeleton，逐具名 arc 保存實際附件及 root ownership；
  所有 U 頂點完整 degree 四，兩框邊附件單射與支援等於 arc 都實際檢查。
  這是導出小骨架的附件校準，沒有枚舉完整 N2 target。
- Numeric-order DFS 的每個完整 U tuple 與獨立「先枚舉全部 internally proper
  tuples，再按實際框附件和 owner contacts filter」結果逐 tuple 比較。
  所有十列、四 owner pins 都保留；ambient 非 owner pin 的四等值副本亦完整
  保存為 ordered16 cells，包括空 fibres。
- Barbell 的兩種實際附件方向均要求精確 table，再用原 edges 驗 bags 互斥、
  induced connectivity 和全部十對 cross edges。Reverse 情況交換原 leaf
  vertices 作第一側，字面框與 root IDs 不動，與本次紙面 minor 一致。
- `authority()` 對 BASE 明列十八個 frozen inputs 實際驗 bytes 與 SHA。
  產物保存 raw BASE SHA；`--check` 重算完整 JSON，使用 `mtime=0` 的
  deterministic gzip 並逐 byte 比較，故原 manifest 與封存 inputs 的 drift
  不能保持既有產物相同。這個 check 的 authority 是 frozen inputs，而非
  聲稱共享工作樹文件從未更新。
- 十份非平面 barbell 保存為撤掉 planarity 的 local `counterexample`，其
  K₅ negative 全部有具體原邊證書；對包含 planarity 的新 theorem 不是
  反例。其他 attachment controls 是局部 `triggered and holds`。全部
  `full_source_status` 保持 `not triggered`，`source_inputs_verified=0`。

有限控制可以核附件 forcing、完整 fibres 與 minor，但不能證任意 block tree
五形分類；該分類已由第2節紙面計數承擔。零完整來源觸發不是來源有限排除。
本次新紙面結果未在 Lean 形式化；任何既有 `lake build` 只能核既有專案。

保留原55 `(1,0)`、`(2,0)`、完整 N2、N1／相鄰／單-root 例外、E-ARC2、
一般出口及 `K∞=K≤5` OPEN。没有新增來源搜尋、外部 theorem、Lean theorem、
commit、push 或 merge/release authority。

## 7. Canonical 接回的最終範圍核對

另讀 canonical `docs/c5_excess_two_n2_unary_diff_closure.md` 與本 audit 根
REPORT，確認新推論「完整目標原55 必 u=0、H 二連通」有效。依凍結殘餘
報告 §1 的 relation 分類，含 U 的可能參數只有 `(0,1)`、`(0,2)`、
`(1,1)`：盾弧預算已排 `u=1,ℓ=2`（兩 long 各需至少兩邊，U 亦需至少兩邊，
合計超過原框五邊），u≤2 由原 H skeleton；u=2 的兩 mixed 已迫 short。
既有 `(0,1)` 與 u=2 排除，加本次 `(1,1)` 排除，遂無原 unary。採納的原 H
骨架是含 r,s 的中央二連通 block 加 owner-root 葉 blocks，unary 與這些葉
blocks 一一對應；u=0 遂使 H 只剩該中央 block。因此二連通結論只作用於
明列完整來源的有效原 H，沒有套到自由孤立座標或契約外 N2。

九格計數仍為七格：新結果排第二 relation 族的 u=1 子情形，但第二格原55
仍有 `(1,0)`；第一格原55 仍有 `(2,0)`。沒有因一個參數子情形 closure
把整個第二 relation 格算成 CLOSED。Canonical 與根 REPORT 的父問題 OPEN
邊界一致，沒有新增 Δ 門檻或來源下界。

只讀已保存 gzip 證書的 counts 與 bytes 核對 canonical 數字：1,050 份
附件、42,000 owner cells、168,000 ambient cells、3,880 空 cells、
2,119,000 完整 tuples、1,040 局部出口控制、十份非平面 barbell；gzip
1,088,012 bytes、解壓 35,291,724 bytes，全部相符。本核對沒有重跑 checker，
沒有新增來源觸發，也沒有更改 canonical、共享文件或舊輸入。
