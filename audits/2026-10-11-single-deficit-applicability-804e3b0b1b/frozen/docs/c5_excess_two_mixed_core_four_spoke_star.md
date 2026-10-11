# ε=2 四-spoke binary：原三-spoke star 的同源扇區排除

**後續（2026-10-03）**：[同列端點 hub 排除](c5_excess_two_mixed_core_four_spoke_hubs.md)
已排除本頁下一入口 012／2、S_C=04、S_U=234，並覆蓋全部 32／64
份殘留；mixed-(1,1) 加一原 binary unary 子型及 root 交換全排。
原 276 份 star 排除與本頁數字／證書保留；ε≥3、跨列 palette 定理仍未證。

2026-10-03，接手基準 `b63a096`；保留前輪未提交工作樹。接續
[binary marked-leaf 必要化約](c5_excess_two_mixed_core_four_spoke_binary.md)。
目前入口由 [Kempe 導覽](c5_kempe_guide.md)維護；實際重播與貼用摘要見
[本輪紀錄](history/2026-10-03-excess-two-four-spoke-star.md)。

**原指定 012／0、S_C=012、S_U=234 已作來源排除。** 原 a-star
與整份原 C 的三個共同框鄰點，連同 disk 外側 apex，直接給 K₃,₃
minor。保留原 a 的三條 spokes 後，同一原 H−a 的連通性進一步將
933／941 的 **116／256** 份具名必要域縮為 **32／64** 份，含 root
交換；兩候選合計新增排除 **276** 份。殘留全為 K 雙禁色 schedules。

本輪完成任意大小的原 star 必要條件與固定域 minor 證書，未證跨列
palette 定理、binary 整型排除或 ε≥3；沒有新增 Lean theorem。
殘留仍是必要支援／完整 relation domains，沒有共同十列圖 witnesses。

## 1. 同一原圖與不變的關係介面

G 有限簡單，指定有序 induced-C₅ 為 disk 外框 B=(b₀,…,b₄)。完整
Σ 是 933／941 或整圖 D₅ 像，每條非框邊刪除都嚴格擴大 Σ。
有效內部 H 非空連通，ε=2，恰兩個相鄰完整 degree-5 roots a、b，
其餘有效內點完整 degree 四。a 的三原 spokes 支援 S_a，b 的唯一
原 spoke 接 b_s。

H−{a,b} 恰為原 mixed C 與原 unary U。C 的原 incidence-(1,1)，
有序 contacts (x,y)、owners (a,b)，容許 x=y；U 的不同原 contacts
(u,v) 皆接 b，屬於同一原連通分量。原邊為 ab、ax、by、bu、bv。
actual supports 記 S_C=N_B(C)、S_U=N_B(U)。

沿用前報告的完整 R_C(β;x,y)、R_U(β;u,v)、leaf image K=C∪{a}、
原 (b,a,y,u,v) joint、原 spoke 接回過濾與所有 pinned (b,a) 纖維。
每份原支援域的共同 lifts、逐字面列完整 schemas、query assignment
identities、來源 IDs 和整圖反射身份全部保留。

下面的連通收縮只用於**拓撲 minor**；不識別 contact 顏色，不改寫
R_C／R_U，也不把 b、C、U 換成一份染色 factor。

## 2. 原 star 的必要扇區條件

按原 C₅ 的循環順序記 S_a={i₀,i₁,i₂}，令 P_j 是從 i_j 到 i_{j+1}
的閉框弧（下標 mod 3）。原三條 ab_i spokes 將 disk 分成三個
star 扇區，各自的框邊部分恰為 P_j。

原 C 連通，且其內部及 attachment 邊不穿越原 a-star。它的內部
必位於同一扇區，實際框鄰點只能在該扇區的閉框弧。因此

\[
\exists j\quad S_C\subseteq P_j. \tag{1}
\]

更強地，原 W=H−a 是連通的：原 by 接回整份 C，原 bu、bv 接回
整份 U，原 b 始終保留。它的 actual boundary support 精確為

\[
S_W=S_C\cup S_U\cup\{s\}.
\]

對同一原 W 套用相同扇區論證，得到

\[
\boxed{\exists j\quad S_C\cup S_U\cup\{s\}\subseteq P_j.} \tag{2}
\]

這是任意大小紙面必要條件，不使用 Gallai、degree-list 或四色定理。
框弧端點可同時由原 star 與 W 接入，不能誤改為不含端點的開弧。
每份 W 使用同一原 b、C、U；沒有跨列／跨分量相加支援跨度。

### 指定入口的直接 K₃,₃

原 S_a=012、S_C=012 時，三份閉框弧為 01、12、2340，均不包含
整份 012。在 disk 外側加 apex α 接全 B，再將**整份連通原 C**
作 minor 收縮。六個 branch sets 是

\[
\{a\},\ C,\ \{\alpha\}\ ;\ \{b_0\},\ \{b_1\},\ \{b_2\}.
\]

兩側九個鄰接依次來自原 a-spokes、actual C attachments 與外側
apex 邊。branch sets 兩兩不交且連通，給 K₃,₃ minor，與原 disk
的 apex 圖平面矛盾。此排除涵蓋 x=y、任意原旁支和 root 交換，
不需在原偶數 bridge path 上指定三條獨立 tethers。
原單列對角 relation witness 的代數等式仍保留；其支援域已不能
由上述原 disk 來源實現。

## 3. 固定具名域與逐份 minor 證書

[Checker](../scripts/c5_excess_two_four_spoke_binary_star.py)／
[artifact](../artifacts/c5_excess_two_four_spoke_binary_star/observations.json)
讀取前報告原 116／256 份域，保留全部原 frame queries、candidate
資料、196 份具名 relation records 及每份完整 same-source domain。
原證書不覆寫；新產物記錄其 SHA256 與完整前序 hash 漂移 audit。

只為 topology 將 W 收縮為 w，保留原 ab 作 aw、全部 actual
S_W attachments、原 a-spokes、C₅ 邊及外側 apex 邊。每份違反
式 (2) 的八點 minor，都保存 K₃,₃ 的兩側 branch 頂點及九條路徑；
核對每條邊、簡單路徑、禁止 branch 作內點、內點及路徑邊互斥。
違反式 (1) 的域另存只收縮原 C、保留 ax 的 minor 證書；三個
共同框鄰點型使用九條直接邊。

| 必要核對層，含 root 交換 | 933 | 941 |
| --- | ---: | ---: |
| 前序具名必要支援域 | 116 | 256 |
| 原 C 與 a 的三個共同框鄰點 | 68 | 144 |
| 原 C 其餘 cyclic 扇區衝突 | 16 | 40 |
| C 已在某扇區，原 W 的額外衝突 | 0 | 8 |
| 本輪來源排除 | **84** | **192** |
| 保留具名必要支援域 | **32** | **64** |
| 殘留只含 K pair schedules | 32 | 64 |

276 份排除均有明示 subdivision，沒有以 planarity oracle 的布林值
承擔結論。372 次原 root 交換對照核對支援、狀態及完整 query
assignments 相同；3,720 次整體 D₅ 搬運核對扇區條件，其中 2,760 次
另核對排除 minor 的九條路徑。D₅ 核對是 topology 層，沒有獨立重命名色框或聲稱
新增完整十列共同 coloring。

941 原先 24 份混合 singleton／pair schedules 全被本輪來源排除。
剩下每份必要 schedule 至少有一個雙禁色 query；沿用前報告式 (6)，
其原 C 完整 relation 精確為對角 pair，原 x–y 為偶數長 bridge path，
仍包含 x=y、長度零。

### 原完整 degree 圖控制

另保存 24 張完整 degree 圖，含 root 交換。原 C 取長度 2、4、6
的偶數 path，或 x=y 且保留 bridge／triangle 旁支；U 的兩個
contacts 保持不同，取長度 1、2、4 的 path。全部 actual attachments、
原內邊及 owners 保留，兩 roots degree 五，其餘內點 degree 四。
在同一字面 q=01021 下，逐圖獨立回溯核對 C 的完整 relation
恰為 {(2,2),(3,3)}，並保存 C／U 的整份 tuple coloring witnesses。
另核對原 C 的 connected branch sets、九個實際鄰接及 W 收縮的
exact edge image。這些圖用來核對 minor 提升及共享 contact 身份，
不聲稱候選 Σ、criticality 或 disk 實現。

## 4. 重播與停止點

新 checker 只需 Python 標準函式庫；原 binary 證書仍用其指定環境。

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
python3 scripts/c5_excess_two_four_spoke_binary_star.py --check
PYTHONHASHSEED=17 uv run --with networkx==3.5 python scripts/c5_excess_two_mixed_core_four_spoke_binary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

本輪重播原 binary checker，包含 720 次完整 joint、11,520 次 pinned
纖維，以及前序 `(2,2)` 全部數學 payload／support table 的核對。
該舊證書的單一 docs hash 漂移仍保留，未修正舊 byte-check，未覆寫
原產物。其餘未重播項目及本地環境見本輪紀錄。

**停止點：原指定入口已排除；binary 子型仍餘 32／64 份必要域。**
下一窄入口固定 a=6、b=5、原 a-spokes=012、b-spoke=2，actual
S_C=04、S_U=234。它在原 933／941 表分別為 frame 4／12、domain 24，
兩者都有同一字面 q=01021 的 C 對角 pair、K pair 與 U 禁 1；
原 W 支援 0234 恰落在原閉框弧 2340。這份通過僅表示本輪 star
必要條件未排除，尚未證同圖跨列 palettes／disk 來源存在。
後續保留原偶數 bridge（含 x=y）、U 的完整 binary relation、所有
實際附件與原 root cycle，研究不同拒絕列的共同 palette 證書。

信任層是原 disk 扇區／minor 的任意大小紙面論證、K₃,₃ 非平面性、
前序必要化約及 Python 固定域／原圖 witness 核對；`lake build`
不形式化本輪 topology。其他 incidence 型及雙 root 分支保留，
共同下界仍 ε≥2，整型排除、ε≥3、一般出口及 K∞=K≤5 未證。
