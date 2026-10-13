# 全內部 W5 的具名完整關係縮減

2026-10-12。採納 [隔離報告與完整證明](../audits/2026-10-12-w5-marked-relation-e299ae98/REPORT.md)
及其 [獨立審查](../audits/2026-10-12-w5-marked-relation-e299ae98/review/INDEPENDENT.md)。
本頁是正式入口；目前停止點由 [Kempe 導覽](c5_kempe_guide.md) 維護，
發布核對見 [本輪紀錄](history/2026-10-12-w5-marked-relation-publish.md)。

## 1. 前提與保存的完整資料

固定有限簡單 plane disk 圖 G、原有序外 C5 框 B，以及五度原內點 v。
其全部鄰點按原旋轉為 U=(u0,…,u4)，U 與 B 不交且誘導 C5；
U 的有界內側恰由 v 及五個三角面填滿。刪中心得 H=G−v。
保留同一原圖的 labels、原邊、附件、ownership、旋轉與空出的五邊面。
此槽位由 [最小來源全內部五輪定理](c5_degree5_link_reductions.md) 條件性供應；
下面的完整染色恆等式本身不需最小性或 edge-critical／N2 身份。

在共用色集 C={0,1,2,3} 下，保存

\[
J_H(\beta,\tau)=\{\eta\in\mathcal C_H(\beta):\eta(U)=\tau\},
\qquad \tau\in C^5.
\]

beta 是外框十個固定代表之一；每列全部 1024 格，包括空 fibres，均保留完整 H
染色。只能共同更名全圖顏色，不能獨立正規化 U，也不能以外框十個 bits 代替 J。

## 2. 五個合法較小圖無損重建 H 與 G

令 Q_j 由 H 在原 U 空面內單獨識別 u_j=u_(j+2) 得到，下標模五。
非鄰接保證沒有 loop；沿面內弧收縮後只簡化平行邊，保留全部原邊 preimages。
B 不被識別，仍是外面。五個操作各自合法，不同時施行。
若 G 有 k 個內點，各 Q_j 有 k−2 個。

以具名商映射 pi_j 將完整 Q_j 染色拉回同一 H，得

\[
S_j(\beta)=\{\chi\circ\pi_j:\chi\in\mathcal C_{Q_j}(\beta)\}.
\]

proper C5 的三色型為 (2,2,1)，四色型為 (2,1,1,1)。因此任一完整 H 染色 eta
在五份 S_j 中的重數 m 恰為二或一：m=2 時 U 用三色，中心可且只能取唯一缺色；
m=1 時 U 用四色，不能接中心。這逐份給出

\[
\mathcal C_H(\beta)=\bigcup_j S_j(\beta),\qquad
\operatorname{res}_H\mathcal C_G(\beta)
=\{\eta:m(\eta)=2\}.
\]

所以只需五份商圖的完整 lifts 與原映射，即可重建全部 H／G fibres；不必另枚舉 H。
商圖中的兩個 U pin 像重合，原十個 pin 名稱仍透過 pi_j 保留。
其逐 fibre 帶符號恆等式亦給計數推論

\[
|\mathcal C_G(\beta)|=\sum_j|\mathcal C_{Q_j}(\beta)|-|\mathcal C_H(\beta)|.
\]

這是完整染色資料的縮減。各 Q_j 的外框關係只保留存在性，無法辨認同一 eta
出現幾次；即使較小圖的關係都在 K，也不能僅由 K 的聯集封閉推出原 G 在 K。

## 3. 正聯集與 annulus 代表的界線

可接中心的五種互斥型以單色位置 i 指定：
u_(i+1)=u_(i+3)、u_(i+2)=u_(i+4)。兩個等式必須由同一份 H lift 同時滿足。
它們的接線交錯，不能直接當成合法的雙對商圖；prism 控制甚至給實際 K3,3
subdivision。各識別列分別接受也不保證存在共同 lift。

紙面另排除普遍適用的局部方案：只用原 U 頂點、加邊及空面內非交叉識別，
而不加新頂點的分支，不能以正聯集實現完整 wheel rim 關係。其任一三色 lift
都可拆色成仍合法的四色 lift。這不排除特定 annulus 過濾多出的 lifts，
也不排除改動 annulus 其他頂點的合法縮減。

若能找到同一 B/U 槽位、完整具名 support 相等的 annulus 代表 A'，保留兩向
完整延伸構造，且 B/U 外私人點 r≤6，補中心後即有 5+r+1≤12 個內點。
不同代表 fibres 不必等基數；此小代表尚未構造。
**一般合法正聯集縮減、r≤6 annulus 代表、十三內點以上來源及 K∞=K≤5 仍 OPEN。**

## 4. 有限證據與重播

固定域為 prism、其32種 annular triangulations 及一份有非單元素 fibre 的裝飾圖。
34 圖保存348,160格，其中345,580空格；完整 H／G／商圖 lifts 分別為
3,250／1,620／4,870。170個合法商圖的直接 DFS 與拉回相同，獨立程式亦完整重算。
只保外圈、獨立正規化 U、单對識別就可接中心、分開 witnesses 可接合四項候選均有反控制。

正式資料為 [完整壓縮證書](../audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz)
與 [摘要](../audits/2026-10-12-w5-marked-relation-e299ae98/controls/summary.json)。
原 [verification](../audits/2026-10-12-w5-marked-relation-e299ae98/verification.json)
保存隔離階段正常／seed17、六種破損證書、拒絕覆寫及 hash 核對；發布時另記錄驗證，
不改原 manifest 或原「未採納」歷史語境。

```bash
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/controls/check_w5.py --check --seed 17
python3 -B audits/2026-10-12-w5-marked-relation-e299ae98/review/independent_check.py --primary audits/2026-10-12-w5-marked-relation-e299ae98/controls/certificate.json.gz
```

本包完整 bytes 直接納入 Git，重播只需 Python 標準函式庫。
普遍結論來自上述紙面證明；有限控制標為 `triggered and holds`，真正最小目錄外
933／941 來源為 `not triggered`。沒有新增 Lean theorem 或重跑上游外部計數證書。
