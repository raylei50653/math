# C8-TERMINAL-S1：原 C6 介面的完整 exterior 轉移與任意大小排除

本節的有限物件只有**原圖已固定的外側 P**。剩餘原 C6 disk L 的嚴格內點
數、邊數及色關係皆不枚舉、不設上限；亦不把 L 換成六私人點 cap。
精確來源契約及八份 U 的 custody 見父目錄。這裡的排除實際只需其中的
原 collar、Σ=933／941、原 terminal 分類及零單接端恰為 W5；不依賴 U 的
額外細化、無弦假設、L boundary degree≥4 或新外部定理。

## 1. 一次固定原圖名字、rotation 與原邊

沿既有原 clockwise `C=(c0,…,c7)`，令正對 pair 為
`{c_i,c_(i+4)}`，`i=0,1,2,3`。原八條 C 邊的第三點仍為 `t0,…,t7`。
PINCH 兩端使用同一原點 x；BRIDGE 左右原端點分別 x、y，保留原邊 xy
及其兩側原面 `(c_i,x,y)`、`(c_(i+4),y,x)`。

`side=0/1` 指任意大小端的 clockwise 半弧起點分別為 `i`、`i+4`。
此端原 endpoint 記 e，四個 t 按此半弧的原次序記 `v0,v1,v2,v3`。
唯一單接原點 w 位於五個原 rotation slots 之一：

- slot 0：e 與 v0 之間，w 的原 C contact 是半弧起點；
- slot 1、2、3：相鄰兩個 v 之間，contact 是共同原 C 點；
- slot 4：v3 與 e 之間，contact 是半弧終點。

故 D 由 `(e,v0,v1,v2,v3)` 在指定 slot 插入 w，得到原具名六環。
此順序是一次固定的原邊界順序，對十個 B 列及所有 literal 色指派不變。

另一半弧只有零單接 terminal，既有 T0 使其精確為原 W5，中心命名 zF。
P 包含全部原 B–C collar、兩半弧到 Q 的所有原面、固定原 W5、原橋邊
（若有）以及原 D 六條邊。P 的內部孔正是 D；L 包含 D 及其內側全部
原點、弦及原邊。兩者交集恰為原 D，邊交集是 D 的六條原邊。任何 D
內弦均屬 L，所以本轉移本身允許 L 有弦。

checker 以原有向三角面重建 P，並暫加一個只供 embedding 驗證的 fan
中心，呼叫凍結 `assemble` 驗證全部 dart、vertex link、Euler 及 rotation；
移去 dummy 後保存 P 的原邊 cyclic order。dummy 的色關係從未參與轉移。

八份 literal collar × 4 正對 pair × 2 variable sides × 5 slots × 2 kinds
共 **640 份**。重複 e 的 933／941 來源仍各有原 query id 與完整十列。

## 2. 原 full-fibre 等式

色集合固定為 A={0,1,2,3}。對原 B 十列之一 β 及全部 4096 份
`γ∈A^D`，令 F_P(β,γ) 是 P 每個原頂點的完整 proper 色指派；不丟失
不 proper 或 proper 但為空的 γ。令 F_L(γ) 是任意原 L 的全部原頂點
色指派。則在同一原圖、同一 literal 色框下有雙射

\[
\mathcal F_G(\beta)=
\bigsqcup_{\gamma\in A^D}
\mathcal F_P(\beta,\gamma)\Join_D\mathcal F_L(\gamma).
\tag{1}
\]

右側的 join 要求六個原 D 點逐點色值相同。PINCH 的 x 從建圖起只有
一個變數；BRIDGE 的 xy 是 P 原邊，故任何 P lift 均滿足 x≠y。將兩側
各自可行的 marginal 色集合相乘不能得到式(1)。

固定 W5 不重新發現：checker 讀取父包凍結 `full_lifts.v2.json.gz` 的
全部 4096 literal J fibres 及 744 完整 U lifts。在每份 P 的每個 β，
使用原 complement skeleton 染色後接回該 J 的每份原 U lift；結果與
直接搜尋 P 全部原頂點的 MRV 染色**逐份全字串相等**。因此保存的不只是
support 或 fibre 大小，而是能重建原 P 每個頂點的完整指派。

`full_lifts.jsonl.gz` 逐份保存640份 P，每份有完整 vertex_order、D_order、
4096 literal D 指派字串及十列 ×4096 個明確 lists。每個非空 list
保存完整 P 色字串；空 lists 亦明確存在。總計 **26,214,400 個 B–D
fibres**，其中 improper γ 自動為空。

## 3. 從完整 literal 轉移得出的來源排除判準

D 的 proper literal 指派有31個全域 S4 軌道。這裡只在完整 literal
轉移完成後為證明歸類，從未獨立正規化 P 與 L，也未改變原 D 點序。
對軌道 q 定義

\[
M_P(q)=\{i:\exists\gamma\in q,
\mathcal F_P(\beta_i,\gamma)\ne\varnothing\}.
\tag{2}
\]

任意**同一原 L** 的 proper 色關係在全域色置換下不變。因此某個 q
若有一份 γ 可延伸於 L，則 q 的每份 literal γ 都可延伸；將該 L
完整色指派全域置換即可。每一次 join 仍使用 P 和 L 的同一份 γ。
令 K_L 是這些可延伸軌道，式(1)立即给出

\[
\Sigma_G=\bigcup_{q\in K_L} M_P(q).
\tag{3}
\]

對原 target S=933 或941，任何含 forbidden B row 的 M_P(q) 都不可能
由 L 接受。故若 Σ_G=S，必要地

\[
K_L\subseteq A_P(S):=\{q:M_P(q)\subseteq S\},\qquad
S\subseteq R_P(S):=\bigcup_{q\in A_P(S)}M_P(q).
\tag{4}
\]

而 R_P(S) 本來已是 S 的子集。所以只須在固定 P 證明
`R_P(S)≠S`，便對任意 L 得到矛盾。此推理甚至允許每個 S4-invariant
抽象 L relation，故不會偷偷以有限 cap 可實現性代替原來源可實現性。

## 4. 全部640份的實際新矛盾

`certificate.json.gz` 保存每份 P 的31個完整 M_P(q)、A_P(S)、R_P(S)、
非零 `missing_target_mask`，並指定一個缺失但原 target 必須接受的
`chosen_missing_B_row`。對每個能延伸這個正列的 q，證書再指定一個
實際也能延伸的 forbidden B row，構成逐軌道可查的 implication witness。

獨立重播所得：

| 原類型 | target | 原具名 exterior 數 | R_P(S)=S 的份數 |
| --- | ---: | ---: | ---: |
| PINCH | 933 | 80 | 0 |
| PINCH | 941 | 240 | 0 |
| BRIDGE | 933 | 80 | 0 |
| BRIDGE | 941 | 240 | 0 |

例如 `PINCH-0-0-0-c15-933` 的 A_P(933) 已空，R=0。
其餘情形亦全部缺失至少一個 target 正列。最接近者可能 R=933、S=941，
仍確實缺失 `β3=01201`；或 R=940、S=941，缺失 `β0=01012`。
完整證書逐個原位置列出結果，沒有用旋轉後的不同來源代替它。

因此任意大小剩餘原 C6 L 均不能令640份 P之一回到原 target：

\[
\boxed{h=3,\quad p\in\{1,2\},\quad s=1\quad\text{不可能}.}
\tag{5}
\]

接既有 s=0 排除，得本輪待證目標

\[
\boxed{h=3,\ p>0\ \Longrightarrow\ s\ge2.}
\tag{6}
\]

新使用的原圖資訊是：單接點在原半弧中的**五個完整 rotation slots**、
零單接另一端的**原 W5 全部 lifts**、其與**整份原 B–C collar**的同色框
完整轉移，以及原 B 十列的**指定正列與指定禁列同時成立**。單純重寫
separator 等式或檢查 C8 gadget 的各個可行 marginal 都得不到式(4)的
固定 P orbit implication 矛盾。關於 L 本身的度数、弦及合法識別限制
可見 theory，但本排除已對更大的所有 S4-invariant L relations 成立。

## 5. 校準、重播與信任界線

slot0/4 的 endpoint-ear `W5+triangle` 共256份完整圖控制另以直接整圖
染色與 P-D join 比較全部 full lifts，256份皆得到 Σ=1023。這些控制
只作校準，式(5)的任意大小結論來自式(1)–(4)，不從這些有限圖外推。

此外 `../review/independent_transfer.py` 使用獨立原邊建構、獨立 CSP，
不 import 本 checker 或舊 terminal kernel，逐份核對全部640份的31
orbit masks 及十列 full P lift 數；總共有 **2,515,696** 份 P full lifts。

```bash
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/transfer/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-terminal-s1-d521163/transfer/check.py --check --negative
```

`--write` 只供首次 exclusive generation；證書或 archive 已存在即拒絕。
`--check` 全程只讀。八項負控制在記憶體中檢查刪 literal empty entry、丟失
full lift、偽造非空 fibre、同一 PINCH endpoint 分裂、忽略 BRIDGE 原邊、
獨立重排 D 名字及舊 kernel 的真空列／漏 lift。損壞的完整 archive
payload 交給正常重播同一個 `compare_payload` 驗證器，並要求其確實拒絕。

這是紙面原圖分類加可重播完整有限 exterior 計算，尚非 Lean 證明。
未擴到 s=2、一般 RING、更大 cap 搜尋，亦未主張一般 no4ct 來源閉合。
`prototype.py`、`explore.py`、`exploration.json` 只記錄初始探索；權威是
凍結輸入、最終 check.py、certificate.json.gz 及完整 archive。

最終 certificate 以 deterministic gzip 保存原 JSON 的完全相同 bytes；
`STORAGE.json` 記錄解壓前後 SHA-256。`final-normal.status.json` 及
`final-seed17.status.json` 記錄最終 checker 的 hash、確切命令及退出碼。
