# W5-RANK2：私人雙環排除與保完整 Σ 的嚴格縮減

2026-10-13。Repository `raylei50653/math`；凍結 BASE
`243a125a80e4d8de40957f59d8da0bdbc974cf69`。
僅本地獨立 audit；未 commit、push、PR、Issue 或外部留言。

**結論：在全部目錄外 disk-C5 圖中先最小化內點、再最大化邊數的完整來源前提下，
任意合法全內部 induced W5 的私人圖均滿足**

\[
\boxed{\rho(G[P])\ge3.}
\]

本輪普遍排除 `ρ=2`，再接 BASE 已證的 `ρ≥2`。三類非 theta 核與所有
essential 位置以任意大小紙面矛盾排除；theta 剩餘域先完整化為 974 個原嵌入
模板，再用四個同槽位 annuli 保持完整 Σ 並嚴格減少內點。
代表只保 `pr_B R_A³`，不宣稱保 `R_A³`。
一般 `ρ≥3` 的來源縮減及 `K∞=K≤5` 仍 OPEN。

## 1. 凍結與精確來源

[BASE.json](BASE.json) 記錄指定 BASE、開始時相同 HEAD、既有無關 C8 audit，
以及 13 份來源的 BASE blob/live bytes 相等與 SHA-256。
`frozen/` 保存其原 bytes；[最終驗證](VERIFICATION.json) 與
[交付清單](DELIVERY.json) 核對凍結、修改範圍與本包產物。
本輪所有寫入只在本 audit，未修改既有 C8 工作、正式 docs、舊 audit、舊
manifests 與封存。結束時共用工作樹另有並行 C8/N2 文件變更；其中 live
`docs/c5_neartri_boundary_collar.md` 已不同於 BASE。13 份 frozen 輸入仍逐 byte
等於 BASE，本輪推導以凍結內容為準；並行修改原樣保留，詳見最終驗證紀錄。

G 的最小性比較域是**全部目錄外 disk-C5 圖**，不是固定 mask、固定私人
圈秩、已三角化圖或已滿足某 degree 條件的子類。
固定原 B=(b0,…,b4)、原中心 v 及循環鄰點 U=(u0,…,u4)，十 pins 互異；
U 誘導 C5，其有界側恰有 v 及五個三角面。
令 A=G−v，P=V(G)\(B∪U∪{v})，r=|P|=k−6，F=G[P]。
`c(F)` 包括所有分量及孤立點。

上游完整來源信任鏈只沿用：`k≥13`、有限簡單二連通 near-triangulation、
原 B/U 誘導性、原內點的**完整 G-degree≥5**、私人点至多接兩個相鄰 B pins、
每個 C4 有界內部無頂點。由原 `ui−v−uj−x` C4 重新取得 U 附件界，
從而私人點每側至多兩個相鄰 pins，私人孤立點才被 degree 排除。
未假設 F 連通，未把完整 degree 換成 d_F，未加入 N2、ε=2、edge-critical
或 Gallai 身份。來源鏈細讀見 [SOURCE_REVIEW](review/SOURCE_REVIEW.md)。
既有 4CT、screen 與 K≤12 的外部計數信任邊界不變，未重播外部大型證書。

## 2. 任意大小覆蓋與四型的結果

[TOPOLOGY](structure/TOPOLOGY.md) 從原簡單圖的 2-core 及非 degree 二分支
證明完備性。圈秩分配只能是兩個 rank-one 分量或一個 rank-two 分量；後者
的 degree excess 為二，壓 degree 二路徑後只有 theta、figure-eight、barbell。
所有原 subdivisions、附著樹、樹分量及原本可能的孤立點都在推導域內。

[STRUCTURE](structure/STRUCTURE.md) 重新計數全部原面。記 p 為 B–U 邊數，
a 為全 terminal 三角面數，h 為 PPP 面數，M 為 BUP 面數，則

\[
e(F)=r-c+2,\quad M=2(c-2+h),\quad p=a+c-2+h,
\]
\[
\sum_{x\in P}d_G(x)=4r+12-c-p,
\qquad r\le12-c-p=14-2c-a-h\le11.
\]

F 恰有兩個 bounded faces。任何不含 U 的 bounded F face 本身是原 PPP
三角面；這同時控制兩環嵌套及含 bridges 的非簡單面界，不靠圖形直覺。

| 私人核心 | 含 essential cycle | 全 contractible |
| --- | --- | --- |
| 兩個分離單環分量 | p=0 的面式迫 c=1，排除 | 兩 facial triangles 的六根/葉給 M 超額，排除 |
| theta | h=1、M=0，但 PPP 面必含 d_F=2 點並迫 M，排除 | 只剩 diamond；974 完備模板全部有嚴格保 Σ 代表，排除 |
| figure-eight | 同上述任意大小 essential 矛盾，排除 | 四個不同根/葉給 M 超額，排除 |
| barbell/dumbbell | 同上述任意大小 essential 矛盾，排除 | 任意連接路徑長，四根/葉仍给 M 超額，排除 |

全 essential 域有 `p=0,h=1,a=0,c=1,M=0`，leaf 不存在，F 等於 2-core；
rank-two core 至多兩個私人 degree>2 點，所以 PPP 三角面的三點中必有
d_F=2 點，其至少三個 terminal 附件在同一原 link 區間迫 BUP 面，矛盾。

全 contractible 域有 `h=2,M=2c,p=a+c`。
theta 的兩個三角面及原簡單性迫 core 是兩三角形共享一邊的 diamond。
M 精確預算又迫兩個 tips 只可各接一條可空私人路徑，branch points 無附樹，
其他分量是非平凡路徑。得到

\[
c=1:\ 7\le r\le10,\quad 0\le a\le10-r;
\qquad c=2:\ 7\le r\le8,\quad 0\le a\le8-r.
\]

每分量的兩個 M 面把原外 facial contour 分成 B/U 兩段，diamond 的兩個
branch points 各接一側的兩個相鄰 pins。p 個原 cross edges 切成一個
diamond strip、c−1 個 path strips 與 a 個 terminal triangles。
所有原邊、attachments、兩環前進量 `(5,5)` 與 rotation 因而可完整重建。
**普遍性先由這份紙面覆蓋證明取得，有限計算沒有被外推成無界定理。**

## 3. 完備有限核心與全部完整 fibres

[templates.json](controls/templates.json) 保存全部參數及逐圖 hash。
[certificate.jsonl.gz](controls/certificate.jsonl.gz) 保存每圖全部原邊、定向面、
rotation、pin map、ownership、完整 G/F degrees，以及十個 beta 代表的
每列全部 1024 個 U cells（含空 fibres）和全部 A/G lifts。

| c | r | a 的模板數分布 | 合計 |
| ---: | ---: | --- | ---: |
| 1 | 7 | a=0:42；1:88；2:104；3:52 | 286 |
| 1 | 8 | a=0:141；1:136；2:58 | 335 |
| 1 | 9 | a=0:172；1:64 | 236 |
| 1 | 10 | a=0:70 | 70 |
| 2 | 7 | a=0:12；1:20 | 32 |
| 2 | 8 | a=0:15 | 15 |
| 合計 | | | **974** |

主程式由定向面構邊並用 MRV DFS；[獨立程式](independent/check.py) 不 import
主程式，從不同 Cartesian products 篩選參數，由 neighbor intervals 獨立
構邊，再用固定點序 direct DFS 重算 A 及實際補中心的 G。
独立程式亦從 rotation 走 darts 核對指定 B 外面、U 空面及補中心五面。
兩側不是分開的 marginals；全部染色都在同一原圖、同一 literal 色框完成。
共同 S4 換色涵蓋全部 240 proper literal beta，improper beta 被原 B 邊拒絕。

| 檢查項 | 主／獨立共同結果 |
| --- | ---: |
| 完備模板 | 974 |
| 完整 cells | 9,973,760 |
| 空 cells | 9,762,297 |
| 完整 A lifts | 344,416 |
| 完整 G lifts | 167,814 |
| Σ 分布 | 1023:970；639:2；1021:1；959:1 |

完整數學串流 SHA-256：
`daf4b2524be46c2615202ddc42430eb11be7d0329bfd3aa4c529a6be0fb0c326`。
結果**並非全部 Σ=1023**；另外四個模板由各自相同 Σ 的代表處理。

## 4. 保完整 Σ 的實際嚴格代表

[REPRESENTATIVE](structure/REPRESENTATIVE.md) 列出實際 plane annuli 的所有
原邊、面及 rotation 證據入口、具名 pin map、雙向 total full-lift selectors。
[完整代表證書](controls/representatives.json.gz) 保存四圖的 40,960 cells、
40,028 空 cells、1,059 A lifts／551 G lifts，及每個來源模板每個 beta 的
兩向選擇器（拒絕列明記 null）。

| Σ | 來源模板 | 合法同槽位代表 | 內點縮減 |
| ---: | ---: | --- | --- |
| 1023 | 970 | B/U 兩環及五條對應跨環邊；r′=0 | k=13…16 → k′=6，減少7…10 |
| 639 | 2 | r′=4 diamond，word BU，gap 0，after BBBUUU | k=13 → k′=10，減少3 |
| 959 | 1 | r′=4 diamond，word BD，gap 0，after BUUBU | k=13 → k′=10，減少3 |
| 1021 | 1 | r′=4 diamond，word UU，gap 0，after BBUBBU | k=13 → k′=10，減少3 |

先在原來源的完整 canonical-to-original pin map 下構造代表，再用同一
map 搬回，保原 B/U 次序、內外側與中心槽位。代表允許改變原內部接線與
U/中心色，不要求繼承來源的三角化或 degree 條件。
對每份完整 G 染色，按同一 beta 取代表的完整 selector；反向同理。
它們是兩向 total 函數，不需互逆；實際等式只有

\[
\operatorname{pr}_B R_A^3=\operatorname{pr}_B R_{A'}^3.
\]

來源到模板是保全部 pins/lifts 的圖同構；模板到代表是較弱的保 Σ 縮減，
兩者沒有混稱。四代表均補恰五條 spokes，故 `k′=6+r′<6+r=k`。
這已直接違反全域最小內點性，**不需要再查四種 mask 的目錄 membership**，
也不需要以 `r′≤6` 作縮減的先決條件。

## 5. 反控制、審閱與驗證

- [八次破損拒絕](controls/negative/summary.json)：反轉 U 面、漏 diamond 原
  共享邊、錯 U pin map、漏一份 A/G 完整 lift，各被兩套 checker 在首圖
  內容檢查時拒絕；不是因截短輸入的 EOF/覆蓋檢查而失敗。
- 同 Σ 但 R³ 不同：代表證書保存一個實際來源模板與 prism 的 named cell
  差異與完整 lift，狀態 `counterexample`。不把 Σ 相等升為 U/中心色保持。
- 完整 degree 控制：兩套 checker 各算 G/F degrees；私人路徑點可 degree
  一、二、三，未誤套 `d_F≥5`。多分量 c=2 的 47 模板實際觸發。
- 額外 [C6 局部 patch 控制](review/local_patch.json)：diamond 雙中心的完整
  六 pin 關係有 732 proper rows、300 非空／432 空、312 full lifts；九條
  候選 chord 皆不 sound，64 種至多單中心 star 皆不等價。
  [紙面與範圍](review/SOURCE_REVIEW.md) 僅否定這個**更強完整 C6 介面**的
  至多一內點替換，不妨礙本輪較弱全 annulus 保 Σ 縮減。

[最終證明審閱](review/FINAL_REVIEW.md)、[獨立報告](independent/REPORT.md)、
[主 normal／seed17](review/primary-verification.json)、
[獨立 normal／seed17](independent/verification.json) 分開記錄。
真正最小 933／941 來源一律 **not triggered**；沒有把合成必要模板聲稱為
最小來源實現，也沒有從零 target 推來源排除。
沒有新增 Lean theorem，沒有把 Python 或紙面 PASS 混稱 Lean 形式化。

```bash
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank2-243a125/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/representatives.py --check
python3 -B audits/2026-10-13-w5-rank2-243a125/independent/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank2-243a125/independent/check.py
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/negative.py --check
python3 -B audits/2026-10-13-w5-rank2-243a125/review/local_patch.py
```

以上為只讀重播；生成器使用 exclusive creation。凍結副本保留原相對連結的
原 bytes，閱讀舊證明請用 BASE.json 指定的原來源路徑，勿改 frozen 連結。

## 6. 採納與精確剩餘義務

本地 audit 採納全部圈秩二来源排除；接舊森林／單環結果，得到任取合法全內部
W5 的 `ρ(G[P])≥3`。四大雙環類型與所有環相對位置均已涵蓋，rho2 域沒有
剩餘結構義務；只有 theta 使用完備有限染色核心，其他分支是純紙面矛盾。

下一個最小尚未控制的圈秩是 **ρ=3**：其完整分量/core/原附件分類及普遍
保完整 Σ 的嚴格縮減尚未建立。本輪沒有處理一般 rho≥3 代表、一般同步、
所有十三內點以上來源排除或 `K∞=K≤5`；這些仍 OPEN。

文件治理核對：已讀 W5 直接父來源、degree5 link 與 STATUS 停止點。
本輪只交付隔離 audit；正式 docs 的既有 `ρ≥2` 是 BASE 已採納界線，
本包 `ρ≥3` 的正式入口整合尚未進行。凍結來源及舊歷史不覆寫，傳播停在
本包 Source/Evidence。沒有 git 或外部發布操作。
