# 同候選外側、較小 bad 嘗試與三候選計數障礙發布

2026-10-18；研究及提交父 BASE `e1617a2756813327d7ad333cfdd0fd92fa9efc38`。
使用者授權整理目前進展並 `commit + push`。本次相連交付三輪研究 audit、
Kempe 導覽、STATUS 及本發布紀錄。原報告的「未 commit／push」保留研究輪語境；
本發布輪的驗證另記於此，實際提交與遠端狀態以 Git 為準。

## 已完成的進展及適用範圍

[同候選原外側](../../audits/2026-10-18-rainbow-exterior-e1617a2/REPORT.md)
在原 b 四度的四個具名兩星位置，原 `01202`、`01212` 皆拒絕時，
證同一 fan-A 的完整集合雙射
`F01232 ≅ F01202 ⊔ F01212`。因此接受 fan-A 後排除三個指定負 fibres
的選路不可行。fan-B 的必要連接保留同一份完整著色中的原外側分量；
不同查詢的路徑仍不得合併。

[較小 bad 構造嘗試](../../audits/2026-10-18-smaller-bad-e1617a2/REPORT.md)
在完整 r6 來源的原 `(p,h)=(p,ell)` 位置，以實際空面的共面識別構造
Q1、Q2，均保原有序框且完成為 k−4；與既有 k−2 的 fan-B 共同保至少
一份原 `01232` 完整著色。原外側八圈、全部局部 lifts、空 fibres 及
Q1／Q2 的精確回填條件均已定位，但合法性與接受覆蓋本身不給出保壞。

[完整計數障礙](../../audits/2026-10-18-smaller-bad-counts-e1617a2/REPORT.md)
使用同一外側的任意大小平面計數張成、必要 Kempe 零座標及精確有限矩陣，
證原支持 932／933 時三候選各有 `N01232 ≤ 4 N01212`。
932 的三個非負整數參數給七種完整支持型態，三張固定候選全部在 K132。
實際分量交換的共同單射另排 932／933 兩商圖的 `01021`，並與計數及接受覆蓋合用，
證 932／933 的原 h=b 接受扇區非空，故 fan-B 接受且必洩漏 `01212`。

**尚未構造較小 bad，也未完成 `bad → success ∨ smaller bad`。**
932 必須換實際構造或直接推原來源矛盾；933 的指定四列合同已排除，
其他完整支持證書仍可研究；941 的同一接受候選三負 fibres 排除仍 OPEN。
必要計數錐與 941 的各候選可行向量都不是原外側實現，不能拼接成同一來源。
普遍位置存在、完整319、`W110+W101>0`、`omega_e=0` 及一般閉合仍 OPEN；
一般 K≤22 與固定 r6 的 k≥25 不變。本次沒有新增 Lean theorem。

## 封存與文件傳播

三 audit 分別 31、53、122 份檔案，合計 206 份、9,406,940 bytes。
[發布 custody](2026-10-18-smaller-bad/audit-custody.json)逐份記錄大小及 SHA256；
本發布不改任何 audit bytes。三輪的 INPUTS、OUTPUTS、完整 fibres、負控制、
交叉審查與研究輪收據一併交付，沒有新增超過 1 MB 的檔案或產物政策例外。

Updated：Kempe 導覽的最新進度、分支停止點、里程碑及 STATUS 直接索引；
舊里程碑補明 932／933 已有後續接受且洩漏結論。
Reviewed-unchanged：原雙 fan 合法性、完成成本、共同接受覆蓋及四列保壞接口
仍有效；README／HANDOFF 的閱讀入口、研究線及進行中標記無須調整。
傳播停於直接父題與本線導覽，未將選路排除升為來源排除或父命題收尾。

## 本發布輪驗證

三個根 checker 均實際重跑通過，核對凍結輸入、完整 lifts、必要閉包、
共同投影、精確計數及污染負控制。原固定圖未觸發來源拒絕前提的部分仍為
`not-triggered`，不作原最小來源的存在或排除證據。
`lake build` 通過既有 8832 jobs，保留既有 linter 警告；94 項工具測試通過。
這些檢查不把本輪紙證或 Python 有限線性代數升為 Lean 形式化。
獨立 SymPy 重播核對全部 1430 個非交錯分割、秩 91、剩餘維度 3／18／44，
以及完整字面投影與 932／933 的精確恆等式，均通過。
全部 206 份 audit 與 Git index 的 SHA256 相符，58 份 JSON 可解析，
四份 OUTPUTS 的 118 條雜湊均一致。

```bash
python3 -B audits/2026-10-18-rainbow-exterior-e1617a2/check.py
python3 -B audits/2026-10-18-smaller-bad-e1617a2/check.py
python3 -B audits/2026-10-18-smaller-bad-counts-e1617a2/check.py
uv run --with sympy python -B audits/2026-10-18-smaller-bad-counts-e1617a2/A/review_c_final.py
lake build
uv run --with-requirements requirements.txt python -B -m unittest discover -s tools/tests -p 'test_*.py'
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/check_generated_artifacts.py
git diff --cached --check
git diff --cached --check -- . ':(exclude)audits/2026-10-18-smaller-bad-counts-e1617a2/routing.diff'
```

完整命令、exit codes 與輸出見[發布檢查收據](2026-10-18-smaller-bad/final-checks.json)。
正式文件及 scoped DocGraph 通過；Git index 產物政策通過，沒有新增例外。
全 staged whitespace 檢查 exit 2：唯一來源是封存 `routing.diff` 中 13 條
帶空格的 unified-diff 空白 context 行。保留其原始 bytes；僅排除此一封存檔
的 whitespace 檢查通過，完整失敗輸出保留於收據，不宣稱全 staged 通過。
正常／seed17 一致性沿用三輪未改 bytes 的原 `checks.json`，本次不重跑 seed17；
未重跑先前原圖及局部 patch 枚舉。whole-tree DocGraph 未重跑，歷史凍結副本
重複 ID 的既有失敗保留；本次正式 docs scope 的結果另記，不宣稱全樹通過。
