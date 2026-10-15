# 第二輪獨立審查與重播

2026-10-15。BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
每組先自驗，主 agent 再以只讀模式獨立執行下列正常重播：

```sh
python3 -B audits/2026-10-15-oddness-descent-6ddea32/check_controls.py --check audits/2026-10-15-oddness-descent-6ddea32/certificate.json
python3 -B audits/2026-10-15-six-pin-forcing-6ddea32/checks/check_forcing.py --check
python3 -B audits/2026-10-15-kempe-compatibility-6ddea32/check.py --check
python3 -B audits/2026-10-15-route-round2-6ddea32/check_counts.py --check audits/2026-10-15-route-round2-6ddea32/count-certificate.json
```

全部 exit0。前三組正常結果保存在 [independent-normal.json](independent-normal.json)
與 [independent-six-normal.json](independent-six-normal.json)。主 agent 另對
前三組各做 seed17，並重播七種原組損壞證書；全輸出、exit status、
命令及前後證書 SHA256 見 [independent-replay.json](independent-replay.json)。
根計數橋的正常、seed17、負控制及覆寫拒絕另存
[count-verification.json](count-verification.json)。

## 有限核對

| 證書 | 完整核對範圍 | 結果 |
| --- | --- | --- |
| 匹配交換 | 3 張具名圖、1361 份 PM、9289 條允許交換 | 兩種 PM 計數一致；完整重接奇偶、全部鄰居及路徑一致 |
| 六接點商圖 | 1440 local-proper rows、96 事件 rows；三圖 2880/1920/1920 份完整染色 | 全部 r lifts、兩／四義務 pullbacks、空 fibres 逐份一致 |
| Kempe 相容性 | 720 狀態、22 軌道、18816 cube targets、202752 composition equations | 同 pairing partition 不變、S4 covariance 與指定 global-swap laws 全部成立 |
| 完整計數橋 | 兩圖 47 份 PM、90 份固定根全染色、540 邊對 | κ=c+1、全部 b lifts、方向權重與逐份 involution 一致 |

以上都是有限控制或抽象系統。真正最小來源實例為零，source realization
均為 `not triggered`；來源共同鄰點定理來自紙面原幾何證明。

## 獨立拒絕控制

主 agent 重播以下七份損壞證書，全部非零退出，原證書 SHA256 未改：

- 匹配：漏一個允許交換鄰居；改壞一段重接路徑。
- 六接點：刪一份完整 lift；錯改平面超額；刪一個空 fibre。
- Kempe：改錯 switch target；刪一個狀態。

根計數證書把二十面體完整染色數加一也被拒。各組另保留
exclusive-create 覆寫拒絕；主 agent 對根證書也實際核對此拒絕。

## 紙面審查

主 agent 逐步審查：

1. 匹配對稱差逐環路徑保留同方向；路徑壓縮保存奇偶；一次切環條件
   確合成一條環。36 點反控制只否決固定方向下降，反轉方向有直接
   下降，原來源缺失已具名揭示。
2. 六接點完整事件的四個互斥分支與不可省略的不等式；三個新原共同
   鄰點公式各自的原 C4/C5、有界側及源 degree 矛盾；J 的平面首步、
   I/H/K 的重邊計數及完成成本。沒有由中間商圖非平面推最後商圖非平面。
3. Kempe checker 的 same-state、同 pairing cube、S4 transport 量詞；
   可見 components 的強模型不可代替真圖隱藏 components 和共同原邊。
4. 計數橋的 plane spanning-subgraph Euler 等式、固定根二染色計數
   及完整 Tait 染色上的兩方向 involution。

各組循環只讀交叉審查均未發現採納範圍內的實質缺口：

- [Kempe 組審六接點](../2026-10-15-kempe-compatibility-6ddea32/CROSS_REVIEW.md)：
  獨立重證三個原環的 bounded-side 與最後商圖的精確邊數。
- [六接點組審匹配](../2026-10-15-six-pin-forcing-6ddea32/CROSS_REVIEW.md)：
  除紙面審查，另以不 import 對方 checker 的實作重枚全部 1361 份 PM
  與 9289 條交換，完整集合一致。
- [匹配組審 Kempe 及計數橋](../2026-10-15-oddness-descent-6ddea32/CROSS_REVIEW.md)：
  核對明列抽象公理、隱藏分量界線、κ=c+1、完整 lifts 與權重 involution，
  並對兩 checker 正常／seed17 重播。

這些審查不是 Lean 形式化，也不把有限 checker 當成無界幾何證明。

## 不變性與傳播範圍

[check_bundle.py](check_bundle.py) 核本輪 Markdown 連結、Python 語法、
tracked diff 為空、權威副本雜湊與前輪 100 檔完全不變，以及八個
新舊 audit 之外沒有額外 untracked 路徑；最終結果見
[bundle-check.json](bundle-check.json)。`git diff --check` 通過。

前輪 bundle checker 的舊四目錄 workspace whitelist 不適用於這輪
增加四個目錄後的工作樹；本輪以新 checker 明確擴大 scope，原 checker
和原收據保持原樣。共享 docs 沒有修改，未重新宣稱全樹 DocGraph
或 Lean build 的新結果。所有證書只讀重播；無 commit／push。
