# BR-SD-1g-ADOPT：獨立數學審查整合

固定審查 base：`c15a635e17d4be814e19aeeeeb765f3d6024099a`。
**ACCEPTABLE**：只限原 [PROOF§1](../2026-10-11-br-sd-1g-dbdc4c35/PROOF.md#1-完整原來源合同與固定量詞) 的完整精確雙旁支合同。
數學阻斷 finding：0。正式採納尚未執行。

獨立 reviewer 在讀原 paper review 之前，自原鄰居、lists 與 block incidence 重建證明；
完整推導見 [獨立 proof REVIEW](agents/proof/REVIEW.md)。Root 另核同一關鍵推論，
不把原 [paper REVIEW](../2026-10-11-br-sd-1g-dbdc4c35/agents/paper/REVIEW.md) 或其 acceptance 當成證明。

## 逐項核查與重建

| 義務 | 獨立推導與結論 |
| --- | --- |
| 原全部鄰居定義的 lists | 對每個原 y∈C，M 鄰居完整分為 C、原 B 附件 A(y)、可能的 s；`L^D(y)=Col−(β(A(y))∪({D} if sy∈E(M) else ∅))`。Wi 內邊、接入邊、附件、r 原坐標均含在內 |
| degree 下界 | `d_C+k+t=4`；β(A(y)) 至多 k 色且不含 D，故 `|L^D|=4−|β(A(y))|−t≥d_C`，不先假設全部 lists 緊 |
| 完整延拓等價 | 固定 β／s=D，`Col(M)≅Col_LD(C)×∏_(z∈Z)(Col−β(A(z)))`，Z 是 effective-H 忽略的原內圖孤立點；各原因子含 D、非空，真正全孤立點的因子才是整個 Col |
| full lifts／空 fibres | 上式是具名完整 assignments 的 restriction／union 雙射；保 Z 原坐標，再按任意 pins 限制仍保完整／空 fibres。忘掉 Z 的投影通常非雙射 |
| 不可染性 | M 自己拒絕 β，故其固定 s=D lifts 空；非空 Z 因子給 C 不可 list-coloring。G critical 不能代替 M 的拒絕／minimality |
| 外部刻畫 | C 有限、簡單、非空、連通；lists 是 degree assignment 且不可染。[Dvořák 作者講義 p.5–6 Theorem10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) 給 Gallai tree、逐點完整 incident union 及相交 palettes 互斥；不要求二連通或預先全緊 |
| 每份 maximal block | 原三環仍是 maximal blocks，uv／兩外臂仍為 bridges；單接點 Wi 無繞路。全部 branch blocks 同受刻畫，bridge palette1、奇環2、Kn 為n−1。非 Gallai 形狀已與不可染性矛盾 |
| J2 witness | 任意奇長≥3的 `w2∈J2−{r,u}` 存在，非 s-contact、無新接線、只 incident J2；d_C=2、完整degree4迫兩個原附件恰 actual pair，故 `P_J2={T,D}` |
| S／L 接口 | C−r 恰原 L⊔S，含 r 和 S 的唯一 C-block 是 J2；Wi 原 ownership 和唯一接點禁止跨側繞路 |
| q 起始 block | q 完整 list 含 T、禁 D；完整 incident union 給 K0 含 T、不含 D。此处 T-only 是相對 T/D，palette 可另含 A/B，不聲稱 singleton |
| 交替維持 | 新 S−q 點含 T/D；進入 block 缺的色須由另一真 incident block 提供。相交互斥使新 block 缺前色，維持恰含 T/D 一色 |
| 始終留 S | 此 exclusive block 不能與 J2 共點，也不能是 J2；因此不含 r、不能經唯一接口進 L |
| 每步不回頭 | block 取不同原出點、vertex 取不同出 block；完整 all-vertex incidence 是有限樹，不回頭 walk 無重複，故新點不是 q |
| 有限矛盾 | 可取有限樹內從 q 起、止於 block 的最長合規路徑；末 block 仍有另一點，其完整 list 又迫另一 block，延長兩條 incidence edges，與最長性矛盾。無無限選擇的隱藏前提 |
| 非割點／leaf／triangle／K4 | 無另一 incident block 時缺色直接矛盾；每個 block 至少兩點，triangle、K4、任意奇環及任意深度有限 W2 都滿足相同步驟 |
| 臂與重合 | p/q 零長、q=a3、a3=v、x2=q／臂內點／普通環點只改原 degree／lists；J2 witness、S 唯一 contact q 與接口不變。超度列先按原 degree 排除 |

## 失效推論與精度裁決

`D∈L(x1) ⇒ D∈P_J1` 是 **counterexample**：x1 是 J1/W1 割點，D 可全部流入 W1 首 block。
本證明沒有使用它，也沒有把某色分給每份 incident palette。局部負控制見
[原 controls](../2026-10-11-br-sd-1g-dbdc4c35/agents/controls/REPORT.md) 和 [新獨立控制](controls/CERTIFICATE.json)。

原最早 proof review 的 ignored-coordinate finding 已由原封存 PROOF§3 的完整因子敘述修正；
本輪重新核對最後 bytes，沒有更改歷史版本。新提案明寫 **S short**，保 canonical 子域標籤；
原 1g 引用 frozen §1／§2.11 已繼承此條件，不將提案擴大到一般 pair-supported 來源。

## 證據分層與依賴

任意大小紙面結論由上述推導和外部刻畫承擔；finite controls 只證其具名小圖。
六圖均接受 β，完整原 source contract **not triggered**；沒有 target realization、沒有新增 Lean theorem。
Fresh primary PDF 與 frozen bytes 完全相同，164927 bytes、SHA256 `50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`，
見 [FETCH](agents/proof/FETCH.json)。既採 1a／1c／1e 是來源合同及局部引理的權威對照；新短證明不靠失效舊引理、SD-A、H_M 二連通或 R31 minor。

完整 `N45-S-NOU-LS-PAIR` 父身份 **OPEN**；完整 OPEN 身份新增無條件關閉數 **0**。
正式採納及上層文件回寫仍須 owner 另行批准。
