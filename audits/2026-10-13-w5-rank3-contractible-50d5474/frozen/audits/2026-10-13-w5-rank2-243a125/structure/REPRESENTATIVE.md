# 四個實際 annulus 代表與完整 Σ 的嚴格縮減

BASE：`243a125a80e4d8de40957f59d8da0bdbc974cf69`。
來源到 974 個必要模板的任意大小、原旋轉完備化約見
[STRUCTURE.md](STRUCTURE.md)。本檔交付模板到較小合法圖的第二步。

**保存目標只有完整外框 Σ，即 `pr_B R_A³`。** 代表保留 B/U 的十個頂點名稱、
原環次序及 U 中心槽位；染色搬運保每個 B pin 的 literal 顏色，可以改變
U pins 的顏色及中心色。十個 pin labels 在圖上存在，不等於十個 pin 顏色固定。

## 1. 可直接重播的實體證據

[representatives.json.gz](../controls/representatives.json.gz) 是 gzip 壓縮 JSON，
頂層有 `representatives`（四圖）、`transfers`（974 份雙向 selector）、
`strength_counterexample`、`beta_order`、`tau_order` 及 `summary`。
每個圖完整保存 `vertices, B, U, private, edges, faces, rotation, ownership`，
以及補中心後的 `wheel_edges, wheel_faces, wheel_rotation`。
`ownership` 記錄指定 B 外面、指定 U 空面、中心編號及十 pins 的原 map。
這些是具體 plane 圖資料，不是抽象 support witness。

每圖另有十個 `rows`；每列保存全部 1,024 個具名 U 色 tuple 的完整 A fibres，
包括空格，以及補中心後全部 G lifts。四圖合計 40,960 cells、40,028 空格、
1,059 份 A lifts、551 份 G lifts。統計入口是
[representatives-summary.json](../controls/representatives-summary.json)。
來源的全部原邊、rotation 與完整 fibres 位於
[certificate.jsonl.gz](../controls/certificate.jsonl.gz)，以 `source_key` 精確對應。

主重播：

```bash
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/representatives.py --check
```

獨立 checker 不 import 主 `check.py` 或 `representatives.py`；其完整結果及
負控制見父 REPORT 的驗證入口。紙面普遍化約、主完整重算、獨立完整重算及
反控制分層記錄；此檔不把未實現的真正最小來源算成有限觸發。

## 2. 四圖的原邊、嵌入與槽位

共同 pins 編碼為 `b_i=i`、`u_i=5+i`，indices mod 5。
十條 boundary edges 恰為兩個 C5；沒有 B 或 U chords。
以下所有原邊之外不再有其他邊。

### 2.1 Σ=1023 的 prism

私人點數 r′=0；另有五條邊 `b_i u_i`。
完整定向面列表是

\[
(b_0,b_4,b_3,b_2,b_1),\quad
(b_i,b_{i+1},u_{i+1},u_i)\ (i=0,\ldots,4),\quad
(u_0,u_1,u_2,u_3,u_4).
\]

第一個是指定外面，最後是指定空 U 面。原圖 n=10、e=15、f=7，Euler 值二。
每個 dart 恰在一個定向面中，反 dart 亦恰出現一次；每點 link 是單一循環。
因此它是具體簡單 sphere rotation，指定 B 外面後給所需 plane annulus。
在 U 空面補中心編號 10 及五條 `10 u_i`，得 k′=6。
五個 annular 四邊面合法；代表不必承繼來源的原內面三角化或最低 degree。

### 2.2 三個 r′=4 diamond 代表

私人點編號 `x=10,y=11,qB=12,qU=13`，五條私人原邊固定為

\[
xq_B,\ xq_U,\ yq_B,\ yq_U,\ q_Bq_U.
\]

以下表格列完全部私人–terminal 附件；每格是該私人點的 terminal 鄰點集。

| Σ | x | y | qB | qU |
| ---: | --- | --- | --- | --- |
| 639 | b0,b1,u0 | b2,u1,u2 | b1,b2 | u0,u1 |
| 959 | b0,b1,u0 | b2,b3,u1,u2 | b1,b2 | u0,u1 |
| 1021 | b0,u0,u1 | b1,u2,u3 | b0,b1 | u1,u2 |

再加以下完整 B–U 邊集合，以 `(i,j)` 代表 `b_i u_j`：

| Σ | 全部 cross edges |
| ---: | --- |
| 639 | (0,0),(0,2),(0,3),(0,4),(2,2),(3,2),(4,2) |
| 959 | (0,0),(0,4),(3,2),(4,2),(4,3),(4,4) |
| 1021 | (0,0),(0,4),(1,3),(2,3),(3,3),(3,4),(4,4) |

三圖皆 n=14、e=32；指定 B/U 面之外的十八面都是三角面，故 f=20，Euler
值二。完整定向面及每點 rotation 已逐項存入 `representatives` 圖記錄，
從 [STRUCTURE §7](STRUCTURE.md) 的原面規則用下列參數亦可唯一重建：

| Σ | diamond word | gap | 後接 terminal triangles |
| ---: | --- | ---: | --- |
| 639 | BU | 0 | BBBUUU |
| 959 | BD | 0 | BUUBU |
| 1021 | UU | 0 | BBUBBU |

此处 B=(1,0)、U=(0,1)、D=(1,1)；三者的 c=1，path word 空。
兩 PPP 面共同為 `(x,qB,qU)` 與 `(y,qU,qB)`；原邊 qBqU 絕不能省略。
B 外面固定 `(0,4,3,2,1)`，U 空面固定 `(5,6,7,8,9)`。
每個 dart/反 dart、單一 vertex link、連通性及 Euler 均按實際資料核對，
不是僅查「抽象圖 planar」。原 pin map 是 `[0,1,…,9]`。
補中心編號14與五條 `14 u_i`，得 k′=10。

代表的某些 B/U degree 小於來源的來源度數下界，這是允許的：全域內點
最小性比較全部 disk-C5 圖，不要求較小代表本身又是最大邊數來源。

## 3. 全部 Σ 對照與原來源內點嚴格減少

固定 literal 色名 {0,1,2,3}，十列順序為

```
01012 01021 01023 01201 01202 01203 01212 01213 01231 01232
```

Σ 的第 i bit 恰表示第 i 列是否有完整 G 延伸。四圖的完整對照是：

| Σ | 拒絕的完整外框列 | 來源模板數 | 來源 r | 代表 r′ | k→k′ |
| ---: | --- | ---: | --- | ---: | --- |
| 1023 | 無 | 970 | 7,8,9,10 | 0 | 13–16 → 6 |
| 639 | 01213,01231 | 2 | 7 | 4 | 13 → 10 |
| 959 | 01212 | 1 | 7 | 4 | 13 → 10 |
| 1021 | 01021 | 1 | 7 | 4 | 13 → 10 |

Σ=1023 的來源 r 分布為 314、350、236、70（按 r=7,8,9,10）。其餘四份均
是 c=1、r=7，精確 descriptors 如下，便於直接定位原 fibres：

| Σ | 來源 diamond word | gap | after |
| ---: | --- | ---: | --- |
| 639 | UOUUD | 0 | BBB |
| 639 | DUUOU | 3 | BBB |
| 959 | DUOOD | 2 | UBB |
| 1021 | DOOUD | 1 | BBU |

O=(0,0)，所有這四份來源的 path word 空。
974 份 transfer 各保存 `r,r_prime,k,k_prime,delta_k,pin_map,preservation`，
逐份驗證 r′<r 與 k′<k。內點減少量分布為：四份減三點、314 份減七點、
350 份減八點、236 份減九點、70 份減十點。
這是實際严格縮減，不只證明代表落在某個人為搜尋上限。

## 4. 保外框的雙向 total full-lift 搬運

對固定 canonical beta，令 C_G(beta)、C_G′(beta) 為原模板/代表的完整 G
染色集合；每份 lift 包括全部私人點、全部 B/U pins 及中心。
完整重算給出

\[
\mathcal C_G(\beta)\ne\varnothing
\quad\Longleftrightarrow\quad
\mathcal C_{G′}(\beta)\ne\varnothing.
\]

對每個共同接受列，certificate 保存完整
`source_selector=s_beta∈C_G(beta)` 與
`representative_selector=t_beta∈C_G′(beta)`；每個共同拒絕列兩值都是 null。
定義

\[
T_{\beta}(\eta)=t_{\beta}\quad(\eta\in\mathcal C_G(\beta)),
\qquad
S_{\beta}(\eta′)=s_{\beta}\quad(\eta′\in\mathcal C_{G′}(\beta)).
\]

這些是兩向 **total** 函數：接受列的每份輸入都有實際完整目標 lift；拒絕列
的 domain 空。完整證書保留每份輸入 fibre，而非只存選中見證。兩函數保
每個 B pin 的 literal 色，不要求互逆、單射、滿射或保留私人 assignment。
它們可以改變 tau 與中心色。

U 是 induced 奇 C5；任何能補中心的 A 染色在 U 恰用三色，中心取唯一缺色。
故上述對照正好給

\[
\operatorname{pr}_B R_A^3
=\Sigma(G)=\Sigma(G′)
=\operatorname{pr}_B R_{A′}^3.
\]

這裏沒有從兩層各自的 marginal 非空拼出一份 full lift，亦沒有忽略中間
介面的 assignment：每個 selector 是整個 capped 圖的直接完整染色。

## 5. 搬回任意原 pin 名稱與任意 literal 外框色

STRUCTURE 的原圖到模板同構保存完整原 rotation 及全部邊。固定共同方向後，
canonical-to-original pin maps 是

\[
g_B(i)=s_B+\epsilon i,\qquad
g_U(i)=s_U+\epsilon i\pmod5,\qquad\epsilon\in\{1,-1\}.
\]

ε 必共同，起點 sB/sU 可以不同。把代表以這同一 map 放回原 B/U 名稱，中心
置於同一原 U 空槽位；代表私點使用新名。原代表已合法 plane annulus，這個
整體改名保留其 rotation、原環順序、外面及空 U 面，不涉及穿越重接。

任意 literal proper B 色列先沿 gB 搬至 canonical pins，再以同一個 S4
置換化為十列之一。將該置換施於一份完整圖染色的所有頂點，使用 §4 selector
後再整體反置換並搬回原 pins。正反兩向均如此，因而對全部 240 個 literal
proper B tuples 都有保原 B 顏色的 total 對照。U 與私人點不得獨立換色。

若原來源是完整最小目錄外來源，原圖/模板同構再接上述代表，得到完整 Σ
相等且內點數減少的另一個 disk-C5 圖。其 Σ 若仍目錄外，違反內點最小性；
Σ 相等保證這一點。因此本縮減不需要額外查四個 masks 的目錄 membership。

## 6. 相同 Σ 不保 R³ 的實際反控制

`strength_counterexample` 固定以下合法 r=7 模板：

```
c=1, r=7, diamond=BOBBD, gap=0, path="", after=UUU
```

它與 prism 的 Σ 同為1023。取同一具名色框

\[
\beta=(0,1,0,1,2),\qquad\tau=(1,0,1,0,3).
\]

tau proper 且恰用三色。原模板的完整 A cell 是空；prism cell 非空，實際
A lift 是 `0101210103`，補唯一缺色中心2得 G lift `01012101032`。
這是「相同完整 Σ 蘊涵相同 R³」的 **counterexample**，不是未觸發控制。
因此本代表搬運不得描述成保全部十 pin 色或保中心色。

## 7. 採納範圍

四代表的 graph/embedding/fibre 驗證是 `triggered and holds`。
真正最小 933／941 來源是 **not triggered**；本包沒有構造它，也沒有從零
觸發推論排除。來源排除由 STRUCTURE 的任意大小完備化約、974 必要模板的
完整染色重算及本檔逐份嚴格縮減共同成立。

三個非 theta 類型與全部 essential 位置已由紙面排除；theta 的全部殘留由
四代表排除。接上游森林/圈秩一結果，得到任意合法全內部 W5 的私人圈秩
至少三。圈秩≥3 的一般保 Σ 嚴格縮減、一般 R³ 代表及 K∞=K≤5 仍未證。
沒有新增 Lean theorem，也沒有改動封存證據。
