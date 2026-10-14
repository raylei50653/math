# 實際驗證與版本界線

2026-10-14。以本包 INPUTS.json 固定 BASE 與直接輸入；未重跑來源圖生成器、外部枚舉或 Lean build。

## 重播

從 repository root 執行：

```bash
python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_quotient.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_quotient.py --check
python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_structure.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_structure.py --check
python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_cap.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/check_cap.py --check
python3 -B audits/2026-10-14-c4-triangle-core-b66f592/controls/negative.py
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

## 證據版本

完整 fibre 的正常／seed17 重播通過，264份集合等式與全部空格一致。

結構初版 [check_structure_v1.py](controls/check_structure_v1.py) 及
[structure.json](controls/structure.json) 保留。審查指出它未檢查 T0 四接點交叉邊，
且只驗 dart／Euler／connected，未驗各頂點 link 單環。初版正常及 seed17
結果僅為這個較窄範圍的成功紀錄，不能當作完整 surface validator。
新版 [check_structure.py](controls/check_structure.py) 明確補齊兩項，採
[structure-v2.json](controls/structure-v2.json)，不覆寫初版 bytes。

獨立紙面覆核見 [review](review/INDEPENDENT.md)。最終逐命令狀態另列於下節。

## 最終實際結果

- 完整 fibre：正常／seed17 PASS，見 [正常](logs/quotient-check.log)、[seed17](logs/quotient-seed17.log)。
- 結構 v2：正常／seed17 PASS，10,895 個開口及新增缺邊／vertex link 檢查均通過；見 [正常](logs/structure-v2-check.log)、[seed17](logs/structure-v2-seed17.log)。
- [負控制](logs/negative-v2.log)：漏完整 fibre record、輸入 drift、覆寫既有證書、漏開口皆拒絕；原證書與 frozen source SHA 不变。兩份icosahedron識別两對頂點形成的非surface，初版接受、新版明確拒絕，資料與舊版行為均保留。
- [文件檢查](logs/check-docs.log)及[正式 docs DocGraph](logs/docgraph-formal.log) PASS。
- [全樹 DocGraph](logs/docgraph-whole.log) exit 1：包含 frozen／scratch 的 duplicate IDs，含本輪凍結副本；未刪歷史或凍結證據來製造全樹 PASS。

以上 checker 是完整有限控制，不驗證任意大小 Jordan／縮圖論證；紙面證明由獨立審閱支援。

新增相鄰四度cap：正常及seed17皆PASS，完整局部延拓數為(2,3,0,1)、24份有序pq指派；
七種C4關係依法縮至13，抽象六接點反控制保留。見 [正常](logs/cap-check.log)、[seed17](logs/cap-seed17.log)。

最後整合後重跑 [check_docs](logs/check-docs-final.log) 與 [正式DocGraph](logs/docgraph-formal-final.log)，均exit0；`git diff --check` exit0。九份frozen輸入逐hash核對drift為零。新研究未commit／push。
