# N45-L1R：LOW1 原圖、完整關係與三接點映射獨立稽核

2026-10-10。BASE／實讀 HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本輪只新增此目錄；未讀本輪其他 reviewer 的裁決，未改共享、worker 或其他 audit。
凍結來源、current-work pins 與 BASE Git objects 分開列於 [inputs](inputs.json)。

**裁決：六項 LOW1 claim 均接受為明列完整契約內的任意大小條件紙面排除。**
沒有發現需要添加的新前提。這是獨立稽核裁決，由監督決定正式採納及文件傳播；
本輪不代替外部 Gallai 定理或 BASE 紙面證明，也不聲稱新 Lean。
精確量詞、逐 claim 的十二項完整前提與獨立論證見 [judgment](independent-judgment.json)。

## 1. 接受範圍與來源身份

任意大小有限簡單 induced-C5 disk 原 G，完整 Σ933／941 及其共同整圖 D5 像，
每非框邊 Σ-critical、ε2、原有效 H 連通且 full B-touch；兩個非相鄰原 degree5 roots，
其餘有效原內點完整 degree4。`H−{r,s}` 恰完整原 unary U 與 mixed P,Q；三份原 pieces
皆 one-sided 且 actual support 非空，兩 mixed 各支援一條原真框邊的兩端並各接兩 roots。
LOW1 指 U 在 r、有唯一原 rx，mixed incidence `(m_r,m_s)=(2,3)`，原兩 roots 各兩 spokes。
唯一刪邊 `e=rb_i`，`X=G−e=M` 為原拒絕 literal β 的 inclusion-minimal45／54 core。

接受時保留全部 U/P/Q 頂點、原內邊、contacts、附件、spokes（除 e），原 shared vertex
單一坐標、ordered contacts、support／ownership／bridges／rotation，以及一個共同色框、
全部十列、全部 pins、空及非空 fibres、全部 full lifts。933 的 q2 在量詞內。
D5／S4／root swap 都共同作用整圖與全部資料。既有忽略的原孤立點只加自由 lift 因子。

LOW incidence2、HIGH、long、原55、其他 cores、非unit／非minimal省略、一般 N2／E及 ε≥3
保持 OPEN。本裁決沒有把可搬用的 BASE theorem 自動升格成其他身份的排除。

## 2. 原邊、degree 與 full-assignment join

e 連 r 與 B，故 `H_X=H_G`，沒有刪 U 或 root-contact。r 由原三 contacts＋兩 spokes
降為三 contacts＋一 spoke，完整 degree4；s 的三 mixed contacts＋兩 spokes完整保留，
degree5。U/P/Q 各点完整 degree4。X 的 β-minimality來自 `X=M` 本身；沒有從父 G 遺傳。

移除 s 後，U/P/Q 各由原 r-contact 接到 r，故唯一实际分量恰
`C=X[{r}∪V(U)∪V(P)∪V(Q)]`。degree4 是 **X 中完整 degree**，不是 `deg_C=4`。
s 的三 contacts繼承原 rotation 次序；简单性給互異鄰點。若其中某點也接 r，兩條約束作用
同一個原變數，不能拆成 r-port 和 s-port。

每份原 Λ_U／Λ_P／Λ_Q 都保存全部內點 assignments、全部內邊、actual boundary attachments。
把它們與 r 的实际 boundary list 沿 **同一 r 坐標** natural join，加入全部原 r-contact不等式，
恰得到 C 的全部 assignments：完整染色的 restriction 與 join 的拼接互為逆。
再共同加入三個 s-contact不等式及 s 的实际 spoke list，恰給 X 的全部 lifts；
G 的 lifts 另加唯一原条件 `r≠β(b_i)`。原图與 derivative 的 lifts沒有混用。
投影到 ordered contacts 時，每個 tuple 保其全部 fibre；F 只用于共同避色查詢，不能复原 R。

對每個 proper literal γ，`|L_γ(v)|≥deg_C(v)`，s-contact 在未 pin s 前有 strict slack。
C connected，因此有完整未 pin 的 C coloring。这个结论逐十列、root pins及其全部 fibres成立。

## 3. 精確 F 與任意大小 K5 抽取

若 s 的兩条原保留 spokes在 β 同色，删其中任一条不会改变任何 list，違反 X 自己的
β-minimality。因此二者字面色 u,v 異色，s 可用色恰 `Col−{u,v}`。X 拒绝 β 迫这些可用色
都在 F_C。删 u-spoke 後的完整 lift 必把 s 染 u，否則已可延拓 X；限制到未改动 C 得到
共同避 u 的完整 witness。v 同理。故 `F_C(β)=Col−{u,v}` 精確成立，而且 R_C 非空。

BASE `c5_two_spoke_three_contacts.md` §1–5 的每個充分前提都在同一 X 中成立：
唯一完整 degree5 s，其他点完整 degree4，sole C，三個互異原 contacts，兩條异色 spokes，
非空完整 R_C 与精確 F。§5 允许任意兩個異色 spoke 位置；不需要相鄰、不要求 X full B-touch、
第二拒絕列或 T4，也不要求 β singleton 位於 U 盾弧中點。

獨立核 [Dvořák 官方講義 Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
連通 degree-list 不可染時所有 lists tight，且不可染 degree assignment由同一 Gallai tree 的
blockwise-uniform palettes 刻畫。其本文与 local PDF 分别已读，外部来源记录見
[external source](external-source.json)。该外部定理没有在本轮 Python 或 Lean 中证明。

兩份 pin complementary colors 的 tight lists只在原三 contacts不同。Leaf-block私有頂點给
block-incidence columns線性獨立；active blocks只交換这两个颜色。三 contacts active-degree1，
其他 vertices active-degree0或2；active incidence forest恰三葉，故是一个 active triangle
加三條任意長 bridge arms，允許零長。原接點、shared cut vertices及 inactive branches均保留。

每個 triangle點两條 triangle邊及一條 arm首邊（零長時是原 s-contact）後，X 中完整degree4
只余一條原邊。它直接接 B 或進入不重接 active structure 的 inactive branch。
若 branch 不碰 X 的 actual B，刪 branch 使 connected remainder在接入口 strict slack，
可染；branch無 B／s constraints，入口內度3，可由四色 slack填入，并共同換其完整 colouring
使 bridge兩端异色，反而延拓拒絕 pin。因此三條实际 boundary tethers必存在，內部互斥。

原 bags `Z={s}`、三份 `V_i=triangle vertex+完整arm`、`O=原整個B+tether內點` 均連通互斥。
三 triangle邊、三原 s-contact邊、三实际 tether及一條**保留的**s-spoke給全部十對 bags鄰接，
得到 X 的 K5 minor。零長 arm保原 contact邊；省略 e 未用于任何邻接。B 只作为最后minor的
connected bag，没有成为保存 colouring relation 的 replacement。與 X 的原 disk embedding矛盾。

## 4. 獨立有限校準與證據界線

[checker](checker.py) 不 import worker checker、certificate 或裁決作決策。
[certificate](certificate.json) 是独立小型抽象 graph/relation校準：具名 `r,u,p,q,t,s`，
U 完整保留，共同 r，shared contact p，非自然順序的 s-contacts `(q,p,t)`。
直接枚举全 C／X assignments，分别与完整 local natural join、全部共同 pin query比對；
G另保原额外 r-spoke inequality。

- 全十個 canonical proper rows，含三色 singleton2列；160個完整 root-pin fibres。
- 每列全部64個 ordered contact tuples，共640 fibres，空 fibre也保存。
- 240次共同 S4 色搬運、100次完整 D5 boundary／attachment 搬運。
- 删除原 U contact 的錯誤 join在全部十列被发现；marginal product與split shared p均產生可识别的假 witness。
- 另刪 certificate 中一個完整 fibre，实际 verifier须 exit2，并给出 certificate bytes mismatch。

这些仅是 relation语義 **triggered and holds** 校準。LOW1 source前提 **not triggered**：
toy有 degree2／3顶点，未證 disk rotation、完整Σ933／941、Σ-criticality、拒绝 β-minimality
或 one-sided真框邊 supports。未執行 LOW1 来源搜索，没有新 source realization、source counterexample
或目标 trigger數。任意大小紙面結論来自 §1–3及明列依賴，不来自有限校準。

## 5. 只讀重播、封存與既存 FAIL

实际 stdout／stderr与exit列於 [checks](checks.json)；normal與seed17須 byte相同。
入口核21份凍結 inputs、四份 BASE Git objects、immutable worker／舊audit inputs。
authority的pre-adoption版本保在 frozen；允许監督後續已授權的共享 adoption／routing更新，
不要求历史worker的live pre-existing inventory在新增独立audit後仍相同。

```bash
python3 -B audits/2026-10-10-n45-l1r/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-l1r/checker.py --check
python3 -B audits/2026-10-10-n45-l1r/checker.py --check --manifest audits/2026-10-10-n45-l1r/MANIFEST.final-v2.sha256
```

[最終 MANIFEST v2](MANIFEST.final-v2.sha256) 凍結全部regular payload；只排除本頂層 final-v2 manifest、delivery及頂層seal-final-v2。
[delivery](delivery.json)另绑定manifest及封存实跑metadata；排除规则不作用到 frozen中的同名巢狀檔案。
没有symlinks、没有整份scratch clone。只新增exclusive audit；未 commit／push／PR／再委派。

首輪自封 generator 誤用 basename 排除規則，漏列 frozen worker 的巢狀delivery，被只讀checker正確
exit2拒絕inventory mismatch；原 [失敗manifest](MANIFEST.sha256)、seal-checks logs及
[finding／原checker](failed-seal-v1/finding.json)完整保留且列入final-v2 payload。
這是封存 generator 的錯誤，沒有數學或input drift；最终generator使用完整relative path排除。

保留历史 E4 provenance FAIL、fresh BASE兩历史缺檔及全worktree DocGraph duplicate-ID FAIL。
本relation稽核不重跑这些既存失败，也不把它们并入paper否决或全部工具PASS。
根监督转告的非阻擋工具finding：worker checks.json 的 postseal_actual_results仍是v1索引；
最后成功入口以delivery明绑的final-v4 metadata为准。本轮不改原檔、不重跑worker strict inventory。

接纳仅限完整 LOW1；LOW incidence2、HIGH、long及一般 N2／E仍 OPEN；无新 Lean。
