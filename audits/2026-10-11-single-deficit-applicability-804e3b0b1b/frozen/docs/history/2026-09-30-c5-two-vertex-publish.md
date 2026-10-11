# 2026-09-30：C₅ 兩點接合、混合框與最小修復發布整理

依使用者要求整理目前進展並 commit + push。本次發布包接續本地
`e751c4b`（具名八點接合與同圖重播），涵蓋八份後續報告、checker、
證書、逐輪歷史及研究導覽；發布完成狀態以即時 Git 為準。
目前研究入口為[兩點重疊導覽](../c5_two_vertex_overlap_guide.md)。

## 成果與適用範圍

| 階段 | 已完成的固定範圍 | 報告 |
| --- | --- | --- |
| 八點接合基礎 | 132 類／1,320 點對索引、六份完整接合及同代表整圖重播；主例 140 軌道 | [具名接合](../c5_two_vertex_join.md) |
| 主例拓撲 | 八點十邊圖的 36 組環序／24 份外面配置，四種 disk 區域關係有見證，無八點 simple 外框 | [主例拓撲](../c5_two_vertex_join_topology.md) |
| 私有內點拓撲 | 正反向十五點三十五邊圖皆有平面及來源 disk 內部互斥見證；兩原框皆被原交錯路徑阻斷 | [正向](../c5_two_vertex_private_topology.md)、[反向](../c5_two_vertex_private_reverse_topology.md) |
| 反向兩混合外框 | 指定兩個五邊形面的完整 relation 為 R255／R1022，分別等於既有單／雙內點 disk 代表 | [第一框](../c5_two_vertex_mixed_frame.md)、[第二框](../c5_two_vertex_second_mixed_frame.md) |
| 共同拉回 | 原 J 為 60 軌道，兩框拉回 P 為 114；補回原邊後仍多 16 軌道 | [完整差集與修復](../c5_two_vertex_mixed_pullback.md) |
| 三點不足與四點最小修復 | 全部 56 份三點投影仍多 16 軌道；70 份四點投影及 2,415 配對中，最少兩份且組合唯一 | [三點下界](../c5_two_vertex_ternary_projections.md)、[四點最小組合](../c5_two_vertex_quaternary_repairs.md) |

最後兩項固定原反向圖、同一 U 與共同色框，以 P 單獨為基底，
只允許原 U 上無輔助變數的局部條件合取。唯一兩份最小組合為
`(a0,a1,a2,a3)`、`(a2,b0,b2,b4)` 的完整投影。
前者在任何四點投影修復中都不可省；後者只在最少兩份時被迫。

下一窄題是同一 P 上全部 inclusion-minimal 四點修復，尤其不含
後一 scope 的較大不可省組合。沿用八種排除集合及完整 54 軌道
差集，不擴張來源圖或環序搜尋。

以上為紙面推論及 Python 固定圖證書，未新增 Lean theorem。
混合框替換須限制未來只接觸該框，並密封其餘十點；其餘控制的
拓撲、一般接合政策、完整 class-pair 後繼表及一般多步充分性
均保留。一般單側／共同出口與 `K∞=K≤5` 仍未證。

## 文件與 artifacts 整理

導覽的逐輪敘述收斂為最新具名模型、完整關係對照、下一窄題及
適用界線；各輪報告與歷史保留。同步 README 的閱讀入口、STATUS
直接索引及 state 導覽，補正資料盤點報告的後續拓撲狀態。
依[文件治理](../DOCUMENTATION.md)，研究線與進行中 tag 未變，
HANDOFF 保留既有入口，不追加成果摘要。

三點證書 2,440,491 bytes、四點證書 3,876,919 bytes，依既有
1 MB 規則在 [manifest](../../artifacts/MANIFEST.json) 記錄 SHA-256、
大小、生成器及相依順序，並加入 `.gitignore`；本機完整檔案保留。
其餘六份新增證書隨 Git 保存。新 clone 可依序重建：

```bash
python3 scripts/c5_two_vertex_ternary_projections.py
python3 scripts/c5_two_vertex_quaternary_repairs.py
python3 tools/artifacts.py status
```

## 本輪驗證

Python 3.14.7 下，本線十個 `--check` 全通過；八個新增 checker
亦全部以 `PYTHONHASHSEED=17` 通過逐 byte 重播。完整重播命令
見[導覽](../c5_two_vertex_overlap_guide.md#4-閱讀與重播入口)。
檢查包含原圖完整 J、來源 hash 鏈、實際原邊延拓、完整差集、
全部三／四點投影及 checker 內建負控制。

`lake build` 通過 8,827 jobs，僅既有 AttachmentOrder／SymRelabel
linter warnings；不表示新拓撲或關係修復已形式化。
`python3 tools/artifacts.py status` 得到 `ok=103`，無 missing、
changed 或 stale；此項是檔案雜湊／生成器指紋核對，並非全部重建。
另在 `/tmp` 隔離目錄只複製來源鏈、不帶兩份大證書，依序生成三點
及四點證書；兩份大小與 SHA-256 均和 manifest 完全相同。

文件檢查通過 383 份 Markdown／3,892 個本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes；
`git diff --check` 通過。命令如下：

```bash
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

未重跑來源大枚舉、任意大小目錄完備性、其餘三例 embedding、
其他研究線 checker 或 Lean axiom audit；未修改 Lean 或研究演算法。
本輪只整理並發布既有成果，沒有推進下一個修復分類問題。
