# C4 方向：no4ct 球面補強與兩個例外五環

2026-10-14。本輪隔離證據包的紙面推導；來源及凍結輸入見 [REPORT](REPORT.md)。下列是紙面推導，沒有宣称完成無界 C4 延拓或 K∞。

## 1. 固定契約與明確依賴

G 是所有 Σ∉K132 的合法 C5 disk 來源中，先全域最小內點數 k、再最大邊數者；共同搬運整張原圖後 B=(b0,b1,b2,b3,b4)、Σ∈{932,933,941}。令 S 是 G 外加 apex u 及全部五條 ub_i 的 sphere triangulation，H=S−ub3，指定外框 Q=(u,b2,b3,b4)。使用：

- audits/2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md §§1–4；尤其 lines 25–47 的 s<k 相對小 cap 邏輯、lines 74–76 的原 C4 空/proper C5 空或 W5、lines 81–89 的原內點至多接兩個相鄰 B 點。
- audits/2026-10-14-c5-c4-boundary-pivot-77fbd5d/PROOF.md §§1–2：H 確為 induced-Q 4-candidate，d_H(u)=4，所有原 G 頂點／邊及 full fibres 保留，F_H(ABCB) 對應 F_G(y0) ⊔ F_G(y1)。
- 歷史證明 audits/2026-10-13-c5-no4ct-frontier-6943561/frozen/audits/2026-10-12-c5-deep-five-wheel-01a12ffa/review/separator_proof.md §6，lines 147–191 已有球面論證雛形；新版 no4ct 的 w5/PROOF.md §6 明說只接該舊文 §§1–5。本文件重新接上 §6，不繼承舊普遍 C4 小代表前提。

G 內點度≥5，B 度≥4，B induced、原內面三角形且無 occupied triangle。全域 k≥23 是現有結論，但此處僅需 k≥2。

## 2. 球面 S 的小 separator 命題

**命題 S6。** S 的最小度≥5，無 separating C3/C4；每個 separating C5 至少一側恰為單一五度點，該 C5 正是此點的 link。這是明列 cycle 性質，通常称 internally-six-connected；不是六頂點連通。

**證明。** 原內點不增度，原框增一度，u 恰五度，故 δ(S)≥5。

三角形若不含 u，則是原 G 三角形，原有界側無點；若含 u，由 B induced，只能是 ub_i b_(i+1)，為新增面。故無 separating triangle。

C4 若有 chord，其 chord 把一側分成兩個三角形。對每個小三角形，另一側含 C4 的另一頂點，故由無 separating triangle，小三角形的 chord 側必空；兩者聯集給 C4 有空側。若 chordless C4 不含 u，則原 G 的有界側空。若 chordless C4 含 u，寫成 u-a-x-c-u；a,c∈B、x 是原內點，且 a,c 在 B 非相鄰（否則 ac 是 chord）。這違反原內點不可同接非相鄰 B 點。因此無 separating C4。

C5 若有 chord，該 chord 分出一個 C3 和一個 C4。各小 cycle 的另一側含原 C5 的非空開弧；無 separating C3/C4 因而使 chord 側兩片都空，C5 非 separating。因此 separating C5 必 chordless。

令 C 是 chordless separating C5。若 u∉C 且 C=B，外側恰為 {u}。若 u∉C 且 C≠B，原 proper-C5 定理說原有界側空或 W5；separating 排除空，故恰一五度中心。

最後 u∈C，寫 C=u-a-x-y-c-u。chordlessness 迫 x,y∉B（否則 ux/uy 是 chord），a,c∈B 非相鄰。寫 B 的短弧為 a-b-c。原五環 D=a-b-c-y-x-a 是 proper C5，且沿 B 短弧的內側 cap 無點或恰 W5。若為 W5，b 的 disk 內 sector 只有中心，故 d_G(b)=3，與 d_G(b)≥4 矛盾。故此 cap 無點。於 S，C 含此短弧一側恰為 singleton b；δ(S)≥5 且該側只此一點，迫 b 與 C 五點全部相鄰，d_S(b)=5。證畢。

注意最後 singleton 是短弧中點 b；在 H 選定外面後，此 singleton 可能落在 H 的有界側，也可能落在外側，不能丟掉方向。

## 3. H 的非外框 C4 全空

**命題 H4。** H 除外框 Q 外，每個原 simple C4 的有界內側無頂點；所以 H 是 internally-five-connected 4-candidate。

**證明。** 令 C≠Q 為 H 的 C4，反設其 H 有界側有點。它也是 S 的 C4，由 S6，其另一側無點。該另一側含 H 的 outer-face 位置，因而含新補回的 e=ub3。S 的三角化空四邊形恰有一條 diagonal，而 e 必是這條 diagonal；其兩 incident 三角面正是 u-b2-b3 與 u-b3-b4，故 C 必是 Q，矛盾。證畢。

這不使用 H 在全部 restrictive 4-candidates 中最小。因此不需要誤套外部 paper Corollary 42 的全域 4-candidate 最小性。

## 4. induced C5 的精確兩例外

**命題 H5。** 令 C 是 H 的 induced C5，s 是其 H 有界內側點數。則：

1. 若 C=B，s=k，H 外側恰為 singleton u。
2. 若 d_G(b3)=4，則 C*=link_S(b3) 是 H 中的一個 induced C5，s=k，H 外側恰為 singleton b3。
3. 除以上兩者外，s≤1；s=1 時 cap 恰為 W5，其中心為 H 五度內點。

B 與 C* 互異，因 u∈C* 而 u∉B。若 d_G(b3)>4，只有 B 這一個例外。

**證明。** 假設 s≥2。把 e=ub3 補回 S，不會增加頂點。因 C 在 H induced，C 在 S 至多有一條 chord，即 e。

若 C 的 S 外側沒有頂點，該側是一個 triangulated empty pentagon，需要兩條不同 diagonal。至多一條是 e，故另一條留在 H，與 C 在 H induced 矛盾。因此 S 的 C 兩側都有點，且有界側≥2。S6 迫外側恰一點 w，d_S(w)=5 且 C=link_S(w)。

w 必是 Q 上的頂點：Q 的某一頂點不在 C（否則 C 包含 Q 四條邊，不能同時是 induced C5）；該 Q 點在 H 外側，所以它就是唯一 w。若 w=b2 或 b4，S 的 link 必包含 edge ub3（它們都與 u,b3 形成 e 的 incident face），此 edge 不在 H，與 C⊂H 矛盾。故 w∈{u,b3}。

w=u 給 C=B。w=b3 給 d_S(b3)=5，即 d_G(b3)=4，且 C=link_S(b3)。此 link 無 chord，由 S 無 separating triangle；它避開刪除邊 e 本身，因 e incident b3，而 link 不含 b3，故 C*⊂H。它确為 induced C5。兩個例外各在 |V(H)|=k+6 中占五個界面點及一個外側點，故 s=k。

對非例外 s≤1；若 s=1，唯一 H 內點的 H-degree≥5 且 cap boundary 五點，迫全五 spokes，Euler 留無額外邊，即 W5。證畢。

**重要反陷阱。** 「H 的每個 proper C5 都空或 W5」是錯的：B 在 H 本身就是 proper C5，內部仍有 k 點。若 b3 原四度，第二個大型 pentagon 也有 k 點。不能把這兩個介面當作 s<k 的小來源套 K132 代表。整份 H 內點 k+2，同樣不能套 s<k 的受限 C4 代表。

## 5. 兩相鄰原框四度點尚未排除

沒有找到已採納定理排除 d_G(b0)=d_G(b1)=4。相反，已保存必要殘留仍包括此型：

- audits/2026-10-13-c8-struct-243a125/classification/CLASSIFICATION.md 的表保留 c04-941，extras=(0,0,1,0,2)，及 c07-941，extras=(0,0,2,0,1)。extras_i=d_G(b_i)−4，故 b0,b1 都四度。
- 這兩份只是未排除的必要 query，不能當作實現圖；亦足以證明現有 C8 necessary-screen 尚未處理掉此型。
- c04/c07 中 b3 也四度，因此 H5 的雙大型 pentagon 情況確實出現在現有來源契約殘留內，不能當作空分支略去。

## 6. OPEN 與下一窄入口

以上新接入不排除任何無界 932/933/941。真正來源 H 比「u degree4 且 link 兩內點連續」更窄：後者對 induced-Q 三角化 4-candidate 幾乎自動；前者有 H4、H5、S6 及原完整 fibres。可以在此更窄契約研究單一大型 pentagon（d_G(b3)≥5）與雙大型 pentagon（d_G(b3)=4）兩支。

無界 ABCB extension 仍 OPEN。932 子支独立排除本身承擔 4CT 難度，不能假定 S 已可染。H4/H5 只是原同圖結構，未提供原 full-fibre 保持的較小替代、C4 猜想證明或 Lean theorem。
