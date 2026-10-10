# N45-SU-J：S／U 固定圖與抽象介面的獨立有限增量核對

2026-10-09。任務：[凍結任務全文](../2026-10-09-n45-s-supervision/cross-audit-tasks.md)。
BASE 與本輪實際 HEAD 均為 `dc8e9aa7d6fccb51f63d30aa3f9c132296d44744`。

**裁決：指定有限證據通過，未見阻斷其有限 payload 的 finding。**
精確目標 N2 來源仍 **not triggered**，沒有來源反例，也沒有新增來源排除。
本報告不裁決 S-01–06 或 U 任意大小 paper；其正式採納仍需 SU-A／監督端。
只新增本目錄，自行完成，未委派、commit、push、開 PR 或對外發訊息。

## 1. 凍結、版本及獨立性

先核 Git、BASE HANDOFF／STATUS／DOCUMENTATION 及任務共用前提。
共享 STATUS、Kempe guide 和歷史派工檔是既有未提交導航；不作數學來源，也未修改。
數學 bytes 由 `git show BASE:path` 核對；另將 `git archive BASE` 解出到本目錄
[base-source](base-source/)，供固定圖重算及 fresh BASE 文件檢查。
這是沒有 `.git` 的 BASE archive，不稱 clean checkout；S 重播中的 HEAD 由父工作樹提供，
其 69 份實讀來源另外逐 byte 對 Git objects，不能單憑這個 HEAD 認證 archive。

來源驗證：[inputs.json](inputs.json)、[initial-state.json](initial-state.json)、
[fingerprints.json](fingerprints.json)。S 69／U 70／J 66 項 manifest 對 BASE 相符，
去重共 71 個權威路徑；原來源副本的 bytes／mtime 亦保留並前後核對。

| 凍結項目 | 核對結果 |
| --- | --- |
| S delivery | 精確 21 項 inventory／bytes／SHA256 全符；含 delivery 本身共 22 檔 |
| S delivery 自身 | SHA256 `fbaaa3540d4a1488211ab32bc466d76ebc8b51b09e47dc69f6362f5c94453808`；另對監督 inputs 中的凍結值 |
| S supervision inputs | SHA256 `05266330c39e2b937a56c732276bb1b42a40b3c83988a28f3a7ac9cb2b990514` |
| U authored | 批次 supervision inputs 凍結的 39 檔精確 inventory／bytes／hash 全符；source 分列，初版、failed attempts、routing drift logs 全保留 |
| batch supervision inputs | SHA256 `e70f233eb99d8d1adaa6868680c5dfc2f1469fcf335c7c6706153bb53344ce8e` |
| J manifest | 89 項精確 inventory／hash 全符；含 manifest 共 90 檔 |
| J certificate | SHA256 `ecdef656ec2eff887c6725cda21a6d205fce41e5387ce14b2270468f20a861d4` |

S／U REPORT、checker、certificate、inputs 均匹配共用任務頭的八個精確 hash。
本轮没有修改上述原檔或原證書。

讀完 S／U checker 與 J 完整介面後，另寫 [checker.py](checker.py)，
只用標準函式庫，不 import／執行 S、U、J checker 或 supervisor review 決策。
固定圖先由原 edges 重建 contacts／shared identity／ownership／attachments／support、
bridges、rotation、faces 及 shields；局部完整染色先枚舉，才投影 contact tuples。
整圖 solver 使用 bit domains、singleton propagation 與完整解枚舉，再分組全部 16 root pairs；
saved tuples／fibres 只作比較，沒有替換成 marginals。
全部 literal β、原具名頂點與空 fibres 保留，U 的 X 與 G−rx 使用不同 vertices／edges／full lifts。

本獨立 certificate 生成及普通／seed17 重播完成後，才讀兩份 supervisor review.py／results。
[supervisor-comparison.json](supervisor-comparison.json) 的 18 個有限欄位全部一致，語義差異 0。
新增重算比原監督核對多核完整局部 relation、容量生成、critical edgecuts 及全部新 γ 投影；
沒有因此扩大图族或採納其 paper 決策。

## 2. CLAIM 裁決及量詞

所有 CLAIM 的證據層均為**有限 Python**；共同依賴為 BASE 原 edges／cells、凍結 S／U／J
證書及本獨立 solver。每列的量詞只及所列固定域，不及任意大小圖。
圖域的共同前提是具名 induced ordered C5、原 degree5 roots 且 χ=0、其餘 private degree4、
原 planar rotation／唯一 C5 外面，以及原 H−roots 分量；從原邊核這些前提。
不預填完整 target Σ、45／54 β-minimal core 或來源實現。

| CLAIM | 完整有限量詞／前提與裁決 | 未涵蓋範圍／finding |
| --- | --- | --- |
| SUJ-01 | 對每個 c∈4、k_r,k_s∈{1,2,3}、8 個 S3 軌道聯集，重建全部 16 pairs；假設 diagonal 全接受，只按雙向 contact 界判定：92 triggered and holds、196 not triggered。12 個低總 incidence 且界成立者全為通用 relation。 | 這是抽象軌道域，沒有具名 graph、full B-touch 或 N-diagonal 的來源證明；SUJ-F03。 |
| SUJ-02 | 3 個指定 abstract models 的 P／Q 全部 16 pairs（含空 pair）、4 個容量欄及 blocker 二分均相同；逐欄五項零 slack。12 個 incidence scalars 留 (2,2)/(2,3)/(3,2)。933／941 的完整 Q(X) 必要表吻合。 | 模型缺 graph／full lifts／Σ-critical／target Σ／minimality；不宣稱 disk 實現；SUJ-F03。 |
| SUJ-03 | 恰 19 個原 N2、190 個 full-Σ rows、3040 pins 與 J 完整 fibres 相同；47 個原 spoke×原拒絕 row derivatives、752 pins 與 J 相同，S 的 218 個保存 full lifts 全合法。所有新增接受 lifts 的刪 spoke 兩端同色。 | 47 全接受，目標省略來源 not triggered；不是一般 S paper 驗證；SUJ-F02。 |
| SUJ-04 | BASE 54 圖的 supplied core edges 重算 degree fields：N2 保存 cores 全 55，12 個 45／54 occurrences 全 N1。有限審核不把它們搬成 N2 正控制。 | 沒有重枚舉 minimal cores；非拒絕 derivative 不觸發 degree4 容量式；SUJ-F02。 |
| SUJ-05 | 本獨立 checker 及原 S／U／J 各普通、seed17 只讀重播均相同；本 certificate exclusive-create，對既有檔生成被拒絕。原 S22／U39／J90 檔及 BASE 來源前後 bytes／mtime 零漂移。 | 只讀 verifier 之外的原生成／整體 driver 未重跑；保留原 failed attempts；無 paper／Lean 結論。 |
| SUJ-06 | 固定 23 圖＝19 N2＋4 N1：3680 original pins、11 整 U omission 的 1760 X pins、1760 G−rx pins 完全相同，包含全部空 fibres。每個 X／G−rx root-pair 集合相等，完整 vertices／lifts 分列。 | 7 個 N2 整 U derivatives 全 Σ1023；不能當 N2 45／54 正控制；SUJ-F02。 |
| SUJ-07 | 690 個 piece-row relations、2802 個 distinct contact tuples、11040 fibres 與 J／BASE／U 相同；全部 2986 piece lifts 重建吻合。11 個新 γ 的 U palette 與所有 X lifts 的 r 投影同 singleton；38 個 F 空列是過強說法反例。 | F 空反例只反駁「每列 F 必 singleton」，不是目標來源反例；SUJ-F01。 |
| SUJ-08 | 原 G90／X12 共 102 欄重算五項非負及左右值；4 個 N1 低度側 X 全五項 0，恢復 U 後全 λ placement。22 個低 incidence、one-sided、full B-touch 支援 instances 滿足支援≥2。 | D／O placement、N2 拒絕 X、singleton 反證分支缺控制；不代證無界 Gallai、U2、SHORT；SUJ-F02／03。 |
| SUJ-09 | 完整七格 target Q(X) 表（含933 q2）及15個非空 contact palettes 的 F 算術吻合。普通／seed17 後 S／U／J 與 BASE 输入仍無漂移。 | E2 必要表及 palette 算術不給圖實現／跨列同源排除；SUJ-F03。 |

## 3. 精確查詢數、空 fibres 與 full lifts

[certificate.json](certificate.json) 保存完整重建 payload；
[diagnostics.json](diagnostics.json) 分列 N1／N2、全部 F 空負控制與 core-edge inventory。

| 範圍 | 查詢數 | 非空 fibres | 空 fibres |
| --- | ---: | ---: | ---: |
| N2 original（19圖×10列×16） | 3040 | 882 | 2158 |
| N1 original（4圖×10列×16） | 640 | 154 | 486 |
| N2 整U省略 X（7份×10列×16） | 1120 | 320 | 800 |
| N1 整U省略 X（4份×10列×16） | 640 | 194 | 446 |
| N2 原 contact 刪除 G−rx | 1120 | 320 | 800 |
| N1 原 contact 刪除 G−rx | 640 | 194 | 446 |
| S 原spoke×原拒絕row derivatives | 752 | 97 | 655 |
| 原piece局部 pin fibres（690列×16） | 11040 | 9694 | 1346 |

U 的整圖域合計 7200 pins；S 的 3040 original pins 已包含在其中。
另加 S 的 752 derivative pins，共 **7952 個不同指定整圖 pin cases**，不重複加總原圖域。
每個非空整圖 fibre 保存一個完整 lift，local tuple 保存**全部** piece lifts。
新證書另保每個 fibre 的完整染色數，原 saved full lifts 以原邊和 literal pins 驗合法，
不要求另一個 solver 選中同一個見證。

S 保存 lifts 共218＝171原圖接受row＋47spoke接受row，全部通過。
U 原圖1036、X514及G−rx514個非空 cells 的保存 full lifts 均合法。
原圖555條非框邊的 fixed deletion Σ 也獨立重算，共5550框列接受性，
619份保存新接受 full lifts 合法；69個原piece critical-contact witnesses
的刪邊同色、outside lift、tight lists與避自身的原外路核對。
4份N1整U minimal rows的 retained-edge full lifts 合法；未重開上游core枚舉。

| 容量域 | triggered and holds 欄 | not triggered records（U計數法） |
| --- | ---: | ---: |
| N2 G | 74 | 171 |
| N1 G | 16 | 32 |
| N2 X | 0 | 70 |
| N1 X | 12 | 36 |
| 合計 G／X | 90／12 | 203／106 |

U 對接受join只記一份 not-triggered record；J 按兩方向記錄，不能直接拿兩者的
not-triggered 數互比。五項值、具名 column、E 域及 J 的逐方向 missing 前提均核對。
4個低度側 placement 是 NA8-0003/index0、NA8-0007/index3、NA8-0009/index0、
NA8-0010/index0，含 root交換；全部為 λ，原G向量(0,0,0,0,1)，X向量(0,0,0,0,0)。

19份N2的Σ分布為959×3、1021×4、1015×4、1007×2、1022×6。
重新共同搬運whole frame的D5目標mask：933像={933,934,940,948,996}，
941像={941,949,950,998,1004}；19圖均不在其內。
故精確 target source 0 triggered、source counterexample 0。
47份 S 查詢及7份 N2整U omission接受，不拿接受性當拒絕degree4等式的觸發證據。

## 4. Findings 與未覆蓋前提

- **SUJ-F01（已知負控制，非阻斷）**：過強的「capacity-one U每列F必singleton」被38列反駁。
  具名例 NA8-0003、P1={8,9}、contact=9、index3，palette={1,2,3}，F=∅；
  tuples及全部4份full piece lifts重建相同。影響SUJ-07及U-REL的過強版本，
  不影響原U允許F空的claim，不是target來源反例。
- **SUJ-F02（coverage）**：SUJ-03／04／06／08沒有N2精確933／941、拒絕45／54 derivative、
  degree4零slack或D／O placement正控制。N1的12個occurrences與4個λ instances另列。
  不接受用其填補N2 coverage；19圖無來源反例不證明一般来源不存在。
- **SUJ-F03（證據層界線）**：SUJ-01／02／08／09只有指定抽象／圖域。
  92個軌道contact界成立不同於graph前提觸發；3個abstract models缺source前提；
  22個支援instance沒有singleton反證分支。不驗無界Gallai、兩unary或SHORT排除，
  不給disk實現、完整同源跨列來源排除或Lean。
- **SUJ-F04（既有文件失敗）**：fresh BASE文件缺兩歷史目標及全worktree duplicate-ID
  FAIL保留，見§5；正式docs PASS不改稱全域PASS。
- **SUJ-F05（沿用的歷史provenance FAIL）**：原A／batch記錄的E4 core／reductions
  普通及seed17各exit1保留。來源E3 REPORT的historical sha `6d385639…` 與BASE
  `73ed652a…` 不同；此輪未重跑那四個上游命令，只讀原log及批次處置，
  不把S/U重播或本輪來源bytes PASS改稱該歷史certificate PASS，也未改其副本。

未見需要人工更改原 S／U／J 證書的 finite discrepancy；所有原證書保持原樣。
本輪停止於有限增量核對；S的LOW／HIGH／long、U唯一U＋long／short、原55、
一般N2及一般猜想E仍OPEN。未核S-01–06或U的任意大小paper；不以本報告關閉其子型。

## 5. 重播、文件結果及交付

本目錄的 [run.py](run.py) 將每個command、環境、exit、耗時、完整stdout/stderr
exclusive-create保存於logs；[checks.json](checks.json)彙總實跑命令與未跑理由。
普通及seed17的本獨立checker、原S、原U、原J共8次只讀重播均exit0。
J原工具的既有普通／seed17重播涵蓋其完整固定域（19N2＋6N1），
本輪新獨立U計算只用指定23圖，沒有以另外2個N1補本輪控制。

```sh
python3 -B audits/2026-10-09-n45-su-j/checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-09-n45-su-j/checker.py --check
python3 -B audits/2026-10-09-n45-s/checker.py --source-root audits/2026-10-09-n45-su-j/base-source --check
python3 -B audits/2026-10-09-n45-u/checker.py --check
python3 -B audits/2026-10-09-n45-j/checker.py --check
```

本独立checker SHA256 `032cbf899961fdb71253ff8f380711bc91a97d9dd3db245e63376bc9ef728f6c`。
新certificate為8023145 bytes，SHA256
`a4b5b4c148f823f8df22a2672700eb40516bae0fd673edf8210a477af3b508ee`。
`--check`完全只讀；對既有certificate重新`--generate`預期exit1／FileExistsError，
未覆寫。輸入与原交付bytes／mtime前後零漂移；初始Git既有變更完整保留。

| 檢查 | 實際結果 |
| --- | --- |
| fresh BASE `check_docs.py` | **exit1**：586 Markdown／6982 links，2個missing paths |
| 共享 `check_docs.py` | exit0：587 Markdown／7022 links；其留存歷史目標不在fresh BASE |
| BASE／共享正式docs DocGraph | 各exit0：62 documents／213 relations／5 families，0 errors／notes |
| 共享whole-worktree DocGraph | **exit1**：62 duplicate-ID errors；保留原scratch、U/source及本輪BASE archive副本，不刪副本把FAIL變PASS |
| tracked `git diff --check` | exit0；本目錄authored文字另核whitespace及report連結 |
| 原來源／交付與本獨立finite payload | 各PASS，與文件／provenance FAIL分列 |

fresh BASE缺的兩個目標原樣保留：
`audits/2026-10-04-task-d5/c4/scope_ledger.json`、
`audits/2026-10-04-task-d2/integration_doc_changes.diff`。
沒有補造旧產物，也沒有修改共享文件、原S／J／A／U目錄或上游artifact。

未跑E3／E4／E4C完整枚舉、ES／ER、U1–U4及其他新圖搜尋；它們超出固定增量域。
未跑lake build／axioms，因沒有新Lean且本任務不承擔形式化。
未稽核external Gallai原文／任意大小proof，由SU-A處理。
原有歷史失败及routing漂移保留，僅本輪輸入／交付的零漂移由本輪fingerprints證明。

完整輸出hash清單為[MANIFEST.sha256](MANIFEST.sha256)，含全部authored檔及5899份BASE archive檔；
manifest自身另見[delivery.json](delivery.json)。兩者自指／循環hash項明示排除，沒有隱藏輸出。
後續由監督端對回凍結版本，與SU-A紙面裁決分層決定S／U採納及下一個residual。
