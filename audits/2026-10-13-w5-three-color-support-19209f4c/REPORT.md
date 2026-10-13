# W₅ 三色鄰環 support 的充分性與保存強度

2026-10-13。BASE：`19209f4cf68261fdce5e84a7804cfe04ae0957bf`。
來源：[W5 具名完整關係縮減](../../docs/c5_w5_marked_relation.md)，
特別是原報告的中心消去恆等式及 annulus 代表義務。
輸入逐檔凍結於 `frozen/`，雜湊見 [INPUTS.json](INPUTS.json)。

**結論為肯定：同槽位 annulus 的三色 B/U support 相等，足以保持補中心後完整外框關係。**
本報告證明任意有限合法來源的充分條件，給出雙向完整染色搬運；有限控制只校準
實作與反例，不負責證明普遍量詞。沒有構造一般 annulus 小代表，也沒有完成
一般正聯集縮減、十三內點以上來源排除或 `K∞=K≤5`。

## 1. 完整前提與資料契約

1. 色集固定為 \(C=\{0,1,2,3\}\)，所有染色都是無額外 list 限制的 proper vertex
   四色染色。使用相同 literal 色名；不分別正規化內外框。
2. \(B=(b_0,\ldots,b_4)\) 是原有序外 C₅，\(U=(u_0,\ldots,u_4)\) 是原有序內 C₅；
   十個 labels 互異，\(B\cap U=\varnothing\)。下標模五。U 在各 annulus 中均誘導 C₅。
3. \(H,H'\) 各為有限簡單 plane disk 圖，帶指定 B 外面與 U 空的有界五邊面；
   其餘頂點與邊都在 B、U 之間。二者嵌入相同具名 annulus 槽位，邊界點、
   環序、內外側及介面 attachment 位置已對齊，沒有隱藏的額外接點。
4. 原 \(G=H+v\) 的中心滿足 \(N_G(v)=U\)，U 內側恰為 v 與五個三角面。
   在 \(H'\) 的同一空面放入對應的 v，加入且只加入五條 \(vu_i\)，得到 \(G'=H'+v\)。
   因而兩份中心均無額外鄰點或禁色。
5. 私人頂點集合可不同；各圖自身的全部原邊、旋轉、ownership、附件與完整染色
   都按該圖保存。比較僅透過既定 B/U 介面；不得旋轉 U、偷換接點、將不同來源
   的 witnesses 拼接，或把全圖換色誤作 U 單獨換色。

「同槽位」是圖與嵌入的前提，不能由關係相等推出。換 annulus 可以改變私人部分，
但仍須交付新圖自己的合法嵌入；本命題不提供把原私人頂點逐一映到新圖的 graph map。
若有外部共同圖，它只能透過明列的介面黏合，且旋轉與槽位必須相容。
最小性、edge-critical、N2 身份、near-triangulation 及四色定理都不是本命題的前提。

令 \(\mathcal B\) 為 B 上全部 proper literal 四色 tuples，定義

\[
J_H(\beta,\tau)=\{\eta:V(H)\to C:\eta\text{ proper},\
\eta(B)=\beta,\ \eta(U)=\tau\},\qquad \tau\in C^5,
\]
\[
R_H=\{(\beta,\tau):J_H(\beta,\tau)\ne\varnothing\},\qquad
R_H^{(3)}=\{(\beta,\tau)\in R_H:|\operatorname{im}\tau|=3\}.
\]

\(\Sigma(X)=\{\beta\in\mathcal B:\mathcal C_X(\beta)\ne\varnothing\}\) 指完整有序外框關係，
不是一個固定 beta 的判斷。以下特別區分 \(\Sigma(H)\) 與 \(\Sigma(H+v)\)。
所有 fibres 包含空格；support 雖只記非空性，其補集仍由完整固定域決定。

實作可只儲存原十列
`01012,01021,01023,01201,01202,01203,01212,01213,01231,01232`。
每個 proper B tuple 用三或四色，故從其首次出現順序的正規代表到該 tuple，
恰有一個全色集置換；三色時唯一未用色亦被唯一決定。因而十列乘共同 S₄ 搬運
恰涵蓋全部 240 個 literal beta。必須將同一置換施於 beta、tau 與整份 lift。

## 2. 命題 W5-R3：精確充分條件

**命題。** 在 §1 前提下，對每個 beta 有

\[
\mathcal C_{H+v}(\beta)\ \cong\
\bigsqcup_{\tau:\,|\operatorname{im}\tau|=3}J_H(\beta,\tau),
\qquad
\boxed{\Sigma(H+v)=\operatorname{pr}_B R_H^{(3)}}. \tag{1}
\]

因此

\[
R_H^{(3)}\subseteq R_{H'}^{(3)}
\Longrightarrow \Sigma(H+v)\subseteq\Sigma(H'+v),
\tag{2}
\]

尤其 \(R_H^{(3)}=R_{H'}^{(3)}\) 蘊涵完整 \(\Sigma(H+v)=\Sigma(H'+v)\)。
兩邊所有四色 U fibres 可以不同，不影響此結論。

**證明。** 限制一份 G 染色到 H，得唯一 eta 及 tau。U 是奇環，proper tau
至少使用三色；v 與全部 U 相鄰，故 tau 不能用四色。因此 tau 恰用三色，
v 必取唯一缺色 \(m(\tau)\in C\setminus\operatorname{im}\tau\)。
反過來，任何 \(\eta\in J_H(\beta,\tau)\) 若 tau 用三色，保留 eta 並令
\(v=m(\tau)\)，所有新 spoke 均 proper，且沒有其他新邊要檢查。
限制與補色互為逆映射，得 (1) 的逐 fibre 雙射；取非空性與 beta 投影即得 (1)、(2)。∎

若目標**僅**為完整外框關係，精確充要條件其實是

\[
\operatorname{pr}_B R_H^{(3)}=\operatorname{pr}_B R_{H'}^{(3)}.\tag{3}
\]

R³ 相等是比 (3) 強、但可保留原 U 顏色的充分條件；不是保持 Σ 的必要條件。
不能以 \(\Sigma(H)=\Sigma\(H'\)\) 取代 (3)，因為前者亦計入不能接中心的四色 tau。

## 3. 可執行的雙向延伸與幾何合法性

固定 H、H′ 各自的一份私人頂點次序，以及色序 0<1<2<3。對每個非空三色 cell，
令 \(s_H(\beta,\tau)\) 為該有限 fibre 中按上述次序字典序最小的完整染色；
H′ 同理。可以枚舉全部私人賦值並逐邊檢查，故選取是明確有限演算法，
不需要效率假設或任意選擇公理。給定 support 相等，其兩向所需 cells 保證非空。

對每份 \(\gamma\in\mathcal C_G(\beta)\)，置 \(\tau=\gamma(U)\)，定義

\[
F(\gamma)|_{H'}=s_{H'}(\beta,\tau),\qquad
F(\gamma)(v)=m(\tau)=\gamma(v).
\tag{4}
\]

反向對 \(\gamma'\in\mathcal C_{G'}(\beta)\) 定義

\[
E(\gamma')|_H=s_H(\beta,\gamma'(U)),\qquad
E(\gamma')(v)=m(\gamma'(U))=\gamma'(v).
\tag{5}
\]

每份輸出都是相應圖的一份**完整** proper 染色；B、U 的各個原 label 及色名、
以及中心色逐一不變。若由十列實作，先將整份輸入共同拉回其 beta 代表，選取後
再以同一全色置換推回，便得到所有 literal 輸入上一個同樣有效的搬運構造；
這未必是 literal 色序下的最小者，但另可保證對全圖共同換色 equivariant。
只有 (3) 時仍可逐 beta 選輸出，但未必保留原 tau。

F 與 E 一般不互逆、未必單射或滿射；它們證明的是每份輸入可搬運，而非全部
私人 assignments 可無損還原。事實上，存在保留 B/U 的兩向染色函數，等價於
R³ 相等：由任意非空三色 cell 補中心後搬運再限制，立即得到另一邊同一 cell 非空。

幾何方面，兩個 U 都界定原槽位的空 disk；在其內放一點，向依序的五個邊界點
畫放射弧，可選弧兩兩只交於 v，所得五個區域正是三角面。因 U labels 互異且
中心全新，不產生 loops 或重邊；B 外面及 annulus 其餘邊、旋轉均保持。
F/E 只選染色，不改嵌入，也不做交叉雙對識別。外部共同部分若只在固定介面
相接，保留其原染色即可；任何未列入介面的私人附件都不在此保證內。

## 4. 三種保存強度與全色 support

| 保存目標 | 所保證的資料 | 不自動保證 |
| --- | --- | --- |
| 補中心後完整 Σ | 每個 beta 是否至少有一份 G lift；等價於 (3) | 原 tau、指定 U witness、計數 |
| 三色 support R³ | 每個 literal 三色 (beta,tau) 是否有 lift；等價於保留 B/U 的兩向搬運 | 每格有幾份 lift、四色 fibres、私人 assignments |
| 全部 full lifts | 原 J 的每格全部 assignments 與來源頂點對應，包含空格；可逐份重建原 H/G | 單由較小表示的非空 bits 無法達成 |

若不同私人頂點域要求「保持 full lifts」，必須另指定逐 fibre 的可逆編碼／雙射
或原圖的無損重建資料；不可把兩向 selector 稱為 full-fibre 雙射。
全部 full lifts 可推出全色 support R，R 可推出 R³，R³ 可推出 capped Σ。
前三種指定目標的逆向蘊涵均有下面的合法圖反例。

* **Σ 不決定 R³。** 原控制 `prism` 與 `triangulated_00` 的 capped Σ 均為十列全接受，
  但十代表 beta 列中的 R³ 分別有 340 與 20 個 cells
  （全 240 literal 列則為 8,160 與 480 格）。這裡比較的是 Σ(G)，不是 Σ(H)。
* **R³ 不保存 full lifts。** `prism_decorated` 在 `prism` 的第一個 annular face
  放入 x=11，只接 b₀、u₀，原邊 b₀u₀ 保留。二者顏色不同，故 x 每次恰有兩種選擇。
  全色 R（因而 R³）完全相同，但每個非空 fibre 從一份變兩份；G lifts 亦倍增。
  限制可刪 x，延伸可選兩色中的較小者，但來回不會保留兩份不同 x assignments。
* **R³ 也不決定全色 R。** §6 的另兩個合法 annulus 在相同 U 外側加入一個全鄰 U
  的私人點 w。它總能接受三色 tau 的唯一缺色，卻拒絕每個四色 tau；完整面資料與
  直接枚舉另存，並不把它們混列為原 34 圖。

本充分條件只針對固定四色情形的 wheel cap。若改為容許四色 tau 的其他內側
補片、中心有額外限制、色集變動、或 U 不再是奇五環，都必須重算 cap 的接受謂詞。
即使 R³ 相同，也不能藉此對任意 cap 宣稱等價。

## 5. 錯誤投影與混合 witnesses 的反控制

下列候選均須標為 `counterexample`，不是對 W5-R3 命題的反例。

1. **只保 Σ(H)。** `prism` 與 `triangulated_01` 均有 Σ(H)=1023，補中心後為
   1023 與 831。beta=`01212` 時後者唯一 H lift 為 `0121223031`，U 用四色；
   前者可用完整 G lift `01212101032`。原色框與全部邊均固定。
2. **把 beta 與 tau 的各自投影作 Cartesian product。** 即使某 beta 出現在 R³，
   某 tau 也在另一列出現，仍須同一 (beta,tau) cell 非空。`prism` 中
   (beta=`01012`,tau=`10103`) 與 (beta=`01021`,tau=`10102`) 都有三色 witness；
   混成 (beta=`01012`,tau=`10102`) 卻違反原邊 b₄u₄，該 fibre 為空。
3. **分開滿足兩個等式。** `triangulated_01` 的 beta=`01012` 下，
   u₁=u₃ 的全部 H witnesses 只有 `0101223231`，u₂=u₄ 的只有 `0101212303`；
   兩集合交集空。不能把兩個接受 bits 接成一個三色分支 E₀。
4. **獨立正規化 U。** `prism` 的 beta=`01012`、tau=`10103` 合法，U 單獨
   正規化成 `01012` 後，原五條 bᵢuᵢ 全部變同色，目的 cell 為空。
5. **一份單對商圖接受就補中心。** proper 四色 U 也有一對非相鄰點同色，故可
   在某單對 quotient 出現；缺色集合仍空。例如 `prism` 的 H lift
   `0101210123` 在 u₀=u₂ 分支出現，U=`10123` 卻沒有中心缺色。

保存 R³ 已經把存在量詞放在完整 cell 內。計算 R³ 時依然必須得到同一圖、
同一 beta、同一 tau 的共同 witness；只在其後才可忘記該 cell 的數量及私人細節。

## 6. 有限驗證與獨立審查

下列計數全部使用**十個代表 beta 列、各列 1,024 個 literal tau**，不把它們
誤稱為 240 literal beta 的原始格數。全部色框的結論由 §1 的共同 S₄ 搬運涵蓋。

### 6.1 原 34 圖：完整 cells 與搬運

`prism` 的邊為原 B 環、U 環及五條 bᵢuᵢ；annular faces 為
`[b_i,b_(i+1),u_(i+1),u_i]`。32 個 `triangulated_mm` 分別在第 i 面中加入
一條對角線：mask 第 i bit 為 1 時加 bᵢuᵢ₊₁，否則加 bᵢ₊₁uᵢ。
`prism_decorated` 則是 §4 的二度私人點例。向量使用 B=0..4、U=5..9、v=10、
私人點 x=11；H/G 的頂點次序各自依數字遞增，不能把 H 向量末位誤作中心。

[主 checker](controls/check_three_color_support.py) 明示沿用凍結前輪的構圖、
面驗證及 DFS，重新生成全部 H/G／商圖 lifts，再加入三色 support 與 pair controls。
[獨立 checker](review/independent_check.py) 不匯入上述程式，從邊／面規則重新構圖，
用自由頂點 assignments 的 Cartesian product 直接篩邊，逐格核對新證書及舊凍結
證書的全部 H/G lifts；它不重新獨立枚舉舊 170 個商圖，這部分由主程式重播。

| 原固定域核對項 | 數量／結果 |
| --- | ---: |
| H/G 嵌入的 darts、旋轉、連通、Euler 核對 | 68 |
| 完整 cells／空 cells | 348,160／345,580 |
| 完整 H／G lifts | 3,250／1,620 |
| 非空三色 cells／逐列中心投影 | 1,280／340 |
| 不同圖的 unordered pairs | 561 |
| R³ 相等且結論成立 | 1 pair：prism／prism_decorated |
| 相等前提未觸發 | 560 pairs：`not triggered` |
| 兩個方向逐份 G selector 輸入 | 1,020：`triggered and holds` |

全部 24 個共同色置換另核對 78,000 份 H／38,880 份 G lifts；獨立 checker
對 `prism`、`triangulated_01` 的全部 240 literal beta 再作直接枚舉，共 480 列，
與色搬運的完整集合一致。這些是明列固定域的 `triggered and holds`。

### 6.2 三色相同、四色不同的補充兩圖

H₀ 只有 B、U 兩圈及 b₀u₀、b₁u₁。H₁ 再在 U 外側的 annulus 放入 w=11，
加入全部 wuᵢ。H₀ 的有向面為

```text
outer [4,3,2,1,0]; inner [5,6,7,8,9]
annular [0,1,6,5]; [1,2,3,4,0,5,9,8,7,6]
```

H₁ 保留前三個面，將最後一面替換為

```text
[1,2,3,4,0,5,11,6]
[11,5,9]; [11,9,8]; [11,8,7]; [11,7,6]
```

兩份表每條邊的兩個方向各出現一次、頂點 link 各為一圈、連通且 Euler 特徵為 2，
因此给出具名平面槽位。補中心僅替換 inner 面。兩套實作亦逐點刪除核對四個 H/G
圖都是二連通；此例沒有聲稱 near-triangulation 或最小來源身份。

每份 H₀ 的三色 tau 唯一延伸至 w=m(tau)，每份四色 tau 則不能延伸至 w。
故 R³ 嚴格相同而 R 不同；反例 cell 為 beta=`01012`、tau=`10123`。
這是獨立的圖論證明，並非從計數猜測等價。

| 補充圖 | R³ cells | R⁴ cells | H lifts | G lifts |
| --- | ---: | ---: | ---: | ---: |
| two_spoke | 700 | 700 | 1,400 | 700 |
| two_spoke_external_apex | 700 | 0 | 700 | 700 |

共 20,480 格、18,380 個空格，雙向 1,400 份 G 輸入均保留 B/U/v。
資料及生成器是 [strict_support.json](review/strict_support.json) 與
[strict_support_check.py](review/strict_support_check.py)；獨立 checker 再從自己的
邊／面構造重算全表，不匯入補充生成器。它們與原 34 圖分開計數。
原 34 圖中此嚴格性例為 `not triggered`，此補充 pair 則是錯誤逆命題的 `counterexample`。

### 6.3 審查、破損證書及重播

[獨立理論審查](review/THEORY.md)、[獨立實作報告](review/INDEPENDENT.md) 與
[獨立結果](review/independent_summary.json) 分別記錄普遍證明與有限域核對。
主 [完整證書](controls/certificate.json.gz) 與 [摘要](controls/summary.json) 保存
全部具名圖、空 fibres、full lifts、support、兩向 selectors 與七項數學反控制。

另外製作 [8 份破損證書](negative/fixtures.json)：刪掉真 R³ cell、把四色 cell
放入 R³、混合 beta/tau marginals、漏一份私人 assignment、U 單獨正規化、
虛構共同等式 witness、錯誤中心色、單獨反轉內面。兩套 checker 均以非零退出
拒絕全部 8 份，合計 16 次拒絕；重複 `--write` 亦拒絕覆寫正常證書。
正常、seed17、獨立、補充重播與上述拒絕共 21 項預期全部符合，完整 logs／
exit codes 見 [verification.json](verification.json)。11 份 frozen inputs 與 live
來源的 hashes 全數相同。破損 fixtures 不作正常輸入，也不改原證書。

```bash
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/controls/check_three_color_support.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/controls/check_three_color_support.py --check --seed 17
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/review/independent_check.py
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/review/strict_support_check.py --check audits/2026-10-13-w5-three-color-support-19209f4c/review/strict_support.json
```

以上四條是只讀重播。`run_verification.py` 另外建立專屬 logs／verification.json，
已執行並拒絕覆寫；既有交付直接讀其結果，不再對同一路徑作生成。
文件檢查通過（636 Markdown／7,905 links）；正式 docs DocGraph 通過。
全工作樹 DocGraph 仍有 62 項歷史 duplicate-ID errors，記為 FAIL，不稱全域通過。
`lake build` 既有回歸通過（8,831 jobs），沒有新增 Lean theorem；未重跑上游大型
枚舉／外部計數證書。工作樹另有並行研究目錄，未讀改或納入本包。

## 7. 可供小代表研究引用的推論與未涵蓋範圍

**條件性小代表推論。** 對任意滿足 §1 的 H，若另行構造合法同槽位 H′，
證明 \(R_H^{(3)}=R_{H'}^{(3)}\)，且 H′ 在 B∪U 外至多 r 個私人點，
則 H′+v 有至多 5+r+1 個內點，並保持原 G 的完整 Σ。
若 r≤6，便得到至多十二內點的代表；能否接用上游十二內點定理仍按該定理前提，
本輪沒有重驗其外部計數或另提供一般 H′ 的存在證明。

本輪已解決的是 W5-R3 的任意有限合法 annulus 充分性、雙向完整染色搬運、
保存強度區別與固定控制。以下仍未涵蓋：一般 annulus 的 r≤6 代表構造、
有效的小型搜尋或壓縮演算法、原五商圖的僅外框 bits 正聯集化、任意 cap 等價、
真正最小目錄外 933／941 來源的實現／排除、一般 `K∞=K≤5` 與 Lean 形式化。
真正最小來源控制為 `not triggered`，不得以零 triggers 宣稱排除。

本輪證據與報告獨立交付，未改舊證書與封存 manifest，未 commit／push。
來源的全 support 條件仍是正確但較強的充分條件；其五商圖 full-lift 重建定理不受削弱。
Reviewed-unchanged：原 W5 入口、degree-5 父入口及 Kempe 導覽的父命題 OPEN 仍成立；
README／HANDOFF 研究線未變。本輪新的可引用結論以本報告為準。
Propagation stop：L2；沒有將子命題充分性提升為小代表存在或主命題完成。
