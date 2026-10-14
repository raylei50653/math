# 獨立來源審閱、分類與發佈邊界

2026-10-14，審閱者 source_ledger。工作樹與 BASE 見 [INPUTS](../INPUTS.json)。
只寫本 classification 目錄，未修改原證明、舊證書、共享 docs 或 Git refs。

## 1. 原 ell-r 非邊：可採納，但是已知幾何的推論

假設 p=5，原 link 是 `(a,b,q,ell,m)`。ell 是原內點，且由 pr、ps 非邊
及前輪 p=5⇒a≥5（故 pt 非邊）知 ell 不等於 r,s,t；亦不等於 p,q
或原框點。若原 ellr 是邊，`C=(y,a,p,ell,r)` 是 simple proper 原 C5。

C 含原外框邊 ya；原 y 的內側順序是 a,t,r,x。因此在 y 處，原 yt 邊
位於 C 的有界側，t 不是 C 的頂點。由
[小 cap 定理 §3](../../2026-10-13-c5-no4ct-frontier-6943561/w5/PROOF.md)，
proper 原 C5 的 bounded interior 只能空或恰一個 W5 中心；此處必為 t。
於是 d_G(t)=5 且它接 C 的全部五點，特別有 tp、tell。
tp 已與 p=5⇒a≥5 矛盾。也可不用前輪共同 fibre：tp⇒a=4，而既有
a=4⇒t≥6 又與 d_G(t)=5 矛盾。

所以 ellr 非邊確為任意大小來源結論；本輪首次明列這條原非邊是合理的，
但它沒有獨立擴大舊排除範圍。證明使用的是原 G proper C5 的 bounded-side
定理，沒有誤用識別後圖中可能有例外的五環，也沒有把球面「某側≤1」
直接當成指定側≤1。上述原 cap 定理已供應正確的有界側量詞。

## 2. 共同三點識別的新來源排除

本輪主結果 `p=5⇒a≥6`，及反射 `q=5⇒c≥6`，獨立紙面審閱通過。

沿前輪 `p=5⇒a≥5`，D=`T0−{x,y,p}` 有 k 點。保留的真實兩面是
`Q=(z,s,r,t)` 與 `P=(z,q,ell,m)`，只共享 z；原 alias m=t 已排。
zr 非邊來自 Q induced；zell 非邊來自四連通 T0 中 p 的 induced 四鄰環；
ellr 非邊由 §1。於是 `{z,r,ell}` 是原獨立三點類。

在 Q 的開面內畫 zr 弧，在 P 的開面內畫 zell 弧。兩弧只有共同端點 z，
在 z 處進入不同原面 sectors，構成嵌入平面樹；共享端點不造成交叉。
收縮這兩條弧得到同一 loopless planar quotient J，抑制平行邊不影響
四色染色。J 有 k−2 點，且 zs 的像仍是一條邊。在其一條邊的面側貼
三個新點的四邊路徑，選空 C5 側為外面，得到 k+1 總點、k−4 內點的
合法比較 disk。原全域最小性、K132 無空關係給 J 的完整四色染色。
此處沒有引用一般四色定理，且沒有分別選兩張商圖的 witnesses。

回拉得同一 D 完整染色，`z=r=ell=A`。p 鄰點只用 A、q、m 三種色，
故至少一個 p lift 存在。每個合法 p lift 都屬同一 R；R 的 ABAC fibre
空，迫 s=t=B。R 的全部 ABAB lifts 又要求 pq 恰用其餘兩色 C,D。
共同命名 q=C；如果 m≠B，p=B 便是合法 lift，矛盾，故 m=B。
此時 p 唯一可取 D。因此有非空完整 fibre

`(z,s,r,t,q,ell,m)=ABABCAB`。

每個此商圖的完整染色都受同一推導約束；S4 的共同換色給24個標號版本。
它不指定 fibre 基數，也不宣稱整個 D 關係已知。t,m 與 s,m 各是互異
原點、其原邊若存在必保留在 D，故 tm、sm 均非原邊。

若 a=5，原 a 在 ya／ab 間的完整內側鄰序必為 t,m,p：p 的原面 amp
已固定 m 的位置，而 t 是 ya 的原 apex。因此原鄰序是
`(y,t,m,p,b)`，內面三角化迫 tm 是原邊，與新共同 fibre 矛盾。
配前輪 a=4 排除，得到 p=5⇒a≥6。只需 a=5⇒tm 這個方向；若要用
tm⇔a=5，應明列 p=5、a≥5、m≠t 與原三角面性，而不可對任意接點表宣稱。

反射必搬運整份原 G、兩個原面與全部完整色框；它將 p,a 一起換到 q,c，
無額外 singleton 假設，故932／933／941兩側皆適用。

## 3. 較弱候選的關係

原 `p=5,a=5,m=5` 候選本身正確：刪四點 x,y,p,m 後兩面是 Q 與
`(z,q,ell,v,t)`，共邊 zt。v=q 被 qm 非邊排；v=r 被
`N_R(z)∩N_R(r)={s,t}` 排；v=s 會使 zms 為非面三角形，因 z 的原
cyclic order 含 x,y,t,m,p,q,…,s，m,s 不連續；其他 aliases 由 simple link 排。
三點識別後 cap 內點是 k−5。回拉的全部 p,m lifts 確產生矛盾。

原 `p=5,a=5,t=5` 候選亦正確：刪 t,p 暴露 `(z,s,r,w,m)` 與
`(z,q,ell,m)`，共原邊 zm；共同識別 z=r=ell 後可選一份合法 t 色 B，
再由 ABAB 的全部 p lifts 迫 pq 避 B，但 q、m 都避 B 時 p=B 又合法。

兩者現均由 §2 的整個 `p=5,a=5` 排除涵蓋，應保留探索紀錄而不重複算
三個獨立成果。一般 p=5,a≥6、反射側、r=6 的319及r≥7仍 OPEN。

### 六度 collar 新非邊

[r6 原幾何證明](../r6/PROOF.md)亦經獨立審閱通過。對原 a 的任一內鄰點
j≠t，原接觸限制與 `N_R(z)∩N_R(r)={s,t}` 保證 j≠r,s,v,w，故所用
兩個 proper C5 都是 simple 原環。若 jv 是邊，C=(r,y,a,j,v) 沿 ya 的
有界側含 t；原 tw 邊兩端均不在 C，不能穿過 C，故 w 同在其有界側。
至少兩點違反 proper-C5 cap。若 jw 是邊，C=(r,y,a,j,w) 的有界側含 t，
cap 迫其唯一中心 t 五度，違反已採納的 r=6⇒t≥6。反射端完整同理。

這是原圖幾何排除，不依賴新有限計數。j=p、q 所得四非邊已有舊證明；
本輪新增的量詞涵蓋其餘 a/c 原鄰點。p5 的 m 是其中之一，因此 mv、mw
非邊確是新明列的原來源子支排除。ell 不是原 a/c 鄰點；不能把此結論
搬成 ellv、ellw 非邊。mask319 與兩個低p/q交集仍 OPEN。

## 4. 分類核對與有限獨立控制

[SOURCE_TABLE](SOURCE_TABLE.md)逐一保留原 mask、h、p/q、r 的量詞。
G28 對固定三點四度來源沒有額外 h 前提；h=3及932,h=4只是已知的
高 p/q 子域。`k=h+6+Σ(d−5)` 是原 Euler 式的等價變形，LL 的 ell
是另個不同原內點，其 degree≥6 已知；由此所得高h budget不依賴模型實現。

[check_common_fibre.py](check_common_fibre.py)從兩個原面和原 x,y,p 全部
接回邊直接枚舉，不匯入研究 agent 的 checker。它遍歷4^7個標號七接點
指派、每列4^3種接回，保留商圖 slice 的全部合法 lifts 與空格。
比較「每份完整 T0 lift 的 xy/pq palette 相同」和 R 的 ABAC空／ABAB
palette 的原條件，並獨立核對唯一保留軌道恰 ABABCAB、tm/sm添邊後無列。
此控制只驗證局部色算術；§§1–2 的原面、平面性與 source minimality
仍是紙面證明。正常、seed17與損壞證書檢查結果見本目錄 receipts.json。

## 5. 一般主線、Lean 與證據 custody

一般 T/T0 的指定染色存在性及合法嚴格下降仍 OPEN，詳見來源表§5。
沒有新增 Lean theorem。本輪穩定的可形式化核心是單一 quotient 與原圖
等式完整 fibre 雙射、固定底圖的全部 lifts、整圖換色及合法分量交換；
兩面同嵌入與小 cap 可染性的條件應單列，不從有限表或 `lake build` 推得。

前輪 cofacial 整包及本輪 frozen INPUTS 應逐 SHA256 保持原樣。
尤其舊 r6 integer-count 證書是三組舊必要方程的可行性，新的來源排除不
否定或改寫它。whole-tree DocGraph 歷史70筆 duplicate-ID必保留，
正式 docs 零錯與 whole-tree FAIL 要分別報告。

相接提交白名單建議：前輪 cofacial audit、本輪 lowpq audit、C4父入口、
Kempe導覽、STATUS、no4ct handoff、synthesis 對應列及一份發布紀錄。
README／HANDOFF 路由若無改動只記 reviewed unchanged。等待所有承諾的
研究輸出與獨立審閱後才整合、封存 manifest、stage、commit、push。
研究 checkers只讀重播；普通與seed17、negative controls、input/manifest SHA、
文件、正式及全樹DocGraph、generated-artifact policy、whitespace分別存證。
發布者依既有工作流程跑 lake build，其PASS只證當前既有Lean建置。
push後以即時Git確認 HEAD=origin/main=remote main 及乾淨狀態；本審閱未執行發布。
