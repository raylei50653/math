# Mixed 容量、十八側型與最小三點接線

2026-09-29，起始 Git `773cdf86e26dbb57a1e79bf017d632019853311c`，工作樹乾淨。
依[交接導覽](../c5_weak_deletion_guide.md)接續較大 mixed 的容量與接點化約；
未重啟 no-mixed 支援枚舉。專題證明見
[mixed 容量報告](../c5_mixed_capacity_contacts.md)。

## 結果與信任界線

- 任意大小、可多 mixed 的紙面容量界：固定另一 root 的色後，每份 mixed
  所禁本側色數至多為本側 incidence 數。Source unary 禁色互不重疊，
  |E_r|=m_r+D_r、D_r≤1，收成十八必要側型；另有每欄容量／重疊／漏出
  的精確差額式。不需要 planarity、T4 或外部 Gallai 定理。
- 各一 incidence 的任意大 mixed 至多兩個禁對；不同 contacts 時兩禁對
  決定完整兩份交叉 tuples，共鄰 contact 則保留同一頂點的完整可取色集。
  唯一 mixed 可新出現 E_z=E_w 為同一 pair 的對稱 source 分支。
- 唯一 mixed 恰三點時，完整固定 q 色域與逐邊接合留下 P₃ 的
  (1,1)／(1,2)／(2,1)，triangle 另留 (2,2)。此結論由有限域控制認證，
  不外推到更大分量，也不把三點形當任意大分量的收縮正常形。
- 真正 minimal q-core 的原 mixed P₃ 控制附 31 份逐邊 coloring 與 K5
  branch sets，明確為非平面控制；全部 240 proper rows 核對完整接合。

[新 checker](../../scripts/c5_mixed_capacity_contacts.py)與
[證書](../../artifacts/c5_mixed_capacity_contacts/observations.json)保存：
258 單側角色候選／143 必要角色、十八型、1,424 覆蓋欄、65,535 完整
二元關係、十一份共鄰色集、1,406 三點色集合配置，以及前層八個 mixed
固定分量的 1,920 介面／30,720 獨立 pinned queries。
P₃／triangle 分別有 15,990／13,104 份完整逐邊色角色接合；不含實際
boundary 支援或 disk 實現證書。保存全部局部 ordered triple bitmasks、
F masks、接合數及 SHA，可重算檢查；新證書小於 1 MB，未登錄大型檔案 manifest。

紙面結論與有限控制分開，未新增 Lean theorem 或 `native_decide`。
未取得新 p₁／p₂ 分離或新增條件式出口類別；完整 Σ、逐染色 repair、
一般／共同出口與 `K∞=K≤5` 仍未證。

## 驗證

```bash
python3 scripts/c5_mixed_capacity_contacts.py
python3 scripts/c5_mixed_capacity_contacts.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 的一般及 seed=17 重播逐 byte 相等，直接載入的前層 Python
及本 checker SHA 綁定於證書。前層完整介面 checker 通過，包括 34,560
原圖 pinned queries、318,720 刪邊 pinned queries、19,920 分量解除
關係與 53,040 全圖 queries。未改寫舊研究 artifacts。

`lake build` 通過 8,827 jobs，保留既有 longLine、unusedSimpArgs 與 show
tactic 警告。未改 Lean 檔案；build 不代表新容量／接點證明已形式化。
文件檢查通過 355 份 Markdown／3,608 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過；四份新增檔案另核對尾端空白與最終換行，通過。

未單獨重跑 no-mixed 十五類、增長／無增長與搬運 checker、舊 mixed
singleton／K2 各家族、root 預算、唯一 degree-5、雙拒絕 atlas、R 系列、
profiles／閉包或 Lean axiom audit。新論證未新增外部定理依賴，未重讀
Gallai 文獻。有限圖控制重用前層完整 tuple 與獨立回溯函式，不是整個
驗證引擎的獨立重寫。

## 交接與工作樹

更新專題、研究線導覽、STATUS、README 與前層完整介面的後續連結。
研究線及進行中 tag 未改，依文件治理不在 HANDOFF 堆疊成果摘要。
下一窄題：唯一 mixed 原 P₃、兩端各一 incidence、source 兩側 E 同一
pair 的實際附件／原五環內外側化約，保留 unary 原分量及外部路徑。
先證內側是否空與必要環序，不以介面相同取代原圖。

未開 sub-agents、未使用 Graphify、未 commit／push、未更新 Codex 記憶。
研究途中另觀察到非本輪產生的 `tools/artifacts.py` 與
`artifacts/MANIFEST.json` 修改；保持原狀，未將它們列為本研究成果。
