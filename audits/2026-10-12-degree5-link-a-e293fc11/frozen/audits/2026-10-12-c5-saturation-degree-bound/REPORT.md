# 最小來源度數界：隔離證據包

2026-10-12。發布 BASE：`5d70a39940182ea37c9ca5d36d9ebb7f612160ad`。
原研究開始時 HEAD 為 `ab0862485b30b12b538c734271f354630afa8e26`；其後共面正規形
已另行提交。本包凍結採納時輸入，不覆寫前輪 scratch 或共面證書。

## 採納與依賴

[權威證明](../../docs/c5_saturation_degree_bound.md) 給條件性紙面結果：一般 C4 關係
有至多三內點代表；global 最小內點、再最大邊數的目錄外 C5 來源，若存在，具有
`k≥13`、邊界度數至少四、內部度數至少五、至少六個五度內點。
繼承的普遍 screen／4CT、132 目錄 witnesses 及聯集封閉、共面正規形和外部
`K≤12=K` 前提明列於原證明。不把任意飽和或固定 mask 最小性混入。

凍結來源與 SHA256 見 [INPUTS.json](INPUTS.json)；[原研究文字](frozen/original_result.txt)
保留當時截點。新採納的中文證明與此原稿分開。獨立紙面審查見
[PROOF_REVIEW.md](PROOF_REVIEW.md)，結論為 conditional PASS。

## 有限證據

[checker](controls/check.py) 與 [certificate](controls/certificate.json) 保存：

- C4 全部 16 masks 的 dummy 增廣表、七份代表的實際邊、完整 fibres 及平面性。
- 三內點四度控制的原圖及兩份合法 quotient，完整十列證 `429=424∪165`，
  並保存兩個單分支丟列 witnesses。
- 六內點 octahedral 控制的完整十列 fibres、全部 31 個缺邊、兩個合法加邊均嚴格
  縮小關係；全內部無 C5。無界 patch 族只作紙面推導。
- 直接 product 與獨立 MRV 對所有合法外框 assignments 的逐份比較，包含空 fibres。

正式重播紀錄見 [VERIFICATION.json](VERIFICATION.json)，各命令輸出在 `logs/`。
normal、seed17 與破損證書負控制的範圍以該紀錄為準。`--check` 只讀，沒有更新舊證書。

## 信任界線與交付

| 控制 | 狀態 | 意義 |
| --- | --- | --- |
| C4 映射與具體小代表 | triggered and holds | 有限映射、full lifts 與平面性通過；普遍性仍接原 screen |
| 任意 Σ-飽和迫全內部 C5 | counterexample | 六內點控制及可任意增大的 patch 紙面族 |
| 單一四度 quotient 保完整 Σ | counterexample | 兩個 quotient 都丟列，只有聯集保全部 |
| 真正 933／941 最小來源 | not triggered | 沒有來源 witness，零觸發不能當作排除 |

cap replacement 保完整邊界關係，沒有聲稱新舊內部 fibres 的基數或著色雙射相同。
一般十三內點以上、小代表主命題、五度配置的可縮減性及 Lean 形式化仍 OPEN。
外部論文的計算證明未重播；既有 Lean build 不表示本輪紙面拓撲已形式化。

使用者本輪只授權整理及本地 commit；沒有 push 或外部發布。
connected 白名單、文件治理檢查及與其他暫存工作的隔離見
[本地發布紀錄](../../docs/history/2026-10-12-c5-saturation-degree-bound-publish.md)。
