---
docgraph:
  id: c5.c8-inner-collar
  family:
    - c5
    - c5.c8
  requires:
    - c5.c8-apex-degree
  verified_by:
    - audits/2026-10-13-c8-followup-6cafdfb/REPORT.md
    - audits/2026-10-13-c8-followup-6cafdfb/PROOF.md
    - audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md
---
# C₈ 原短弧接點、內圈與剝層

2026-10-13 現況：本頁短弧接點與 m=9 排除已由
[無四色定理前提 C8 接入](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md)
採納於全域最小 932／933／941 來源契約；後續 m=10 排除得到
**h=3⇒k≥19**。932 的 h=3 已全排，所餘
[八項必要殘留](c5_c8_apex_degree.md#八項必要殘留)均未證來源可實現或任意大小排除。
下文保存原 m=9 論證、證書及當輪 `h=3⇒k≥18` 界。

## 前置來源與使用前提

| 前置來源 | 本頁消費的結論與界線 |
| --- | --- |
| [新三支 C8 契約](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/REPORT.md)、[依賴修復證明](../audits/2026-10-13-c5-no4ct-c8-6cafdfb/geometry/PROOF.md) | 同一全域最小原 disk-C5、原有序框及實際 induced C8；H 內面三角化、嚴格內點 degree≥5。原內部 C3／C4 cap 空、C5 cap 空或 W5，依 C4 的 `s≤k−4<k`、C5 的 `s≤k−5<k` 使用受限代表／最小性；共面商圖可染性只在相對頂點界內成立。 |
| [C8 apex 度數](c5_c8_apex_degree.md#1-精確來源與新增結論) | 八項所有五個 apex 的 H-degree≥4，加上既有三個 y 的 H-degree≥4，供本頁短弧中點度數矛盾使用；不改變八項必要殘留的身份。 |

## 本頁輸出與後續涵蓋

| 依賴鏈中的角色 | 結論／後續來源 |
| --- | --- |
| 原短弧與接點限制 | C 上環距二／三雙接排除；每個 I 點至多兩個 C 接點，雙接只能相鄰或正對；八個原面第三點 t_i 全異，並由 outerplane 耳點證 m≥9。 |
| m=9 完備等號分類 | 唯一 H 的內圖為 W8；回接八項原 collars 的全部十列均為 Σ1023，排除 m=9，得到本頁的 `h=3⇒k≥18`。 |
| [第一層 RING／PINCH／BRIDGE](c5_c8_peeling.md#1-適用前提與任意大小分類) | 下游另消費原 rotation 與無 occupied C3，將本頁接點限制變成完整外面 walk 的三型分類；相鄰雙接唯一性不能只由「至多兩接點」推出。 |
| [m=10 完備分類與排除](c5_c8_peeling.md#3-m10-完備分類與原來源排除) | 三族共 16 個具名 H，回接八項 collars 的 128 圖全 Σ1023；連同本頁排除得到 `h=3⇒m≥11⇒k≥19`。 |
| [任意有限 separator 完整轉移](c5_c8_peeling.md#2-完整染色轉移與任意大小反覆剝層) | 另有一般剝層定理，保存同一原色框的全部 fibres（含空 fibre）、原接點及跨層邊；PINCH 共享原點同色 join，BRIDGE 保留原邊異色。此定理不要求每層維持第一層 C8 前提。 |

下一層 degree≥4、無弦及至多兩接點**均未自動傳遞**；具名控制見
[剝層 §4](c5_c8_peeling.md#4-不能照搬-c8-契約的具名障礙與停止點)。八項 h=3
任意大小來源排除及固定寬度壓縮仍 OPEN。**[h≥4 義務另列](c5_c8_peeling.md#5-h4-的另列義務)**：932 已知
`h≥4,n₅≥10`，但其來源排除及 933／941 的 h≥4 分支仍 OPEN；十九內點界
不涵蓋它們，一般 `k≥16` 由 [K15-SPHERE](c5_k15_sphere.md)獨立證成。
目前交接見 [無四色定理前提交接](tasks/c5_no4ct_handoff.md)，停止點由
[Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

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
