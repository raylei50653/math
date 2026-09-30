# Mixed P₃ 中點／端點接線：保留原末端的六跨度來源排除

2026-09-30，Git 基準 `d72b6cb`。起始 main 與本地 origin/main 一致，
工作樹已有未提交的[非對稱分支](../c5_mixed_p3_asymmetric.md)成果及
相連文件；本輪在其上接續，未覆寫舊 artifacts，未作遠端查詢或 commit／push。
完整結論、前提與證明見[專題報告](../c5_mixed_p3_middle_endpoint.md)。

## 結果及證據界線

在 induced-C5 disk minimal q-core、相鄰雙 degree-5、其餘 degree-4、
唯一 mixed 原 P₃ 的前提下，contacts 恰為 zx₁、wx₂ 的全部 residual
已來源排除，含整份 root 交換、路徑反向及合成型。

完整三點關係只禁 (a,3)，只剩 E_z/E_w 為 {a}/{a,3} 或 {a,3}/{3}。
未接 root 的原 x₀ 有三條 boundary 邊，必見三個不同 q 色。把 x₀
及其全部附件保留在 x₁ 外側的原連通區塊，與兩個完整 root 側和
x₂ 構成原四環的四個同序區塊。兩型分別給 1+2+1+2，或兩段原框弧
3+3／2+4 的六邊下界。一色側跨度可以是零。

連同前層兩端接線，唯一 mixed P₃ 的**兩個不同接點、各一 root
incidence** 全部來源排除。任意 unary 大小與原 bridges／旁支皆保留；
不需 T4、Gallai／degree-list 外部定理，零 target，未新增 Lean theorem。
四區塊聯集只用於必要幾何，沒有改換 P₃ 的完整著色介面。

## 新證書與實際驗證

[Checker](../../scripts/c5_mixed_p3_middle_endpoint.py)／
[證書](../../artifacts/c5_mixed_p3_middle_endpoint/observations.json)保存：

- 500 組實際附件與完整 triple／contact／禁對 masks；112 組非空禁對，
  224 組 residual 案例，22,400 組必要側角色接合。
- 336 份整體對稱變換控制，加上原附件共 13,376 次 pinned queries，
  完整 triples、禁對、側角色及框反射／共同色置換均核對。
- 兩個生成器得到相同 570 份四區塊必要幾何；44 案例／4,400 組側角色
  無環序支援，其餘 180 案例／18,000 組在 1,032 份相容幾何中全部
  被整側支援不變性排除。零保留、零 target。
- 288 份支援不變性控制、兩段原框弧的字串下界，以及長度六、
  一色側零跨度的必要支援正控制。均不宣稱 degree／minimality 實現。

證書 833,943 bytes，小於 1 MB；未改大型 artifact manifest。
新證書綁定本 checker、capacity 及 base interface 的 Python SHA。

本輪命令：

```bash
python3 scripts/c5_mixed_p3_middle_endpoint.py
python3 scripts/c5_mixed_p3_middle_endpoint.py --check
PYTHONHASHSEED=17 python3 scripts/c5_mixed_p3_middle_endpoint.py --check
python3 scripts/c5_mixed_capacity_contacts.py --check
python3 scripts/c5_mixed_p3_asymmetric.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 checker 一般及 seed=17 逐 byte 重播均通過；容量、非對稱、完整
有序介面回歸均通過。完整介面仍核對 34,560 原圖 pinned queries、
318,720 刪邊 pinned queries、19,920 分量解除關係與 53,040 全圖 queries。
既有 Lean build 通過 8,827 jobs，保留既有 linter 警告；未改 Lean
檔案，這不形式化本輪 Jordan／六跨度論證。

文件檢查通過 361 份 Markdown／3,677 本地連結；DocGraph 通過
62 documents／213 relations／5 families，零 errors／notes。
`git diff --check` 通過；新加入的四份檔案另查尾端空白與最終換行。

未單獨重跑對稱 P₃、no-mixed 十五類／增長／搬運、mixed singleton／K2
各家族、root 預算、唯一 degree-5、雙拒絕 atlas、R 系列、profiles／閉包
或 Lean axiom audit。前層非對稱／容量／完整介面重播範圍如上，不能
將它們稱為整庫重驗。沒有新增外部文獻依賴。

## 文件與交接

新報告、checker、證書及本紀錄已接入 README、STATUS、weak-deletion
導覽與單側出口失敗核心限制。非對稱及容量報告新增有日期的後續入口，
保留原正文的當輪停止點。研究線與進行中 tag 不變，依文件治理保持
HANDOFF 的短導覽。

下一窄題是共鄰端點型 masks=(0,0,3)／(3,0,0)：前層六份必要色配置，
實際 boundary 鄰點數 (3,2,1)，保留原 triangle 及 x₂–x₁–x₀ 鏈。
不可拆分共同 contact 或直接換成 shared singleton。更多 incidences、
triangle、更大／多 mixed、逐染色 repair、完整 Σ、一般／共同出口與
`K∞=K≤5` 仍未證。

未開 sub-agents、未使用 Graphify、未 commit／push、未更新 Codex 記憶。

## 同日提交前核對

後續依使用者 `commit + push` 指示，將非對稱及中點／端點兩輪的
checker、證書、專題、研究紀錄，連同 README、STATUS、weak-deletion
導覽、容量／對稱報告及單側出口更新，一併整理為 14 個相連檔案。
前文與非對稱紀錄的「未 commit／push」保留研究輪當時的語境。

提交前 fetch 後，HEAD 與 origin/main 均為 `d72b6cb`，沒有分歧。
兩份新證書及 capacity／完整介面證書的 producer SHA 與目前 Python
一致；Lean 原始碼及鎖定工具鏈無變更。沿用本會話研究輪已通過的
新 checker 一般／seed=17、非對稱、capacity、完整介面及 8,827 jobs
Lean build；本提交輪未重跑研究枚舉或擴大驗證範圍。
補入本節後另重查文件、DocGraph 與 staged diff。推送後以本地 HEAD、
origin/main、遠端 refs/heads/main 及工作樹狀態讀回核對；發布結果以 Git 為準。
