# BR-SD-1a：共用 r 雙奇環的 D-palette 矛盾獨立驗證

2026-10-11。**裁決：在任務明列的完整原來源合同下，直接矛盾成立。**
這份新獨立封存確認任意奇環長與原外臂長的紙面來源排除；
沒有把有限零觸發當排除，也沒有修改 N45 canonical 覆蓋／採納表。

工作目錄：`/home/ray/developer/ai/math`。
來源 BASE：`4dd11f422c6fa49265a412085116b088786d0344`。
執行 actual HEAD：`0f18104528dcf0b744cdba9e408a5a2bfa466e21`，起始 Git 工作樹乾淨。
專屬輸出：本目錄 `audits/2026-10-11-br-sd-1a-0f181045/`，exclusive-create。
沒有 commit／push／發布；共享 docs、舊證書、舊 audit 不變。

## 精確消除的來源子域

保留 [新任務](authority/current/audits/2026-10-11-single-deficit-publication/NEXT-TASK.md)
引用的 [BR-SD-1 合同1–4](authority/current/audits/2026-10-11-single-deficit-applicability-804e3b0b1b/NEXT-TASK.md)：
N2、無 U、原 long L／真框邊 pair short S、exact-S、X=M=G−原 rb_i，
同一原拒絕 literal proper 三色 β，M 自己 minimal，完整原 G 的 Σ933／941／共同整圖 D5像與逐邊 witnesses。
原 ordered contacts、actual attachments/supports、ownership、rotation、bridges、完整 relations／fibres／full lifts 和原四色座標均保留。

M 內唯一 s 完整 degree5、其他內點4；s 恰兩原有序 contacts p/q，三原 B-spokes 全留。
C=H_M−s 是同一實際 sole component，恰三個原 odd-cycle blocks J1/J2/J3 與原 bridges；
J1∩J2={r}，J3 與兩者不交；J2 私有 u≠r 到 J3 私有 v 的唯一環間原 bridge uv；
p/q 經原外臂分別到 J1/J3 私有點，臂可零長；無其他 blocks／旁支。
D 是 β 未用的第四色。

精確 inventory 是 **N45-S-NOU-LS-PAIR 的 split22／上述三環單 bridge 子域**。
45／54 只在同一原圖上共同交換 roots roles 與全部資料；不另正規化 components。
22 項逐前提核對、9 份 frozen hashes、60 個引用行段、4 種零／正臂組合見
[MAPPING](agents/mapping/MAPPING.md)／[mapping.json](agents/mapping/mapping.json)。
整個 N45-S-NOU-LS-PAIR 身份仍 OPEN，完整 OPEN 身份新增無條件關閉數0。

## 為何矛盾

[完整原點／原邊證明](PROOF.md) 的四步：

1. 原 M 邊給 `L^D(x)=Col−β(N_B^M(x))−({D} if sx為原邊 else ∅)`。
   每點完整度4給 `|L^D(x)|≥d_C(x)`；若 C 可染，與原 β、s=D 沿全部原邊拼出 M 完整染色，違反拒絕。
2. 若 a1 為 p 外臂在 J1 的原錨點，選 `w1∈J1−{r,a1}`、`w2∈J2−{r,u}`。
   各奇環至少三點；無旁支與末端 contacts 保兩點都非 C 割點、非 s-contact，包含零長臂。
3. 兩點在原 C 的全部鄰居恰為本環兩鄰點，其他原 M 鄰居恰兩個 B 附件。
   D 未在 β 上使用，所以 D∈L^D(w_i)。不可著色 degree-list 的正式刻畫給 `L^D(w_i)=S_Ji`。
4. 原 J1/J2 在同一 r 相交，刻畫要求 `S_J1∩S_J2=∅`；兩者卻都含同一 D，矛盾。

外部正式數學依賴是 [Dvořák, List coloring and Gallai trees](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
Theorem10 (Gallai)，印刷頁6，及同頁 blockwise-uniform 定義。
作者講義中有完整定理與證明；本 audit 不將它標成期刊發表或 Lean theorem。
已下載、抽取並核實頁面，原 PDF SHA256 為
`50e998fcb016418698ef31b932c6c2e728007f5e3b3348b93744781196ac1aea`；見 [SOURCE](external/SOURCE.md)。

獨立 paper 分工未讀 screening 報告，逐步重證後四步均判成立；
主端完成 PROOF 後又請其只讀交叉核對，無實質 finding。見 [REVIEW](agents/paper/REVIEW.md)。
證明使用的必要資料是 C degree lists、同一 β 拒絕、s=D 合法、連通 C、原無旁支形狀與外部刻畫。
不依 SD-A、H 二連通、T4 定位或 R27 minor；minimality／Σ 等原身份強前提仍保留。

精度 finding：J3 外臂錨點 a3 是否不同於 v 未明寫，不能由「私有點」推 H_M 二連通。
本證明只選 J1/J2 的 w，沒有使用 a3≠v；限定矛盾不受影響，也不排一般非二連通分支。
舊四 query／uv→R27／target minimality 是舊 minor 路線額外義務，本次明示無須補完，沒有宣稱已完成。

## 有限控制與完整 witnesses

[獨立 controls 報告 v2](agents/controls/REPORT.v2.md) 與
[normal 證書](agents/controls/certificate.normal.json) 保留每列完整列表與一份全點 coloring witness。
有限圖從原 edges 重建 blocks、全部點刪除 components、contacts、cutpoints、w 選取。
最小三三三／零臂的 tight degree-list 域完整枚舉31,104列；五三三／零臂及三三三／雙長1臂各核96個明列 ranks。
總31,296列全部可染。後兩個域只是抽樣；任意大小量詞由上面紙面證明負責。

| 控制層 | 明列結果 | coverage label |
| --- | --- | --- |
| 三份 bounded list domains，w1/w2皆含D | 31,296完整列表／全點染色，全可染 | triggered and holds |
| 撤去 noncut/noncontact w1 的 D-presence | 同一 C 的合法 disjoint block palettes、tight lists及 empty完整fibre；是撤前提後的拒絕例 | triggered and holds，撤前提負控制 |
| 三個 synthetic M，原度4/5、unusedD、原邊接合 | 每圖全M-β fibre恰32；所有原邊色對與四C-query fibres完整保存 | triggered and holds |
| actual BR-SD-1a disk／β拒絕／完整來源合同 | 無來源提交，三個 synthetic M 明確接受β，沒有提供 target rotation／Σ-critical witnesses | not triggered |
| 實際完整來源反例 | 沒有 | 無 counterexample |

撤D負控制的 J1={A,B}、J2={C,D}、uv={A}、J3={B,C} 給相交 blocks互斥；
w1 非割點且非 s-contact卻不含D，所以不滿足由原 β 未用D所迫的列表來源條件。
它不能冒稱完整合同反例。三個 synthetic M 的 disk embedding 未提供／未宣稱。

主端另写 [independent_fibres.py](independent_fibres.py)，不 import list solver、
不從 lists／palette 推結論，直接枚舉全部 M 原邊的 pinned assignments；
比較全 M-β lifts 與移除 s–B 限制的四種 s 色 C fibres，三圖全部完整集合相等。
四 C-query counts 分別是 `(56,16,32,32)`、`(56,16,32,32)`、`(128,128,32,32)`。
這裡保留空／非空完整 tuple 集合的語義，沒有只比布林值或 marginals。

## authority、重播與封存

14 份 current authority exact bytes均與執行 HEAD 的 Git blobs相等；其中6份存在舊 BASE，
8份是 BASE 之後的 audit／出版輸入，明列 BASE absence，沒有偽造 BASE blob。
4份共享 docs 已在出版階段改動，current／BASE分開保存；見 [authority-v2](authority-v2.json)。
舊 A、B、publication 合共680檔、48,702,624 bytes的原地 custody見 [prior-custody](prior-custody.json)。
封存與 live檢查逐SHA256核零漂移、Git tracked/index零變動、全部新untracked僅在本專屬目錄。

本次正常／PYTHONHASHSEED=17 的 controls完全重算與獨立原邊fibre重播均exit0，raw stdout byte-equal。
獨立生成 normal／seed17證書亦byte-equal，均1,388,989 bytes，SHA256：
`7379e65f205108360fa5afb910dc85f78f257bc99837a09eb71ba724b77888e8`。
損壞 coloring tuple 證書預期exit1；主端另移除一個完整M fibre tuple，獨立原邊checker同樣exit1。
封存manifest損壞負控制預期exit1。raw commands／stdout／stderr／exit見
[checks-root-v1](checks-root-v1.json)、[logs](logs/)、[seal-validation](seal-validation.json)。

從 repo root重播：

```sh
python3 -B audits/2026-10-11-br-sd-1a-0f181045/verify.py --check --live
python3 -B audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1a-0f181045/agents/controls/checker.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
python3 -B audits/2026-10-11-br-sd-1a-0f181045/independent_fibres.py --check --certificate audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json
```

`verify.py --check` 核 frozen／Git指定blobs與seal；`--live` 再核當前HEAD／authority／舊audits／exclusive-write，
日後共享資料若有授權更新，live drift不能冒稱零漂移，frozen重播仍分開。
seal-v1.json 綁定製作時全部 immutable payload；seal-validation與其raw logs／損壞manifest是封存後驗證輸出，
未放進自我引用的seal。seals／hashes僅核bytes，不能取代紙面證明。

保存兩處修正代次：authority.json 的 initial_git_status 在freeze後採樣，v2改名git_status_after_freeze，
原v1不覆寫；controls REPORT.md對損壞前原色值的文字誤記，以REPORT.v2.md修正，原文／負控制均保留。
沒有數學失敗步驟，沒有刪除負控制或修改既有封存以求PASS。

## 精確停止點與證據界線

本次完成 BR-SD-1a 指定子域的獨立紙面來源矛盾與新封存；
canonical採納／共享文件更新／commit／push／發布均未執行。
紙面任意大小證明、正式外部定理、有限校準、actual source、Lean保持分層：
actual target source not triggered，沒有新增來源實現或新Lean theorem。

一般bridge-separated三環、其他接點位置、旁支、更多環、一般非二連通來源、其他derivative/core、
55、無45／54來源、一般N45／N2／E、ε≥3、一般單側／共同出口及主命題仍OPEN。
本次只核新audit相關內容；沒有重跑舊R／N45大枚舉、整庫DocGraph或lake build，
那些操作不承擔此紙面矛盾的驗證。
