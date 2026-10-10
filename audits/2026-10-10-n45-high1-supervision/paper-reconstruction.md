# HIGH1 原邊、完整同色 lifts 與來源排除重推

只量化 worker REPORT 的 H1–H13，任意有限大小；原 U 為單 contact sx，原 r/s 各兩 spokes。
本稿不代獨立裁決。所有原 vertices/edges、附件/support/ownership、ordered/shared contacts、
bridges/rotation、共同 literal 色框、十列及所有空非空 fibres/full lifts保留。

1. X僅刪rb_i，r完整degree4仍留rb_j，s完整degree5；X=M自己β minimal。
   H_X−s的原分量恰C={r}∪P∪Q與U，contact分拆(2,1)。r在C內度3但完整X度4。
2. C保全部ordered二contact tuples與r=c的完整fibre，包含rb_j條件；U保單contact全部fibre。
   同一s=a施三contact不等式作restriction/union全assignments雙射，孤立原點自由因子保留。
   G只比X新增c≠γ(b_i)。shared r/s contact只是一個原值；不能把X有lift當G有lift。
3. Xβminimal給s兩spokes異色；C/U unpinned connected各有contact slack，完整relation非空。
   逐刪s-spoke witnesses給F_C∪F_U精確覆蓋兩可用色。任刪分量incident edge的R10解除
   給各private color，兩集合遂為互異singleton。局部N-diagonal令r=s=a≠β(b_j)可染C，
   故F_C={β(b_j)}，另一singleton是三色β的未用色D，F_U={D}。
4. BASE (2,1)路由對實際X重核；相鄰指定類是排除，split-support全列公式及nonadjacent
   pA/pB是延拓，均不自動恢復e。原source/fullΣ搬運同時作用整圖，不各piece正規化。
5. 原one-sided P/Q的trueedgepair支持給互斥單邊盾弧，故兩支援邊不同。
   若共端v，原G六bags為P,Q,O=B−v和{r},{s},{v}，皆connected、互斥。
   四root-piece contacts、兩piece-v attachments、一O-v原框邊、兩root-O spokes給九鄰接。
   r/s各原2不同spoke端點，必各有端點不為v；O-r容許用e，因這個minor是在G。
   K₃,₃與G平面性矛盾，故支援邊頂點互斥。
6. 原critical sx給G−sx新增接受γ的full witness；其s=x色a，否則已可接回。
   若U另有contact避a的完整assignment，也可接回同一outside witness；故F_U(γ)非空。
   H−U連通及fullBtouch提供避U的原外路，BASE unary shield定理給盾弧長≥2。
   兩mixed邊移去後C5餘長2與長1兩段，連續U盾弧與它們邊互斥，只能恰長2。
   BASE支援等於盾弧全部頂點，得U actual support恰連續三點T。
7. 任意proper三色γ的未用色D，若某已見色h未出現於T，整份U的全部constraints在
   transposition(D h)下不變，全部assignments與contactpalette作雙射。單contact F_U至多1色；
   F_U不可能含D，否則亦含h。故有完整U assignment contact避D。
   以同一γ置原r=s=D，兩roots全部原spokes（包括e）皆合法。BASE E4§4.1的局部
   N-diagonal明確給各short P/Q全contacts共同避D的完整assignment，不需已給外部染色。
   三份完整piece assignments與同一r/s/I pins union，直接是原G全部原邊的full lift。
8. canonical三色q_k在連續三點T見齊三色恰當k∈T，故Q(G)⊆T。
   933有4個拒絕位置（含q2），941有非連續3點，皆不能含於連續3點T；整圖D5保此性質。
   全H1–H13內任意大小G矛盾。這不涵蓋HIGH2/3、long或一般N2/E。

外部信任：[Dvořák Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪官方PDF已核讀。BASE shield／局部N-diagonal等paper依賴沿明列原文，不聲稱新Lean。
固定relation toy／位置schemas只校準語義與算術；沒有有限具名HIGH1來源或trigger數。
