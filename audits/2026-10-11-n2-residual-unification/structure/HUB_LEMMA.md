# N2 原55的共同 singleton-support 三-hub 排除候選

2026-10-11，基準 `5f0979793c19e452dbb5fc7e9fe7e43cb8a991cc`。
紙面候選 **N2-55-SINGLETON-HUB**，等待獨立驗證；原55与 E-ARC2 保持 OPEN。

## 1. 完整來源域與明列輸入

沿用 `docs/c5_excess_two_arc_spoke_closure.md:24-40` 的完整 N2 來源域：
有限簡單 induced C5 disk，指定有序 B；完整 Sigma933／941 或整圖共同 D5 像；
非框邊 Sigma-critical、epsilon2、有效 H 連通且 full B-touch；非相鄰原 degree5
roots r,s，其他有效內點原完整degree4；原 H−{r,s} 恰兩 mixed P,Q，其餘 unary；
每份 mixed actual support 非空。全部原件、框、ordered／shared contacts、ownership、
實際附件、rotation、bridges、完整 relations／空 fibres／full lifts 保留。

使用既有紙面結果：

- 分量必留：`docs/c5_excess_two_arc_component_slack.md:154-168`，每份原 C 刪除全收；
  故任一原拒絕 proper 列 beta 的 G−P 有一份完整染色。
- Unary 盾下界及實際支援：`docs/c5_unary_shield_budget.md:117-142`，每份原 U
  至少三個連續框支援點、盾弧至少兩邊；所有 one-sided 原 pieces 盾邊互斥。
- Hub 定理 B：`docs/c5_unary_shield_budget.md:155-179`，連通原 degree4 piece 的
  不可延拓外染色，若其鄰點能以≤4個互斥連通、兩兩相鄰、各在 piece 鄰點上常色且
  所見常色各異的 hubs 覆蓋，則原圖含 K5 minor。常色要求只在 N(P) 的交集上成立。

## 2. 共同引理與完整證明

**引理（候選）。** 完整來源若含 singleton-support mixed P，则原 unary 數 u=0，
且两 roots 的原框spoke總數 t=0。

反設 `N_B(P)={h}`，而有 unary U 或有原 root-spoke。
取任一原拒絕 proper 列 beta。G−P 的完整 beta 染色 psi 不可補回 P，
否則原 G 接受同一 beta。P 原連通、每點原完整 degree4。

**有 U 的情形。** 共同交換 roots 後 U owner 為 r，取三個原 bags

`R={r} union U`、`S={s} union Q`、`T=B`。

R 由 U−r 原 contact 連通；S 由 Q−s 原 contact 連通；B 是原框 cycle。
三 bags 互斥且都避 P。它們兩兩鄰接：

| bags | 保留的原鄰接 |
| --- | --- |
| R、S | Q 到 r 的原 mixed contact |
| R、T | U 的原框附件；U actual support 非空 |
| S、T | Q 的原框附件；Q actual support 非空 |

P 是原 H−{r,s} 的完整分量，故 `N(P)={r,s,h}`。
其與 R、S、T 的交集分別恰 `{r}`、`{s}`、`{h}`，完整覆蓋且各為 singleton。

**沒有 U、但 t>0 的情形。** 共同交換 roots 使 r 有一條原 root-spoke。
取 `R={r}`、`S={s} union Q`、`T=B`。三 bags 仍互斥連通並避 P；
R−S 由 Q−r contact、R−T 由該原 root-spoke、S−T 由 Q 框附件。
它們與 N(P) 的交集仍恰為 `{r}`、`{s}`、`{h}`。

兩種情形下，按 psi(r)、psi(s)、psi(h) 將取同色的 bags 合併。
原三 bags 的相鄰圖是 triangle，所以任一合併組都連通，合併後的 hubs
仍互斥、兩兩相鄰，數量≤3。psi 在每個 hub 與 N(P) 的交集上常色，
且各 hubs 的常色兩兩不同。Hub 定理 B 的全部前提成立，得原 G 的 K5 minor，
與 disk planarity 矛盾。故 u=t=0。∎

沒有要求 psi 在整個 hub 常色，沒有重染任何外部頂點，沒有保 Sigma 的 minor 声称；
source piece、原框及整份外部 witness 始終保持同一原圖／同一字面 beta。
此 proof 不使用三列具體色值，故任何共同 D5 搬運只需搬運 beta 本身。
也沒有借45 derivative minimality或低 incidence的欄飽和前提。

## 3. 對原55 relation 族的直接收窄

1. **u=2 的原55子型不存在。** 兩 U 盾長各至少2，先迫 ell=0；兩 mixed
   均短且 support 非空。引理禁止任何 singleton，所以兩 mixed 都是真框邊 pair，
   原盾費至少 `2+2+1+1=6>5`，矛盾。這沿用原盾互斥，不跨列相加色容量。
2. **u=1、ell=1。** 原 short mixed S 必為真 pair；U、long L、S 的盾長
   至少2、2、1，恰用五邊。因而 U、L 均為 actual 三個連續框點，S 真框邊兩點。
   可共同整圖搬至 `U support012`、`L support234`、`S support40`；
   這僅是已知 actual supports 的共同正常化，全部 relations／pins 仍保留。
   此完整原55模板 **仍 OPEN**；已採納45的指定 derivative proof不能直接搬用。
3. **u=1、ell=0。** 兩 short mixed 均為真 pair；U 盾長只能2或3，
   對應 U actual support 長3或4。原55的完整跨列 joint **仍 OPEN**。
4. **u=0、t>0。** 若有 short mixed，必為真 pair。u=0、t=0 的 singleton
   mixed 仍可保留；低 incidence source 引理另外给它 k≥4，但沒有一般排除。

若獨立核對接受，原表九格仍是六個已覆蓋真core格加三個原55名稱；
三個原55族中已排 u=2 子型，另兩個 u=1 子型有上述新的共同支援限制。
沒有一般 N2 來源排除、沒有界內全搜尋、沒有新來源或 Lean theorem。
