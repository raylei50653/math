# 四色實驗室進展整理與發布核對

2026-10-25。入口：[四色實驗導覽](../four_color_guide.md)。本次整理已有成果，不擴大研究枚舉。

## 結果與邊界

- 逐點試色與完整關係消元／回填共用原圖格式、固定色及逐步播放器。
- 共同接口交集、原環閉合及保中心色的二／三元接口反覆傳播；十二點固定色反例由8次消元降至0次，九點反例仍需4次。
- 四十例兩模式皆27可解13無解；完整解保留、結構全域投影、隨機族指定見證及有界搜尋分開記錄。
- C₅裸環查表、五度鄰環局部掃描及結構推導均為有限必要推理，不是disk來源覆蓋、一般免消元或四色定理證明。

共用 solver／CLI／viewer 已整合各輪模組，作一個連貫提交；保留各輪凍結來源、失敗／超限原型與原始收據，不重建虛構歷史版本。
README／HANDOFF 增實驗入口，STATUS 壓縮為直接報告索引；各主題的數字與停止點以來源報告為準。
六份超過1 MB的 JSON 登記 exact frozen exceptions，封定 bytes／SHA，不把目前 solver 當成歷史產生器。

## 本次實際核對

```sh
uv run --with-requirements requirements.txt python -m unittest discover -s tools/tests -p 'test_*.py'
lake build --no-ansi
python3 scripts/c5_equivalent_forms_check.py
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
```

工具測試265項通過；Lean build 8832 jobs通過，保留既有lint警告；等價形式checker通過（60圖／600列有限matching控制）。
上述C₅ checker只是既有本地四份提交的重播，沒有開始P1–P4或新增來源結論。

[本次只讀證據核對](2026-10-25-four-color-lab-publication/propagation-audit.json)確認6報告、76本地目標、105來源快照、268份gzip記錄及12個頂層artifact雜湊；局部資訊報告在記憶體重播逐位元組相同。
最新條件原環31份來源與目前程式相符；舊輪共用程式已有後續改動，沿用其凍結來源，不改寫封存報告或實驗資料。
歷史normal／seed-17批次與瀏覽器檢查本次未重跑，保留原收據的時點與範圍；本次hash核對不能改稱語義重播。

全工作樹DocGraph仍有72個歷史／scratch重複ID錯誤；正式docs的結果另列，不能混稱全域通過。
最終路由、staged artifact policy與推送狀態以本次Git及最後核對為準；本記錄不預稱遠端CI成功。
