# 六接點組交叉審查

審查對象：`../2026-10-15-six-pin-lifts-6ddea32/` 的 PROOF、REPORT、
check.py、完整 certificate 與凍結來源契約。只讀對方檔案。

**結論：在報告明列的量詞及來源範圍內通過，未發現阻斷問題。**
沒有將單一色差對的 cube 完整性升格為不同色差對混合後的全域返回，
也沒有將三張平面控制當成完整原最小來源。

1. 三原邊等價自行重證：同 XOR 的兩個二色集合是同一個二元子群的
   兩個 cosets。同一對時，兩三角形迫 m,z 在另一對，mz 邊迫它們
   互異，故三差相等；互補對時，m,z 在不同 cosets，故 mz 差異於
   前兩差。這證 `E iff d(vw)=d(pq)!=d(mz)`，全部使用同一完整染色。
   獨立枚舉432份 proper 六點列及96份 E，沒有假定列可延拓。
2. 固定一份 E-free 染色與一個色差對時，對所有三標記的實際同環
   partition，獨立枚舉全部 cycle-bit 子集。165份情形與正式表逐列
   相等；有任意子集可返回 E 當且僅當有單一 cycle-bit 可返回。
   「一個 switch 足夠」的量詞限於這個固定 state／pair，紙面寫得準確。
3. 球面雙色對偶環是一個 Jordan cycle；跨環的原邊恰是該環所記錄
   的完整原邊集合。一側加 `a XOR b` 只把跨邊差 a,b 互換，保所有
   原邊 proper，並可原樣拆回 s,t。它不被誤稱為一個普通 vertex
   Kempe component，而是同側兩對色的實際 components 同時交換。
   反向 cut 的每個對偶頂點度0或2，因此確為交替環的聯集；差一個
   全域平移不影響 E。由此得到普通 vertex Kempe 序列的封閉性合理。
4. 對照前輪合法 cofacial construction：J=U/(s=t) 有 k−1 點，
   三點薄 cap 得 k−3 內點，嚴格小於來源 k，足以供應某份完整染色。
   這個論證沒有指定 pq palette。恢復 s,t 增1，恢復 r,x,y,b 增4，
   再拆 a,c 增1，總數回到 k+5；並未得到較小 completed source。
5. 實際控制的完整 J/U 染色已由不同固定頂點序 DFS 獨立重建。
   J數依次240、288、24；E數24、96、0；U數864、960、96。
   全部 r lifts 直接以四色減鄰色再核，空 lift 列依次96、192、0，
   沒有丟棄不能接 r 的 U 染色。正二十面體控制的全部原三角形也
   獨立比對為恰20個原面。

重播記錄在 [CROSS_VERIFICATION.json](CROSS_VERIFICATION.json)，
獨立程式為 [review_six.py](review_six.py)：正式 checker 正常及seed17
皆PASS，獨立抽象／全染色重建PASS。原圖面與 link 的球面驗證採用
正式 checker 直接重建；本交叉審查沒有另寫第二套完整曲面分類程式。

來源界線保持：12點控制拆回的 z,s,t 度數不滿足原來源，逐面插點
控制也有分離三角形。三者都不是 minimum-source realization。
新表是來源必須滿足的必要條件；來源必違反某列、完整319排除、
ω=0、一般主命題及 strict completed-source descent 仍 OPEN。
