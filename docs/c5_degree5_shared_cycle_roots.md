# 共用點雙奇環：四列可延拓介面與縮環反向控制

發布註記：本報告與 R21–R23、Lean 接合基礎一併發布，核對見 [STATUS §27](STATUS.md)。
以下保留研究輪當時的提交狀態與驗證範圍。

2026-09-18，R23。接手 HEAD `3d6a647` 及未提交 R21–R22。
本輪完成共用 cut vertex 雙環的 **fixed-q list 可延拓判準**，並找到
縮環不保持完整 root／交集的具體控制。尚未完成真正來源 minor、
degrees、逐邊刪除著色及 R15 拓撲證書合成，故不新增 disk 排除結論。
紙面介面論證＋Python 有限驗證，未新增 Lean theorem。

## 1. 一般奇環在自由 root 的二色剛性

令奇環為 r,v1,…,v(2k)，r 的 list 為 U={0,1,2,3}，其餘 lists
至少二色。記可延拓的 r 色集為 E。則 |E|≥2，且

```
|E|=2 iff 所有私有 lists 都是同一個二色 S；此時 E=U\S。
```

證明可直接用路徑傳遞。固定 r=c 後，v1 的訊息是 L(v1)\{c}，
沿路徑每步把前訊息的 singleton 從當前 list 扣除。任一步訊息
至少二色，之後每步都恢復當前整個 list，最後必能避開 c。
因此 c 被拒絕時，每步必為 singleton，末端強迫色必為 c。
若不同 c,d 都被拒絕，第一個 list 必為 {c,d}，兩個傳遞的
singleton 互異；逐點歸納，每個 list 都必為 {c,d}，且兩個
傳遞交替。反之共同二色奇環恰拒絕這兩色。這同時排除三個
被拒絕色，並證明所述充要條件。非均勻 lists 可給三色或四色 E。

## 2. 共用點的精確接合與 D 剛性

沿用 [R15 位置分類](c5_degree5_shared_triangles.md)：r 已用滿
四條環邊，沒有外臂或 spoke；兩臂在同環不同私有點、分處兩環、
同一私有點會合，或整個 cluster 在無接點旁支。旁支交回既有消去。

固定 z=a，先求兩臂的完整訊息，只有 singleton 會禁止其端點一色。
不同端點原為三色 list、共同端點原為 U，扣除後每個私有 list
仍至少二色。共同 root 色集恰為 E1(a)∩E2(a)。由 §1，交集為空
**恰在兩環各自全部私有有效 lists 是共同二色 S、T，且 T=U\S**。
這是任意兩環長度的公式，不使用 bridge 兩端 singleton 判準。

D 被拒絕因此固定這對互補 palettes。各未標記私有點的 list
已固定為其 palette；不同端點 p 原 list 為 S∪{c}，臂在 D
必輸出 c∉S；同點會合時兩臂必輸出 U\S 的兩個不同色。

## 3. 縮環保留的是四列可延拓布林值

每環保留 r 與兩個私有點。若同環有兩個不同接點，兩者都保留；
只有一個接點時另保留一個未標記點；無接點時任保留兩個私有點。
這在 list 層給出共用 r 的雙 triangle。逐個 a 比較：

- 分處兩環：兩個目標各保留一個 palette 錨點；目標拒絕 iff
  兩個標記點都回到各自的原 palette，與來源相同。
- 同環不同點：另一個無標記環固定其 palette T，因此目標要拒絕
  必須讓有標記環的兩點都為 S=U\T；這也等價於來源拒絕。
- 同點會合：有標記環仍保留一個 S 錨點，另一環固定 T；兩者
  拒絕 iff 標記點的有效 list 為 S，來源與目標相同。

故四種 a 的「能否延拓」及完整禁色集合 F 相同。不同端點型
還有指定 singleton 的唯一反向輸入，故 F={D}；同點型可能另拒
一色，不能只檢查 D。有限控制中保存 240 個此類雙拒絕查詢。
它們是介面控制，不是 minimal obstruction 候選。

**完整 E_i(a) 甚至 E1(a)∩E2(a) 不保證相同。** 以 bitmask
表示色集，bit c 對應顏色 c，U=15，S=3={0,1}，T=12={2,3}。
兩臂皆零長且 D=3，原標記 lists 都為 S∪{3}。在 a=0：

```
來源 J1 lists = [15,10,3,10,3]，root 色集 = 15；
保留 r 及兩接點的 triangle lists = [15,10,10]，root 色集 = 5；
另一環 root 色集 = S=3；
共同 root 交集從 3={0,1} 變為 1={0}，但兩者都可延拓。
```

另保存 [15,10,10,3,3] 的 root 13 對 triangle root 5。
這些控制禁止把本輪介面升格為 root 關係或任意 pinning 保持。

## 4. 有限證書與重播

[程式](../scripts/c5_degree5_shared_cycle_roots.py)、
[證書](../artifacts/c5_degree5_shared_cycle_roots/observations.json)。
沿用 R20 的 67 個完整四列外臂 profiles（所有二色路徑訊息的閉包）。

| 核對域 | 數量 |
| --- | ---: |
| C5 所有至少二色私有 lists，獨立暴力 coloring 對照 | 14,641 |
| C7 全二色私有 lists，核對二色剛性 | 46,656 |
| 同環不同點四列比較 | 27,750 |
| 分處兩環四列比較 | 10,560 |
| 同點會合四列比較 | 5,280 |

後三類取環長 3、5、7、9，全部六個 palettes、D 相容 profiles
及保留接點位置；分處兩環採同長同位置的控制，沒有枚舉全部
有序環長對／位置對。一般結論來自 §1–3，不依賴有限控制窮盡。
證書保存 query digest、腳本及依賴指紋、兩個具體反向控制。

```bash
uv run python scripts/c5_degree5_shared_cycle_roots.py --check
lake build
git diff --check
```

`--check` 唯讀重算、逐 byte 比對；沒有 topology oracle。
本輪另重播 R22 checker，未重跑 R15／R17／R19 大型拓撲覆蓋。

## 5. 精確停止點

下一步建立這三類的真正 boundary 固定來源 minor，保留 r 和接點，
核對完整 degrees、四列可延拓布林值與每條非 boundary 刪邊著色，
再合成 R15 的既有非平面證書。至少涵蓋一長環及雙長環、偶數 arc、
同環三個保留點、同點 F={D} 與雙拒絕反向控制。

不能要求完整 root 色集相同；應直接核對 §3 的較弱四列判準，
再由 degree-4 分量解除引理及 F={D} 重建 minimality。
共用點長環的 disk 排除、更多環、其他 degree-5 分拆及主命題仍開放。
