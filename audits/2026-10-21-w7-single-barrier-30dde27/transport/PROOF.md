# 恰一障礙：完整分量傳輸、混色連通與確切停止點

2026-10-21；exclusive BASE `30dde27293b5d3ad63c75fae73cda5be96db705b`。
[BASE.json](BASE.json) 與 `frozen/` 保留十份來源的原 bytes／SHA；checker
每次亦核對原檔沒有漂移。本項只寫本 `transport/`，不更動舊探索或共同路由。

承接[原 SOURCE_CONTRACT](../../2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)、
[完整原第三面點與 link](../../2026-10-21-w7-private-face-points-d23f94f/PROOF.md)
及[任意 K 障礙公式](../../2026-10-21-w7-exploration-30dde27/BARRIER_FORMULA.md)。
原圖仍為任意大小的同一有限簡單 plane C5 disk，完整 941／最小來源、原 stars、
rotation、全部私有附件、原 C3／C4／C5 pocket 定理及 strict only-R/W7 合同
均保留。這裡固定完整 profile 0 或 1，沒有對原外側 E 加大小上界。

本項得到任意 K 的完整分量作用公式及一條有條件的遠側混色連通義務。
本項的 78,780 個有限必要連通 gate 沒有新增來源排除；整個父審核的其他
證明結果不由這個陰性結果否定。

## 1. 同一實際 target 中的精確前綴／後綴

始終固定

```text
D = G − {b,p,h,R,x,y,r},
rim(D) = (a,n,u4,u3,u2,u1,L,q,c,s,v,w,t),
P = (n,u4,u3,u2,u1,L),  φ(P)=121212,  φ(a)=0, φ(q)=3.
```

令 A 為沿原完整外側 links 得到的有序 a–q 原弧；profile 0 經
`H_n,z1,H1,z2,…,z5,H_L`，profile 1 從 `a=z1` 開始。由原第二層定理，
這些點身份與次序固定，沒有補邊或刪除未列附件。

固定任一份**同一 D 的完整 target 著色**，並假設 A 恰有一個反色 12 障礙
點 y。令 A−、A+ 分別是 y 之前、之後的全部 A 點，均含對應端點 a、q。
它們是兩條完整 03 原路，故

\[
A^-\subseteq K_{03}(a),\qquad A^+\subseteq K_{03}(q).
\]

原完整 target 的唯一 03|12 欄迫兩個實際完整分量不同。五個 zi 因而只會
按 A 原序落在 a 側前綴與 q 側後綴，沒有中間無框片段。全 D 仍可有任意
其他不碰 A 的 boundary-free 03 分量，不得刪掉或補到 a／q 分量。

兩個原 target 的完整 contacts 是：

| target | 原唯一 03|12 欄 | K03(a) rim contacts | K03(q) rim contacts | K12(P) rim contacts | K12(c) rim contacts |
| ---: | ---: | --- | --- | --- | --- |
| A=44459 | 306985 | a | q,v | n,u4,u3,u2,u1,L,w,t | c,s |
| B=44466 | 306993 | a | q,w | n,u4,u3,u2,u1,L,t | c,s,v |

每個障礙直接接其反色中心，故 y 始終在完整 `K12(P)` 中。

## 2. 翻完整 K03(a)、K03(q) 的任意 K 結果

記 Sa、Sq 為交換這兩個**實際完整分量**的 0／3。它們作用於全部私有點，
不是只作用 A 交集。因 palette induced graph 不變，Sa、Sq 為可交換對合，
其在 A 上的作用完全確定：

```text
Sa：A− 全部 0↔3，A+ 不動，y 不動；
Sq：A+ 全部 0↔3，A− 不動，y 不動。
```

它們都保留 b=1、同一原度數向量及原分量的點集合。令 ε 表示 y 的左右
03 鄰點是否異色；單翻一側恰把 ε 改為 1−ε，同時把 a、q 的異色狀態改為
同色。故沒有奇偶矛盾：原公式 `ε≡1+K`（0 型）、`ε≡K`（1 型）固定了
**原端點 0、3**，不能在改成同色端點後原封不動再套一次。

| 起點 | Sa 或 Sq 後 canonical state | SaSq 後 canonical state |
| ---: | ---: | ---: |
| 44459 | 44050 | 44459 |
| 44466 | 44046 | 44466 |

Sa、Sq 的字面結果仍不同；[certificate.json](certificate.json) 保留每份完整
字面 rim tuple，沒有只記 canonical ID。

再對 SaSq 的結果作一次全域 0／3 正規化，A 上所有色恰回原樣。但是若 U
是原著色中所有 boundary-free 03 完整分量的聯集，這個完整操作恰等於翻 U。
因此**原 rim 與 A 色回原樣不等於整份完整著色回原樣**。原外側私有點的
相位仍可能不同；沒有在這一步消去隱藏 witness。

## 3. 不能把目的 fibre 補滿：一個確切的必要模型反控制

Sq 將 A 送到 44050、B 送到 44046。作用保留原 03 component vertex sets，
所以實際像仍位於原欄 306985／306993；然而目的**整份 fibre**的完整 family
分別容許三欄：

| 目的 state | 全部 03|12 incident columns | 其中 a、q 已合併的欄 |
| ---: | --- | ---: |
| 44050 | 306983,306984,306985 | 306983 |
| 44046 | 306991,306992,306993 | 306991 |

後一欄的存在是原必要 family 的反控制，不宣稱已實現新的原來源圖。
它精確指出不能把作用的實際像換成目的整 fibre，再宣稱其中所有著色仍有
原 target 的 a／q 分離。反向也只能還原那份帶完整歷史與分量身份的像。

## 4. 兩步後的第三個混色動作：A 有共同 contacts，B 必須分五案

令 Sc 交換原完整 K12(c)。它與 Sa／Sq 的 palettes 相互不交，所以可交換。
Sc 不碰 P；A 上的 03 點不在 12 palette，唯一障礙又在另一個 K12(P)，
故 **Sc 不碰 A 的任何點**。這個結論適用任意 K 的 b=1 分支。

在當前同一完整著色上作 `Sq`、`Sc` 後，分別得到

```text
A → M_A=44111: (0,1,2,1,2,1,2,0,2,1,3,1,2),
B → M_B=44107: (0,1,2,1,2,1,2,0,2,1,2,3,2).
```

於 M_A 重新取當前完整 K13(v)。原完整 family 的五欄
`147448,147449,167802,226130,231666` 全部迫其 rim contacts 恰為 `{s,v,w}`，
交換得到 44127。此分量避開所有 P 點，所以亦避開：

- 全部 zi：若 zi 色 3，它接一個色 1 的 P 端點，會直接連入該 rim 點；
  若 zi 色 0，本來就不在 13 palette。
- 所有中心在 `{n,u3,u1}` 的 H 點：其中色 3 的點接其色 1 中心，不能在
  這個不碰 P 的分量中；其他色亦不在 palette。

因此這第三個混色動作只能在 `{H_u4,H_u2,H_L}` 中搬動 1／3 障礙，不能
逐點搬任一 y。若把 y 從 1 變 3，它亦可能在別處同時造出新障礙；目的
44127 不是原 target，沒有一條已證條件迫此時 a／q 仍分離。

M_B 的完整 02|13 incidence 有十四欄，不能直接套 A 的 contacts：

| 完整 K13(w) rim contacts | 原欄數 | 交換後 canonical state |
| --- | ---: | ---: |
| s,w | 5 | 44131 |
| w | 5 | 44104 |
| u1,w | 2 | 46291 |
| u3,u1,w | 1 | 65974 |
| u3,w | 1 | 63787 |

全部原欄 ID、完整 component partitions、字面作用及目的 states 均保存在
certificate 中。六個第三步目的 states 都是原已證零值閉包的存活列；本項
沒有在它們找到新的原邊同色或 cap-zero 矛盾。這不給共同計數可行模型。

## 5. 新的有條件遠側連通義務

令 c=φ(t_y) 為 y 的原中心色，η=φ(y)=3−c。額外假設：

> 在所有原中心色為 c 的 H 列表中，**原 H 頂點的總集合恰只有 y**。

這是對全部 H 點的限制，不只是「色為 12 的障礙只有 y」；後者已由 b=1
給出，卻不足以支持以下推論。K=1 自動滿足這個額外條件。

**結論：** 對 x=0、3，當前完整 `K_{ηx}(y)` 都必碰原 D rim。

**證明。** 假設其中一個完整 K 不碰原 rim，則它不碰 P。任一色 x 的 zi
接一個色 η 的 P 端點，故不能在 K 中；其他 zi 亦不在 ηx palette。任何
色 x 的 H 點若中心色 η，亦直接連入 P，不能在 K 中；若中心色 c，則由
額外條件唯一可能點就是 y。A 上唯一原色 η 點也恰是障礙 y。故
`K∩A={y}`。交換整個 K 後，原 D rim 字面色完全不動，A 全部成為 03 原路，
把 a、q 連起；但原 target 的唯一完整 03 欄禁止此連通，矛盾。證畢。

當 K=1、profile 1 的 y 兩側 03 異色，這兩個混色連通由兩側 zi 與其 P
端點的原邊已局部觸發。profile 0 的兩側同色 β，`K_{ηβ}(y)` 亦局部觸發；
另一個 `K_{η,3−β}(y)` 則**不能經 y 的兩個 A 鄰點或原中心離開**。
由第二層 induced 性，這個必要連通必使用原 E 中保留的後續附件。
這給出了需要追的具體遠側路徑，沒有假定它的終端接點、長度或獨立可選性。

若同色中心另有 H 點，這些原 03 點可能在混色交換後變成新障礙，前述
移除唯一障礙的論證就停止；本項不把這個例外省略。

## 6. 有限校準的域、全部記錄與陰性結果

固定任意 proper 的已知原子圖 C（保留 P、全部 A 及原 D rim）。對任一
palette，C 中已連起的 rim contacts 在實際完整 D 中只能再合併，不能被拆開。
所以從原完整 incident columns 保留所有不拆這些 contacts 的欄，是來源的
必要 gate。接受欄僅是一個必要 partition，沒有把不同 palettes 的接受欄
拼成同一原圖或同一外側 witness。

[checker](check.py) 對兩型 `1≤K≤5` 的全部有序長度向量，逐一固定每個
唯一障礙位置。每個位置恰有一份端點 0、3 的局部色列，不枚舉新來源圖。
共 3,030 個位置、兩 target 6,060 份色列；每份做四個 Sa／Sq parity 下的
三個 split gate，再做 SqSc 中間態的 02|13 gate，合 **78,780 個 gate**。
結果全部非空，沒有新增位置排除。

certificate 保每個位置／完整長度向量、兩 target、十三份 gate 的全部保留
原欄 ID；相同清單用 pattern index 共用儲存，沒有省略任何位置。
另外完整掃描原 307,197 欄取得所有用到的 incident columns，從全列 XOR
variation profiles 重建 component blocks，再翻全部非 anchor blocks 重生
每欄的完整支持。78 個長度 1 至 3 的有序 a／q／c 動作字逐步保留字面 tuple。

normal、seed17 加 `-O` 的唯讀重播一致；漏一欄、部分分量交換、把目的像
補成整 fibre 及冒稱來源排除四種污染均拒絕。每次重播保 frozen／live SHA。

```text
python3 -B audits/2026-10-21-w7-single-barrier-30dde27/transport/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-single-barrier-30dde27/transport/check.py
```

本項的 closure scope 是任意 K 的分量作用與條件連通紙證，以及上述有限域
完整必要 gate。marked-y 的遠側連通尚未分類其全部原 E 接合；沒有建立
跨 palettes 的共同來源實現，也沒有推出新的完整零 fibre 或較小合法替換。
兩型來源排除、一般 W7／J1／J2、strict smaller bad 及主命題在本項仍 OPEN。
沒有 LP、任意大新圖枚舉、四色定理、matching 或新 Lean。
