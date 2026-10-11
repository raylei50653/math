# N45-S 含 long：U 在降度側 r 的實際 sole C 映射與窄排除

2026-10-10，`SL-MAP-R`。BASE `0d76c4c887033e565eaa0ca4d2a515619d7c97f3`。
接續 [完整保留 U/L/S 的契約與必要化約](../2026-10-10-n45-s-long-contract/REPORT.md)。
原契約、v2有限證書與delivery bytes保持不變；本輪只推進其 U owner=r 的 SL-MAP。
29份凍結權威輸入及 prior certificate hash 見 [inputs.json](inputs.json)。

**窄結論 SL-R-EXCLUSION：** 在前輪 K1–K12 全部契約內，另設原 U 的 owner 是
降度 root r，則只省略原 spoke e=rb_i、且 X=G−e=M 自己 β-minimal 的身份不存在。
涵蓋 U 的全部必要原 incidence、long L 任意大小及 short S 的真 pair／singleton。
這是任意大小紙面前提映射＋既有 BASE 來源排除；有限工具不承擔此排除。
U 在 s 的兩分量分支、無 U 的 long／兩long、其他 core 身份及一般 N2／E仍 OPEN。
目前停止點由 [Kempe 導覽](../../docs/c5_kempe_guide.md) 維護。

## 1. 精確來源與原圖邊界

G 有限簡單 induced-C5 disk，原完整 Σ=933／941或共同D5像、非框Σ-critical、ε2。
原有效 H 連通、full B-touch；非相鄰原 degree5 roots r,s，其他有效原內點完整degree4。
H−{r,s} 完整分量恰 U,L,S，U只接r，L/S各接兩roots；L long，S short。
原 contacts／shared identity、actual attachments／support、ownership、bridges、rotation全留。
只刪原 e=rb_i，V(X)=V(G)、E(X)=E(G)−{e}；X=M自己拒絕同一literal β且inclusion-minimal。
U不是 coloring star，也不預設其 contact 數n_U=1。

每條 retained 非框邊f的 **X−f同β完整 witness** 來自X自己的 minimality；
原G各邊Σ-critical witnesses另列，不能遺傳或跨列相加。
自由孤立原點不進有效H，染色介面仍乘其全部自由assignments；對有效核心引用BASE。

前輪已證必要式：U/L原盾各至少2、邊互斥；其支援頂點聯集B，所以U/L附件全留使X full B-touch。
若不擁U的s有3原spokes，H−s連通及原fullB-touch使star長面只有3框邊，但原U+L需4，矛盾。
故t_s∈{0,1,2}。此步同时涵蓋pair／singleton S；pair的額外PG幾何更給t_s≤1。

## 2. SL-R-CORE：同一實際 X 的 sole C 與完整 degree

\[
C=H_X-s=\{r\}\cup V(U)\cup V(L)\cup V(S),
\]

\[
E(C)=E(U)\cup E(L)\cup E(S)\cup E(r,U)\cup E(r,L)\cup E(r,S).
\]

三原件皆連通且各有實際r-contact，所以C連通。沒有另一有效分量，沒有s−U、rs或inter-piece邊。
s到C的全部原contacts為 P=N_L(s)∪N_S(s)，繼承原有序座標；圖簡單且兩件互斥，
所以 |P|=m_s=5−t_s 個相異原頂點。shared r/s contact仍只是一個actual vertex。

s是X唯一完整degree5有效內點；r只因刪e降為4，C其餘點也是X完整degree4。
框B、原外面及restricted rotation仍是X的disk embedding。這不是取另一個小core，
也不是收縮U/L/S或從Σ-critical G偷得X的minimality。

## 3. SL-R-JOIN／F：完整 C relation、空 r fibres 與精確禁色

對全部proper literal γ，令 A_r^X(γ)=Col−γ(N_B^X(r))。
Λ_T°(γ;a) 是原T滿足完整internal edges／actual B attachments及全部r-contact避a的
所有assignments，**此處不pin s，也不加其contact避色**。則

\[
\Lambda_C(\gamma)=\coprod_{a\in A_r^X(\gamma)}
\{r\mapsto a\}\times\Lambda_U^\circ(\gamma;a)
\times\Lambda_L^\circ(\gamma;a)\times\Lambda_S^\circ(\gamma;a).
\]

restriction／union在原頂點原邊上互逆。按P投影得到R_C(γ)，每個tuple τ保全部
r色a及全部full lifts；所有(a,τ)∈Col×Col^P的ambient fibres含空者也保留。
不能從s已pin的joint先量化掉s，再稱它完整unpinned-s C relation。

對全部16 ordered r/s pins (a,b)，完整X lift恰為

\[
\mathcal L_X(\gamma;a,b)\cong
1[b\notin\gamma(N_B(s))]
\coprod_{\tau\in(\mathrm{Col}\setminus\{b\})^P}
\Phi_C(\gamma;\tau,a),
\]

其中Φ_C保存τ及r=a的全部C assignments，另乘自由孤立點因子。
恢復e依然是同一full lift上的r≠γ(b_i)；下節來源反證不需這項恢復，但不丟此座標。

未pin s時，L_γ(v)=Col−γ(N_B^X(v))滿足（r用刪e後的retained neighbors）
|L_γ(v)|≥deg_C(v)+1[v∈P]。C連通且P非空，因此strict-slack greedy使R_C(γ)非空。
令 F_C(β)=⋂_{τ∈R_C(β)}set(τ)，E_s=Col−β(N_B(s))。X拒絕给E_s⊆F_C。

X own β-minimality使所有retained s-spokes的β色互異：若重色，刪一條不改constraints，仍拒絕。
對每條s-spoke sb_j，X−sb_j完整β witness必取s=β(b_j)，否則它已可恢復成X。
該witness的完整C assignment全部contacts避該色，故β(b_j)∉F_C。於是

\[
\boxed{F_C(\beta)=E_s=\mathrm{Col}\setminus\beta(N_B(s)),\quad
|F_C(\beta)|=4-t_s.}
\]

此等式只用X自己的同β witnesses；不預填原U的禁色，也不從另一列補容量。

## 4. BASE 前提逐項映射與共同色框

原β是proper三色C5列：原G接受全部T4。一次共同整圖D5把singleton搬到b4，
一次S4把整個β搬到q=01012；G/X/e、rotation、contacts、所有tuples／fibres與witnesses同搬。
Σ(X)随之搬運，**不要求它等於933／941**；原G的target mask也保持同一整圖D5像。

| BASE需要 | 實際X提供 |
| --- | --- |
| finite simple induced-C5 disk及effective interior連通 | 原G restriction，§2的actual connected C和s。 |
| own edge-minimal q-obstruction | X=M自身minimal，K12供給每條retained-edge同β witness；整圖transport保其完整性。 |
| 唯一完整degree5點z，其餘有效內點完整degree4 | z=s；r已在X降4，U/L/S全保，§2逐點核。 |
| H−z sole connected C，5−t不同有序原contacts | §2 actual C與P，保shared vertex單坐標及全部tuple preimages。 |
| 完整C禁色，而非contact marginals | §3的full assignments／ambient r fibres；F_C=Col−spoke literal色。 |
| t=1/2的真實外hub連通與minor鄰接 | retained s-spoke在X中連B與s；不使用已省略e、不补造新outside路。 |

三條BASE排除各只需要一個rejected q的上述來源前提，不需第二拒絕列、T4、
完整Σ(X)=933/941、U省略或β是盾中點。t=0的(5)另**不需C外s−B路或K4-free**。
t=2若改命名兩spoke色0/1，須視作另一個whole-color presentation；不能同時硬要求
canonical q和特定兩spoke色。直接用BASE§5的任意異色spoke positions版本即可。

## 5. SL-R-T0／T1／T2：互斥窮盡的三個來源矛盾

**t_s=0，P有5點，F_C=Col。** 映回 [no-spoke §4](../../docs/c5_no_spoke_exterior.md)。
對四個d∈Col，完整C的M_d(v)=L_β(v)−{d: v∈P}均不可染且有degree-list下界。
tightness與同一block incidence matrix的欄獨立性給四份palettes的共同係數τ。
正active block為K4，負active block為bridge，接點恰為active forest葉。
若有h個非空分量與k個K4 nodes，葉數是2h+2k，不能等於5。
这里保留K4；沒有套只適用多分量／connected exterior的K4排除，也不假造s−B外路。

**t_s=1，P有4點，F_C為3色。** 映回 [single-spoke (4) §§1–5](../../docs/c5_single_spoke_four.md)。
原B∪{s}由retained s-spoke連通，故connected-exterior K4 lemma的原hub前提吻合。
同一C的三份rejected palettes迫兩個互斥positive triangles、一條negative原bridge、零contact arms。
完整degree4讓左triangle三點各留一條真外邊；原inactive branch若不碰B，slack與一次整branch換色
就能填回拒絕lists，矛盾。因此三條原boundary tethers存在、內部互斥並避active結構。
原五bags {a},{b},{x},{s,c,d,y}, B∪(三tethers內部) 的十鄰接分別由triangles、
s-contacts、bridge、tether首邊及**retained s-spoke**供給，得到X的K5，矛盾planarity。

**t_s=2，P有3點，F_C為互補2色。** 映回 [two-spoke (3) §§1–5](../../docs/c5_two_spoke_three_contacts.md)。
minimality已證兩spoke異色；该報告§5明涵蓋任意不同β色spoke位置，不把非相鄰框端點硬搬相鄰。
同一C兩份tight palettes的差给一active triangle與三條原bridge arms，終點恰原三contacts。
任意長arms與零長arms都覆蓋；完整degree4再給三條真boundary tethers。
五bags {s}、三條triangle端點＋完整arms、B∪(tethers內部) 的全部十鄰接來自
原triangle、三contacts、tether首邊及一條**retained s-spoke**，仍為X的原K5矛盾。

t_s=0/1/2互斥窮盡§1全部owner-r來源；pair只用0/1、singleton保0/1/2，不漏U incidence2。
矛盾是X自身的parity或原minor，所以這一窄來源身份不存在，沒有「X指定延拓自動提升成G」步驟。

以上沿用已採納BASE的任意大小block／tether論證。外部依賴為
[Dvořák《List coloring and Gallai trees》Lemma7／Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)：
本輪重新核講義的connected degree-assignment tightness及blockwise-uniform Gallai刻畫，
没有把此外部定理稱作Python／Lean已證。原框／branch sets收縮只作非平面反證，不是coloring replacement。

## 6. 有限介面、獨立核對與保存失敗

[checker.py](checker.py) 只重播前輪19份N2控制中U-owner的原spoke省略圖。
從原邊重建actual sole C、原P與X完整degree；對十列保存全部C assignments／R_C、
全部ambient(r,τ) fibres含空者，核16根pins的C接合与直接X全部lifts相等；
另對回前輪v2完整X fibres，且原G恢復式逐pin相等。
新證書的root cells存counts；全部X lifts由完整C assignments、ambient indices及pins可完整重建。
工具直接枚舉C，不另做三原pieces的unpinned-s natural join比較；该等價由§3 restriction／union承擔。
它不驗source rotation／criticality、沒有β-minimal正控制，不是來源排除oracle。
正式數量與hash見 [certificate.json](certificate.json)、[checks.json](checks.json)。

26份owner-r原spoke省略、260 literal rows，逐列核4160 root-pin fibres，
並保250880 ambient(r,τ) fibres，其中240740空；2436 root-pin cells為空。
原root順序含11份r-first、15份r-second，對prior證書比較時整對換坐標。
t_s=1有24份、t_s=2有2份、t_s=0沒有控制；兩份t_s=2是NA8-0020/0021、
兩原mixed皆short，不能當含long來源正控制。

有限source判定仍 **not triggered**：這些X全接受十列，原圖也不是完整933/941來源。
BASE三份只讀controls已重播；它們核palette／arms／bags，無界排除由§5紙面承担。
三份只讀分工與根agent逐項核前提：t0不能借外hub；t1的hub用retained spoke；
t2核任意異色position和完整r fibre。scope與共同normalization另有獨立核對。
[核對紀錄](reviews.json)保留r-list须用N_B^X的記號精化及finite inventory的修補。
普通／seed17重播byte一致；[負控制／漂移核對](negative-and-drift.json)中錯C full lift、
覆寫canonical與額外未列control均被拒絕，29 frozen inputs及prior證書零漂移。
formal-doc DocGraph與Markdown檢查均exit0；未重跑whole-worktree DocGraph，
不把歷史scratch duplicate IDs稱作已消除。

setup首次把PA補充報告當BASE Git blob，`git show` exit128；原八份已凍結文件未改。
[setup-attempt1.json](setup-attempt1.json)保留該失敗；PA及前輪contract改按各自delivery bytes
凍結並標明不是BASE blob，不把物理archive還原檔冒作Git authority。

前輪60份manifest payload bytes／hash全部核回。首次精確directory inventory因多一個runtime
`__pycache__/checker.cpython-314.pyc`而FAIL，見[custody-attempt1.json](custody-attempt1.json)；
cache保留，後續限定核manifest payload且明列extra，不宣稱整棵原directory零漂移。
前輪delivery的三個shared hashes是歷史快照；本輪routing修改後不再稱current。

```sh
python3 -B audits/2026-10-10-n45-s-long-r-map/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-long-r-map/checker.py --check
python3 -B scripts/c5_no_spoke_exterior.py --check
python3 -B scripts/c5_single_spoke_four.py --check
python3 -B scripts/c5_two_spoke_three_contacts.py --check
```

沒有新Lean theorem。本turn此前`lake build`已成功，之後只加紙面／Python evidence與Markdown，
未重跑同一Lean build，也不由build推出本輪拓撲形式化。

## 7. 覆蓋、remaining OPEN與傳播

**Closed scope：** 前輪K1–K12，完整原U owner=r、一long L、一short S，
只刪原r-spoke且X=M自身minimal的全部pair／singleton子支。紙面＋BASE／外部Gallai。
**Remaining OPEN：** U owner=s的實際C/U兩分量；無U的long／兩long；其他45／54、
原55、無45／54來源、一般N2／E與ε≥3；沒有新來源實現或Lean。

下一個窄義務是owner=s的完整C/U private-color covering及各t_s來源映射，
依舊保r fibres與全部literal列。pair的raw必要profiles和singleton incidence≥4不當來源證書。

L0此來源／有限介面；L1 N45權威頁、Kempe停止點和STATUS；因限定子支closure，
L2核直接父E4§4.3與頁首dated後續：reviewed-unchanged，三個一般relation族未關，
原dated含long OPEN仍是當輪語境，現況已連向N45；不改歷史worker原表。
直接consumer Phase B§2.1只補此owner-r窄後續；§3.2 reviewed-unchanged，
原容量接口與source控制0觸發不變。不提升一般N2／E或跨列候選，停止L2。
README／HANDOFF與跨線synthesis無新語義。
未commit／push／PR。前輪contract及歷史worker／證書bytes不改。
