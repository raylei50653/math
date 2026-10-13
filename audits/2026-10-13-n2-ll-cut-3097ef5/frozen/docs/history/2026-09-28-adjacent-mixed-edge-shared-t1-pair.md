# 2026-09-28：共鄰端點 K2 的 t_w=1、(2)，局部 K5 搬運與雙列分離

接手乾淨 main@e83f614b6f65042de3dbf30a96ebd0492a817385。依使用者的新推導，
先審核「既有引理足夠」候選，而非開發新的 target first-bridge 機制。
訊息中的 sandbox ZIP 未掛載，故依 repo 原始記錄獨立重建 checker；
未讀取或重播附件。沒有重開舊圖枚舉，未開 sub-agents；研究階段未
commit／push，後續整合發布見文末。

## 紙面審核與結果

[報告](../c5_adjacent_degree5_mixed_edge_shared_t1_pair.md) §2–4 補齊兩段
任意大小搬運。C_w 二接點若夾住 spoke，原 contact cycle 的 Jordan
分隔會阻止 spoke 或 diamond 的 u、v 抵達 B；兩接點因此是一個原區塊。
annulus crosscut 使五個原單位同序，保留共享框點、間隙及非最短 hull。

局部 degree-list／解除、K4-free、奇數 bridge 與逐塊 residual 證明都只
使用被測 unary 內完整 degree=4、兩接點、飽和禁色；另一 degree-5
root 位於分量外。原 diamond 提供外部 hub，以及排除時抵達補弧的原
simple path。五個 branch sets 的連通、不交及十條原邊鄰接重新明列。
未直接引用舊「全圖唯一 degree-5」的整套前提，也無新增跨列 first-bridge。
沿用外部 [Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)，
本輪讀取原文第 5–6 頁；紙面審核由本輪執行者完成，沒有獨立第二審稿者。

| 證書項目 | 結果 |
| --- | ---: |
| 原正常形及原 ID 綁定 | 36，`original_source_ids_bound=true` |
| 兩套幾何枚舉相同集合 | 1,140 |
| q 必要支援資料 | 356 |
| 原 diamond／spoke 路徑 K5 排除 | 292 |
| 保留必要資料 | 64 |
| 保留資料指定 target 查詢 | 128／128 接受，0 未決 |
| 保留 target 完整禁色候選接合 | 638，全部接受 |
| 無相容支援的原正常形 | 20 |
| 保留資料所屬原正常形 | 61、163、251、302 |
| q／target 公式與直接四點著色比對 | 2,578 |
| 字面 target 反射查詢 | 712 |
| 保留資料共同色框見證核對 | 15,312 |
| 含排除前候選的共同色框見證核對 | 52,368 |
| K5 skeletons／residual／支援穩定子控制 | 310／48／192 |

原 JSON SHA256 為 `6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`。
36 筆的完整原記錄、全部 schema、原局部 K2 ID 與輸入 SHA256 保存在新
artifact；原 306／288 筆及 9,312 schemas 保持。來源排除與 target 接受
分開計數，必要表不證 disk 可實現性；skeletons 也不是 degree/list 來源。

新層加入 checker、JSON、全表與報告，並更新 README、STATUS、HANDOFF、
degree-5 導讀、相鄰雙 root 介面、前序報告及出口。t=2 checker 將兩份
報告作雜湊輸入，新增後續通知後只刷新其兩個文件 SHA256；t=2 的
數學記錄及 38／76 結果保持，另核對除輸入雜湊外完全相同。

出口第八類擴至 t_w=1、(2)。完整 Σ(M)=Ω∖{q} 明用來源雙缺失與
刪邊繼承，不由兩列接受自行推出。證據為紙面＋外部定理＋Python，
未新增 Lean theorem；一般單側／共同出口及 K∞=K≤5 仍未證。

## 驗證

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

十份 checker 全部通過；新 JSON／Markdown 表逐 byte 重播相同。
`lake build` 成功（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 251 份 Markdown、2,816 個本地連結；DocGraph 通過 44 份
metadata 文件、122 條關係、5 families，零錯誤。HANDOFF 維持 143 行。
`git diff --check` 通過；所有新檔另檢查 trailing whitespace 與 EOF，通過。
原來源 JSON 與 HEAD 逐 byte 相同；t=2 artifact 除兩個文件輸入雜湊外
逐欄相同。上述 Lean build 沒有將本輪新論證形式化。

未重跑整個 repo checker suite：沿用其餘 singleton／mixed K2、唯一
degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、profiles／閉包與 Lean
axiom audit；未新增或擴大來源圖枚舉。紙面任意大小論證的審閱不由
上述有限核對取代。研究階段完成時工作保留於工作樹，HEAD 為 e83f614。

## 精確停止點

t_w=1、(2) 已完成指定雙列分離。接續 **t_w=1、(1,1) 的 72 筆**，
保留原 C_z 二接點、w 側兩份不同 unary、唯一 w-spoke、共鄰 u、chord zu
與原 diamond 外側環序，先證三份 actual supports 的同序必要域。
t_w=0 兩型、其他 mixed、一般雙 root、degree≥6、非相鄰 roots 及更多
高 degree 點保留；優先序見 [HANDOFF](../HANDOFF.md)。

## 整理與發布

同日依使用者「整理目前進展後 commit + push」要求，將本輪完整證據包
一併提交：新 checker、JSON、必要全表、紙面報告及本紀錄；同步 README、
HANDOFF、STATUS、degree-5 導讀、相鄰雙 root 介面、兩份前序報告、
條件式出口及 t=2 證書的文件雜湊，共 14 份檔案。
發布前讀回遠端 main，仍為基準 e83f614b6f65042de3dbf30a96ebd0492a817385。

發布整理只補明歷史／發布語境，沒有改動 checker、紙面數學或證書內容。
上節十份 checker 與 `lake build` 的成功結果沿用同一來源內容；另核對
新證書與 t=2 證書的 24 個輸入雜湊、原 36 筆 ID／完整記錄及原 JSON
不變性，全部通過。整理後文件檢查仍為 251 份／2,816 個本地連結，
DocGraph 仍為 44 份／122 條關係，皆通過；另核對工作樹與暫存區差異。
一般單側／共同出口與主命題仍未證，下一入口保持 t_w=1、(1,1) 的 72 筆。
最終提交、push 與本地／追蹤／遠端 SHA 一致性，以發布後 Git 讀回為準。
