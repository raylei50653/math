# 2026-09-29：無 mixed 的同色 residual、容量與逐邊 minimality

接手 main@c178cf1，工作目錄 `/home/ray/developer/ai/math`。保留前序所有
未提交研究成果，讀 HANDOFF、STATUS、Git 狀態及直接依賴後，推進使用者
指定的無 mixed 型。未重開大圖枚舉、未使用 Graphify、未開 sub-agents，
未 commit／push。

## 成果與界線

[新報告](../c5_adjacent_degree5_no_mixed.md) 完成：

1. 無 mixed 使刪 zw 的完整關係恰為乘積；非空對角乘積迫使
   E_z(q)=E_w(q)={c}。不預設 c=3。
2. root-spoke 刪邊見證迫使 spokes 異色、所有 unary 禁色位於 A_r；
   完整 minimality 等價於聯集 A_r∖{c} 及各原分量有私有色。
   各類刪邊的完整 root 色對與被刪兩端同色均明列。
3. 每側容量缺額加重複覆蓋量恰一，得全部必要正常形。每側 t≤2；
   唯一重疊型是 t=0、(2,2)，兩份二禁色交集一色。
4. 每份 unary 碰 B；對側的實際路徑經原 zw 提供避開 C 的 root–B
   路徑。沿用 degree-list／原圖 K5 論證排除 K4 block，以及三接點
   兩拒絕、四接點三拒絕的側型。一般平面來源每側只剩
   t=2:(2)、t=1:(2,1)、t=0:(2,2)／(2,1,1)，不需 T4。

前三項是初等任意大小紙面證明；第四項依賴已重讀的
[Dvořák Lemma 7／Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
與既有三／四接點結構，補上本來源的原 zw 路徑。Python 只核對下列
有限代數與圖控制。未新增 Lean theorem，沒有獨立第二審稿者。

| 證書層 | 數量 |
| --- | ---: |
| 任意 residual 乘積，包含空集 | 256 |
| 單側候選／固定對側 c 的逐類刪邊核對 | 2,502／10,008 |
| 單側正常形／共同反射核對 | 149／149 |
| 平面必要篩選保留側資料 | 118 |
| 同一 c 的有序雙側接合，篩選前／後 | 5,647／3,548 |
| 下一 t_z=t_w=2、(2)/(2) 必要資料 | 88 |
| 真正非平面 minimal q-core | 2，分別 c=3、c=2 |
| 逐邊完整 q-染色 | 23＋29=52 |
| 固定圖全部 proper-row 接合 | 480 |
| 完整 tuples 的 marginal-product 負控制 | 6 |
| 原 zw 路徑 K5 選取子圖 | 400：K4 320、三接點 60、四接點 20 |
| 刪 zw 後指定 minor witness 失效 | 400 |
| target 分離查詢 | 0 |

118／3,548／88 是未指定 unary 支援及環序的必要資料，非 disk 來源
數量。兩張圖都有明列原 K5，不是 disk／T4 正控制。400 份 skeleton
不是完整 degree/list 來源枚舉；刪 zw 只驗證指定 witness 失效。
480 proper-row 計算只驗證固定非平面圖的公式，未計作一般 target 分離。

已新增 checker、JSON、正常形表、專題報告及本紀錄；更新 README、
STATUS、HANDOFF、介面／degree-5 導讀、前序通知及出口的失敗核心界線。
出口定理沒有新增無 mixed 類別；此前正常形與支援 artifacts 保留。

## 驗證

以下六個 checker 已實際通過，JSON／新正常形 Markdown 重播 byte-identical。
`lake build` 通過 8,827 jobs，僅既有 AttachmentOrder／SymRelabel lint
warnings；沒有 Lean 變更，build 不表示紙面結果已形式化。
文件檢查通過（269 Markdown、2,954 本地連結），HANDOFF 147 行；
DocGraph 為 50 份 metadata 文件、151 條關係、5 families，0 errors／0 notes。
`git diff --check` 通過；新增檔案亦已核對行尾空白。未 commit／push。

```bash
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_four.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

本輪未重跑 mixed K2／singleton 支援子類、唯一 degree-5 完成表、
雙拒絕 atlas、R 系列大覆蓋、profiles／閉包或 Lean axiom audit。
前序指定雙列結果沿用各自記錄，沒有宣稱本輪重驗全庫。

停止於無 mixed 的必要化約。下一窄入口為兩側 t=2、(2) 的 88 份
共同色框資料，補兩組原 spokes、原 zw、兩份二接點 unary 的實際
支援與 disk rotation，再推指定 p₁、p₂。任意列仍可能有 E_r=∅；
不能把 q 的 singleton 與私有色條件直接搬到 targets。
一般單側／共同出口及 K∞=K≤5 仍未證。
