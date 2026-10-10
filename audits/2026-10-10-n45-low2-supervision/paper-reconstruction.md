# LOW2 監督端重推與限定 LOW 覆蓋

量詞恰worker REPORT §1的全部十二項LOW2前提，任意有限大小；本稿不代獨立裁決。

1. 原r的incident edges是rx1、rx2、對P/Q各一、唯一rb_i。僅刪rb_i後四條contact保留，
   r完整degree_X=degree_C=4，無框或s鄰。s三mixedcontacts＋兩spokes全留為唯一degree5。
   U/P/Q原點完整degree4。H_X=H_G；X=M自己β-minimal，不從原G遺傳。
2. C=H_X−s恰{r}∪U∪P∪Q及全部原內邊和四r-contacts。三pieces connected且接r，
   故為唯一實際分量。U內x1–x2路及兩原r邊形成的cycle仍完整存在，未套unit bridge身份。
   s三原contacts K繼承rotation且互異；shared r/s contact只是一個原變量。
3. 同一literal γ下，U/P/Q全assignments沿一個r色c接合；U兩條不等式同時作用同一f_U。
   原piece間沒有另邊，所以 restriction／union是全部C色assignments的雙射。
   全Col³ fibres（含空）、全部r/s pins與full lifts保留。X再加s兩原spokes和三contact條件；
   G只多原條件r≠γ(b_i)。D5/S4/root swap只共同搬整圖、全部attachments及資料，933 q2照留。
4. 對實際X框list，|Lγ(v)|≥deg_C(v)+1_[v∈K]，connected C有contact slack故可染，R_C非空。
   β下X自己minimality排除兩s-spokes同色。其色u,v異色，A_s=Col−{u,v}⊆F_C；
   刪u-spoke的β-full lift迫s=u，C不變，故u∉F_C；v同理，得到精確F_C=Col−{u,v}。
5. 分別pin兩補色a，M_a是同一C全部原頂點的degree-assignment，拒絕迫全tight。
   Gallai Theorem10給兩份block palettes；其lists只在三原contacts有補色差。
   leaf-block私有點歸納使block-incidence columns線性獨立，所以activeblocks僅交換補色。
   contacts active-degree1，其餘0/2；恰三葉activeforest只能有一tree，唯一三度block為triangle，
   其餘bridge給三arms。arms任意長或零長。U原cycle是C某原block的一部分，不被刪改。
6. triangle每點已有兩triangle邊＋arm首邊（零arm則原s-contact）；完整degree4只剩一原邊。
   該邊接B或是一條bridge進入無s-contact且不重接active結構的inactivebranch。
   若branch無B，刪它給connected remainder入口slack可染；branch入口內度3、其他4，
   全Col四色可由slack染，整支共同行使色置換避bridge端色就能延拓，矛盾。
   branch即使包含r也沒有B/s constraints，原刪邊rb_i不是X約束；不能用rb_i作tether。
   因此三原boundarytethers存在，內部互斥且避active結構。
7. 原bags Z={s}, V_i=triangle點＋arm, O=整個B＋tether內點皆connected互斥。
   三triangle邊、三原s-contacts、三tether原接邊、一保留s-spoke見證全部十對K5bags。
   零arm仍有原s-contact；不使用被刪rb_i。與原X的disk平面性矛盾。

只用一次全圖S4重命名u,v及補色，BASE三接點§5允許任意異色spoke位置。
外部依賴：[Dvořák Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)；
官方文稿本輪已web讀取。原BASE paper、外部定理、Python封存、來源控制與Lean分層。
沒有新LOW2 source control、trigger數、source realization或Lean。

## 限定 LOW composition，須另對回 L2A 的獨立覆蓋裁決

只取authority§1精確原spoke省略X=G−e=M與原S06的S-SHORT-U-LOW：唯一原U在r，
原兩mixed真edgepair支援，mixed incidence(m_r,m_s)=(2,3)。令u為U原incidence，t為r原spokes。
degree_G(r)=5給2+u+t=5；原U非空且接r給u≥1，e原spoke存在給t≥1。
因此u=1或2，分別t=2或1；s三mixedcontacts給原t_s=2。
u=1全滿已採LOW1契約，u=2全滿此LOW2契約，兩支互斥窮盡。
若兩paper均正式接受，限定S-SHORT-U-LOW不存在。root swap共同搬全部原身份。
這不包括HIGH(U在s)、long mixed、其他cores／原55、一般U或nonminimal省略、一般N2/E／ε≥3。
