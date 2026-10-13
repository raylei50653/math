# 森林來源與保存強度的獨立完整審核

本檔在 BASE `3097ef5be241b7777451a5ef8a663f3987d6b866` 任務中重新完整閱讀指定來源。
只新增本隔離 review 產物；沒有修改舊 audit、證書、manifest 或 shared docs。

## 審核結論與信任邊界

森林排除可沿用，量詞涵蓋任意合法全內部 induced W5。它不是「有限大小找不到反例」：
原面、原完整 degree 計數先處理任意大小、多分量、分支樹與孤立點，再將全部
必要來源縮到三組參數及 70 個路徑模板。有限 DFS 只核對該完備必要域。

完整讀取：`docs/c5_w5_three_color_support.md`、舊 `forest/REPORT.md`、
`t1/forest_independent.md`、`t1/REPORT.md`、`representatives/REPORT.md`、
`conditional/REPORT.md`，以及另一份 `2026-10-13-w5-three-color-support-19209f4c/REPORT.md`。
另外核對 degree5/saturation/cofacial 正式來源的來源前提，閱讀森林主程式及獨立程式。

1. 私人點在 B 上至多兩個鄰點，若兩個則相鄰；在 U 上同理，但後者必須另由
   occupied C4 排除與原中心 spokes 證明。這條推論在單環分支也有效。
2. 私人森林有 `m=r-c`，annulus Euler 為 `E=3r+20, t=2r+10`，
   `M=2c, p=c+a`，私人完整 degree 總和為 `4r+10-c-p`。
   `degree_G≥5` 迫 `r≤10-2c`，而 `r≥7`。
3. 孤立私人點 degree 至多四，不可能。每個 tree 至少兩個 leaves；leaf 的完整
   degree 迫 B/U 各兩附件，並在原 rotation 提供 M 面。M 恰 `2c`，所以每個
   tree 都恰兩 leaves、全是 path，並且所有非端點沒有 M 面。由 r≥7 得 c=1。
4. 三組參數為 `(r,p,a)=(8,1,0),(7,1,0),(7,2,1)`。兩側 ownership 固定 B/U，
   endpoint steps `(1,1)`，內點 steps `(1,0),(0,1),(1,1)`，每條原環邊只能
   供應唯一 annular 面，排除倒退、重用及跳接。四組多重集排列為 20、30、10、10。
5. 原圖到模板的對應是完整嵌入同構；B/U 可各選起點，但方向反轉必須共同。
   私人路徑次序、所有原 edges/faces/rotations 一起搬運。不是 U 獨立正規化。
6. 森林主 checker 與獨立 checker 的真正分工：主程式用 permutations/faces 構圖，
   獨立程式用三字母 words 過濾、neighbor intervals 構邊，並以 fixed-order DFS
   分別直接枚舉 H、G。兩者逐份比較全部 cells/full lifts，不僅 Sigma。
7. `Sigma=1023` 與 `1023 in K` 依賴完整 132-mask 目錄；上游 `K≤12=K≤5`、
   最小來源正規形、四色定理或外部大枚舉仍是各自既有信任輸入。本次没有重證
   這些上游定理，也没有新增 Lean theorem。

70 模板得到 716800 cells、701956 空 cells、18282 H lifts、9308 G lifts，
全部 70 個 capped Sigma 恰 1023。真正最小 933/941 來源仍是 `not triggered`；
普遍排除由紙面覆蓋證明與有限核心共同成立，不能用零 triggers 代替。

## 保存強度與代表審核

W3 transport 的普遍命題是 `R_A³=R_A′³` 等價於存在保每個 B/U pin、因而保
中心唯一缺色的雙向 total 完整染色對照。可以每個共同 nonempty cell 選任意
完整 lift；不要求可逆、雙射、fibre 數量相等或私人 assignments 可重建。
只保 capped Sigma 的精確條件是 `pr_B R_A³=pr_B R_A′³`，不能宣稱保 U pins。

舊控制中 prism 與 triangulated_00 的 capped Sigma 均 1023，但三色支援為
340 與 20 cells；prism 與 decorated prism 的 R³ 相同，所有非空 fibres 倍增。
兩者都是真實合法 annulus，都是錯誤更強命題的 counterexample。

representatives 的 r=2 equality 圖及任意面插入放大有紙面雙向搬運，但含可移除
低度點／occupied triangle，所以最小來源契約不觸發。其 r≤1 下界也不否定
r=2,...,6 或只保 Sigma。conditional 的五 quotient positive-union no-go 是
同一假定來源上的目錄關係障礙；它的兩份 support 控制是抽象資料，沒有圖實現。
這些結果都不能當成單環來源已有代表的證明。

## 單環可用的獨立推導

以下直接由原圖重新推導，沒有把森林公式原封套用。令 rho(F)=1、c 為含孤立點的
分量數、q 為全私人三角面數、a 為全 terminal 三角面數、M 為 BUP 三角面數、p
為 B-U 邊數。則

```
m = r-c+1
2-private faces = 2m-3q
1-private same-ring faces = 10-a
M = 2(c-1+q)
p = c-1+q+a
sum_{x in P} degree_G(x) = 4r+11-c-p
r <= 11-c-p
```

最後一式用的是原 G 的完整度數，絕非 F 的 degree≥5。

**Contractible 分支排除。** C 的有界內側沒有 B/U。若 C 長 ell、內有 s 點，
其 triangulated disk 完全在 F 中，圈秩為 `2s+ell-2≤1`，迫 ell=3、s=0。
因此 C 是一個全私人三角面，q=1，M=2c。對 C 上每個根 z：若它有附樹，
在該附樹選一個私人 leaf，給至少一個 M 面；若沒有附樹，degree_F(z)=2，
完整 degree≥5 迫至少三個 terminal 鄰點。B/U 各至多兩個，故兩種都有；
三角面佔去 link 的一側，外側 terminal 鏈必有 B/U 相鄰轉換，亦給 M 面。
三個根所收費的私人點各異。其他 c-1 個 tree components 各有至少兩 leaves，
各給不同 M 面。因此 `M≥3+2(c-1)>2c`，矛盾。孤立點早已由 degree 排除。

**Essential 分支的完整結構縮減。** C 分隔 B 與 U，所有不在 C 上的私人點
都只能位於某一側。任何私人 leaf 由完整 degree 迫同時有 B/U 鄰點，其 incident
edges 必跨 C，違反原 embedding。因此沒有葉、沒有其他樹分量、没有附枝；
F 恰為 C，c=1。亦沒有 B-U 邊，所以 p=a=q=M=0，`7≤r≤10`。
兩側分別是原 C-B、C-U 三角化 annulus，沒有遺漏分量或私人附件。

每個 C 點有一或兩個 B 鄰點及一或兩個 U 鄰點，原 rotation 給每側連續 interval。
以各側原環前進邊數記 `(dB,dU)`，則三種 steps 為 `(1,0),(0,1),(1,1)`，
且各側總和均五。故 r 點 cyclic word 中三種字母數為
`(r-5,r-5,10-r)`；r=7,8,9,10。先固定原 cycle 的起點與兩環起點、共同方向，
其全部 rooted words 數為 `210+560+630+252=1652`；重複同構不影响覆蓋。
這是一般大小到有限必要域的紙面完備化約，尚須由主交付給出完整模板/圖關係核對。
本審查本身不宣稱 1652 個 templates 的 Sigma 已算完。

## 實際只讀回歸與 freeze 清單

已執行的命令與 exit codes 見 [regression.json](regression.json)。森林 normal/seed17
兩次各與凍結 certificate 的完整解壓 bytes 相等；獨立 checker 再逐份 H/G DFS。
沒有重跑舊生成式 run_verification.py，避免碰觸舊 logs 或 manifest。

森林證據最小完整 freeze 閉包：

```
audits/2026-10-13-w5-three-support-19209f4c/forest/REPORT.md
audits/2026-10-13-w5-three-support-19209f4c/forest/check.py
audits/2026-10-13-w5-three-support-19209f4c/forest/certificate.json.gz
audits/2026-10-13-w5-three-support-19209f4c/forest/summary.json
audits/2026-10-13-w5-three-support-19209f4c/t1/forest_independent.md
audits/2026-10-13-w5-three-support-19209f4c/t1/forest_independent.py
audits/2026-10-13-w5-three-support-19209f4c/conditional/frozen/cells.json
```

報告前提另 freeze 使用者指定的全部正式來源，及 conditional/INPUTS.json。
若將附加保存強度回歸視為本包證據，還須 freeze 對應 checker、certificate、summary
及其讀取的 frozen dependency；不能只凍結 README 或報告摘要。
