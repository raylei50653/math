# C5 大 k 隨機搜尋的本地提交核對

2026-10-23；研究BASE為`78375cc0e995c868c221605c24835d7e622f0091`。
研究結論及精確重播以[實驗報告](../../audits/2026-10-23-c5-large-k-random-78375cc/REPORT.md)為準。
報告中的未提交狀態保留為實驗完成時的歷史紀錄；本次只作本地commit。

提交範圍：完整實驗包58檔、State導覽、STATUS短索引、本紀錄，
及六個大型封存產物的精確bytes／SHA256例外。沒有更新其他研究線。

- 14,400份原圖、144,000列精確Σ判定；零K132外值，無一般排除定理。
- 57項SHA256清單完整吻合；忽略的`__pycache__`不屬交付。
- 從Git暫存版本獨立取出58檔，重播兩階段completion checker，
  10,800／3,600圖的收據與封存版本逐byte相同。
- 接受列由127,940份全點witness獨立核實；16,060個拒絕列有完成的獨立UNSAT判定。
  所有CSP cap只涉及已有合法完整witness的接受列，未充作UNSAT。
- 正常／seed17核對及原實驗重生成已完成；本次沒有重做抽樣。
- `lake build --no-ansi`成功（8,832 jobs）；文件、正式docs DocGraph、
  `git diff --cached --check`及Git index產物政策檢查通過。

一般`K∞=K132`、來源排除與新Lean定理仍OPEN。
下一抽樣義務：獨立起始族與固定k鏈長對照；實驗前先另記提議。
核對停於L1，HANDOFF／README的研究線與路由未變。
