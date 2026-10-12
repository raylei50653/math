# 共面識別正規形與十二內點的完整關係界

2026-10-12。本文為本題的權威入口；完整證明與固定證據保存在
[隔離研究報告](../audits/2026-10-12-cofacial-uniform-separation-eb6b2303/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護。

2026-10-12 後續：[完整外圈限制](c5_neartri_boundary_collar.md) 在同一最小來源
排除二邊 crosscut，並證 933／941 分別至少有九／八個五度內點；941 的最低
邊界超額只剩 `(4,4,5,4,5)` 的 C7 必要上界。一般來源仍 OPEN。
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
