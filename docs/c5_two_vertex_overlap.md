# C₅ class 兩點重疊：資料盤點與接合規格

2026-09-30。來源為本輪使用者澄清：**任選兩個 C₅ class，各從五個
邊界頂點選兩點，按指定對應識別，主要研究重疊造成的染色狀態**。
本報告保存研究設計、既有資料與點對投影重播；沒有完成一般拓撲後繼分類。
目前停止點與下一步見[兩點重疊導覽](c5_two_vertex_overlap_guide.md)，
研究線標記見 [HANDOFF](HANDOFF.md)。

2026-09-30 後續：[具名八點接合](c5_two_vertex_join.md)已完成 evaluator、
六份固定接合的完整 relation／A、B 回投影及同代表整圖核對。
下文保留資料盤點輪的語境；完整後繼表、拓撲及多步充分性仍未完成。

## 1. 本輪確定的研究範圍

兩塊各有具名有序邊界

\[
B_A=(a_0,\ldots,a_4),\qquad B_B=(b_0,\ldots,b_4).
\]

選 $i<j$、$k<\ell$，再指定兩點的雙射。例如
$a_i=b_k=x$、$a_j=b_\ell=y$；另一種雙射交換 $k,\ell$。
兩側私有內部互斥，除此兩個頂點以外沒有其他頂點識別，沒有額外跨塊邊。
染色語義保留兩側全部真實邊；重複的同端點 simple-graph 邊不改變染色限制。
是否容許某種共同邊、指定側別或區域重疊，仍須由拓撲接法另行規定。

這不是在單一 C₅ 上任意加邊，也不是兩個 C₅ 整框五點對齊。
早先討論過的 C₅→C₆→C₅ 路徑黏合只是一個未採用的候選切入口，
**不作這条新線的起點**。本輪沒有啟動 C₆／C₇ 轉接或較大 cell 枚舉。

固定兩個帶標號 class 時，原始接法標號數為
$\binom52\binom52\cdot2=200$；這是篩選／去重前的接點對應數，
不是 200 種不同幾何，也不表示 200 種接法全合法。
Class 指完整帶標號 Σ；$D_5$ 商類不能省掉具體接點對應。

## 2. 可以立即沿用的資料

| 資料 | 內容與範圍 |
| --- | --- |
| [cell 目錄](../artifacts/c5_cells/cells.json) | 132 個帶標號完整 Σ；來源為至多五內點的 disk cell 目錄，含 chords；24 個 $D_5$ 軌道 |
| [relation 庫](../artifacts/boundary_relations/library.json) | 其中 87 類有完整 patterns、點對查詢、染色 witnesses 及合計 750 條 entry-specific 條件強迫規則 |
| [本輪點對索引](../artifacts/c5_two_vertex_overlap/pair_interfaces.json) | 全部 132×10 個點對的類型、同色／異色子 mask、完整五點染色 witnesses 與來源 SHA-256 |
| [relation API](../scripts/boundary_relations.py) | `condition`、`query`、`project`、`rename`、`reorder`、同介面 `meet` |
| [pp 層](pp_relations.md) | 完整原子、共同變數與存在量化；須保留同一共同色框 |
| [接合語義](state_language.md)、[密封與替換](local_closure.md) | 完整共同 relation、共享變數與私有內部的分工 |

Cell 目錄的 `pattern_order` 決定十 bit 的含義；`cells[str(mask)]` 指向
代表資料。每個 entry 有 `k_eff`、`edges`、三色 profile、dead prefixes 等欄位。
**`edges` 是 C₅ 框邊以外的邊**；重建代表圖要另加入
`(0,1),(1,2),(2,3),(3,4),(4,0)`，不能把 `edges` 當作整份圖。
最省 witness 的邊集不是這個 Σ class 所有圖實現的清單。

既有 87 類全部包含於 132 類，不是額外 87 類。
一般 cell 的 $k\le3$ 層也有 87 類，但與這份固定 grammar 的 87 類集合不同；
細節見 [cell enumerator](c5_cell_enumerator.md) §3。
750 是逐 entry 規則數相加，不是 750 條互異的全域規則。

本輪 checker 直接確認 87 個 ID 都在 132 類內，並按共同 `pattern_order`
核對其完整 relation。來源報告的枚舉完整性、24 個 $D_5$ 軌道及最小
內點數沿用既有資料；本輪不重新證明這些項目。

## 3. 兩點介面的精確染色語義

以下是由完整 relation 直接得到的**紙面推導，未新增 Lean theorem**。
它適用於對全域 $S_4$ 換色封閉的 relation，沒有絕對色名的預染色條件。

令 $R_A,R_B$ 是展開為 labeled assignments 的完整 Σ。
對兩點定義

\[
T_A(i,j)=\{\mathrm{eq}:\exists\alpha\in R_A,\alpha_i=\alpha_j\}
\cup\{\mathrm{neq}:\exists\alpha\in R_A,\alpha_i\ne\alpha_j\}.
\]

空 relation 給空集合；非空時只有強迫同色、強迫異色、兩者皆可三型。
所有同色有序色對位於同一 $S_4$ orbit，所有異色有序色對也位於同一 orbit。
因此，在 §1 的獨立私有內部與精確兩點共享前提下，

\[
R_{A\star B}\ne\varnothing
\iff T_A(i,j)\cap T_B(k,\ell)\ne\varnothing.
\]

必要性由共同染色限制到共享點得到。充分性是選兩側支持同一型的完整
染色，將其中一側做一次全域換色，使共享兩點的實際顏色相同，便能合併。
兩個識別方向都有此相容性判準；但它們的完整具名後繼仍應分別保存。

將接合後八個不同頂點的集合記為 $U$，兩側嵌入記為 $\iota_A,\iota_B$：

\[
J=\{c\in\{0,1,2,3\}^{U}:
c\circ\iota_A\in R_A\ \land\ c\circ\iota_B\in R_B\}.
\]

這才是接合後完整八點 relation。**不能只比較兩側各自正規化的 pattern
數字**；必須允許所有符合共享點的相對換色，最後只按一次共同全域換色
正規化。否則會丟掉非共享點之間可實現的跨側等色方式。

若只觀察原 A 的五點，精確投影是

\[
\pi_A J=\{\alpha\in R_A:
(\alpha_i,\alpha_j)\in\pi_{k,\ell}R_B\}.
\]

B 對 A 的影響即同色 guard、異色 guard、不加限制或無解。篩列可連帶
在 A 的其他點對產生新強迫，不能把原 R_A 改成獨立點對條件。
此式作為當下投影總是有效；**若要用它取代整個 J 供後續施工，
B 的其餘三點及私有內部必須永久不再被讀取**。
若後續可接觸兩側剩餘頂點，就要保留 J 或另證充分的摘要。

## 4. 本輪保存的 1,320 份點對投影

證據為 **Python 固定資料重播**。Checker 不使用 graph 枚舉器：
先獨立遍歷全部 $4^5$ 個賦色，取 240 個 proper C₅ assignments，
以 24 個色置換取最小代表，核對來源的十種 pattern 順序。
對每個 class 的每個點對，另以全部接受的 labeled assignments
重算實際有序色對集合，核對同／異色投影及兩個子 mask 的無交分割。

| 所選點對 | 無解 | 強迫同色 | 強迫異色 | 同／異色皆可 |
| --- | ---: | ---: | ---: | ---: |
| 相鄰點對，132×5 | 0 | 0 | 660 | 0 |
| 對角點對，132×5 | 0 | 0 | 35 | 625 |
| 合計 | 0 | 0 | 695 | 625 |

**這份 132 類目錄的每個點對都容許異色。** 因而由 §3 的紙面判準，
任意兩個既有 class、任意兩點雙射，在只有該兩點共享且無額外限制時，
都有非空的染色接合。這不是逐一枚舉全部 class-pair 接法所得的表，
也不是一般大小所有 disk class 的新定理。

對目前目錄，兩點接入對原 A 只會產生「異色篩列」或「不改變 Σ」；
無條件的強迫同色型沒有出現。有額外條件後的子 relation 不受此統計保證。
起始 class 非空不表示任意增加共同條件之後仍可行。

一個交接用的參考案例：A=B=R1023，將 A 的 `(0,2)` 接到 B 的 `(0,1)`。
B 的實際框邊要求 A 的兩點異色，原 A 上的投影為 R1016，與加弦 `(0,2)`
的染色效果相同。這個五點投影不宣稱原 A 框在整份接合圖中仍為 disk 外界。
完整八點接合與整圖回溯對照留待後續。

## 5. 拓撲資料與尚未完成的部分

拓撲線與狀態線使用同一份 class IDs、實際代表圖、接點雙射與共同接合圖。
需要分清下列資料：

- 相鄰點對或對角點對；兩側都有相應實際邊時，接合可能共享該邊。
  對角點也可能有 chord，不能只依「相鄰／對角」判定共同邊。
- **強迫異色不等於實際有邊**。是否有邊須讀代表圖；Σ 本身不記錄邊身份。
- 具名環序、側別、共同邊的處理、允許的區域重疊及仍可施工的位置。
- 一般抽象平面性、指定 C₅ 是 disk 外界、與兩份指定 disk 區域可按要求
  重疊，是需要分開判定的性質。

本輪不假定接合後仍有唯一 C₅ 外框，也不指定任意新 C₅ 便可以忘掉其他點。
若另選下一個 C₅，要驗證被忘記部分對所有後續施工的 separator 條件。
`geometry=unknown` 不能標成合法 disk transition。

目前沒有：完整八點後繼表、所有接法的拓撲分類、同 $(\tau,R)$ 的任意
歷史均有相同後繼的定理、有限拓撲摘要充分性、生成圖類完備性，或
$K_\infty=K_{\le5}$。兩點投影只足以處理 §3 的相容判定與單側投影，
不是任意多步施工的完整 state。

## 6. 重播、信任與接手

```bash
python3 scripts/c5_two_vertex_overlap.py          # 寫入本輪點對索引
python3 scripts/c5_two_vertex_overlap.py --check  # 只讀重算、逐 byte 比對
```

[Checker](../scripts/c5_two_vertex_overlap.py) 僅用 Python 標準函式庫。
Artifact 綁定兩份來源 JSON 及 checker 的 SHA-256；每個 class 保存
`source_cell_key`，每個 pair 保存 `equal_mask`、`different_mask`、
`equal_witness`、`different_witness`，witness 是完整五點染色 pattern。

本輪產生及 `--check` 通過；未重跑來源圖的染色延拓、disk embedding、
大枚舉或 Lean axiom audit，未新增 Lean 檔案。原有 Lean
`LocalClosure.summary_glue`、`replacement`、`seal_future` 是語義基礎；
本報告的兩點 corollary、統計及 geometry 問題不冒稱新 Lean 證明。
驗證及工作樹基準見[本輪紀錄](history/2026-09-30-c5-two-vertex-overlap-handoff.md)。

當輪停止於「輸入資料與單點對接口已備齊」。接續順序由
[導覽](c5_two_vertex_overlap_guide.md)維護，不先生成更大的 cell catalogue。
