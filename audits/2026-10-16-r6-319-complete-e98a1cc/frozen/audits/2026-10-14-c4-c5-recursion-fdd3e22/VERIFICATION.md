# 本輪驗證與信任界線

2026-10-14。主 checker 皆採 exclusive-create 證書及唯讀 `--check`；
完整命令、環境、exit code 及輸出見 [logs](logs/receipts.json)。

| 控制 | 實際範圍／結果 |
| --- | --- |
| [返回單射](fibre/check_return.py) | 六接點全指派／component partitions；三張明列三角化 disk 的完整固定框 fibres、非空集合映射與逆映射；正常及 seed17 PASS |
| [使用者的三度剝除](degree3/check.py) | 504 份共同指派、兩套獨立判定、全部 s lifts、可能 q=w 及反射重合；正常及 seed17 PASS |
| [r 六度轉移](degree4/check_transfer.py) | 4^7=16384 指派兩套寫法相符；完整上界319及 K132 三關係；外框必要閉包、原可選邊；正常及 seed17 PASS |
| [r 六度／t 五度再剝除](degree4/check_t5.py) | 16384份一般指派、4096份 h=p 指派；nested/direct 全 t/r lifts 相符；542無目錄子關係、575經紙面兩交換降63無目錄子關係；正常及 seed17 PASS |
| [七接點共同計數](fibre/r6_counts/check_counts.py) | 三種互補色對各自完整標號交換軌道分解同一列計數；三關係皆有精確整數必要模型；正常及 seed17 PASS，不證來源實現 |

可由 repo root 重播：

```sh
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/check_return.py --check
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree3/check.py --check
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_transfer.py --check
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/degree4/check_t5.py --check
python3 -B audits/2026-10-14-c4-c5-recursion-fdd3e22/fibre/r6_counts/check_counts.py --check
```

反例／負控制包括省略 no-rainbow 前提、錯誤以存在一個 lift 代替全部 lifts、
交錯分量、已禁止框列、零計數與不一致的共同列計數；另有實際篡改證書拒絕日誌。
正常來源保留所有空 fibres 和零個 r lift 的指派；沒有將後者誤刪。

[獨立返回審閱](degree3/KEMPE_REVIEW.md)及 [r 六度審閱](degree3/R6_REVIEW.md)
分別覆核原來源到較小 disk 的接線／rotation、接點身份及紙面交換。
有限局部表與 K132 查表是任意大小條件推導中的有限步驟；真正目標圖控制為0，
不以樣本搜尋未命中宣稱來源排除。來源排除依報告的普遍必要性與紙面矛盾。

輸入與文件檢查的最終結果記於下節。本輪未新增 Lean theorem，
未重跑外部≤28圖枚舉或 plantri；不提升一般 K≤22／k≥23。
計數模型的求解器只尋找候選，權威重播全部用 Python 整數，無須 solver。


## 最終核對

- 五份主控制正常／seed17 共十次 PASS；獨立原 cap checker 另 PASS。
- 16 份 frozen 輸入 SHA 全數相符，數學輸入的 live drift 為0；原 STATUS
  路由變動另列，不算數學輸入漂移。K132 副本與原檔逐 byte 相同。
- `check_docs` PASS：683 Markdown、8,896 本地引用；正式 docs DocGraph
  PASS：97 文件、379 relations、0 errors。
- 全樹 DocGraph **FAIL**：70 項皆為保留的 frozen／scratch 重複 ID。
  不刪歷史證據，不把正式 docs PASS 當成全樹 PASS。
- `git diff --check` PASS；本輪採納 audit 文件的42條本地連結皆存在。

證書最終身份見 [MANIFEST](MANIFEST.json)；manifest 不自列。
獨立 checker 的生成改為 exclusive-create；數學結果及既有證書不變。
