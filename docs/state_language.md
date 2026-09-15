# 延伸、接合與強迫的討論表示法

2026-09-13。用途是固定討論用的物件、函數與觀察格式，方便之後改變起點、重疊方式或局部規則。
這是一份**表示法與介面規格**；除下表明確列出的既有操作外，不表示已實作一般幾何狀態類。
可直接觀察的計算例子在 [狀態觀察表](../artifacts/state_views/examples.md)。

## 1. 四個物件

| 名稱 | 記法 | 保存什麼 | 意義 |
| --- | --- | --- | --- |
| 介面 | `Interface B` | 有序具名頂點、共同色標；幾何側另存邊界 occurrences／活動面 | 未來還會讀取的位置 |
| 狀態 | `State S` | 介面 B、完整染色關係 R、幾何資料 E、證據引用 | 一個具體候選局面的摘要 |
| 分支 | `Branch h` | 目前狀態 S、已選条件 Γ、來源／操作歷史 | 到達該局面的某種走法 |
| 候選族 | `Choice C` | 一組帶身份的 branches、列舉範圍是否完整 | 多個替代選擇；不要求全部同時發生 |

幾何資料 E 的型別由模型決定。固定端點路徑 grammar 可使用 forbidden-set F；
一般活動面／移動前緣的 E 尚未定義充分表示，因此 **State 目前是候選摘要，不是已證的通用充分狀態**。
不同起點只是分支來源，除非它帶來預染色、指定側別或其他實際限制。
同一個實體頂點可能在 boundary walk 出現多次：染色要相等，幾何 occurrence 仍分別保留。

類風格的閱讀方式（pseudocode，非已存在的 Python API）：

```text
State:
    interface: Interface
    colors: FullRelation
    geometry: GeometryData | Unknown
    evidence: EvidenceReferences

Branch:
    state: State
    given: Conditions           # 已反映在 state 中；染色條件進 colors，幾何／側別條件進 geometry 或 evidence
    history: OriginAndActions   # 回放來源；不能擅自假設與未來無關

Choice:
    branches: [Branch]
    scope: CompleteFor(scope) | Partial
```

固定色標的數學語意為 $R\subseteq\{0,1,2,3\}^{B}$。
既有 Python `Relation` 將每列解讀成一個**共同全域 S4 orbit**，只適用於換色不變的關係。
不能用它表示絕對預染色 `b0=red`；這類條件需改用 labeled rows，或明確保存共同顏色 frame。

條件依作用域至少分成兩類：染色條件 $\Gamma_{\mathrm{color}}$ 與幾何／側別條件 $\Gamma_{\mathrm{geom}}$。
前者可直接反映在完整 relation R；後者必須由指定幾何模型的 E／evidence 保存或判斷，不能假裝成對 R 的 row filter。
下文 `condition`／`split`／`query` 的明確 relation-level 語意只針對染色 predicate；若 predicate 讀取幾何資料，必須另有 model-specific evaluator 與證據。

## 2. 七個動詞

| 動詞 | 記法 | 結果與規則 |
| --- | --- | --- |
| 條件化 | `condition(S, Γ)` | 對染色條件在完整 R 上篩選 rows；幾何條件須由模型另外處理 |
| 分化 | `split(S, φ)` | 對染色 predicate 回傳 φ 與 ¬φ 兩個條件分支；記錄哪些分支為空 |
| 接合 | `join(L, R, alignment)` | 兩塊同時存在；共享頂點色一致，幾何另外判斷 |
| 消去 | `forget(S, X)` | 先套用全部相關限制，再消去未來不再讀取的 X；geometry 需產生 residual E′ 或降級 unknown |
| 查詢 | `query(S, φ)` | 對染色 predicate 回無解、強迫 φ、強迫 ¬φ、尚未強迫；附 witness |
| 相容表 | `compat(C_L, C_R)` | 每一對 branches 的接合結果，不只一個布林值 |
| 觀察 | `view(S)` | 產生統一狀態卡；摘要顯示不取代完整 R |

`extend(S, action)` 可作上述局部更新的外層名稱，但 action 必須屬於指定 grammar，
回傳 `Choice` 與合法性證據；這個通用操作目前只作討論符號，不假定存在完整 evaluator。

`forget` 的 relation-level 核心是存在量化，但 State 還有幾何資料。若 $X\subseteq B$ 可安全消去，概念上是

\[
(B,R,E)\longmapsto (B\setminus X,\ \exists_X R,\ E').
\]

這要求所有仍會被未來的邊、預染色、共享 frame 或其他條件讀取的變數都保留在介面。
同時，幾何模型必須提供消去後仍足以支援其後操作的 residual summary $E'$；若目前沒有這種已證更新，應明確令 `geometry = unknown`，而不是默認沿用原 E。
因此只做 `Relation.project(keep)` 能證明的是染色投影，不能單獨推出包含幾何 continuation 的未來等價。

**三種情況用不同記法：**

```text
Choice(L, R)                 # L 或 R，是替代方案
join(L, R, alignment)        # L 與 R，限制必須同時滿足
deduplicate(L, R, proof)     # 已證對未來等效，合併重複搜尋但保留來源
```

Choice 的染色投影可取 union，但不能把不同幾何 witnesses 的 union 偽裝成一個已實現 patch。
只憑 `L.colors == R.colors` 不足以做包含幾何行為的 deduplicate；§8 區分幾種不同強度的等價。

## 3. 接合的精確語意

令左右介面為 $B_L,B_R$。先用顯式 alignment 指明哪些頂點其實是同一個；
對合併介面 $B$ 上的賦色 a，定義

\[
R_{\mathrm{join}}=
\{a\in\mathrm{Color}^{B}:a|_{B_L}\in R_L\land a|_{B_R}\in R_R\}.
\]

這裡 restriction 按指定頂點嵌入解讀，不按兩側陣列位置猜測。
同一有序介面就是 `R_L ∩ R_R`；不同介面是上述自然接合。
所有仍共享的內部變數都要提升到介面，或留在共同公式裡，不能先各自忘掉。
如果接合還要增加跨側新邊，其 NEQ 限制也要另外加入；對齊既有頂點不會自動生成那些邊。

**proved in Lean：** 私有內部獨立的同介面實際圖接合見 `LocalClosure.summary_glue`／`replacement`。
不同介面的上述式子在此作語意定義；本輪没有新增一般幾何 compiler 或定理。

`join` 的結果應分開顯示：

```text
colors:    empty | nonempty
geometry: verified_legal | verified_illegal | unknown
```

完整 relation 為空或有有效幾何拒絕證書，可剪枝。
`nonempty + unknown` 只叫「染色相容」，不叫「已合法」。
只有證據對應到當次實際接合，才能標 verified；兩個原子各自合法不構成 joint certificate。

## 4. 預選、強迫與相容表

**預選**是 `condition` 或 `split`，保留所選條件之後的完整關係。
`split(S, φ)` 的兩側互斥，合起來恢復 S 的染色關係；若兩側非空，尚無強迫。

對非空 R：

\[
\operatorname{query}(R,\varphi)=
\begin{cases}
\mathrm{forced\_true},&\forall a\in R,\ \varphi(a),\\
\mathrm{forced\_false},&\forall a\in R,\ \neg\varphi(a),\\
\mathrm{undetermined},&\text{兩種 witnesses 都存在}.
\end{cases}
\]

空 R 回 `infeasible`，不把矛盾解讀成「什麼都強迫」。
`query` 問的是給定 predicate；一個條件被強迫不表示整個染色或整棵延伸樹只有唯一解。
既有 `Relation.query(x,y)` 是 φ=`x=y` 的特例，名稱為 `forced_equal`／`forced_different`／`free`。

相容表每格保存 `join(L_i,R_j)` 的狀態卡。
刪去沒有任何可能相容 partner 的分支，就是**候選篩選**；某一 row／column 被選定，會限制另一側。
幾何 unknown 的格子不能當作已拒絕。若候選族只是 Partial，沒有找到 partner 也不能推出全局無解。
三棵以上延伸樹須保留共同 joint relation；全部 pairwise 檢查通過不保證同一全域賦色存在。

## 5. 一套可直接引用的例子

令 `L=R91`、`R=R935`，固定共同介面 `B=(b0,b1,b2,b3,b4)`。

```text
query(L, b0=b2)                 = undetermined
query(R, b0=b2)                 = undetermined
J = join(L, R, identity)
query(J, b0=b2)                 = forced_true
condition(J, b0!=b2).colors     = empty
```

**computationally observed／本輪重驗：** 兩側單獨都允许同／異色，接合後有 48 個賦色且全部同色。
若兩側各自 `split(b0=b2)`，相容表為：

| 左分支／右分支 | R：b0=b2 | R：b0!=b2 |
| --- | ---: | ---: |
| L：b0=b2 | 48 | 0 |
| L：b0!=b2 | 0 | 0 |

這是「相遇後兩側的異色預選都被排除」，不是事先任意選擇同色。
此表只顯示染色相容；這兩個指定 witnesses 的一內一外幾何證據另見 `boundary_relations.md`。

另一個引用簡寫：`F=R767`、`Γ=(b1=b4 ∧ b0!=b2)`：

```text
query(condition(F, Γ), b0=b3)   = forced_true
```

**proved in Lean（既有 native finite check）：** `C5PairForcing.fan_guard_forces`。
本輪觀察表以全域 24 個色置換展開 labeled rows，重驗條件化、交集和 witness；沒有新建 Lean 定理。

## 6. 固定觀察格式

以後討論新例子先填一張卡：

```text
名稱／起點：
介面 B：                         # 頂點對齊、共同色標
模型／活動面：
已選條件 Γ：                     # 標明 color / geometry / mixed
完整 R：                         # 色型列表或可回放的引用
幾何 E 與證據：
查詢 φ：
結果：infeasible / forced_true / forced_false / undetermined
witness／拒絕證書：
狀態：proved in Lean / computationally observed / conjectured（逐項）
```

派生問題便能寫成短式：

```text
# 換一個起點後，是否相同？
compare(view(S_from_p), view(S_from_q))

# 一側預選，另一側還剩哪些 branches？
compat(Choice(condition(L, Γ)), C_R)

# 哪些限制是在兩側相遇後才出現？
compare(query(L, φ), query(R, φ), query(join(L,R,a), φ))

# 封閉後，限制留下在哪些介面點？
view(forget(condition(join(L,R,a), Γ), closed_private_ports))
```

`compare` 是觀察用途，不以相同卡片欄位自動推定未來等價。
週期／博弈控制仍依使用者指示僅保留注意事項，沒有加入本輪操作或搜尋。

## 7. 既有程式對應與重現

| 討論符號 | 現有程式 | 範圍 |
| --- | --- | --- |
| FullRelation | `boundary_relations.Relation` | 共同全域 S4-invariant 色型 |
| condition | `Relation.condition` | EQ／NEQ guards；只處理染色條件 |
| 同介面 join | `Relation.meet` | 同一組具名 ports；按名稱重排 |
| forget | `Relation.project(keep)` | 只做染色投影；上層須保證未來依賴與 geometry residual |
| pair query | `Relation.query` | 同／異色，非空強迫與 witnesses |
| 共同約束＋隱藏變數 | `pp_relations.Formula`／`evaluate` | 小型 pp 公式；geometry unchecked |
| 完整 State／Choice／compat | 本文件的規格與觀察格式 | 尚無一般幾何 API |

```bash
python scripts/state_views.py
python scripts/state_views.py --check
```

這兩個命令只使用既有 catalog 及 relation API，產生／重驗 `artifacts/state_views/examples.md`。
輸出含狀態比較、分支相容矩陣與全部十種 C5 色型的存活表。
沒有重跑圖搜尋、修改既有 API 或啟動一般多起點接線研究。

## 8. 三層等價與 replacement 強度

為避免把「boundary relation 相同」直接升格成「所有未來行為相同」，後續至少區分三層等價。

### 8.1 染色等價 `≡color`

對具有同一具名介面 B 與共同顏色 frame 的兩個狀態／patch，定義

\[
S\equiv_{\mathrm{color}}T
\quad\Longleftrightarrow\quad
R_S=R_T.
\]

它只聲明完整 boundary coloring relation 相同；不包含 embedding、活動面、可接線位置或其他幾何 continuation。
因此 `S ≡color T` 足以回答「兩者允許哪些介面染色」，但一般不足以做搜尋狀態 deduplicate。

### 8.2 圖 context 等價 `≡ctx`

在指定的 graph-context 類別 K 中，若兩個具有同一介面 B 的實際 patch G、H 滿足

\[
\Sigma(G\cup_B K)=\Sigma(H\cup_B K)
\]

對所有允許的 K 都成立，稱其在該 context 類別中等價，記為 $G\equiv_{\mathrm{ctx}}H$。

**proved in Lean（既有定理）：** 在 `LocalClosure.summary_glue`／`replacement` 的假設下，兩側私有內部彼此獨立、只經共同介面 B 接合時，boundary summary 相同即可推出這一類 graph contexts 中可互換。
這是從 relation equality 到實際圖 replacement 的語意橋；它仍不聲明任意施工歷史、活動面或幾何 grammar 都無法區分兩者。

### 8.3 未來等價 `≡future`

固定一套 extension grammar／允許的未來 actions。若從 S 與 T 出發，所有合法未來 contexts／action sequences 的接受、拒絕與可觀察結果都一致，才稱

\[
S\equiv_{\mathrm{future}}T.
\]

這是搜尋狀態 deduplicate 所需的強等價。它通常同時依賴染色 relation 與足夠的 residual geometry。
在固定端點 wiring grammar 中，`LocalWiring.residual_exact`／`chord_residual_exact` 已給出 forbidden-set F 的 exact continuation 分類；一般活動面／移動前緣目前沒有對應的完整充分狀態定理。

三層關係不要反向混用：

```text
same colors                    -> 只得到 ≡color
LocalClosure replacement hypotheses + same summary
                               -> 得到該 graph-context 類別的 ≡ctx
指定 grammar 的 exact residual proof
                               -> 才可宣稱 ≡future，並安全 deduplicate
```

例如若研究目標只是「每個可實現 C5 boundary relation 是否存在至多五個內部頂點的代表」，所需結論是找到 H 使 `Σ(H)=Σ(G)`；再配合已證 replacement hypotheses，可得到相應 graph-context 互換。
這個代表命題本身**不需要**主張 H 與 G 在任意逐步施工 grammar 中 `≡future`，也不要求由 G 經一串局部操作逐步化簡到 H。
