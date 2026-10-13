# C8-STRUCT：固定來源契約

BASE：`243a125a80e4d8de40957f59d8da0bdbc974cf69`。
本輪只研究下列十項，不重啟其餘六十项查詢：

| 完整 Σ | 原查詢 |
| --- | --- |
| 933 | c15、c18 |
| 941 | c04、c07、c15、c16、c18、c20、c30、c32 |

逐項的具名 C₈ 順序、超額分配、原附件、完整原邊、原 274 座標向量、
全部十列外框計數，以及保留整份契約的反射映射，見
[classification.json](classification/classification.json)；其紙面分類見
[CLASSIFICATION.md](classification/CLASSIFICATION.md)。共同的邊界色列順序為
`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`。
這個順序與原 frozen 證書完全一致，空列不能刪除。

## 原來源的量詞

G 是所有完整關係不屬於 K132 的有限簡單平面 disk-C₅ 圖中，先最小化
原內點數，再最大化邊數的來源。外框是原有序
`B=(b0,b1,b2,b3,b4)`。整張圖及其全部染色經同一次 D₅ 搬運後，
完整 Σ 恰為 933 或 941。不是固定單一 mask 的局部最小化。

沿用 BASE 已證前提：B 無 chord、G 二連通、全部內面三角化；原框点
度數至少四，原內點完整度數至少五；沒有含頂點的分離三角形，也沒有
原內點同時接兩個不相鄰 B 點。所有來源至少十三原內點。
目錄代表、C₄ 三內點代表與 `K≤12=K≤5` 的上游依賴原樣保留；本轮沒有
重證或重播其外部計算。沒有加入 N2、ε=2、edge-critical、degree-4／degree-5
roots 或 Gallai 前提。

寫 `e_i=deg_G(b_i)-4`，則本域 `sum(e_i)=3`。原框邊 `b_i b_(i+1)` 的
面 apex 為 `a_i`；它對 B 的全部附件恰為 `{b_i,b_(i+1)}`。
`b_i` 的內側 rotation 恰為
`a_(i-1), y_(i,1), ..., y_(i,e_i), a_i`。
每個私人點 `y_(i,j)` 對 B 只有附件 `b_i`。
五個 apex 與三個私人點互異。

五個原面 `(b_i,b_(i+1),a_i)`，以及每個 b_i 與上述 rotation 相鄰兩點
所成的原三角面，完整填滿 B 和 C₈ 之間的環帶。所有其餘原點與原邊
都在同一 C₈ 的閉內側 H。不得為不同色列改換 H、附件、rotation 或私有區域。
H 的嚴格內點對 B 沒有任何附件；其完整度數就是 H 度數。

因此在這一個 H 上，同時有 `deg_H(a_i)≥3`、`deg_H(y_(i,j))≥4`，
嚴格內點度數至少五，內面三角化及原分隔限制。新證的無內弦與小 cap
條件見 [geometry/PROOF.md](geometry/PROOF.md)，不是額外假設。

## 計數及交換的共同色框

固定 literal 四色 `0,1,2,3`。對具名 C₈ 每一個 proper word p，x_p
是同一 H 上延伸 p 的**所有完整染色數**。274 個 S₄ 代表只是同一全圖
色名置換的索引；二色列穩定子及原軌道大小仍保留。
原外框固定 literal 列 r 的全圖計數為 `y_r=sum_p T[r,p] x_p`。
T 使用原環帶全部附件，不以分別正規化的兩側代表直接黏合。

新 Kempe 條件把同一圖的可逆分量交換軌道按完整邊界列共同計數。
它不把逐列任選的分割當成同一 H；非負軌道權重的必要性另有普遍
雙射證明。它也不要求 noncrossing equality 展開係數非負。
滿足這些必要條件的向量仍不是實際圖、source realization 或反例。

五度輪的完整 J_e fibres 仍須來自該同一 G，並保留中心以外完整染色。
既有跨邊雙射不能從本輪只記 C₈ 的向量中自行恢復原五度中心、原邊
與 singleton 分量。需要的 escape 前提仍須另證，不能把不同邊或不同列
的存在見證視為共同完整 lift。

## 證據保存

[BASE.json](BASE.json) 記錄從指定 Git object 讀取的 58 份輸入。
上游 `interface.json` 是未追蹤的生成檔，本輪先驗證它與 BASE 已提交
MANIFEST 的 SHA256 和位元組數完全一致，再獨立凍結；來源見
[DERIVED_INPUTS.json](DERIVED_INPUTS.json)。舊證書、舊失敗、manifest 和
其他 session 的檔案均未修改。

本輪授權僅限本地研究、證明、程式、文件及驗證；不 commit、push、
建立 PR／Issue 或對外留言。紙面定理、有限核心、有限圖校準、必要條件
殘留及 Lean 狀態分開驗收。
