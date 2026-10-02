# 共同 repair lemma：完整 witness 與覆蓋的充要條件

**形式化後續（2026-10-02）：** [Lean 共同 repair 判準](lean_common_repair.md)
已補 W／C 與全部 repair 模板的雙向等價、極小／極大失敗分類、完整殘留、
唯一最少解及 P=J 退化支。六圖的前提實例化仍由 Python 證書負責；
下文「未新增 Lean theorem」保留原輪次語境，不表示後續仍無抽象形式化。

**後續（2026-09-30）：** [來源充分條件](c5_two_vertex_repair_sources.md)已從
具名私有接線、十一份構造補全及色數推導 W／C，並以保核心的度數三消去
與外框證書推到任意大小指定來源族；兩原框可用另給退化來源 lemma。
這些是充分條件，未分類全部來源。下文保留抽象 lemma 的原停止點。

2026-09-30。接續[六例 transport audit](c5_two_vertex_repair_transport.md)，
將共同公式抽成一般集合論 lemma；四個 `P=J` 案例保留為獨立退化支。
目前停止點見[兩點重疊導覽](c5_two_vertex_overlap_guide.md)。

本輪證成：在明列的保真條件下，三種 exact-rejector witnesses 與兩類
覆蓋等式，**充要地刻畫**全部 repairs 為 `{A,B}` 或某個 `{A,T,E}` 的
上閉包。因此全部 inclusion-minimal repairs 恰為這些集合。
每例僅三個 witness 就可統一證明所有極小解的逐項不可省性。

一般 lemma 為紙面證明；[checker](../scripts/c5_two_vertex_common_repair.py) 與
[證書](../artifacts/c5_two_vertex_overlap/common_repair.json) 只驗既有六圖的前提，
不把圖樣相似當來源結構定理。未新增 Lean theorem、`native_decide` 或外部定理。

## 1. 模型及完整前提

令 Ω 為同一份具名配置的全集，`J⊆P⊆Ω`；J 是目標完整 relation，
P 是固定基底。令 Λ 為有限的候選條件索引集，各索引 λ 有接受集合
`K_λ⊆Ω`，且滿足**保真性** `J⊆K_λ`。定義

\[
\Delta=P\setminus J,\qquad F_\lambda=\Delta\setminus K_\lambda,
\qquad \rho(x)=\{\lambda\in\Lambda:x\in F_\lambda\},
\]
\[
R(H)=P\cap\bigcap_{\lambda\in H}K_\lambda
\quad(H\subseteq\Lambda),\qquad R(\varnothing)=P.
\]

H 是 repair 指 `R(H)=J`；是 inclusion-minimal repair 指刪除任何一項
都不再是 repair。保真性給出基本等價式

\[
R(H)=J\iff\bigcup_{\lambda\in H}F_\lambda=\Delta.
\tag{1}
\]

這裡使用完整集合，不是排除數量、pair marginals 或彼此獨立換色後的資料。
若某個 `K_λ` 刪掉 J 中的 row，右式仍可能成立而左式失敗，故保真性不能省。
Ω、P、J 不要求有限；Λ 有限用於將「所有 repairs」與「全部極小 repairs」互換。

非退化支另選互異的 `A,B,T∈Λ`，以及非空
`𝓔⊆Λ\{A,B,T}`。索引集 Λ 可以含任意其他條件，不預設它們的排除集合大小
或彼此包含關係。要求以下五條前提：

| 前提 | 完整敘述 |
| --- | --- |
| W_A | 存在 `x_A∈Δ`，`ρ(x_A)={A}` |
| W_BT | 存在 `x_BT∈Δ`，`ρ(x_BT)={B,T}` |
| W_BE | 存在 `x_BE∈Δ`，`ρ(x_BE)={B}∪𝓔` |
| C_AB | `F_A∪F_B=Δ` |
| C_ATE | 對**每個** `E∈𝓔`，`F_A∪F_T∪F_E=Δ` |

Witness 的 rejector 集合相對於**全部 Λ** 精確相等。只驗其在指定 repair
中被誰拒絕，或只說某個 scope 拒絕它，不足以排除其他 repair。

## 2. 共同 repair lemma 及證明

**Lemma。** 在 §1 的模型與角色前提下，五條 W／C 前提等價於：對每個
`H⊆Λ`，

\[
R(H)=J\iff
\{A,B\}\subseteq H\quad\text{或}\quad
\exists E\in\mathcal E,\ \{A,T,E\}\subseteq H.
\tag{2}
\]

**充分性。** 若 H 修復，W_A 迫使 `A∈H`。若 `B∈H`，即含 `{A,B}`。
若 `B∉H`，W_BT 迫使 `T∈H`，W_BE 再迫使某個 `E∈𝓔∩H`，故含
`{A,T,E}`。反之，C_AB、C_ATE 與 (1) 證明兩類集合都修復；保真性使加入
其他條件仍保留 J，因此所有包含它們的 H 也修復。∎

此證明沒有枚舉 `2^|Λ|` 個子集合，也未先將其他 scopes 丟棄。
它解釋為何完整資料中的小排除類、空排除類不會產生其他極小解。

**必要性。** 假設 (2)。先取 H 為 `{A,B}` 及每個 `{A,T,E}`，由 (1)
得到兩類覆蓋等式。再取下列三個集合：

\[
M_A=\Lambda\setminus\{A\},\quad
M_{BT}=\Lambda\setminus\{B,T\},\quad
M_{BE}=\Lambda\setminus(\{B\}\cup\mathcal E).
\tag{3}
\]

它們都不含 (2) 的任何模板，故各有一個 `x∈R(M)\setminus J`。
該 x 的 rejectors 只能在 M 的補集中；再由覆蓋等式補足精確相等：

- 對 M_A，C_AB 迫使 x 被 A 拒絕，得到 `ρ(x)={A}`。
- 對 M_BT，C_AB 迫使 B 拒絕 x；任選一個 `E∈𝓔`，C_ATE 迫使 T 拒絕 x。
- 對 M_BE，C_AB 迫使 B 拒絕 x；逐個 E 套 C_ATE，迫使**全部 E** 都拒絕 x。

因此三個 exact witnesses 都存在。非空 𝓔 與角色互異在此確實使用。∎

等價地，(3) 是全部 **inclusion-maximal 非 repair**：對不修復的 H，
若缺 A 則包含於 M_A；否則 H 必缺 B，並且缺 T 或缺全部 𝓔，分別包含於
M_BT 或 M_BE。向三個 M 任加一個缺項就含模板，故都極大。
在五條前提下更有完整殘留等式

\[
R(M_X)\setminus J=\{x\in\Delta:\rho(x)=\Lambda\setminus M_X\}.
\tag{4}
\]

所以 witness 前提也可用三個明確的非空殘留集合表達；只驗這三份非空
而未驗覆蓋，仍不足以推出 (2)。

## 3. 極小性、唯一 forced scope 及退化支

由角色互異，`{A,B}` 和各個 `{A,T,E}` 彼此均不包含。
(2) 因而給出全部極小修復，共 `1+|𝓔|` 組；最少份數恰為二，唯一
minimum repair 為 `{A,B}`；所有極小 repairs 的交集恰為 `{A}`。
有限 Λ 也保證每個 repair 都含一個極小 repair，故這份極小分類反過來
蘊含 (2)，再由 §2 推出 W／C 前提。

三個 witnesses 可重用於所有逐項刪除：

| 極小 repair | 刪除項 | 通過其餘全部條件的殘留 witness |
| --- | --- | --- |
| `{A,B}` 或 `{A,T,E}` | A | x_A |
| `{A,B}` | B | x_BT |
| `{A,T,E}` | T | x_BT |
| `{A,T,E}` | E | x_BE |

這是**刪掉一項後仍不能修復的見證**，不是對每個錯誤 row 給出同圖換色
操作，也不保證不同來源圖的完整刪除殘留相同。

**獨立退化 lemma。** 若 `P=J` 且全部條件保真，則每個 `H⊆Λ` 都修復，
唯一 inclusion-minimal repair 為 `∅`，無 forced scope；空集合已修復。
此時 `Δ=∅`，三個 W 前提不成立，不套用非退化 lemma 或虛設 A/B/T。
對 arity ladder 而言直接有 `r*=0`。

## 4. 六份原圖的實例化

沿用[transport audit](c5_two_vertex_repair_transport.md)的原圖、原 U、
原內點／邊、接點雙射與共同色框 `D={0,1,2,3}`：

\[
\Omega=D^U,\quad
J=\{u:u\text{ 延拓至同一原接合圖}\},\quad
P=\bigcap_{C\in\mathcal C}\pi_C^{-1}(\pi_CJ).
\]

𝓒 恰為原 U 上可作**整張原圖 disk 外界**的全部 C₅。每個框的 relation
都由完整 J 投影；基底只有 P。兩個非平凡例取全部七十個四點 scopes 為 Λ，
`K_S=π_S⁻¹(π_SJ)`，保真性自動成立。不同 scope 的接受延拓可以不同，
不能拼接成一份八點延拓。

```text
U = (a0,a1,a2,a3,a4,b0,b2,b4)
A = (a0,a1,a2,a3)
T = (a0,a2,b0,b2)
B_forward = (a0,b0,b2,b4)
B_reverse = (a2,b0,b2,b4)
𝓔 = {S⊆U : |S|=4, {b2,b4}⊆S} ∖ {B}
```

每例 `|𝓔|=14`，`|J|=1,440`、`|P|=2,736`、`|Δ|=1,296`，即
60／114／54 個全域 S₄ 軌道。具名 witnesses 與三個完整殘留如下；pattern
依原 U 次序，不在兩例間重命名。

| 角色 | 正向 witness | 反向 witness | 正向／反向 `R(M)\J` 軌道數 |
| --- | --- | --- | ---: |
| W_A | `01232113` | `01232112` | 4／4 |
| W_BT | `01201130` | `01212132` | 4／2 |
| W_BE | `01012122` | `01012122` | 26／26 |

新 checker 先重建原 J 與 P，再由原 U 的具名角色檢查前提；不先讀既有
`structure` 或極小解答案來推論角色。它逐 tuple 驗全部七十份投影與
rejector 集合，重播六個 witness 的 **384 份**接受 scope 原圖染色，
以及 **12 份**分別 frame 延拓。每份接受染色都核對所有原邊及指定 scope
上的同色框相等；完整八點不延拓則由原圖窮盡關係排除。

每例另驗十五份完整覆蓋等式與修復後 relation 恰等於 J；前提通過後才
比對前輪全部十五組答案。每例三個固定 witnesses 統一驗證44次逐項刪除，
兩例共 **88 次**。三個極大失敗集合的完整殘留亦無損保存，並逐項驗證
任添一個缺項即完成覆蓋。共同 lemma 不要求兩例的排除集相同；上表的
4／2 差異仍保留，也不推論原圖、J、P 或排除資料可由頂點雙射搬運。

四個退化案例為 `reference`、`reference_reverse`、`free_pairs`、
`shared_chord_frame_edge`。新 checker 分別重建 J/P 並驗完整集合相等，
記錄各自唯一空 repair、無 forced scope、`r*=0`。不加非空 witness 前提。

非平凡兩例的 `r*=4` 仍依前輪獨立的三點下界與四點充分性證書。
**共同 lemma 本身不推出四點 arity 下界**，也不預設 Λ 必為投影條件。

## 5. 五條前提的獨立性控制

為分清「缺 witness」與「缺覆蓋」，用五個抽象索引 `A,B,T,E₁,E₂`，
先取三個 row 的 rejectors 為 `{A}`、`{B,T}`、`{B,E₁,E₂}`。
這可實現為保真集合系統：令 `J={j}`、`P=J∪Δ`，各條件接受 j 及未被拒絕的 rows。

| 單獨刪去的前提 | 修改 | 其餘前提成立時的失敗 |
| --- | --- | --- |
| W_A | 刪第一個 row | `{B}` 已修復，不迫 A |
| W_BT | 刪第二個 row | `{A,E₁}` 已修復，不迫 T |
| W_BE | 刪第三個 row | `{A,T}` 已修復，不迫任何 E |
| C_AB | 加 rejectors 恰為 `{T,E₁,E₂}` 的 row | `{A,B}` 不修復 |
| C_ATE 的 E₂ 一項 | 加 rejectors 恰為 `{B,E₁}` 的 row | `{A,T,E₂}` 不修復，但 E₁ 的覆蓋仍成立 |

Checker 對每個小模型驗其餘四條成立、指定一條失敗，枚舉32個子集合
確認極小解家族不同，且前提 verifier 確實拒絕。它們是一般集合 lemma 的
前提獨立性控制，**未宣稱可實現為 C₅ disk 圖或四點投影系統**。

## 6. 重播、證據界線與下一個窄問題

新[證書](../artifacts/c5_two_vertex_overlap/common_repair.json)以 SHA-256
綁定來源 audit、原接合、框證書、來源 cells 與所用程式；關係仍以完整全域
S₄ 軌道無損保存，運算均用具名 tuples。檔案小於1 MB，直接保存。
`--check` 重算並逐 byte 比對，不改寫來源或輸出。

```bash
python3 scripts/c5_two_vertex_common_repair.py
python3 scripts/c5_two_vertex_common_repair.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_common_repair.py --check
python3 scripts/c5_two_vertex_repair_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證及沿用範圍見[本輪紀錄](history/2026-09-30-c5-two-vertex-common-repair.md)。
README／HANDOFF 依[文件治理](DOCUMENTATION.md)維持既有研究線入口。

**停止點：抽象分類充要 lemma 與既有六圖的前提實例化已完成。**
下一個圖論窄題是找到可檢查的**來源結構**，在指定原圖／共同色框下保證
W_A、W_BT、W_BE 及兩類完整覆蓋；不能以共同公式、相同軌道數或缺邊 family
名稱代替這些證明。沒有證明任意 class pair 皆落在這兩支，也未新增 class-pair
枚舉。一般後繼表、輔助變數、指定 disk 重疊政策、多步摘要充分性、完整 Σ、
一般共同出口及 `K∞=K≤5` 仍保留。
