# 第四輪三標記匹配：二缺額與五／七割障礙

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。唯一寫入本目錄，
前12 audit與shared docs唯讀；未commit／push。

**來源的三標記普通PM失敗已縮成四類精確障礙，尚未證這些障礙全被
排除。** 在同一J*上，兩族為 `110: e,f入且g出`、`101: e,g入且f出`。
三標記對偶邊互不相交；來源原非邊還使兩個強制二邊集都是induced。
刪除強制邊四端點X、再刪禁邊h，得到殘圖H，與普通目標PM有完整雙射。

[PROOF.md](PROOF.md)接本輪J四連通，證明任何Tutte違反集恰為二缺額。
取最大刪點集S後，所有殘分量均奇數階且factor-critical，並滿足

`Σ_C (|δ(C)|−3)/2 + |E(S)| + |E(S,X)| = 1+τ ≤ 2`，

其中τ記禁邊是否跨兩個殘分量。因此非單點分量只可能：

- 沒有，全部單點；
- 一個5割分量；
- 兩個5割分量；
- 一個7割分量。

後兩類另迫τ=1、S內與S-X都無邊。若5割對應原C5避m,z，原小圈再迫
該factor-critical分量恰為保留的五度W5之對偶C5。其餘5割必經m或z。
這定位了來源障礙，沒有假定普通PM或偶補終點已存在。

本輪完整核對兩個加權量：全部J失敗染色數為 `12(W110+W101)`，
普通PM計數與W嚴格分開。

| 固定控制 | 全部PM | 普通110／101 | 偶補權重W110／W101 |
| --- | ---: | ---: | ---: |
| 前輪12點J對偶 | 36 | 1／4 | 2／6 |
| 前輪翻邊J對偶 | 38 | 2／2 | 8／6 |
| 前輪逐面插點J對偶 | 7 | 0／1 | 0／2 |
| 固定Petersen三標記 | 6 | 0／0 | 0／0 |

Petersen控制無非平凡3割，卻有兩份全單點Tutte障礙；它非平面，不能
作來源反例。其餘三圖也不是完整最小來源。沒有以弱控制代替來源推導。

[certificate.json](certificate.json)保存全部87份PM、完整Tait fibres含空、
完整原面／rotation、原J全部染色與固定根lifts、兩族殘圖PM、全部
262,784個Tutte刪點集的分布及全部違反集、最大障礙的逐點刪除匹配。
三張原J控制的Tait積分與獨立完整四色DFS逐tuple核同。

```sh
python3 -B audits/2026-10-15-three-edge-matchings-6ddea32/check.py --check audits/2026-10-15-three-edge-matchings-6ddea32/certificate.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-15-three-edge-matchings-6ddea32/check.py --check audits/2026-10-15-three-edge-matchings-6ddea32/certificate.json
```

正常／seed17通過；`negative/wrong-weight.json`及
`negative/missing-barrier.json`均拒絕；exclusive-create拒覆寫。
見[VERIFICATION.json](VERIFICATION.json)及[INPUTS.json](INPUTS.json)。
唯一新增外部定理為作者原文Tutte 1954 p.348 Theorem A；精確已核內容
及直接PDF存取限制在PROOF §1明列，其餘割預算由本輪自行證明。

另完成[J幾何及完整all-r交叉審查](CROSS_REVIEW.md)：四連通原C5
sector、短圈anchors、雙star完整fibres及12W係數均通過。獨立重建
四份patch全染色，逐boundary row試全部16個hub pairs，並核117個
combined cubes；官方normal／seed17及兩損壞控制也符合預期。

剩餘義務：用原來源排掉上述實際障礙，並在非空普通族內取得偶補
正值；兩步皆不可省略。殘圖不是較小完成來源，接回後原大小不變。
完整319排除、ω=0、一般主命題仍OPEN；沒有新Lean或點數界。
