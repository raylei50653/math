# 六私人點 C6 核心的獨立紙面覆核

2026-10-13。本覆核只檢查 [主證明](../theory/PROOF.md) §§5–6 的
boundary chord 化約及六點私人核心兩分支；不生成新圖，不修改來源證書。
所用全域最小來源契約與直接輸入依 [INPUTS](../INPUTS.json) 保留。
這是紙面推導覆核，不是任意大小嵌入論證的 Lean 形式化或生成器完備性證明。

## 1. 精確域及可採納結論

P 是含具名 simple C6 外框、恰六個私人點的 finite simple disk
triangulation。所有私人點的 **P 內完整度數** 至少五；不假設它们是
原未知 H 的度數，也不假設 C6 pins 的度數下界。P 接在同一 exterior
中的既有距離二 Eq 旁，與清空後的 digon 共用一個原 boundary image。
八份 U、原 C8 pin map 及 literal 色名均保留。

覆核結論為：

- 若 P 有 boundary chord，存在至多五私人點的同側替代 gadget，其
  原 C8 pullback 關係包含於 P 的 pullback 關係。因此已知 signed 五點
  域無拒絕，亦排除此種 P 的空交拒絕。
- 未被此化約處理的 P 可限為 boundary chordless。若每個私人點接
  C6，私人 induced 核心是六點 maximal outerplane graph，私人點的
  P-degree 全為五，且私人到 boundary 的邊恰十二條。
- 否則至少一個具名私人點是度五的 deep wheel 中心，其五個鄰點恰為
  另外五個私人點。此項只給 wheel 子圖及中心的原 rotation／面，不
  採納 induced 鄰環或鄰環外側無弦。

這些結論均未給八份 U 新的來源排除；兩個核心入口仍未經完整分類或排除。

## 2. Boundary chord 必落回五點域

取任一實際 boundary chord xy。其兩條 C6 原弧各至少長二；以較短弧
長度分類，它在指定 disk 中切出 C3+C5 或 C4+C4。兩個 pieces 除共同
邊 xy 及其兩端外沒有共享點；不存在跨兩個開側的原邊，否則它會穿過
xy 或原外框。全部六私人點各屬於恰一側。

因此兩側可在固定原 boundary 指派、同一 literal 色框下以完整 fibre
作 join。先選一份原 C8 row，所有共用 pins 直接取該 row 的同一色值；
不能在不同 rows 上分別挑選兩侧的非空 fibres。

每側私人點數 s≤6<k，因本契約 k≥19：

- C3 側至多九個總點，故相對可染性給一份 proper 完整染色。其三個
  boundary pins 的 proper 指派只有一個 S4 orbit，全域換色可接回
  任意指定的 proper 三色 row。因而可清空全部私人點，保留 boundary
  relation；不主張 full-lift 數量相等。
- C5 側是合法、具名、有序 disk-C5，內點仍是 s<k。由同一全域最小性，
  完整關係在 K132，有至多五內點的精確代表。代表放回此側，保留
  原五個 pins、共同 xy 邊及其兩端身份。
- C4 側可使用受限 s<k 引理。四列依序為 0101、0102、0121、0123，
  完整 mask 只可能為 7、10、11、12、13、14、15。mask 7 用一點 W4；
  mask 10、11、14、15 可選零點對角線的 mask 10；mask 12、13 可選
  零點對角線的 mask 12。所選完整關係非空且包含於原側關係。

七份 C4 具體代表及原表見 frozen
[C4 報告](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
與 [完整證書](../frozen/audits/2026-10-13-c5-no4ct-degrees-6cafdfb/C4_CERTIFICATE.json.gz)。
此處沒有把 s<k 擴充為任意大小 C4 代表定理。

兩側替換總共需要 C3+C5 的至多五點，或 C4+C4 的至多兩點。對每份
固定原 row，替代 sides 的 full fibres 同時可延伸，就各自證明原 sides
在 **同一 row** 下可延伸；原私人名字互不相交，故可作原圖 full join。
這證明完整 pullback 支援包含，不建立替代 lifts 到原 lifts 的雙射。

替代 pieces 的 drawing 均留在原 chord 的兩側，digon 及原 Eq pin map
不變。依主證明 §4 的展開與三角化接口，得到至多五私人點的合法 signed
C8 drawing。援引其無拒絕時仍保留既有 plantri 完備性依賴；沒有把這一
紙面 chord 化約稱為新的枚舉結果。

## 3. Euler 計帳及全接框分支

記 I 為六個私人點，Q=P[I]；q 是 C6 boundary chord 數，eII 是私人間
邊數，eIB 是私人到 boundary 邊數。P 有十二個總點，外面長六，其內面
全三角；Euler 與面邊計數給

\[
|E(P)|=3\cdot12-6-3=27,
\qquad e_{II}+e_{IB}=27-6-q=21-q.
\]

私人完整度數的總和恰為 2eII+eIB。最低度五因此給

\[
30\le2e_{II}+e_{IB}=21-q+e_{II},
\qquad e_{II}\ge9+q. \tag{1}
\]

若每個私人點都有 C6 鄰點，該接框邊從該點的一個面角出發，其開邊不
遇到 Q，並終止於原 C6。原 C6 及其外側均屬於平面補集的無界區域，
所以此面角是 Q 的 unbounded face 的面角。六點都 incident 於 Q 的
同一 unbounded face；由繼承的實際 drawing，Q 是 outerplane，沒有
改換嵌入或只採納抽象 outerplanarity。

六點 simple outerplane graph（允許最初不連通）有 eII≤2·6−3=9。
與 (1) 合併已迫 q=0、eII=9，並由 eII+eIB=21 得 eIB=12。總私人度
恰為三十，各私人度均至少五，故 **逐點 P-degree 都恰為五**。

達到 2n−3 的 simple outerplane graph 必是 maximal outerplane：若
有可加邊的 disconnected components、cutvertex 面角或非三角 bounded
face，就能在保持所有點 incident 外面的前提下增添一條 simple edge，
違反上界。故 Q 連通且二連通，其外面為六點 simple cycle，所有 bounded
faces 皆三角。這項外圈是私人核心 Q 的外圈，不是原 C6 的同一六個 pins。

每私人點有至少一條接框邊，且 P-degree=5，所以其 Q-degree≤4。
原 C6 boundary 的度總和為

\[
\sum_{c\in C6}\deg_P(c)=12+2q+e_{IB}=24. \tag{2}
\]

(2) 給平均四，**不給逐點至少四**；此處沒有 boundary-degree 下界。

## 4. 不全接框分支的 wheel 說法

若私人 u 沒有 C6 鄰點，P 簡單且總私人點僅六，因此 u 最多接其他五
私人點。度至少五遂迫 deg_P(u)=5，且 N_P(u)=I\{u}。

P 為 disk triangulation，u 是嚴格內點；其五鄰點依原 rotation 記為
u0,…,u4，互異且 consecutive pair 之間有原邊。五個 incident 三角面
正是 uuiui+1，它們的聯集是由此五鄰環圍住的原 disk，恰含中心 u 及
五 spokes。於是六個實際私人點含一份具名 W5 子圖。

輪外側的私人間邊没有由這個 star 論證排除：若要再聲稱鄰環 induced，
須另證非相鄰鄰點間沒有外側 chord。本覆核不作此推論，也不採納
occupied-C3/C4、原 H 的最低度或其他來源幾何去限制這份輔助 cap。
此分支只要求至少一個這樣的 u，沒有聲稱中心唯一。

## 5. 採納界線

Boundary chord 化約與兩個結構入口的計帳在上述精確域內成立。全接框
分支給六點 maximal outerplane 核心與原接框邊的精確數目；deep wheel
分支給實際五鄰 rotation。它們沒有涵蓋各核心到原 C6 的全部具名
attachments，亦未求出其完整 relation／fibres。

特別不能把六個 boundary pins 的平均度四改成最低度四，故加 exterior
cone 後不能直接套用十三點、最低度五的球面分類。此處未做新的球面
枚舉、原來源 realization、共同計數矛盾或 Lean 驗證；八項與主命題的
OPEN 狀態保留。
