# W5-RANK2 最終獨立證明審閱

BASE：`243a125a80e4d8de40957f59d8da0bdbc974cf69`。
核讀本包 `SOURCE_REVIEW.md`、`structure/TOPOLOGY.md`、`structure/STRUCTURE.md`、
`structure/REPRESENTATIVE.md`、主／獨立 checker、四份代表及兩套完整執行紀錄。審閱者另實跑主 checker 的
`--check`，974 份逐 byte 完整核對通過；局部 C6 控制另從頭生成及重算。

**判定：PASS，保留明列上游信任邊界。** 四大私人 rank-two 類型均已覆蓋並排除；
theta 的唯一剩餘 domain 由紙面完整化約、974 個必要模板、獨立完整染色及四個
實際較小代表排除。因此可對任取合法全內部 induced W5 採納
`rho(G[P])≥3`。這不是無界有限搜尋外推，也不是新增 Lean theorem。

## 1. 來源與四型分類

來源在全部目錄外 disk-C5 圖中全域最小內點、再最大邊數；其完整前提由已凍結
上游取得。本輪只用 r≥7、原 annular 三角面、B/U 十 pins 互異且各 induced C5、
完整內點 degree≥5、B/U 附件界與短環來源定理。没有加入 N2、ε、edge-critical、
Gallai 或私人 degree≥5；也沒有先假設 F 連通。

連通分量圈秩相加為二，故有環分量分配恰為 1+1 或 2。2-core 的
`Σ(deg−2)=2` 使連通雙環只有一個四度分支點，或兩個三度分支點。抑制 degree
二路徑後的 loop／parallel-edge degree 方程精確給 figure-eight、theta、barbell。
抑制只是分類，不是代表操作；原簡單性、所有 subdivisions、附樹及獨立樹分量
均保留。圖示直覺並未代替覆蓋證明。

F 有恰兩個 bounded faces。任一不含 U 的 bounded F face 沒有任何 G 內部點邊，
因此必為原 PPP 三角面。這個說法使用的是**完整嵌入 F 的實際補集面**，所以
不會忘掉巢狀的另一分量或帶 bridge 的重複 boundary walk。此空面引理一次處理
全部環相對位置：含 essential cycle 時 h=1，全部 contractible 時 h=2。

## 2. 新原面式與任意大小排除

獨立重算與主證明一致：

```
e(F)=r−c+2;
M=2(c−2+h),   p=a+c−2+h;
Σ d_G(P)=4r+12−c−p;
r≤12−c−p=14−2c−a−h.
```

所以任意大小先有 r≤11；all-contractible 域再有 r≤10。使用的是完整 G 度數，
沒有機械移植森林 h=0 或圈秩一常數。

Essential 域有 p=0、h=1，迫 c=1、a=M=0。Leaf 的原 link 必給 M 面，所以
F 沒有附枝、即其 2-core。唯一 PPP 三角面三頂點中至少一個 private degree 二，
其全部 terminal link 在三角面的外側，完整 degree≥5 迫 B/U 切換而給 M，矛盾。
因此四型的所有 essential 位置皆已純紙面排除。

All-contractible 域兩個 bounded faces 都是三角面，h=2、M=2c。分離雙單環、
figure-eight、barbell 的非分支三角根，按「自己或附樹 leaf」分別給六、四、四份
不同 M 見證，加上其他樹分量各兩份，皆超出 2c。Theta 兩個三角面迫三條原路徑
長度 1,2,2；原簡單性排除 2,1,1。因此唯一未在此步排除的 core 是 diamond。

## 3. Diamond 原 rotation 覆蓋是有限核心的關鍵

兩 tips／其附枝末葉及其餘樹分量恰用盡 M=2c。故 branchpoints 無附樹、tip
附樹只能為一條路徑、其他分量也只能為路徑；中間私人點沒有 M。原外 contour
在兩個指定末端間的兩條路，各經不同的 diamond branchpoint，因而一側全接 B，
另一側全接 U。兩 branchpoints 各恰接其側兩個相鄰 pins，完整 degree 五。
這也可由 `SOURCE_REVIEW.md` 的同邊界 crosscut 論證獨立得到。

`p=a+c≥1` 個 B-U 原邊切開 annulus。允許共端點，也允許 p=1 時同一原邊
的兩個 sides。每個切開 region 至多由兩個 bounding cross-edge sides 供應 M；
而每個私人分量恰需兩份。因此一 region 不能藏兩個私人分量；沒有私人點的
region 只可能為一個 terminal triangle。這覆蓋 c=2 的額外路徑、所有 a 個
terminal-only faces，不能省成只有一條私人 backbone 的情形。

其後每側 terminal fan 有一或兩個相鄰 pins，故只前進零或一步；所有原 B/U
環邊各使用一次，兩個總前進量均為五。Diamond gap 額外消耗兩側各一步，
並保留共享的原邊 qBqU。各類點允許的 letters 恰由其完整 degree 推得。
主程式與紙面參數一致，獨立程式以另一順序、四字母產品、region 產品重建同一
974-key 集合。沒有依同構去重、猜測上限或抽象 support 省略模板。

原來源到模板是整個帶嵌入圖的具名同構；B/U 可各移起點，但方向同步。
附件、private edges、cross edges 及所有 faces 均被重建，沒有未計原邊。
此同構保全部 full lifts；它與後面的保 Σ 縮減是兩種不同操作。

## 4. 兩套完整染色與實際代表

主程式從有向 faces 構邊、用 MRV DFS；獨立程式不 import 主程式，從鄰點
intervals 構邊，再用固定變數次序直接枚舉完整 A 與補中心 G。獨立程式由 rotation
逐 dart 走回 faces，核對原 B 外面、U 空面、vertex links、Euler 與連通。
兩套均保全部十個外框代表、每列全部 1024 個 U cells、所有空 fibres 及完整 lifts。
同一私人指派在整圖 DFS 中共同使用，沒有兩側 marginal 的錯誤接合。

完整結果一致：974 模板、9,973,760 cells、9,762,297 空 cells、344,416 份
A lifts、167,814 份 G lifts。Σ 分佈為 970 個 1023、2 個 639、1 個 959、
1 個 1021；**不是全部全收十列**。
主 mathematical SHA256 為
`daf4b2524be46c2615202ddc42430eb11be7d0329bfd3aa4c529a6be0fb0c326`。

四個 mask 均有指定同槽位的實際 plane 代表：1023 使用 r′=0 prism；639、959、
1021 各使用 r′=4 的 diamond annulus。三個 r′=4 圖的參數分別為
`(BU,BBBUUU)`、`(BD,BUUBU)`、`(UU,BBUBBU)`，gap 均為零、沒有額外 path。
這只是參數簡記；正式證書保存每圖的 literal edges、faces、rotation、pin map，
全部 40,960 cells、40,028 空格、1,059 A lifts 與 551 G lifts。
獨立 checker 已逐圖重建全部這些資料及直接 G 染色，結果 PASS。

對每個來源模板、每個 beta，證書保存 source 與對應代表的完整 G fibre selectors；
拒絕列明記空，接受列兩側都非空。把任何輸入 lift 送到同 beta 的目標 selector，
即得兩向 total 函數，逐 literal B pin 保色。共同 S4 搬運涵蓋 240 個 proper
literal beta；原 B 的 improper rows 兩側均拒絕。

這只證
`pr_B R_A³=pr_B R_A′³`，不保各 U pin 色、中心色或 fibre 重數。
正式 strength counterexample 有同 Σ 而不同 R³ 的實際 source／prism cell，
獨立 checker 亦核對其原 full lift 及目標空格，沒有把較弱保存升格。

`review/primary-verification.json` 的主 normal／seed17 及代表 normal／seed17
全部通過，對應輸出 SHA256 各自一致。`controls/negative/summary.json` 及八份
traceback 另核對四種破損：只反 U 面、漏原 diamond 邊、改具名 U pin map、
同時漏一份 A 及 G full lift，均被主／獨立 checker 各拒絕一次。
獨立拒絕點分別為指定 U 面、原邊比較、ownership pin map、完整 A fibres；
主拒絕點均為第一張原記錄的完整重算不一致，沒有用縮短檔案後的 EOF 假裝
測到破損。這些為 `triggered and holds` 的防錯控制。

## 5. 嚴格縮減與採納

全部原模板 r≥7，代表 r′為零或四，所以補中心後
`k′=6+r′<6+r=k`。974 次縮減量的完整分佈為：4 次減三、314 次減七、
350 次減八、236 次減九、70 次減十。按同一 canonical-to-original pin map
搬回，代表仍是同原外框的合法 disk 圖，完整 Σ 相同；這已直接違反來源的
全域最小內點性，不需要代表保持來源 degree／三角化或再查 mask∈K。

因此 theta 殘留也排除。接既有私人森林與單環排除，得到對任意合法全內部 W5
皆有 `rho(G[P])≥3`。本輪 rho=2 域沒有尚待普遍化的結構分支。
最小未控制的新域是 rho≥3 私人核心；一般保 Σ 嚴格代表、一般 R³ 代表及
K∞=K≤5 仍未證。真正最小 933／941 來源仍是 **not triggered**；來源排除來自
紙面完備化約與完整 finite kernel，不来自零觸發。

## 6. 另有窄域局部 no-go，不能誤作一般障礙

`local_patch.py/json` 從頭列出 diamond 雙五度中心 cap 的完整 C6 關係：
732 個 proper rows、300 接受、432 空 fibres、312 lifts。九條可能 boundary
chords 各有原接受列的同色反例，因此同關係的一內點代表不能有 chord；
其餘只剩 64 個單點鄰集，每個都有完整關係不等的見證。
這完備排除保**完整 C6 介面**的二內點到至多一內點局部縮減。
它與已成功的只保外框 Σ、改整個 annulus 的代表相容，不限制本輪採納。

本審閱不替代上游外部定理或 Lean 形式化；本輪採納只在本地隔離 audit，沒有
修改 shared docs、舊證據，也沒有 commit、push、PR、Issue 或外部留言。
執行命令與破損證書防錯紀錄由本包驗證檔另外保留。
