# 最小來源 W5：contractible 圈秩三排除與私人圈秩至少四

2026-10-13 最新後續：[圈秩四兩分支排除](c5_w5_private_rank4.md)
合併contractible的6,389模板與新essential的2,872模板，
得到任取合法全內部W5的私人 `ρ(F)≥5`。一般縮減／小代表及主命題仍OPEN；
下文原輪次界線與證書保留，不宣稱不同圖的R³等價。


2026-10-13，固定 BASE `50d5474f2446403f3b3001d5943571184c8c9936`。
完整紙面、凍結輸入、原嵌入與全部染色證書見
[W5-RANK3-C 隔離報告](../audits/2026-10-13-w5-rank3-contractible-50d5474/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 1. 精確結論與來源量詞

G 是全部目錄外 disk-C5 圖中先最小化內點數 k、再最大化邊數的來源。
**任取**合法全內部 induced W5，原中心 v、原循環鄰點 U、原外框 B，
十 pins 互異，U 內恰為 v 及五個原三角面。令

\[
P=V(G)\setminus(B\cup U\cup\{v\}),\quad F=G[P],\quad
r=k-6,\quad\rho(F)=|E(F)|-|V(F)|+c(F).
\]

本輪完全排除 ρ=3 且 U/v 位於 F 無界面的 contractible 分支。
接[私人圈秩至少三](c5_w5_private_rank2.md)與
[essential 圈秩三排除](c5_w5_private_rank3_essential.md)，可採納

\[
\boxed{\text{任取合法全內部 W5，}\rho(G[P])\ge4.}
\]

這是完整最小來源的條件定理；沒有加入 N2、ε、edge-critical、Gallai 或
F 連通前提。仍從 k≥13、r≥7 開始，不依賴並行 K13-COLLAR 結果。

## 2. 可重用的結構與完整附件化約

本輪獨立核對一般圈秩面式。contractible 的三個有界 F 面都必是原 PPP
三角面，因此 t_P=3、M=2c、p=a+c，且

\[
7\le r\le13-2c-a.
\]

完整 G-degree≥5 與每環至多兩附件先排私人孤立點，再排 c≥3。
剩 c=1、7≤r≤11 或 c=2、7≤r≤9。這裡 M 分別是2、4，沒有借用 essential
的 M=0 或私人無葉性。[原面及分量證明](../audits/2026-10-13-w5-rank3-contractible-50d5474/structure/FORMULAS.md)

對 cyclic block H，令 ℓ 是原外面長、i 是原內部點數，得到
`ℓ+2i=ρ(H)+2`。圈秩至多三的 blocks 只有 triangle、diamond、三角化
五邊形及含一內點的 K4；K4 內點的完整 G-degree 恰三，直接矛盾。
對一個分量的 m 個 cyclic blocks，block-cut 連接樹最多使用 `2(m−1)`
個 ear incidences；每個未使用的 ear 或其附樹 leaf 供應不同 BUP 面。
這排除全部多 cyclic-block 配置及 c=2 的 (2,1) 分配。
M 預算取等號迫唯一剩餘形狀為**三角化五邊形 fan、兩耳各一條可空路徑，
另加 c−1 個非平凡路徑分量**。所有原 bridges、cut vertices、subdivisions
保留。[完整 block 分類與 ear/leaf 計帳](../audits/2026-10-13-w5-rank3-contractible-50d5474/structure/CORE.md)

原 contour 的兩次 terminal 切換迫兩側 fan；B–U crosscuts 把 annulus
完整分成 fan strip、path strips 與全 terminal triangles。短側 apex 必接
一或兩 pins，長側兩點各接兩個 pins；兩種 B/U 方位均保留。原旋轉的
[完整編碼](../audits/2026-10-13-w5-rank3-contractible-50d5474/structure/ATTACHMENTS.md)
恢復全部原邊與面，給 c=1 的2,162份、c=2 的108份必要模板。

## 3. 完整 Σ 直接排除，不需要代表

2,270份模板逐一保存 literal edges、指定 B/U 面、rotation、pin map、
私人分量、完整 G/F-degree、十列各1,024 cells、空 fibres 及全部 A/G lifts。
完整 Σ 分佈為

| Σ | 91 | 511 | 639 | 767 | 1007 | 1021 | 1022 | 1023 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 模板數 | 2 | 8 | 32 | 8 | 2 | 1 | 1 | 2,216 |

八種都屬固定 BASE 的 K132，且整圖 D5 pin 拉回仍在 K132，直接矛盾目錄外
來源身份。這是完整必要域的結論；模板不必全部符合尚未使用的其他來源條件。

本輪採直接 Σ membership 完成，**沒有聲稱縮減代表或 R³ 保存**。
source-to-template 同構保全部 pins/full lifts；它不是較小代表。
實際 prism 控制與來源模板同為 Σ=1023 卻有不同 R³，保存強度反例完整留存。

## 4. 驗證及剩餘界線

主 normal／seed17、獨立鄰點重建與固定次序 DFS 全部一致：
23,244,800 cells、22,713,170 空格、928,404 A lifts、465,866 G lifts。
八種破損各被兩套 validator 拒絕，共16次；另有同Σ異R³反例。
詳細命令、儲存與文件檢查見[REPORT](../audits/2026-10-13-w5-rank3-contractible-50d5474/REPORT.md)。

證據為紙面完備化約＋Python完整有限證書；沿用上游 K132、四色定理及外部
計數的信任範圍。真正最小目錄外來源實例仍是 `not triggered`，排除不是
由零觸發樣本推出。`lake build`僅作回歸，沒有新增 Lean theorem。
一般圈秩≥4來源縮減、一般小代表及 `K∞=K≤5` 仍 **OPEN**。
原隔離研究只作本地驗證；本次主線整合、原 seal 保存與重播範圍見
[發布紀錄](history/2026-10-13-k13-rank3-publish.md)。原報告的「未 commit／push」保留當時語境。
