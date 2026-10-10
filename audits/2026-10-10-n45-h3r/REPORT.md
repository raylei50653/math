# N45-H3R：原圖、完整關係及 lifts 獨立裁決

日期：2026-10-10。BASE `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。
此交付是候選，監督尚未採納。完整量詞限於
[共同契約 K1–K13](frozen/routing/common-contract.md)；
[任務](frozen/routing/n45-h3r-task.md)與[輸入 pins](input-index.json)皆已凍結。
8 current pins、6 BASE blobs、管理端及本端 frozen 副本全一致。

裁決：七項 claim 在完整 K1–K13 內成立，無新增充分前提，未找到此限定映射的 gap。
任意大小 HIGH3 排除由以下原圖論證與指定 BASE paper／外部 Gallai 信任承擔。
本端不採納 HIGH3，不提升為全部 HIGH、全部 S、其他 45/54 身份、一般 N2／E 或核心存在性。
結構化量詞、前提使用及精確殘留見 [independent-judgment.json](independent-judgment.json)。

## 1. CORE 與實際 COMPONENT

K10 明示 X=G−e=M 自己是原拒絕 literal β 的 inclusion-minimal core。
因此 X 拒絕 β，且每條 X 中的非框邊 h 都有 X−h 的完整 β-lift。
此處沒有從原 G 的 Σ-criticality 推出 X minimality。
K4/K9/K11 給 r 在 X 完整 degree4，s 完整 degree5，其餘有效原內點完整 degree4。
X 繼承原 disk embedding、有序 induced B，且 H_X=H_G；原孤立內點 I 全留。

K5/K7/K8 給 H_X−s 恰兩個實際分量：

- C={r}∪P∪Q：P/Q 原 connected 且各與 r 有正 incidence，所以 C connected。
  s 的接點依原順序記 (y_P,y_Q)，兩點因 P/Q 原分量相異而相異。
- U：完整原 connected U；s 的接點為原 (x1,x2,x3)，三點相異。
  U 無 r 邊，也無通往 P/Q 的邊，所以保持另一完整分量。

故實際 contact 分拆為 (2,3)，五點互異，N_B^X(s)=∅；不是抽象重分組。
P/Q 的每條實際附件、同一 piece 內 r/s 共鄰點、原 ownership、bridges、rotation 皆留。
例如 r/s 共鄰的 y_P 仍只有一個原頂點變量，不能各給一個獨立顏色。
C 仍含原 rb_j；原 U 的全部頂點、三 contacts、內邊及所有附件全留。

## 2. JOIN 與 RESTORE：完整量詞與空 fibres

令 Col={0,1,2,3}。對每個 proper literal γ:B→Col，取
L_γ(v)=Col−γ(N_B^X(v))，並保留原具名頂點作所有 assignment 的坐標。
對 T=P,Q,U，A_T(γ) 是 T 的全部 proper boundary-list assignments，
包括每條實際 T 內邊及全部原框附件，沒有對接點逐一存在量化。
記 P/Q 的原 r-neighbor 集為 D_P,D_Q；同一頂點可同時屬 D_T 與 {y_T}。

對全部 a∈Col、t=(t_P,t_Q)∈Col²，定義完整 r-color fibre

```
Φ_C^γ(a,t) = {(f_P,f_Q): f_T∈A_T(γ), f_T(y_T)=t_T,
             f_T(v)≠a for every v∈D_T, T=P,Q,
             a≠γ(b_j)}.
```

它精確代表 C 的完整 coloring，r=a。無效 r-pin 或不可實現 tuple 的 fibre 定義為空。
R_C(γ)={t: 存在 a 使 Φ_C^γ(a,t) 非空}，但仍保存每個 a 的全部 assignments。
對全部 u=(u1,u2,u3)∈Col³ 定義
Φ_U^γ(u)={f_U∈A_U(γ): f_U(xk)=uk，k=1,2,3}；R_U(γ) 是其非空支援。
Φ_U 保持同一完整 f_U 同時滿足三個 contact 約束。

再對全部 a,d∈Col、t∈Col²、u∈Col³、ζ∈Col^I 定義

```
J_γ(a,d,t,u,ζ) = Φ_C^γ(a,t) × Φ_U^γ(u) × {ζ}
                if d∉set(t)∪set(u), otherwise ∅.
```

將同一 pair (f_P,f_Q)、同一 f_U、r=a、s=d、原孤立點 ζ 與 boundary γ union，
就是 X 的完整 lift。逆映射是對原頂點集的 restriction。
piece 間唯一連接在 r/s，且 rs 不存在；所有這些不等式已逐條列出，所以兩映射互逆。
因此對每個 literal γ、所有 r/s pins、全部 ambient tuples／free factors，
J 與 X 的完整 lifts 逐 fibre 雙射，包括空 fibres。
十個 canonical rows 只是共同 S4 搬運整列後的索引；從未獨立正規化 pieces。

恢復 G 恰加回原 e=rb_i，故同一完整 fibre 只再施加 a≠γ(b_i)。
這是 RESTORE 的全部差異；不丟 r 投影，不將 X 的某份延拓宣稱是 G 延拓。
原 G、X、各 X−h 的原邊與 lifts 始終分明。

## 3. F：slack、覆蓋及逐 incident-edge 的完整 witnesses

對 D=C,U，令 P_D 為其上述有序 s-contacts。
在所有 proper γ 下，D 每點在 X 完整 degree4，且 D 外鄰只有 B 及 s。
因此 |L_γ(v)|≥deg_D(v)+1_(v∈P_D)；contacts 非空且 D connected。
以其中一個 slack 點為生成樹根，從葉至根貪婪著色，給 R_C(γ)、R_U(γ) 非空。
此證允許 boundary 同色鄰居，沒有先對 γ 假定 minimality。

定義 F_D(γ)=交集_{w∈R_D(γ)} set(w)。非空 relation 立即给
|F_C(γ)|≤2、|F_U(γ)|≤3。
F 只對共同 s 色須避開全部 contacts 的接合是精確投影，並非完整 R/fibres 的可逆替代。

現在僅固定 K10 的拒絕 β。因 s 無 spoke，JOIN 给 X 的可延拓 s 色恰為
Col−(F_C(β)∪F_U(β))。X 拒絕 β，故 F_C∪F_U=Col。

令 E_D 為 X 中至少一端在 D 的全部非框邊。
對每個 h∈E_C，X 自己 minimality 給完整 ψ_h∈Lift_β(X−h)。
令 d_h=ψ_h(s)。原 U 的全部邊與三條 s-contact 沒有被 h 觸碰，
故 ψ_h 的 U restriction 是同一原 U 的完整 assignment，避開 d_h。
所以 d_h∉F_U；由剛證的覆蓋得 d_h∈F_C−F_U。
同理每個 h∈E_U 的完整 witness 給 d_h∈F_U−F_C。
這對全部 incident edges 成立，不只某個代表；兩 private sets 皆非空。

特別當 h=sw 是其中一條原 contact，ψ_h(s)=ψ_h(w)，否則 ψ_h 已是 X lift，
與 β 拒絕矛盾。其他四條 contacts 都保持不等式；ψ_h(r) 保留 rb_j 條件。
這些是 X−h 的完整 witnesses，不施加省略 rb_i，不假裝是原 G−h 的 lifts。
沒有實際 HIGH3 source 被提供，所以此 witness 結論是 K10 的存在量詞，沒有數值來源證書。

由 4=|F_C∪F_U|≤|F_C|+|F_U| 及 |F_C|≤2，得 |F_U|≥2。
沒有指定哪個禁色給 C 或 U，也沒有把三 contact U 套成 HIGH1 單 contact 的容量一。
抽象不可刪減 covers 可有大小 (1,3)、(2,2)、(2,3)，所以此處也不先假定兩者各二。

## 4. MAP 與限定 HIGH3 結論

完整 mask 933／941 都接受 T4={2,5,7,8,9}；所有原拒絕 β 為三色 proper C5 literal。
每份這種 literal 的 singleton 位置可由一次共同整圖 rotation 送到 b4，
再由一次全局 S4 將兩重色送到 0/1、singleton 色送到 2，得到 q=01012。
此操作同時搬 G、X、r/s、全部原頂點／邊、contacts、pins、relations、fibres、lifts。
它不預設 β 是 U 盾中點；933 的 q2 沒有漏掉，也不要求搬後 Σ 仍用未搬的數字標籤。

令 BASE 文中的 G=X、z=s，分量為實際 U（三 contacts）及 C（兩 contacts）。
X 自己 edge-minimal q obstruction、唯一完整 degree5 s 無 spoke、其餘有效內點完整 degree4、
H_X connected、原 disk／induced C5、五個原 contacts、有序完整關係，逐項滿足
[BASE no-spoke exterior §1](frozen/base/docs/c5_no_spoke_exterior.md)。
F 覆蓋／private 已從 X 自己 witnesses 核回，而不是先假設 BASE 的角色正常形。

U 外有真實 s–B 路徑：先用原 sy_P，沿原 connected C 到 r，再用保留 rb_j。
所以 [BASE §§2–3](frozen/base/docs/c5_no_spoke_exterior.md) 的外部 hub／K4 排除適用。
U 的三原 contacts 及 |F_U|≥2，恰接回該頁 §5 的三 contact 兩禁色排除，
其 (3,2) 表列就是本端具名 (C,U)=(2,3)，只交換列示順序而未改圖。
§5 用同一 U 的兩份拒絕 palettes、active triangle／原 arms／實際 tethers，
外部 C 路徑只作 K5 hub；不把 C 併進 U coloring relation，也不重寫原來源。
因此完整 K1–K13 的 HIGH3 source 不存在。

任意大小信任鏈為上述直接 proof，加
[BASE interfaces §§1–4](frozen/base/docs/c5_degree5_interfaces.md)、
[BASE no-spoke exterior §§1–3、§5](frozen/base/docs/c5_no_spoke_exterior.md)、
[BASE three-one §§2–3](frozen/base/docs/c5_single_spoke_three_one.md)。
外部 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
用於 degree-list tightness 與同一 Gallai tree 的 block palettes，原 PDF 已獨立核讀，
凍結 [PDF](frozen/external/gallai.pdf) SHA256 為
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`。
標準 K5 minor 的非平面性亦列為數學信任。Python 與 Lean 未證這些任意大小步驟。

## 5. 輕量控制、custody 與精確停止點

[verify.py](verify.py) 只讀核十四份權威 pins、manager/local freezes、完整本端 immutable manifest、
authored Markdown links／whitespace、結構化裁決，以及[抽象／toy 證書](abstract-toy-certificate.json)。
只用一張固定代數 toy，直接枚舉全部 240 proper literals 的完整 assignments，
比對 C 雙 contact／r fibres、U 三 contact assignments、全部 r/s pins、
所有 ambient 空／非空 fibres、兩個 shared r/s contact 單坐標及一個原孤立自由點。
另直接比對 G lifts 等於 X lifts 加 r≠γ(b_i)，含被恢復邊實際擋掉的 toy lifts。
該 toy 不聲稱 disk、Σ933／941、critical 或 β-minimal，絕非來源正控制。
抽象 cover 算術與整列 q transport 都標 `triggered and holds`；
marginal 錯接命題標 `counterexample`。逐項分類見 [controls.json](controls.json)。
完整 HIGH3 finite source 未建立／未執行，標 `not triggered`，trigger_count=null。

實際只讀 replay 命令、stdout／stderr／exit 及 manifest 綁定保存在 top-level
receipts.json；normal 與 `PYTHONHASHSEED=17` 必逐 bytes 一致。

```
python3 -B audits/2026-10-10-n45-h3r/verify.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-h3r/verify.py
python3 -B audits/2026-10-10-n45-h3r/verify.py --negative
```

負控制只在記憶體破壞算術證書，不改凍結檔，預期 exit2。
immutable manifest 精確排除僅 top-level manifest.json、delivery.json、receipts.json；
nested 同名檔不排除。metadata 綁 manifest/payload hashes；verifier 不自行写證書。
lake build、whole-worktree inventory／DocGraph、無關枚舉與舊全量研究 checker 均未跑。
歷史缺檔、E4 provenance 及已知 62 duplicate-ID DocGraph FAIL 保留，未為本端核對修 shared 或刪 scratch。

本端停於候選 HIGH3 完整契約的任意大小 paper 排除及實際完整 relation 映射。
未新增有限來源、source realizability 或 Lean；HIGH2 在製內容未讀，其他 HIGH／long／N2／E 保留。
無 shared edits、舊 audit 改寫、commit、push、PR、外部訊息或再委派。
