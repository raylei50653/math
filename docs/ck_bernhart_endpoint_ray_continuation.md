# Bernhart：RIP 共同端點補證與 r₂ 射線來源研究

2026-10-30 後續：[標記六葉與安全分離](ck_bernhart_marked_separation.md)
補完整二端 fibres／signed signatures／倍率契約，並證含 f 二邊割若存在必有無葉側。
具名全染色控制否定單邊替換後自動保留閉圈標記；其完整 lift 不符靶標，
一般無標記二端分離、目標來源排除及 r₂ 仍 OPEN。
同日再後續：[通用標記與唯一 lift](ck_bernhart_universal_marking.md)補無標記六葉來源到標記目標的
完整倍率 12 構造，因而 free-edge 分支也可正向化約到標記目標非空性；仍未排除 r₂。

2026-10-29。接續 [retained 共同原邊交會](ck_bernhart_retained_intersection.md)與
[跨 split 稽核](ck_bernhart_cross_split_audit.md)。本頁承擔完整 RIP 的當前公式，
及選定第二個 41 列 full lift 的全來源必要條件；舊報告與 frozen 證書保留原版本。

兩項驗收分開：**RIP 補證完成；射線來源排除仍 OPEN。**
前者有一般紙證及全部既有未涵蓋案例的精確重播；後者取得適用所有候選來源與比例的
共同配對、合法六葉封口命題，但尚未證這些必要條件必然矛盾。
沒有排除一整條射線，原 76 列新增必零座標仍為 0。

## 1. RIP 的共同端點公式及適用範圍

固定一張有向 plane near-cubic disk、同一份 proper Tait 染色及同一條完整 ab
boundary-to-boundary 原路徑 S。切開 S，使用由原 rotation 決定的共同側別、每側真實環序。
P 是該側一個完整 retained ac 分量，Q 是一個完整 retained bc 分量；保留全部路徑及閉圈、
每條共同 c 原邊身份。一般定理不要求兩路端點互異。

### 正向與推離規則

每側邊界取正向，即該側內域在行進方向的左邊。令 ε(v)=+1 表示原 cubic 頂點
的逆時針色序為 (a,b,c)，反序為 −1。H=∂P∩∂Q 的共同端點只能是
cut port 或原始 c 邊界葉；兩個系統在每個共同端點都沿同一條原 c 邊結束。
不可能只有共同端點而沒有共同 c 邊：該端點剩餘度數為一且唯一邊色為 c。

共同端點用很小的邊界 collar 拆成 P、Q 的兩個終端。規則如下。

- rotation 推離：共同 cut port ε=+1 時沿正向排 P,Q，ε=−1 時排 Q,P；
  這相當於將 P 終端放在原 a dart 所在一側、Q 終端放在原 b dart 所在一側，
  保留原 (a,b,c) 的 cyclic rotation。
- 原始 c 葉沒有原 cubic ε，明定用正向 P,Q；不能把下面的人造 cap 符號說成原葉的 ε。
- canonical 推離：全部共同端點一律沿正向排 P,Q；與 rotation 推離相差的恰為
  ε=−1 的共同 cut ports。

為驗正負號，取局部座標：邊界為 y=0、內域 y>0、正向由左往右。
在 (0,δ) 放人造 cubic cap，a 支向 (−δ,0)、b 支向 (δ,0)、c 支向 (0,2δ)。
從 cap 觀看逆時針色序為 (a,b,c)，故正向 P,Q 的 cap 符號 η=+1。
互換兩終端則 cap 符號變 −1。這推導同時決定了公式中的號，沒有任選每個端點的 ε。

### 兩個等價公式及邊界修正

將原 cubic 頂點保留 ε，原始 c 葉的 cap 值明定為 +1，記為 barε。
令 C=E(P)∩E(Q) 是共同原 c 邊的集合，每條邊只計一次，定義

\[
L=\sum_{uv\in C}[\bar\epsilon(u)=\bar\epsilon(v)],\qquad
B=\sum_{v\in H\cap\operatorname{ports}(S)}[\epsilon(v)=-1]\quad(\bmod2).
\]

則完整 RIP 為

\[
\boxed{L=\operatorname{Alt}_{\rm rot}(P,Q)},\qquad
\boxed{L+B=\operatorname{Alt}_{\rm can}(P,Q)}\quad(\bmod2).
\]

Alt 是相應推離後四個互異終端的交錯指標。若至少一個分量是閉圈，沒有共同端點，
仍沿用舊 RIP、右側為零；兩個路徑在不同側時也無共同原邊，值為零。
四端點原本互異時 H 空、B=0，回到舊式。

**證明。** 先按 rotation 規則在每個共同端點添 cap、把同時結束的兩條曲線分開。
cap 是局部平面 collar 操作，不更改鄰域外的共同原 c 邊。每個 cut-port cap 的
cyclic 色序等於原頂點 ε，葉 cap 的符號依明定為 +1。新終端全部互異。
每條共同 c 邊的 ribbon 兩端附件交錯，當且僅當兩端 cap／內點符號相同；
不同 c 邊有不相交 ribbon 鄰域，鄰域外曲線不相交。故總交叉奇偶等於 L。
disk 中兩 proper arcs 的交叉奇偶等於邊界四端點的交錯，得到第一式。
此處引用舊 RIP 證明的局部 ribbon 計算，並沒有假設未知來源的特殊路徑長度。

從 rotation 推離改為 canonical 推離時，每個 ε=−1 的共同 cut port
恰互換一對相鄰的 P、Q 終端，交錯指標因此翻轉一次；其他端點不變。
因此 Alt_rot=Alt_can+B，得到第二式。
亦可直接把共同邊邊界端點的有效符號改成 +1：因為
[x=y] 對任一端點符號翻轉恰改一次，而每個共同端點恰接一條共同 c 原邊，
總交叉數從 L 改成 L+B。這給出同一公式的逐邊核對。

共同 c 邊兩端都在邊界時沒有例外：leaf–port 只累加 port 項；
port–port 分別累加兩個 port 項，即使落在同一條原邊仍不能漏一端；兩次翻轉會抵消；
leaf–leaf 的 barε 兩端皆 +1，該邊貢獻 1，P,Q,P,Q 恰交錯，B=0。
這也涵蓋 P、Q 是同一條單邊路徑的情形。

此定理只對同一實際 disk、同一染色、同一切口的具名完整分量成立；它是必要條件，
不證平面來源充分性，也不從一個失敗 extension 排除所有射線來源。

## 2. 選定 r₂：完整支援的全稱限制

只選 [原分解](ck_bernhart_cross_split_audit.md#3-精確非極端分解及兩個較小子靶)
中第二個 primitive full lift r₂，不更換 lift，也不逐字改選來源。
假設一張同一實際來源 Q 的**全部**計數為 (y,n)=λr₂，λ∈2ℤ₊。
以下條件不截斷頂點數、路長、內圈數或比例，也不假定不同染色使用相同的原路。

完整 46 個正 signed signatures 各 primitive 權重 1，唯一分成 23 對
(S, S∪{(2,3,−1)})；S 不含端口 2、3。所有 243 個正 literal words 均 w₂=w₃。
對六端口順序 (0,1,4,5,6,7)，定義 h(u) 為任意插回共同色 x 的八字計數；
三個 x 的值完全相同。729 個六字中 648 個為零、75 個值 1、6 個值 2，Σh=87。
刪除 (2,3,−1) 並重標後的 23 個正六葉 signatures 各取 k_S=1，其他為零；
完整六葉 incidence 方程也成立。這些是固定資料的精確等式，並不自行拆分原圖。

### 全來源引理 A：同圖三個 fibres 等勢

設同一實際 plane near-cubic disk Q 的全部 (y,n)=λr₂，λ>0（不需先用偶性）。
固定任一完整 Tait 染色 φ。因零字無染色，φ 在 e₂、e₃ 上有共同色 x。
取 y≠x。完整 xy 系統中 e₂、e₃ 所在的路必互相配成 e₂–e₃：其實際
signed signature 為正權重 signature，而上列 23 對已覆蓋全部允許 signature。
因此交換這條**同圖實際完整路**的 x、y，保持其餘六葉，將共同色 x 改為 y。
逆交換是在所得染色的同一條無向原路上，故是雙射。對每個固定六葉 word u，
三個共同色 fibres 各有 λh(u) 份完整染色。此敘述對所有允許來源和所有 λ 成立，
不把不同染色的路徑拼接在一起，也未聲稱三條交換可選成相同原路。

### 全來源引理 B：相鄰二葉的封口與標記邊

先假設 e₂、e₃ 的 leaf edges 分別接不同 cubic vertices p、q。兩內端點必互異：
若相同，proper Tait 在該點不可能給兩條不同 incident 原邊相同色。刪除兩葉及
兩 leaf edges，在原葉間**不含其他葉的相鄰外邊界弧**附近添入 p–q 邊 f，沿原兩
leaf stems 及該弧走線。其餘原邊與 rotation 保留；p、q 的 f dart 佔被刪 stem
的原 rotation 位置。這是同一 disk 中的平面封口；f 可以與舊邊平行，不把它們
當同一原邊。所得 Q̂ 是容許平行原邊的六葉 near-cubic disk，f 是具名標記邊；
即使原來源另限簡單圖，這項必要降階的六葉目標類也須容許平行邊。

每份 Q 染色將兩相同色 stems 合成同色 f，得一份 Q̂ 染色；反向切開 f 亦唯一。
Q̂ 的任意完整染色切開都給 Q 的完整染色，因 Q 的全部計數假設而落在原支援。
故這是**全部**染色的一一對應，並非只對選定 fibres。對每個六葉 u，
`n_Q̂(u)=Σ_x n_Q(u with x,x)=3λh(u)`。

完整 six-lift 也可精確寫出。將 23 對中的 S 依剩餘葉序 `(0,1,4,5,6,7)` 重標，
得 k 的 23 個正六葉 signatures，權重均 1。固定任一 split ab 及與 S 相容的六葉
word u；以 c 為第三色。f 色為 c 的染色，切開後的八葉 signature 是 S，計數
λk(S)；f 色為 a 或 b 的兩個互斥子族，切開後 signature 都是
`S∪{(2,3,−1)}`，各計數 λk(S)。封口只把這條已迫出的路關成偶閉圈，不改其他
邊界路或其長度奇偶，所以新六葉 signature 仍恰是 S。故
`y_Q̂(S)=λk(S)+2λk(S)=3λk(S)`；原權重為零的 signatures 在封口後也逐項為零。
這裡使用的是「固定 compatible boundary word 下、實際完整 Tait 染色的 signature
計數」等價於 y 的定義，並非把 y 當普通 PM 數。於是全部 `(y,n)_Q̂=3λ(k,h)`。

更強地，對 Q̂ 的任意染色，令 f 的色為 x。對每個 y≠x，f 必在 xy 系統的
**閉圈**上：若它在 boundary-to-boundary 路上，沿 f 切開將把該路分成兩條路，
使原 Q 中 e₂、e₃ 各配到其他葉；這與引理 A 的完整 signature 互配結論矛盾。
原 e₂–e₃ 奇長路在封口時以一條 f 取代兩條 stems，長度減一成偶圈；
反向切開長度加一，與原 signature 的 sign −1 一致。此處閉圈包括平行邊
所成二圈；沒有假設閉圈是面邊界、沒有內部附件，亦沒有收縮它。

#### leaf-to-leaf 例外

若 e₂ 的 leaf edge 直接接另一葉 eⱼ，則該原邊是獨立分量，可任意改其色而
保持所有其他原邊。Q 有完整染色且每份均 e₂=e₃，迫 j=3。此時 e₂e₃ 本就是
獨立 free edge。可刪此分量得到真正六葉圖 Q₆；三個共同色 fibres 均直接等於
Q₆ 全部 fibres，因此 `n_Q₆(u)=λh(u)`。若欲統一保留總計數 3λh，則封口對象
必擴充為「Q₆ 加一個無頂點、三色可選的獨立標記圈」，這不是通常有限圖的
near-cubic disk，必須明說，不能默認成普通標記邊。連通且有 cubic interior 的
來源不會有這個 leaf-to-leaf 分支。若 e₂、e₃ 分別是不同 free edges，其顏色可
獨立改變，立即違反全支援相等性，因此不允許。

free edge 分支直接刪除後，完整六葉 lift 為 λ(k,h)，包含原權重為零的 signatures。

因此，若能獨立排除六葉 lift (k,h) 的全部正偶比例實際來源，即可排除 r₂；
目前尚無此六葉全稱排除。若來源類允許不連通圖，任何實際六葉 μ(k,h) 來源
加一條獨立 free edge 都給八葉 μr₂ 來源；這項反向構造的連通性限制不能省略。

封口後同一標記邊在每份染色的兩個相關系統中皆在閉圈，是保留原來源的必要條件。
尚未證它迫出可剝離的二端分量，不能無條件刪邊或將圈收縮成 plane vertex：
圈內外仍可能有原附件。也沒有證所有這類六葉來源都有違反完整 RIP 或零權重後繼的切口。

## 3. 共同 token 與全部同 pair 交換，這一鬆弛仍無矛盾

為檢查「再補同字聯合狀態與分量交換就會排空」的推論，構造一份**形式模型**。
它沒有實際原圖、原邊、retained 接線或 rotation，不稱為真同圖交換。

每個正八字 w 設 n_w 個 primitive ranks；三個 split 各將這些 ranks 與其排序後的
全部正 signatures 一一對應，得到同一 token 上的三份 signatures。
再加二值 b，得到比例 λ=2 的 522 個 tokens。固定 pair 的 signature 不變，
交換任一路徑子集時翻該配對兩端的 boundary 色，移至目標字同一 signature 的 rank；
b 不變。全部子集動作構成同 pair 的布林群，包含逆交換及任意同 pair 的組合。
另設一個形式閉圈動作翻 b；全路徑交換再翻 b，恰等於全域 pair 換色。
全域 S₃ 對字作色置換、對 b 加置換奇偶，形成無不動點的全域色群作用。

模型逐項保完整 n/y marginals、共同三 split tokens、同 pair 全部分量子集作用及色群相容。
對 λ=2m，只取 m 份有標號的同模型，動作保留副本編號；故這個鬆弛對**每個正偶比例**均非空。
這證明上述 token 層條件本身尚未迫矛盾，並沒有給出任何 λ 的實際來源。
尤其沒有三 split 在同一原邊上的共同交集、原 rotation 或切口的真實側別，不能據此說
完整 RIP 對射線無效，也不能宣稱「射線來源排除為假」。

## 4. 有限驗證、證據層與重播

RIP 及全來源封口／雙射為紙面證明；Python 核對固定來源與固定 lift。
未新增 Lean，未修改主求解器或前輪 frozen 程式／證書。

舊 checker 的兩側 order 都沿切口起點到終點列 ports；在這兩個 frozen 來源族中，
side 0 內域在右、side 1 內域在左。新 checker 將舊 side 0 反轉，取得公式要求的正向環序。
一般輸入須由自身 rotation 決定方向，不能把這項 side 編號慣例外推。
另按原葉序收口到共同外部頂點，驗證 marked boundary；僅核 open graph genus 不夠。

| 真平面來源 | 舊已覆蓋重核 | 共同端點新覆蓋 |
| --- | ---: | ---: |
| 兩份 ray-local、四條切口 | 40 | 16 |
| C₈ wheel、43 染色 344 切口 | 3,056 | 1,432 |
| C₈ wheel stack、43 染色 344 切口 | 4,068 | 1,560 |
| 合計 | 7,164 | 3,008 |

原未涵蓋的 **16＋2,992 全部通過**。local 新分支含 12 組單 port、4 組雙 port；
wheel／stack 含 1,344 組單 port、144 組雙 port、672 組 port＋leaf、832 組單 leaf。
四組新增共同端點負控制只反轉一個非切口 cubic 頂點的 rotation，保持原圖、染色、
完整 retained 表與環序；兩個公式皆拒絕，marked 邊界收口 genus 由 0 變 1。
舊 theta 及非共同端點 rotation 正負控制也完整重播保留。

- [端點補式 checker](../scripts/ck_retained_endpoint_parity.py)、[完整證書](../audits/2026-10-29-bernhart-endpoint-ray/endpoint-parity.json)。
- [r₂ 全支援／形式作用 checker](../scripts/ck_bernhart_ray_source_support.py)、[完整證書](../audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json)。
- [本輪驗證及治理紀錄](history/2026-10-29-bernhart-endpoint-ray.md)、[收據](../audits/2026-10-29-bernhart-endpoint-ray/RECEIPT.json)。

大型端點證書按[封存規則](../audits/README.md#新-checkout-的還原)保留原 bytes；新 checkout 先還原：

```bash
python3 tools/audit_archive.py restore --artifacts
python3 scripts/ck_retained_endpoint_parity.py --check audits/2026-10-29-bernhart-endpoint-ray/endpoint-parity.json
python3 scripts/ck_bernhart_ray_source_support.py --check audits/2026-10-29-bernhart-endpoint-ray/r2-support-actions.json
```

## 5. 分開驗收與下一個精確義務

**RIP 補證完成：** 原定有向 near-cubic disk、同染色、同實際切口的全部 mixed
retained 分量，包含共同 cut ports、原葉及同一條單邊分量，都有明定推離及修正項。
紙證為一般結論；16＋2,992 案例與正負控制為有限實作核對。

**射線來源排除 OPEN：** 本輪沒有覆蓋「所有允許來源、所有正偶比例必矛盾」的最後一步。
已覆蓋全部來源與比例的是共同配對、三色 fibres 雙射及六葉封口的**必要性**。
尚需從實際標記六葉來源的全支援與同圖交換，證有切口違反完整 RIP／共同側別，
或出現零權重後繼 signature；也可另證六葉 lift 全部正偶比例不可實現。
所給形式 token 模型不填補這個原邊／rotation 缺口。

未排除 r₁ 或 r₂ 的整條射線，沒有新必零座標；即使日後 r₂ 全排除，也不能直接推出
原 76 列面上任一座標必零。單 split `LOCK-NO-GAIN` 與古典 Bernhart C 還原的範圍不變。
本輪未 commit／push。
