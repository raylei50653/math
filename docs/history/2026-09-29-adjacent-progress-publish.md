# 2026-09-29：相鄰雙 degree-5 七輪成果整理與發布驗證

接手基準 `main@c178cf1`，工作目錄 `/home/ray/developer/ai/math`。
本輪依使用者「整理目前結果 commit + push」，整理七輪相連研究成果、
重播各報告列出的直接依賴，準備同一份 checker／證書／報告／交接 bundle。
本輪不新增數學排除、不延伸枚舉、不修改 Lean；未開 sub-agents 或 Graphify。

## 本次相連成果

| 報告 | 結果與界線 |
| --- | --- |
| [共鄰端點 t_w=1、(1,1)](../c5_adjacent_degree5_mixed_edge_shared_t1_singles.md) | 原 72 份接成 32 份必要支援，64 個 target 全接受；不需 T4 |
| [共鄰端點 t_w=0、(2,1)](../c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) | 102 份的 204 個 target 全接受；另以原路徑 K5 排除 94、保留 8 |
| [共鄰端點 t_w=0、(1,1,1)](../c5_adjacent_degree5_mixed_edge_shared_t0_singles.md) | 原 108 份皆由所需跨度至少 6>5 排除；0 target 查詢 |
| [K2 同端點型](../c5_adjacent_degree5_mixed_edge_same_endpoint.md) | 原 240 份由 K5／跨度／原 v-star 排除 105／123／12；整型 disk 來源不存在 |
| [K2 四 incidence 型](../c5_adjacent_degree5_mixed_edge_k4.md) | 原 K4 與實際外部路徑排除一般平面來源；完成唯一 mixed K2 全接線，出口第八類移除接線限制 |
| [無 mixed 必要化約](../c5_adjacent_degree5_no_mixed.md) | 同色 singleton residual、逐邊 minimality、容量缺額加重疊恰一；平面每側剩四型，118 份側資料／3,548 份共同色框接合 |
| [無 mixed 兩側 t=2,(2)](../c5_adjacent_degree5_no_mixed_t2.md) | 原 88 份中 42 份有相容支援，接成 322 份必要資料；206 份雙列已證，512／644 個 target 接受、132 個未決 |

必要支援、完整 relation schemas 與有限 minor 子圖仍不等於 disk 實現。
任意大小論證為紙面證明；適用處沿用外部 degree-list 定理，Python 重播
有限證書。未新增 Lean theorem，一般單側／共同出口與 K∞=K≤5 仍未證。
原 zw、實際附件、具名 contacts、環序、原分量身份與共同色框均保留。

## 證書與文件整理

新增七個 checker、七份 JSON 及七份 Markdown 證書表、七份專題報告、
七份原輪研究紀錄與本發布紀錄；同步 README、STATUS、HANDOFF、
介面／degree-5 導讀、前序狀態通知與條件式出口。
各原輪「未提交／下一步」保留當輪語境，當前停止點只由 HANDOFF 管理。

兩份已入庫證書 `mixed_edge_shared_t1_pair`、`mixed_edge_shared_t2`
相對 `c178cf1` 僅更新 `inputs_sha256` 中的前序文件雜湊。本輪獨立
比較：移除該欄後 JSON 完全相同，所有變更 key 都是 `docs/` 路徑，
其新雜湊與現檔一致。原數學資料、原 shared JSON、無 mixed 88 份
子表均保持；新 322 份表另存，不覆蓋原正常形。

## 發布前重播

七份新報告的重播清單去重後，共 **20 個 checker**，本輪全部以
`--check` 實際通過，未以重新生成覆蓋檔案來代替驗證：

```bash
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_k4.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_order.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_same_endpoint.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
git diff --cached --check
```

`lake build` 已通過 8,827 jobs，僅既有 AttachmentOrder／SymRelabel
lint warnings；build 不表示新紙面拓撲或 Gallai 定理已形式化。
文件檢查通過：273 份 Markdown、2,987 個本地連結；HANDOFF 149 行。
DocGraph 通過：51 份文件、155 條關係、5 families，0 errors／0 notes。
工作樹及 staged diff 均須通過 whitespace 檢查後才提交。

本輪未重跑其他 singleton 子類、唯一 degree-5 完成表、雙拒絕 atlas、
R 系列大覆蓋、profiles／閉包、大圖枚舉或 Lean axiom audit；不是全庫研究重驗。

## 停止點與發布定位

無 mixed 兩側 t=2 仍有 132 個 target 查詢未決。下一窄入口為新
record 4／p₁，原 frontier 31、sides=(137,147)：B_z=04、S_z=01、
F_z(q)={1}；B_w=34、S_w=123、F_w(q)={0}、c=3。唯一失敗上界
F_w(p₁)={0,3} 使 E_w=∅；仍需同一 C_w 的 bridge／固定框弧論證，
保留 wb3、wb4、zw 及原 C_z，不能把候選上界當作反例或逕自刪除。

本紀錄隨相連成果一併提交；可由本檔的 Git 歷史定位該次提交。
實際 push 後須另核對 `HEAD=origin/main=遠端 main` 與 clean worktree，
完成狀態以 Git 及當次交付訊息為準，不在檔內預填尚未驗證的 SHA。
