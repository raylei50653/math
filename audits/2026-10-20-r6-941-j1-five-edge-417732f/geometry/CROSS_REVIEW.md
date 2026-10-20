# residual 分支獨立交叉審查

審查範圍為 sibling [residual/check.py](../residual/check.py) 與其
[certificate.json](../residual/certificate.json)。逐段讀取生成器，並以
獨立 stdlib 小程式從證書的原面、邊與染色重建以下有限結論；未重複
全部染色枚舉。全套正常／seed17重播由本輪主審統一執行。

**在已列 local-disk／精確傳輸範圍內通過；沒有阻擋問題。**

1. W7 與獨立凍結八點 disk 沿同一條原 hL 邊接合。W7 的內部 R 與
   另一片的 k5/k6/k7 互異，兩片只共 h,L；hL 恰屬兩面。重建得到
   14點、29邊、16個三角面，Euler 值1，外框恰為
   `(n,h,d4,d3,d2,L,u1,u2,u3,u4)`。生成器另逐點核對完整 link 為
   一條路或一個圈，足以校準這個明列接合確為三角化 disk。
2. 原 R 的完整鄰集恰 `{n,h,L,u1,u2,u3,u4}`，沒有漏掉 h 或任何
   新路點。整圖直接枚舉，與刪 R 後每份完整核心著色的全部合法 R
   lifts，分別建立後比較集合相等；並按全部59052個 proper字面外框
   保留空 fibres。此處 h 留在核心，所以 full R cap 檢查七個鄰點。
   counting 分支刪 h 的 F13 左 cap 另把 h 當作變數，兩個模型的取法
   相容但不可將此處七點 mask 換成六點。
3. 初始兩份完整染色均逐邊 proper，且同時含實際12五邊路
   `n-u4-u3-u2-u1-L`。初始觀測恰一個完整 fibre。每個合法 rooted
   Kempe action 使用全圖實際分量；私有 k5/k6/k7 與 R 都未被刪出
   分量。生成器在全部完整染色上另核對 action 的合法像與逆向還原。
4. 給定觀測歷史的精確集合大小為 `2→1→1→0`。第一步的單份像
   與保留下來的單份原點，以原點／當前點配對獨立反向重播吻合。
   第二次同動作只撤銷置換，不能撤銷中途觀測；第三步要求另一分支
   觀測恰空。此處不曾用不同完整染色供不同監視格的見證。
5. 程式分開保留「補回整個觀測 fibre」「只做 mask 不搬運」「非法
   action 當 self-loop」「漏原 R 鄰點」「假設 cap 與核心 Kempe交換」
   的反例資料。所選歷史集合亦以字面全域換色數 `2/0` 對照同一整圖
   `3/3`，正確顯示不能把選定歷史的計數向量直接代入整個來源的
   全域 S4／完整 orbit 守恆方程。

此明列 local disk 不含原 C5 外框 `(x,y,a,b,c)`、941支持與全域壞源
最小性等完整來源條件。證書的 `real_J1_source_realized=false`、
`source_excluded=false` 與 `smaller_bad=false` 均必須保留。本次審查
沒有把它升為 full J1 來源反例、一般 fibre 界或 J1 排除。
