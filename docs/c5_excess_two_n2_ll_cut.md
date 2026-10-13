---
docgraph:
  id: c5.excess-two-n2-ll-cut
  family: [c5, c5.excess-two, c5.n2]
  requires:
    - c5.excess-two-n2-diagonal-three-row
  derives_from:
    - c5.excess-two-n2-double-long-joint
---
# N2 原55雙 long：基本 LL-CUT 介面與加強版來源排除

**後續（2026-10-13，N2-BRIDGE）**：[前提橋接與932來源排除](c5_excess_two_n2_bridge.md)
已逐項補足原E4完整三列來源契約，該域N2全排；E-ARC2仍剩N1及相鄰roots來源。
本頁完整Σ契約及歷史正文保留，新移植證明由上述入口承擔；無新Lean theorem。

2026-10-13；凍結 BASE `3097ef5be241b7777451a5ef8a663f3987d6b866`。
[完整契約與前提核對](../audits/2026-10-13-n2-ll-cut-3097ef5/CONTRACT.md)、
[本輪報告](../audits/2026-10-13-n2-ll-cut-3097ef5/REPORT.md)及
[任意大小完整證明](../audits/2026-10-13-n2-ll-cut-3097ef5/paper/TOPOLOGY.md)
保存原來源、共同色框、各原 bags 與有限介面證書。
目前入口見 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)。
後續發布核對與原證據保存見[整理紀錄](history/2026-10-13-c8-w5-n2-publish.md)；
下文「未commit／push」保留本地研究完成截點。

**本輪採納 LL-CUT+diag，排除完整原55 `(ℓ,u)=(2,0)` 的全部剩餘來源。**
原 K₅／K₃,₃ leaf 引理配合同來源接線容量，覆蓋 `(t_r,t_s)=(2,0)、(1,1)、(2,1)`；
既有 t=0／1 排除保持原證明。本輪沒有證成基本 S 必触發 cut 的獨立機制。
基本介面仍有19,229份共同可行投影，不能稱為來源實現或 LL-CUT 反例。

合既有含U及一long排除，**指定完整契約內的九格已有全部覆蓋**。
LL-CUT當輪未涵蓋只指定三列的較廣 N2；原E4完整三列來源契約已由上述N2-BRIDGE後續排除。
N1、相鄰／允許的單-root core例外、契約外原55及E-ARC2仍不由本頁排除。
有限完整目標仍 **not triggered**；一般來源排除由紙面證明承擔。
沒有新增 Lean theorem；本輪只作本地研究，未 commit／push／發布。

## 1. 同一原來源與基本介面

沿用[原55完整契約](c5_excess_two_n2_diagonal_three_row.md#1-完整來源契約)：
有限簡單 planar disk、有序 induced `B=(b0,…,b4)`、完整 Σ933／941 或整圖共同
D₅像、T4全收、每條非框邊Σ-critical、ε=2、連通且full B-touch的有效H；
恰兩個非相鄰原完整degree5 roots r,s，其餘有效內點原完整degree4。
`H−{r,s}` 恰為两份原long mixed P,Q，沒有unary；H二連通、pieces one-sided。
原頂點、原邊、ordered/shared contacts、owners、actual attachments、rotation、
bridges、旁支、完整relations、空fibres、full lifts及自由座標乘積因子全部保留。
不借用最小內點／最大邊數來源的 degree≥5、h≥3、W5 前提。

固定同一字面框 `I={0,1,3}`，`q0=01212,q1=01202,q3=01021,D=3`。
`t=t_r+t_s` 是原root-spokes總數；shared contact 的兩條root邊分別計入incidences。

基本 `S_C(i)` **恰為**原contact／框碰色行列，加有shared contact時的diagonal；
定義與矩陣方向沿用[共同容量定理](c5_excess_two_n2_double_long_joint.md#4-剩餘域與可反駁的-ll-cut)：

```
M=0 on S_P; M=1 on S_Q;
k_P^s−1 ≤ 每行和 ≤ k_P^s;
k_P^r−1 ≤ 每列和 ≤ k_P^r.
```

若三列都避開基本cuts，對原附件必有

```
k_C^other≥2 ⇒ W_C^v⊆Z(T_v),
Z(T)={h: 每個i都有q_i(h)∈q_i(T)}.
```

原因是 P 的整行接受迫整行零，若 `k_P^s≥2` 就違反行下界；Q 用互補上界同理。
此處逐列取同一原附件，故只能有一份共同 Z：
空集／單點不擴大；`Z(12)=124,Z(40)=024`；其餘相鄰pair不擴大。
在兩份三點支援中，雙spoke恰為唯一未用框邊e，
`Z(e)∩S_C` 沒有相鄰框點。此結論含全部五個字面位置，沒有逐列旋轉。

## 2. 兩條保留另一 long 的原 minor

取原 C 的 leaf 奇環上相鄰私有、非shared contacts p,z；單cycle時取相鄰頂點。
令 `C0=C−{p,z}`，仍非空連通，p,z各有另一原cycle邊接C0。
它們各恰有一個實際框鄰居。另一原long記C′。

**K₅-H。** 若p,z都附h，令 `R={r,s}∪C′`；取
`a∈S_C′−{h}`、`b∈S_C−{a,h}`。兩份long保證存在，C到b的附件仍在C0。
原框a–h兩弧中，A避b、A′含b。五袋為

```
{p}, {z}, {h}, R∪(V(A)−{h}), C0∪(V(A′)−{a,h}).
```

後兩袋分別由原C′–a、C0–b接通。十對跨邊是pz、ph、zh、兩條原root邊、
兩條剩餘cycle邊、兩弧在h的末邊及A′在a的首邊。故原G非平面。
這個引理不需h有spoke，也不需p,z有相同owner。

**K₃,₃-O。** 若p屬r、z屬s且 `k_C^s≥2`，取

```
left:  {p}, {s}, B
right: {r}∪C′, {z}, C0.
```

每袋互斥連通；九條原跨邊逐行為

| 左袋 | 到 `{r}∪C′` | 到 `{z}` | 到C0 |
| --- | --- | --- | --- |
| p | pr | pz | 另一cycle邊 |
| s | s–C′ contact | sz | 尚餘s–C contact |
| B | C′的實際附件 | z的實際附件 | C0的實際附件 |

最後一條因C有至少三個support點、p,z合共只移走至多兩點附件而存在。
另一s-contact因p非shared及 `k_C^s≥2` 而保留。若r側至少二則整體交換方向。
全程沒有把強迫同色／異色當成原邊。

## 3. 明列新增的 diagonal 資訊

若原完整 `F_C(q_i;D,D)` 空，shared slack先排shared。
由原degree lists與Gallai刻畫，leaf奇環私有點同有該block的palette。
私有contact的list不含D，普通私有點的list含D；已有leaf私有contact，
故失敗時該奇環全部私有點必為contacts，每點恰有一個框附件。
leaf bridge端點則有一個owner與兩個相鄰框附件。

若C三列diagonal皆拒，奇環私有點的附件在三列都同色；五個原框點的
signatures互異，迫它們其實都附同一h，K₅-H排除。
因此**永久diagonal失敗的long只有bridge leaves**；sole cycle亦排除。

這些是完整fibres的紙面接受資訊，另定義

```
S_C^diag(i)=S_C(i) ∪ {(D,D): 原完整F_C(q_i;D,D)非空}.
```

本節沒有變更基本S。新接受格有上述原lists／minors證明，
沒有從未報告的完整染色枚舉偷加。

## 4. 三個剩餘域的窮盡

**spokes (1,1)。** 某C兩側接線都≥2時，§1迫兩側W各含於各自單點spoke。
失敗diagonal不可能有bridge leaf；cycle leaf的相鄰私有contacts若同owner，
同附h而觸發K₅-H；若不同owner，觸發K₃,₃-O。sole blocks同樣涵蓋。
故這種C三列diagonal全部接受。
兩root各有總incidences四。若沒有這種C，只能交錯拆成 `(1,3)/(3,1)`，
基本矩陣總量已矛盾：`3(3−1)=6>3·1=3`。
否則兩份都全接diagonal，或另一份k≤3；後者以已採納低接點出口接同一列。
這同時覆蓋支援 `{3,3}` 與 `{3,4}`。

**spokes (2,1)。** 整體命名 `k_P^r=1,k_Q^r=2`。
若 `k_P^s=3`，基本總量cut為 `2(3−1)=4>3·1=3`。
否則Q兩側≥2、P總k≤3。Q的r側W是獨立集、s側W至多單點，故沒有bridge leaf。
失敗diagonal的cycle私有path不能換owner（K₃,₃-O）；也不能屬s（K₅-H）。
每個leaf至少耗兩r-incidences，至少兩leaves卻需四條，違Q只有兩條。
sole cycle若全部同owner則違mixed。故Q三列全部接受，再接P的低接點出口。

**spokes (2,0)。** 同樣命名r側為1、2。
若 `k_P^s=4`，基本總量cut為 `2(4−1)=6>4·1=4`。
否則Q兩側≥2，其s側W空、r側W獨立；同樣排bridge leaves，
cycle leaves全須r-owned，兩leaves耗四條r邊也矛盾，sole cycle違mixed。
故Q三列全部接受。若P總k≤3，直接同列接回。
唯一餘下 `P=(1,3),Q=(2,2)`：若P沒有出口，§3使其至少有兩個bridge leaves。
P的r側W仍獨立，兩leaf必屬s；原H度二附件單射迫它們用掉P三點支援的兩條框邊。
因此 `W_P^s=S_P`。取該支援見齊三色的指定列，s無spoke，矩陣每行有三個
原附件迫出的零，僅餘一格；卻要求行和至少 `k_P^s−1=2`，即 **`2≤行和≤1`**。

所有最終接回都在一個q_i、同一pins `(D,D)`，取兩份原完整lifts。
D避全部原spokes、原rs不存在，兩份piece之間無原邊；合併後滿足全部原邊。
完整Σ仍是來源契約，沒有把它弱化成任意三列拒絕。

## 5. 有限介面、採納範圍與重播

[介面覆蓋](../audits/2026-10-13-n2-ll-cut-3097ef5/profiles/REPORT.md)
由原盾弧／spokes映射到85份字面幾何，再保存兩側incidences、原contact owners、
shared身份與實際B附件；三列從同一筆資料求值。
基本篩選後保留19,229份投影、3,764份局部contact介面成員，
其相容乘積為64,408份。內邊、rotation、block身份保留在原來源ledger，
不由投影反推；覆蓋是必要方向，沒有宣稱所有有限profiles可實現。

[獨立checker](../audits/2026-10-13-n2-ll-cut-3097ef5/checker.py)
重建同源S與容量界，完整枚舉各格0/1值，核對2,455份矩陣和604份cut代表；
原框算術及兩種新minor另有獨立控制。
[完整fibres控制](../audits/2026-10-13-n2-ll-cut-3097ef5/controls/REPORT.md)
保留320局部cells、856tuples、160joint cells、181全圖lifts及全部空fibres。
既有雙diagonal拒絕而off-diagonal接回的非平面控制仍正確標為非目標。
容量界、固定格、漏原邊、混框、跨列與minor跨邊毀損皆有拒絕控制。

```bash
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/profiles/domain.py --check
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/checker.py --check
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/checker.py --check
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/paper/topology_checker.py --check
```

正常／seed17、負控制、文件檢查及回歸執行範圍見
[驗證紀錄](../audits/2026-10-13-n2-ll-cut-3097ef5/verification.json)。
[父分類核對](../audits/2026-10-13-n2-ll-cut-3097ef5/review/ROOT_REVIEW.md)
只將完整Σ契約內的原55最後一格接回；當輪一般N2與E-ARC2保持OPEN，
原E4完整三列N2的後續涵蓋見頁首N2-BRIDGE。
基本LL-CUT保留為未獨立證成的較強證書機制；不以加強版排空來源後的真空性，
冒稱每份基本可行profile已被基本cut排除。
