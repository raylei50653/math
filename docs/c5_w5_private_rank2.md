---
docgraph:
  id: c5.w5-private-rank2
  family: [c5, c5.w5]
  derives_from: [c5.w5-private-unicyclic]
  verified_by:
    - audits/2026-10-13-w5-rank2-243a125/REPORT.md
    - audits/2026-10-13-w5-rank2-243a125/review/FINAL_REVIEW.md
---

# 最小來源 W5 的私人圈秩至少三

2026-10-13 現況：在全部完整外框關係不屬 K132 的 disk-C5 圖中，先最小化
內點數、再最大化邊數，對所得原來源任取合法全內部 induced W5，後續已得
私人 `ρ(F)≥5`。本頁覆蓋 `ρ=2` 的四種私人核心及全部 essential 位置，
接森林與單環排除得到當輪的 `ρ≥3`；後續
[essential](c5_w5_private_rank3_essential.md)與
[contractible](c5_w5_private_rank3_contractible.md)兩支覆蓋 `ρ=3`，
[圈秩四兩分支排除](c5_w5_private_rank4.md)再覆蓋 `ρ=4`。
保存層次及全鏈見[具名關係入口](c5_w5_marked_relation.md#0-保存強度與私人圈秩覆蓋鏈)。
一般私人來源縮減、小代表存在及 `K∞=K≤5` 仍 **OPEN**；下文保留原輪次
證明、證書與當時停止點。

2026-10-13。接續 [私人單環排除](c5_w5_private_unicyclic.md)，完整證明與證據見
[W5-RANK2 隔離報告](../audits/2026-10-13-w5-rank2-243a125/REPORT.md)，
凍結 BASE 為 `243a125a80e4d8de40957f59d8da0bdbc974cf69`。
[獨立證明審閱](../audits/2026-10-13-w5-rank2-243a125/review/FINAL_REVIEW.md)判定 PASS；
本次整理及原證據保存見[發布紀錄](history/2026-10-13-n2-rank2-c8-publish.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

**在全部目錄外 disk-C5 圖中先最小化內點、再最大化邊數的完整來源前提下，
任取合法全內部 induced W5，原外框為 B，輪中心為 v、原循環鄰點為 U，
令 k 為 G 的內點數、P=V(G)\(B∪U∪{v})、r=|P|=k−6，則 ρ(G[P])≥3。**
本定理沿用原 B/U 十 pins、完整 G-degree≥5、原三角面及小分隔環限制，
不假設私人圖連通，也不加入 N2、ε、edge-critical 或 Gallai 身份。
上游外部計數及四色定理信任邊界不變；沒有新增 Lean theorem。

## 1. 任意大小分類與來源排除

圈秩二的完整私人核心只有分離雙單環、theta、figure-eight、barbell 四型；
所有 subdivisions、附樹、樹分量及 essential 位置均在分類內。
從全部原面與完整 G-degree 推得 r≤11；全部 contractible 域再得 r≤10。
所有 essential 位置及三型非 theta 核由任意大小紙面矛盾排除。
Contractible theta 必為兩個 facial triangles 共邊的 diamond；原 rotation、
附件與度數把剩餘域完備化為 974 個具名嵌入模板，並非以搜尋上限代替證明。
分類與推導見[拓撲](../audits/2026-10-13-w5-rank2-243a125/structure/TOPOLOGY.md)
及[原面結構](../audits/2026-10-13-w5-rank2-243a125/structure/STRUCTURE.md)。

## 2. 四個實際代表與嚴格縮減

974 個模板的完整 Σ 分佈為 970 個 1023、2 個 639、1 個 959、1 個 1021。
四個同槽位實際 annulus 代表分別有 r′=0 或 4；證書逐圖記錄來源與代表各自的
literal edges、faces、rotation、pin map、全部 cells、空 fibres 及 full lifts。
來源到必要模板是保原嵌入的整圖具名同構，以同一份原 B/U pin map 及共同
四色框逐 cell 搬運，保 R³、完整 fibres（含空格）及全部 A/G lifts。
共同搬回原色框後，
代表保完整 Σ，並減少 3 或 7–10 個內點，直接違反全域最小內點性。
代表只保 `pr_B R³`，不保 R³、U pins 的色或 fibre 重數；更強保存反控制保留。
其雙向 total full-lift selectors 按同一 beta 給完整輸出，不要求互逆，
不構成逐 U cell 的 fibre 雙射；這與來源到模板的同構保存是兩個步驟。
詳見[代表證明](../audits/2026-10-13-w5-rank2-243a125/structure/REPRESENTATIVE.md)。
因此 ρ=2 全域排除，再接既有森林與單環排除，得到 ρ≥3。

<a id="3-驗證與精確剩餘義務"></a>

## 3. 原輪次驗證與當時剩餘義務

主／獨立 checker 完整核對 9,973,760 cells、9,762,297 空格、344,416 A lifts
及 167,814 G lifts；normal／seed17 相同。四種破損證書各被兩套 checker
拒絕，共八次；漏原邊、反 U 面、錯 pin map 與漏 full lift 的防錯紀錄保留。

```bash
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank2-243a125/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank2-243a125/independent/check.py
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/representatives.py --check
python3 -B audits/2026-10-13-w5-rank2-243a125/controls/negative.py --check
```

真正最小 933／941 來源仍為 **not triggered**；排除由紙面完備化約與有限完整
核心承擔，零觸發不作來源排除。圈秩二域沒有殘留；本段保留 essential 採納後、
contractible 採納前的停止點：當時已排除 ρ=3 的 essential 分支，
剩餘最小義務是 contractible ρ=3 的完整結構分類與保 Σ 嚴格縮減。一般 ρ≥3 的縮減、r≤6 代表、R³ 代表及
`K∞=K≤5` 仍 **OPEN**。新 checkout 先依[封存說明](../audits/README.md)還原。
