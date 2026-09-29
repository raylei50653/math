# No-mixed 逐 root 不可搬運界與精確接合介面

2026-09-29，起始 Git `98b26b7fff528f0c792c80275dccec7a035f5c78`，工作樹乾淨。
研究完成時未開 sub-agents，未 commit／push；後續授權發布見本文末節。證明直接補入
[既有 hypothesis audit §3.1–3.3](../c5_no_mixed_hypothesis_audit.md#31-逐-root-不可搬運界)，
前置為[跨度預算](../c5_no_mixed_span_budget.md)與
[前輪三假設驗證](2026-09-29-no-mixed-hypothesis-audit.md)，目前入口與後續
窄問題見[weak-deletion 導覽](../c5_weak_deletion_guide.md)。

## 本輪結論與範圍

沿用同一 induced-C5 disk、相鄰雙 degree-5、no-mixed、minimal q-core，
及共同同序支援 lifts、正跨度、框邊內部不交、既有側跨度下界。紙面證明
Π_C(q,p)=∅ 迫 span_L(C)≥2，進而每 root 至多一份不可搬運原分量；
有不可搬運分量的側跨度至少 max(ω_r,m_r+1)，A/B/C/D/E 下界為 2/3/3/4/4，
所以雙不可搬運只可能 AA/AB/AC。這些推導不依賴 44 筆查詢的有限統計；
不查支援表仍明用既有結構引理，沒有改稱無前提或免結構分類的結果。

完整 T_C 由相容置換雙向搬運，F_C 是完整 tuple 色集的交集，像不依
置換選擇。搬運全部可搬運原分量後，E_r=R_r∖F_Cr(p)，每側至多一份
未知，無未知時 E_r=R_r。A_h≠D_p；前者可有兩份同 root，後者不行。
這不是固定單一 source 染色後的 repair；全部原分量、旁支、接點、
spokes、zw、環序及同一字面色框保留，外部路徑也未移除。

新[checker](../../scripts/c5_no_mixed_root_transport.py) 只用 stdlib，
不 import 舊 checker。新[artifact](../../artifacts/c5_no_mixed_root_transport/observations.json)
保存 script/input SHA-256、record 與 geometry 的指向與 hash、原具名
context、共同 placements、全部查詢與候選以及 434 份失敗 join 證書入口。
讀取七類完成 artifacts，AA 額外讀原 t2 geometry 及 endpoints 證據，
另讀前輪 anchor artifact 逐查詢對照；全部 input 在 replay 前後 hash
相同。沒有重枚舉來源圖，沒有改寫舊七類或三假設 artifacts。

## 實際重播結果

| 核對項目 | 本輪結果 |
| --- | --- |
| 全部支援子集 × target，等色分割與所有單圈 injective lifts 的 hull 下界 | 32×2=64，全通過 |
| 四類互斥失敗形式的獨立 root-list 控制 | 16×16=256；雙空 1、只空 z 15、只空 w 15、同 singleton 4、PASS 221 |
| Retained records／保存 placements | 2,082／2,082，全通過同序／跨度核對 |
| Source 完整 relation instances／相容置換控制 | 111,152／289,332；隨 record 身份計數，未把 schemas 說成實際來源圖 |
| Target 查詢 | 4,164；不可搬運數 0/1/2 分別 2,936/1,184/44 |
| 雙不可搬運分布 | AA24、AB12、AC8，全部分屬不同 roots |
| A_h 雙分量 | 同 root 880、不同 roots 1,396；不混同 D_p |
| 原候選域與完整式／A_h 式／D_p 式的 E_z、E_w | 11,096 個候選，逐筆完全相同 |
| 舊失敗 joins 的互斥分類 | EMPTY_BOTH 0、EMPTY_Z_ONLY 184、EMPTY_W_ONLY 192、SAME_SINGLETON 58，合計 434 |
| 有上界失敗 join 的查詢 | 378；不是新增未決 target，既有 final status 均為 accept |

每份失敗保留 record、target、join index、具名 D_{p,r}、R_z/R_w、全部
候選 F、E、原排除入口及內容 hash。AA54/p₁ 位於 `failures[27]`，
AB22/p₂ 位於 `failures[162]`，其全路徑／非守恆端點控制繼續保留。
EMPTY_BOTH 無實際代表，明存 null；只在抽象 256 root-list 控制中出現。

候選去重鍵是原 record × 字面 target × 按具名分量次序排列的 F tuple，
保存原 join index；沒有對稱、E 或 target 去重。獨立重建每分量完整
搬運像或容量／穩定子上界後，比對原 joins 的完整集合與無重複性，再
比對前輪 anchor 保存的每份失敗清單。434=AA160+AB146+AC8+BB120，
與原域相同；未將重分組記作新增排除或接受。

## 本輪實跑命令

```bash
python3 scripts/c5_no_mixed_root_transport.py
python3 scripts/c5_no_mixed_root_transport.py --check
PYTHONHASHSEED=17 python3 scripts/c5_no_mixed_root_transport.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 一般／不同 hash seed 的 `--check` 逐 byte 比對相同 artifact；
生成模式只寫新 artifact。`lake build` 通過 8,827 jobs，保留既有長行、
unused simp 與 show tactic 警告。文件檢查通過 347 份 Markdown、3,521
個本地連結，涵蓋路徑／錨點／直接索引／HANDOFF；DocGraph 通過 62 份
documents、213 relations、5 families，零 errors／notes。`git diff --check`
通過；另檢查新 script／history 無尾端空白。

完成版 SHA-256（全部十份 input hashes 另見 JSON 的 `inputs_sha256`）：

| 項目 | SHA-256 |
| --- | --- |
| `scripts/c5_no_mixed_root_transport.py` | `fbd1e623f2cff244725735a9e8630890dac2dbc6700cb519b8ba305cf0d430f2` |
| `artifacts/c5_no_mixed_root_transport/observations.json` | `9a27a3b3c9b84fa64ae6f736f693ed4268d313e69d932e7cc73c4e976ad13b83` |

## 沿用而未重跑

本輪未執行三份舊 `c5_no_mixed_hypothesis_{transport,anchor,palettes}.py`
checker、`c5_no_mixed_span_budget.py`、七類／其餘十五類完成 checker、
no-mixed 初始化約與 root 預算 checker。只讀其明列 artifacts、完整
schemas、placements、joins 及排除入口；不把已保存的 eliminated 狀態
當成本輪重跑 K5／endpoint／palette 幾何證明。既有外部 degree-list／
Gallai 定理與 annulus／原路徑紙面引理沿用，未重讀外部文獻或重新證明。

其餘 mixed／唯一 degree-5 家族、雙拒絕 atlas、R 系列、profiles／閉包、
Lean axiom audit 未重跑。不修改 Lean 檔案，沒有新 Lean theorem 或
`native_decide`；8,827-job build 只是既有專案建置，不能代替新紙面證明。

未宣稱來源可實現性、完整 Σ、新 source 排除、新 target 接受、共同
repair 定理、一般共同出口或 K∞=K≤5。下一步若研究共同 repair，須
同時處理每側一份未知禁色、AB22 非守恆端點與 AA54 全路徑交換，
保留所有外部原路徑。依文件治理，HANDOFF 的研究線及進行中 tag 不變，
更新線內導覽與 STATUS；沒有另拆一份數學專題報告。

## 後續提交與發布核對

同日使用者授權 `commit + push`，將本輪 checker、完整 artifact、紙面
報告、跨度報告的後續連結、README、STATUS、研究線導覽及本紀錄作為
同一份交付。HANDOFF 的研究線與進行中 tag 不變，依治理規則保留。

提交前重算並確認上列 script／artifact SHA-256 及全部十份 input hashes
與已通過本次對話重播的版本相同；沒有其它工作區變更。沿用上節已實跑
的一般／seed=17 checker 與 Lean build，不重跑相同研究檢查；文件內容
更新後重跑 `python3 scripts/check_docs.py`、`python3 tools/docgraph check`
與 `git diff --check`，暫存後另核對 `git diff --cached --check`。
本節保存提交前核對；實際 commit、push 及本地／tracking／遠端 SHA
一致性以 Git 與交付回覆為準。
