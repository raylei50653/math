---
docgraph:
  id: c5.cofacial-normal-form
  family: [c5, c5.minimal-source]
  related: [c5.no4ct-handoff]
  verified_by:
    - audits/2026-10-12-cofacial-uniform-separation-eb6b2303/REPORT.md
    - audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/checker.py
    - audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/certificate.v2.json
---

# 共面識別正規形與十二內點的完整關係界

2026-10-14 後續：[C5→C4 完整來源橋](c5_c4_boundary_pivot.md)沿用正規形及
no4ct 度數修復，接外部 4-candidate 完整計算得 `K≤22=K≤5`，最小來源共同 k≥23。
本文及舊證書保留各輪界線；二十三內點以上與無界主命題仍 OPEN。

## 證明鏈與閱讀定位

本文是共面正規形及原 `K≤12=K≤5` 推導的權威入口；
[兩條證明鏈的閱讀表](tasks/c5_no4ct_handoff.md#1-先讀這四份權威報告)
分列原鏈與不以 4CT 為前提的替代鏈。下列歷史補註不取代各步的原前提。

| 本文使用的前置 | 實際用途與證據 |
| --- | --- |
| [Kempe／外側 screen](c5_kempe_screen.md#3-外側-cell-測試) | 原鏈由非空性及外側黏合的 4CT 得普遍必要 screen，只留 933／941 的整圖 D5 像；有限 mask 表不證普遍 soundness |
| K 的 132 份小 witnesses、二元聯集封閉與全域最小內點／再最大邊數 | 共面 Eq／Diff 分解給不增內點的正規形；[紙面證明](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/paper/cofacial_normal_form.md)與 [v2 證書](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/certificate.v2.json)分開承擔一般論證與有限核對 |
| [count-cone 翻譯](c5_count_cone_bridge.md#1-文獻錨點與精確翻譯)及外部 Corollary 20 | 對偶 `2k+4<30` 才可得 `m≤0`，與候選的 `m=x24>0` 矛盾；[EXTERNAL](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/EXTERNAL.md)保留未重播的文獻計算信任 |

替代鏈的前置改由[零內點 cap 下降報告 §§2–5](../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md#4-不用-4ct-的最小來源分類)
提供：空關係及十個低候選嚴格下降，只對全域最小來源保留 **932／933／941**。
三支均非空、全收 T4，故可重用本文的共面／Jordan 論證及 count-cone 翻譯，
仍接同一外部 Corollary 20。這不證普遍 exterior screen，也不排除一般 932。
一般 932／933／941 及 `K∞=K≤5` 仍 **OPEN**。

DocGraph 的 `related` 連到替代鏈交接；無 metadata 的 screen／count-cone 前置
以本表定位，未虛造 ID。`verified_by` 是證據路徑標籤，正文連結與重播命令才是核對入口。

2026-10-13 整理補註：[無四色定理前提下降與正規形](../audits/2026-10-13-c5-no4ct-dependency-6cafdfb/REPORT.md)
另以零內點 cap 下降處理空關係／低候選，保留 932／933／941 三支；
仍接外部 Corollary 20 的有界定理。後續[受限 C4 與球面接入](../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
完成替代 `K≤15=K≤5` 證明。下文普遍 screen 的原依賴保持，無界三支仍 OPEN。

2026-10-13 最新後續：[K15-SPHERE](c5_k15_sphere.md)證 `K≤15=K≤5`，一般來源至少十六內點；
[C8原接點／剝層定理](c5_c8_peeling.md)另證 `h=3 ⇒ k≥19`；八項無界來源仍 OPEN。
八項無界殘留與一般主命題仍OPEN；下文及舊證書保存各原輪次語境。


2026-10-13 最新後續：[K14-SPHERE](c5_k14_sphere.md) 已證 `K≤14=K≤5`，
一般目錄外來源至少十五內點；同份新紙面證明給 `h=3 ⇒ k≥16`。
下文先前界線與證書保留當輪語境，h≥3、n₅≥9不提高。


2026-10-13 後續：[K13-COLLAR](c5_k13_collar.md) 完整排除十三內點剩餘外圈，
得到 `K≤13=K≤5`，一般目錄外來源至少十四內點；`h≥3`、`n₅≥9` 不提高。
下文原輪次的十三內點 OPEN／k≥13 保留歷史語境；新結果未 Lean 化。

2026-10-12。本文為本題的權威入口；完整證明與固定證據保存在
[隔離研究報告](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。

2026-10-13 後續：[跨原邊缺陷搬運](c5_cross_edge_kempe.md) 證五度輪的完整
J_e fibres 三元組、相鄰五度中心的共同中間 lift 雙射及同一 lift 的二色路徑限制；
一般來源排除與普遍同步仍 OPEN。

2026-10-12 後續：[完整外圈限制](c5_neartri_boundary_collar.md) 在同一最小來源
排除二邊 crosscut；2026-10-13 再以共同計數排除941的最後C7上界，
933／941 均必 h≥3、至少九個五度內點。一般來源仍 OPEN。
同日 [全內部五輪及 A／B／C 交付](c5_degree5_link_reductions.md) 進一步保證
全內部 induced W5，完成具名位置契約、固定域重接表及 C5＋C5 cap 閉合；一般縮減仍 OPEN。
同日後續[最小來源度數界](c5_saturation_degree_bound.md) 沿用本文前提，排全部四度內點，
證邊界度數至少四、內部至少五及至少六個五度內點；一般主命題與十三內點以上仍 OPEN。

## 1. 結論與適用範圍

對有限簡單 disk 圖，固定帶標號、有序的 C5 外邊界，允許內側 chords，
以完整十 bit 延伸關係定義 \(K_{\le r}\)。本輪得到

\[
\boxed{K_{\le12}=K_{\le5}=K,\qquad |K|=132.}
\]

若目錄外關係存在，來源至少需要十三個內點。一般
\(K_\infty=K_{\le5}\) 仍 **OPEN**。

證據是既有 Kempe／外側相容必要性（後者使用 4CT）、本輪有限目錄核對、
一般紙面正規形及 Dvořák–Lidický 的外部計數定理。沒有枚舉六至十二內點圖，
沒有新增 Lean theorem，也沒有重播外部論文的計算證書。

## 2. 可重用的正規形機制

對共面非相鄰頂點 \(u,v\)，至少一端是內點時，可合法識別並保留原 C5：
若另一端在邊界，保留該 label；平行邊簡化時保留原框邊。完整關係滿足

\[
\Sigma(G)=\Sigma(G/(u=v))\cup\Sigma(G+uv).
\]

132 個目錄關係對二元聯集封閉。在所有目錄外來源中，先最小化內點數，再最大化
邊數。quotient 減少內點，必在目錄中；若加邊結果也在目錄中，原關係由聯集封閉
性也在目錄中。因此這種最小來源的每對共面、至少一端為內點的頂點必已相鄰。

刪除不影響完整關係的分量及割點枝塊，最小性迫圖二連通。若長面含內點，兩條
面外既存連線，或一條面外邊與經外側 apex 的路徑，會連接交錯端點，違反平面
分離性。既有必要 screen 又使目錄外來源全收 T4、邊界無 chord。故最小反例
可選為**簡單、二連通、chordless-C5、所有內面皆三角形**，不增加內點。

這是最小反例的存在正規形，不是任意原圖都能逐步保持同一完整 Σ 而補成三角化
的演算法。這裡的最大邊數來源也不能套用舊 edge-minimal／edge-critical 的
deficiency 或 Gallai 前提。[完整紙面證明](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/paper/cofacial_normal_form.md)

## 3. 十二內點界與外部依賴

正規形有 \(k\) 個內點時，對偶有 \(2k+4\) 個頂點；外面對偶點 degree 五，
其餘 degree 三。Dvořák–Lidický 的 Corollary 20 適用於**少於三十**個頂點。
沿既有 [count-cone 翻譯](c5_count_cone_bridge.md)，該定理給 \(m\le0\)。

目錄外候選只有 933／941 的整圖 D5 像。共同搬運後，它們的 singleton support
包含於 \(\{2,4\}\)，且 `01232` 有完整延伸，故 \(m=x_{24}>0\)。當
\(k\le12\) 時矛盾。結合目錄中每個關係的五內點 witness，便得 §1 的等式。
本推導不需再假定五內點 graph enumeration 的完備性。

文獻來源及沒有重播的部分見
[外部定理界線](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/EXTERNAL.md)。

## 4. 完整 fibres 與重接界線

在全域內點最小的 933／941 來源，每份 `01232` 延伸都使所有共面且至少一端為
內點的不同點異色。933 另有 `01231` 的同樣結論。在三角面正規形上，此條件
退化為 properness，不能直接繼續合併。

保留一列的全部完整延伸仍不足以保重接後的 Σ：兩內點控制從 567 經合法 flip
變成 854，原 `01232` 延伸全部保留。另一個刪邊再識別控制變成 774。
它們沒有觸發固定 933／941 前提。

對內邊 `e=st` 及兩側 opposite vertices `u,v`，後續保留 `G−e` 同一份染色的
四格 \(J_e(p;[s\ne t],[u\ne v])\)，包括全部十列的空 fibres 與 full lifts。
已證一個窄推論：至少一個 opposite vertex 為內點時，若
\(J_e(01232;1,0)\ne\varnothing\)，則某個原拒絕列 \(p\) 滿足
\(J_e(p;0,0)\ne\varnothing\)。這給同一新增列的二色四邊形見證，沒有證明不同
原邊的這些見證能共同配合。[精確共同關係與反控制](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/review/rewire_analysis.md)

## 5. 重播與信任邊界

```bash
uv run --with networkx==3.5 python audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/checker.py --check audits/2026-10-12-cofacial-uniform-separation-eb6b2303/controls/certificate.v2.json
python3 audits/2026-10-12-cofacial-uniform-separation-eb6b2303/review/rewire_controls.py --check
```

本輪核對 132 個完整關係 witness 與 apex 平面性、8,778 組聯集、必要 screen 的
153／142／10 分類、D5 搬運、完整 Eq／Diff lifts 及重接負控制。
normal／seed17 一致，破損證書被拒；原研究凍結檔保持不變。

具體 933／941 最小來源是 `not triggered`，未聲稱實現；普遍正規形與有界排除
來自紙面證明，不能由零 target 控制推得。有限 screen 的普遍 soundness 仍依赖
原 Kempe／disk 黏合紙面論證及 4CT。十三內點以上、一般壓縮定理及 Lean 化保留。
發布核對見 [本輪紀錄](history/2026-10-12-cofacial-normal-form-publish.md)。
