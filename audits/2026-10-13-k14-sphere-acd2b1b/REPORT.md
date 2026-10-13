# 十四內點完整球面覆蓋與 C₈ 的十六內點分支界

2026-10-13。BASE `acd2b1beea6c909edade565a00eeeeac05d2b3a7`。
兩項不同證據層的結論為

\[
\boxed{K_{\le14}=K_{\le5}=K132},\qquad
\boxed{h=3\Longrightarrow k\ge16}.
\]

第一項是紙面完備化約接完整有限 Python 證書；第二項是在既有 C₈ 前提下的
新紙面結構證明。一般目錄外來源至少十五內點。`K≤15=K≤5`、933／941
的任意大小來源、八個 C₈ 無界殘留及一般主命題仍 **OPEN**。
沒有新增 Lean theorem，不提高共同 `h≥3`、`n₅≥9`。

## 1. 精確來源契約與完備覆蓋

固定有序的原外框 B=(b₀,…,b₄)，Σ 是同一圖在十個固定 normalized 外框列的
完整延伸關係。圖類是有限簡單 disk 圖，原來允許外框 chords。
反設存在至多十四內點、Σ∉K132 的圖，在**全部**目錄外來源中先最小化
內點數 k，再最大化邊數，得到 G。這不是固定 mask、固定 h 或 edge-critical
圖的極小化。

沿用 [K13-COLLAR](../../docs/c5_k13_collar.md)，k 恰為十四；沿用
[共面正規形](../../docs/c5_cofacial_normal_form.md)及
[度數定理](../../docs/c5_saturation_degree_bound.md)，G 為簡單二連通、
chordless-C₅ disk、所有內面三角形、B 度數至少四、內部度數至少五。
這些上游結論的完整關係聯集／全域最小性／外部定理依賴全部保留。
未加入 N2、ε=2、Gallai、root incidence、無 C chord 或額外 collar 假設。

在 B 外面的 disk 加一個新點 z，恰接五個 B 點。所得球面三角剖分 T 有
二十點、54 邊、36 個三角面，最小度數至少五，z 度五。
反之，任取二十點簡單球面三角剖分的五度點 z，刪掉其原星形 disk，
保留原 rotation 中五個有序鄰點為 B，就得到十九點／十四內點、49 邊的
disk 圖。此逆向域容許較多來源，包括鄰環有 chord 等情形，**全部保留**。

因此列出全部 T 並取每一個五度點，必覆蓋所有可能的 G。嵌入同構只搬運
整張原圖、root、B、邊、面、rotation 與全部染色；B 的十種起點／方向
共同搬運，沒有對獨立分量另作色彩正規化。每份 graph 計算完整十列，
包含空 fibre；若全部 Σ∈K132，即與 G 的選擇矛盾。
結合既有每個 K132 關係的五內點 witness，得到上述等式。

## 2. 球面生成的責任與實際結果

使用 BASE 內的 plantri 5.8 C 原始碼，完整執行 `-m5 20`。生成完備性的
外部數學依賴是 Brinkmann–McKay 的 minimum-five construction 及 canonical
construction path；不是由圖數吻合推出完備性。來源及版本另核對
[作者官方頁面](https://users.cecs.anu.edu.au/~bdm/plantri/)，
[minimum-five 原論文](https://users.cecs.anu.edu.au/~bdm/plantri/min5paper_sc.pdf)及
[生成論文 expanded version](https://users.cecs.anu.edu.au/~bdm/papers/plantri-full.pdf)。
前輪的完整引入說明已按 BASE 凍結於 `frozen/`，其 theorem／implementation
信任沒有升級為 Lean 或 formally verified generator。

第二路從 `-m4 20` 的全部 **64,719,885** 份输出候選中，只在 output callback
檢查最小度五，生成 recursion 不加剪枝。兩路各得 **73** 份，使用逐 dart、
兩個整圖方向的嵌入 canonical form 核對逐類相等，亦核對各自無重複。
它們是不同生成入口，但共享 plantri 的部分實作，不稱完全獨立生成器。
本輪又從凍結原始碼重編譯／重播，兩份 planar_code 各與保存 bytes 完全一致。

| 核對項 | 數量／結果 |
|---|---:|
| 二十點球面嵌入類 | 73 |
| 全部五度根點刪除圖 | 1,001 |
| literal 外框 rows | 10,010 |
| 完整 G lifts | 180,228 |
| 完整關係 | 1,001 份均為 1023∈K132 |

根圖按 h 的數目為 `0:21,1:85,2:245,3:385,4:240,5:23,6:2`。
它們未必全符合最小來源；沒有在染色前用 h、collar、mask 或 degree profile
篩掉任何根點。也没有用 933／941 的零觸發作排除理由。
來源排除來自 §1 的**完備覆蓋**與逐圖完整關係核對。

## 3. 完整原圖、fibres 與獨立核對

[certificate.json.gz](certificate.json.gz) 每份保存 sphere/root、全體原點到
canonical 座標的 map、所有原邊、rotation、有向面、指定外面、完整度數、
原 B 與十列全部 full lifts，以及十個 D₅ frames 的原點 map／列置換／計數。
所有完整染色都在同一圖上搜尋，不使用 marginals 或分開可行的 masks。
三色列 normalization 的剩餘第四個顏色使用唯一未用色，故 D₅ 搬運為完整
literal 染色的雙射；保留 base full lifts 與 map 可以恢復各 frame。

[主程式](check.py) 使用固定頂點次序 DFS；
[獨立程式](independent/compare.py) 用凍結前輪的另一套 parser、dart traversal
及 domain propagation／MRV 搜尋，從 sphere 的**原 labels**直接計算，最後
才沿同一 map 逐字比對全部 lifts。兩者沒有共用染色或 topology 函式。
獨立核對也重建全部原邊、rotation、faces、root coverage 及 D₅ 關係。

normal／seed17 兩套重播都一致；[負控制](independent/negative.py)針對漏 lift、
偽空 fibre、漏列、漏 root、錯原邊、錯 pin、錯 rotation，共八次 validator
拒絕。負證書只放臨時目錄，原證書未覆寫。另以C5、W5及C5＋原chord02完整小控制核對兩套solver與直接product，
包含五格及三格真正空fibres；它們不觸發目錄外來源前提。
完整 payload SHA256：`01c6ef3c978868479c7a292f5575a803f7e27d4de8275b43084a477bc0d97d7e`。

## 4. C₈ 的紙面加強：h=3 必須 k≥16

完整證明見 [C8_PROOF](independent/C8_PROOF.md)。固定同一原 C₈ 內側 H，
沿用已證的 induced C₈、邊界 H-degree≥4、嚴格內點 degree≥5，令
I=V(H)\C₈、m=|I|、Q=H[I]。既有曲率給 m≥6，k=8+m。

Q 連通，且不能有 degree-one 點：那個點的原循環 link 至少有四個連續 C
鄰點，迫某個 C 點的兩個原面第三點相同，從而 H-degree=3，矛盾。
若全部 C-degree=4，每份 C-I incidence 被唯一原 C-edge 三角面兩兩配對，
所以每個 I 點的 C 鄰點數為偶數。

- m=6：全部 I-degree=5、C-degree=4，Q 有七條邊；六個 Q-degree 都奇數，
  無 leaf 卻迫每個至少三，與總 degree 14 矛盾。
- m=7、I-degree 為 5⁶,6：Q-degree 被迫為 3⁶,2，且每個 Q 點都接 C，
  因此在原 embedding 中 outerplane。但 outerplanar 圖至少兩個 degree≤2
  點，矛盾。
- m=7、I-degree 全五：恰一個 C-degree 五，唯一中間 incidence 是唯一配對
  缺口；六個 Q-degree 奇、一個偶，總和至少20，實際只有18，矛盾。

這是對全部八項 C₈ 契約的大小限制，不表示八項無界來源已被排除。
該證明不依本輪球面生成，反過來球面覆蓋亦不使用 C₈ 加強作剪枝。

## 5. 重播、邊界與交付

從 repo root 執行，以下均不改現有證書：

```bash
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/generation/replay.py
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k14-sphere-acd2b1b/check.py --check
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/compare.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/compare.py
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/negative.py
python3 -B audits/2026-10-13-k14-sphere-acd2b1b/independent/calibration.py
```

[BASE.json](BASE.json) 保存初始 Git 狀態與原輸入 hashes；
[C8_INPUTS.json](C8_INPUTS.json)另凍結 C₈ 紙面依賴。舊證書未改。
首次 output-filter 編譯把已由 C macro stringify 的 plugin 再加引號而失敗；
原失敗 log 保留，改為 `-DPLUGIN=min5_filter.c` 後兩路生成與重播通過。
本輪沒有重播 Dvořák–Lidický 外部計算證書，也沒有擴大其少於三十的原定理。
實際 933／941 最小來源仍為 `not triggered`；有限來源覆蓋為
`triggered and holds`，破損證書為拒絕控制。一般無界來源仍 OPEN。
文件／既有 Lean 回歸及傳播核對另見本輪研究紀錄；無 commit／push。
