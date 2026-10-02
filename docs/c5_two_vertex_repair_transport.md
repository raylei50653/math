# 六份 C₅ two-vertex joins 的 local-repair transport audit

**後續（2026-09-30）：** [共同 repair lemma](c5_two_vertex_common_repair.md)
已將本頁三種 witness／兩類覆蓋抽成充要定理，核對六圖實例與獨立 P=J
退化支；[來源充分條件](c5_two_vertex_repair_sources.md)及後續替換族已給
指定圖類的來源定理，全部代表必要分類仍保留。下文保留本輪 audit 的數字及當時下一步。

2026-09-30。接續[反向案例全部極小修復](c5_two_vertex_minimal_repairs.md)，
只使用[既有六份具名接合](c5_two_vertex_join.md)的原圖。
使用者確認的 frame 定義為：**原八點 U 上、能作整張接合圖 disk 外界的全部 C₅**。
不是只讀既有 rotation 的面，也不把不能作整圖外界的原 A/B 框加回基底。

結果分兩支：四例的 frame 拉回已恰為 J，r*=0；正、反向私有內點例
均 r*=4，且共享 forced-core + alternative-family 的修復公式。
兩例的完整具名排除資料不能經八點重新命名互相搬運。
下一步選擇**抽象有明確前提的共同 repair lemma**，保留 frame-exact 的退化支；
本輪沒有發現需要另開非平凡 repair taxonomy 的第二種公式。

證據是固定六圖的 Python 窮盡證書及下述關係／覆蓋推論，未 Lean 化。
目前停止點見[研究導覽](c5_two_vertex_overlap_guide.md)。

## 1. 完整模型與 cross-case matrix

每例保留原 A/B 具名邊界、兩點雙射、所有原邊與私有內點、原 U 的欄序
及同一色框 `D={0,1,2,3}`。令

\[
J=\{u\in D^U:u\text{ 延拓至原接合圖的正常染色}\},\qquad
P=\bigcap_{C\in\mathcal C}\pi_C^{-1}(\pi_CJ),\qquad
\Delta=P\setminus J.
\]

𝓒 為上述全部可用五框；投影均為整張原圖的完整 relation。
不同框的延拓可以不同，不能拼成一份 U 延拓。
基底始終只有 P，未先加入原邊、二點或三點投影。

令 `P_r=P∩⋂_{|S|=r} π_S⁻¹(π_SJ)`，`P_0=P`；
`r*=min{r:P_r=J}`。全部 r=0,…,8 均有計算。
用所有恰 r 點投影與用所有至多 r 點投影等效：任何較小 scope 都能擴至
r 點，較大投影限制蘊含較小投影限制。本輪不預設四點充分。

下表 J/P/Δ 及 ladder 均為**全域 S₄ 軌道數**；本輪所有八點軌道
均含至少三色，具名賦色數一律乘 24。「空」是一個空集合 repair。

| Join | 可用／候選框 | J | P | Δ | r=0,1,2,3,4 的殘留 Δ | r* | r* 排除類數 | Minimum 份數／組數 | 全部 inclusion-minimal |
| --- | ---: | ---: | ---: | ---: | --- | ---: | ---: | --- | --- |
| `reference` | 2／2 | 140 | 140 | 0 | 0,0,0,0,0 | 0 | 1 | 0／1 | 空：1 組 |
| `reference_reverse` | 2／2 | 140 | 140 | 0 | 0,0,0,0,0 | 0 | 1 | 0／1 | 空：1 組 |
| `free_pairs` | 4／4 | 152 | 152 | 0 | 0,0,0,0,0 | 0 | 1 | 0／1 | 空：1 組 |
| `shared_chord_frame_edge` | 2／2 | 140 | 140 | 0 | 0,0,0,0,0 | 0 | 1 | 0／1 | 空：1 組 |
| `private_interiors` | 2／5 | 60 | 114 | 54 | 54,54,16,16,0 | 4 | 8 | 2／1 | 二份：1；三份：14 |
| `private_interiors_reverse` | 2／5 | 60 | 114 | 54 | 54,54,16,16,0 | 4 | 8 | 2／1 | 二份：1；三份：14 |

r=5,…,8 六例殘留均為零。r*=0 時唯一零點 scope 為空 scope，
relation 是 `{()}`、排除集合為空；它不出現在極小 repair 中。
四例沒有 forced scope。另兩例唯一 forced scope 都是
`S_A=(a0,a1,a2,a3)`，不是兩份最優投影都在任意極小解中被迫。

兩個非平凡例的具名數均為：J=1,440、P=2,736、Δ=1,296；
加所有二點或三點投影後 P_r=1,824、殘留384。
這些數字來自完整 tuple 集合運算；未以同基數、hash 或邊際相同代替相等。

## 2. 全部可用框與拓撲完備性

[Frame 證書](../artifacts/c5_two_vertex_overlap/repair_transport_frames.json)
完整列出六圖原 U 上全部二十條 simple C₅，按起點最小、正反向取一的
固定次序列舉；不是新 class-pair 搜尋。

十四條可用框各附一份整張原圖的 rotation。Checker 逐 dart 追面、
驗連通性及 `V−E+F=2`，並核對指定 C₅ 確為一個面，故可選為整圖外面。
其餘六條各保存兩條只用原邊、互不相交、內部避開 C₅、四端點沿框交錯的
路徑。若全圖都在該框 disk 內，兩條 crosscuts 必相交，矛盾。
因此每條候選都有肯定或否定證書，不靠一個 planarity Boolean 當作完備證明。

| Join | 全部可用框；括號末數為該框 relation 的軌道數 |
| --- | --- |
| `reference`、`shared_chord_frame_edge` | `(a0,a1,a2,a3,a4)`：7；`(a0,a2,b2,b3,b4)`：10 |
| `reference_reverse` | `(a0,a1,a2,a3,a4)`：7；`(a0,a2,b4,b3,b2)`：10 |
| `free_pairs` | `(a0,a1,a2,a3,a4)`、`(a0,a1,a2,b3,b4)`、`(a0,a4,a3,a2,b1)`、`(a0,b1,a2,b3,b4)`：各10 |
| `private_interiors` | `(a0,a1,a2,b4,b0)`：9；`(a0,a4,a3,a2,b2)`：8 |
| `private_interiors_reverse` | `(a0,a1,a2,b0,b4)`：9；`(a0,a4,a3,a2,b2)`：8 |

每例 U 使用原 join 的欄序；尤其 `free_pairs` 留下 b1，其餘控制例留下
b2 或 b0，不能把不同欄名當同一個點。表中兩個私有內點例均使用
`U=(a0,a1,a2,a3,a4,b0,b2,b4)`。

正向例先前保存的 rotation 只有四邊形與六邊形非三角面；本輪新增
同一原圖的肯定 rotation，證明仍有兩條可用五框。既有 A/B 原框阻斷
維持成立。本輪只要求各框分別可作外界，沒有指定新的來源 disk
重疊政策，也沒有枚舉私有內點圖的全部嵌入。

四個 frame-exact 控制例均包含原 A/B 框，完整來源自然接合已給 J；
加入其他 `π_CJ` 不會再刪掉 J。這解釋 P=J，但計算仍逐例獨立重建。

## 3. r* 上的完整排除集合與全部 repairs

對每個 r* scope 定義 `F_S={u∈Δ:u|S∉π_SJ}`。
每個投影均保留 J，故修復 iff `⋃F_S=Δ`。以**完整具名 F_S 集合相等**
分組，再核對它恰為保存的全域軌道集合之展開。相同大小不構成同類。

兩個非平凡例各有七十個四點 scopes、八個排除類。下表按角色對齊，
不是宣稱 scope 或排除集合可重新命名搬運；每類完整軌道 ID 集合、
全部具名 scopes 及投影 relation 都在[完整證書](../artifacts/c5_two_vertex_overlap/repair_transport.json)。

| 角色 | 正向 scope／class | 反向 scope／class | scopes 數 | 排除軌道數 |
| --- | --- | --- | ---: | ---: |
| A | `(a0,a1,a2,a3)`／0 | 同 scope／0 | 1 | 12 |
| 空排除 | class 1 | class 1 | 51 | 0 |
| A 下方小類 | `(a0,a1,a3,b4)`／2 | `(a0,a1,a3,b0)`／2 | 1 | 4 |
| 普通 E | class 3 | class 3 | 13 | 38 |
| T | `(a0,a2,b0,b2)`／4 | 同 scope／4 | 1 | 20 |
| 最優 B | `(a0,b0,b2,b4)`／5 | `(a2,b0,b2,b4)`／6 | 1 | 48 |
| T 下方小類 | `(a2,a4,b0,b2)`／6 | `(a0,a3,b0,b2)`／5 | 1 | 12 |
| 特殊 E，W | `(a4,b0,b2,b4)`／7 | `(a3,b0,b2,b4)`／7 | 1 | 44 |

例如 A 與 T 下方類都排除12軌道，仍是兩個不同的完整集合。
每例對八類的全部 `2⁸=256` 子集合做聯集與逐項刪除，另以完整具名
tuple 集合獨立重算；不先固定 A、T，不只搜尋最小份數。
同一排除類中兩個 scopes 不可能同時不可省，因此全部具名展開是完備的。

正向極小類組合為 `{0,5}`、`{0,3,4}`、`{0,4,7}`；
反向為 `{0,6}`、`{0,3,4}`、`{0,4,7}`。
各展開為十五個無序具名集合，沒有四份或以上的極小解。

令 `A=S_A`、`T=(a0,a2,b0,b2)`，並逐例設定

```text
B_forward = (a0,b0,b2,b4), scope 34
B_reverse = (a2,b0,b2,b4), scope 64
E_family  = {S⊆U : |S|=4, {b2,b4}⊆S} ∖ {B}
```

**各例全部 repairs 恰為 `{A,B}`，以及 `{A,T,E}`（E 遍歷十四個 E_family）。**
Minimum 恰為兩份，唯一最優組合為 `{A,B}`；A 是唯一 forced scope。
這是對七十 scopes 獨立分類後所得，並非套用反向例的答案。

## 4. Forced scope、arity 下界及逐項不可省見證

以下字串都按私有內點例的原 U 次序，屬於該例 Δ。Checker 為每個
見證核對**全部**拒絕 scopes，並對全部接受 scopes 保存一份具名原圖
正常染色；完整八點本身由原圖窮盡延拓拒絕。

| 用途 | 正向 pattern | 反向 pattern | 拒絕它的全部四點 scopes |
| --- | --- | --- | --- |
| 迫 A | `01232113` | `01232112` | 只有 A |
| 不用 B 必用 T | `01201130` | `01212132` | 只有 B、T |
| 迫含原缺邊的 family | `01012122` | `01012122` | 全部含 `{b2,b4}` 的十五個 scopes，即 B 及 E_family |

在每例「加入除 A 外全部六十九份投影」後仍有四個 Δ 軌道留下；
證書保存其完整 ID 集合及上述 forced witness。其他每個 scope
都沒有這種私有排除，且在某個已列出的極小 repair 中缺席。

arity=3 的下界見證可取正向 `01201130`、反向 `01201132`；
各保存全部五十六個三點 scopes 的原圖延拓。arity=0、1、2 也各有
單獨見證及全部 scope 延拓。這證明 P 加所有至多三點投影仍不足。
任意保留 J 的局部條件表都必包含 `π_SJ`，故在原 U、無輔助變數的
局部條件合取模型中，三點以下的較弱條件也不能完成修復。

每例十五組 repairs 共44份逐項刪除記錄，兩例合計**88份**。
每份保存移除的 scope、完整殘留 Δ 軌道集合、具名大小及 witness；
witness 通過所有保留 scopes，由刪掉的 scope 拒絕。
刪 A 後殘留6軌道；二份解刪 B 後42；三份解刪 E 後26；
刪 T 後普通 E 均為8；特殊 W **正向留下4、反向留下2**。
共同 repair 公式不保證相同的逐項刪除殘留大小；相同大小也不代替完整集合。

所有34個極小 repairs（含四個空 repair）各自另掃全部 `4⁸` 賦色，
直接查詢全部框及所選投影，不讀覆蓋 bitmask 或預算好的 P membership。
共2,228,224次域查詢，每組接受的完整 tuple 集合都恰等於原 J。

## 5. Transport 層級及下一步選擇

正反向的十五組具名 repairs 有十三組相同，各有兩組獨有。
窮盡八點的全部40,320個雙射後，恰有兩個能搬運 repair 家族：

```text
τ₁ = (a0 a2)
τ₂ = (a0 a2)(a1 a3)
```

其餘點固定。**兩者都不能搬運完整 J、P 或具名排除資料。**
例如 τ₁ 將正向 J 中 `01201110` 送到反向 J 以外的 `21001110`；
τ₂ 將正向 J 中 `01021112` 送到反向 J 以外的 `02011112`。
兩者都把正向 scope 8 `(a0,a1,a3,b4)` 送到反向 scope 38
`(a1,a2,a3,b4)`：前者排除4軌道，後者排除零。
任何完整排除 audit 同型都必先搬運極小 repair 家族，所以這兩個失敗
已排除所有由 U 頂點雙射誘導的完整 audit 同型。
本輪不聲稱排除其他不保留頂點語義的抽象 incidence 同型。
特殊 W 分支刪 T 的殘留亦不同（正向4、反向2軌道），須保留各例完整集合。

**下一步選共同 repair lemma，前提應是完整排除關係及三種 witness 的
rejector 集合，不能是「圖反向後同型」。** 可抽出的充分條件為：

1. 有只由 A 拒絕的 witness、恰由 `{B,T}` 拒絕的 witness，以及
   恰由 `{B}∪E_family` 拒絕的 witness。
2. `F_A∪F_B=Δ`，且每個 E 都有 `F_A∪F_T∪F_E=Δ`。

這些條件在兩例均已逐集合核對。它們給出相同的短覆蓋推論：每個修復
含 A；含 B 時極小性迫使只有 `{A,B}`；不含 B 時必含 T 及某個 E，
而該三份已足夠，所以極小性迫使恰為 `{A,T,E}`。
圖論上的後續窄題是說明哪個可檢查的來源結構會保證上述條件；本輪
沒有把六個有限控制提升為一般圖定理，也沒有另找新 class pair。

四個 P=J 案例作獨立退化支保存，不能硬加入非空 forced core。
若後續具名資料不滿足上述 signatures，再擴 repair taxonomy。

## 6. 證書、重播與限制

- [Checker](../scripts/c5_two_vertex_repair_transport.py)：標準函式庫；
  從來源代表補回 C₅ 框邊，核對原圖、完整自然接合及全部圖染色。
- [Frame 證書](../artifacts/c5_two_vertex_overlap/repair_transport_frames.json)：
  二十個候選框的逐條肯定／否定證明。發現階段用 NetworkX 3.6.1；
  重播不 import NetworkX、不依賴其 planarity 結果。
- [完整 audit](../artifacts/c5_two_vertex_overlap/repair_transport.json)：
  六份 J/P/Δ、frame relations、arity ladder、完整 scope projections、
  排除類、全部 minimum 及 inclusion-minimal repairs、forced／逐項 witnesses、
  原圖延拓與跨例矩陣。關係以完整全域 S₄ 軌道字串無損保存；hash 只供查核。

證書以 SHA-256 綁定原六份接合、frame witnesses、前輪極小修復及 checker。
反向 J、P、Δ、八類完整排除集合與十五組 repair 逐項符合前輪。
新 artifact 小於1 MB，直接保存；原大型證書不改寫。
新 clone 如缺前輪三點／四點證書，依[導覽](c5_two_vertex_overlap_guide.md)
先重建這兩個輸入，再作只讀重播。

```bash
python3 scripts/c5_two_vertex_repair_transport.py
python3 scripts/c5_two_vertex_repair_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_two_vertex_repair_transport.py --check
python3 scripts/c5_two_vertex_join.py --check
python3 scripts/c5_two_vertex_minimal_repairs.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

實際驗證見[本輪紀錄](history/2026-09-30-c5-two-vertex-repair-transport.md)。
負控制含漏框、缺 dart、交叉路徑失效、漏類、同基數錯誤排除集、漏解／重複解、
錯誤不可省 witness、同基數錯誤殘留及修復 relation。
本輪無新 Lean theorem、`native_decide` 或外部染色定理；不處理輔助變數、
一般 Boolean 條件、其他來源代表、指定區域政策或多步摘要充分性。
`K∞=K≤5` 仍未證。
