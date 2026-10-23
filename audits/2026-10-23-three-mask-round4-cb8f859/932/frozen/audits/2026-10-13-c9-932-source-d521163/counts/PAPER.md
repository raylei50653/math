# C9-932、h=4：同一 H 的完整計數與 100 個 apex 三度假設

本節重新在 C9 的 **820 個完整共同色框列**上建立局部 D3 計數引理；
沒有使用 C8 的 apex 結論、274 維介面或數值線性規劃。
原輸入是本輪凍結 frontier v2 的 20 項 `induced-932` 必要殘留。
每項五個具名 apex 的 H-degree=3 假設，共 100 項，均由 D3 與一般 C9
Kempe 支援閉包得到空集。本節只排除這些低度假設，不排除 20 項來源本身。

## 1. 同一原圖、同一份完整計數

H 是原來源 G 刪去原 B 後、以原 induced C9 為外框的內側 disk。
固定原 C9 順序、原 annulus 和顏色 `{0,1,2,3}`。對每個 proper literal
邊界指派 p，令 x_p 計數 **H 的全部完整染色**中延伸 p 的份數。
共同 S4 改色是雙射，因此 x 由 820 個 canonical C9 words 索引；
canonical 化作用於全份指派，不獨立改動 pieces 或接點。
其中 85 列用三色、735 列用四色，各有 24 個不同 literal lifts。

每項原 collar 保存一個 10×820 非負整數矩陣 T。T[r,p] 是在固定原 B
canonical word r 下，p 的 24 個 literal lifts 中符合全部具名 annulus
原邊者的數目。因此原 G 延伸 r 的完整染色數恰為

\[
N_G(r)=\sum_{p=0}^{819}T[r,p]x_p.
\]

完整 Σ(G)=932 要求 r∈{2,5,7,8,9} 時 Tx 的該項為正，
r∈{0,1,3,4,6} 時為零。T 由全部原 annulus 邊逐一重新枚舉；每個係數
並與 frozen 的完整、含空 inner-then-outer fibre 核對。因 C5 與 C9 每列
的共同色名軌道都恰有 24 份，這個 T 係數也等於該 frozen fibre 的大小。
完整 lifts 並未以邊際或獨立 masks 取代。

同一 x 還滿足以下來源必要條件。

* x≥0，且 frontier 的同圖 transfer＋Kempe 上界 U 外，x_p=0。
  20 項 U 的大小為 352（5 項）、356（10 項）、376（5 項）。
* 對原 C9 的每個 independent noncrossing partition π，
  定義 E[p,π]=1 當 p 在每個 π-block 內同色，否則為 0。
  不同 blocks **允許同色**。232 個合法商圖各有
  `k−9+|π|≤k` 點；由本來源的 no4ct 相對大小引理，可得
  `sum_p E[p,π] x_p > 0`。這不是普遍四色可染性。
* 同一完整 x 屬於這個 820×232 矩陣 E 的 signed column span。
  這裡不要求係數非負。證明如下：在 H 的全部原邊展開
  `∏(1−δ_color(u),color(v))`，再對全部嚴格內點顏色求和。
  每個邊子集的 connected components 在 disk 邊界誘導 noncrossing
  partition π；不觸邊界的 component 各貢獻因子 4。
  因此每項是整數 signed coefficient 乘 E[·,π]。
  若 π 同塊包含 C9 相鄰點，其 E 列在 proper C9 domain 上恆為零，
  可刪去；餘者正是這 232 份 π。這是直接對 C9 的有限展開，
  不是移植 C8 equality matrix，也不需要聲稱 E 的 rank。
* 每個 x_p>0 的列及每個互補色對 split，都有一份來自 **該 H 的實際
  boundary-touching Kempe components** 的完整 flip orbit 包含於 supp(x)。
  實際 components 在原 C9 上給 noncrossing partition；同色對的原圈邊
  兩端必屬同 component。獨立翻轉這些實際 components 的全部結果仍是
  同一 H 的完整染色。因此 frozen 一般 C9 obligations 是合法上界。

商圖正性與 signed span 都作用在同一 x 上。以下 100 項矛盾只需要
非負性、原 U、Kempe obligations、新 D3 和一份接受列的正性；
不需對 signed span 求解。證書仍逐項記錄完整 T 及全部 232 quotient masks。

## 2. C9 的原三度 apex 局部引理

固定具名 apex a，假设 d_H(a)=3。記 u、v 為它在原 C9 的兩鄰點。
由 induced C9、原三角化與原 rotation，a 恰有一個嚴格內側鄰点 t，
且 `(u,a,t)`、`(a,v,t)` 是實際原面；tu、tv 為原邊。
這些幾何事實由本輪 geometry 的局部證明建立。

固定原 C9\{a} 的同一份 literal 指派 s，令 s(u)=s(v)=c。
在 **同一 H−a** 上令 z_d 計數全部延伸 s 且 t 色為 d 的完整染色。
因 tu、tv 是原邊，z_c=0。若其餘三色為 i,j,k，逐份保持 H−a 的全部
染色不動，僅補回 a，得到精確式

\[
x_{s,i}=z_j+z_k,\quad x_{s,j}=z_i+z_k,\quad x_{s,k}=z_i+z_j.
\]

於是每項滿足 D3 三角不等式

\[
x_{s,i}\le x_{s,j}+x_{s,k},
\quad x_{s,j}\le x_{s,i}+x_{s,k},
\quad x_{s,k}\le x_{s,i}+x_{s,j}.
\]

精確整數計數還有非負整數
`z_i=(x_{s,j}+x_{s,k}−x_{s,i})/2` 等，但本輪排除不需額外使用 parity。
若 u、v 不同色，剩餘兩個 a 色選項僅與 t 的兩個可能色互換，
不產生這組三角不等式；checker 不向該情形添加 D3。

重新列舉 820 列與所有三個 literal a 色後，每個 C9 位置有 91 份
不同 D3 triples。程式保存三個 occurrence 和一份固定其餘八色的 witness，
沒有先把 triple 轉成集合。此 C9 domain 上三個 canonical 索引恰好全異：
去掉 a 後的八點 path 若只用兩色，其兩端 u、v 必不同色，與 s(u)=s(v)
矛盾。故 fixed eight-site coloring 至少用三色，無非平凡色置換可以固定
全部這八個位置並把三個 a 色互換。

## 3. 精確支援排除證書

對每項 e、每個原具名 apex a，從原 U 開始反覆施行兩步。

1. 若某 D3 triple 只有一個 occurrence 的座標仍可能為正，三角不等式
   迫其為零。一次 D3 stage 的全部刪除均讀同一個 before support。
2. 對每個仍有支援的 p，若某 split 的 **全部**合法 orbit 都包含目前
   已迫零的列，則 p 也為零。同一 Kempe stage 的刪除同樣共用 before。

每一步都只刪除同一假定來源 H 的零計數。歸納即得 supp(x) 始終包含於
記錄的 support。沒有把不同來源圖、不同列的獨立存在性拼成一份染色。

全部 100 項於 3–6 個有變動的 alternating rounds 後都得到空支援。
證書欄位 `rounds_including_final_stationary` 為 4–7，明確多計一次終止檢查。
每項保存完整 before/after masks；每份 D3 刪除指向其 literal 三項式；
每份 Kempe 刪除保存一個 split 與其 **每個**候選 orbit 的已迫零 blocker。
每項的 820 個完整計數因而全為零。

這與原接受列 r=2 的 `T[2,·]x>0` 矛盾；事實上五份接受列全部消失。
也與 π=全 singleton partition（索引 231）的來源相對商圖正性矛盾；
此商圖就是原 H，頂點数 k。本輪全部 232 份正性項最後都失敗，
但不把 232 次失敗誤算成 232 個獨立來源排除。

## 4. 結論、重播與界線

在本輪固定 no4ct 全域最小來源、完整關係 932、h=4 下，
20 項必要殘留的全部五個原 apex 均滿足

\[
\boxed{d_H(a_i)\ge4,\qquad d_G(a_i)=d_H(a_i)+2\ge6.}
\]

主要 exact replay 使用 Python standard library：

```bash
python3 -B audits/2026-10-13-c9-932-source-d521163/counts/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c9-932-source-d521163/counts/check.py --check --negative
```

[certificate.json.gz](certificate.json.gz) 以 exclusive-create 產生；checker
從 frozen C9 v2 驗其 SHA256、重建全部 820 色列與 9×91 個 D3 triples、
重算 20 份完整 transfer、全部 232 quotient masks，再逐步重播 100 項。
本輪獨立 review 另由 Bell partitions 重建所有 noncrossing partitions 和
generic Kempe obligations，並以獨立程式重播各次刪除，避免只核總數。

這是 100 個 apex-degree3 假設的不可能性證書；不是任一來源圖存在證書。
仍保留 20 項在所有 apex 度數至少四下的同圖實現問題；一般 932 與 h≥5
均 OPEN。signed span/quotient constraints 本身沒有被稱為來源存在的充分
条件，亦無新增 Lean theorem。
