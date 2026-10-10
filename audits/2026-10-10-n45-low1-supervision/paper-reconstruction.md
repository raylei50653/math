# LOW1 監督端獨立重推

範圍恰為 worker REPORT §1 的完整任意大小 LOW1 契約；所有前提一起量化。
本稿先記論證，正式接受須再對回獨立裁決與封存版本。

1. 唯一刪邊是原 rb_i，故 H_X=H_G。r 的原 2 mixed contacts＋rx＋2 spokes
   降為完整 degree4，s 保持 3 mixed contacts＋2 spokes的完整 degree5；其他點完整 degree4。
   X=M 自己的 β-minimality 是另給前提，不能從原 G 的 Σ-criticality推給一般 derivative。
2. H_X−s 的頂點恰 {r}∪U∪P∪Q，每份原 piece connected且接r，故為 sole connected C。
   原 s 的三contacts在P/Q，簡單圖使其互異；原 rotation 給其順序。
   共鄰contact仍是一個坐標，degree_C不能當complete degree_X。
3. 同一字面 γ 下，把 U/P/Q 全部內點 assignments接到同一r色 c，逐原r邊施不等式；
   原部件間沒有另邊，故restriction與join互逆。s=a再共同施三原contact不等式。
   全十列、pins、空／非空 fibres與全部 full lifts照此保留；G的lifts比X僅多rb_i限制。
   C用實際X框附件的lists，至少一個s-contact有strict slack，Lemma7保R_C非空。
4. s兩spokes若β同色，刪一條不改任何約束而仍拒絕，違反X自己minimality，故色u≠v。
   拒絕X給Col−{u,v}⊆F_C；逐刪s-spoke的完整β-lift迫s用被释放色，給u,v∉F_C。
   因此F_C=Col−{u,v}恰兩色。這不聲稱F能逆向復原R。
5. 對兩補色a各pin原s，由完整degree4得到M_a為degree-assignment；其不可染迫全tight。
   兩lists只在三具名contacts差補色。Gallai Theorem10給同一C的blockwise palettes。
   leaf-block私有點歸納給vertex/block incidence columns獨立，故activeblocks僅交換補色。
   contacts active-degree1，其餘0或2；active incidence forest恰三葉，只有一棵非空tree，
   唯一三度block為triangle，其他activeblocks是bridges，得到三條可零長的原arms。
6. triangle每點已用兩triangle邊和arm首邊（零arm則用原s-contact）；complete degree4只餘一邊。
   該邊直接接B，或是進入無s-contact、不能重接active結構的inactivebranch的bridge。
   不同branch互斥。若branch不接B，刪它使剩餘連通圖在入口得slack可染；branch自己無B/s
   禁色且入口有slack可四色染，只對該完整自由branch同時置換色避bridge端色，可接回矛盾。
   故三個原boundarytethers存在，其內部互斥並避active結構；保留U沒有被替換或刪除。
7. 原bags Z={s}, V_i=triangle點＋其arm, O=整個B＋三tethers內點，皆connected且互斥。
   3triangle邊、3原s-contact邊、3原tether接邊、1保留s-spoke見證全部10bagpairs，得原X的K5 minor。
   省略rb_i沒有被用來補邊；零arm不使s-contact消失，與disk平面性矛盾。

BASE two-spoke-three-contacts §5允許任意兩個β異色spoke位置。
以上直接按原β推，不需先把βsingleton搬到U盾中點；933 q2照留。
一次整圖S4可只重命名u,v和兩補色；若搬D5也須搬整圖、rotation與全部十列一起。

信任界線：任意大小paper＋固定BASE theorem＋外部Dvořák Lemma7／Theorem10；
外部官方PDF已以web讀取（2026-10-10），[原文](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。
Python僅核封存，沒有新LOW1來源、targettrigger、source realization或Lean。
不裁LOW incidence2、HIGH、long、其他core／原55、一般N2／E或ε≥3。
