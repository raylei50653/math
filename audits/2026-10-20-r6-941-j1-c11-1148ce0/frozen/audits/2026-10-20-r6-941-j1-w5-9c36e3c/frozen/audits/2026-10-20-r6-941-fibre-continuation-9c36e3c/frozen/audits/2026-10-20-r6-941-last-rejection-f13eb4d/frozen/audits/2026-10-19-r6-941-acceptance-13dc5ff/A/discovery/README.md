# 非正式發現／抽取紀錄

此目錄無正式證明權威。`synthesize_controls.py`以浮點最小總核心權重合成分支控制；`extract_controls.py`僅從已合成向量抽取整數證書，不求解LP。兩份pickle是浮點合成輸出。`explore.py`及`explore_span.py`為初步探索。

正式控制為上層 acceptance-zero-controls.json；上層 check.py全用標準庫及精確整數獨立核對，完全不讀本目錄pickle，不匯入scipy，不呼叫最佳化。
