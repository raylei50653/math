# 三-spoke 的任意樹分量排除與連通外框 K4 引理

發布整理（2026-09-18）：本報告隨 R11–R15 五輪成果一併提交。下文的
「未提交／HEAD／下一題」保留各輪當時狀態；最新停止點見
[HANDOFF](HANDOFF.md)，發布前核對見 [STATUS §16](STATUS.md)。

後續（2026-09-18）：[單 triangle 報告](c5_degree5_triangle_components.md) 已排除
一個 triangle 加任意 bridges 的二接點分量，涵蓋全部接點位置；下一題是
恰一個長 odd-cycle。以下保留本輪原始證明與停止點。

2026-09-18。接續 [區域化約](c5_degree5_sectors.md)；HEAD 仍為 `be97121`，
前輪成果留在工作樹。本輪完成兩個不限制內點數的紙面結論：

1. 唯一 degree-5 點 z 至少有一條 boundary spoke 時，minimal q-obstruction
   的 degree-4 分量不含 K4 block。此項只需 planarity，不需 T4。
2. z 有三條 boundary spokes、H−z 是單一二接點**樹**分量時，不存在接受
   全部 T4 的 C5 disk minimal q-obstruction。兩接點可在樹的任意位置，
   允許任意分叉、尾枝與主路徑長度。

第二項以紙面分枝化約及色序列縮減，接上 648 個必要小模板的非 disk
證書。不是從短路徑測試外推。兩項皆未新增 Lean theorem，未處理含 cycle
的二接點分量，也未證一般 degree-5 單缺失或 `K∞=K≤5`。

## 1. 連通外框排除 degree-4 分量的 K4

沿用 [完整介面](c5_degree5_interfaces.md)：C 為 H−z 的一個連通分量，
每點完整 degree=4。取 q 下被 C 拒絕的一個可用 z 色 a。
minimality 的 private-color 條件保證每個 C 都有這樣的 a；固定外部色
q 及 z=a 後，C 不可著色，但刪除任一碰 C 的邊都可著色。
後者也可直接由前報告的分量解除引理得到。

設 J 是 C 的 K4 block。J 的每點已有三個 clique 鄰居，故恰有一個外接
方向：直達 X=B∪{z}，或沿 C 中的一條 bridge 進入一個外側分量。
這些 bridge 外側互不相交；若同時返回 J 的另一點，就不會是 K4 block。

刪去其中一條 bridge，兩側根的可取色集都非空。若能選到不同色，就可
拼回 C 的 coloring；因此兩側都只能取同一個 singleton 色。
外側必碰 X，否則其 coloring 可任意置換四色，根不會只有一色。
所以可從 J 的每點選一條抵達 X 的路徑，四條路徑的內部互不相交。

若 z 有 boundary spoke，X 在來源圖中連通。將 X 及四條路徑去掉 J 端點
後的部分合成一個 hub branch set，J 的四點各為 singleton，得到 K5 minor。
這與 planarity 矛盾。最後的 hub 會識別 boundary，只用來證非平面性；
不宣稱它是 boundary-state 操作。

此證明重新核對了 z 的多接點，不是直接套用「整張 H 全 degree=4」的舊
定理。它涵蓋 t=1、2、3 的所有接點分拆；**t=0 時 X 不連通，未涵蓋**。
checker 另保存一張含 K4、兩個 z 接點及兩個 D forcers 的具名 minimal
q-obstruction，直接核對來源圖上的五個 K5 branch sets，不用 planarity oracle。

## 2. 任意樹先保留兩接點間的主路徑

以下取 t=3。由前輪區域化約，只需固定
N_B(z)={b0,b1,b4}，C 全部位於 arc (b1,b2,b3,b4) 一側。
q=(A,B,A,B,C)、D 為第四色，且 **F_C(q)={D}**。
本節以 C 表示分量；句中的「C 色」表示 q 的第三色。

假設分量 C 是樹，兩接點為 s、t。取它們間的唯一主路徑 P。
每個 P 外分枝 F 只以一條邊連到某個 v∈P，而且不含 z 接點；固定 q 後，
它的 root 介面不依賴 z 的取色。

在 z=D 下刪該 bridge，由 minimality 得到可著色的兩側。原圖不延拓，
所以兩側 root 可取色集都必為同一個 singleton {c}。
因此，F 對主路徑的精確限制只是「v≠c」，對**全部四種 z 色**都一樣。

在每個 v，把原 boundary spokes 的 q 色與各外枝強迫色放在一起。
它們必互異：若兩項重複，刪一條相應 spoke／bridge 後仍有相同限制，
原 q 仍不延拓，違反 minimality。主路徑端點另外有 z=D 的限制，故
端點的上述兩項都不能等於 D。完整 degree=4 保證每個主路徑點，扣除
沿 z∪P cycle 的兩條邊後恰有兩個外接方向，消去後的 residual list 大小為二。

## 3. 分枝化約保留完整的固定-q 禁色集

所有替換都固定五個原 boundary 頂點，不識別同色 boundary。

- 若分枝強迫 c≠D，它必碰到一個 c 色 boundary 頂點；否則在分枝內交換
  c、D 會破壞 singleton 強迫性。將整個分枝收縮進 v，只保留一條實際
  c 色 spoke。這與原分枝在 q 下同樣只禁止 v=c。
- 若分枝強迫 D，它必碰到全部三個 q 色，理由同樣是缺色交換。將整個
  分枝收縮成一個與 v 相鄰的 D 葉點，每個 q 色只留一條實際 spoke。
  其 root 在 q 下仍恰取 D。

不同分枝互不相交。非 D 分枝可一起併入各自的 v；D 分枝各自收縮，
boundary 始終 singleton。替換後仍是 disk minor，所有非 z 內點 degree=4。
每個主路徑點至多有一個 D 葉點；s、t 都沒有 D 葉點。

所得正常形只有主路徑及若干 D 葉點。它保留 **F_C(q) 的全部四個查詢**，
因此仍為 {D}；沒有只檢查 z=D 而遺失三個刪-spoke 條件。
用完整介面的 minimality 充要條件，正常形仍是 minimal q-obstruction。
不聲稱保持其他 boundary rows、完整 Σ 或 T4；後續排除只需要它是 disk。

若主路徑某點 residual pair R 含 D，它有兩條禁止其餘 q 色的 spokes。
若 R 不含 D，它有一條禁止剩餘 q 色的 spoke，及一個三-spoke 的 D 葉點。
所有實際 boundary 接點仍在 (b1,b2,b3,b4) 上。

## 4. 二色 lists 等價於從 D 回到 D 的色序列

令主路徑依序有 residual pairs R₁,…,Rₙ；z 同時鄰接兩端。
固定 z=a，第一點可取 R₁\{a}。沿路徑傳遞可取色集時，一旦某點有兩種
選擇，下一點的二色 list 也全可取，此後不會再變成 singleton。
所以拒絕 a 的充要條件是每一步都被迫，且最後一點恰被迫取 a。

把被迫色記成 c₀=a,c₁,…,cₙ=a，就得到

```
Rᵢ={cᵢ₋₁,cᵢ},    cᵢ₋₁≠cᵢ.                            (1)
```

若同時拒絕兩個不同色 a、b，兩條被迫序列在每一步都互異。因此每個
Rᵢ 都只能是同一 pair {a,b}。反過來，共同 pair 的偶數點路徑恰拒絕
該 pair，奇數點路徑不拒絕任何色。

於是 **F_C(q)={D} 等價於 (1) 有 c₀=cₙ=D，且色序列使用至少三色**。
這一次直接把 minimality 的全部 z 色查詢放進判準；前輪 F={C,D} 的
負控制正好是只用兩色的退化情形，不會混入後續 normal forms。

checker 對長度 1 至 5 的全部 9,330 組二色 lists，以被迫序列、集合傳遞、
完整 color tuples 三種求值交叉核對。任意長度結論由上述歸納承擔。

## 5. 任意色序列縮到五型

在 c₀…cₙ 中，若 cᵢ=cⱼ，可刪除 i 到 j 之間的閉子序列，只要剩餘序列
仍使用至少三色。每次嚴格縮短；有限次後停止。完整分類如下，其中 a、b、c
為互異的非 D 色，左右方向仍保留。

| 名稱 | 不可再刪的色序列 | 主路徑點數 | D 葉點數 |
| --- | --- | ---: | ---: |
| triangle walk | D,a,b,D | 3 | 1 |
| split walk | D,a,D,b,D | 4 | 0 |
| nested walk | D,a,b,a,D | 4 | 2 |
| square walk | D,a,b,c,D | 4 | 2 |
| lollipop walk | D,a,b,c,a,D | 5 | 3 |

這些名稱描述色序列，不表示分量 C 含 cycle；C 仍是樹。

**覆蓋證明。** 若 D 在序列內部出現，分成多個 D-excursions。任何一次
刪除都必使剩下的序列只用兩色；因此只能有兩段，各自只用 D 與一個
不同非 D 色。段內沒有 D、相鄰色又不同，兩段只能各長二，得到 split。

若沒有內部 D，而某個非 D 色 x 重複，刪去兩個 x 間的段後必只剩
D、x。因相鄰色不同且沒有內部 D，這兩個 x 必位於第一與最後內部位置。
它們之間不能再有重複色，否則可刪除而留下至少 D、x 及另一色。
故得到 nested 或 lollipop。若非 D 色沒有重複，只有 triangle 或 square。
這也解釋為何只保留三／四步序列並不完整：五步的 lollipop 必須保留。

**每次刪除都是真 minor。** Rᵢ 對應主路徑的第 i 個頂點；刪掉該段的
spokes 及 D 葉點，再收縮對應的連續路段。若刪除碰到路徑頭尾，將該段
併進 z；否則併進前一個保留路徑點。z 可同時吸收前綴、後綴，branch set
仍經 z 連通。其餘保留點及葉點的 attachments 不變，boundary 固定。

每個保留路徑點仍有兩個 cycle 方向及原外接部分，所以 degree=4；z 仍
有三條 spokes 與兩個路徑鄰居，degree=5。縮後序列仍從 D 回 D 且用至少
三色，§4 再給 F={D}，故 minimality 亦可獨立恢復。步驟沒有聲稱保存 Σ。

## 6. 五型的全部實際接線都非 disk

沿固定 arc，A 色只有 b2，B 色可為 b1 或 b3，C 色只有 b4。
對含 D 的 residual pair，兩條 spokes 各自選一個被禁止色的實際頂點；
對不含 D 的 pair，選剩餘 q 色的 spoke，並為 D 葉點選 A、B、C 各一個。
所有點獨立選擇，**不假設相同 palette 就有相同 attachments**。

| 色序列類型 | 具體 palette 序列 | 全部 lifts | disk |
| --- | ---: | ---: | ---: |
| triangle | 6 | 48 | 0 |
| split | 6 | 48 | 0 |
| nested | 6 | 168 | 0 |
| square | 6 | 96 | 0 |
| lollipop | 6 | 288 | 0 |
| 合計 | 30 | 648 | 0 |

每個 lift 的 boundary-apex 圖都含保存的 K5 或 K3,3 subdivision，共用
31 份證書。`--check` 只重播實際路徑、來源邊、內部互斥及 branch 接線，
不重新呼叫 planarity。所有 lifts 另直接核對 F={D}、degree 及逐非 boundary
邊刪除後的完整 q-coloring。模板至多九個內點，是紙面化約的目標上界，
不是 k≤9 圖 catalog，也不是原圖或一般 minimal obstruction 的內點上界。

至此證成任意樹排除：假想來源 disk 先由 §2–3 化為正常形，再由 §5 縮成
上述某個 lift；boundary 固定的 minors 必仍 disk，與 subdivision 矛盾。
只在最初區域定位使用接受全部 T4，沒有假定中間 minors 保持 T4。

## 7. 證書、驗證與新停止點

[checker](../scripts/c5_degree5_tree_components.py)、
[certificate](../artifacts/c5_degree5_tree_components/observations.json)。

- 9,330 組完整二色 list 控制；22,128 條長度至多十的至少三色閉序列，
  皆按明列規則縮至五型。這是局部控制，無界覆蓋由 §4–5 證明。
- 648 個 lifts 全部保存 degree／F／刪邊 coloring，31 份 subdivisions。
- 30 個具名長正常形、60 次縮減；逐步與合成的 boundary 固定 branch sets，
  最終 K5／K3,3 minor 再合成回各自來源的 apex 圖。
- 10 個具名原始樹控制：非 D forcing 尾枝、長 D 分枝、D 分叉樹，保留
  各分枝的完整 root 可取色核對及真正收縮；包括接點不在原樹葉端的例子。
  這些控制同樣保存來源圖上的非平面 minor。
- 一個 K4／二接點控制，保存固定 q 禁色、逐邊延拓及來源圖上的 K5 minor。
  它是明知非平面的控制，不是 disk witness。

程式與前輪區域證書保存 SHA256，`--check` 重算後逐 byte 比對。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_tree_components.py --check
uv run --with networkx==3.5 python scripts/c5_degree5_sectors.py --check
lake build
git diff --check
```

本輪實際驗證見 [STATUS §12](STATUS.md#12-三-spoke-任意樹排除接續未提交區域成果)。
紙面 topology／minor、Python 有限證書與 Lean 狀態分開：未新增 Lean theorem，
沒有重播舊全量 catalogue／deletion audit，也沒有修改前輪 scripts／artifacts。

**新停止點：C 必有 odd-cycle block。** Gallai 必要條件沿用前報告，§1 排除
K4，§2–6 排除無 cycle 的樹。下一個窄問題選 **C 恰有一個 triangle block，
其餘為 bridges**：保留兩接點到該 block 的路徑及共同色框，研究雙接點
接回 z 後的禁色。不能把 triangle 的不同接點拆成獨立 root marginals。

含 cycle 的三-spoke 分拆 (2)、其他接點分拆的一般幾何排除、t=0 的 K4、
一般 degree≥5、單側／共同出口、候選 A 與 `K∞=K≤5` 均仍開放。
本輪及前輪成果尚未 commit／push。
