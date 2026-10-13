# 2026-10-07：唯一 mixed 指定稽核與 U1 no-mixed44 排除

接續使用者「繼續推進」：先依導覽的窄提議核對相鄰唯一mixed四份舊排除，
再利用同一全degree-4分類推進C44″的U1。接手已有README、C44″、STATUS、
Kempe導覽的未提交修訂，以及前輪整合紀錄、scratch副本；均保留。
沒有開sub-agents、commit、push或改寫歷史artifacts。

## 成果與證據

[指定稽核](../../audits/2026-10-07-c44pp-mixed-audit/REPORT.md) 核對四份任意大小化約、
同源joint接回、run markers、S₄支援與收縮星的前提；
標準函式庫獨立verifier重算全部固定核心root pairs、支援constraints、
368,859份UNSAT proofs與6,008份明示subdivisions，全部通過。
上游全部分類／拓撲枚舉未重新稽核；E5的新證明要求仍保留。

[U1新報告](../c5_excess_two_no_mixed_core44.md) 排除相鄰no-mixed的兩-root44身份：

| 原spokes身份 | 本輪排除 |
| --- | --- |
| (2,3)，含交換 | core的w是單點D-forcer，z在triangle；第二triangle會與雙triangle無外掛樹分類衝突，唯一triangle則與其palette含D及branch強迫色不含D衝突 |
| (2,2) | 兩原binary-U各迫triangle，core恰為兩triangle直接bridge；64核心×16具名spoke接回的Σ只有830／958／1016／1020／1022，無933／941的整圖D₅像 |

**覆核更正與補完。** C44″以E6-D的t_r≤2收窄雙spoke只對933／940成立；
941仍容許三-spoke側，core內度≤3不能排其保留unit U的spoke省略。
已在C44″§5明示更正，保留當輪表的歷史語境。
本輪將雙spoke排除擴至全部344份bridge-marker核心，3,498次接回無目標Σ，
不依原收窄。單-run／雙-run／path／雙triangle各為1,440／576／458／1,024次。

新checker獨立對原接回邊集回溯34,980次，與同一完整root-pair relation的
字面spoke過濾一致。新artifact低於大型產物登錄門檻，保存全圖witnesses與逐列存活索引。
沒有擴大一般k搜尋，也沒有得到完整Σ933／941的來源正控制。

完整Σ前提的44殘留由四族縮為三族：U2相鄰m=2、U3非相鄰N1 incidence11／12／21、
U4非相鄰N2五族。no-mixed其他core型、單-root刪除例外、三列推廣與ε≥3未完成。
更新專題報告後續提示、Kempe導覽與STATUS；HANDOFF與README沿用入口。
當前窄提議由[Kempe導覽](../c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 實際驗證

| 檢查 | 實際結果／範圍 |
| --- | --- |
| `python3 audits/2026-10-07-c44pp-mixed-audit/verify.py --output audits/2026-10-07-c44pp-mixed-audit/validation.json` | 四份指定固定域PASS；2,112 transfer控制與3,386標記壓縮覆蓋全部344模板。新增run控制首輪因空tail漏處理而IndexError，修正新verifier後全量重跑PASS；舊輸入無變動 |
| `python3 scripts/c5_excess_two_no_mixed_core44.py --check` | 最終PASS：344核心、3,498接回、34,980獨立逐列查詢、target hits=0；前版64雙triangle子型的兩次重播亦PASS，但不足以代替更正後的全部域 |
| `PYTHONHASHSEED=17 python3 scripts/c5_excess_two_no_mixed_core44.py --check` | PASS，同樣數字，與新artifact逐byte一致 |
| `python3 scripts/check_docs.py` | 最終PASS：571份Markdown、6693本地連結／anchors／index／HANDOFF；941更正及全部344域入口已涵蓋 |
| `python3 tools/docgraph --include 'docs/**/*.md' check` | PASS：62 documents／213 relations／5 families、0 errors；僅正式docs |
| `git diff --check`；新檔whitespace另查 | PASS：tracked差異與全部新增code／報告／audit輸出的尾空白及末尾換行檢查；新artifact為992,965 bytes，低於1,000,000門檻 |

未重跑四個歷史producer、上游全部枚舉、ES／ER搜尋或lake build。
預設DocGraph的scratch duplicate-id既有干擾未處理；不將正式docs檢查說成全工作樹通過。
