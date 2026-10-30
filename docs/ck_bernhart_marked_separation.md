# Bernhart 標記六葉：完整切口契約與保標記反控制

2026-10-30 同日後續：[含標記 bond 的存在性](ck_bernhart_marked_bond_existence.md)
證任一目標來源可作完整 lift 乘二的 diamond 插入，輸出標記不在任何二邊割內。
故全稱含標記 bond 存在性等價於目標來源類空；兩者尚未裁決，也未提供完整目標反例。
下文保留前輪的條件式分離、控制與停止點。
再後續[通用標記與來源限制](ck_bernhart_universal_marking.md)證固定二端構件可將任一無標記 h 來源
乘 12 變成符合目標且無含標記二邊 bond 的來源；原題仍 OPEN，沒有將 MC40 當成目標反例。

2026-10-30，接續 [端點與六葉降階](ck_bernhart_endpoint_ray_continuation.md)。
研究對象是連通 plane near-cubic 六葉網路，容許平行原邊，六葉依既定環序；
外面有具名原邊 f，且每份完整 Tait 染色中，f 在含其顏色的兩個雙色系統皆屬閉圈。
目標來源另要求**全部** `(y,n)=μ(k,h)`、`μ∈6ℤ₊`，k、h 固定為來源文件的六葉降階。

**本輪裁決：閉圈不足以保證二端區域單邊替換後，縮圖仍有雙閉圈標記；一般無標記分離仍 OPEN。**
具名控制 MC40-G45-Y33 的全部 576 份染色滿足外面標記雙閉圈，但唯一無葉二端區域
包含 f；消去後是樹，沒有任何可繼承雙閉圈條件的標記邊。它不符合目標完整 lift，
因此只否定上述一般保標記推法，**不反駁目標 lift 專用分離，更不排除 r₂**。
本輪亦證：對目標完整 lift，**任何含 f 的二邊割若存在，必有無葉側**，可依下述契約安全分離。
尚未由全稱閉圈性證出這樣的割必定存在。

## 1. 具名完整控制：能分離計數，不能自動保留標記

控制名 **MC40-G45-Y33**。完整具名原邊及 rotation 見
[control-input.json](../audits/2026-10-30-bernhart-marked-separation/control-input.json)；
[verification.json](../audits/2026-10-30-bernhart-marked-separation/verification.json)
保存全部染色、729 個 literal word fibres、191 個 signed signatures、實際閉圈交換軌道及完整回寫 fibres。
它有 44 個 cubic 頂點、6 葉、69 條原邊，`f=12=(14,38)`。
六葉外面正序為 `(42,49,48,47,44,43)`；checker 由同一 rotation 逐 dart 走面，
驗連通、球面 Euler 值 2，以及同一外面含 f 和六葉，並非只核抽象圖可平面。

完整枚舉給 576 份 Tait 染色；含 f 的兩個系統共 1,152 次檢查全部為閉圈。
96 個實際交換軌道全為六環。完整 n 有 48 個正字，各 12；完整 y 有 13 個正 signatures，
各 12；所有其餘座標及空 fibres 明列為零。目標 h 有 81 個正字、k 有 23 個正 signatures，
故這張圖的完整 lift 不是任何正比例 `μ(k,h)`，即使其總計數也滿足六倍整除。

窮舉全部 `C(69,2)=2,346` 次二邊刪除，唯一不含原葉的二端原區域為
`U={0,…,39}`，其原切口為 `59=(26,40)`、`64=(32,45)`。f 嚴格在 U 內，既不在切口，
也不在補側。因此沒有另一個可保留同一 f 的無葉二端消去選項。
這兩條 cut 邊本身都是 bridge；U 的補側是兩棵三葉樹，故這是二端區域而不是 bond。
U 連通，補側每個分量皆經原葉連到同一外面，因此補側圖不能藏在 U 的有界面內；
填滿 U 的細 ribbon 鄰域之空洞後，得到只跨這兩條邊的實際 Jordan disk，適用下節契約。

刪 U 後在 40、45 之間接入單邊，縮圖為 4 個 cubic 頂點的六葉樹，完整染色數 48。
每份縮圖完整染色的回寫 fibre **恰有 12 份**原完整染色，逐份保留同一六葉字及三 split
signed-signature tuple，因而全部 n、y 均恰除以 12。樹上每條邊都沒有閉圈，
所以連「另選一條標記邊保留全閉圈性」也做不到。

這是**保標記消去**的完整反控制，同時是**無標記計數分離**的正控制。
此處「保標記消去」要求單邊替換後的六葉縮圖仍有全染色雙閉圈標記。
若只做完整 factor 分離，f 及其原身份仍能保存在 U 的回寫 factor；本控制沒有否定這種表示。
它沒有否定「全閉圈必存在某個無葉二端區域」；本例確有該區域。
也不能把沒有符合目標 lift 的本例升格為 r₂ 的來源或反來源證明。
單邊替換的完整計數倍率是 12，沒有使用 free-edge 分支。

## 2. 條件式二端分離：完整 fibres、signatures 與倍率

以下是「已有實際二端原區域」時的安全手術契約，並未由標記邊的全閉圈性證出該區域存在。
固定同一張連通 plane near-cubic 六葉圖，保留各原邊身份、原 rotation 及葉的環序。
取不含原葉的非空連通 cubic 原頂點集 U，假定其原邊割恰為兩條具名原邊 e₁、e₂，
並有一條只跨 e₁、e₂、內部恰包住 U 的實際 Jordan 曲線。補側圖不必連通；
若兩側圖皆連通，這是 plane bond，其對偶二圈即可提供該曲線。
原葉全在補側，故可在此 leaf-free disk 中做替換。平行原邊分別保留身份。

切開 e₁、e₂ 得 ordered 2-pole R，記 F_R(x₁,x₂) 為兩個端口指定色下的全部完整
Tait extensions。由 `3|U|=2|E(U)|+2` 知 |U| 偶；對每個色數 incident darts，
兩個端口的該色出現數均為偶。因此 x₁≠x₂ 時 fibre 空；兩端必同色。
全域色置換給出三個 F_R(x,x) 的雙射，故其共同大小 t 與色 x 無關。
若 R 可染且 U 非空，固定端口色 x，另兩色 y,z 在 U 上形成非空的完整偶閉圈族；
依最小具名原邊選定其中一圈，交換 y,z 不改該雙色分量的無向邊集，故給無不動點的
involution，t 是正偶數。若不可染則 t=0，須單列，不能除倍率。

刪 U 並在原兩外端之間接入一條具名邊 g，得 core H。若原圖有完整染色，兩外端
不會是同一 cubic 頂點，否則兩條同色 incident cut 邊已違反 proper Tait。
對每個完整六葉 word w，有自然且逐份的 disjoint-union 雙射

\[
F_Q(w)\ \cong\ \bigsqcup_{\psi\in F_H(w)}F_R(\psi(g),\psi(g)).
\]

雙射保留 core 的全部原邊色；反向將指定的**整份** R extension 回填，並非拼接端點邊際。
空 fibres 也包含在公式內。若只任選其中一份 extension，只得到存在性回填，不能聲稱保存
完整解空間。

固定一份完整染色及任一 split ab，令 x=ψ(g)。若 x 不屬 ab，該雙色系統不穿過 cut。
若 x 屬 ab，R 中 e₁、e₂ 同在唯一一條端口到端口的完整 ab 路上；兩端邊同色，故此段
為奇長。將整段替換為一條邊，長度差為偶數；其他 boundary 路均不變。因此每份染色的
全部 boundary signed signatures 保留：sign −1 仍表示奇長／等色端邊。這同時保留同一份
染色的三 split signature tuple，並保留涉及 g／cut 的完整分量究竟是路還是閉圈。
R 內部另有多少閉圈則由完整 extension fibre 計入 t，不能拿普通未加權 PM 數代替。
於是，包括全部零座標，

\[
n_Q=t\,n_H,\qquad y_Q=t\,y_H.
\]

一般替換為另一個相同 ordered 2-port 的 R′，倍率 t′ 時，對每個完整 boundary word、
甚至每個三 split signature tuple 的計數 N，都有 `t′ N_Q=t N_Q′`。只在所除倍率正時
可改寫成商。以單邊替換的倍率是 1；這是本二端手術的 core 邊，不是來源文件的
獨立 free-edge 分支，不能移用該分支的 λ 倍率。

### 標記邊及目標尺度的保留

若標記 f 留在 core，完整分量映射保留其兩個相關系統的閉圈性。若 f 本是 e₁、e₂
之一，則以新邊 g 為標記，同樣保留閉圈性；f 原在外面時，另一條 cut 邊也同在外面，
替換邊可保留外面標記。若 f 在 U 內，上述 boundary fibre／signature 契約本身沒有給出
可繼承的標記；須另證指定新標記在每份縮圖染色的兩系統皆為閉圈。

對本指定 `(k,h)`，若原圖完整 lift 為 μ(k,h)，t>0，則縮圖為 μ′(k,h)，μ′=μ/t。
因 k 的正座標均為 1，完整 y 計數迫 t|μ。若又保留全閉圈標記，固定 boundary word u，
交換含標記邊的實際 xy 閉圈，給三個標記色 fibres 的雙射，故三份各為 `μ′h(u)/3`。
h 有值 1，故 μ′ 被 3 整除。另 `k_empty=1`；六葉全取同一第三色時，另外兩色在非空
cubic 內部形成閉圈，交換一圈無不動點，迫 `y_empty=μ′` 為偶。故 μ′ 仍屬 6ℤ₊。
若未保標記，僅憑 μ∈6ℤ₊ 及 t|μ 不能斷言 μ/t 仍被 6 整除。

## 3. 指定 lift 對含 f 二邊割的實際限制

本節的實際邊割指 `D=δ(A)`，不是任意造成不連通的刪邊集合。
對任意一份完整染色，令 f 色為 x，另兩色為 y,z。若一個實際邊割 D 含 f，
xy 與 xz 的兩條含 f 閉圈各須再跨 D 至少一次。故 f 不是 bridge；若 D={f,g}，
兩個閉圈都只能再經 g，迫 g 同時屬 xy 與 xz，即每份染色均有 φ(g)=φ(f)。
這尚未證有此二邊割。

對本指定 h，完整核對全部 64 個葉子集 A：只有 A=∅、A={0,…,5} 對所有 81 個正
boundary words 都滿足 `XOR_{i∈A}u_i=0`。其餘 62 個 proper 非空子集各有具名正 word
反證，見本輪 verification.json 的 `leaf_split_two_cut_witnesses`；色 1、2、3 視為
F₂² 的三個非零元素。

因此若實際二邊割 {f,g} 的一側含原葉集合 A，對該側 cubic 頂點的 F₂² flow 求和，
給出 `XOR_{i∈A}u_i=φ(f) XOR φ(g)=0`。完整支援包含 h 的全部正 word，迫 A 只能
為空或全部六葉。故此二邊割有一個不含葉的側。

還需核對這是實際二端原區域：原圖連通且 f 非 bridge，刪兩邊後不可能有三個以上
連通分量，否則兩條被刪邊的 quotient 是樹，f 將是 bridge。因此恰有兩個連通側，
leaf-free 側是上述 plane bond 2-pole，確實適用完整安全分離契約，並將標記對應到替換的新邊。
這是**任意含 f 的二邊割若存在，便可安全分離**的條件定理；仍不是二邊割存在定理。

## 4. rank 23 的準確用途：僅控制切 f 後的等色 sector

本輪六葉 incidence 矩陣限制在 k 的 23 個正 signature 欄，有一個 23×23 整數 minor
det=+1，因此欄 rank=23。具名選列、全部矩陣與 determinant 均保存於 verification.json。

固定 split ab，第三色為 c。令 A_S 為六葉圖中 f=c、實際 signature 為 S 的計數；
等價地，由第三色 matching 含 f 的那些完整偶補匹配，按其閉圈填色數加權。
所以 A 是共同 signature 權重，不是任選的逐字邊際。其支援限於 k 的 23 欄。
標記色三 fibres 等勢給 `M₆A=(μ/3)h`；rank 23 迫 `A=(μ/3)k`。
在 f 屬 ab 的另兩部分，沿含 f 的 ab 閉圈交換，保持 boundary word 及 S，
故 f=a、f=b 部分也各為 `(μ/3)k`。

在相鄰外面弧切開 f 成兩條 stems，**要求兩個新葉同色的 sector**與原六葉全部染色
一一對應。原 f 不屬所選 split 時保留 S；原 f 屬 split 時，其閉圈切為新兩葉互配的
奇長路，添入具名 pair `(2,3,−1)`。因此這個等色 sector 的完整 n／signed counts
恰為 `(μ/3)r₂`；比例 μ/3 為正偶數，可由 `A_empty=μ/3` 的另一色閉圈交換看出。

**不能由此宣稱切開後整張八葉圖的全部 lift 是 r₂。** 切一條邊成兩條獨立 stems 會
放寬原本「兩端同色」的約束；切圖可能另有兩新葉異色的完整染色，原六葉圖沒有對應
染色，原圖全閉圈性亦沒有量到這些新 fibres。rank 只決定上述等色 sector，沒有把異色
sector 證空。要得到真正完整 r₂ 八葉來源，須另外證所有異色新 fibres 空。來源文件的
正向封口有原八葉全部支援作前提，不能倒用成無條件逆封口。

本節沒有證一般安全分離存在，也沒有排除 r₂。

## 5. 真閉圈交換的六桶限制

固定完整六葉字 u，取其全部染色為頂點。染色中 f 色為 x 時，分別沿含 f 的 xy、xz
**實際完整閉圈**交換，得到兩個不同鄰點。每項動作可逆、保 u，每點度數恰二，
故有限動作圖是互不相交的環。環上 f 的顏色按三色週期排列；每次交換又翻轉 f 任一端點 p
的 cyclic 色序符號 ε(p)，因此每環長度為 6m。每環六桶 `(f色,ε(p))` 各有 m 份，
兩端符號乘積 ε(p)ε(q) 沿軌道不變。沒有假設不同 pair 的交換可交換。

故 `n(u)∈6ℤ`，三種 f 色 fibres 各有 `n(u)/3` 份且各為偶數；這僅重現目標已允許的
`μ∈6ℤ₊`，未多排任何 μ。固定 signature 的子 fibre 不一定對這些交換封閉，
不能無條件逐 signature 套六桶，也不能由兩種 involutions 推出四倍整除。
控制的 96 個完整六環為此一般紙證的有限實作核對，不是目標 lift 的實現。

## 6. 證據、重播及停止點

一般二端手術、含 f 二邊割限制、六桶引理及等色 sector 的意義是紙面論證。
Python 使用整數與 Fraction 精確消元；23 欄有 det=+1 minor，全部 2,187 個六葉 incidence
方程及 62 個 proper 葉子集反證重播通過。三組額外手術控制以 C₆ 六葉圖的 66 份完整染色
為 core，插入 parallel 2-pole、K₄−edge 2-pole、雙 parallel 串鏈後分別有 132、132、264 份；
完整回寫倍率 2、2、4，逐份保三個 signed signatures。這三組平面插入有直接的局部畫法；
其程式核對是染色及 fibres，獨立於 MC40 的 rotation／面核對。

- [完整 checker](../scripts/ck_bernhart_marked_separation.py)
- [完整證書](../audits/2026-10-30-bernhart-marked-separation/verification.json)
- [具名輸入](../audits/2026-10-30-bernhart-marked-separation/control-input.json)
- [本輪收據](../audits/2026-10-30-bernhart-marked-separation/RECEIPT.json)

```bash
python3 scripts/ck_bernhart_marked_separation.py --check audits/2026-10-30-bernhart-marked-separation/verification.json
```

checker 未使用四色定理、圖庫 oracle 或資源 limit 作裁決，沒有新增 Lean。
文件連結檢查與正式 docs DocGraph 通過；全工作樹 DocGraph 仍因保留的歷史快照有
72 項既存 duplicate-id 而失敗，沒有將正式 docs 通過當成全樹通過。
一般無標記二端區域存在性、目標 lift 的保標記分離、全部允許倍率的實際來源排除均 **OPEN**。
本輪沒有排除 r₂ 或 r₁，76 列新增必零座標仍為 0；free 分支仍另為 `λ(k,h)`，
本輪不混用其倍率。未 commit／push。

文件閉包：本頁為此子題權威來源；端點來源加入後續連結，任務二、4CT 導覽與 STATUS
連入本頁並保留一般分離／射線排除 OPEN。較上層存在性宣稱未變，停止於這些直接 consumers；
HANDOFF 的研究線標記不變。
