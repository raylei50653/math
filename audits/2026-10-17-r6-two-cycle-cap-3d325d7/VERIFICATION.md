# 驗證範圍與只讀重播

2026-10-17；BASE `3d325d7197aa05815c71bedc52c1b253d736c7bb`。
本 audit 以 exclusive mkdir 建立；[INPUTS](INPUTS.json) 保存 13 份精確 BASE
輸入及前輪全部 77 份檔案盤點。checker 固定 manifest SHA256，逐份比較
frozen／BASE，並驗 live 非 routing 權威及前輪 77 檔零漂移。
只有 Kempe 導覽與 STATUS 的目前路由改動；README／HANDOFF 保留。

## 紙證與交叉審核

| 產物 | 獨立推導 | 外部交叉審核 |
| --- | --- | --- |
| cap–m 任意大小排除及 m-面距離 | [A](A/PROOF.md)、[自審](A/REVIEW.md) | [C 審 A](C/CROSS_REVIEW.md) |
| 全參考區域奇偶、兩完整補圈及三分量 | [B](B/PROOF.md)、[自審](B/REVIEW.md) | [A 審 B](A/CROSS_REVIEW.md) |
| 同一實際染色的 z-圈等價與指定短圈排除 | [C](C/PROOF.md)、[自審](C/REVIEW.md) | [B 審 C](B/CROSS_REVIEW.md) |

root 另核對三份完整證明與整合摘要的量詞、同源接回及 OPEN 邊界。
交叉審核接受不代替 Lean 形式化；本輪沒有新增 Lean theorem。

## 可重播控制

```sh
python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/check.py
python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/B/check_controls.py
```

root 完整證書保存固定七稜柱及另一個連通 cubic 圖的**全部**完美匹配參考，
包括非偶補者；對偶補參考重建每個完整交換分量及所含補奇圈數。
七稜柱的 28 個偶補參考皆連通；兩奇圈加一偶圈圖的 5 個偶補參考中，
1 個不連通。R=M 的非偶補反控制均把兩奇圈分開，確實觸發前提邊界。
B 的獨立實作用三稜柱及同構的另一圖另作校準，含 malformed reference 拒絕。
兩套固定圖皆無原完整來源／fibres／lifts，不是來源反例或任意大小枚舉證明。
真正最小來源實現仍 **not triggered**。

[首輪 checks.json](checks.json) 與[完成收據 checks-v2.json](checks-v2.json)
記錄實際命令、exit code、所需拒絕文字及 log SHA256。
正常／seed17 重播須一致；漏掉一份完整 reference 的證書、缺權威的 manifest
須被拒絕。`--write-certificate` 只用 exclusive-create，對現存證書須拒絕且
原 bytes 不變。負控制檔與失敗收據保留，不覆寫。

首輪前輪 publication checker 在目前工作樹因 `unexpected live routing drift`
退出 1：其舊契約只容 STATUS 漂移，而本輪也已授權更新 Kempe 導覽。
這份實際失敗保留；不放寬、不修改舊 checker／inventory／snapshot。
[replay_old_custody.py](replay_old_custody.py) 只讀匯出精確 3d325d7 的舊 audit、
發布檔與兩份導覽／索引，在暫存快照重播原 checker。完成收據分開記錄此
BASE 重播結果及新版 root checker 對目前全部 77 原研究檔的零漂移核對。
舊 live-routing guard 的失敗不被更名為當前工作樹全通過。
結果：精確 BASE 快照上的原 checker 通過，76 項原 seal 與 77 檔 inventory
一致；當前 root 正常／seed17 重播亦通過。

## 文件與既有庫

正式文件檢查、formal／本 audit scoped DocGraph、既有 `lake build` 及 tracked／
新撰寫檔的 whitespace 檢查結果見 checks.json；凍結 bytes 不做格式化。
新檔案另以完整候選檔案清單驗大小，沒有超過 1 MB；沒有 stage 或 commit。
不把未 stage 的新檔案誤報成已通過 Git index 產物政策檢查。
[delivery-check.json](delivery-check.json) 記錄 61 條新撰寫 audit 本地連結與
所有新撰寫 Markdown／Python 的空白核對。檢查器首輪把 `git diff --no-index`
無空白診斷的正常差異退出碼 1 誤判為失敗；修正診斷判讀後通過，原工具例外
保留在 [delivery-check-attempt1.json](delivery-check-attempt1.json)，沒有更動證據 bytes。

實際結果：695 份正式 Markdown／9148 條本地連結通過，formal／scoped
DocGraph 通過，既有 Lean build 完成 8832 jobs（保留既有 linter warnings）。
本輪所有紙證審核為 ACCEPT；正常／seed17 一致，兩個污染與 exclusive-create
拒絕均觸發，證書原 bytes 不變。檢查不證明新紙證已 Lean 化。
[OUTPUTS.sha256](OUTPUTS.sha256) 封存本輪檔案及兩份已更新路由，排除 seal 本身；
重播 `sha256sum --quiet -c audits/2026-10-17-r6-two-cycle-cap-3d325d7/OUTPUTS.sha256`。

未重跑全樹 DocGraph、歷史大型來源枚舉、九框計數、前輪大型固定圖控制或
無關工具測試。whole-tree 歷史錯誤不藉本輪 formal／scoped 通過宣稱消失。
原封存 custody 另重播；新控制不增加紙證、來源實現或 Lean 的權威。

兩圈匹配修復、其餘適用分支的 z-圈存在性、active-f 七圈、其他奇補圈、
H 相連殘案、`W110+W101>0`、`omega_e=0` 與完整319仍 OPEN。
