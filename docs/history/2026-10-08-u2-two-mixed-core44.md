# 2026-10-08：U2 相鄰兩 mixed 的44身份排除

基準 `main @ 2971d46d715d213f25f534958bdab499d2573b69`。
使用者要求「推進U2」。先讀HANDOFF、STATUS、Kempe導覽與C44″當輪身份，
沿原mixed11省略缺口推進；未啟動逐來源key或更大k枚舉。
證明及限制見 [U2報告](../c5_excess_two_adjacent_two_mixed_core44.md)，
目前停止點由 [Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 成果與精確界線

在完整Σ933／941或D₅像、disk、Σ-critical、ε=2、兩相鄰degree-5 roots、
恰兩mixed的原來源，任何原mixed11 D都滿足Σ(G−D)=Ω；故兩-root44的U2身份全排。
不是整個相鄰m=2來源排除，其他core型、U3／U4及任意大小猜想E保留。

126既有triangle正常形、570具名root邊的5,700次比較中，1,710空接受列、
3,927容量衝突、63進固定支援；2,016支援查詢的1,917份跨列不相容，99份
相容者全由27份同源收縮星subdivisions排除。正式新證書含24 K₃,₃、3 K₅，
246條實際邊路徑。

20原D／G控制的200完整接回、976整份D的S₄搬運與26原長core的260份
完整triangle joints均一致。染色控制不宣稱disk／Σ-critical。
獨立支援實作從65,536完整二元relations得到89禁對域，重建32支援域／81 shapes，
全部5,700比較／2,016支援查詢一致；不import primary或歷史producer。
另只讀核對126域與既有邊集、5,700完整root／contact關係及4,004個實際控制witnesses。
任意大小覆蓋仍依賴上游Gallai／全四分類與triangle拓撲／run證據，未重新稽核全部上游枚舉。

## 新產物與重播

- [Primary checker](../../scripts/c5_excess_two_adjacent_two_mixed_core44.py)
- [Primary證書](../../artifacts/c5_excess_two_adjacent_two_mixed_core44/observations.json)：
  4,064,924 bytes，SHA256 `65e5c8d3e8c039a94c97e5eb1baf7681e125e276a3ea904740852627b8477e95`。
- [獨立auditor](../../scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py)
- [獨立支援證書](../../artifacts/c5_excess_two_adjacent_two_mixed_core44/independent_support_audit.json)：
  261,739 bytes，SHA256 `f1300d35ee0004ec156140c9c8b68a57f85bf4f2a137a67dbe7c28d3ad6dcbc7`。

```sh
python3 scripts/c5_excess_two_adjacent_two_mixed_core44.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_adjacent_two_mixed_core44.py --check
python3 scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_adjacent_two_mixed_core44_audit.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
git diff --check
```

上述兩份checker的default／seed17完整byte replay都通過。
`lake build`通過8,831 jobs，只有既有lint；沒有新增Lean theorem，未建置LC額外targets。
正式證書首次生成使用已安裝的`.venv/bin/python`及NetworkX 3.5；replay均只用標準函式庫，
不重作planarity search。沒有改寫任何歷史數學payload。
`check_docs.py`通過575份Markdown／6,742個local links；限定正式docs的DocGraph
通過62份metadata documents／213 relations／5 families，0 errors。
預設全worktree的`python3 tools/docgraph check`仍因既有
`scratch/task-c44-delivery/repository/docs/`複本出現62個duplicate-id而exit1；
保留scratch及此FAIL，不把正式docs通過寫成全樹通過。
`git diff --check`及兩份新script的syntax check通過。
新MANIFEST單份entry的bytes／SHA256／producer fingerprint／依賴另核對通過；
未重跑全manifest status、上游大證書、ES／ER搜尋或LC額外Leantargets。

大證書依既有規則以明示path登錄MANIFEST及.gitignore；只新增本producer／hash／依賴，
不接受或重寫舊證書漂移。小獨立證書留作普通檔案。
README／HANDOFF研究入口與進行中標記不變，依DOCUMENTATION由guide維護新停止點。
既有audits及scratch未清理，未commit／push／開PR。
