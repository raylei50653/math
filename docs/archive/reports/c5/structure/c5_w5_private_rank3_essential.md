---
docgraph:
  id: c5.w5-private-rank3-essential
  family: [c5, c5.w5]
  derives_from: [c5.w5-private-rank2]
  verified_by:
    - audits/2026-10-13-w5-rank3-essential-45bc1c3/REPORT.md
---

# 最小來源 W5：私人圈秩三的環繞分支排除

2026-10-13 現況：在全部完整外框關係不屬 K132 的 disk-C5 圖中，先最小化
內點數、再最大化邊數，對所得原來源任取合法全內部 induced W5，後續已得
私人 `ρ(F)≥5`。本頁只排除 `ρ=3` 的 essential 分支；
[contractible 圈秩三排除](c5_w5_private_rank3_contractible.md)覆蓋另一支，
兩支合併才得到 `ρ≥4`，再由[圈秩四兩分支排除](c5_w5_private_rank4.md)得到 `ρ≥5`。
保存層次及全鏈見[具名關係入口](c5_w5_marked_relation.md#0-保存強度與私人圈秩覆蓋鏈)。
一般私人來源縮減、小代表存在及 `K∞=K≤5` 仍 **OPEN**；下文保留原輪次
證明、證書與當時停止點。

2026-10-13。接續[私人圈秩至少三](c5_w5_private_rank2.md)，本頁是新增結果的
正式入口。完整任意大小證明、凍結輸入與全 fibres 證書見
[隔離報告](../../../../../audits/2026-10-13-w5-rank3-essential-45bc1c3/REPORT.md)。
目前停止點由 [Kempe 導覽](../../../guides/c5_kempe_guide.md#3-停止點與保留缺口)維護。
本次封存及發布核對見[整理紀錄](../../../../history/2026-10-13-w5-rank3-c8-apex-publish.md)。

## 1. 精確結論與來源

G 是所有完整關係不在 K132 的簡單 disk-C5 圖中，先最小化內點數、再最大化
邊數的來源。任取合法全內部 induced W5，保留原外框 B、中心 v、具名循環
鄰點 U，以及同一原圖、同一四色框。令

\[
P=V(G)\setminus(B\cup U\cup\{v\}),\quad F=G[P],\quad
r=|P|=k-6,\quad \rho=|E(F)|-|V(F)|+c(F).
\]

稱 F 的簡單環為 essential，若它在原 annulus 中分隔 B 與 U。
在完整最小來源前提下，本輪證明

\[
\boxed{F\text{ 含 essential 環}\Longrightarrow\rho(F)\ge4.}
\]

本輪原已證 \(\rho\ge3\) 尚未提高為普遍四；後續提升見頁首。若 \(\rho=3\)，則只能保留全部私人環
皆 contractible 的分支；其必要界進一步是
\(7\le r\le13-2c-a\le11\)，其中 a 是全 terminal 的原三角面數。
這是全域最小來源的條件性排除，不加入 N2、ε、edge-critical 或 Gallai 身份。

## 2. 任意大小化約與完整有限核對

設 p 是 B–U 邊數、h 是全私人原三角面數、M 是 BUP 原三角面數。
逐原面與原邊計數得到

\[
M=2(c-\rho+h),\quad p=a+c-\rho+h,\quad
\sum_{x\in P}d_G(x)=4r+10-c+\rho-p.
\]

Essential 且 \(\rho=3\) 時，h=2、p=0，故 c=1、a=M=0、r≤12。
私人 leaf 或私人度二的 PPP 原三角面頂點都會迫 M≥1；因此這些頂點不存在。
又 \(\sum(d_F-2)=4\)，兩個原私人三角面必共享一條邊，四個頂點全私人度三。
其餘私人點度二，完整 F 恰為 diamond 加上連接兩 tips 的一條原路徑。

原 rotation 再迫 diamond 兩個非 tip 點分別只接 B、只接 U，各接兩個相鄰
pins；其餘點在兩側沿同一方向前進。原 degree≥5 與各環恰用五條邊給出
完備接線字域：兩 tips 允許 `(0,0),(1,0),(0,1),(1,1)`，其他點排除 `(0,0)`，
兩側字步長總和均為四，diamond 另各用一步。r=7,…,12 分別有
22、131、340、440、280、70 份，共 **1,283** 份必要模板。

逐圖保存原邊、面、rotation、B/U pins、全部十列各 1,024 個 cells，包含
空 fibres 及全部 A=G−v、G 完整 lifts。主／獨立 checker 都得到所有模板
\(\Sigma(G)=1023\)，與原來源 933／941 矛盾。
模板化先有任意大小的完備證明；沒有把有限搜尋上限當作完備性。
來源到模板是原嵌入的整圖具名同構，須用同一份原 B/U pin map 及共同四色框
逐 cell 拉回；這一步保 R³、完整 fibres（含空格）及全部 A/G lifts。
本輪用完整 Σ=1023 直接排除來源；此同構模板不是較小代表，沒有提出
保 R³ 或 fibre 雙射的縮減構造。

<a id="3-驗證與保留界線"></a>

## 3. 原輪次驗證與當時保留界線

兩套 checker 核對 **13,137,920 cells、12,714,781 空格、730,480 A lifts、
352,020 G lifts**；主程式 normal／seed17 與獨立固定次序 DFS 重播相同。
漏 diamond 原邊、錯 U pin map、反 U 面及漏 full lift 四項破損均被兩套
validator 拒絕，共八次。

```bash
python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/controls/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/controls/check.py --check
python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/independent/check.py
python3 -B audits/2026-10-13-w5-rank3-essential-45bc1c3/independent/negative.py
```

證據為紙面完備化約＋Python 完整有限證書；沿用既有四色定理及外部計數定理
的信任界線，沒有新增 Lean theorem。真正最小 933／941 來源的構造控制為
`not triggered`，排除來自普遍化約，並非零觸發樣本。
當輪的 contractible 圈秩三、一般圈秩至少四、一般 annulus 小代表及
\(K_\infty=K_{\le5}\) 仍 **OPEN**。
