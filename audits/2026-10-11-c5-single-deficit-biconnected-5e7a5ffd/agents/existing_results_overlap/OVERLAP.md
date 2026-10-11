# BASE 文獻重疊與直接 Gallai 推論

獨立子查證。BASE `4dd11f422c6fa49265a412085116b088786d0344`；實際 HEAD 與 BASE 相同。只讀權威文件，沒有重跑舊 checker、Lean build、來源枚舉，沒有編輯權威輸入。本筆記只處理既有成果比較，以及從本題前提直接推出 `H−s` Gallai 的部分；高內度 `D` 例外分類与 minor 排除由主查證處理。

## 1. 不需 minimality 的直接 Gallai 推論

設 `U={0,1,2,3}`。對同一原圖 `M` 及同一 proper boundary row `β`，令

`Lβ(v)=U \ {β(b): b∈N_M(v)∩B}`。

因 `B` induced 且 `β` proper，延拓問題恰等於 `H=M−V(B)` 的 `Lβ` 著色問題。對任一內點，boundary 禁色數至多 boundary 鄰居數，因此

`|Lβ(v)| ≥ 4−|N_M(v)∩B| = 4−d_M(v)+d_H(v)`。

這給普通內點的 `|Lβ(v)|≥d_H(v)` 與特殊點的 `|Lβ(s)|≥d_H(s)−1`。不要求 boundary spokes 在 `β` 下異色，也不要求 lists 緊。

按二連通的標準 convention，`|V(H)|≥3`，故 `d_H(s)≥2` 且 `C=H−s` 非空連通。上述下界給 `Lβ(s)≠∅`。任取 `a∈Lβ(s)`；由同一原圖附件定義

`Lβ,a(v)=U \ ( {β(b):b∈N_M(v)∩B} ∪ ({a} if vs∈E(M), else ∅) )`，`v∈C`。

每個 `v∈C` 在 `M` 中完整 degree=4，所以

`|Lβ,a(v)| ≥ 4−|N_M(v)\C| = d_C(v)`。

如果 `C` 不是 Gallai tree，標準 degree-choosability 定理對這一個實際 list assignment 給出 `C` coloring；接回 `s=a` 及原 `β` 得到 `M` coloring，違反拒絕。因此 `H−s` 是 Gallai tree。這一步甚至可在證成 `d_H(s)=2` 前執行；其只用 `H−s` 連通、`Lβ(s)≠∅`、其餘內點完整 degree=4 及外部 degree-choosability 定理。

與 BASE 的差別：`docs/c5_weak_list_cores.md:101–107` 對任意 degree-4 連通分量，透過 minimality 先染外部，再套 degree-choosability。`docs/c5_degree5_interfaces.md:110` 也明說各分量 Gallai 由 minimality 化約。本題外部就是已 proper 的 `B` 加可選色的單一 `s`；外部 coloring 可直接建立，因此不需 minimality。`docs/c5_degree5_interfaces.md:114–125` 已包含固定 `b,a` 的 degree-list 下界及拒絕迫緊，故局部 list 計算是既有機制的應用；解除 minimality 與 arbitrary proper row 的精確定理範圍是本題新增覆蓋。

## 2. 既有成果的精確比較

| BASE 成果 | 本題的重疊 | 本題確實新增／沒有新增之處 |
|---|---|---|
| `c5_weak_list_cores.md:18–35` 的 list 翻譯 | 同一 `M` 的 boundary 鄰居禁色；四色延拓 iff residual-list coloring | 舊文固定三色 `p`、minimal obstruction，由 minimality 排除同色重複 spokes；本題只用禁色數上界，適用任意 proper 四色列，不需要 tight |
| `c5_weak_list_cores.md:96–110` 的 degree-4 Gallai forest | 標準 degree-choosability 外部定理 | 本題靠已染的 `B+s` 直接證明連通 `H−s` Gallai，移除 minimality；不是重新證明外部定理 |
| `c5_degree5_interfaces.md:79–100,114–137` 的單 root 接合 | 原附件、共同四色框、固定 root 色後的 degree-list bounds | 完整 joint relation、`F_C`、block palettes 都是既有機制；本题结构定理只需可延拓性，不新增全部 rows 的完整 `Σ` |
| `c5_k4_blocks.md:13–20,78–100` 的原圖 `K4+B` 得 `K5` | 互斥 connected branch sets，最後把 `B` 作一組，排除 planar 原圖 | 舊文處理全 degree-4 minimal obstruction 的 K4 block，靠 minimality 取得各 bridge 外側通到 boundary；本題 `D` 异常 family 与 complete 情況的实际内部度数直接迫原 B 附件，是不同的适用條件。`K4+B` 的 minor 手法重述，不應算新一般 minor 定理 |
| `c5_k4_blocks.md:102–129` 全 degree-4 單缺失 | Gallai 與 planar minor 機制 | 舊結論是接受全部 T4 的 disk minimal `q` obstruction 得 `Σ=Ω\{q}`。本題有 degree-5 點，只得 `d_H(s)=2`、`H−s` Gallai，既不包含也不提升該 `Σ` 結論 |
| `c5_degree5_guide.md:16–31,36–49` 三-spoke `(2)` 來源結構 | 新定理的 `d_H(s)=2` 在完整 degree5 下等價於三條原 B spokes；二連通使 `H−s` 為同一個連通二接點分量 | 舊 R 系列還假設接受全部 T4、minimal `q` obstruction，并按 Gallai block 型作圖層排除；本題沒有證明 `H−s` block 型數量、來源不存在、其他拒絕列接受、R31 任意長來源 minor |
| `c5_single_sided_exit.md:170–213,217–224,293–311` 條件式單側出口 | `d_H(s)=2` 跟已處理三-spoke核心型一致 | 舊定理另要來源 `Σ(G)=Ω\{p,q}`、相鄰三色 singleton patterns、可處理 minimal core存在性；新结构結論不提供這些前提，不是新出口定理 |
| `lean_guide.md:10–11,21–23,35–47` Lean 工具及缺口 | BoundaryDegree 已有原附件→lists→degree 前提及 root 接合工具 | 新 arbitrary-size single-deficit分類、外部 degree-choosability/Gallai 定理、D family minors及 disk拓撲未形式化；沒有新增 Lean theorem |

## 3. 二連通前提帶來的覆蓋與停止點

本題的新结构定理只篩出一個 degree-5 點的二連通內核：高內度被排除，root 只有兩個內鄰居，而刪 root 後為連通 Gallai tree。它不能套到一般 connected `H`，尤其不能把原圖切成 blocks 後，把多 block cutvertex 的完整 `M` degree 當成單個 block 的 degree。

舊 degree-5 R 系列三-spoke `(2)` 假設，與本題結論會重疊，但沒有全等。舊文沒有要求 `H` 本身二連通；故 C 中可能有不處在兩接點間的末端枝／block。本題若 H 二連通，任何這種只經一個 cutvertex 接入且不含 root 接點的真正旁枝會在 H 中保留 cutvertex，所以不能出現。不要因此宣稱全部既有 Gallai 二接點型已排除：本題仍未處理完整 `Σ`、其他列、所有 block位置与来源可实现性。

`c5_degree5_guide.md:7–10,26–27,44–49` 明確保留 R31、其他三環位置／更多環、完整 `Σ` 和完整 Lean 缺口。本題不会補完这些来源 minor 或分类，除非另外给出覆盖每个相应原图的论证。`c5_single_sided_exit.md:164–166,203–213` 明確保留一般出口。`c5_k4_blocks.md:19–20` 保留共同 pivotal edge、候選 A、`K∞=K≤5`。本子查證没有对 45/54/55、ε≥3、一般出口或上述 equality 给出任何新结论。

## 4. 使用的 memory 與 live verification

Memory 只用于定位既有范围边界；以上 doc 内容均以本次 HEAD/BASE 的实际文件核读。Memory 使用位置为 `MEMORY.md:1507–1515`，rollout id `01a0eb22-3c95-7a41-81af-2f0f449b7f64`。若主报告 final 使用此 memory 记录，应追加规定的唯一 memory citation block；纸面报告不需要把 memory 当数学依据。
