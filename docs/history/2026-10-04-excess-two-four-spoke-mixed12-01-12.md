# 2026-10-04：A₂，mixed-(1,2) 的原 01／12 長／短 face 與完整 joint

使用者指定接續 A 報告 §7，固定原 a=5、b=6、spokes=01／12，
含 root 交換，保留原 C ternary、U singleton relation、actual supports
及完整六角色 joint；若只能收窄須保存殘留／witnesses，不擴大來源
圖枚舉。接手 HEAD=`0e38127`，工作根目錄
`/home/ray/developer/ai/math`。保留既有 A、B、P₃ 等未提交資料；
本輪未 commit／push，沒有改写 A 的原 observations。

## 成果、具名入口與證據層

[A₂ 報告](../c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md)在
A 的固定完整 Σ933／941、Σ edge-minimal induced-C₅ disk、有效 H
連通、ε=2、相鄰兩個完整 degree-5 roots、其餘有效內點 degree 四、
唯一 mixed C incidence=(1,2)、a 側一原單接點 unary U、spokes 各二
及原 ab 的前提下，排除 **原 01／12 整份來源，含 root 交換**。
y₀≠y₁，x 獨立或共享其中一點均保持同一原頂點。

任意大小紙面推導的關鍵是：

- Critical au 迫 U 固定位於長 face 0–4–3–2–b–a。A 的 G−U
  全收與完整 five／six-role 接合迫各拒絕列的原 R_U singleton。
- 01202 的長 face 包絡只見 0、2，固定所有 actual attachments
  的 (1 3) 置換迫完整 R_U={2}。同一原 U 的未用色 3 守恆，
  加上 01212→01021 的 (1 2) 搬運，迫原 actual 2 附件存在。
- 原 a–u↝U–2 crosscut 封長 face C 的 boundary 支援至 {2}；
  另一共同短 face 1–a–b 的 C 支援包含於 {1}。
- 固定同一原 U witness，01202 上取 (a,b,u)=(3,0,2)。短／長
  C 的三個 hubs 色分別為 3／0／1、3／0／2；原 exterior 連通
  的 K₄ 排除與既有三-hub Gallai 引理給完整 C witness。
  接出原 (3,0,X,Y₀,Y₁,2) joint tuple，與兩 masks 的拒絕矛盾。

這只需要指定列／root-pair 的完整 fibre，不主張所有 root pairs
延拓或 ax 省略前後六角色 joints 相等。沒有 C–U 邊，原 U path
的 topology contraction 保持 C 的全部 incidences／degree／exact
lists；不聲稱收縮保持整份 source coloring、Σ 或 relation。

外部 [Dvořák 原講義](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
Lemma 7、Theorem 10 已本輪直接讀取，核對 connected degree assignment、
tightness、Gallai tree 與 blockwise uniform palettes 前提。
原 short-support、single-contact conservation、minimal-core／two-spoke
ternary 與無界 hub／K₄ 論證沿用既有紙面證據；未全面重跑其歷史
checkers，沒有將固定圖 controls 當作任意大小覆蓋。

## 原必要域與保留證書

[新 checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py)
唯讀 [A 原 artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed12/observations.json)，
只重新指定四份 01／12 原框架及其固定七頂點 rotations，核對原
omission identities／actual U singleton schedules。原 A 的 22／26
各排兩份 root 身份，保存 **20／24** 原框架、**52／86** actual U
face／support records、**68／124** 完整 singleton schedules。
全部保留框架以完整原物件保存，不以 anonymous bucket 替換；
原 A 的完整 witnesses 留在原 artifact，輸入 SHA-256 明列。

本題原繼承 U support identities 為 4／6（含 root swaps），每份
唯一 schedule 均為拒絕列 singleton 2。C 幾何後支援 023 已因缺少
原框點 4 而不符合完整來源支援；指定列排除仍涵蓋全部繼承身份。
本題 residual=0／0，沒有將機制搬運到其他入口或擴大來源圖枚舉。
原 crosscut 的 0、4、3 三個 forbidden endpoints，各原 root 身份
及 mask 均保存 explicit apex subdivisions，共 **12** 份。

[新 joint helper](../../scripts/c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py)
的 **36** 張手建完整 degree 圖保持 spokes01／12、兩側 roots、
C sealed support1／2、三種 x 身份、exact U supports023／234／0234。
其中 x 獨立、x=y₀、x=y₁ 各12張，root swaps18份；每份保存原邊、
actual attachments、original owner-to-attachment paths 及整份 witnesses。

固定完整語義核對為：

- **2,880** 次獨立全圖 joins、**46,080** pinned fibres，含 **37,020** 空纖維。
- **57,264** 六角色 tuple coloring witnesses、**3,240** 五角色 witnesses。
- **1,440** 原 spoke 接回、360 原 ax 接回、360 G−au=T_N×R_U 接回。
- 360 非空原 N／U 完整域核對 singleton identity。
- 36 份指定 q=01202 的實際完整 R_U={2} 與 (a,b,u)=(3,0,2)
  下完整 C fibre／完整 G joint，全部有逐邊合法 witnesses。
- Ternary marginal 假接合及 ax 省略後六角色 joints 不相等負控制。

36張原圖完整 Σ 都是1023；這些是固定 relation／degree 控制，
不宣稱 disk、edge-critical 或候選来源實現。未用 planarity oracle，
沒有枚舉新來源 catalogue。

## 重播與工作區檢查

以下研究檢查已通過；main 修改輸入 provenance 後重新生成自己的
observations，再以最終程式及兩種 hash seed 重播：

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py --check
python3 scripts/c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_four_spoke_mixed12_01_12_joint_controls.py --check
lake build
```

Main `--check` 逐 byte 唯讀比對新 artifact；helper 重算 controls，
不寫原 artifacts。`lake build` 通過8,831jobs，只見既有 linter warnings，
沒有新增 Lean theorem，不表示本輪的 disk／palette／minor 證明形式化。
A 舊主checker與其他前序 source-exclusion checkers未全面重跑；
只核對選定四框架的完整數學 payload 與目前保存 input hashes。

新約75 MB observations 登錄自己的 producer／manifest／generated
gitignore；沒有重登錄或覆寫其他來源 artifacts。文件／artifact
最後檢查命令及結果在下方記錄。

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py record artifacts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12/observations.json
python3 tools/artifacts.py status
git diff --check
```

檢查均通過：check_docs 核對523份Markdown、5,414條本地連結；
DocGraph 核對62文件、213relations、5families，0errors／notes。
Artifact status 為ok=141，是檢查當下共用工作區快照，不表示本輪
重播了其他140份artifacts。僅指定新A₂ observations作record，bytes=
77,602,012，SHA-256=`a69f6d8fd188acb1f414885b7d04303cc0163dd2efe9b4821320b7143d00ccf4`；
原A保存bytes=156,113,384不變。最終HEAD仍`0e38127`。

## 停止點與貼用摘要

報告、STATUS、Kempe 導覽、synthesis 與 README 已連接 A₂；A 原
報告頁首加有日期的後續入口，保留原正文、當輪 counts 與原證書。
HANDOFF 仍為研究線薄索引，研究線／進行中 tags 未變，依
DOCUMENTATION 不追加逐輪結果。未 commit／push。

> A₂：先讀 docs/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.md。
> 在 A 的固定 Σ933／941、ε=2、相鄰degree5 roots、mixed12+a-unary、
> spokes各二及ab原來源前提下，01／12及root交換整份排除。
> 完整R_U在01202為{2}，同一原U確有actual2附件；原crosscut封長C至{2}，
> 短C只碰{1}。固定(a,b,u)=(3,0,2)，三hub引理取得完整原C witness，
> 接出原六角色joint，与候選拒絕矛盾。原C ternary及x共享身份保持。
> 其餘20／24具名框架、52／86actual支援、68／124singleton relations保存。
> 新36完整degree控制、2,880joins／46,080fibres及整份witnesses保存，
> 不宣稱disk來源實現。重播：PYTHONHASHSEED=17 python3
> scripts/c5_excess_two_mixed_core_four_spoke_mixed12_01_12.py --check。
> 停止於此，不擴大來源圖枚舉；共用01／01等仍保留，mixed12整型、
> ε≥3、一般出口、Lean拓撲定理及K∞=K≤5未證；未commit／push。
