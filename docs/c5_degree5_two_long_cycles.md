# 兩個互斥長奇環：連續縮減與來源 minor

發布註記：本報告與 R21–R23、Lean 接合基礎一併發布，核對見 [STATUS §27](STATUS.md)。
以下保留研究輪當時的提交狀態與驗證範圍。

2026-09-18，R22。從 HEAD `3d6a647` 及未提交 R21 接續，完成交接指定的
雙長環來源與兩步縮減。R21 scripts／artifacts 原封保留，未 commit／push。

**唯一 degree-5 點 z 有三條 boundary spokes，C=H−z 是連通二接點分量，
blocks 恰含兩個互斥 odd cycles、其餘為 bridges 時，不存在接受全部 T4
的 C5 disk minimal q-obstruction。** 兩環長度、外臂、中間 bridge 路徑
及無接點外枝均無上限。本輪補完兩環都長的情況，與 R16–R21 合成上述
任意兩個互斥 odd cycles 的結論。共用點且含長環的情況不在此結論中。

這是紙面化約＋Python 有限來源證書，未新增 Lean theorem，不是完整 Σ
保持或一般 degree-5 排除；`K∞=K≤5` 仍未證。

## 1. 雙側必要性不要求另一側為 triangle

沿用 [R21 §1](c5_degree5_long_triangle_minors.md) 的區域化約與旁支消去：
q=(A,B,A,B,C)，N_B(z)={b0,b1,b4}，F_C(q)={D}，分量 attachments
位於 arc (b1,b2,b3,b4)；鏡像相同。每個非 z 有效內點完整 degree=4。
如果中間 bridge 不分隔兩個 z 接點，消去無接點側後交回單環／樹結果。
否則兩臂各到一環，環間保留一條二色 list 路徑。

對任意固定 z=a，每側 bridge root 的色集 M_i(a) 非空。不同接點型的
root 原 list 有三色，其他有效環 lists 至少二色；若不可著色，cycle-list
引理會要求每點皆為同一二色，與 root 三色矛盾。同點型的 root 原 list
U，外臂至多刪一色，仍至少三色，理由相同。

若 M_1(D) 或 M_2(D) 至少二色，可從另一端任選一色，沿中間二色 lists
貪婪延伸，最後用該至少二色端點避開前一色，故不能拒絕 D。因此兩側
M_i(D) 均為 singleton。這個論證只用非空 root 與中間二色 lists，
**不要求任何一側已是 triangle**。

現在可分別使用 [R20 §2–3](c5_degree5_long_triangle_roots.md)：各側私有
環 lists 必為共同二色 S_i。不同接點型的四列為 D 下 singleton、其餘
三列原三色 list；同點型為 (U\S_i)\δ(P_i(a))。S_1,S_2 無須相等或互補，
也不假設它們不含 D。兩側的四列及中間路徑在共同 z 色 a 下精確接合。

## 2. 第一步後第二側的前提逐項保持

用 [R21 §2](c5_degree5_long_triangle_minors.md) 的三段 arc branch sets
先縮 J_1 為 triangle，保留其 bridge root、外臂接點與需要的私有點：

- M_1(a) 的四列完全相同；J_2 的全部點、邊、attachments、外臂及中間
  bridge 路徑原封不動，所以 M_2(a) 也完全相同。
- 因此精確串接給 F_C(q)={D}；另一側 singleton 必要性仍成立。
- J_2 的接點型、S_2、lists 與完整 degree 都沒有改動。
- z 仍 degree=5，其餘有效內點仍 degree=4；分量連通、兩環仍互斥。
  q 下實際禁色互異。分量解除引理及三條 z-spokes 的刪除測試重新給出
  minimality，而非援引一般 minor 自動保持 criticality。

故可合法縮 J_2 為 triangle，再次保留全部四列、degrees 與 minimality。
也可交換順序；沒有中途重選色框、boundary 接線或臂的訊息。

兩次縮減只作用於互斥的環點及各自被移除點的 attachments，boundary
和 z 始終 singleton，兩條臂與中間 bridge 保持。把兩份 branch sets
取合成即為來源到雙 triangle 的 boundary 固定 minor；交換順序得到
同一份合成 branch sets（固定每環保留點與 arc 收縮方向後）。
這是本構造的可交換性，不是任意圖 minor 或任意壓縮規則可交換。

## 3. 排除與信任界線

假想原圖為 C5 disk，兩次 boundary 固定 minor 後仍是同一指定 arc 的
C5 disk；全部 degree、F={D} 與 minimality 條件保持。
雙 triangle 目標的兩側不同接點型交給 [R17](c5_degree5_bridge_arms.md)，
至少一側同點交給 [R19](c5_degree5_bridge_mark_minors.md)。其完整接線
覆蓋排除 disk，得到矛盾。後續結果不要求中間目標保持全部 T4；T4 僅
在來源區域定位使用。旁支型由 §1 交回既有單環／樹。

這補完雙長環；零個長環由 R16–R19、一個長環由 R21，因此兩個互斥
odd-cycle blocks 的任意長度均已處理。無界性來自 §1–2 的一般公式與
branch-set 構造，再接既有任意臂長化約及完整接線覆蓋。
以下固定域驗證實作與機制，不取代紙面無界證明或 Lean 形式化。

## 4. 來源證書與重播

[程式](../scripts/c5_degree5_two_long_cycles.py)、
[證書](../artifacts/c5_degree5_two_long_cycles/observations.json)。

沿用 R21 的 144 個具名控制，將剩餘 triangle 也展開；有序環長取
(5,7)、(7,9)、(9,5)，三段 arc 含偶數長，保留實際 B-spokes 和 D 葉點。
同一來源構造兩個中間圖，分別保留第一／第二長環，最後抵達原雙 triangle。

| 核對 | 結果 |
| --- | --- |
| 雙長環來源 | 144 張，四種有序接點型各 36 張；沿用短／長路徑代表及六種第一側 palettes，實際有 21 組有序 palette pairs |
| 兩個順序 | 288 條兩步縮減、576 個逐步 minor；兩種合成 branch sets 逐來源完全一致 |
| 四階段圖 | source、兩個不同中間圖及 target，逐張核對完整 degrees、連通性、互斥環長、固定-q 四種 z 色及全部非 boundary 刪邊 coloring |
| 直接四列 root | 各階段在兩個 bridge roots 切開中間方向，保留該側實際圖／外臂／D 葉點，作 18,432 次 (z色,root色) pinning 查詢；兩側四列跨階段完全相同 |
| 刪邊著色 | 來源 12,258 份；四階段合計 37,224 份，逐 witness 核對 q 與每條邊不等色 |
| 來源拓撲 | 重驗既有 target subdivision，合成 K5／K3,3 minor 到每張 source apex 圖，直接驗證來源邊與 branch sets |
| 來源追蹤 | 保存腳本／依賴／R21 輸入 SHA256，先驗既有來源及輸入指紋 |

21 組 palette pairs 是這個控制域的實際覆蓋，沒有宣稱窮盡所有 palette
接線；一般證明不需要這個有限集合窮盡。沒有呼叫 planarity oracle，
沒有重跑 R17／R19 的大型拓撲覆蓋。

```bash
uv run --with networkx==3.5 python scripts/c5_degree5_two_long_cycles.py --check
lake build
git diff --check
```

`--check` 唯讀重算並逐 byte 比對。本輪沒有更動 R21 或更早研究程式／證書。
R21 checker 已於前輪通過；本輪直接重算所用圖與 witness、核對輸入指紋，
不把這些核對稱為重跑完整 R21 checker。

## 5. 精確下一題

下一題是**兩個共用 cut vertex 的 odd-cycle blocks，至少一環長於三**。
先沿 [R15 §1–4](c5_degree5_shared_triangles.md) 分：兩臂在同環不同點、
分處兩環、同一私有點會合，以及整個 cluster 在無接點旁支。
共用 cut vertex 已用滿四條環邊，不能再接外臂、spoke 或 z。

先求四個 z 色下、共同 cut vertex 的完整可用色集及兩側交集；不得把
本輪的「bridge 兩端 singleton」移用到共用點。尤其一般長環有三色 root，
而同環二接點可能需要保留三個標記點，須先驗證縮環充分性與反向控制，
再做來源 minor。尚未將此分支列為排除。

更多環、其他 degree-5 分拆、一般出口、候選 A 及主命題仍開放。
