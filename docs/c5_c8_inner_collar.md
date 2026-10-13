# C₈ 原短弧接點、內圈與剝層

2026-10-13 整理補註：[新三支 C8 接入](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md)
已以相對最小性修復小 cap／商圖可染性，將本頁短弧與 m=9 排除接到
無四色定理前提的 932／933／941 契約。932 的 h=3 全排，原八項仍留；
後續剝層界 `h=3⇒k≥19` 同樣接入。無界三支仍 OPEN，下文保留當輪證明。

2026-10-13 後續：[原接點三型與反覆剝層](c5_c8_peeling.md)對任意大小完整分類
RING／PINCH／BRIDGE，並給同一原色框的完整 fibres 轉移。m=10 紙面僅三族、
16 個具名 H；回接八項原 collar 的 128 圖全 Σ1023，故進一步得到
**h=3⇒k≥19**。一般 separator 剝層已證；同型 C8 遞迴有七項具名障礙，
八項任意大小來源仍 OPEN。下文保存原 m=9 論證及當輪 k≥18 界。

2026-10-13。BASE `6cafdfb`。本頁為本次C8後續的權威入口；完整原圖前提、
證明、八份具名完整fibres及獨立覆核見
[隔離報告](../audits/2026-10-13-c8-followup-6cafdfb/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

對全域內點最小、再邊數最大的目錄外disk-C5來源，沿用既有八項h=3契約，
原內圈C為induced C8，內側H的C點度數至少四、嚴格內點度數至少五。本輪證得

\[
\boxed{h=3\Longrightarrow k(G)\ge18.}
\]

令I為C內的嚴格內點、m=|I|，故k=8+m。新證明先得到任意大小的原接點限制：
I中的一點不能同接C上環距二或三的兩點，因此每點至多接兩個C點，八條
C邊的原面第三點亦全部相異。

理由是短弧加兩條原邊形成C4或C5 cap。既有[小cap定理](c5_degree5_link_reductions.md)
使其為空或單一五輪；原C無弦時，任一情形都迫短弧中間點在H的度數僅三，
與原度數界矛盾。全部論證保留原圖、原面與cap側，不依跨列挑選染色。

若I全部接C，原Q=H[I]會是最小度至少三的outerplane圖，與必有低度耳點
矛盾，故八個第三點之外至少還有一點，得到純紙面m≥9。
等號m=9時，原面迫C與另一個C8形成唯一三角化環帶，內C8無弦且只有一個
中心，故Q恰為W8。這是所有等號來源的完整分類，沒有預設搜尋截斷。

把唯一H接回933的c15/c18與941的c04/c07/c15/c18/c20/c30，八圖完整十列
均為Σ1023，排除m=9，故k≥18。獨立程式從舊證書的literal collar edges
重建原圖，以另一搜尋次序逐字比對全部full lifts，包括十列完整fibres。

```bash
python3 -B audits/2026-10-13-c8-followup-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c8-followup-6cafdfb/check.py --check
python3 -B audits/2026-10-13-c8-followup-6cafdfb/independent/check.py
python3 -B audits/2026-10-13-c8-followup-6cafdfb/check.py --negative
```

這是紙面結構證明加八份強制等號圖的完整有限染色證書，沒有新增Lean theorem。
實際933／941來源仍未觸發；排除依據為完備等號化約及完整Σ，並非零觸發。
**八項任意大小殘留仍OPEN**；共同h≥3、n₅≥9及W5私人圈秩≥5均不提高。
一般來源的k≥16由[K15-SPHERE](c5_k15_sphere.md)獨立證成，不能把本頁h=3的
十八內點界套到h≥4。
