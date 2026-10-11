# BR-SD-1a：共用 r 雙奇環的 D-palette 矛盾獨立驗證

工作目錄：`/home/ray/developer/ai/math`。
來源 BASE：`4dd11f422c6fa49265a412085116b088786d0344`；執行時記錄 actual HEAD，
凍結本任務與引用來源的 exact bytes。此任務是舊 [BR-SD-1](../2026-10-11-single-deficit-applicability-804e3b0b1b/NEXT-TASK.md)
的窄接續，不覆寫其原封存。

先讀 HANDOFF、STATUS、[N45§2.11](../../docs/c5_excess_two_nonadjacent_unit_core45.md#211-單缺額查證與無-u-二連通子域)、
[degree-5介面§2／7](../../docs/c5_degree5_interfaces.md)、舊BR-SD-1來源合同與本輪[screening](REPORT.md)。
外部刻畫是 Dvořák [List coloring and Gallai trees，Theorem10，p.6](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
A目前為指定前提的紙面查證通過，沒有新Lean；本任務直接明設來源形狀，證明不依A。

## 精確來源合同

保留舊BR-SD-1合同1–4的同一原G、X=M=G−原r-spoke、proper三色β拒絕、
原完整Σ／逐邊witness、全部actual attachments／ownership／contacts／rotation。
M內唯一s完整degree5，其餘內點4；s恰兩個不同內鄰p/q、三原spokes全留。
C=H_M−s為唯一實際分量。C的全部blocks恰J1/J2/J3三原odd cycles及原bridges，
J1∩J2={r}，J3與它們互斥；J2私有u與J3私有v由唯一環間原bridge uv相連，u≠r。
p/q經原外臂分別到J1/J3私有點，臂可零長；無其他blocks或旁支，環長任意奇數。
D明定為β未使用的第四色。不得以抽象lists控制冒充滿足合同的disk來源。

## 待獨立核對的短證明

1. 從原M邊定義
   `L^D(v)=Col−β(N_B^M(v))−({D} if sv是原邊 else ∅)`。
   核每點 |L^D(v)|≥d_C(v)，且若C可著色便與原β及s=D拼成M著色，故C不可著色。
2. 逐原點選w1∈J1、w2∈J2，證它們既非C割點、亦非s-contact。
   J1只需避開r與外臂錨點；J2只需避開r與u。各odd cycle至少三點，保留這個存在性證明。
3. 核w_i的全部原鄰居，證d_C(w_i)=2且D∈L^D(w_i)。
   由不可著色degree assignment的blockwise-uniform刻畫，L^D(w_i)恰為J_i palette。
4. J1/J2在r相交，刻畫要求兩palettes互斥，但它們都含D，矛盾。
   核這是在完整來源合同下的任意大小紙面推論，不是零觸發控制的排除。

本任務不要求uv→R27 minor、target β-minimality或四query保持。
如核對四s-query，語義是固定β的C–B與s–C約束，暫不施加s–B spokes；
完整M在β下四種s色的全圖延拓均空。

成功：獨立封存上述精確子域的直接來源矛盾及外部定理依賴，對回原identity。
失敗：保存第一個不能證成的具名前提、原點／原邊／全部列表與完整見證，停在該步。
有限控制如使用，須區分triggered and holds／not triggered／counterexample；
無actual source不能以toy失敗宣称来源存在。不要擴到全部bridge-separated三環、
旁支、其他接點位置、更多環、非二連通、55、一般N45／ε≥3或主命題。

交付：REPORT、逐前提mapping、外部正式來源／hash、獨立核查與完整必要witness；
如有checker，附normal／seed17及損壞證書負控制。原輸入只讀，僅寫全新專屬audit目錄，
exclusive-create且保留失敗代次。不得改共享文件／舊封存、commit、push或發布。
本次保存任務文本不代表已發布派工或已執行獨立封存。
