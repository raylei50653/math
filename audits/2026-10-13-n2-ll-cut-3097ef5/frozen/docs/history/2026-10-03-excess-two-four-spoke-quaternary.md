# 2026-10-03：四-spoke 原 mixed-(1,3) 四接點 leaf-slack 排除

基準 `b63a0965434d68a28292994638b2c98e848585b8`，工作目錄
`/home/ray/developer/ai/math`。保留 singles／binary／star／hubs／ternary
前序未提交成果，接續使用者指定的 mixed-(1,3) 無 unary 原四接點窄型。
本輪未要求亦未執行 commit／push，沒有重開來源圖枚舉。

## 結果與證據

[新報告](../c5_excess_two_mixed_core_four_spoke_quaternary.md)／
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py)／
[joint helper](../../scripts/c5_excess_two_four_spoke_quaternary_joint_controls.py)
完成原 incidence-(1,3) 無 unary 的來源排除，含 root 交換。
同色原 spoke 省略後保留唯一原 K=C+a，四 contacts=(a,y₀,y₁,y₂)，
原 C 的四點 tuple=(x,y₀,y₁,y₂)，x 可共享任一 yᵢ。

拒絕要求完整 F_K 包含 b 的三個可用色；a 的保留兩 spokes 看到兩色，
且 deg_K(a)=1，對任何已見色 d，a 的 exact list 有二色，其餘每點 list
至少內部 degree。原 spanning tree 以 a 為根逆序貪婪染色，得到 d∉F_K，
故 |F_K|≤2，矛盾。指定 012／2、q=01021、省略 a0／a2 時取 b=1；
完整染色接回同色原 spoke 仍有效。這份反證不需要 M 的 q-minimality、
Gallai、K₅ 或 T4；任意長度／旁支的 soundness 由直接紙面貪婪證明負責。

933／941 的20／60具名框架全排；40／160個 queries 全部 leaf-slack，
80次 root 交換及2,000次整體D₅搬運。保存原 necessary skeleton edges、
apex rotation及source index，未將它們視為完整來源disk實現。
連同前三子型的紙面結論，(3,1) 唯一 mixed 全部四份原 incidence 分拆封閉。
其他四-spoke (2,2) 及 ε≥3 仍未證。

另保存80張完整degree圖：八種原C形狀×五份附件×root交換。
2,400完整六點joints、2,400完整K四點relations、38,400 pinned fibres、
480同色省略等式及2,400份整圖貪婪extension witnesses與獨立回溯核對。
所有原C tuples、共享x身份、exact lists、tree parents及全染色均保存。
四點marginals假允許／完整guarded fibre空的反例也保留；有限圖不聲稱
disk、候選Σ或criticality，沒有以短圖外推任意大小。

## 實際驗證與產物

新層預設 seed 與 PYTHONHASHSEED=17 的逐 byte checks 通過；前序 ternary
checker 也重播通過，該 checker 同時精確核對既有 (3,1) active-triangle
完整 payload。實際執行：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_ternary.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py record artifacts/c5_excess_two_mixed_core_four_spoke_quaternary/observations.json
python3 tools/artifacts.py status
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel linter
warnings，沒有新增 Lean theorem。文件檢查通過 497 份 Markdown／5,095 個
本地連結；DocGraph
通過 62 documents／213 relations／5 families，零 errors／notes。產物 status
為 `ok=131`，無 missing／changed／stale，`git diff --check` 通過。
這些檢查不形式化本頁的任意大小紙面 connected-list 證明。

新 observations 為 **52,711,125 bytes**，SHA256
`a5ffb7f80b33196cbe42be4c1f3cc00452d545b692fb6428e8573989cfd2ad07`。
依大型產物政策留本地，MANIFEST 記錄 digest、producer 及 source 依賴。

前序 single-spoke 舊 byte-check 的三份既有文件 hash 漂移維持；新層明存
這三份 drift及原source digest。本輪未重播該歷史byte-check，完整數學
payload相同的唯讀audit沿用[前輪紀錄](2026-10-03-excess-two-four-spoke-ternary.md)。
更前序two-two單一docs hash漂移亦未處理，全部舊artifact保留。
本輪不重跑其餘binary／star／singles、唯一degree-6、R-series、
weak-deletion、完整來源catalogue或Lean axiom audit。

HANDOFF維持薄研究線索引，線及tags未改；README、Kempe導覽、STATUS、
全線整合及前序ternary／leaf-fibers的後續指向隨本輪更新。

## 停止點與貼用摘要

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及docs/c5_excess_two_mixed_core_four_spoke_quaternary.md。
保留b63a096上的既有工作樹，本輪未commit/push。
完成四-spoke(3,1)、mixed-(1,3)無unary及root交換的任意大小來源排除。
原a012/b2、q01021省略a0或a2；唯一原K=C+a，contacts=(a,y0,y1,y2)。
原C四點relation=(x,y0,y1,y2)，共享x和所有原附件/bridges完整保留。
拒絕要求K禁b的3色；leaf a只容至多2禁色。取b=1，L(a)={2,3}>deg_K(a)=1。
原spanning tree逆序貪婪給整份原M/G witness，不需minimality/Gallai/K5/T4。
933/941原20/60具名框架全排；200queries、80root交換、2000D5。
80完整degree圖、2400joints/K relations、38400pinned fibres、2400貪婪extensions、480等式。
重播：PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_quaternary.py --check。
新證書兩seeds及前序ternary byte-check通過；lake build通過8831jobs。
文件/DocGraph/產物status通過，ok=131；git diff --check通過。
前序single_spoke三份docs hash漂移維持；完整payload audit沿用前輪，舊產物不覆寫。
結合前序singles/hubs/ternary，唯一mixed的(3,1)全部四份incidence分拆已封閉。
下一窄型(2,2)、mixed-(1,1)+各側一unary：原a5/b6、兩側spokes01先作具名入口。
保留R_C(x,y)、R_U(u)、R_V(v)及同框(a,b,x,y,u,v)完整joint，分清shared x與不同contacts。
該型尚未分析；其他(2,2)、較少spokes、(5,5)、多mixed/no-mixed/非相鄰等仍保留。
共同epsilon>=2不變；epsilon>=3、新Lean theorem、一般出口、來源實現及K∞=K≤5未證。
```
