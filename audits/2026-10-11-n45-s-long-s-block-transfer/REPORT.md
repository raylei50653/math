# N45-S-LONG-S-BLOCK-TRANSFER

2026-10-11。任務 D。共同 BASE `f2692089ad4259808e27d9b7e882ac09505b180a`。
**全部成果待獨立驗收。**

本輪完成任意大小 actual C block-tree 的精確完整 assignment recurrence，及五個预宣告
microcases 的具名介面校準。restriction／union 在 actual cutvertex 同色接合，是所有原
proper assignments 的雙射，保存完整原頂點、ordered/shared contacts、全部 tuple
preimages、r 色與空 fibres。這是輔助 transfer 交付，沒有新增任何 schedule 的來源排除。

## 證明及量詞

[transfer-proof.md](transfer-proof.md) §2–5 給出原 bridge、任意長 odd cycle 的完整局部
assignment 規則，及 all-original-vertex/block incidence tree 上的 recurrence。原 r 保留
兩個 odd-cycle blocks，L/S 的全部原旁支繼續按實際分塊展開。每個原 attachment unary
constraint 在對應 vertex node 核一次；union 與全 assignment 的 restriction 互逆。
不使用 finite-template compression，也不以存在性或可用色集合替代完整介面。

任意大小 recurrence 只假設 actual decomposition 與字面附件；degree4、disk topology、
K11/K12 不是這個接合恆等式的前提。要把 supplied graph 稱為本題來源，仍须獨立建立
全 K1–K12，尤其原 G 各邊的 Σ-critical witnesses 與 **X 自己每條 retained 非框邊的同 β
完整刪邊 witnesses**。本輪未供這些來源 witnesses。

每個共同 literal γ，certificate 保存全64 ordered `(u_L色,u_S色,r色)` ambient cells，
及全部16 ordered `(r,s)` pins，diagonal 與空 cells 皆在。每份 preimage 是包含全部原 C
vertices 的完整 vector；任一其他 ordered r/s contact tuple 的全部 preimages 可直接由
這些完整 vectors 分組取得。shared contact 仍是一個原 vertex，其不同角色讀同一座標。

若另供同一原來源的 actual U 全 preimages，完整 X 接合恰為

`literal s-spoke factor × Λ_C(γ;a,b) × actual Λ_U(γ;b) × Col^I`。

原 rb4 只加 `a≠γ(b4)` 的完整 filter。q0/q1/q4 用色2、q2/q3用色1，五份 T4 亦按
literal 最後一位；不能借未用色。跨列搬運須作用於同一 actual piece 的所有原座標與
attachments，保持相容 pins，返回共同 literal 框後才能接合。證明 §6–8 明列全部條件。

## 權威與採納

工作第一個動作是只讀核派工包，通過。本輪 HEAD 是指定 BASE；更早 BASE 只作歷史
provenance。完整 K1–K12、已採納 review REPORT／acceptance／corrections／fibre-paper-review，
原 B REPORT §§2–9 及 obligations 都已讀。原 B pending bytes 沒改；採納範圍以封存 review
更正附錄為準。三十 queries 分類使用 **12+4+10+4**，SF-RESIDUAL 依賴補列
**SF-T2-Q0-Q1-RESTORED**。

[inputs.json](inputs.json) 分列12 BASE Git blobs、11 sealed audit SHA256 inputs，以及
继承的 external theorem pin。封存 review 的 `git_blob=null`，不聲稱它在 BASE 中。
本輪 recurrence 不依賴 external Gallai theorem；該 pin 只標記來源 block 結構的繼承背景，
本輪未重新抓取 PDF。

兩個指定 observations 路徑的 `git show BASE:path` 都 exit128，原 stdout／stderr／exit
保於 `logs/missing-0.*` 和 `logs/missing-1.*`。finding 保留，不讀 physical／quarantine
資料替代，不執行依賴缺 blob 的有限重播；紙面恆等式與本輪具名 C 校準可繼續。

## 預宣告 microcases 與 degree 校核

[cases.json](cases.json) 在染色計算前固定全部五個名稱、原 vertices／edges、blocks、
attachments、ordered contacts／ownership、L/S、rotation 及三種 s-spoke factors。
上限8 cases、每案11個 C vertices；本輪實際最多7點。

| case | C 點數 | 原 block 形狀 | 判定 |
| --- | ---: | --- | --- |
| TT5 | 5 | r 上兩 triangles | degree4介面有效 |
| T5_7 | 7 | r 上5-cycle＋triangle | degree4介面有效 |
| BRIDGE_BAD6 | 6 | r 上兩 triangles，l0 有原 bridge 旁支 | 保留失敗：l0 為3＋2＋0=5 |
| BRIDGE_FIX6 | 6 | 新名稱更正上案 l0 的附件，原 bridge 旁支保留 | degree4介面有效 |
| NONROOT_CYCLE7 | 7 | r 上兩 triangles，非根 l0 有原 triangle 旁支 | degree4介面有效 |

[degree-audit.json](degree-audit.json) 逐原頂點列 `deg_C(v)+|N_B(v)|+1[sv∈E]=4`。
r 在 C 中 degree4，沒有 retained r-spoke；恢復原 e 後原 G 的 r 是degree5。
有效 cases 的 C−r 恰原 L/S，r contacts 各兩點，actual supports 是L234／S40。
S 是兩點原 piece；未預設單頂點。rotation 有原鄰接的 cyclic 資料，**未驗 disk topology**。
microcases 只供 C fragment，不供 actual U／全 G；不建立 Σ-critical 或 X 同β minimal。
BRIDGE_BAD6 未刪除，失敗 finding 同時保在原 case、degree audit 與 certificate。

## 完整介面校準與負控制

[transfer.py](transfer.py) 從原 edges 另核 actual biconnected blocks，再按紙面 recurrence
接全部 assignments。[direct_enumerator.py](direct_enumerator.py) 只用標準函式庫，沒有
transfer/checker imports，直接枚舉原邊與原 attachment inequalities。[checker.py](checker.py)
唯讀比較這兩套算法及 [certificate.json](certificate.json) 的每一完整欄位；沒有 target search。
不加 `-B` 的 checker 也在 local imports 前關閉 bytecode 寫入。

| 已執行介面控制 | 結果 |
| --- | --- |
| 四有效cases×十literal列，完整原assignments | 40列／1,344 assignments；triggered and holds |
| 全 ambient tuple/r fibres | 2,560 cells，1,966空；triggered and holds |
| 全16 pins／每列三種 literal s-spoke factor | 640 pins／1,920 factor-filtered pins；triggered and holds |
| 原 rb4 filter、r contacts/shared座標、原 bridge/cycle 旁支 | 全preimages逐項相等；triggered and holds |
| 普通／seed17唯讀重播 | checker及direct各自stdout/stderr byte相等；triggered and holds |
| 非空自由孤立因子 | 有完整紙面Col^I，finite未供非空I；not triggered |
| actual whole-X/G、K1–K12 target source | executed=false，trigger_count=null；not triggered |

三份原負證書、[negative-plan.json](negative-plan.json) 與六次 native rejection logs 全留。
checker 和 independent direct 分別均 exit1，指出以下 named cell／原頂點：

| 指定負控制 | 失敗證書 | 精確拒絕位置 |
| --- | --- | --- |
| 改一份完整preimage的r色 | negative-r-colour.json | TT5／01012／tuple(0,1),r=2；原r從2改3 |
| 刪一個空ambient fibre | negative-empty-cell.json | TT5／01012／tuple(0,0),r=0，empty |
| 漏一個原旁支 | negative-missing-branch.json | BRIDGE_FIX6／原l2（原bridge l0-l2） |

這些 expected rejection controls 是 **triggered and holds**；BRIDGE_BAD6 是 degree4 前提的
**counterexample**，不是 K1–K12 來源反例。未宣稱或測試新的較強 cross-row fibre lemma，
因此沒有將抽象 relation 反例提升為來源反例。

## 完整必要域與停止點

[coverage.json](coverage.json) 列全部24 assigned necessary schedules、38 actual s-spoke
變體、各完整Δ、十列和全部16 pins（6,080份符號 pin 義務）。這些數字不是來源圖數，
不计完整幾何數目。四個歷史恢復排除 schedules 另列其已採納依賴；沒有新採用同批其他
worker 結論。每案 concrete source relations／preimage counts 都是null，未捏造來源資料。

剩餘來源的 precise OPEN fibres：對 `γ∈Δ`、`a≠γ(b4)`，若 literal s-spoke factor為1且
actual `Λ_U(γ;b)` 非空，真來源要求所有避b的完整 `Φ_C(γ;τ,a)` 空。排除還須在同源上證
其中至少一個這樣的 fibre 非空，或抽取同源原邊 minor。recurrence 提供完整介面，沒有
給出該非空性。具名 residual 是 **same-source-Delta-restorable-r-fibre-nonemptiness**。

紙面恆等式完成；finite僅具名transfer校準；target source未建立／未執行；source
realizability、Lean、一般N45/N2/E仍未建立。完成本窄域後停止，等待獨立驗收。

## 原生重播、custody 與工作界線

正式命令的完整argv/cwd/env、分流stdout/stderr、exit在 [checks.json](checks.json) 與 `logs/`。
最小唯讀重播是：

```sh
python3 -B audits/2026-10-11-n45-s-long-s-block-transfer/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-n45-s-long-s-block-transfer/checker.py --check
python3 -B audits/2026-10-11-n45-s-long-s-block-transfer/direct_enumerator.py --check --certificate audits/2026-10-11-n45-s-long-s-block-transfer/certificate.json
```

初期內部分工的help／in-memory smoke、structural／文字核對使用tool-call capture，原命令
及工具當時實際傳回的資料保留於 `*-agent-*`。原生事件取回了完整輸出與exit；各記錄仍明列
merged output與未分流stdout/stderr的限制，不補造分流streams。所有正式生成、校準、普通／seed17、
負控制與根agent的完整obligations核對都有已知exit；正式有限控制使用native subprocess
分流capture，沒有重建歷史輸出冒稱原生。

前後snapshot核1,204份protected authority／舊交付／原輸入；新增certificate後另核1,205份。
changed=[]，HEAD及tracked diff相等，certificate零漂移。沒有重跑上輪19 controls。
[local-review.md](local-review.md) 是本任務內部只讀審查，不能代替獨立採納。
最終 [delivery.json](delivery.json) 列精確檔案inventory／SHA256，只排除它自身的自參照hash。
只新增本專屬目錄；共享docs、原交付、其他worker目錄與舊證書均未修改。
沒有commit／push／PR／外部訊息。**成果仍待獨立驗收。**
