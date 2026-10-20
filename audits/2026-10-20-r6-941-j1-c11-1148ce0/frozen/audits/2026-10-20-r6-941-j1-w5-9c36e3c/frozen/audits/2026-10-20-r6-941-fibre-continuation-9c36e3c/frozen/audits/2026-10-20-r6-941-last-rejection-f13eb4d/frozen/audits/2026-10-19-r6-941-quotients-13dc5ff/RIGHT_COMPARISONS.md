# 原 r 六角洞的同源較小比較

本頁在 [完整來源契約](SOURCE_CONTRACT.md) 的同一 G 上操作。
原 r 的完整 facial link 是 `(x,y,t,w,v,s)`；原三角皆面，因此六圈沒有
非連續頂點間的原邊。刪 r 恰留下這一個六角面，所有其他邊及私有點保留。

六圈的九對非相鄰點各可在洞內畫弧再識別。每對至多含一個原框點；
沒有 loop，不合併兩個原框點，只抑制重邊，仍保留原有序 B。各圖刪一點、
識別一次，完成內點數 `k−2`。另可在同一洞的內部加三條對角線三角化，
全部14種各完成 `k−1`。不要求這些比較圖保留原度數或 r6。

左側原 p,h 洞與原 r 星的內部互不相交；其各次原共面操作可以一起完成。
因此上述右商圖接原 Q1、Q2、G_B，完成成本分別是 `k−6,k−6,k−4`；
右三角化接這三候選則是 `k−5,k−5,k−3`。
左右六角洞各取14種三角化的196個組合完成 `k−3`。操作不新增任何點，
沒有額外重建成本。全域最小性使這些實際同源嚴格較小圖的完整支援都在 K132。

[right_minimality.py](right_minimality.py) 從固定同一 E 字面列，逐一枚舉
全部 `(s,v,w,t)`；刪 r 後保留原 `xs,yt` 及全部 core 邊，再施加所選
商等式或對角線不等式。每份 lift 記回同一個 D10 的固定字面 fibre，
不是把不同 core 的 lifts 相乘。完整資料含空集合存於
[right-minimality.json](right-minimality.json)。原左 cap 的全部 lifts 與
左洞三角化據此同步投影同一 Z，產生完整十列固定字面計數。

兩份封存正值控制對以上**全部**比較圖都給 K132 支援，故這批新增最小性
比較仍容 `allK_source_positive`，不能據此完成主目標。比較圖的真實存在、
合法性、完成大小與最小性鏈只用於實際來源；必要向量沒有被當成來源。

獨立 [C/review_right.py](C/review_right.py) 不匯入本程式、B 的矩陣或舊
model，以全部 proper 字面 C10 著色及另一個 Catalan 遞迴重建14種三角化，
核對兩控制共576份完整十列計數；它也不提供來源實現。

```bash
python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/right_minimality.py
python3 -B audits/2026-10-19-r6-941-quotients-13dc5ff/C/review_right.py
```

預設唯讀；`--build` 只以 exclusive-create 保存證書。這是方法足夠性的
負結果，主目標的同一候選三拒絕仍另行判定。
