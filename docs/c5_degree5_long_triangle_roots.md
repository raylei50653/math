# 長奇環加 triangle：完整條件 root 介面

發布整理（2026-09-18）：本報告隨 R16–R20 一併提交。下文的「未提交／HEAD／
下一題」保留各輪當時狀態；最新停止點見 [HANDOFF](HANDOFF.md)，
本次提交核對見 [STATUS §22](STATUS.md#22-r16r20-提交整理與核對)。


後續（R21）：[混合雙環來源 minor](c5_degree5_long_triangle_minors.md) 已補完
四型實際來源、逐邊刪除著色及非平面 minor 合成，完成互斥混合雙環排除。
以下保留 R20 當時的停止點。

2026-09-18，R20。接續 [R19](c5_degree5_bridge_mark_minors.md)，保留
R16–R19 scripts／artifacts。本輪完成指定的**四列條件 root 介面**及
cycle-to-triangle 的 list 語意等價；尚未新增實際來源圖的 minor／非 disk
證書，不把這一步記作混合雙環的完整排除。紙面證明＋Python 精確核對，
沒有新增 Lean theorem，未 commit／push。

## 1. 範圍、定義與共同 palette 的必要性

固定 q=(A,B,A,B,C)、U={A,B,C,D}、N_B(z)={b0,b1,b4}，F_C(q)={D}。
C=H−z 恰有兩個互斥 odd-cycle blocks，一個長奇環、一個 triangle，
其餘 bridges。沿用 R19 的位置分拆：若中間 bridge 不分隔兩個 z 接點，
消去無接點側，交回既有單環結果。以下每個 z 接點各經外臂到一個環，
兩環間保留一條 bridge 路徑；無接點外枝已消去，保留原 attachments。

固定 z=a，外臂末端訊息記為 P(a)。零長臂是 P(a)={a}；非零長臂
各內點有二色 list。定義 δ(P)=P（若 P 是 singleton），否則為空集。
外臂對環點只刪 δ(P(a))；這是固定 a 後的存在量化，不跨列重選色框。

長環的 bridge root 為 r，外臂接入點為 p。定義 M_r(a) 為刪去中間
bridge 方向後，長環連同外臂在 r 的完整可取色集。另一側 triangle
同樣定義。中間路徑內點的 lists 都為二色；兩端 M 均非空。
若其中一端至少兩色，從另一端選一色往它貪婪延伸，最後總可完成。
因此**拒絕 D 必使兩側 M_r(D) 都為 singleton**。

使用 [R14 §2](c5_degree5_odd_cycle_components.md) 的自足 cycle-list
引理：奇環各 list 至少二色時，不可著色 iff 全部 lists 是同一二色 S。
以下用此引理推出任意環長的必要條件，有限核對不替代這個論證。

## 2. 不同接點 p≠r

r,p 的原 lists 各三色，其餘環點各二色。外臂刪色後，p 仍至少二色。
假設 M_r(D)={c}。把 r 的 list 改為 L(r)\{c}，整個環便不可著色；
每個 list 仍至少二色。引理強迫它們全部等於某個二色 S，故

```
L(r)=S∪{c},  L(p)=S∪{d},  c,d∉S,
其他環點的 list 全為 S，P(D)={d}。
```

二色路徑的指定 singleton 有唯一反向輸入：要在一步後輸出 {d}，
前一步只能是該 list 的另一色；一路倒推至 z。故 a≠D 時 P(a)≠{d}，
p 的有效 list 必含 d。

完整公式為

```
M_r(D)={c}；
M_r(a)=S∪{c}，a≠D。
```

D 列可將 r 塗 c，其餘偶數個點交替塗 S。其他列若 r 取 S 中任一色，
令 p 取 d，兩條 r–p arc 上的私有 S 點各自交替即可；沒有 arc 奇偶限制。
若 r=c 且 c≠d，同樣令 p=d。若 c=d，將 p 的有效 list 去掉 c，
仍留至少一個 S 色；r 外於 S，剩餘偶數點的 S 路徑可以選取相應交替方向。
所以 r 原有的三色全部可取。這也證明任意 p 的位置皆適用。

保留 r,p 和任意一個私有點縮成 triangle，在 list 層具有同一公式。
**保留的是四列 root 集，不只是可著色性或 D 列 singleton。**
它不保持任意兩點 pinning，見 §5。

## 3. 同一接點 p=r

r 原 list 為 U。先不接外臂，令 R 為環本身的 root 集。R 至少二色：
若至多一色，取 U\R 中任意二色 T 作 r 的 list，環不可著色，cycle-list
引理強迫全部私有 lists 等於 T；但此時 root 集是 U\T，恰二色，矛盾。

外臂至多刪一色，所以 M_r(D) singleton 強迫 |R|=2。把 r 的 list
設為 S=U\R，環不可著色；引理再次強迫全部私有 lists 等於 S。
反之，共同 S 給 R=U\S：r∈S 時，剩餘偶數點的交替路徑兩端不同，
不可能同時避開 r；r∉S 時可交替完成。

因此完整公式為

```
M_r(a)=(U\S)\δ(P(a))，a∈U。
```

D 列成 singleton iff P(D) 是 U\S 中的一個 singleton。
其他列可能為 singleton 或二色，**不能套用不同接點型的三色列公式**。
保留 r 與任意兩個私有點的 triangle 具有同一 intrinsic root 集 U\S，
故保留所有外臂訊息下的 M_r(a)，比只保留四列更強。

一般非共同 palette 的長環仍可能有三色 R；本輪不是排除這種介面的
存在，而是證明它經外臂刪至多一色後仍有至少二色，不能出現在拒絕 D
的 bridge 串接中。S 可含 D，沒有沿用早期 S⊆{A,B,C} 的限制。

## 4. 四列接合與縮環結論的界線

固定 a，從左側 M_L(a) 沿中間路徑的二色 lists 依次作

```
T_L(X)={y∈L : 存在 x∈X，x≠y}。
```

最後訊息 X 與右側 root 可接 iff 存在 x∈X、y∈M_R(a) 且 x≠y。
直接 bridge 是零次 transfer 後作最後一次不等色測試。
這給出精確 F_C(q)，同一 a 的左右 root 使用同一色框。

§2–3 表明長環換成保留接點的 triangle 後，左右四列及中間路徑均不變，
故全部 F 保持，尤其來源若 F={D}，目標 list 模型仍 F={D}。
同點型仍有拒絕兩色的合法介面組合；只保留拒絕 D 會漏掉 minimality
所需的其他三列。這裡沒有各自任意縮臂或中間路徑。

在圖層，若能以 boundary 固定 branch sets 實現此 replacement，保留點的
attachments 不變、degree 恢復 4／5，則可依既有分量解除引理重建 minimality，
接上 R17／R19。**本輪停止在完整介面及這個條件式接續點**：未保存混合
雙環的具名來源圖、刪邊著色或合成非平面 minor，故不把 list 等價冒充
完成的來源 minor 核對。下一輪須落實這些來源證據及紙面圖構造。

## 5. 有限證書與反向控制

[程式](../scripts/c5_degree5_long_triangle_roots.py)、
[證書](../artifacts/c5_degree5_long_triangle_roots/observations.json)。Python 僅用標準庫。

| 核對 | 域與結果 |
| --- | --- |
| 不同接點、未假設共同 palette | C5 的四個 p 位置，r 三色、p 任意二／三色、其他點任意二色，共 34,560 組；DP 與完整 tuples 一致，singleton 必強迫共同 palette |
| 同點、未假設共同 palette | C5 私有 lists 全部 1,296 組；DP 與完整 tuples 一致，root 至少二色且二色 iff 私有 lists 全相同 |
| 外臂的全部四列 transfer | 從零長臂開始，在六種 pair 步驟下閉包恰 67 個 profiles；逐轉移核對閉合、保存每態最短路徑及 268 列完整 tuples 核對 |
| 必要共同 palette 的四列 | C3／C5／C7／C9、全部六個 S、全部 67 個臂 profiles；同點 1,608、不同點 2,280 組四列查詢，與 triangle 完全一致 |
| 介面與耦合 | D 列 singleton 的不同點 12 種、同點 18 種；全部 30×30×67=60,300 次橋接四列查詢，其中 4,266 次 F={D}，18 次含 D 但另拒絕一色 |

67 態是有限閉包的窮盡：任意有限臂由零長態連續加 pair 得到，閉合性給
歸納覆蓋；每態有來源路徑，沒有虛構不可達狀態。橋接也用相同 transfer
閉包。數字是介面查詢數，不是圖同構類數、disk 數或實際接線覆蓋數。

保存三項局部控制及一項耦合控制（證書 mask 僅是 U 子集編碼）：

- 一般三色 root：r 的 list U，依環序私有 lists 為 AB,AB,AC,AC，
  root 集為 {B,C,D}；任取此例的 r 與第一、第三私有點作 triangle，
  root 集變成 U。未使用 obstruction 必要性前，不能任意縮環。
- 同點的非恆定四列：S=AB、零長臂，A／B／C／D 四列依次為
  {C,D}、{C,D}、{D}、{C}。
- 二元 pinning：C5 lists 依序 {C},AB,{C},AB,AB 可著色；
  兩個 pinned 接點縮成相鄰 triangle 點後不可著色。
- 耦合雙禁色：保存左右完整四列及具體中間 pair 路徑，F 含 D 及另一色。
  這是 list 介面控制，不宣稱為符合全部 disk／T4 假設的反例。

```bash
uv run python scripts/c5_degree5_long_triangle_roots.py --check
lake build
git diff --check
```

`--check` 唯讀重算並逐 byte 比對，保存程式 SHA256、全部查詢摘要、67 個
profiles 與路徑、30 個必要介面及反向控制。不讀寫既有證書，不呼叫 planarity，
不重跑 R17／R19 已完成的大覆蓋。一般環長由 §1–3 紙面證明負責，未 Lean 化。

## 6. 精確下一步

用已證四列介面，在一長環＋triangle 的混合來源上實現保留接點的縮環：
分長環／triangle 兩側各同點或不同點的四種組合，保留實際 B-spoke 接線
及 D 葉點，核對 branch sets、degrees、四種 z 色、全部非 boundary 刪邊
著色；將 R17／R19 既有目標 obstruction minor 合成回來源。旁支情形沿用
單環排除，不重跑 topology cube 覆蓋。此後才把混合互斥雙環標為完成排除。

兩長環、共用點長環、更多環、其他 degree-5 分拆、一般共同出口及
`K∞=K≤5` 仍各自開放；不聲稱保持完整 boundary Σ 或 T4。
