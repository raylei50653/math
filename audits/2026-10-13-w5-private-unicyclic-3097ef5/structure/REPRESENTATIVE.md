# Essential 單環必要核心的保 Σ 嚴格代表

BASE：`3097ef5be241b7777451a5ef8a663f3987d6b866`。
這是 [`STRUCTURE.md`](STRUCTURE.md) 的推論，保存強度**僅為補中心後完整外框 Σ**。
它不宣稱保存具名 R³、原 U 顏色、原中心色或 fibre 重數。

## 1. 精確適用域

來源是 STRUCTURE §§5–6 完备分類的 essential 圈秩一必要核心：原 B/U 是十個
不同 pins，全部私人點是 essential C_r，7≤r≤10，各點步型為
`(1,0),(0,1),(1,1)`，兩側原五環各前進五次。這個域包含假定最小來源的全部
essential 圈秩一情形。它亦包含違反其他來源條件的控制，不把這些控制當作
真正最小 933／941 來源。

紙面完備化約加全部 1652 核心的完整染色核對已證，此域每張補中心圖 G 的
`Σ(G)=1023`。以下使用的是這個完整十列結論；不能只保其中一個接受列。
主／獨立完整結果及全部空 cells 見父 REPORT、`controls/summary.json` 和
`independent/verification.json`。

## 2. 實際 r′=0 代表與指定槽位

保留原 B/U 的十個 labels 和原環邊，沒有其他私人點。先採用 STRUCTURE §6
明列的完整 label map，在其共向 canonical 座標以 B=(b0,…,b4)、U=(u0,…,u4)
表示原 pins；在相同 annulus 槽位加入五條 `b_i u_i`，得 pentagonal prism
annulus A′。搬回原來源後，這五條邊精確為 `gB(i)gU(i)`，不能漏記兩個起點。
若直接以原共向座標建代表，可取兩個起點都為零。其定向面為

```
(b4,b3,b2,b1,b0)                    designated outer face
(b_i,b_(i+1),u_(i+1),u_i)          i=0,…,4; indices modulo 5
(u0,u1,u2,u3,u4)                    designated empty inner face
```

每條 dart 恰出現一次，每個頂點的 rotation 是一個三循環；圖連通，且
`V−E+F=10−15+7=2`。這些實際面指定平面 embedding，B 保持外面、U 保持
原空內面，沒有隱藏點、識別、交叉或額外 attachments。

若來源先由完整圖同構搬到 canonical word，先在該座標建此代表，再用**同一份**
原 B/U label map 搬回。來源 B/U 的記錄方向若以相反邊界方向給定，明列該
記錄到共向座標的對照後再搬回。這個操作保持具名原環的次序與內外側；
它允許改動 annulus 內部及原 B–C、U–C attachments，不是假裝保留那些舊邊。

在 U 原空面加入中心 v′及恰五條 `v′u_i`，得 G′。內點只有 U 的五點與 v′，
所以 `k′=6`。代表不要求继承來源的原內點 degree≥5、三角化、最大邊數或
私人含環性：這正是全域最小來源可比較的合法 disk 類。

## 3. 代表全收十列的任意 literal 著色證明

給定任意 proper literal B 色列 β，固定色集 `{0,1,2,3}`。先令 v′色為 3；
需把 U 染於 `{0,1,2}`，並避開每條 `b_i u_i` 的顏色。令

\[
L_i=\{0,1,2\}\setminus\{\beta(b_i)\}.
\]

各 L_i 有兩或三色。我們直接證 C5 可由這些 lists 著色：

* 若某個 L_i 有三色，把該 u_i 留到最後。剩餘四點形成 path，依序 greedy
  著色：每點至少有兩個 list 色，只須避開已染的前一點。最後 u_i 有三色，
  至多避開兩個鄰點色，因此可染。
* 若所有 L_i 都恰有兩色，β 全用 `{0,1,2}`。它是 proper C5 色列，故相鄰
  β 不同，對應 lists 不同。取一對相鄰 i,j，先為 u_i 選 `L_i\L_j` 中一色，
  再沿**避開 j 的方向**依序染其餘三點，把 u_j 留到最後。每步只避開一個
  已染鄰點。最後 u_j 的 list 不含 u_i 的色，所以只須避開另一個已染鄰點，
  在兩色 list 中仍有選擇。

這給一份完整 proper G′ 染色。U 是奇五環，所以它實際恰用三色，中心3合法。
每個 proper β 都接受；不 proper β 在原 B 的某條環邊同色，G′ 必拒絕。
因此在完整 literal 域有

\[
\boxed{\Sigma(G')=\text{全部 proper B 色列}=1023.}
\]

這是一般紙面構造，不由固定有限 β 樣本外推。可固定最小可選 index／色，
使上述規則成為確定性的 full-lift selector。

## 4. 完整 Σ 的雙向 total 搬運

每份來源 G 完整染色先限制到原 B 色列 β，按 §3 構造一份 G′ 完整染色。
整個原 B 逐 pin、逐 literal 色保持；τ=γ(U) 及原中心色可能改變。

反向給定 G′ 的任一完整染色 γ′，取同一 β。完整 1652 核心結果保證原來源 G
對此 β 有至少一份完整 lift。固定 G 的頂點順序和四色順序，直接枚舉並選
字典序首份，即給反向 full-lift selector。這是終止的有限演算法，存在性由
已證完备有限核心保證，而非把兩層 marginals 拼接。使用證書時可將 β 與原
graph labels 共同拉回其 canonical word；必要時只作一次整圖共同 S4 色置換，
讀取該 β 行的一份**完整 G lift**後，用同一逆 label／色置換搬回。

兩個方向對每份輸入皆有完整輸出，因此是雙向 total 對照。它们不必互逆，
不必保持 U 色、中心色或任何私人 assignment，也不主張 fibre 基數相同。
精確關係等式只有

\[
\operatorname{pr}_B R_A^3=\operatorname{pr}_B R_{A'}^3.
\]

若有人把此代表宣稱為 `R_A³=R_A′³`，必須另給逐 named cell 等式；本交付
不作此宣稱。相同 Σ／不同 R³、相同 R³／不同重數的完整控制，見
[`../controls/strength.json.gz`](../controls/strength.json.gz) 及父 REPORT。

## 5. 嚴格內點數與最小性矛盾

來源 r∈{7,8,9,10}，代表 r′=0，因此

\[
(r,k)=(7,13),(8,14),(9,15),(10,16)
\longmapsto (r',k')=(0,6).
\]

各自嚴格減少 7、8、9、10 個內點。因 G′ 是同原 B 的合法 disk 圖，且完整
Σ(G′)=Σ(G)，便已與全域最小內點來源矛盾。這個排除只需 `k′<k`；
它順帶滿足 k′≤12，但不必為矛盾再調用 K≤12。

contractible 分支已由純紙面 M 面計帳排除，沒有該分支的待縮減來源。
essential 此代表只覆蓋已證必要核心，不提升為所有私人含環來源的小代表。
同一 W5 無須重新挑選，故連同 STRUCTURE 的前提化約，結論適用於任取合法
全內部 induced W5。真正最小 933／941 圖未被控制實現，仍標 `not triggered`。
一般私人含環 r≤6 代表、K∞=K≤5 與本紙面證明的 Lean 形式化仍未完成。
