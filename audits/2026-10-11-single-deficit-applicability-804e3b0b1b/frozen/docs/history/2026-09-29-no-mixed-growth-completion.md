# No-mixed 增長完備性與免表共同分離

2026-09-29，起始 Git `3174f088880392485aca53ffe46f01e80831243b`。
接手時工作樹已有 local-screen／no-growth checker、artifacts、報告、
歷史與 README／STATUS／導覽／前層報告變更，全部保留並接續。
本輪未開 sub-agents、未 fetch、未 commit／push，未更新 Codex 記憶。

專題證明見[增長完備性](../c5_no_mixed_growth_completion.md)，目前停止點
由 [weak-deletion 導覽](../c5_weak_deletion_guide.md)維護。

## 本輪結果與證據界線

完成交接的窄題：影響 root 可用色的 singleton→pair 增長，必被共同
守恆原路徑／非守恆原端點規則排除。結合前輪無增長定理，指定 p₁、p₂
的共同存在性分離已免查必要支援表證成。

紙面推導從同一 source 側跨度出發：正規化 target p₂ 後，增長支援必
含 b2 及 b0／b4，所在側只能是 A/B，且側弧只能為 234、1234、4012。
每種位置直接指定固定框弧及原外部路徑；守恆分支將 β 排至至多一個，
沿用整條原路徑 palette 交換收尾。非守恆有害 pair 以整個原端點聯集
排除；其餘 pair={1,2} 與 R={0,3} 不交，另一 root 可用色為 {3}。

保留原分量、具名 contacts、bridges／旁支、實際支援、共同環序及全部
完整關係。p₁ 的整列反射、source／target 各自的全域色置換與 target
root pair 逆像明列於報告及證書；不對分量分別選色框。

新 [checker](../../scripts/c5_no_mixed_growth_completion.py)／
[artifact](../../artifacts/c5_no_mixed_growth_completion/observations.json)
重播 2,240 個增長候選，固定配方排除 2,010、保留 230 個無害 pair。
11,096 joins 中排除 3,018，保留 8,078 全有異色 root pair，其中
7,848 無增長、230 無害增長。原 434 個失敗全部取得排除；AA54/p₁/j4
及 AB22/p₂/j4 保留原全路徑／非守恆端點機制。

較強前層篩選的 2,208 排除／32 保留不變。本輪多保留的 198 份亦不
影響 R，並非推翻原排除。由全搜框弧改成固定配方，唯一 β 收尾由
40 變為 246；沒有新增來源排除或 target 接受。

有限控制另有 384 個 pair 穩定子檢查、1,524 個原 minor skeleton
檢查。新 checker 不呼叫舊 local_rule／frame_evidence 搜尋器，也
不用原 target 接受／排除 flags 作判定；仍重用共同 lift 解碼、候選
搬運及 minor control 純函式。不是全部幾何引擎的獨立重寫。

任意大小依紙面 source／原路徑引理及外部 Gallai 定理。Python 僅作
固定域控制；未新增 Lean theorem／native_decide，亦未給從一份指定
source 染色出發的建構式 repair。來源實現、完整 Σ、一般出口、
較大 mixed 原分量及 K∞=K≤5 均保留。

## 實際驗證

```bash
python3 scripts/c5_no_mixed_growth_completion.py
python3 scripts/c5_no_mixed_growth_completion.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_growth_completion.py --check
python3 scripts/c5_no_mixed_no_growth.py --check
python3 scripts/c5_no_mixed_local_screen.py --check
python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 的一般及 seed=17 重播均逐 byte 相等，11 份既有輸入
SHA 前後不變，所有載入的研究 Python 模組 SHA 記入 artifact。
前層三份 checker 全通過，原 7,848 無增長 joins、2,208／32 局部
篩選及 root-transport 4,164 查詢／11,096 joins 均未改寫。

`lake build` 通過 8,827 jobs，保留既有 longLine、unusedSimpArgs
及 show tactic 警告。無 Lean 檔案修改，不表示新紙面幾何已形式化。

文件檢查通過 353 份 Markdown／3,589 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過；本輪新增 checker、artifact、報告及歷史另查
尾端空白與最終換行，全部通過。

| 檔案 | SHA-256 |
| --- | --- |
| `scripts/c5_no_mixed_growth_completion.py` | `ddccda74be870656b06fb682b11b0b92034afa992ec26ff56a4111c201a31719` |
| `artifacts/c5_no_mixed_growth_completion/observations.json` | `b5a96f34e323ac594dc382913414c88aef97dbbe8ad15b97347ddd39fa5096a1` |

未單獨重跑十五類完成 checker、三份舊 hypothesis checker、跨度／
root 預算 checker、mixed／唯一 degree-5 家族、雙拒絕 atlas、R 系列、
profiles／閉包或 Lean axiom audit。前層 annulus／原路徑紙面引理及
外部 Gallai 文獻沿用，未另重讀外部文獻。

新專題／歷史／checker／artifact 與 README、STATUS、導覽互連；
前四層報告加日期與後續連結，保留當輪未解敘述與數字。研究線及
進行中 tag 沒有改變，依文件治理不在 HANDOFF 堆疊成果摘要。
導覽下一窄題轉為較大 mixed 原分量的容量／必要接點化約，先讀完整
有序色對介面，不重新枚舉已完成 no-mixed 家族。

## 後續提交與推送核對

2026-09-29，使用者明確要求 `commit + push`。本次將 local-screen、
no-growth、growth-completion 三輪相連的 checker／artifact／報告／
歷史，以及 README、STATUS、weak-deletion 導覽和前層後續連結一併提交。
上文「未 commit／push」保留研究輪當時語境。

發布前已 fetch origin，確認起始 HEAD 與 origin/main 同為 `3174f08`，
沒有遠端分歧。重新執行四份 checker 的一般 `--check`，皆通過；
三份新 artifact 的全部輸入及 checker SHA 綁定也再次一致。
`lake build` 再次通過 8,827 jobs。不同 hash seed 的重播沿用本次
對話研究輪已通過的結果，未在發布輪重複執行；其他未重跑範圍同上。
文件／DocGraph 與暫存差異檢查於提交前核對。

提交後以 `git push origin main` 推送，再讀回 HEAD、origin/main、
`git ls-remote origin refs/heads/main`，並核對工作樹乾淨；最終 commit
及遠端狀態以 Git 與本次發布回覆為準，不將尚未執行的步驟記為通過。
