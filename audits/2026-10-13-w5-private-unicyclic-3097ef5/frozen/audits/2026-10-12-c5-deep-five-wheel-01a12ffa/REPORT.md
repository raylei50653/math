# 最小目錄外來源必有全內部五輪，且至少七個五度內點

2026-10-12。本輪是接續研究的隔離交付；BASE 為
`5d70a39940182ea37c9ca5d36d9ebb7f612160ad`。來源與 SHA256 見
[INPUTS.json](INPUTS.json)，未覆寫上游證書、共用文件或其他工作。

沿用 [最小來源度數界](../../docs/c5_saturation_degree_bound.md) 的完整前提，
本輪條件性紙面結論是：

\[
\boxed{D_B\ge21,\quad n_5\ge7,\quad
\exists v\in V(G)\setminus B:\ \deg_G(v)=5,\ N_G(v)\cap B=\varnothing.}
\]

因此可選取一個中心及五個鄰點**全部為原內點**的 induced 五輪。
另證每個 C4 的有界內部為空；每個異於原框的 C5，其有界內部為空或恰為
單一五輪中心。這些結論仍沒有給出保留完整 Σ 的五輪縮減。

## 1. 精確前提及替換語義

固定有限簡單平面 disk 來源與有序具名外框
\(B=(b_0,b_1,b_2,b_3,b_4)\)。Σ 是四著色的完整十列 S4-orbit 延伸關係；
只共同更換色名，不各自重新正規化組件或介面。

假設目錄外來源存在，在所有 \(\Sigma(G)\notin K\) 的來源中，先全域最小化
內點數 \(k\)，再最大化邊數。沿用前輪已證：

- \(K\) 有 132 個關係，各有至多五內點的 disk 代表，且對聯集封閉。
- 普遍 screen、4CT、共面正規形及十二內點界，给出 \(k\ge13\)，G 二連通、
  chordless-C5、內面全三角形。
- 原內點度數至少五、原外點度數至少四，沒有包住頂點的三角形。
- 任意有序 C4 disk 完整關係有至多三內點代表。

十二內點界沿用 [共面正規形](../../docs/c5_cofacial_normal_form.md)；其外部依賴
是 Dvořák–Lidický 的 [Corollary 20](https://arxiv.org/pdf/1907.04066v2)，
界限是對偶頂點数**少於三十**。本輪核讀該界限，沒有重播論文的計算證明。
這些前提不由本輪有限控制重新證明。

對一條簡單環 C，取有界內域及 C 作為 cap。其嚴格內點都是原 G 的內點；
Jordan 分離確保這些點的 G-degree 就是 cap-degree。
若以同一有序 C 上完整關係相等的 disk 替換 cap，則保留原 Σ：
任取整圖著色，先保留外部和 C 上的實際四種色，再取替換 cap 的一份延伸；
反向同理。此處需要所有介面 assignments，包括空 fibres。
不要求新舊內部著色數相等或形成雙射。

替換不識別不同框點，可依原 rotation 填回；若與外部邊產生平行副本，
保留一份即可，原框邊保留。新來源不必維持三角化或度數下界，因為全域最小性
比較的是**所有** disk 來源，而非只比較這個正規形。

## 2. 排除包住內點的四環

設 C4 cap 有 t 個嚴格內點。若 \(t>3\)，換成至多三內點代表會保 Σ 並減少
原內點，與最小性矛盾。因此 \(t\le3\)。

設 cap 的框內弦數為 q，內點間邊數為 i，內點至 cap 框的邊數為 j。
Euler 及三角化给出

\[
E=3t+5,\qquad i+j=3t+1-q.
\]

由每個嚴格內點 degree 至少五，

\[
5t\le2i+j=i+3t+1-q,\qquad i\ge2t-1+q\ge2t-1.
\]

當 \(t=1,2,3\) 時，這都超過簡單圖的 \(\binom t2\) 上界。
故 **每個 C4 都沒有頂點嚴格位於有界內部**。環本身可有對角線；結論不是
「圖中不存在四環」。

## 3. 每個 proper C5 只可能包住一個五輪中心

令 C 為異於 B 的 C5。因 B 無 chord，C 至少使用一個原內點。這個點現在
位於 cap 框，故 cap 嚴格內點數 \(t<k\)。全域最小性使 cap 的關係在 K，
可用至多五內點代表替換；再用最小性，得 \(t\le5\)。不能對 C=B 使用此步。

一般長度 b 的三角化 disk 有

\[
E=3t+2b-3,\qquad
i+j=3t+b-3-q,\qquad i\ge2t-b+3+q.
\]

取 b=5，得到 \(i\ge2t-2+q\)。若 \(2\le t\le5\)，每個嚴格內點必有
cap 框鄰點，否則 degree 至多 \(t-1\le4\)。所以嚴格內點的 induced graph
在繼承嵌入中是 outerplane：其每點通向 cap 框的邊證明該點鄰接無界面。
簡單 outerplanar 圖（包括不連通情形）有 \(i\le2t-3\)，矛盾。

只剩 t=0 或 t=1。t=1 時唯一內點必接五個框點，且 Euler 迫 q=0；cap
恰好是 W5。因此：

\[
C\ne B\quad\Longrightarrow\quad
|V(\operatorname{int} C)|\in\{0,1\},
\]

非空時就是 degree-5 中心的五個面三角形。

## 4. 外圈接觸與深處五度點的精確計數

若原內點 x 接兩個不相鄰外點 a,c，令短框弧為 a-b-c。四環 a-b-c-x 的內部
由 §2 為空，必由對角線 bx 三角化，因 ac 是禁止的外框 chord。
兩個面 abx、bcx 填滿 b 的 disk 側扇區，因此 b 只有 a,c,x 三個鄰點，
與 \(\deg b\ge4\) 矛盾。

故每個原內點至多接兩個外點，而且兩者必相鄰。對每條框邊，其內側面三角形
提供一個共同內鄰。若還有第二個共同內鄰，兩個同側三角形中較大的一個
包住另一個第三點，違反沒有 occupied triangle。五條框邊的共同內鄰互異，
否則某點會接至少三個框點。所以**恰有五個內點各接兩個外點**。

令 L 是有外圈鄰點的原內點集合，並設

\[
D_B=\sum_{b\in B}\deg_G b,\qquad
X=\sum_{v\notin B,\ \deg v\ge7}(\deg v-6),\qquad
h=|\{v\in L:\deg v\ge6\}|.
\]

原框與內部間有 \(D_B-10\) 條邊。L 每點貢獻一條，恰有五點多貢獻一條，故

\[
|L|=D_B-15.
\]

Euler 的 \(n_5=D_B-14+X\) 減去 L 中 \(|L|-h\) 個五度點，得到

\[
\boxed{n_5\bigl(V(G)\setminus(B\cup L)\bigr)=1+X+h\ge1.}
\]

因此至少有一個 degree-5 原內點 v 完全不鄰接 B。其五個循環鄰點互異，
由五個 incident facial triangles 接成全內部 C5。非連續鄰點間若有 chord，
該 chord 與 v 形成的三角形兩側都有其他鄰點，違反 occupied triangle
排除。故 rim induced，整個六點 W5 都在原內部。

## 5. 排除五個外點全為 degree 4，得到至少七個五度內點

若 \(D_B=20\)，每個 b_i 的 degree 恰四。設框邊 b_i b_{i+1} 的唯一
共同內鄰為 x_i。五個 x_i 已證互異，b_i 的兩個內鄰恰為 x_{i-1},x_i。
三角化的內側 fan 迫 \(x_{i-1}x_i\in E(G)\)。

於是 \(Q=(x_0,x_1,x_2,x_3,x_4)\) 是全內部 C5。
五個面 b_i b_{i+1}x_i 和五個面 b_i x_{i-1}x_i 填滿 B 與 Q 間的環帶；
所有其餘原內點都在 Q 內。其數目為 \(k-5\ge8\)，與 §3 的上界一矛盾。
所以

\[
\boxed{D_B\ge21,\qquad n_5=D_B-14+X\ge7+X\ge7.}
\]

這裡確實用到 k 的既有下界；punctured icosahedron 的 k=6、D_B=20
是相容的邊界控制，其內層 C5 恰包住一點。

## 6. 五輪存在與保完整 Σ 的縮減仍有距離

現在可以選擇全內部 rim \(U=(u_0,\ldots,u_4)\)，刪去中心 v。
外部是以 B、U 為雙邊界的環帶，不能視為另一個 C5 disk 而直接套小代表。
對每個原框列 p，令 J_p 是同一份 G-v 著色在 U 上的**完整有序關係**。
則 p 延伸至 G，當且僅當 J_p 含一份恰用三色的 tuple。

對 proper C5 的三色 tuple，兩組重複色各佔一條 diagonal，且兩 diagonal
端點交錯。因此精確條件是同一份 tuple 同時滿足某組

\[
u_i=u_{i+2},\qquad u_{i+1}=u_{i+3}\qquad(i\bmod5).
\]

每個單對角識別 \((G-v)/(u_i=u_{i+2})\) 是保留原框的較小 disk 來源，
但它還允許 rim 四色 tuple；分別成功的兩個 quotient 可以使用不同 lifts。
不能把投影後的交集當作同份 tuple 的交集，也不能將交錯雙識別自動當成合法
平面填補。具體完整關係控制見 [五輪重接分析](review/local_wheel.md)。

新的邊界接觸引理已直接排除舊 [任務 C](../../docs/tasks/c5_degree5_link_tasks.md)
中同時鄰接非相鄰外點 a,c 的原來源位置。這是條件來源的紙面排除，**沒有**
聲稱執行或證明該任務另列的全部 132² 抽象 cap joins。
任務 B 的全目錄操作域也未執行；本輪只核對明列的具體控制。

## 7. 審核、重播與信任界線

獨立紙面檢查見 [boundary review](review/boundary_review.md)；
完整短分離環證明及加外 apex 後的球面推論見
[separator proof](review/separator_proof.md)。後者另證無 separating C3/C4，
每個 separating C5 有 singleton 側；沒有用此術語代替五輪可縮減性。

主 [checker](controls/check.py) 只用 Python 標準庫：

```bash
python3 audits/2026-10-12-c5-deep-five-wheel-01a12ffa/controls/check.py --check audits/2026-10-12-c5-deep-five-wheel-01a12ffa/controls/certificate.json
PYTHONHASHSEED=17 python3 audits/2026-10-12-c5-deep-five-wheel-01a12ffa/controls/check.py --seed 17 --check audits/2026-10-12-c5-deep-five-wheel-01a12ffa/controls/certificate.json
```

[證書](controls/certificate.json) 保存具名 punctured icosahedron 的 literal
edges、20 個定向球面三角面、rotation，以及全部 240 個 proper 原框
assignments 的完整 fibres。直接 product 與獨立 MRV 比較逐份 lifts；其
完整 Σ=1023。另核對含 apex 球面圖的 122 個 C3/C4/C5 及兩側實際頂點。
定向面、每頂點單圓 link、連通性與 Euler 特徵二一起認證球面嵌入。

| 證據／控制 | 狀態 | 範圍 |
| --- | --- | --- |
| 本輪普遍結論 | conditional paper proof | 僅 §1 的 global 最小來源；完整介面替換和圖上計數 |
| punctured icosahedron | triggered and holds | 邊界接觸、全內部輪及等式校準；Σ=1023 屬 K |
| D_B≥21、n5≥7 的 k≥13 前提 | not triggered in finite control | k=6 控制不能驗證或反駁該條件性排除 |
| 單／雙識別及聯集可直接縮減的自然猜測 | counterexample in named controls | 見五輪重接控制；非一般來源枚舉 |
| 真正 933／941 最小來源 | not triggered | 未構造，也未由零觸發宣稱排除 |
| Lean | 未形式化 | `lake build` 僅既有工程核對，無本輪新 theorem |

實際執行記錄與破損證書負控制見 [VERIFICATION.json](VERIFICATION.json)。
原度數界證書有唯讀重播；沒有重跑原 132 圖枚舉或外部論文證書。
凍結輸入雜湊均不變；執行期間共用任務描述另有澄清文字更新，逐項審閱確認
不改數學前提且本輪已符合，差異留在 [SOURCE_DRIFT.json](SOURCE_DRIFT.json)。
附加的小 cap plantri 校準只作交叉核對，入口見
[原執行紀錄](../../scratch/c5-small-separators-20261012-01a12ffa/small_caps.json)，
普遍證明不依賴它的枚舉完備性。

目前停止點：全內部五輪必存在；需在同一 B/U 色框下研究環帶完整 J_p，
證明至少一種合法操作保整份 Σ，或用同份 full lifts 完成可用的聯集分解。
十三內點以上來源的排除、一般 \(K_\infty=K_{\le5}\) 及 Lean 化仍 OPEN。

本轮遵循專屬目錄交付，沒有更新共用 guide／STATUS 或舊任務描述，也沒有
commit／push。採納時需將 guide 的「未保證全內部 link」更新為本結果，
並把舊任務 C 的來源位置標為本輪已條件排除；一般縮減和獨立有限 join 命題仍分開。
