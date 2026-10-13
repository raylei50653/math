# 文件維護規則

更新：2026-10-09。本規則管理文件角色、更新順序與查找入口；不改變研究結論。

## 按主題漸進披露

讀者先由 README／HANDOFF 選主題，再讀所屬導覽的目的、現況、主要結果與
精確未解義務，按需進入權威來源及證據。只從導覽進入也應能找到這些資訊，
不必先遍歷 STATUS 或歷史紀錄。

```text
README / HANDOFF → topic guide → canonical source entry → Lean / scripts / artifacts / audits
```

每個子題指定一個當前權威來源入口；完整論證散在互補報告時，由該入口導向
各報告，不強制合檔。共用引理引用原權威論證，不在每條研究線複製證明。
父子主題、Markdown 引用與數學證明依賴分別判定，導航樹不等於證明 DAG。
Topic／Proposition／Inference 等名稱可作局部段落組織，並非必填 schema、
一命題一檔或新 registry；按真實閱讀需求調整。

## 文件責任

| 文件 | 維護內容 | 更新時機 |
| --- | --- | --- |
| [README](../README.md) | 專案定位、閱讀路徑、基本操作 | 使用方式或入口改變 |
| [HANDOFF](HANDOFF.md) | 研究線導覽連結與進行中 tag | 研究線增減或進行中狀態改變 |
| 各研究線導覽 | 目標、項目現況、閱讀順序、精確停止點、缺口及證據／重播入口 | 該線現況或停止點改變 |
| [STATUS](STATUS.md) | 完整直接索引、後續關係及簡短狀態 | 新報告或既有結論狀態改變 |
| 專題報告 | 前提、結論、證明、證書、重播與限制 | 該主題有新證據或更正 |
| 歷史快照／研究紀錄 | 當輪數字、驗證、停止點與發布紀錄 | 保存當輪紀錄，不承擔當前優先序 |
| `paper/` | 特定論文草稿的敘事與證據 | 論文整合時；不作目前研究入口 |
| `docs/sources/` | 匯入來源原稿 | 保留來源版本；審閱結論寫入專題報告 |

HANDOFF 上限 30 行，只列導覽連結、tag 說明與治理／索引入口。
研究線使用 `- [名稱](本地檔名_guide.md)`，進行中才在行末加 `#進行中`。
可有零條或多條進行中；無 tag 不代表完成，排列不另表優先級。
HANDOFF 不放成果摘要、witness、停止點或命令。導覽維護本線現況，
STATUS 只保留短狀態及直接索引；數字、完整前提與驗證以原報告為準。
README／HANDOFF／STATUS／DocGraph 負責 Routing；導覽與跨線 synthesis
負責 Summary；權威專題報告負責 Source；Lean、scripts、artifacts、audits
負責 Evidence；歷史紀錄負責 History。這是維護責任，允許簡短背景與交叉連結。
STATUS 的狀態只作查找提示，不另存長版現況；synthesis 只擁有跨線綜合，
`c5_common_language.md` 只擁有共通語言與跨線接口。兩者引用各題來源，
不接管各題的 OPEN／CLOSED 或排程。
導覽包含目標與範圍、項目狀態表、停止點／缺口、閱讀及重播入口；
既有導覽可沿用章節。保留線不虛構正在執行的下一步，已完成線明列完成前提。
STATUS 不再追加逐輪研究及 commit／push 紀錄。歷史可大，現況入口應短。
新歷史紀錄使用 `docs/history/YYYY-MM-DD-topic.md`，同一天可有多個主題。
既有快照保持原路徑，以免破壞相對引用；不是要求全面搬動舊檔。

## 每次研究更新

每次**實質研究更新或報告更新**均觸發下列流程，由執行該輪的 Agent 或
reviewer 在該輪完成前履行。觸發核對不代表每層必須產生 diff；沒有新事實
的純重播只記驗證範圍，不假造研究進度。commit、PR merge、checker PASS
或有限搜尋零殘留，都不自行決定數學收尾。

1. 先更新或核對專題報告與證據，寫明下列必要資訊。
2. 核對所屬研究線導覽的相關子節；現況、停止點或引用改變才更新，不堆疊逐輪摘要。
3. 核對 STATUS 的對應條目／新報告索引；短狀態、直接連結或後續關係改變才更新。
4. 需保留的逐輪驗證／發布詳情放歷史紀錄，並從 STATUS 歷史區連入。
5. 只有研究線增減或進行中狀態改變才更新 HANDOFF；README 不逐輪複述成果。
6. 執行文件檢查。發布狀態以即時 Git 為準；未執行的檢查不得寫成通過。

### 修改範圍與擴大觸發

| 層級 | 何時核對 | 範圍與停止條件 |
| --- | --- | --- |
| L0 Source／Evidence | 每次實質研究更新 | 只處理該分支的命題、前提、論證、證據、replay 及限制；保留 frozen evidence |
| L1 Topic Summary／Index | 每次實質研究更新 | 核對所屬 guide 的相關子節及 STATUS 對應條目；有變動才修改，不掃改其他研究線 |
| L2 直接父主題／直接 consumers | 子分支真正 closure、正式 supersession，或已採納內容語義失效 | 必查直接父主題及直接使用該結論的摘要；更新受影響處或簡記 reviewed-unchanged 理由 |
| L3 跨線摘要／全域 Routing | L2 語義變動確實影響上層，或研究線增減／活躍狀態改變 | 才查 synthesis、HANDOFF、README；無影響立即停止 |

範圍按數學意義與文件主責決定，不按檔案位置決定。STATUS 位於全域，
日常仍只維護對應條目；同一 guide 包含多個子題，也不要求全頁重審。
L2／L3 不隨每輪進展自動展開；新共用來源確實改變跨線入口時，記明路由原因。

### 真正收尾與反向核對

Closure 指明確數學範圍內的證明義務已完整解決，或經正式裁決終止／取代。
必須明列命題、圖類／量詞、全部假設、定義內分支覆蓋、證據層與未涵蓋範圍；
不足時保持 OPEN。交付一批結果或有限域零 survivor 不能代替這項判定。

1. 對回權威來源，確認上述 closure scope；子分支收尾不推升父命題。
2. 必查直接父主題的已證／開放義務、分支清單與範圍。
3. 以 DocGraph 已宣告的反向邊、直接 Markdown 引用與已知跨線 consumers
   找受影響候選，逐份對回前提、結論、停止點及來源版本。缺 metadata 的文件
   仍用普通檔案搜尋；零反向邊不能當作沒有 consumers。
4. 只有父摘要的語義變動影響更高層，才繼續向上。父題仍 OPEN 且上層說法
   沒有變化時停在 L2；不要求每次查到 README 或重寫全圖。
5. 在現有研究收尾紀錄或已授權的 PR／Issue 回饋中簡記下列結果，不新增總帳：

```text
Closure scope / Canonical Source + Evidence
Updated: 受影響區段與理由
Reviewed-unchanged: 核對區段與不改理由
Remaining OPEN: 未涵蓋義務
Propagation stop: 停止層級與理由
```

反例、重大前提錯誤、證據失效或正式 supersession 若影響已採納結論，
**立即**核對直接使用者及受影響上游，明示暫停／失效的宣稱，不等待下次 closure。
舊快照中有日期的 OPEN 保留當時語境；不能把它誤當當前摘要，也不能覆寫它
來遮掩錯誤。實作取捨簡記「觀察問題 → 候選改動 → 需求影響 → 證據／取捨 →
採納或待裁決」；改變收尾語義、信任邊界或引入高成本強制治理，先交 owner 裁決。
本輪試點與負控制見 [Issue #4 紀錄](history/2026-10-09-issue4-documentation-pilot.md)。

研究線是否進行中只在 HANDOFF 標記；線內下一步只在所屬導覽維護。
專題報告保存當輪停止點並連向導覽，避免多處維護目前排程。
歷史中的「未解／下一步／未提交」保留當時語境；目前索引應明示後續涵蓋情形。
若專題報告的舊「下一步／未解」已被後續成果涵蓋，在頁首加上有日期的
後續狀態與直接報告連結，保留正文的當輪語境；區分圖層排除與抽象計算
是否實際更新。報告中的「未提交」可連向既有發布紀錄，不改寫歷史驗證。
若報告有數學錯誤，須在報告加日期與更正說明，不只改索引掩蓋錯誤。

## 專題報告必要資訊

新報告或實質更新的報告須含以下資訊；可沿用適合數學敘事的章節名稱。
既有報告按需補齊，不為格式一次改寫全部正文。

- 日期、來源／依賴報告與適用圖類、完整前提。
- 精確結論及不涵蓋的範圍；標明活躍、保留、已完成或被後續涵蓋。
- 證據層：紙面證明、外部定理、Python 固定域證書、Lean 普通證明、
  Lean `native_decide` 分別記錄；列出具名 theorem／script／artifact 入口。
- 重播命令與實際驗證範圍，分清本輪重跑及沿用既有證據。
- 剩餘缺口或後續報告；目前停止點連向所屬導覽；研究線標記見 HANDOFF。

固定 q 不自動提升為完整 Σ；list 介面不自動提升為 disk 實現；
有限模板不自動提升為任意大小定理；`lake build` 不表示紙面拓撲已形式化。

## 信任範圍與工作約定

工作目錄為專案根目錄。

- **Lean 普通證明**：以具名 theorem 及 `#print axioms` 為準；
  **Lean 有限 `native_decide` 證書**另含 native compiler 信任，不能混稱純 kernel reduction。
- **紙面證明／化約**與 **Python 固定域計算／拓撲證書**分開記錄；
  `lake build` 通過不表示新紙面 minor 或 disk 論證已形式化。
- 完整有序 Σ 是關係語意的基線；先共同對齊色框及 boundary，再投影。
  Pair projections、觀察桶或一次 cut 介面不自動是可安全合併的多步 state。
- 區分一般 planar C5 與 C5 是 disk 外邊界；一般 planar BAD 構造不是 disk 反例。
  固定 q 的 minor 不自動保持全部 boundary patterns 或 T4。
- 不以四色定理作搜尋 oracle，不假設待證 boundary-state 命題。
  使用文獻條件的報告須保留其前提與信任標示。
- 接手先讀文件及 `git status`，沿用既有 witnesses／證書；不重跑已完成的大枚舉。
  未獲要求不開 sub-agents、不 commit／push；不刪除研究產物或無關變更。
- 採 document-first。僅使用者 `/graphify`，或文件不足以解釋跨檔關係時才用 Graphify。
- Lean／mathlib 鎖定 `v4.34.0-rc2`；不為接手自動 `lake update`。
  Python 使用報告指定的 `uv run --with ...`；不並行寫同一 `.olean`。

發布狀態以即時 Git 為準；歷史生成器可能覆寫 artifacts，勿把重建指令當只讀 checker。

## DocGraph metadata

報告可在檔首加入 `docgraph:` front matter（stable `id`，選填 `family`、
`requires`、`derives_from`、`related`），由 [DocGraph](../tools/docgraph/README.md)
產生 family、反向關係與 D2 圖。只記錄有實際語義的關係，反向與後續關係不重複填寫；
沒有 relation 的文件合法。第一階段只涵蓋 single-spoke／two-spoke 主線及其直接輸入，
不要求補齊歷史報告。後續關係仍見 STATUS／報告，研究現況見各線導覽，進行中標記見 HANDOFF；
DocGraph 不承擔研究狀態或排程，不因本次治理調整擴充 metadata。
DocGraph 的 reverse／dependency closure 只涵蓋已解析的 metadata；Markdown
連結由 `suggest` 提出候選，不自動成為 relation，更不代表數學蘊涵。

## 檢查與搬移

```bash
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
python3 tools/docgraph check
git diff --check
```

檢查器以標準函式庫掃描 README、docs、paper 及 artifacts 中的 Markdown：
檢查 inline／reference 連結的本地檔案與 Markdown 章節錨點、直接報告索引覆蓋、
HANDOFF 導覽清單格式、tag 位置與 30 行上限。外部網址不連線檢查；不驗證數學結論或 GitHub UI。
HTML 僅辨識明示的 `id`／`name` 錨點；不支援一般 HTML 連結或完整 CommonMark 語法。
報告必要資訊由人工審閱，不以關鍵字出現判定數學內容合格。
CI 執行同一檢查；純文件整理不要求重跑研究枚舉或 Lean build。

正式 docs 與全工作樹 DocGraph 的結果分別記錄。全工作樹若因保留的 scratch／
快照重複 ID 失敗，仍報告失敗及來源；正式 docs 通過不能改稱全域通過，
也不刪歷史或 scratch 來隱藏失敗。
機器可查可達連結、錨點、索引、ID 與明確關係候選；closure 真偽、量詞／
假設是否相同、局部 soundness 能否推出上層結論、摘要是否過時仍需語義審閱。
沒有新增大型 checker／CI gate；若日後擬加自動檢查，先給真實漏失與攔截證據。

搬移時保留內容與相對引用，並檢查舊章節入口。STATUS 既有 §5–75 等錨點
保留導向歷史的相容入口；新引用應直接指向歷史原節，不新增相容章節。
舊 [HANDOFF_HISTORY](HANDOFF_HISTORY.md)、[近期交接快照](HANDOFF_2026-09-22.md)
及 [STATUS_HISTORY](STATUS_HISTORY.md) 是歷史來源，不逐句改成現況。

HANDOFF 舊 §2 錨點保留在研究線清單前，供既有歷史引用使用；新引用直接連向所屬導覽的停止點。
