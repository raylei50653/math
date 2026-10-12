# 任務 A：degree-5 link 位置分類與替換契約

2026-10-12。BASE：`bc7c0820e6b5e585869b8a59e04f52da0dad2d33`。
本包完成指定任務 A 的紙面來源契約與有限校準，尚未採納到共用文件。
沒有使用任務 B 的重接結果或任務 C 的有限閉合結論。

## 結果

[完整紙面證明與位置表](paper/classification.md) 從原最小性重證 link 為 induced C5，
分類 `m=|L∩B|=0,…,5` 的九種位置，保存共同循環方向、共有邊、cap 邊界、
annulus 雙邊界及重複 pin 的 boundary walk。每種位置都給出原分量／bridge
ownership、可能 chords、完整具名替換契約及精確內點數。

新得到的條件性紙面推論是：

> 在 BASE 所述全域內點最小、再最大邊數的目錄外來源中，
> 每個 degree-5 內點與原外框的接觸，只能是空集、單點，
> 或一條原外框邊的兩端點；該邊亦為原 link 邊。

三接點的「一條共邊＋一個孤立接點」型有兩個 C4 caps；同框替換後只需
`3+3+3=9` 內點，與 `K≤12=K` 矛盾。其餘 m≥3 型均有共用連續兩邊，
迫原外框中央點 degree 三，違反已採納的外框度數界。

再由完整 cap 替換與全域最小性，原 C4／C5 cap 自身的私有內點數已有
`r≤3／r≤5`。當 `2≤r≤5`，每個私有點因 full-G degree 至少五而必接 cap
邊界，故私有誘導圖為 outerplane，至多 `2r−3` 邊。Euler 的 degree sum
立即矛盾；所以原 C4 cap 只可能 r=0，原 C5 cap 只可能 r=0 或 1。
前者在 C4＋C6 型迫原度數不足；後者在 C5＋C5 型使原圖至多六內點。
兩種非相鄰接點型因此也被排除，無需任務 C 的有限閉合。

剩下三種**未排除的必要位置**，不表示已有實際目錄外 witness：

| 位置 | 完整介面／幾何 | 已有計數與精確殘餘 |
| --- | --- | --- |
| m=0 | 兩個五環邊界的 annulus，10 個 pins | `6+r`；需同介面且同拓撲的 `r≤6` 代表 |
| m=1 | 9 個 pins，接點出現兩次的 pinched boundary | `5+r`；需 `r≤7` 代表及同一 pin 識別 |
| m=2，相鄰 | 一條共有邊＋簡單 C8 cap | `4+r8`；需完整八 pin 關係的 `r8≤8` 界 |

僅用一般 C4／C5 代表計數，兩個非相鄰型原本只得到 `7+r6` 與 14；
本包是另外使用**原 cap** 的局部最小性及原 degree 下界才將它們排除，
沒有把十四內點誤套十二內點界，也沒有把度數下界施加於替換後的代表。

替換引理對十個原外框列逐一提供雙向 full-lift 構造。它保持同一外部圖、
所有具名 pins 及原嵌入位置，沒有聲稱新舊內部 fibres 的基數相同或存在雙射。
`G−v` 的普通外 C5 小代表雖由最小性存在，仍會忘掉 L 的 pins 與接回中心的
空位，不能直接取代所需 marked relation。

## 有限證據與審查

[拓撲控制說明](controls/README.md) 與正式 [v2 證書](controls/certificate.v2.json)
保存九個 literal 骨架、原邊、oriented faces、每點 rotation、原附件 ownership、
十列所有 `(B,L)` 介面 cells（含 empties）、中心可用色及全圖 full lifts。
1262 份帶原 L 方向符號的循環接觸編碼中，362 份通過 induced／共邊契約，
分到九個代表；其餘 900 份不滿足接觸契約，不是來源反例。
這是有限 incidence 編碼的完整核對；任意大小來源的覆蓋來自紙面 Jordan 論證。

checker 比較完整介面 join、直接全圖枚舉與獨立回溯，並檢查 face darts、
rotation、Euler 與保留 B 的 apex 平面性。九個骨架的 full-lift 數依序為
`900,300,100,78,78,33,28,12,5`；它們不是符合全域最小性與度數界的來源。

[漏 pin 反控制](review/projection/certificate.json) 給兩個外圈關係同為 1023
的 literal patches；加入同一外部 spokes 後，完整關係變成 255 與 987。
`01231` 列在第一圖為空，在第二圖有 `012310` 全圖 lift。
兩種邊均可嵌於同一原外部面，故反控制明確定位在遺失 pin 關係。

独立審查分為 [topology](review/topology.md)、[replacement](review/replacement.md)
及對最終紙面稿的 [proof review](review/final-proof-review.md)；新增排除另有
[small-cap 引理獨立推導](review/small-cap-refinement.md)。
重播及負測試的實際結果见 [VERIFICATION.json](VERIFICATION.json)；
凍結輸入見 [INPUTS.json](INPUTS.json)，包內雜湊見 [MANIFEST.json](MANIFEST.json)。
舊 v1 控制證書保留其原始 bytes；v2 只修正被拒接觸編碼的 coverage 標籤，
其正式重播入口如下。

```bash
.venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/controls/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/controls/certificate.v2.json
PYTHONHASHSEED=17 .venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/controls/check.py --seed 17 --check audits/2026-10-12-degree5-link-a-e293fc11/controls/certificate.v2.json
.venv/bin/python audits/2026-10-12-degree5-link-a-e293fc11/review/projection/check.py --check audits/2026-10-12-degree5-link-a-e293fc11/review/projection/certificate.json
python3 audits/2026-10-12-degree5-link-a-e293fc11/verify_package.py
```

checker 使用目前 `.venv` 已有的 NetworkX 3.5；未重跑上游大型證書或外部論文
的計算證明。有限 certificate 均為完整重建後比較，`--check` 不覆寫。

## 範圍與停止點

| 項目 | 狀態 | 證據界線 |
| --- | --- | --- |
| 九種接觸位置、原區域分解、替換與計數 | triggered and holds | BASE 前提下的紙面推論，兩份獨立核對 |
| m≥3 及兩個非相鄰接點型排除 | triggered and holds | 紙面度數／九內點界／原 small-cap degree 引理，不由零目標控制推得 |
| 九個 literal 骨架與完整 fibres | triggered and holds | 固定域有限幾何／著色校準 |
| 只保外圈十 bit 即可忽略額外 pin | counterexample | 同外部、同合法 slot，255／987 不同 |
| 真正 933／941 及 D5 像的條件來源 | not triggered | 無實際來源，不捏造數值 fibres |
| 新 Lean theorem／本輪 Lean 驗證 | not triggered | 未新增、未執行 |

任務 A 所需的位置分類、具名平面分解、替換引理與各類計數已完成。
三個保留型的小代表／縮減義務、任務 C 的任意 132² 有序 cap-pair 有限閉合、
至少六個五度點是否迫出可縮減位置、十三內點
以上的一般來源、一般壓縮及 `K∞=K≤5` 仍 **OPEN**。

修改限定本專屬目錄；共用導覽、STATUS、原證書及其他研究包只核對而未採納更新。
這遵守任務自身的隔離交付要求。沒有 commit、push、PR 或外部發布。
收尾時另觀察到共用文件有並行變更，列於 [workspace drift](logs/workspace-drift.json)；
本包仍以原 BASE 的 15 份凍結輸入為準，凍結雜湊沒有漂移，沒有把新共用內容
混入本轮證明。
