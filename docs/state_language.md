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
    given: Conditions           # 已反映在 state.colors；不是尚未套用的註記
    history: OriginAndActions   # 回放來源；不能擅自假設與未來無關

Choice:
    branches: [Branch]
    scope: CompleteFor(scope) | Partial
```

固定色標的數學語意為 $R\subseteq\{0,1,2,3\}^{B}$。
既有 Python `Relation` 將每列解讀成一個**共同全域 S4 orbit**，只適用於換色不變的關係。
不能用它表示絕對預染色 `b0=red`；這類條件需改用 labeled rows，或明確保存共同顏色 frame。

## 2. 七個動詞

| 動詞 | 記法 | 結果與規則 |
| --- | --- | --- |
| 條件化 | `condition(S, Γ)` | 在完整 R 上篩選符合 Γ 的 rows |
| 分化 | `split(S, φ)` | 回傳 φ 與 ¬φ 兩個條件分支；記錄哪些分支為空 |
| 接合 | `join(L, R, alignment)` | 兩塊同時存在；共享頂點色一致，幾何另外判斷 |
| 消去 | `forget(S, X)` | 先套用全部相關限制，再存在量化未來不再讀取的 X |
| 查詢 | `query(S, φ)` | 無解、強迫 φ、強迫 ¬φ、尚未強迫；附 witness |
| 相容表 | `compat(C_L, C_R)` | 每一對 branches 的接合結果，不只一個布林值 |
| 觀察 | `view(S)` | 產生統一狀態卡；摘要顯示不取代完整 R |

`extend(S, action)` 可作上述局部更新的外層名稱，但 action 必須屬於指定 grammar，
回傳 `Choice` 與合法性證據；這個通用操作目前只作討論符號，不假定存在完整 evaluator。

**三種情況用不同記法：**

```text
Choice(L, R)                 # L 或 R，是替代方案
join(L, R, alignment)        # L 與 R，限制必須同時滿足
deduplicate(L, R, proof)     # 已證對未來等效，合併重複搜尋但保留來源
```

Choice 的染色投影可取 union，但不能把不同幾何 witnesses 的 union 偽裝成一個已實現 patch。
只憑 `L.colors == R.colors` 不足以做包含幾何行為的 deduplicate。

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
已選條件 Γ：
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
| condition | `Relation.condition` | EQ／NEQ guards |
| 同介面 join | `Relation.meet` | 同一組具名 ports；按名稱重排 |
| forget | `Relation.project(keep)` | 上層須保證沒有遺漏未來依賴 |
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
