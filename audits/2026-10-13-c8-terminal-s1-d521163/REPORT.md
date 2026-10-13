# C8-TERMINAL-S1：單接點 PINCH／BRIDGE 的任意大小來源排除

2026-10-13。BASE `d5211633ba80c2b10cb12eaa8189421e35a31cc3`。
本輪只寫此獨立 audit；既有證書、共享研究入口及其他未提交改動不變。
輸入逐檔凍結於 [INPUTS.json](INPUTS.json)，初始工作區見
[BASE_STATUS.txt](BASE_STATUS.txt)。

## 1. 結論及精確契約

在全域最小原內點數、再最大邊數的 no4ct 目錄外 C5 來源契約下，
全部 `h=3,p∈{1,2},s=1` PINCH／BRIDGE 均被排除，剩餘 C6 的嚴格內點數
沒有上限。與既有 `s=0` 排除合併，得到

\[
\boxed{h=3,\ p>0\ \Longrightarrow\ s\ge2.}
\]

此處只用既有來源契約所給的八份原 collar／target、原接點三型及零單接端
W5 定理。新排除的核心是：這些**固定原圖外側 patch** 都無法把任何
四色置換不變的 C6 關係轉成指定的完整 B 關係。任意大小 C6 是未知的原圖
disk，從未限制它的內點數，也未以固定階數 cap 枚舉代替它。

本報告的最終驗收狀態及執行紀錄見 [VERIFICATION.json](VERIFICATION.json)；
完整原圖論證見 [theory/PROOF.md](theory/PROOF.md)，獨立審查見
[review/PROOF_REVIEW.md](review/PROOF_REVIEW.md)。

## 2. 凍結權威、八份 U 與原色框

原來源 G 的有序外框為 `B=(b0,…,b4)`，`C=(c0,…,c7)` 是同一原 induced C8，
內側為 H；`I=V(H)\C`、`Q=H[I]`。全域最小性涵蓋全部目錄外關係，並非
只對 933 或 941 分別最小化。no4ct 依賴及受限小 cap 的接入沿用凍結的
[C8 geometry](frozen/audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md)。

[AUTHORITY.json](AUTHORITY.json) 由 [authority.py](authority.py) 交叉核對
no4ct finite certificate、最終 Kempe support、原 274 座標、十列 B 順序及
原 collar 的全部邊。當前 U 為以下必要上界；不把 U 當成可實現關係。

| 原查詢 | 完整 target | 當前 U 大小 |
| --- | ---: | ---: |
| c15-933 | 933 | 134 |
| c18-933 | 933 | 134 |
| c04-941 | 941 | 193 |
| c07-941 | 941 | 193 |
| c15-941 | 941 | 171 |
| c18-941 | 941 | 175 |
| c20-941 | 941 | 171 |
| c30-941 | 941 | 175 |

特別是 c15／c20-941 必用最終 171 列；較早 quotient 證書的 173 列不是
當前 U。本輪完整 P→B 轉移已足夠矛盾，無須再對 U 的 274 座標施加計數
鬆弛；上述核對固定來源身份與依賴，並非把舊必要向量當作新來源。

所有 literal 色值為 `0,1,2,3`；原 B 十列固定為

`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`。

## 3. s=1 的完整原圖分類與繼承限制

固定正對 pair `{c_i,c_(i+4)}`，`0≤i<4`，再選單接點所在半弧
`a=i+4ε (mod 8)`，`ε∈{0,1}`。該半弧端點依原 rotation 命名為 e，
四個原面第三點依序是 `t_a,…,t_(a+3)`。唯一單接點 w 位於五個原 link
位置之一，`j=0,…,4`，唯一 C 附件是 `c_(a+j)`。

剩餘介面 D 的固定順序是 `(e,t_a,…,t_(a+3))` 中，在位置 `j+1` 插入 w。
它是原簡單 C6；此時**不假設無弦**。另一端零單接，所以精確是原 W5，
由其 endpoint、另一側四個 t 及一個原中心 zF 組成。

PINCH 兩側共享同一原 x；BRIDGE 左右 endpoints 為 x、y，並保留唯一原
bridge xy 及兩個原三角面。原 C、全部附件、兩側方向與 rotation 全固定，
不逐色列改名。兩型 ×四個 pair ×兩側 ×五位置給 80 份 H 外側骨架，
各接八份原 collar，合計 640 份具名 P。

逐點繼承的度數是：D 上四個 t 的 L-degree 至少三；w 至少四；
distinguished e 初始只保證至少二。L 嚴格內點没有 L 外附件，度數至少五；
所有 L 內面是原三角面。C3／C4 cap 空、C5 cap 空或 W5 的限制使用原內部
介面及嚴格大小，並非把 L 直接當成較小 C5 來源。

本輪另證以下原圖限制，詳細證明在 theory/PROOF.md。

* 若 D 有弦，距離三弦把 L 分成兩個空 C4，違反 terminal 有嚴格內點。
  距離二弦的空三角耳只能是 e；其補側為 occupied C5，故 L 恰為 W5 加 e 耳。
  w 必為 e 的兩個框鄰之一，故只可能 `j=0` 或 `j=4`。
* 若 D 無弦，e 的度數也至少三。單一嚴格內點會迫 W6，使 w 度三，故此時
  L 至少有兩個嚴格內點；這不是本輪設定的內點上限。
* 在無弦 D 中，若一個嚴格內點同接某條長二或三的 D 弧兩端，且 w 嚴格
  位於該弧內，原 C4／C5 cap 會迫 w 的完整 L-degree 恰三，矛盾。

這些結論使用原面的完整 sector、實際 C 附件與 w 的原度數。
最終的轉移矛盾比這些必要限制更強，因此不需要先排弦，也不需要額外的
合法識別或相對可染性命題。

## 4. 全部 literal fibres 的精確轉移

令 P 包含原 B–C collar、固定 W5 端、C 與 D 間全部原面和邊，以及 PINCH
的共享原點或 BRIDGE 的原邊 xy。D 的框邊可同時存於 P 和 L；L 的其他邊，
包括可能的 D 弦，均保留在 L。兩者頂點交集精確為 D，沒有遗漏的跨片邊。

固定 β 與 γ，F_P(β,γ) 保存 P 的全部完整 literal 著色，F_L(γ) 保存 L
的全部完整 literal 著色。按同一原具名 D 同色黏合，有原圖著色的雙射

\[
\boxed{\mathcal F_G(\beta)=
\bigsqcup_{\gamma\in\{0,1,2,3\}^{D}}
\mathcal F_P(\beta,\gamma)\Join_D\mathcal F_L(\gamma).}
\tag{1}
\]

PINCH 的 x 只有一個變數；BRIDGE 的 xy 永遠檢查異色。每個 β 的全部
4096 份 γ 均保留，包含 improper γ 及 proper 空 fibres；每份 P lift
保留全部原點色值。固定端使用凍結的
[terminal full_lifts.v2.json.gz](frozen/audits/2026-10-13-c5-no4ct-frontier-6943561/terminals/full_lifts.v2.json.gz)
及其原 J/U 對應，不重新發現 kernel。

[transfer/check.py](transfer/check.py) 以原面重建 P 的原點、邊、rotation
與孔洞，並對每一原 B 列比較直接完整著色與 skeleton＋literal W5 kernel
的**全部完整 lifts**。輸出包含原圖骨架、十列 ×4096 fibres 及空格，不只
保存投影非空性。

## 5. 從完整转移得到任意大小矛盾

對任一 literal γ，L 全圖的同一全域色置換給出相應 fibre 的雙射。
因此 L 的非空 D fibres 必為完整 S4 色軌道的聯集；proper C6 有 31 個軌道。
這是**完成 literal join 後**的支援診斷，沒有分別重染兩側。

對每份固定 P 及 C6 軌道 q，定義十列 mask

\[
M_P(q)=\{b:\exists\gamma\in q,\quad
                 \mathcal F_P(\beta_b,\gamma)\ne\varnothing\}.
\]

令 R_L 為 L 非空 fibres 的軌道集。(1) 及同一 L 的全域色置換直接給

\[
\Sigma_B(G)=\bigcup_{q\in R_L}M_P(q).                 \tag{2}
\]

固定原 target τ，所有拒絕列必為空，故

\[
R_L\subseteq A_{P,\tau}:=\{q:M_P(q)\subseteq\tau\}.
\]

進而必要有

\[
\tau=\Sigma_B(G)\subseteq
M^*_{P,\tau}:=\bigcup_{q\in A_{P,\tau}}M_P(q)
\subseteq\tau.                                      \tag{3}
\]

完整有限外側核對對全部 640 份 P 都給出

\[
\boxed{\tau\setminus M^*_{P,\tau}\ne\varnothing.}     \tag{4}
\]

證書逐份列出缺失的原接受列，以及所有能到達它的 D 軌道為何也到達某個
原拒絕列。若 L 有該軌道，拒絕列被染出；若 L 沒有全部這些軌道，接受列
無法被染出。矛盾始終在同一原圖、同一色框與完整 fibres 上成立。

這不是枚舉剩餘 L：式(2)甚至允許任意 S4 不變的 D 支援。來源可實現的 L
只是這個更大類別的一部分，所以無界大小、原弦及全部內部形狀同時排除。
新增資訊相對既有 C8 gadget／計數條件，正是原來源 `s=1` 強制的完整
W5 端、單接點的五個實際位置，以及它們與原 collar 的**共同完整轉移**。

## 6. 驗證、可採納範圍與停止點

主證書和完整 fibres 位於 transfer/；独立 checker
[review/independent_transfer.py](review/independent_transfer.py) 使用另一套
原附件／原邊建構與直接著色程式，不呼叫主圖建構或 W5 kernel。
它核對全部 640 份、每份 31 個完整軌道 masks 和原 B 十列計數；合計
2,515,696 份 P lifts（按 640 個查詢計數，重複 collar 依查詢保留）。
此數是有限外側著色數，不是目錄外來源見證數。

全部 640 份目標不可達，其中 498 份的 M* 為空；其餘 142 份仍逐份缺少
至少一個指定接受列。來源排除為紙面原圖完備分類、精確轉移定理及完整
有限外側證書的合併結果，不由零 source triggers 或有限內點枚舉推出。

可採納：本契約內全部 s=1 PINCH／BRIDGE 排除，接上游 s=0 得 s≥2。
再由原 terminal 耳下界，PINCH 必 `m≥13,k≥21`，BRIDGE 必 `m≥14,k≥22`。
這是這兩型的條件界；一般 h=3 的 RING 下界及 h≥4 不因此提高。

本輪不擴到 s=2、一般 RING 或更大 cap 搜尋。八份來源在其他接點型態／
單接點數、h≥4 的三支、一般 `K∞=K≤5` 與 Lean 形式化仍 OPEN。
沒有新增外部定理或 4CT 前提；承繼的有限型錄與生成信任不因此消失。
沒有 commit／push。

完整 archive 明存 26,214,400 個 B–D fibres，其中 25,659,554 個為空。
大型證書採 gzip 保存；[STORAGE.json](STORAGE.json) 記錄凍結輸入的儲存
路徑及解壓前後 SHA256，原 INPUTS.json 的來源位元組承諾不變。
[verify.py](verify.py) 提供只讀 custody／證書整合核對；它不代替下列完整
著色重播。

重播命令及逐項結果以 VERIFICATION.json 為準：

```bash
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/authority.py --check --negative
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/transfer/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-terminal-s1-d521163/transfer/check.py --check --negative
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/review/independent_transfer.py
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/theory/check_structure.py
python3 -B audits/2026-10-13-c8-terminal-s1-d521163/verify.py --check
```
