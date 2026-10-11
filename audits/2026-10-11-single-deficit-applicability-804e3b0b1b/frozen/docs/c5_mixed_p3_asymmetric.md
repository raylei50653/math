# 唯一 mixed P₃：非對稱 residual 的六跨度排除與兩端接線完成

後續（2026-09-30）：[中點／端點接線](c5_mixed_p3_middle_endpoint.md)已保留
未接 root 的原末端及三份附件，排除 masks=(0,1,2) 與整份對稱型的
全部 residual。連同本頁，兩個不同接點、各一 root incidence 已全
作 disk 來源排除；本頁兩端接線的證書與當輪數字不變。

2026-09-30，Git 基準 `d72b6cb`。接續
[mixed 容量](c5_mixed_capacity_contacts.md)與
[P₃ 對稱分支](c5_mixed_p3_symmetric.md)。
**唯一 mixed 原分量為 P₃=x₀x₁x₂，z 只接 x₀、w 只接 x₂ 時，
非對稱 source residual (1,2) 及整份 root 交換型都不存在 induced-C5 disk 來源。**
結合前層對稱分支，這個兩端各一 incidence 接線的全部 residual 已排除。

一色側可以零跨度；本證明沒有假設它具有二元 residual 的正跨度。
若它剩第四色，需要三個已見色；若它剩已用色 a，沿原環序把 a 與
另一側必見的另外兩色共同計費。兩種情況都需至少六條框邊。
不限制原 unary 大小、bridges 或旁支，不需 T4、Gallai／degree-list
外部定理，沒有 target 查詢或新增 Lean theorem。

[Checker](../scripts/c5_mixed_p3_asymmetric.py)／
[證書](../artifacts/c5_mixed_p3_asymmetric/observations.json)提供固定域控制，
紙面證明不依支援枚舉。驗證範圍見
[研究紀錄](history/2026-09-30-mixed-p3-asymmetric.md)，目前停止點見
[weak-deletion 導覽](c5_weak_deletion_guide.md)。

## 1. 前提與唯一待拒絕的有序色對

M 有限簡單，B=(b0,…,b4) 是 induced C5 disk 外框；H=M−B 非空連通。
q=01012、U={0,1,2,3}。M 拒絕 q，刪任一非框邊後接受 q。
相鄰 roots z,w 完整 degree=5，其餘內點完整 degree=4。
H−{z,w} 的唯一 mixed 原分量恰為 C*=x₀x₁x₂，contacts 恰為
P*ᶻ={x₀}、P*ʷ={x₂}；其餘原分量皆 unary。全部實際接點、附件與
原外部路徑保留；不識別同 q 色的框點。

沿用原完整有序 tuples 定義 mixed 禁對 F*，及每份 unary 的禁色 f_D。

\[
E_r=U\setminus\left(q(N_B(r))\cup\bigcup_{D\sim r}f_D(q)\right),
\qquad Z_M(q)=(E_z\times E_w)\setminus(\Delta\cup F^*).
\tag{1}
\]

先固定 |E_z|=1、|E_w|=2。刪 zw 必釋放一份可用對角，故必可寫成

\[
E_z=\{a\},\quad E_w=\{a,b\},\quad a\ne b,
\qquad (a,a)\notin F^*,\quad(a,b)\in F^*.
\tag{2}
\]

最後一式是唯一原非對角的拒絕。F* 的其他格仍由同一完整 P₃ 關係
決定，沒有自行刪除、投影或選取兩端 marginals。交換整份 roots／
側圖並反向命名 x₀,x₁,x₂，即涵蓋 (2,1)。

## 2. 原 P₃ 拒絕迫使 a 或 b 是第四色

三個 x_i 各有恰兩個原 boundary 鄰點 S_i，令 L_i=U∖q(S_i)。
每份 L_i 至少二色且包含 3。在 roots=(a,b) 下，P₃ 的 lists 為

\[
M_0=L_0\setminus\{a\},\quad M_1=L_1,\quad M_2=L_2\setminus\{b\}.
\]

若端點 list 至少二色，從另一端開始貪心即可染完；若中點至少三色，
先選兩端再選中點。因此拒絕恰須

\[
M_0=\{s\},\quad M_2=\{t\},\quad s\ne t,\quad M_1=\{s,t\}.
\tag{3}
\]

故三個 L_i 都恰為二色，三份實際 S_i 各見兩個不同 q 色。
若 a,b 都不是 3，兩個端點 residual 都包含 3，會給 s=t=3，矛盾。
所以恰有一個 root 色是 3。特別是 b=3 時，a≠3 而 s=3，得到

\[
L_0=\{a,3\},\quad L_1=L_2=\{t,3\},\quad
q(S_0)=U\setminus\{a,3\},\quad t\in\{0,1,2\}.
\tag{4}
\]

此處 t 可以等於 a，不假設三個 lists 不同；各份實際 S_i 仍分開。

## 3. 原五環、單點側支援與不變性

[對稱分支 §2](c5_mixed_p3_symmetric.md#2-原五環的內側為空外部路徑保留)
的原五環空內側論證只用 minimality、incidence 數和 degree，沒有使用
兩側 E 都是 pair，因此仍適用：每份 unary 有 0<|f_D|≤k_D≤3；
若不碰 B，其 f_D 對全 S₄ 不變，只能為 ∅ 或 U，矛盾。
每份 unary 遂有原 contact-to-boundary 路徑。它們與
J=z–x₀–x₁–x₂–w–z 不交，只能位於 J 外側；J 無 chord、開內側為空。
另保留 z–x₀–B、w–x₂–B 的原外部路徑。

定義完整側支援

\[
A_r=N_B(r)\cup\bigcup_{D\sim r}\{b_i:N(b_i)\cap D\ne\varnothing\}.
\tag{5}
\]

任何逐色固定 q(A_r) 的置換都作用於原 r 側的整份 coloring，故保持
精確 E_r。這只讀取同一份側圖，沒有把所有 unary 換成新的獨立分量。
利用 q 不用 3，得到三條本輪所需的必要式：

| 原 residual | 完整側支援的必要已見色 | 理由 |
| --- | --- | --- |
| E_r={3} | q(A_r)={0,1,2} | 少見 c 就能交換 c、3 |
| E_r={a}，a≠3 | a∈q(A_r) | 不見 a 就能交換 a、3 |
| E_r={a,3}，a≠3 | U∖{a,3}⊆q(A_r) | 每個缺見的外部色 c 都能與 3 交換 |

每份支援皆非空；pair 側至少兩點，一色側可能只有一個框點。
原 J 的 annulus crosscut 論證仍給同序共同 lifts

\[
T_z,\ T_0,\ T_1,\ T_2,\ T_w,
\quad \max T_z\le\min T_0\le\max T_0\le\cdots\le\max T_w
\le\min T_z+5.
\tag{6}
\]

模五分別是 A_z,S₀,S₁,S₂,A_w，或整體反向。允許 T_z 單點、
共享框端點和區塊間隙。原連通鄰域由 J 外側的 root collar 與全部
原 unary／spokes 構成；其他區塊若穿進一份支援的外端 crosscut，
便無法接回內圓周。單點支援同樣有到內圓周的原路徑，所以不能
藏入另一區塊的開支援弧。這個次序步驟不依賴五份跨度都為正。

令 ℓ_i=max T_i−min T_i。由 §2，ℓ₀,ℓ₁,ℓ₂≥1；由 pair 側
不變性，ℓ_w≥1。只保留 ℓ_z≥0，並由 (6) 得總長至多五。

## 4. 兩個六跨度矛盾

### 4.1 一色側剩第四色：a=3

由 §3，A_z 見三色，故 ℓ_z≥2；其餘四份跨度各至少一。
於是 5≥ℓ_z+ℓ₀+ℓ₁+ℓ₂+ℓ_w≥6，矛盾。

### 4.2 一色側剩已用色：a≠3、b=3

取 T_z 中一個 q 色為 a 的 lift h，並寫 U∖{a,3}={c,d}。
式 (4) 給 S₀ 完全不見 a，故

\[
\min T_0-h\ge1.\tag{7}
\]

另一方面，A_w 同時見 c,d。沿同一份原框方向從 min T_w 走到
h+5 的區段，包含這兩色及終點的 a，至少含三個不同框點，因此

\[
h+5-\min T_w\ge2.\tag{8}
\]

這條區段包含原 A_w 支援、其後的間隙與 A_z 到 h 的部分；只在
原框上計費，沒有添加新的支援邊或把稀疏支援填成實際附件。
(7)、三份原 P₃ 跨度、(8) 是同一圈上內部不交的區段，中間間隙
皆非負。因此

\[
5\ge(\min T_0-h)+\ell_0+\ell_1+\ell_2+(h+5-\min T_w)
\ge1+3+2=6,\tag{9}
\]

矛盾。這裡完全容許 ℓ_z=0；代價來自原環序中 a 與 c,d 的位置。
兩個分支及整份 root 交換型全部作 **disk 來源排除**。

## 5. 兩端各一 incidence 的全部 residual 已覆蓋

[容量與刪邊條件](c5_mixed_capacity_contacts.md#53-唯一-mixedm_zm_w1-的-source-residual)
只容許 (|E_z|,|E_w|)=(1,2),(2,1),(2,2)。最後一型必是兩側同 pair，
已由[對稱分支](c5_mixed_p3_symmetric.md)排除；前兩型由本頁排除。
因此在 §1 圖類中，**唯一 mixed 原 P₃ 的兩端各一 root 接線不存在**，
不另要求某一 residual 型。這可加入單側出口的失敗核心限制，不新增
空的出口類別，也沒有藉此計算任何 target 或任意來源的完整 Σ。

## 6. 固定域證書與重播

- 全部 10³=1,000 組實際 S₀/S₁/S₂，保存完整 triple、contact、F* masks；
  16,000 個獨立 pinned 回溯核對全部有序 root 色對。
- 以一色側為 z 正規化，共 384 份非對稱附件／residual，a=3 與 a≠3
  各 192 份；保留 26,400 組完整側角色接合。相同附件可有不同 residual，
  這不是 384 份不同附件，更不是來源圖的計數。
- 共同 lifts／跨度與 gap 的生成法，以及從實際支援子集建 cyclic hull
  的獨立生成法，都得到 110 份原環序幾何；包括單點 A_z。
  340 份資料／23,200 組角色無原環序支援；剩 44 份／3,200 組角色
  在 84 個相容幾何中各有完整側支援的不變性反證。零保留、零 target。
- 框反射 ρ=(3,2,1,0,4) 與共同色置換 π=(0 1) 保留完整 triples 及
  排除分類。Root 交換反向三個 x_i、轉置完整 F*，逐份交換全部側角色，
  核對仍在完整 minimality 接合中；(2,1) 不冒充新的獨立來源樣本。
- 全部 32 份框支援的 224 個不變性檢查，核對 §3 的三條必要式。
  另保存一份六框邊的必要支援正控制：一色側跨度零，仍滿足局部拒絕
  與所需支援色，總成本恰 1+3+2=6。它不是 degree／minimality 來源圖，
  只確認本輪反證使用了 C5 的長度限制。

```bash
python3 scripts/c5_mixed_p3_asymmetric.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_asymmetric.py --check
python3 scripts/c5_mixed_p3_symmetric.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

無 `--check` 生成本層證書；`--check` 重算逐 byte 比較，SHA 綁定本
checker、capacity 與 base interface Python。只用標準函式庫，不讀舊
接受／排除 flags，不改寫舊 artifacts。有限控制重用前層精確介面與
pinned 回溯，不宣稱整個引擎獨立。Jordan／任意 unary 大小的部分
屬紙面證明；未新增外部定理或 Lean theorem，`lake build` 不形式化它們。

本輪停止於兩端各一 incidence 的全部 residual 排除。下一窄題可取
唯一 mixed 原 P₃、P*ᶻ={x₁}、P*ʷ={x₂}，即接線 masks=(0,1,2)，
及其整份 root 交換／路徑反向型；必保留未接 root 的原 x₀ 及其三份
boundary 附件。它有原四環而非本頁的原五環，不能刪 x₀ 後套 K2。
其他 P₃ 接線、triangle、更大／多 mixed、逐染色 repair、完整 Σ、
一般／共同出口及 `K∞=K≤5` 仍未證。
