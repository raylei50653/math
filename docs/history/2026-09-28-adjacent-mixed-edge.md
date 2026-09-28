# 2026-09-28：唯一 mixed 原 K2、各一接點的必要化約

接手 main@104c8bcccb32486dbddd7d23183c47b0c7282526，保留共鄰 singleton
五輪 checker／artifacts／報告及出口整合的未提交成果。沿 HANDOFF 進入
唯一 mixed 原 K2、兩 root 各一 incidence，即原 z–u–v–w–z 四環。
未 commit／push，未開 sub-agents，未重開唯一 degree-5 或圖 catalogue。

## 結果與界線

[證明報告](../c5_adjacent_degree5_mixed_edge.md) 先給任意大小的完整關係
與逐類 minimality，再保存有限必要域。q 下 K2 的兩端 list 不同且都含
3，mixed 恰禁唯一 (d,e)，d≠e。root-edge 刪後同色見證使兩側 residual
只能為 ({d},{d,e}) 或 ({d,e},{e})。

一色側的 unary 容量全部飽和、禁色互不相交；兩色側差一。原 r–u–B
或 r–v–B 路徑給連通 hub 及三接點 active triangle 的 K5，排除 (3)。
平面來源一色側剩五型，兩色側只剩 (2)、(2,1)，不需 T4。
原四環內側沒有其他有效頂點；原 u／v 支援另作 disk crosscut 限制。

| 證書項目 | 結果 |
| --- | ---: |
| 每側 unary 容量候選 | 209 |
| 九種 ordered 缺色的逐類 minimality／正常形比較 | 393,129 |
| 抽象 minimality 資料 | 816 |
| 原路徑 K5 排除含 (3) 的資料／保留資料 | 240／576 |
| 原 u／v 有序 q 支援／交錯排除／剩餘必要 pair | 40／4／36 |
| 全部實際 K2 支援乘 proper rows | 100×240＝24,000 |
| 獨立 pinned queries／實際刪邊 queries | 16,000／112,000 |
| 刪邊端點同色核對／共同色框搬運 | 6,020／24,000 |
| 任意列完整判準 | 22,500 |
| 真正 minimal q-core 控制的全列／逐邊 coloring | 240／27 |
| K5 skeletons／刪 rp_r 指定 witness 失效 | 各 480 |

576 筆只記 q 下 unary 禁色與接點角色；36 組只記原 u、v 的實際兩個
boundary pair，兩者尚未與全部 unary 支援／環序接合。不是平面實現性
證書，也沒有新增 p₁／p₂ 延拓查詢或擴充條件式出口。
真正 minimal 控制只接受 canonical 01021、01201、01231，不接受全部
T4；沒有把它當成 disk 正控制。完整 tuple／marginal 負控制保留 uv
異色條件，避免用假的 (3,3) 接受 root pair (0,1)。

Dvořák 的 degree-list Theorem 10 本輪線上核對；原 K4 hub 及三接點
active triangle 論證沿用既有報告並重核其前提。紙面 arbitrary-size
化約、外部定理、Python 關係／minor 控制分層；未新增 Lean theorem。
原有 checker／artifacts 未改寫；34／40 報告僅新增後續入口。

## 驗證

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

四份 checker 全通過；新 JSON 與 Markdown 必要表逐 byte 重播相同。
`lake build` 通過（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 238 份 Markdown／2,712 個本地連結；DocGraph 通過 40 份
metadata 文件／105 條關係／5 families。HANDOFF 保持 150 行。
`git diff --check` 通過；新 checker、兩份 artifacts、報告及歷史紀錄
另逐檔核對 trailing whitespace 與 EOF。

沿用且未重跑：singleton 同側／三份長弧 checker、no-spoke 大支援表、
唯一 degree-5 其餘完成表、雙拒絕 atlas、R 系列大覆蓋、抽象 profiles／
閉包、圖枚舉與 Lean axiom audit。依賴 checker 的歷史計數不當成本輪
K2 來源數；lake build 不形式化新紙面 disk／minor 證明。

## 精確停止點

必要化約已完成；下一入口取一色側 t=2、(1)，兩色側 (2) 或 (2,1)。
一色側單接點 F={3} 迫使其 actual support 見全部三個 q 色；需在原
四環外側同時接合兩條 root-spokes、原 u／v 支援及所有 unary 支援，
再用同一來源的跨列關係。其他一色側四型亦未分離。
唯一 mixed K2 的完整指定分離、無 mixed、其他 mixed 接線、一般雙 root、
degree≥6、一般單側／共同出口與主命題仍未證。當前優先序只見
[HANDOFF](../HANDOFF.md)。
