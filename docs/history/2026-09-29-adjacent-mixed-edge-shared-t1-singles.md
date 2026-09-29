# 2026-09-29：共鄰端點 K2 的 t_w=1、(1,1)，飽和環序與雙列分離

接手乾淨 main@c178cf1，工作目錄 `/home/ray/developer/ai/math`。按 HANDOFF
選定原 72 筆 t_w=1、(1,1)；先重播 t=1、(2)、t=2、(1) 及共鄰端點
化約，三份既有證書均 byte-identical。未重開完成的圖枚舉，未開 sub-agents，
未 commit／push。

## 紙面與有限證據

[報告](../c5_adjacent_degree5_mixed_edge_shared_t1_singles.md) 保留 C_z 的完整
有序二接點關係、w 的兩份不同單接點分量、原 diamond／chord zu 及 spoke。
局部 degree-list／K4-free 論證適用每份原 unary，不要求另一 root 為 degree-4。
三份支援各至少見兩個 q 色，禁 3 的 w 分量另須見三色。原 diamond 外側
同序遂使總跨度下界 1+2+1+1=5 飽和；兩份單接點身份從未合併。

| 項目 | 結果 |
| --- | ---: |
| 原 ID／完整記錄綁定 | 72 |
| 兩套幾何算法的相同集合 | 780 |
| 必要支援記錄 | 32 |
| 有相容支援／空纖維的原正常形 | 16／56 |
| 指定 target 查詢 | 64 全接受，0 未決 |
| 完整禁色候選接合 | 128 全接受 |
| q／target 公式與原四點直接著色比對 | 160 |
| 字面 target 反射核對 | 64 |
| 具名單接點分量交換核對 | 32 |
| 共同色框局部見證核對 | 3,072 |
| 新來源 minor 排除 | 0 |

此型不需 T4、新 K5 排除或跨列 first-bridge。兩份完整 F 的 target 上界
連同 C_z 關係在共同色框接合，所有候選都接受；每個 target 還保存一份
對全部候選通用的原 (z,w,u,v) 見證。證據為任意大小紙面＋沿用外部
degree-list 定理＋Python，未另讀外部原文，也沒有獨立第二審稿者或新增
Lean theorem。必要支援不證 disk 可實現性。

原 shared JSON SHA256 仍是
`6b9b689c1f45b22feb182958c953b18989fe47655f69d5d2a17d8ed509555532`。
新報告／checker／JSON／全表與 README、STATUS、HANDOFF、前序通知及
出口第八類相互接合。新增前序通知須刷新 t=2、t=1、(2) 證書的文件 SHA256；
另以 JSON 去除 inputs_sha256 後與 HEAD 逐欄比較，確認兩份證書的數學
記錄完全一致；變更僅為 shared 報告的一個雜湊及 pair 報告的另一個雜湊。

## 驗證

以下全部實際執行通過；七個 checker 的 JSON／Markdown 均 byte-identical：

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_singles.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t1_pair.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared_t2.py --check
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_singleton_long_arc.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 完成 8,827 jobs，只有既有 AttachmentOrder／SymRelabel 的
lint warnings。文件檢查為 254 份 Markdown、2,838 個本地連結；HANDOFF
145 行，低於 150 行上限。DocGraph 為 45 份 metadata 文件、127 條關係、
5 families，0 errors／0 notes。這是既有 DocGraph 驗證，未使用 Graphify。

不重跑其他相鄰 mixed／singleton 子類、唯一 degree-5 完成表、雙拒絕 atlas、
R 系列大覆蓋、抽象 profiles／閉包及 Lean axiom audit；不是全庫研究重驗。

## 停止點

t_w=1、(1,1) 完成指定雙列分離，共鄰端點接線的 t_w≥1 全部接回出口
第八類。完整 Σ(M)=Ω∖{q} 另用來源雙缺失與刪邊繼承，非兩列接受單獨推出。
下一窄入口為 t_w=0、(2,1) 的 54 筆；保留 C_z 二接點、w 的二接點與
單接點原分量，先補無 spoke 的 actual supports／環序與原外部路徑。
t_w=0、(1,1,1) 的 108 筆及一般出口／K∞=K≤5 仍保留。
