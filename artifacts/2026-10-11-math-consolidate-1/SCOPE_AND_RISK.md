# MATH-CONSOLIDATE-1：範圍、風險與審查界線

日期：2026-10-11。讀取基準：`8c56b76922a1c7ac4c011096f2041b49c4a67cc8`。
本目錄是 read-only mathematical synthesis 的新交付；內容是整編提案，沒有採納新定理。

## 權威與範圍

目前數學狀態以 [N45 canonical](../../docs/archive/reports/c5/excess/other/c5_excess_two_nonadjacent_unit_core45.md)、其具名採納 review／history 為準；原 worker 的 candidate、pending、舊 residual 敘述保留當輪語境。
已核對 HANDOFF、STATUS、Git HEAD 與 canonical。既有文件足以說明跨檔依賴，本輪未使用 Graphify。

只整理 N45 已採納窄命題、BR-SD-1a／1c／1e／1g、直接 degree-list／Gallai／palette／minimality 依賴，以及共用這些步驟的 U／LOW／HIGH／LONG 結構。
不重枚舉來源，不建立新 source，不重跑歷史封存工具，不重開已採納分支；舊 replay、seal、certificate 的通過狀態是引用既有紀錄，不是本輪重新認證。

「最小已知充分前提」有兩個層次：來源排除仍使用目前完整採納合同；抽出的局部步驟只列其證明實際需要的充分條件。後者較弱不代表已獲授權縮小 canonical 合同，也不宣稱是邏輯上的最弱前提。

## 不可壓縮的資料

每次應用均固定一份原來源、同一 literal 色框及指定 β；G、X=M、刪 contact 圖各用自己的原邊與 lifts。
完整資料包括 ordered contacts、shared 頂點單一座標、actual attachments／supports、ownership、rotation、原 bridges、全部原 witnesses、完整 relations、空 ambient fibres、tuple preimages、full lifts，及被 effective-H 忽略的原座標與允許色因子。
共同 D5／S4／root swap 必須一次搬運整份資料。不得分別正規化 pieces 或把不同 β 的禁色需求相加。

完整原 degree 包括 B 附件；原 U 或其他 piece 被省略仍按原 G 收盾費，spoke 不收 piece 盾費。
原 G 的 Σ-critical 不供給 X 的同 β minimality；X=M、自身拒 β、自身刪邊 witnesses 都須逐項保留。
β-minimal 不推出二連通。原 G 或原 X 的 minor 只能證該圖非平面，不能當染色 replacement。

## 四類處置

| 類別 | 本輪結論 | 審查後才可做的事 |
| --- | --- | --- |
| **可安全精簡** | 接合／原 spoke filter／slack 的重複證明可引用共同接口；1c 的 terminal 路線已在原 PROOF 證出且覆蓋全部 degree-legal 接點；HIGH1 的最終 G-lift 反證可獨立於 supporting MAP 分類呈現 | 另授權後，編修 canonical 的引用與證明組織；原 audit 留存 |
| **需要新證明** | 跨更多 W／多接點旁支、不同環接線、失去 pair support 後的 TERM／PB 路線、一般可恢復 Δ-fibre 非空或一般 minimality 繼承 | 新命題、獨立證明與採納審查；BR-1a／1e 的 private-D 步驟未使用 pair support，較弱來源登記須另做 scope／adoption review，不能擅改合同 |
| **不可合併** | U 整份省略與 S 刪 spoke；LOW1／LOW2 原 incidence；HIGH 的 (2,1)/(2,2)/(2,3) contacts；LONG 的 owner=r/s；BR 的零／一／兩旁支；不同 β、不同來源及 G/X minors | 可共用局部引理，定理合同仍分列 |
| **仍 OPEN** | N45-S-NOU-LS-PAIR 父身份、未覆蓋多旁支／其他 splits 或骨架、R31、其他45／54／原55／無45／54來源、一般 N45／N2／E、ε≥3、出口與主命題 | 保持 OPEN；精確已排子域不重新登記為 OPEN |

## 具體失敗模式

| 風險 | 必須保留的防線 |
| --- | --- |
| HIGH2 使用四色 γ 卻稱有未用 Dγ | JOIN／RESTORE／PALETTE 對全部 proper γ；未用色恢復只對 proper **三色** γ。既有 finding 與 literal counterexample 保留 |
| cutpoint list 含 D 就分給每個 incident palette | incident-union 只能確保至少一個 palette 含 D。1c 原反例保留；1g 使用全 incident palettes 與 J2 屏障 |
| 把 1c terminal 套到 1e／1g | 旁支可能接 q 或臂內點，破壞唯一末端／無額外 C 邊前提；改用各自已證 witness／barrier 路線 |
| 把非空 root-pair 聯集說成每個固定 pin 非空 | T1／q0 等只能引用其原存在性量詞；保留空 fibres 及 null source preimages |
| 用 transfer 恆等式推出可恢復非空 | 恆等式只描述 fibres。完整 LONG K1–K12 已給 Δ≠∅；一般 **Δ 的可恢復 r-fibre 非空**仍未證，兩者不同 |
| 忽略 effective-H 外座標後宣称完整雙射 | 先補原允許色乘積；只做投影時不能宣稱 bijection |
| 混掉 SD-A 與 BR 前提 | SD-A 要 H_M 二連通；BR 四支不依二連通或 SD-A |
| 用有限 controls／零 trigger／seal 代替任意大小證明 | paper、正式外部 theorem、finite calibration、actual source、custody、Lean 分層；actual source not triggered 不承擔來源排除 |
| 洗掉 LONG-S 的歷史信任缺口 | q0 的 SF-QX／SF-T2-EXTEND／E2 paper／historical finite-terminal 依賴與兩份缺 BASE blob finding 留存；T1／q2 的新存在性另列 |

## 修改與發布界線

本輪新增六份整編提案；canonical、STATUS、HANDOFF、既有 audits、seal、certificate、歷史 review 均不得變動。後續依使用者「整理後 commit」授權，僅本地提交六份提案；不 push／PR，不關閉 OPEN 或新增 Lean claim。
具體壓縮前後的文本只在暫存 preview 計算；preview 未覆寫 repository 原檔。
文件重構與新定理採納各需另行授權。這不是要求本輪追加批准：已授權的整編交付會完整完成。
