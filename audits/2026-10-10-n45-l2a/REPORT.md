# N45-L2A：LOW2 任意大小紙面與限定 LOW 覆蓋獨立稽核

2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
本稽核只新增此專屬目錄；未讀本輪 peer judgments，未改共享或舊 audit。

**裁決：六項 LOW2 claims 在完整十二條原契約內成立。** 另獨立裁定：已採納 LOW1
與本輪 LOW2 排除窮盡權威 §1 精確 S 身份下的 §3 S-SHORT-U-LOW；限定父 LOW 可合成排除。
後一裁決是另證的原身份覆蓋，不是單從 LOW2 成立便推廣。HIGH、long、其他 cores／原55、
一般 N2／E、來源實現及 Lean 均仍 OPEN。正式採納與共享文件傳播由監督另裁。

[完整結構裁決](independent-judgment.json)逐項保留量詞、source_contract、依賴及兩項獨立裁決。
[固定輸入](inputs.json)將 current pins、四個真 BASE blobs、worker 版本分層。

## 1. 範圍及自己的 degrees

任意大小有限簡單原 disk G，induced 有序外框 B=C5，原完整 Sigma=933/941 或共同整圖 D5 像，
每條非框邊原 Sigma-critical，epsilon=2。有效 H connected、full B-touch，恰兩個不相鄰原 degree5
roots r,s，其餘原有效內點完整 degree4。H 去兩 roots 的原完整分量恰 U/P/Q，U unary at r，
兩 mixed P/Q one-sided 且各有真原框邊 pair support、正的雙側 incidence；所有 support 非空。
LOW2 指兩個不同原 U neighbors x1,x2，兩條 rx1/rx2 都完整留在 X；mixed incidence=(2,3)，
r 對 P/Q 各一條，s 對 P/Q 一條與兩條。原 r 唯一 spoke e=rb_i，原 s 兩 spokes sb_j,sb_k。
只省略 e，指定原拒絕 literal beta 下 X=G-e=M 自己 inclusion-minimal45/54；降度 root 名為 r。
原 contacts、shared 坐標、attachments/support/ownership、bridges/rotation、共同 literal frame、
十列完整 relations／所有 ambient empty fibres／full lifts 都保留；共同 root swap/D5/S4 搬整圖。
不假定 beta 是 U 盾中點，933 q2 保留。完整十二前提另在逐 claim JSON。

唯一刪 e 的兩端為 r 與 B；故 H_X=H_G。原 r 的五條邊是 rx1,rx2,rp_r,rq_r,e，
X 保前四條而無 r-B 邊；原 s 的三 mixed contacts 與兩 spokes 完全保留，degree5。
U/P/Q 每個有效點的原內邊、root 邊、框附件都留，故完整 degree_X=4。
X 是原 disk embedding 的邊刪除子圖；B/rotation 繼承，沒有重新選 embedding。
X 自己 minimal 是契約，不由 G criticality 遺傳。每條 X 非框邊 h 的刪除有完整 beta-lift，
否則 X-h 是仍拒 beta 的真子圖。原忽略孤立內點只作自由四色 full-lift 因子。
這證 LOW2-CORE。

## 2. 真 C 與原 U 迴圈

C=H_X-s 的實際頂點恰 {r} disjoint-union U disjoint-union P disjoint-union Q。
實際全部邊恰三原 pieces 內邊，加 rx1,rx2,rp_r,rq_r；三 pieces 各 connected 並連同一 r，
故 C 唯一 connected，沒有被遺漏分量。U 內任何連接 x1/x2 的路與兩條原 r-U 邊共同形成的
真 cycle 全留；沒有將 U 改成 unit piece、單 contact bridge、star 或 relation replacement。

s 原 rotation 去兩個 B neighbors 得 ordered K=(p1,p2,p3)，三點互異來自簡單性。
r 與 U 沒有 s-contact。若 mixed 的同一點同時被 r/s 接觸，就只用同一頂點同一變數。
令 d_B(v) 是 X 實際框鄰點數，逐邊有
`deg_C(v)=4-d_B(v)-1_[v in K]`。r 的 deg_C=4；其他點不能把 degree_X=4 寫成 degree_C=4。
這證 LOW2-COMP，不需要 LOW1 bridge 假設。

## 3. 任意列完整 join

任意 proper literal gamma，Col={0,1,2,3}。Lambda_T(gamma) 保存 T=U/P/Q 全頂點 assignments，
滿足原全部 T 內邊與 gamma 下 actual B attachments；root 邊在共同 join 才加。
令 c 是同一 r 色；X 沒有 r-spoke，故 c 遍及 Col。以
`f_U(x1)!=c AND f_U(x2)!=c AND f_P(p_r)!=c AND f_Q(q_r)!=c`
接合三份完整 assignments。兩個 U 不等式必在同一份 f_U 上，不能從獨立 marginals 拿兩份 coloring。
限制 C 全 coloring 到 r/U/P/Q 給此 join；反向 union 因跨 pieces 只有已列 r 邊而給原 C coloring。
逐完整 assignment restriction/union 互逆，沒有獨立 piece 換色或共享 port 拆分。

對每個 c in Col 及每個 ambient t in Col^3 定義 Phi_gamma(c,t) 是上述 C 全 lifts 中 r=c、K tuple=t
的 fibre，空 fibre 亦定義；Fib_gamma(t) 是逐 c disjoint union。R_C(gamma) 只是非空 fibre 的支援。
對任意 s-pin a 再加所有 t_i!=a。X full lifts 正是 a 避兩個原 s-spoke 色、上述 C lifts 避 a，
加 B=gamma 與原孤立點自由 factors；G full lifts 在同一 assignment 上再且僅加 `c!=gamma(b_i)`。
這裡 gamma 是一般 literal row，不能寫成 beta 的 spoke 色。所有 pins/tuples/十列/共同整圖色搬運照留。

L_gamma(v)=Col minus gamma(N_B^X(v))。前節精確 degree 式給
`|L_gamma(v)| >= deg_C(v)+1_[v in K]`。C connected，K 三點皆 strict slack；
從其中一點為根、逆 distance 貪婪給完整 C coloring。故 R_C(gamma) 非空；並不要求每個 pinned fibre 非空。
這證 LOW2-JOIN；貪婪論證直接可核，與官方 Lemma7 一致。

## 4. X 自己 minimal 的精確 F

寫 u=beta(b_j)、v=beta(b_k)。若 u=v，刪任何一條 s-spoke 不改 beta lists，仍拒 beta，
違反 X minimal。故 u!=v；A_s=Col minus {u,v} 恰兩色。由完整 join 及 X 拒 beta，A_s subset F_C(beta)。
刪 sb_j 的完整 beta-lift 必令 s=u，否則仍滿足被刪邊、可接回 X。C 完全沒被該刪邊改動，
其限制給一個全 C lift 共同避 u，故 u 不在 F_C。刪 sb_k 同理给 v 不在 F_C。
因而 `F_C(beta)=Col minus {u,v}`，R_C(beta) 非空。沒有搬用 SS 未接框點或 U 盾中點 forcing。
這證 LOW2-F。

## 5. 任意大小 active Gallai 抽取

[真 BASE 三接點](frozen/BASE/docs/c5_two_spoke_three_contacts.md) §§1–5 的角色在 X 中為 z=s、
sole C=H_X-s、三原 ordered contacts K、其他完整 degree4、兩條 beta 異色原 spokes、X 自己 minimal。
該 §5 明允許任何兩個異色 spoke 位置；只共同全圖 S4 命名 u/v 為 0/1，其餘為 2/3。
不交換 boundary 位置，不需要把 gamma/beta singleton 放在 U 中點。外部定理信任來自
[官方 Dvorak Lemma7/Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
[獨立下載 PDF](external/gallai-official.pdf) 與 BASE PDF 同 SHA256；本輪讀完整陳述及證明。
不是 Python/Gallai 本地形式化，也不使用有限 subdivision 樣本代任意長論證。

令 M_a(v)=L_beta(v) minus {a} 當 v in K，其他不變，a=2,3。各是 degree-assignment，
各不可染；connected strict-slack lemma 迫每點 tight。K 的 actual boundary colors避 2/3 且互異；
其他點的 boundary colors也互異。兩 lists 的指示差恰只在 K，為 1_[v in K]*(1_[color=3]-1_[color=2])。
官方 Theorem10 给同一 C 的 Gallai blocks 及兩組 blockwise-uniform palettes；交於同點的 palettes互斥。

vertex-versus-block incidence columns 以 leaf-block 私有頂點逐塊消去而獨立。
對色0/1，vertex差零迫每塊差零；對色2/3，vertex差互負迫每塊差互負。
故任一 block palette 固定或只交換2/3。後者為 active，disjointness 使每點至多各一個正/負 active block。
K 三點 active degree1，其餘 active 點 degree2。真 block incidence tree 限制成 active forest；
每個 block-node 至少2、無孤立點。恰三葉使只有一棵 tree，tree degree identity迫恰一個
三點 active block，其餘二點 active blocks。Gallai 三點 block 是 triangle；二點 block 是 bridge。
因而原 C 中恰一 active triangle 與三條原 bridge arms，終點恰 K，任意長或零長均可，
不同 arms 除 triangle 外不相交。U 的真 cycle 仍屬原 C 的某 block，不是被預設為 active bridge。
沒有 contact 在 inactive structure。

## 6. r 無 B 鄰點仍有 actual tethers；十對 K5 原邊

每個 triangle 點 v_i 用两條 triangle 原邊及一條 arm 首邊；零長 arm 時第三條是原 s-contact。
完整 degree_X=4 剩唯一 actual 邊，若到 B 即 direct tether；否則必進 inactive W_i。
該邊不能在另一本非trivial block（需至少另2邊），故為 bridge；block incidence tree禁止重接
active structure，且不同 W_i 不相交。全部三 s-contacts 已是 arms 終點，故 W_i 不接 s。

若 W_i 無 actual X boundary neighbor，刪 W_i 後 C-W_i connected，原 M_2 lists 不變，
v_i 因少 bridge neighbor 獲 strict slack，故可染。W_i 在 X 沒有 B/s constraints，entry w_i
在 W_i degree3、其他點 degree4，以整份四色 list 為 degree-assignment且entry strict slack，可染。
共同置換這一整份未受外 pin 的 W_i coloring，使 entry 色避 v_i 色，完整接回 C，矛盾 M_2 不可染。
因此 W_i 真碰 X 的 B；即使它含 r，r 無 B 鄰點只會讓這個假定更強，整個反證仍成立。
沒有用已省略 rb_i 當 tether，也沒有在原 relation資料中獨立換 U/P/Q frame。

三條 tethers 可選最先碰 B 的 actual paths，內部避 active structure、互相不交，框端點可重合。
Z={s}；V_i={v_i}加其全原 arm（零長則單點）；O=完整原 B 加三 tethers 的內點。
五 bags 非空 connected且pairwise disjoint；O 因 induced原C5 connected。全部十對 adjacency 如下：

| pairs | 保留的 X 原邊 |
| --- | --- |
| V0-V1、V0-V2、V1-V2 | 三條 triangle 邊 |
| Z-V0、Z-V1、Z-V2 | 三條具名 s-contact 邊，zeroarm也保留 |
| V0-O、V1-O、V2-O | 三條 actual tethers 各離開 V_i 的第一邊 |
| Z-O | 原 sb_j（sb_k亦可） |

省略 e 不在任何 witness；B 只作最後 minor bag，沒有替換 coloring 圖。
這給 X 原邊 K5 minor，違反其原 disk planarity。因此 LOW2-MAP 及 LOW2-EXCLUSION 均成立，
量詞任意大小，未對內點數、cycle 或 arm 長度加上界。

## 7. 另證限定 S-SHORT-U-LOW 覆蓋

composition 輸入為 frozen current authority §1 的**精確 S**：原 e=rb_i 被省略、X=G-e=M，
其餘完整 source 前提及同源十列／full lifts 都保留；且兩原 mixed short。
已採納 [原 S §7](frozen/current/audits/2026-10-09-n45-s/REPORT.md) 的 N45-S-06，
由 [SU-A S06](frozen/current/audits/2026-10-09-n45-su-a/independent-judgment.json) 獨立核過，
給唯一原 unary、mixed incidence在 unary側/另一側為2/3、P/Q真框邊 pair。
限定 LOW 再指 U 與 e 都在降度 r；HIGH 的 U在s身份不在本合成。

令 n 是 U 原 r-contact 數，t 是 r 原spoke數；U作 H-root分量且 unary，n>=1。
簡單圖使 n contacts有不同neighbors；root完整degree5 與兩mixed contacts逐原邊給 `5=2+n+t`。
e 是實際原spoke，故 t>=1。於是 `n+t=3` 只有 (n,t)=(1,2),(2,1)。
s 無unary且有3原mixedcontacts，其degree5另迫2原spokes。不能用後刪圖 support重定 n。

n=1 分支逐滿 [已採LOW1完整契約](frozen/current/audits/2026-10-10-n45-low1-supervision/acceptance.json)：
同一原G共同前提、uniqueUatr、exactrx、mixed(2,3)、兩roots各2spokes、只刪e且X=M、full original data。
n=2 分支逐滿本輪LOW2完整契約：兩不同原rx1/rx2全留、r唯一spokee刪後0、s2spokes，
所有其餘source前提與同源資料相同。n=0違反原U存在，n>=3迫t<=0違反被刪原spoke存在。
root swap只共同把降度側命名r；不能透過swap把HIGH塞進LOW。D5/S4同搬全部資料，933q2保留。
兩分支無缺前提且互斥窮盡，故 accepted LOW1 + LOW2 exclusion 推限定S-SHORT-U-LOW來源為空。

此父 LOW 合成有自己的前提、分支對應與裁決，並未排整個S、任意LOW稱呼、所有spoke derivatives、
非minimal衍生圖、HIGH、long、其他core/原55、一般N2/E或epsilon>=3。未建立 finite source control，
沒有source trigger數、沒有source realization，無新增Lean。

## 8. 封存驗證及保留界線

本 verifier 只讀核 exact manifest、frozen/current/BASE input hashes、claims導航、report本地links、
own authored whitespace及 receipt明綁的實際 normal/seed17 logs；它不機證前述紙面論證。
mutable authority 只在 intake 核當時 pin，再從 frozen copy重播；因此後續正式採納共享文件不會失去可重播性。
舊 worker/shared files 未被本稽核改寫；全部歷史缺檔/whole DocGraph/E4 provenance FAIL 按原交付保留，
本稽核未修、未重跑該全工作樹工具，也未宣称它们通过。官方PDF下载/read-only文字提取另留实际exit。
未建立／未執行 source 控制，沒有trigger數。封存checker成功不給任意大小數學證明。

```bash
python3 -B audits/2026-10-10-n45-l2a/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-l2a/verify.py
```

Closure scope：完整LOW2與另核的§1 S/§3 S-SHORT-U-LOW窮盡合成，等候監督正式採納。
Updated：本專屬audit；Reviewed unchanged：所有shared/old audits；Remaining OPEN：HIGH/long及一般N2/E等上述界線。
沒有commit/push/PR、外部訊息、再委派或新Lean。此报告未读本轮任何peerjudgment。
