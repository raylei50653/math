# N45-S-LOW1：保留完整 U 的單-root 三接點排除候選

2026-10-10。BASE／實讀 HEAD：`dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
任務凍結見 [task](task.md)，六個 current-work pins 見 [inputs](inputs-initial.json)，
Git-object 數學依賴見 [BASE inputs](base-inputs.json)。

**交付結論：完整 LOW1 契約內的任意大小來源不存在；這是新 paper 候選，待獨立增量裁決，尚未採納。**
唯一刪邊是原 spoke `rb_i`。U 完整保留；`H_X−s` 恰一個 connected degree-4 分量，
有三個實際原 s-contacts、兩條 β 異色原 s-spokes及精確兩色禁集。
因此可對回 BASE two-spoke-three-contacts §1–5，抽取 X 自己原邊上的 K₅ minor。
不用 SS 的整 U 刪除／框內點未接論證，不先限制 β 的 singleton 位於 U 盾弧中點。

本交付只量化下列 LOW1；LOW incidence2、HIGH、long、原55、其他 cores、一般 N2／E
及 ε≥3 保持 OPEN。本輪沒有新有限來源、trigger 數、source realization 或 Lean。

## 1. 完整原來源契約、量詞與依賴

任取任意大小的有限簡單 disk 圖 G。有序 induced C₅ 外框 B=(b0,…,b4) 為外面。
完整 Σ(G)=933／941 或其一次共同整圖 D₅ 像；每條非框邊對完整 Σ critical；ε(G)=2。
有效 H 忽略原孤立內點，連通且 full B-touch。恰兩個非相鄰原完整 degree5 roots r,s；
其他有效原內點完整 degree4。

`H−{r,s}` 的完整原分量恰為 unary U 和 mixed P,Q；三者 one-sided、actual support 非空。
U 唯一原 contact 為 rx，歸屬 r；沒有 U–s 邊。P,Q 每側 incidence 皆正，
各自 actual support 恰一條原真框邊的兩端；`(m_r,m_s)=(2,3)`。
因而 r 對 P,Q 各一原 contact，s 的原 contact 數分配為 1 與 2；兩 roots 原各兩 spokes。
不任意交換 P,Q 的具名身份；以下以它們原 contact 清單作證。

固定原 spoke e=rb_i、原拒絕 literal β；`X=G−e=M` 是 β 的 inclusion-minimal 45／54 core。
以一次共同 root swap 命名降度側 r。除 e 外，全部原頂點、U/P/Q 內邊、root contacts、
框附件與其他 spokes 完整保留。原已忽略的孤立內點可逐點自由 lift，沒有新有效孤立點。

原圖的具名 ordered contacts、shared vertex 單一坐標、actual attachments/support、ownership、
bridges、rotation、共同 literal 色框及全部十列 relations、空／非空 fibres與全部 full lifts
一併保留。D₅／S₄／root swap 都只共同作用整圖和全部資料，不獨立正規化 pieces。
canonical 941 拒絕 q0,q1,q3；933 另拒絕 q2；本證明逐任意 β 成立，沒有略去 q2。

| 凍結依賴 | 本輪使用與信任界線 |
| --- | --- |
| [S 原交付 §1、§7](frozen/current/audits/2026-10-09-n45-s/REPORT.md)、[SU-A S-06](frozen/current/audits/2026-10-09-n45-su-a/independent-judgment.json) | 接收已採納 LOW 必要身份；本輪另從指定 LOW1 全部原邊重新證明 X 的新圖類前提 |
| [BASE R10 §1–4](base-source/docs/c5_degree5_interfaces.md) | 完整 degree-4 分量介面、degree-list 與 minimality；本輪直接重證本 sole-C 的精確 F，不沿用父 G criticality |
| [BASE two-spoke-three-contacts §1–5](base-source/docs/c5_two_spoke_three_contacts.md) | 任意大小 active triangle／三臂／實際 boundary tethers／原 K₅ bags，尤其 §5 任意兩個異色 spoke 位置 |
| [BASE list-critical §1](base-source/docs/c5_weak_list_cores.md) | β-minimality 的同色 spoke 冗餘；下文另給刪邊直接證明 |
| [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) | strict slack／tightness及 Gallai blockwise-uniform 刻畫；外部定理，非本輪 Python／Lean 證明 |

BASE PDF、官方當日 PDF bytes 相同；見 [external check](external-source-check.json)、
[官方 PDF](external/gallai-official.pdf)及 [BASE PDF](base-source/audits/2026-10-04-task-d4/a3/gallai-primary-source.pdf)。
兩個陳述與證明已讀取，text extraction 在 `logs/gallai-text.stdout.log`。
SS／SSA／監督 acceptance 六個指定 current-work inputs 均凍結核 pins；它們不充作 LOW1 新證明。
不 import worker checker 或裁決結果當獨立證明；本輪自查也不是獨立驗收。

## 2. LOW1-CORE：唯一刪邊、完整 degrees 與 minimality

**量詞／前提：** §1 全部契約，每個指定 (G,e,β,X)。**層：** 任意大小 paper。
因 e 只有 r 與框點兩端，原 induced interior H 的邊完全不變：`H_X=H_G`。

| 點／原因子 | G 的完整 degree／邊 | X 的完整 degree／保留 |
| --- | --- | --- |
| r | 兩 mixed contacts＋rx＋兩 spokes＝5 | 只刪 rb_i；兩 mixed contacts＋rx＋一 spoke＝4 |
| s | 三 mixed contacts＋兩 spokes＝5 | 全部保留，degree5；rs 原不存在 |
| U、P、Q 每點 | 全部內邊、原 contacts、actual B attachments 合計 degree4 | 一條邊也未刪，完整 degree4 |
| B | 原 induced C₅及全部原附件 | C₅不變；只有 rb_i 不在 X，disk rotation 是原 rotation 的限制 |

因此 X 自身 ε=1，唯一 degree5 內點是 s。X 的 β-minimality是任務的 `X=M` 前提；
**沒有從 G 的 Σ-criticality 遺傳。** 每條 X 非框邊 h 被刪後都接受同一 literal β，
否則 `X−h` 是拒絕 β 的真子圖。這也使 X 自己 Σ-critical，後文只使用 β-minimality。
沒有引用 E2 必要 mask 表、U4／retained44 下界或任意 derivative 自動 critical 的說法。

## 3. LOW1-COMP／JOIN：sole C、三 contacts 與完整接合

**量詞／前提：** §1 全部契約及 §2。**層：** 原邊的任意大小 paper。
原分量完整清單直接給

`C=H_X−s=X[{r}∪V(U)∪V(P)∪V(Q)]`。

其邊完整為 U/P/Q 的全部原內邊、rx、r 對 P,Q 各一 contact；不存在不同原 pieces
之間的其他邊。P、Q 都 connected 且有 r 邊，U connected 且有 rx，所以 C connected。
沒有另外分量。此式是對 X 的既有原頂點集合命名，沒有刪 U、收縮 r 或替換 pieces。
C 的每點在 **X** 中完整 degree4；不能把 `deg_C` 誤寫成 4。

令 `(p1,p2,p3)` 是 s 原 rotation 清單中剔除兩條 B-spokes後，繼承的三個具名 contacts
及次序。它們都是原 P/Q 頂點；簡單圖使同一 root 的三個 neighbors 互異，P/Q 互斥。
U 和 r 均非 s-contact。若某 p_j 同時也是 r-contact，它始終是一個原頂點坐標；
其 r 與 s 兩個不等式共同作用該坐標，沒有分裂成兩個 ports。

對任意同框 literal proper row γ（包括十列及其整列 S₄ 搬運），設 Col={0,1,2,3}，
`A_r^X(γ)=Col−γ(N_B^X(r))`。Λ_T(γ) 是原完整 T=U/P/Q 的**全部**內點 assignments：
滿足 T 全部原內邊和全部 actual boundary attachments；保留每個 contact 的原坐標。
Λ_T 先不 pin roots，沒有用原 root 色對 relation 的 marginals。

完整 C lifts 恰為下列原邊 natural join：

```text
L_C(γ) = { (c,f_U,f_P,f_Q) :
    c ∈ A_r^X(γ), f_T ∈ Λ_T(γ) for T=U,P,Q,
    f_U(x) ≠ c,
    f_T(v) ≠ c for every original rv contact of T=P,Q }
R_C(γ) = { (f(p1),f(p2),f(p3)) : f ∈ L_C(γ) }
L_C(γ;a) = { f ∈ L_C(γ) : f(pj) ≠ a for j=1,2,3 }
F_C(γ) = { a ∈ Col : L_C(γ;a) is empty }
```

這些集合保留全部 assignments；R_C 每個 tuple 的 fibre 就是 L_C 中投影到它的全部 lifts，
包括空 fibre。對同一 c，各 pieces 可沿唯一共同 r 坐標接合，且 converse 是 restriction，
故沒有遺失或新增任何 C assignment。U 的原 full lifts 在 c 坐標接入，不被刪除或改成 star。
若查原 mixed `A_T(γ)`，則 `(c,a)` 必須由**同一** f_T 同時避開全部 r/s-contacts；
這恰是 L_C(γ;a) 中的條件，shared contact 仍只有一個色值。

令 `A_s(γ)=Col−γ(N_B(s))`。X 全部 γ-lifts就是各 `a∈A_s(γ)` 的 L_C(γ;a) 加上 s=a、B=γ；
G 全部 γ-lifts再共同加唯一原條件 `f(r)≠γ(b_i)`。兩圖的 lifts 不混用。
上述式逐十列、每個 root pin及其空／非空 fibres成立；沒有獨立挑列或獨立換色拼圖。

**R_C(γ) 非空。** 每個 v∈C 用實際 X 邊給
`L_γ(v)=Col−γ(N_B^X(v))`，有 `|L_γ(v)|≥deg_C(v)`；在每個 s-contact 處至少多一色，
因其完整 degree4 中另有一條 sv 邊。C connected，Lemma 7 strict-slack 貪婪法給完整
L_γ-coloring，故 L_C(γ)、R_C(γ) 非空。這沒有先假定 pinned s 能接回。

## 4. LOW1-F：β 異色 spokes 與精確 forbidden set

**量詞／前提：** §1–3，每個指定 β；使用 X 自己的 minimality。**層：** paper。
命名兩条原 s-spokes `sb_j,sb_k`，兩者在 X 完整保留。
若 β(b_j)=β(b_k)，刪任一 spoke 不改 s 的 list，X−spoke仍拒絕 β，違反 β-minimality。
因此它們的字面色 u,v 互異，`A_s(β)=Col−{u,v}` 恰兩色。

X 拒絕 β 及 §3 精確 join 給 `A_s(β)⊆F_C(β)`。
刪 sb_j 後的 β-full lift 必使 s=u：若 s≠u，同一完整 lift 已滿足被刪的原 spoke，會延拓 X。
限制該 lift 到 C，得到 L_C(β;u) 非空，所以 u∉F_C(β)。刪 sb_k 同理給 v∉F_C(β)。
因此

`F_C(β)=Col−{u,v}=A_s(β)`，且 `R_C(β)≠∅`。

這是完整三-contact relation 的避色查詢，不宣稱 R_C 可由 F_C 復原。
每個 β-spoke 刪邊 witness 屬 X−spoke；用於此處的 precise F 與原 G−e 的跨列 witness
不同，不能把它們交換。未要求 β 是 U 的 forcing 列、U 盾中點列或任何 SS 特定列。

## 5. LOW1-MAP：BASE §1–5 全部充分前提與原 K₅

**量詞／前提：** §1–4。**層：** 新圖類前提映射＋明列 BASE paper／外部定理。

| BASE 使用點 | 在本 LOW1 的完整對應 |
| --- | --- |
| §1 有限簡單 induced-C₅ disk、minimal q-obstruction | 同一 X=G−rb_i；B與原 rotation保留；literal β-minimality由 X=M 自己提供 |
| §1 唯一完整 degree5 z、其他完整 degree4 | z=s；r 只降度，U/P/Q 完整保留；§2 的完整 degree 清單 |
| §1 `H−z` sole connected C、三個互異原 contacts | §3 明列 C 頂點及全部邊；原有序 `(p1,p2,p3)`，無新接線、無縮圖 |
| §1 非空 R_C、F_C恰兩個互補色 | §3 strict slack及 §4 刪原 s-spoke 的完整 witness；不是推測兩 mixed joint 的 marginals |
| §1、§2 全 vertex degree-lists、同一 C 的兩份 tight assignments | §3 的 L_β；pin a 後從 s-contact list刪 a，`|M_a(v)|≥deg_C(v)`；拒絕迫 tight |
| §2 block-column independence／active forest | 同一 C 全部原 blocks；兩 lists差只在這三個原 contacts，不改原 shared cut vertex |
| §3 complete degree4／inactive branch／actual tether | 用 X 的 complete degrees和全部原 inactive branches，包括仍在其中的 U／r；tether必由 X 保留邊取得 |
| §4 root-to-boundary edge、原 K₅ bags | 兩条 sb_j,sb_k 都在 X；任一條給 root-bag 到原 B-bag 的鄰接；不使用省略 rb_i |
| §5 任意兩個 differently β-colored spoke 位置 | u≠v；不要求 j,k 相鄰；只共同搬整圖 D₅／S₄，原接點次序與 rotation保留 |
| §5 第二拒絕列／T4 | 此較強排除不需要二者作額外 theorem 前提；不為湊原 printed q 另選 β |

若對照 printed q=01012，可將三色 β 的唯一 singleton 框點以整圖 D₅搬到 b4，再共同
S₄將整列搬為 q。所有 941／933 原拒絕列都屬此三色 orbit；保全部被搬的十列和 mask，
不重新要求搬後 mask仍印成 canonical 941／933。BASE §5 再允許兩個 q 異色 spokes的任意位置。
也可直接留在原 β，只用一個全圖 S₄將 u,v 命名 0,1、其餘兩色命名 2,3。
以下 equations只見这兩個 pin 色與同一原 boundary lists，所以原 β次序不變。
兩種搬運都沒有先把 β singleton對到 U 盾弧中點。

為核對任意大小搬用，列出 BASE §1–4 在 X 的抽取鏈。
對 a=2,3，`M_a(v)=L_β(v)−({a} if v∈{p1,p2,p3} else ∅)` 不可染、degree-lists且全部 tight。
contacts 的 boundary colors避 2,3；兩份 lists差恰
`1_[v contact](1_[color=3]−1_[color=2])`。Theorem 10 給同一 C 的 block palettes；
block-incidence columns以 leaf-block 私有點歸納線性獨立，故 active blocks只交換 2↔3。
原 contacts各 active-degree1；非contacts active-degree0或2。active incidence forest恰三葉，
因此只有一棵非空 tree、恰一個三點 active triangle，其餘是三條 bridge arms。
arms可任意長、可零長；終點恰原 p1,p2,p3，三臂除 triangle外互斥。

每個 triangle點 v_i 有兩條 triangle邊及一條 arm首邊，零長時第三邊為原 s-contact。
X 中完整 degree4只剩一條原邊；它是直接 B附件，或進入一個不重接 active structure、
沒有 s-contact的 inactive branch W_i 的 bridge。不同 W_i互斥。
若 W_i在 **X** 不碰 B，C−W_i connected且在 v_i獲 strict slack，可染 M_2；
W_i 的接入口 degree3、其他點 degree4且無 B／s constraints，用 Col再由 slack填入，
只共同重命名這個不受外部禁色的完整 W_i coloring使 bridge兩端異色，即延拓 C，矛盾。
故每個 W_i真有 X boundary attachment，取其原路給 tether；三tethers內部互斥且避 active structure。
U沒有因此被刪或改寫。此旁支的 local coloring雙射只證可填；不拿獨立正規化的 pieces拼原跨列資料。

令 Z={s}，V_i是 triangle點 v_i加其完整原 arm，O是原整個 B加三tethers全部內點。
五 bags均非空、connected、互斥。三 triangle原邊給 V_i兩兩鄰接；三原 s-contact邊給 Z–V_i；
三原 tethers給 V_i–O；保留的 sb_j給 Z–O。十對 bags均有 X原邊見證，故 K₅ minor，違反 disk平面性。
零長 arm時 V_i={v_i}，原 sv_i仍給所需邊；沒有消失的 contact或以省略 e補鄰接。
B只在最後的 minor中作 connected bag，沒有成為保染色的 replacement。

## 6. LOW1-EXCLUSION、coverage 與正式停點

§2–5 對每個滿足 §1 的 (G,e,β,X)給矛盾，故 **LOW1完整契約內不存在任意大小來源**。
六個逐 claim量詞、全部前提及依賴見 [claims](claims.json)。
這是 candidate paper judgment；本執行者沒有採納或修改 N45的當前 OPEN。

| 證據層／控制 | 本輪狀態 |
| --- | --- |
| 任意大小 paper | LOW1-CORE／COMP／JOIN／F／MAP／EXCLUSION；充分前提逐項如上，待独立裁決 |
| BASE與外部信任 | BASE three-contact theorem／R10及 Dvořák Lemma7／Theorem10；官方PDF與BASE bytes相同 |
| 新有限 source control | **未建立、未執行；無 trigger 數**；不把其他 N1、SS或LP controls當 LOW1覆蓋 |
| 工具封存核對 | normal／seed17只核 inputs／manifest／live drift／local links；不計作任意大小paper或source排除證明 |
| 來源實現／反例 | 沒有新的具名 source realization；沒有來源 counterexample |
| Lean／一般命題 | 沒有新 Lean；未跑 lake build／axioms；一般 N2／E保持 OPEN |

没有 finite graph query，故不製造 `triggered and holds` source計數，也不把未評估寫成 0觸發。
既有 S/SU finite source不觸發的結論只作歷史邊界；本輪不重跑、更不升格成 LOW1正控制。
本輪沒有新数学 gap finding；獨立 reviewer仍須核 §5 新圖類搬用、外部依賴與完整契約。

## 7. 驗證、既存 FAIL 與寫入範圍

實際 commands／exits／stdout／stderr 見 [checks](checks.json)及 [最終封存命令](seal-final-v3/commands.json)。
[最終 MANIFEST v3](MANIFEST.final-v3.sha256)凍結 payload；[delivery](delivery.json)另綁 manifest與封存核對證據。
首輪 verifier比較 string排序與 Path排序而錯拒相同檔案集合；原 [v1 manifest](MANIFEST.sha256)、
[失敗命令](seal-checks/commands.json)及 [工具 finding／原碼快照](failed-seal-v1/finding.json)完整保留。
這是工具 inventory排序錯誤，沒有 paper前提或資料漂移；v2統一排序後另封，不覆寫 v1。
第二輪又把初始 Git列出的四個 nested-repository directory entries錯記為缺檔；
[v2 manifest](MANIFEST.final-v2.sha256)、[失敗命令](seal-final-v2/commands.json)及
[分類 finding／原碼快照](failed-seal-v2/finding.json)保留，v3依原始帶 slash的 Git清單辨識目錄。
兩次都沒有改數學論證。首輪負控制停在排序錯誤，不能算 digest負控制覆蓋；最終 v3另核實錯誤 digest被拒。

| 已實跑的文件／來源檢查 | 結果與範圍 |
| --- | --- |
| HEAD／六個指定 current-work pins | HEAD=BASE；六份全部符合任務 SHA256，凍結 current與BASE明確分開 |
| 12個具名 BASE blobs／官方 Gallai PDF | Git object、archive bytes／hash一致；官方PDF與BASE PDF byte相同 |
| fresh BASE `check_docs.py` | **exit1**；恰兩個歷史缺檔：D5 c4 scope ledger、D2 integration diff，實際原路徑留於 checks |
| fresh BASE正式 docs DocGraph | exit0 |
| current `check_docs.py`／正式 docs DocGraph | 各 exit0；只證相應文件範圍 |
| current whole-worktree DocGraph | **exit1**；62個 duplicate-ID errors；本輪新 BASE archive也保留在列出的副本中 |
| tracked／cached `git diff --check` | 各 exit0；既有 shared diff保留不變，沒有提交 |

normal／seed17 的封存入口、corrupted-manifest負控制及列明 pre-existing Git inventory零漂移，
以封存命令及 delivery的實際 bytes綁定；工具不驗證任意大小數學。

```bash
python3 -B audits/2026-10-10-n45-s-low1/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-s-low1/verify.py
```

入口只讀；需要 original workspace root有同一 HEAD、六個 current-work pins與 Git列出的既有
25,869個 regular-file bytes、22個 symlink identities及4個 nested-repository directories。
四個 nested repos只核原清單的目錄存在，**初始未遞迴 hash其內部，不能宣稱此項 fulltree零漂移**。
其餘列明檔案 hash及所有指定 authority inputs的零漂移另核。完整 BASE來源在本目錄 `base-source/`；
沒有要求凍結 BASE重建 current-work採納文件。normal／seed17結果及負控制的實際數字以 checks為準。

歷史 E4 provenance byte-replay FAIL保留，不在本輪重跑。fresh BASE `check_docs.py`的兩個歷史
缺檔及 whole-worktree DocGraph duplicate-ID FAIL分開記錄；正式 docs DocGraph的結果另列，
不合併成全部工具PASS，不刪 retained copies隱藏FAIL。

Closure scope：僅 §1 LOW1任意大小 paper候選，未正式採納。
Updated：只新專屬 audit的 Source／Evidence交付。
Reviewed-unchanged：current N45、Kempe guide／STATUS保留 LOW1待處理與一般父題 OPEN；
歷史 adoption快照的尚未啟動字樣保留當時語境。HANDOFF／README／DOCUMENTATION無新路由語義。
Remaining OPEN：LOW incidence2、HIGH、long、原55、其他 cores、非unit／非minimal身份、一般 N2／E及 ε≥3。
Propagation stop：L0交付、L1窄核對；由後續獨立裁決決定是否採納及傳播，本輪不選下一residual。

只寫 `audits/2026-10-10-n45-s-low1/`，不改任何共享或其他封存；無 commit／push／PR／對外訊息或subagents。
