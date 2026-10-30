# 兩輪差異附件分隔：證據與驗證

2026-10-30。權威前提、紙證與 OPEN 邊界見
[附件分隔報告](../../docs/c5_d2_attachment_separation.md)。
新引理排除至多五附件的差異分量；本目錄沒有合法全封鎖四週期見證。

## 同源資料

- [controls.json](controls.json)：完整原圖／面／輪轉／O、所有字面 fibres、完整 Kempe 分量、真交換與全域正規化。
  所有來源檔案的 SHA-256 在 `provenance_inputs`；n17 使用上游保存第 0 份原 rotation，沒有重跑圖分類。
- [separation-certificate.json](separation-certificate.json)：每 Q 全部原鄰點、原面、附件、輪廓、R 與其含 Q 面 W、原簡單分隔環、全部固定五環及當下完整 O 分量接合。
- [review-certificate.json](review-certificate.json)：不匯入 producer 的獨立重播，記錄輸入、producer 與 checker SHA-256。

| 控制 | 最小度五／S34／S5 | ABACD fibre | 完整 O 字面染色 | Kempe 商態 | 真交換 | 比較 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| n17 原第 0 圖、v=2 | 是／是／是 | 8 | 1,296 | 54 | 10 | 1 |
| Errera | 是／是／否 | 12 | 2,400 | 100 | 20 | 4 |

每源的全部 1,024 個字面 B 字均被保留：240 個 proper B 字逐列保存完整 fibre 的
共同 S₄ lift 引用，實際空列為 0；其餘 784 字由原 B 邊直接判空。
獨立的完整 O 原邊著色枚舉逐份等於全 Kempe 商態的 24 個共同 S₄ lifts。
兩源皆只有一個完整 Kempe 分量，且均含三色框。

獨立 checker 核五份差異輪廓、五份附件內原簡單環、145 份固定原五環比較；
其中 n17 有 33 份，Errera 四次各 28 份。
共三個不同 Q∪A 工作區、60 份完整色態快照，每份六色對，合 360 份當下接合等式。
每次都重新計算完整 O 分量、工作區局部分量與遠端全部附件；
checker 以局部分量的 union-find 接合，另與完整 O 的投影比較。

n17 的 Q={12,16} 接固定原無弦六環，兩側 2／9 點；原 collar 有兩缺口且為固定七環。
第三輪第 3 步碰框三點，h³ 未定義；一次另選真交換即可到三色框，故未封鎖。
Errera 每次比較均重現外層固定原 w 五環包住差異、兩開側各六點，核實 S5 失敗。
這些控制不反駁全封鎖且 H⁴c=c 的候選命題。

## 已執行重播

```bash
python3 -B scripts/c5_d2_boundary_controls.py --check
python3 -B scripts/c5_d2_separation.py --check
python3 -B scripts/c5_d2_separation_review.py --check
python3 -B scripts/c5_period4_s5_replay.py --check
python3 -B scripts/c5_period4_face_constraints.py --check
```

以上通過；上游完整 12–24 點搜尋沒有重跑，既有分類結果未當作本輪新的全域證明。
沒有新增 Lean theorem，未執行 Lean build。

## 文件傳播與檢查

Closure scope：附件分隔引理及所有至多五附件差異核心排除；六點以上分支保留。
Canonical source 為上述報告，Evidence 為本目錄三份 JSON 及三個可重播腳本。

Updated：S5／週期四原報告新增下游連結，Kempe guide 增加閱讀入口，STATUS 增加新報告索引。
Reviewed-unchanged：HANDOFF 研究線未變；來源封鎖報告的偶週期、fibre 下界及父命題 OPEN 沒有改變。
Propagation stop：L2，原父 P₄ 仍 OPEN，不向其他研究線或 README 擴散。

`python3 scripts/check_docs.py` 通過（802 份 Markdown、10,710 條本地連結）；
`python3 tools/docgraph --include 'docs/**/*.md' check` 通過（98 文件、386 關係）。
`git diff --check` 通過。

全工作樹 `python3 tools/docgraph check` 仍失敗：72 errors，含歷史 frozen audit 與
scratch 複製文件的重複 ID，例如 `c5.adjacent-degree5-interfaces` 同時出現在
正式 docs、`audits/2026-10-09-n45-pc/source/docs/` 及
`scratch/task-c44-delivery/repository/docs/`。本輪新報告沒有 DocGraph ID，
未刪除或改寫這些歷史來源；正式 docs 通過不代表全域通過。
