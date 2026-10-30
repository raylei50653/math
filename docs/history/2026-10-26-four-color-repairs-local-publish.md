# 四色反例修復與局部訊息求解發布

2026-10-26。從基準 `f30cd6f166ed0eb05935ee08c6784bb2f8115cc6` 整理四輪相連工作：
反例稽核、容量與編號修復、等色類與色群歸一化、按需接口求解。
目前研究入口為[四色導覽](../tools/four_color_guide.md)，本頁保存當輪結果與發布核對。

## 完成內容

| 工作 | 已完成結果 | 範圍與來源 |
| --- | --- | --- |
| 反例與必要條件 | 找到14點固定色傳播缺口、6×7格圖的紀錄容量上限，以及超大整數編號輸出失敗 | [原始稽核](../../audits/2026-10-26-four-color-counterexamples-f30cd6f/findings.json)；傳播穩定不等於有解，超限不等於無解。 |
| 修復 | 加入可選共同一致性；提高預設紀錄容量；安全序列化巨大編號 | [修復與驗證](../tools/solver/four_color_guarantee_gap.md#2026-10-26修復與保留範圍)；完整消元與原圖核對保留，明確低上限仍回limit。 |
| 歸一化 | 14點固定色整次檢查455489→6648；裸圖同一共同查詢147961→20576 | [少步推理](../tools/solver/four_color_logic_optimization.md#2026-10-26等色類與共同色群歸一化)；全部624解及完整支援保留，裸圖整次成本未下降。 |
| 按需局部訊息 | 6×7格圖41組、14點裸圖71組不同接口查詢求得一解；固定色反例281組後判否 | [局部接口](../tools/solver/four_color_local_information.md#2026-10-26按需查詢局部接口)；獨立原型只求一份見證，完整來源隱式保存，不先建立全部接口表。 |

局部訊息的各區塊沿合法袋樹接合，每次詢問同一字面框中的完整交界色組；
子樹保留內部限制與見證，所有根成功後才回填。九份具名條件的每個答覆，
均由同袋分解的完整表獨立核對；200份小圖條件另與原邊枚舉比較。
不同引擎的計數口徑各自標示，沒有用較少訊息列冒充相同比例的 CPU 加速。

## 證據與來源保管

四個原始稽核目錄、各輪驗證與seed-17收據原樣保存：

- [反例稽核](../../audits/2026-10-26-four-color-counterexamples-f30cd6f/)
- [第一次修復](../../audits/2026-10-26-four-color-repairs-f30cd6f/)
- [歸一化對照](../../audits/2026-10-26-four-color-normalization-f30cd6f/)
- [按需訊息對照](../../audits/2026-10-26-four-color-local-messages-f30cd6f/)

修復前反例的來源可由基準Git物件取回，第一次修復的來源由歸一化前快照保留；
目前來源與歷史來源分開核hash，不要求演進後的主程式等於每輪舊版本。
按需訊息另保存完整依賴快照。發布前的STATUS原bytes另存於
[前一版索引](2026-10-26-four-color-repairs-local-publication/pre-publication-docs/STATUS.md.txt)，
供歷史收據的文件hash核對；本次只在目前STATUS歷史區新增發布連結。

早期修復後atlas收據所綁定的 `four_color_constraints.py` 中間版本尚未找到相符快照；
這一筆保留為歷史來源缺口，不以後來版本冒充。主要修復報告的31份來源均有相符快照。
本次另用目前來源重跑完整atlas對照，結果與原始及修復後收據的判定／見證摘要相同。
核函式時間與未採納優化的探索收據保留為歷史觀察；主要歸一化對照有獨立重播程式。

[只讀證據核對器](2026-10-26-four-color-repairs-local-publication/audit_artifacts.py)
及[核對收據](2026-10-26-four-color-repairs-local-publication/artifact-audit.json)
只驗證已存結果、輸入與來源，不重跑整批舊效能實驗，也不覆寫歷史收據。

```bash
python3 docs/history/2026-10-26-four-color-repairs-local-publication/audit_artifacts.py --root . --out /tmp/four-color-repairs-local-artifact-audit.json
```

## 本次發布驗證

[工具測試](2026-10-26-four-color-repairs-local-publication/tool-tests.log)共405項通過，使用與CI一致的依賴：

```bash
uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'
```

[目前來源atlas對照](2026-10-26-four-color-repairs-local-publication/atlas-current.json)
涵蓋1253圖、3755份條件、7510次求解，6186次可染、1324次無延伸，無差異與超限。
這涵蓋兩個既有模式；可選共同一致性與局部訊息的核對範圍另見其專題測試。

文件、docs-only DocGraph、Git index產物政策及提交空白檢查另存於同一驗證目錄。
本輪未修改Lean來源，不重跑Lean build，也沒有新增Lean定理。
push後的local／tracking／remote SHA及遠端CI分別即時核對；push不代表CI已完成。

## 停止點

本批完成指定功能與有限核對；等色與共同推理沒有一般消元前完備性或普遍加速保證。
按需查詢仍可能問遍全部接口列，接口大小可能增長；原型沒有列舉全部fibres，
也沒有提供跨程序隱私隔離。完整求解的資源上限仍可回未判定。

README／HANDOFF入口與研究線排程核對後不改。原C₅／932、W7、J1／J2及同一平面來源
必有可延伸邊界的義務不受此演算法發布影響；有限求解能力不當作獨立四色定理證明。
