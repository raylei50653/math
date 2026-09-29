# 2026-09-29：共鄰端點 K2 的 t_w=0、(2,1)，原 diamond 路徑與雙列分離

接手 main@c178cf1，工作目錄 `/home/ray/developer/ai/math`；工作樹保留上一輪
尚未提交的 t_w=1、(1,1) checker、證書與文件變更。先將七個交接 checker
重播為 byte-identical，再處理原 54 筆 t_w=0、(2,1)。保留上一輪變更，
未重開完成的圖枚舉、未開 sub-agents、未 commit／push。

## 結果與證據層

[報告](../c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.md) 核對無 root-spoke
的局部支援下界、K4-free 與原 diamond 外側環序。原 r–u–b_i 恢復每份
unary 的外部 hub；w 的二接點不能夾住另一單接點分量。兩套同序幾何
算法保留 actual support 間隙及共享框點，並與原正常形／完整 schemas 接合。
雙禁色 bridge 引理沿用前輪已局部化的版本；本輪所有 K5 外部路徑都只
走原 diamond 和 u／v 附件，不需 root-spoke 或其他 unary。

| 項目 | 結果 |
| --- | ---: |
| 原正常形 ID／完整記錄綁定 | 54 |
| 兩套幾何算法的相同集合／placements | 240／240 |
| 必要支援記錄 | 102 |
| 有相容支援／空纖維的原正常形 | 12／42 |
| 來源 K5 排除 | 94：C_z 專用 4、C_wp 專用 52、兩者均可 38 |
| 保留支援／原正常形 | 8／2（原 ID 54、156） |
| 全部指定 target 查詢／完整禁色候選 | 204 全接受／348 組全接受，0 未決 |
| 保留八筆的 target 查詢 | 16 全接受，0 未決 |
| 保留列完整禁色接合 | 16 組，三份 relation 均精確搬運 |
| q／target 公式與原四點直接著色比對 | 450 |
| 字面 target 反射核對 | 204 |
| 保留列／全部有見證候選的共同色框核對 | 384／8,352 |
| K5 skeletons | 130：94 筆排除＋36 份長度／cut／tether 控制 |
| residual／逐塊支援穩定子控制 | 48／192 |

紙面任意大小證明＋外部 degree-list 定理＋Python 有限證書；不需 T4，
未新增 Lean theorem，也沒有獨立第二審稿者。外部 Dvořák Lemma 7／
Theorem 10 原文第 5–6 頁於本輪重讀；web 分頁讀取失敗後，下載同一
[原始 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf) 並用 pdftotext 核對。
必要支援及 skeletons 不證 disk 可實現性。

原 shared JSON SHA256 仍是
`6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`。
新 checker／JSON／全表／報告、出口第八類、README、STATUS、HANDOFF 與
直接前序通知已接合。前序文件通知改動需刷新 t=2、t=1、(2)、t=1、(1,1)
三份證書的文件 SHA256；去除 inputs_sha256 後，已逐欄確認數學記錄
與接手快照完全一致。

## 驗證

下列十個 checker 均已實際執行通過，JSON／Markdown byte-identical。
七個交接 checker 先重播；文件通知更新後，再生成並重播三份受影響
證書及新 checker，另重播兩份原 minor／external 依賴。

`lake build` 完成 8,827 jobs，只有既有 AttachmentOrder／SymRelabel lint
warnings。文件檢查為 257 份 Markdown、2,861 個本地連結；HANDOFF 149
行。DocGraph 為 46 份 metadata 文件、132 條關係、5 families，0 errors／
0 notes；`git diff --check` 通過。

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t0_pair_single.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

不重跑其他相鄰 mixed／singleton 子類、唯一 degree-5 完成表、雙拒絕 atlas、
R 系列大覆蓋、抽象 profiles／閉包及 Lean axiom audit；不是全庫研究重驗。
DocGraph 是既有文件驗證，本輪未使用 Graphify。

最終核對另確認排除前全部 102 筆的 204 查詢已接受，並在新 checker
加入明示 assertion；因此 §4 的 pair K5 是獨立來源收窄，非雙列分離的
必要步驟。支援下界所用的局部 K4-free／平面性論證仍是前提。

## 停止點

t_w=0、(2,1) 完成指定雙列分離，加入出口第八類；完整 Σ(M)=Ω∖{q}
另用來源雙缺失與刪邊繼承。共鄰端點型只剩 t_w=0、(1,1,1) 的原 108 筆，
接手須保留 C_z 完整二接點關係與 w 的三份不同單接點原分量，檢查
同一原 diamond 外側 actual supports 的總跨度與雙列。一般出口及 K∞=K≤5
仍未證；未推進未經要求的下一分拆。
