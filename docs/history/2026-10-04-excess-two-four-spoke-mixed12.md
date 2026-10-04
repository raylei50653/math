# 2026-10-04：任務 A，mixed-(1,2)+a-unary 的具名來源排除與停止點

使用者指定任務 A 主線優先，接續 Kempe 導覽及 mixed11 完成報告 §6，
先取原 a=5,b=6、spokes01／23，核對原 unary crosscut、spoke省略的
minimal-core 身份，再銜接完整 ternary。接手 HEAD=`0e38127`，
cwd=`/home/ray/developer/ai/math`；保留前輪未提交成果及同工作區
另一路任務 B／P₃ 的變更。本輪未 commit／push，也未覆寫前序 artifacts。

## 完成範圍與原身份

[新報告](../c5_excess_two_mixed_core_four_spoke_mixed12.md)、
[固定 checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py)、
[artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12/observations.json)
在固定完整 Σ=933／941／整圖 D₅ 像、Σ edge-minimal induced-C₅ disk、
連通有效 H、ε=2、相鄰雙 degree-5 roots、其餘有效內點 degree 四、
唯一原 mixed incidence=(1,2)、a 側一原單接點 unary、兩側各兩 spokes
及原 ab 存在的前提下，排除 **原01／23及root交換**。
y₀≠y₁，x 可共享 y₀或y₁；全部原分量、附件／supports、bridges、
ownership、環序及同一字面色框保持。

核對得到兩個不同的原 ternary：

- a-spoke省略後若拒絕，省略圖自己 minimal；刪 b 後是單一
  **C+a+U**，contacts=(a,y₀,y₁)，deg(a)=2，一條原 a-spoke保留。
- 整份 U 省略的 N=G−U 若拒絕，N自己 minimal；刪 b 後是
  **C+a**，相同 contacts、deg(a)=1，兩條原 a-spokes保留。

兩者都違反既有 two-spoke 三接點 K₅ 定理，因此均全收。
G−au亦全收，但 u 的 degree降三，沒有把 G−au稱為minimal core。
完整五角色 N relation與整份R_U的精確接合迫每個原拒絕列的
全部N witnesses及原R_U具有同一singleton a色。

Critical au的actual支援必為03或034，原 a−u↝U−3 crosscut
封同longface C支援至{3}；另一原共同shortface允許{1,2}。
同色tightness後才作二hub合併；connected-exterior K₄排除及
二／三hub Gallai依賴逐項補齊。該原C替換僅主張π_(a,b,u)等式，
完整六角色joint不相等的負控制保存。

三個共同拒絕列01021、01202、01212的完整R_U由原S₄搬運迫
singleton為 **3、2、3**；同一原U的單接點固定未用色3守恆反證。
因此具名入口整份來源排除，不只證一列出口，也不以mixed11舊表分類新incidence。

## 新必要域與全部殘留

a-spoke省略全收迫a-pair為原框邊。b-pair沿用通用單spoke
minimality／拒絕位置獨立條件，固定933有7份、941有9份。
兩種root身份共 **70／90** 份新框架；所有固定七頂點骨架rotations
共 **6,432／8,224 assignments、160／200 disk rotations**。
共用pair有四份disk rotations，保留不同embedding及face身份。

短支援與同一原U的完整singleton covariance／fixed-unused3 screen
排除 **48／64** 份，保留 **22／26** 具名框架、**56／92** 個
原face／actual-U-support records、**72／130** 個完整relation schedules。
剩餘身份逐項保存於artifact與報告§6，涵蓋兩種root身份、三種x共享身份、
原C介面與每份U placement相容的同一rotation／C faces。
160root swaps核對原faces／支援／完整relations，1,480次共同D₅
搬運核對殘留的完整singleton schedules；沒有識別不同來源relations。

停止域包含尚未加入全部C幾何／degree-list限制的必要放寬，並非
來源實現或已完成mixed12分類。原共用pair也保存，沒有擴張本輪分類。

## 完整圖與重播驗證

[joint helper](../../scripts/c5_excess_two_four_spoke_mixed12_joint_controls.py)
保存72張完整degree圖：30張x獨立、24張x=y₀、18張x=y₁。
原C／U所有附件、actual supports、具名原圖路徑及整份coloring witnesses
明列；原完整Σ為68張1023、4張959，不宣稱disk或候選來源實現。

實際固定核對：

- 5,760次獨立全圖接合、92,160 pinned fibres（73,224空纖維）。
- 70,482完整六角色及6,732完整五角色tuple witnesses。
- a-spoke省略K=C+a+U有1,440完整ternary核對；G−U的K=C+a有720份。
- b-spoke省略L=C+b有1,440完整binary核對。
- 720 G−au／G−U完整乘積、720五角色投影等式、2,880原spoke接回。
- 180封{3}的C替換投影核對，另保存六角色不相等與marginal假接合控制。
- 225非空完整域的guard算子確認：拒絕 iff 兩域是同一singleton。

以下檢查已實際通過：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_joint_controls.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_unary_controls.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_spoke_three_contacts.py --check
lake build
```

主checker亦唯讀重算既有two-spoke ternary的完整payload、單接點
fixed-color local payload相同；這不是重播全部原conservation歷史table。
`lake build`完成8,831jobs，只有既有linter warnings，沒有新增Lean theorem。
原刪roots／ab、(4,4)完成證書與完整支援定理沿用，未重跑其所有歷史checkers；
本輪不宣稱舊文件hash的byte-check全面通過。

無seed的主checker逐byte重播亦通過。最後文件與artifact檢查通過：

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

check_docs核對516份Markdown／5,316本地連結；DocGraph核對62文件、
213relations、5families，0errors／notes；artifact status為ok=139。
本輪新observations已單独登錄manifest；不把共用工作區其他producer
的狀態當作本輪數學重播。檢查期間另外一份同時編寫的P₃歷史文件曾
尚未落盤，當時全域check_docs失敗；其落盤後完整文件檢查已通過。

外部依賴亦已直接讀取[Dvořák原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
Lemma7及Theorem10：connected degree assignment的slack／tightness、
Gallai tree及blockwise-uniform palettes適用條件與報告一致。
未以此聲稱外部定理已Lean形式化。

## 接手入口與貼用摘要

README、STATUS、Kempe導覽及synthesis已接入新報告；前序完成報告
加有日期的後續入口，原正文／歷史保留。HANDOFF仍為研究線薄索引，
研究線與進行中tag未變，依DOCUMENTATION規則不追加逐輪摘要。
大型observations由指定新producer、manifest與.gitignore重建；只登錄本輪新artifact。

> 接續任務A：先讀 docs/c5_excess_two_mixed_core_four_spoke_mixed12.md 及
> docs/c5_kempe_guide.md。固定Σ933／941、ε=2、相鄰degree5 roots、
> mixed12+a單接點unary、spokes各二及ab的原01／23（含root交換）已排。
> a-spoke省略刪b後是單一原C+a+U ternary；整份G−U刪b後是C+a ternary，
> 兩者全收。完整joint迫同一U的拒絕列singleton3／2／3，違反未用色守恆。
> 新必要域70／90已排48／64，22／26框架、56／92actual支援與72／130
> 完整singleton relations保存。停止於此；下一窄題原a5b6、spokes01／12
> 及root交換，U支援933=023／0234、941另有234，拒絕列R_U都{2}。
> 保留原R_C(x,y₀,y₁)與(a,b,x,y₀,y₁,u) joint、actualsupports、同一rotation
> 及完整witness。重播：PYTHONHASHSEED=17 python3
> scripts/c5_excess_two_mixed_core_four_spoke_mixed12.py --check。
> ε≥3、mixed12整型、來源實現、一般出口及K∞=K≤5未證；未commit／push。
