# 2026-10-03：四-spoke (2,2) 共用原 pair 的 sealed mixed 窄排除

基準 `b63a0965434d68a28292994638b2c98e848585b8`，cwd=
`/home/ray/developer/ai/math`。保留前序 singles／binary／star／hubs／
ternary／quaternary 未提交成果，接續使用者交接的 (2,2)、mixed-(1,1)
加各側一原單接點 unary。本輪未要求亦未執行 commit／push，沒有
重開來源圖枚舉。

## 窄結論與保存範圍

[新報告](../c5_excess_two_mixed_core_four_spoke_equal_pair.md)／
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py)／
[joint helper](../../scripts/c5_excess_two_four_spoke_equal_pair_joint_controls.py)
完成原共用 spoke-pair 排除，含指定 a5／b6、spokes=01／01 及 root
交換。原 diamond 的 crosscuts 迫完整 C 位於某個原 a–b–框點三角
內，全部實際 boundary 支援只在該框點；既有三-hub Gallai 引理
延拓每份合法三角染色，保留同一完整 R_C(x,y) witness。接原 G−C
全收，得到 G 全收，與固定候選 Σ 矛盾。外部 degree-list 講義
Lemma 7／Theorem 10 已核對；局部連通 triangle hub 的 K₄-free
前提亦紙面銜接。沒有四色定理 oracle或新 Lean theorem。

933／941 原 (2,2) 具名必要 skeletons 有 47／75 份；相同 pair
排除 7／9 份，**unequal pair 仍有 40／66 份，整個 mixed-(1,1)
加兩 unary 子型尚未完成**。原 01／01 indices=96／132，下一
具名 01／02 indices=97／133，root 交換=111／153。
保存原 edges、apex rotation、16 次 root 交換及 1,600 次整體 D₅／列
搬運。另有全部 diamond 的 80 份 rotation assignments／40 spherical
rotations；任意原嵌入結論由紙面 crosscut 承擔，未宣稱骨架實現。

三-hub 舊數學 payload 唯讀重算相同（1,201 份接線／28 份拒絕），
112 份返回原 C₅ 的 K₅ skeletons 保存所有 bags 及十對來源邊。
這些 general three-hub controls 不滿足選定 (1,1) degree-5 來源預算，
未混稱完整來源圖；其餘 36 張手列完整 degree 圖保存全部原
C／U／V、附件、兩 unary ownership、shared／distinct contacts 與十列
witnesses。七種原省略身份共 2,520 joints／40,320 pinned fibres、
1,800 原邊接回及 1,260 完整 root 交換核對相同。完整 degree 圖只
驗證 relation 身份，不宣稱 disk、Σ-critical、候選或 sealed geometry。
原 marginal 假允許／guarded fibre 空及接回 spoke 後 joint 全空的
負控制均保存。

## 實際驗證與產物

新層預設 seed 及 PYTHONHASHSEED=17 的逐 byte 重播均通過；既有短支援
checker 亦重播通過，沒有覆寫舊產物。實際執行：

```bash
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py record artifacts/c5_excess_two_mixed_core_four_spoke_equal_pair/observations.json
python3 tools/artifacts.py status
git diff --check
```

`lake build` 通過 8,831 jobs，只有既有 AttachmentOrder／SymRelabel
linter warnings，沒有新增 Lean theorem。文件檢查通過 499 份 Markdown／
5,114 個本地連結；DocGraph 通過 62 documents／213 relations／5 families，
零 errors／notes。產物 status 為 `ok=132`，無 missing／changed／stale，
`git diff --check` 通過。這些檢查不形式化本輪紙面 Jordan／Gallai 合成。

新 observations 為 **29,991,464 bytes**，SHA256
`426870ac0f7c2ec60090f82ba3c759457e157d4317b6ce63a9456b2bcb4a95de`。
依大型產物政策留本地，MANIFEST 記錄 digest、producer 及 source 依賴；
目前記錄 132 份大型產物／127 producers。本輪只 record 這份新 artifact。

原 single-spoke 的三份 docs hash 漂移維持，新 observations 記錄原
source digest 及漂移，舊 artifact 不覆寫。原 single-spoke 完整数學
payload audit 沿用前序 ternary 紀錄，本輪未重播其歷史 byte-check；
更前序 two-two docs hash 漂移亦保持。本輪不重跑 G−C 全收、舊
K₄、quaternary／ternary／其他四-spoke、R-series、來源 catalogue、
weak-deletion 或 Lean axiom audit 的全部歷史證書。

HANDOFF 的線及進行中 tags 保持，依治理規則仍是薄索引；README、
Kempe 導覽、STATUS、全線整合及前序 quaternary 的後續指向更新。

## 停止點與貼用摘要

```text
cwd=/home/ray/developer/ai/math；先讀docs/HANDOFF.md、docs/STATUS.md、
docs/c5_kempe_guide.md及docs/c5_excess_two_mixed_core_four_spoke_equal_pair.md。
保留b63a096與前序工作樹，本輪未commit/push。
推進四-spoke(2,2)、mixed-(1,1)+U-at-a/V-at-b，每unary一原contact。
原01/01入口及全部相同spoke-pair已排除，含root交換。
原diamond/crosscut封完整C在一個原(a,b,bh)三角；N_B(C)只可能含bh。
每份合法原三角染色由degree-list/Gallai及既有三-hub K5引理延拓整份C。
與同一原G-C全收接合，迫G全收，候選來源矛盾；不取marginals或獨立色框。
933/941原47/75份(2,2)必要框架，排除7/9，仍保留40/66 unequal pairs。
整份(2,2)、mixed-(1,1)+兩unary尚未完成；相同pair排除不外推全部型。
80 diamond rotation assignments/40 spherical；16 root swap/1600整體D5列搬運。
舊三hub1201接線/28拒絕payload原樣重算相同；112原K5 skeleton controls。
36完整degree圖；2520全圖joints/40320含空fibres/1800原邊恢復/1260 root swaps。
完整R_C(x,y)、R_U(u)、R_V(v)與(a,b,x,y,u,v)六角色joint/witnesses保存。
x=y只是一個原頂點；GC投影保留(a,b,u,v)。完整圖不聲稱disk/候選/criticality。
重播：PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_equal_pair.py --check。
新層兩個seeds與舊短支援byte-check通過；lake build=8831 jobs。
文件499 Markdown/5114 links；DocGraph零errors/notes；產物ok=132；diff --check通過。
新產物29991464 bytes，digest與producer記於MANIFEST；所有舊artifact保留。
原single-spoke三份docs hash漂移及更前序two-two漂移維持，未覆寫舊證書。
下一具名入口a5/b6、spokes01/02，source indices97/133，root交換111/153。
保持同圖原C/U/V、所有附件/actual supports/ownership/環序/同一色框。
先分析原C所在face的實際支援包絡，本輪不擴展分析該新入口。
共同epsilon>=2不變；epsilon>=3、新Lean theorem、一般出口、來源實現及K∞=K≤5未證。
```
