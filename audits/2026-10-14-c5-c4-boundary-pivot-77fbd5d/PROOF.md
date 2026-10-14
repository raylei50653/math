# C5 稀疏 singleton 到 C4 diagonal-forbidding 的完整來源轉換

2026-10-14。隔離研究包紙面證明；外部計算信任另見 [EXTERNAL](EXTERNAL.md)。未 commit。

## 結論與前提

設 G 為有限簡單、二連通的 plane disk 圖，指定外框 B=(b0,b1,b2,b3,b4)。
假設：

1. B induced，每個內面為三角形，每個 G 的三角形都界定內面（無有內點的分離三角形）。
2. 每個內點度至少 5，每個邊界點度至少 4。
3. 同一四色框、同一完整延伸關係滿足 y0=y1=0；其中 yi 為 singleton-i 的固定 assignment 全部延伸數。

則可不刪任何原 G 頂點／邊，只增加一個頂點，得到 C4 diagonal-forbidding 的 4-candidate H。
總頂點數 |V(H)|=|V(G)|+1=k+6。

引入 Dvořák–Lidický–Mohar arXiv:2504.08327v2 §2、印刷 pp.24–25 的外部完整計算結果，
可排除 k≤22 的這類 G。故原全域最小目錄外來源正規形的 932／933／941 三支均需 k≥23。
再依既有 no4ct 三支分類／正規形／度數前提，得到 **K≤22=K≤5=K132**；完整反證在 §3.1。
這是新來源橋加外部有界計算；不是新枚舉，不是無界排除，不是本地重播外部程式。

## 1. 構造：只加四條外側 spokes

在 G 的外側 C5 disk 放新點 u，連接 ub0,ub1,ub2,ub4，保留全部原邊。
將新面 Q=(u,b2,b3,b4) 選作外面，得到 H。
等价地，先在球面把 G 加全五 spokes 成 S，再移除 ub3；但直接構造無須先假設 S 可染。

H 的新增內面恰為 u b0 b1、u b1 b2、u b4 b0。
所有原內面照常保留。外面是四個互異頂點組成的 Q；Q induced：ub3 未加入，b2b4 因 B induced 而不存在。

H 中不含 u 的三角形就是 G 的原三角形，仍界定面。
含 u 的三角形只能由 u 的兩個相鄰 B 鄰點生成；因 B 無弦，恰為上述三個新增內面。
所以每個 triangle 確實 facial，這比僅宣稱沒有 separating triangles 更直接符合外部 4-candidate 定義。

H 的內點恰為 G 的原內點，加上 b0,b1。
原內點 degree 不變；b0,b1 各增加一條 u 邊，故其 H-degree 至少 5。
u,b2,b3,b4 是外點，外部定義不要求這四點 degree 至少 5。
因此 H 為 simple 4-candidate；由 induced Q 或頂點數立即知道不是 diamond。

這項 topology/degree 證明不使用 4CT、不使用 count-cone 猜想、不使用 G 的 edge-criticality。
它使用的是上述明列的 normal-form 與 degree 結論，不能套任意固定 mask 最小來源。

## 2. 同一完整來源的全部 fibres

固定 Q 的一份 proper assignment q=(q_u,q_2,q_3,q_4)。
令 F_G(b) 是 G 在固定 B assignment b=(b0,...,b4) 的全部完整染色集合。
則 H 的完整 fibre 有 literal disjoint-union bijection：

F_H(q) = disjoint union over b:
  b2=q2, b3=q3, b4=q4,
  b proper on B,
  b_i != q_u for i in {0,1,2,4},
  of { f union {u -> q_u} : f in F_G(b) }.

不同 b 的原頂點色值不同，故聯集互不重疊。映射 inverse 就是限制到原 G。
這保留原 G 的所有內點、邊、literal boundary labels，並完整接合所有相容的 full lifts，包含空 fibres。
不宣稱每份原 G 染色都相容於新增的四條邊。
没有獨立選取多個 marginal witnesses，也沒有將三角化圖的 existential extension 當成原 G 染色。

令四個 C4 fixed-assignment types 依序為
ABAB=(0,1,0,1), ABAC=(0,1,0,2), ABCB=(0,1,2,1), ABCD=(0,1,2,3)，
位置順序均為 (u,b2,b3,b4)。逐一列出剩餘兩個原色值 b0,b1 得到：

n_H(ABAB) = 2 x24.
n_H(ABAC) = y3 + x02 + x14.
n_H(ABCB) = y0 + y1.
n_H(ABCD) = y2 + y3 + y4.

每個值仍為一份固定 assignment 的計數，不乘 4、6 或 24。
ABAB 的 2 是原 b0,b1 的兩種異色順序；在原同源完整 fibre 中真有兩份 disjoint preimages。

第三列可以完全不靠計數恆等式直接看：指定 Q=(A,B,C,B)，u=A。
原 b0,b1 都不能用 A（u 邊）或 B（原 b4b0、b1b2），且 b0b1 是原邊，
所以只可能 (b0,b1)=(C,D) 或 (D,C)。原 B 分別為 (C,D,B,C,B) 或 (D,C,B,C,B)，
其 singleton 分別恰為 b1 或 b0。這兩份 preimages 的全部full lifts正是上式 y1、y0。

尤其若 y0=y1=0，H 的 ABCB fibre 全空。這是完整 C4 來源的 diagonal-forbidding，
不是只把必要計數向量投影。

932、933、941 三支共同 y0=y1=y3=0 且 x24>0。
因此 932 的完整 C4 支援恰為 mask 3，933／941 恰為 mask 11（上述 bit 次序）。
若沿計數恆等式令 c=x24，a=y2，b=y4，則四態 counts 為
(2c,2c+a+b,0,a+b)。a=b=0 對應 932，933 為 a=0,b>0，941 為 a,b>0。
計數恆等式只用於這個最後簡寫；diagonal-forbidding 已由 fibre 公式直接成立。

## 3. 外部結果的正確身份

Primary source:
https://arxiv.org/pdf/2504.08327v2
Title: On a conjecture concerning 4-coloring of graphs with one crossing.
Authors: Zdeněk Dvořák, Bernard Lidický, Bojan Mohar.
Version date: 2025-04-14.

Local supplied PDF:
audits/2026-10-13-singleton-literature-6cafdfb/sources/one-crossing-2504.08327v2.pdf
SHA256: 7592926ac2f9586ab792be41463496f12726ffaeb1a824a7e3ad600dc8adca72

原文定位：
- 印刷 p.13 §2 開頭：candidate 是外 cycle、全部內面三角形、每個 triangle facial、全部內度至少5。
- 印刷 p.24 §2 末段與註1：作者宣稱完整生成所有 ≤28 頂點 4-candidates；沒有 rainbow-forbidding；
  diagonal-forbidding 只有四點 diamond。C++ 實作達28，另一 Python/Sage 實作獨立核對至25。
- 印刷 p.25 Table1：逐階數統計與相同結論；28 是全部頂點數，包含四個外點。
- 印刷 p.2：separating subgraph 由刪除全部其頂點後不連通定義。
- Theorem10 是 equivalence；不能把它本身當無界 coloring theorem。

本推導直接用 §2 的完整 4-candidate 計算結論，不需要先繞到 Theorem10 的 one-crossing 等價，
也不使用該文未證 Conjecture2。文獻將這次完整枚舉稱為 computer-assisted proof；
目前未取得正式 journal publication 身份，故標成 arXiv v2 的外部已報完整計算結果。
其原始程式／完整枚舉未在本輪重播。

若 |V(H)|≤28，H 既非 diamond 又 diagonal-forbidding，與該外部計算結論矛盾。
故 k+6≥29，即 k≥23。界是 ≤28，不是 <28。

no4ct 信任邊界：本地轉換未使用 4CT。已逐段檢閱 §2 的 generation completeness：
Observation18、Lemma19、Observation20、Lemmas21–24 到 Corollary25 使用平面性、度數、
discharging 與具名 reductions；不經 §1 的4CT-dependent Theorem10／Corollary17。
因此此处直接引用完整 4-candidate 生成及染色檢查。外部程式及完整計算仍未由本 repo 重播，
不能把 paper-dependency 核對寫成 independently verified external computation。

### 3.1 從全域最小來源得 K≤22=K≤5

令 K 為132份具體五內點以內 witnesses 的完整關係集合。這給 K⊆K≤5。
反設存在內點≤22且關係不在K的來源；在所有目錄外來源中取全域最少內點 k，
再於該k取最大邊数。由存在的反例知 k≤22。

[凍結 no4ct 分類 §§4–5](frozen/audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)
給出共同 D5 像的932／933／941、二連通、無框弦與內面三角化；
[凍結度數修復 §4](frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
給框度≥4、內度≥5及無帶頂點分離三角形。共同搬運整張原圖到固定標號後，
三支均 y0=y1=0。套 §1–2 得不是diamond的diagonal-forbidding 4-candidate，
其總點數 k+6≤28，與本節外部有限結果矛盾。因此 K≤22⊆K，
結合 K⊆K≤5⊆K≤22 得 K≤22=K≤5=K。

該反證是全域最小反例的存在正規形；不宣稱每份指定來源逐步保持同一Σ變成H。
但一旦選定這份G，§2轉換保留G全部頂點、邊、實際色框及完整fibres。
輸入正規形／度數是既有一般紙面定理，checker的132控制並不取代它們。

## 4. 933 的獨立 one-crossing 描述

對 933，可把全五 spokes 的 S 加上 b1b3，令 b1b3 只穿 ub2 一次，得 X。
S 的每份染色限制原 G 都只能是 y4；該列 b1=b3，故 X 無四色染色。
S 是無 separating triangles 的簡單 sphere triangulation，故4-connected；加邊保持4-connectivity。
X 全部 degree 至少5。此為原文 Conjecture2 的特例，但只能用其已計算≤28域。
這一較直觀描繪不處理941；共同 C4 投影已同時處理933／941／932。

## 5. 可執行驗證與未證範圍

python3 -B audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/controls/check_transfer.py --check

checker 独立枚舉全部固定 C4 assignment 的 C5 六點 cap 選擇，驗證4×10完整計數矩陣；
全部1024抽象支援檢查轉換；132個舊具體 C5 witnesses 則逐份枚舉真實 G full fibres，
用 S4 完整搬運＋只加 u 取得 H fibres，另以 H 上 MRV independent search 完整逐集合比較，
共528份完整 fibre comparisons，含空 fibres。counts及完整集合hash保存 [certificate](controls/certificate.json)。
負控制檢查錯誤開 ub2 與誤把 ub3 接回確實改變矩陣／fibres。
沒有任何真正932/933/941來源正控制，target not triggered；三個抽象向量不是圖。

這填補舊 literature audit 明列缺少的 C5→C4 source bridge；舊 audit 已列外部定理，
但未給此同源 cap-opening 構造與 degree／facial-triangle 接入。
無界的新窄中介題是：
「outer Q=(u,a,b,c) 的 4-candidate，u degree4，且其兩個內鄰點沿 link 連續；
是否必有 a=c、u!=b 的 diagonal 延伸？」
我們來源的 u-link 恰為 b4,b0,b1,b2，所以落此帶標記子類。
一般外部 diagonal conjecture 足夠但更強；本輪只取得≤28的外部有界結論，無界仍OPEN。

## 6. 多洞普通正接合的限制（旁支結果）

F4=C5加 chords14,24 的 fan，完整support為165，包含於933與941。
F2 的完整support為424，也包含於941。
固定任意有限 plane context，帶r個互不相交內部的簡單具名C5洞，洞邊界始終五個不同點，
各G_i只與context共享該洞邊界；任取literal alignment。將每個來源改為其內含fan F_i。
若全部fan填充後的圖有一份完整染色，限制每個洞得到一份F_i支援內的邊界assignment；
由包含關係各自取同assignment的G_i完整lift，與同一context染色接回。
所以「all-fan填圖可染 ⇒ 原來源填圖可染」不需要4CT，且適用任意洞數。
若最後是無loops的閉合平面圖，4CT保證all-fan填圖可染；故這種任意多copy普通正接合
不能把933/941轉成零染色矛盾。帶固定outer pins時須真的有all-fan延伸，4CT不自動供給。
這比舊單次B5-pairing限制涵蓋更一般多洞，但不是新來源排除；C4方法得益於度數／無非面三角形
結構，不是企圖用純support閉合製造零染色。
