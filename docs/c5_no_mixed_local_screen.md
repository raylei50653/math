# No-mixed 統一局部篩選：禁色增長、原端點與整條路徑交換

後續（2026-09-29）：[增長完備性與共同分離](c5_no_mixed_growth_completion.md)
已從三個共同側弧位置直接指定排除配方，免查必要支援表地排除影響 R
的增長；結合無增長定理完成指定 p₁、p₂ 的存在性分離。下文未解描述
保留當輪語境；逐染色建構式 repair、完整 Σ 與一般出口仍未證。

後續（2026-09-29）：[無增長短側引理](c5_no_mixed_no_growth.md) 已用共同側弧、
單現框點與支援色穩定子，免查必要表地排除無增長時的同 singleton。
下文 §2、§5 對該缺口的描述保留本輪語境；有增長時的局部排除完備性
仍未免表證成。7,848 個無增長 joins 由新 checker 重播，沒有新增接受。

2026-09-29，基準 `3174f08`。沿用[逐 root 精確介面](c5_no_mixed_hypothesis_audit.md#32-搬運後每側至多一份未知的精確介面)
與七類保留必要支援，將跨列檢查統一成 **singleton→pair 的局部排除，
再接合原 root 色**。規則本身不按 AA／AB 等家族分支；有限覆蓋仍依
既有必要支援表，尚未給免表的共同 repair 證明。

新 [checker](../scripts/c5_no_mixed_local_screen.py) 重算 2,240 個局部增長
候選，排除 2,208 個；剩下 32 個 pair 都與其 root 的 R_r 不交，不影響
可用色。11,096 個完整候選 joins 中，3,216 個含已排除局部 pair，
其餘 7,880 個全部有異色 root pair。原 434 個失敗 joins 全部重新取得
排除；**沒有新增 target 接受或 source 排除**。

證據為條件式紙面引理及 Python 必要表覆蓋；沿用外部 degree-list／
Gallai 結構，未新增 Lean theorem 或 `native_decide`。未證 disk 實現、
完整 Σ、一般共同出口或 `K∞=K≤5`。目前入口見
[weak-deletion 導覽](c5_weak_deletion_guide.md)，當輪驗證見
[研究紀錄](history/2026-09-29-no-mixed-local-screen.md)。

## 1. 完整前提與候選語義

完整沿用[跨度報告 §1](c5_no_mixed_span_budget.md#1-適用前提與精確語義)：
M 為有限簡單圖，induced C5 的 B=(b0,…,b4) 是 disk 外框，M−B 非空
連通；q=01012 拒絕，刪任一非框邊後接受 q。恰有相鄰 z,w 完整 degree=5，
其餘內點完整 degree=4；H−{z,w} 每份原分量只接一個 root。四色
U={0,1,2,3}，target p₁=01021、p₂=01212。不需 T4，不假設來源接受
其他列，不限制原分量大小。

保留同一原分量、具名接點、全部 bridges／旁支、actual supports、
原 spokes／zw、共同環序及字面色框。T_C(β) 為完整有序接點關係，
F_C(β)=⋂_{τ∈T_C(β)}set(τ)，不能換成 endpoint marginals。
沿用 source 必要式 m+s+a≤5 及逐 root 搬運界：每側至多一份不可搬運
C_r；搬運其他完整關係後，

\[
E_r(p)=R_r(p)\setminus F_{C_r}(p),
\]

沒有不可搬運分量時 E_r=R_r。延拓恰當
(E_z×E_w)∖Δ 非空。R 的代數吸收沒有刪去外部原分量路徑。

候選域獨立重建：有相容色置換時使用精確搬運像；否則使用
|F_C(p)|≤接點數及 target 支援逐色穩定子保持 F 的全部子集。
每個 record 的具名 F tuple Cartesian product 與原 11,096 個 joins
完全相等；不以某個候選可延拓代替真實完整關係的延拓。

本文「增長」專指原二接點分量 F_C(q)={d} 而候選 F_C(p)=D 為 pair。
它必不可搬運；source 已為 pair 的分量不算增長。所有保存的支援、
完整 schemas 與共同 placements 都是必要資料，沒有宣稱可實現。

## 2. 容量引理及不影響 R 的增長

**紙面容量引理。** 在上述 no-mixed source，若某側所有分量皆滿足
|F_C(p)|≤|F_C(q)|，則 E_r(p) 非空。

證明：沿用 source O_r=0、E_r(q) singleton，spokes 與各 source 禁色
互不重疊，故 t_r+Σ|F_C(q)|=3。Target 的 spoke 色數至多 t_r，聯集
禁色大小至多 t_r+Σ|F_C(p)|≤3；四色中至少剩一色。證畢。
因此**空 root 必有增長**；各分量接點數至多二，唯一可能的容量增長
即 singleton→pair。這未排除 E_z=E_w={a}，不能只靠容量聲稱 p 延拓。

兩側抽象禁色聯集都為 {0,1,2} 時，兩側 E 都為 {3}；這是容量論證
不能排除同 singleton 的負控制，不是符合 target 支援的 disk 反例。
本輪另外逐筆驗證 **7,848 個無增長 joins 全有異色 pair**；這一結論
仍屬必要表依賴，尚未由共同支援幾何直接證成。

**紙面充分條件。** 若只有 r 側有未知 C，|R_r|≥2、R_{r′} 非空，且
F_C(p)∩R_r=∅，則 p 延拓。因 E_r=R_r 至少二色、E_{r′}=R_{r′} 非空，
可挑不同顏色。此條件不要求 F_C(p) 不增長。

本輪 32 個未被局部規則排除的增長候選全滿足此條件：只有一份未知，
|R_r|=2，另一側 R_{r′}={3}，D∩R_r=∅。分 AA20、AB12，全部保留。
例如 AA5/p₂ 的 Cw 有 S=1234、source d=0、D={1,2}，
R_w={0,3}、R_z={3}，可取 (z,w)=(3,0)；AB98/p₁ 的 Cz 有
S=0124、d=1、D={0,1}，R_z={2,3}、R_w={3}，可取 (2,3)。
這是必要候選上的充分條件，**既不證這些 pair 可實現，也不證它們
不可能**；無需強化成「所有 singleton 永不增長」。

## 3. 同一局部規則的兩個分支

固定原二接點 C，F_C(q)={d}，反設 F_C(p)=D 為 pair。
沿用[原路徑引理](c5_adjacent_degree5_no_mixed_t2_path_palettes.md#1-前提與同一原路徑)：
兩原接點間有奇數長 bridge 路徑 P=x₀…xℓ；刪全部 P 邊後的 W_j
保留所有旁支及實際支援 T_j⊆S_C。局部 residual L_j 尚未扣 root 色，
target 下均為 D；它與完整 F_C、root residual E_r 是不同對象。

令 K={a:∀i∈S_C，q_i=a iff p_i=a}；以 𝒯(s,S,R) 記所有 T⊆S，
使逐色固定 s(T) 的置換皆保持 R。Rooted palette 唯一性及固定色歸納
沿用[旁支引理](c5_single_spoke_branch_palettes.md#2-rooted-palette-唯一性與固定色守恆)。

### 3.1 d 守恆：逐奇數 bridge 排除，再交換整條路徑

d∈K 時，若 d∉D，原端點 tightness 與固定色歸納已矛盾。否則每條
奇數原 bridge 的兩端 q residual 為同一 {d,β}；偶數 bridge palette
為 {d}。對每個符合 {d,β}∩K=D∩K 的 β≠d，兩端的實際支援都屬

\[
\mathcal T_\beta=
\mathcal T(q,S_C,\{d,\beta\})\cap\mathcal T(p,S_C,D).
\]

空族排除該 β；非空時，若存在**同一份**連通三框弧 B=X⊔Y⊔D_B，
所有 T∈𝒯_β 都碰 X、Y，且有避開 C、B 內部的原 root–B 路徑落在
D_B，就用原相鄰 W、其餘原 P、原外部路徑及固定框弧取得 K5。
不可為不同 T 換不同分割；外部路徑可能經另一原分量，不能刪除它。

若所有 β 排除，P 不可能；若只剩 b，全部奇數 bridge 用 b，偶數用 d。
[全路徑交換引理](c5_adjacent_degree5_no_mixed_t2_path_palettes.md#3-唯一剩餘-β-迫使第二個-source-禁色)
保持全部旁支 palettes，只交換 P 邊的 d/b，建立同一原 C 在 root=b
時的完整拒絕證書，推出 b∈F_C(q)，與 F_C(q)={d} 矛盾。
這沿用 Gallai 定理充分方向；不把局部 residual 直接當成完整 F。

### 3.2 d 不守恆：合併所有端點 β，固定一次框弧

d∉K 時不使用上面的全路徑交替推論。沿用
[原雙端點 tightness](c5_adjacent_degree5_no_mixed_t2_t1_endpoints.md#1-同一來源完整接合與原雙端點)，
只有兩個**原端點**必有 L₀^q={d,β₀}、Lℓ^q={d,βℓ}。
不設 β₀=βℓ，也不對下一個內點套此等式。兩端實際支援均屬

\[
\mathcal E=\bigcup_{\substack{\beta\ne d\\
 \{d,\beta\}\cap K=D\cap K}}\mathcal T_\beta.
\]

若 𝒠 空則端點不存在。否則必須對**整個聯集**找同一份 X、Y、D_B
及原外部路徑 L，而非各 β 分別選框弧。所有 T∈𝒠 都碰 X、Y 時，
原圖 branch sets

\[
\bigcup_{j=0}^{\ell-1}W_j,\quad W_\ell,\quad
V(L)\cup D_B,\quad X,\quad Y
\]

兩兩不交、各自連通，原 bridges、兩 contact 邊、實際附件與三框弧
切口給十鄰接，矛盾於平面性。整段中間原路徑保留；ℓ=1 同樣適用。
這是既有任意大小端點引理，局部規則不需要先假設整張 M 拒絕 p。

## 4. 全域覆蓋與精確計數

同一套規則對所有 singleton→pair 上界候選執行，包括已具有 root pair
的 joins；不讀取原七類證書的 `eliminated` 或 final acceptance 來決定結果。

| 局部候選分類 | 數量 | 本輪規則 |
| --- | ---: | --- |
| d 守恆但 d∉D | 890 | 端點固定色矛盾 |
| d 守恆、全部 β 排除 | 850 | 空族或逐奇數 bridge 固定框弧 |
| d 守恆、剩唯一 β | 40 | 整條原路徑 palette 交換 |
| d 不守恆、端點聯集排除 | 428 | 同一端點聯集與固定框弧 |
| d 不守恆、局部規則未排除 | 32 | D∩R_r=∅ 的充分條件 |
| 合計 | 2,240 | 2,208 排除、32 保留 |

前 1,780 個守恆候選重算得到與前輪相同的 890/850/40；未使用其
保存的判定值。本輪補齊 460 個非守恆候選的同一局部篩選，其中
428 排除、32 保留。這些是 record×target×具名分量×pair，非來源圖。

| 家族 | 全部 joins | 含已排除局部 pair | 保留且有 root pair | 原失敗：守恆／非守恆規則 |
| --- | ---: | ---: | ---: | ---: |
| AA | 2,892 | 1,372 | 1,520 | 80／80 |
| AB | 3,148 | 996 | 2,152 | 68／78 |
| AC | 640 | 176 | 464 | 8／0 |
| AE | 336 | 48 | 288 | 0／0 |
| BB | 3,504 | 624 | 2,880 | 48／72 |
| BC | 288 | 0 | 288 | 0／0 |
| BE | 288 | 0 | 288 | 0／0 |
| 合計 | 11,096 | 3,216 | 7,880 | 204／230 |

204/230 以「有守恆排除則先歸守恆，否則歸非守恆」形成互斥分組。
剩下 230 個原失敗全為恰一側空；58 個同 singleton 失敗均被守恆規則
涵蓋。AA54/p₁/j4 保留全路徑交換，AB22/p₂/j4 保留非守恆原端點，
新證書 `controls` 明列它們的 local-rule IDs。

3,216 個被篩掉的 joins 中，只有 434 個原本沒有 root pair；另外
2,782 個原先有 pair，仍可因局部 F 不可能而移除。這是在收緊 target
上界域，**不是 3,216 個來源排除，也不是新增延拓**。7,880=7,848 個
無增長 joins＋32 個不影響 R 的增長 joins。

結合既有任意大小必要覆蓋與 §3 條件引理，真實 F tuple 必落在此域，
不能包含已排除的局部 pair；每個保留 tuple 都有原 root pair，故仍得
全部指定 p₁、p₂ 延拓。這重建既有結論，並將七類的 target 處理統一為
同一局部規則；source 支援覆蓋、無增長相容性及局部規則的全表成功
仍依有限證書。沒有證明對任意 root 圖或表外支援的機制完備性。

## 5. 重播、信任界線與剩餘問題

新 [JSON](../artifacts/c5_no_mixed_local_screen/observations.json) 綁定 root-transport
及其十份原輸入 SHA，另綁定本 checker 與全部載入的研究 Python 模組。
每個局部 rule 保留完整來源 record 的 pointer/hash、具名接點／支援、
source/target 禁色、全部 β 族及固定框弧／原外部路徑；每個查詢保留
完整具名候選域 hash、原 join index、排除 rule 或實際異色 root pair。
Source 完整 schemas 與 placements 沿 pointer 保留，未以邊際取代。

新 checker 重用既有純函式 `admissible_supports`、`frame_evidence` 及
兩種 minor skeleton 控制；**不是獨立重寫全部幾何引擎**。重算 2,324
份 skeleton（奇數 bridge 局部型及端點長度 1/3/5），核對 branch sets
不交、連通、十鄰接、原 root incidences／actual supports 與反射／root
交換。這些 skeletons 不是 degree-list 來源圖；任意長度由 §3 沿用
紙面引理承擔。未重讀外部 Gallai 文獻，未新增其形式化。

```bash
python3 scripts/c5_no_mixed_local_screen.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 只生成本層 artifact，所有舊輸入前後 hash 不變。
已執行及未重跑清單見[本輪紀錄](history/2026-09-29-no-mixed-local-screen.md)。

若繼續尋找免表的共同證明，現在可精確拆成兩個缺口：
**以共同支援幾何排除無增長時的同 singleton；以及證明影響 R 的增長
必符合 §3 某個排除條件**。32 個不影響 R 的候選不需作局部排除。
本輪尚未解決這兩個全稱缺口；目前方向由研究線導覽維護。
