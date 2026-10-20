# 同一來源的十個五度商圖與十四個六角洞完成圖

固定 BASE 及完整來源同 [CHORDS](CHORDS.md)。本頁給任意大小的合法
完成比較及其精確完整 fibre 接口；不宣稱這些比較足以證主目標。
全部新增輸入與 SHA256 見 [INPUTS.json](INPUTS.json)。

## 1. 十張合法 k−2 五度商圖

p,h 的完整原 facial links 分別是 `(a,b,q,h,n)`、`(p,q,L,R,n)`。
在其中一個五度點 z 的 link 中，任意非連續點 u,v 必非邊：否則原
triangle zuv 不是 z 的五個已指定原面之一，違反每個原三角形皆為面。
故刪 z 後可在實際五邊面畫 uv arc 並收縮，得到以下十張獨立圖：

| 刪點 | 五個識別 pair |
| --- | --- |
| p | a=q, a=h, b=h, b=n, q=n |
| h | p=L, p=R, q=R, q=n, L=n |

每張的 arc 都在該張圖的一個實際面內；不把交錯的 pairs 同時收縮。
每張 pair 至多包含一個原 B 點。識別無 loop，僅抑制平行重複邊，並
保留原 B 邊 copy；因此每張是同原框 `(x,y,a,b,c)` 的合法簡單 plane
C5 disk。原 G 有 k+5 點，刪一點並識別兩點後有 k+3 點，故完成
內點數恰 **k−2**。沒有新點、換框或漏算的接回成本。

因 G 是所有目錄外 disk 的全域最小來源，**每張圖的完整支援必在 K132**。
這是全稱必要條件；它不保留其原度數、r6 或 941 身份。

## 2. 同一 E 的全部完整 fibres

E 是原 `G-{b,p,h}`，有序框 `(a,n,R,L,q,c,x,y)`。
固定任一原框字面列 `(x,y,a,b,c)`、一份完整 E 著色。

若刪 p，剩餘 cap 點是 h；全部合法 h 色恰為
`h outside {q,L,R,n}`，並保留原 `b outside {a,c,q}`。
若刪 h，剩餘 cap 點是 p；全部合法 p 色恰為
`p outside {a,b,q,n}`，並保留同一 b 不等式。
然後只加該張 quotient 的一條 u=v 等式。

這覆蓋每條剩餘原邊，且原完整 stars 保證無其他 cap 附件。因此這是
完整著色雙射：固定同一完整 E 著色，取其全部剩餘 cap lifts，再作
實際識別；反向沿商映射拉回、記錄 cap 色值即可。

certificate 的 `quotient_interfaces` 對十張圖、每一個原字面列，保存
**全部**有效 `(C8_id,n,R,L,q,survivor)`；空 fibres 存空列表。
對同一個原 E 完整計數向量 e，該張圖每列計數就是遍歷列表求 `e[C8_id]`
之和。canonical id 只使用全圖統一的色置換；其數值是固定代表的延拓數，
不是色軌道總數。不同圖沒有拼接接受或拒絕。

## 3. 十四張 k−2 六角洞三角化完成圖

刪原 p,h，實際洞 rim 是 `(a,b,q,L,R,n)`。
每組三條互不交叉六角形 diagonals 形成一個無新點填片，共 Catalan
數 C4=14 組。它們都在同一實際原洞內畫出；若某條新 inequality 已有
外側同端點邊，只抑制平行 copy，染色約束完全相同。
原 B 及全部外側邊、私有點保留，所以這是合法完成 C5 disk，內點
數 k−2。全域最小性使十四張的完整支援也都在 K132。

`filling_interfaces` 保存各張三條對角線及全部
`(C8_id,n,R,L,q)`。固定同一 E 的每份完整著色後，只檢查這三個不等式；
沒有新增內點色值要任意挑選。`minimality.py:triangulations(6)` 的標準
順序是六角形索引 `(0,1,2,3,4,5)=(a,b,q,L,R,n)` 下的 lexicographic
三組 pair tuples；root 的其他共同完成可重用這個 convention。

## 4. 兩份控制的精確作用

| 控制 | 十張五度商圖 | 十四張六角洞完成圖 |
| --- | --- | --- |
| Q2_source_positive | 九張在 K132；`(G−h)/(L=n)` 恰 941 | 全在 K132 |
| allK_source_positive | 全在 K132 | 全為 1023，在 K132 |

前者若有真來源實現，具名合法 `(G−h)/(L=n)` 有完成 k−2 內點，且
其完整支援 941 不在 K132，會違反原全域最小性。這是另一條精確
真來源排除鏈；前者本來也會由合法 k−4 的 Q2 排除，不當成更強縮減。
後者完全通過本頁二十四張比較；因此這些必要條件還不能迫出本輪目標。

這沒有排除其他未列圖、其他完整支援證書，也沒有證明 allK 可實現。
完整逐列 counts、完整 masks 及 K132 membership 都保存在
`quotient_control_projections`／`filling_control_projections`，由同一份
frozen 控制向量計算。

## 5. 重播與分工界線

```
python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/B/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/B/check.py
```

checker 只用標準庫、預設唯讀，對照 SHA、完整 pocket、全部 cap lifts
與精確整數 counts。負控制破壞 q 度數前提、完成成本、c=4 分支、單個
完整 lift 及同一來源向量，皆拒絕。幾何合法性由本頁實際面操作證明；
程式只重播有限接口，沒有用程式枚舉替代 arbitrary-size 圖論證明。
