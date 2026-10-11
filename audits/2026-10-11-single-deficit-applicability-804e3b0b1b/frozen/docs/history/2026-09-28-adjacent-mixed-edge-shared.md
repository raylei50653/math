# 2026-09-28：唯一 mixed K2 共鄰端點的完整關係與逐邊 minimality

接手 main@104c8bcccb32486dbddd7d23183c47b0c7282526，保留前輪尚未提交的
singleton 與 mixed K2 成果；依 HANDOFF 處理 P*ᶻ={u,v}、P*ʷ={u}。
未 commit／push，未開 sub-agents，未重啟唯一 degree-5 或大圖 catalogue。

## 結果與信任界線

[新報告](../c5_adjacent_degree5_mixed_edge_shared.md) 先給任意大小的紙面
關係與 minimality 充要式，再建立有限控制。u 原接 z,w,v，故只剩
一條 boundary 邊；v 接 z,u，故有兩條 boundary 邊。共享 u 使用同一
變數，完整關係為存在同一 (s,t) 且 s≠t、s≠a,b、t≠a。

q 下 mixed 禁對恰為 {d,3}×{e}，h=q(N_B(u))，v 的 boundary 色為 h,e。
逐邊 minimality 強迫 z 無 spoke、唯一二接點 unary，其禁色為 {h}、
{h,d}、{h,3} 之一；w residual={e}，每份 unary 禁色恰達容量且互不重疊。
w 的三接點分量由原 w–u–B 路徑、active triangle 與原 tethers 給 K5。
任意大小部分不需 T4；此排除沿用外部 degree-list 定理，當輪已核對
[Dvořák 講義 Theorem 10](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)。

| 證書項目 | 結果 |
| --- | ---: |
| z／w 容量候選 | 41／209 |
| 九種 h／d 的 minimality 判準核對 | 77,121 |
| 抽象必要資料／(3) 排除／平面必要保留 | 306／18／288 |
| 展開完整 q 關係的必要 schemas | 9,312 |
| 全部局部支援／boundary rows | 50×240=12,000 |
| 獨立 pinned／逐邊刪除 queries | 8,000／56,000 |
| 刪邊端點強迫／共同色框搬運 | 3,640／12,000 |
| q 相容具名 K2 支援（附反射 ID） | 28 |
| 任意列拒絕公式控制 | 6,600 |
| 實際 minimal q-core／全列接合／逐邊 coloring | 3／720／71 |
| 原 w–u–B 的 K5 skeleton | 84 |

三張完整 degree=(5,5,4,…) 的控制分別實現三種 z 禁色，canonical
接受列皆只有 01021、01201、01231，故不接受全部 T4；沒有 disk 正控制
宣稱。三份圖不是任意大小覆蓋的依據。84 份 skeleton 只驗 branch sets，
刪 wu 後指定 witness 失效，不宣稱整圖因此平面。

288 筆尚未接合全部 unary 實際支援與 embedding 次序；9,312 是完整
q 關係的必要 schemas，不是來源數。28 組局部 K2 支援另存，不能相乘
後宣稱 disk 實現。一般出口與主命題仍未證，沒有新增 Lean theorem。

README、STATUS、HANDOFF、degree-5 導讀、介面與出口報告已接上新成果，
前輪四環排除報告加上後續入口。出口類別沒有增加。

## 驗證

```bash
python3 scripts/c5_adjacent_degree5_mixed_edge_shared.py --check
python3 scripts/c5_adjacent_degree5_shared_singleton.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
python3 scripts/c5_single_spoke_three_one.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

四份 checker 全通過；新 JSON／Markdown 必要表逐 byte 重播相同。
`lake build` 通過（8,827 jobs），僅既存 AttachmentOrder／SymRelabel warnings。
文件檢查通過 244 份 Markdown／2,752 個本地連結；DocGraph 通過 42 份
metadata 文件／113 條關係／5 families，零錯誤。HANDOFF 保持 149 行。
`git diff --check` 通過；新增 source、報告、歷史、JSON／表的 trailing
whitespace 與 EOF 另行檢查通過。Lean 建置沒有形式化本輪新論證。

沿用且未重跑：各一接點 mixed K2 與原四環次序 checker、singleton
同側／各長弧 checker、唯一 degree-5 完成表、雙拒絕 atlas、R 系列大覆蓋、
抽象 profiles／閉包、圖枚舉與 Lean axiom audit。沒有修改它們的證書。

## 精確停止點

共鄰端點型的完整 mixed／unary q 關係、逐邊 minimality 與五種平面
w 分拆已作必要化約。下一窄型為 w 側 t_w=2、(1) 的 18 筆：由原
z–w–u–v–z 四環及 chord zu 證全部 unary actual supports／環序，再接合
28 組局部 K2 支援及同圖任意列判準。各一接點型的周長論證不可直接移植。
本型 disk 來源排除／雙列分離、其他 mixed、一般雙 root、degree≥6 及
一般單側／共同出口仍保留。當前優先序只見 [HANDOFF](../HANDOFF.md)。
