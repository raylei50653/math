# 三點弧研究：E-ARC2、完整 N2 真核心排除與原55大小界整理發布

2026-10-11；整理開始時 HEAD 為 `f428f6be3ee1eb59e3cb0b356239c4f16c4a6444`。
使用者授權「整理目前三點弧相關研究 commit + push」。本輪整理既有未提交成果，
核對論證、證書、直接 consumers 及重播依賴；沒有新增來源搜尋或 Lean theorem。
各原報告保留其生成基準、當輪檢查數字及「未提交」語境，發布狀態由本次 Git 提交定位。

## 1. 成果鏈與精確範圍

共同目標及紙面等價見 [synthesis §8.1](../c5_research_synthesis.md#81-猜想-e超額拒絕定律)。
在原域 `1≤|Q|≤4` 中，沿用已證 ε≤1 層後，完整猜想 E 等價於
`ε=2 ⇒ Q 包含於連續三點弧`。給定 ε≥3 的來源自動滿足 E 的數值下界；
這不等於已證完整 Σ933／941 的來源必有 ε≥3。Q=B／932 屬另列的較強版本。

| 權威來源 | 已證結果與接入範圍 |
| --- | --- |
| [真子圖單拒絕](../c5_excess_two_arc_pair_critical.md) | 原域反例的每個有效真子圖至多拒絕一列；任意兩個不同拒絕列的 minimal cores 聯集為原 G。沿用低 ε、兩-root44排除及至多一列單-root例外 |
| [原分量共同重色](../c5_excess_two_arc_component_slack.md) | 同一原分量的重色 slack 至多涉及一個拒絕列；完整 N2 前提接 N45-U 後，全部原分量及 incident 邊必留，真 core 只省一條原 root-spoke |
| [末端 block 與全部真核心排除](../c5_excess_two_arc_spoke_closure.md) | 完整 N2 的全部45／54真 cores已排；每條非框邊刪除全收，每個拒絕列只以有效原 G 作55 minimal core。無 unary 時，以同一 H 二連通及兩次 SD-A 排 spoke；含 unary 時逐項核既有完整契約 |
| [原55大小界](../c5_excess_two_arc_size_bound.md) | 同一完整 N2 域的 H 為中央 block 加至多兩個 root 葉 blocks，內度二點至多五個，原 C 為 bridge／奇環 cactus；有效 `|H|≤35−6u−3t` |

這裡完整 N2 的所有原來源契約以 [spoke 報告 §1](../c5_excess_two_arc_spoke_closure.md#1-完整來源前提與依賴)
為準：非相鄰雙 degree-5、恰兩份原 mixed、one-sided 原 pieces、完整 Σ933／941
或整圖共同 D₅ 像、全部原附件／ownership／rotation／bridges，以及同一色框的完整 relations／fibres／full lifts。
u 是原 unary 數，t 是兩 roots 的原 boundary-spokes 總數；自由孤立內點仍保留完整染色因子，
但不计入有效 H。u=0／1／2 時，有效內點至多35／29／23。

**Remaining OPEN：** 界內原55的同圖共同矛盾、完整 N2 來源排除、N1／相鄰 roots／
一般單-root例外、一般 E-ARC2、一般出口與 `K∞=K≤5`；新論證未 Lean 化。
既有至多九內點搜尋不覆蓋35點界，本輪未搜尋10–35點。當前下一窄義務見
[Kempe 導覽 §3](../c5_kempe_guide.md#3-停止點與保留缺口)，本記錄不接管排程。

## 2. 相連產物與驗證

四份主產物及所有初版／故意毀損負控制／失敗 receipts 原 bytes 均保留：

| 產物 | bytes | SHA-256 |
| --- | ---: | --- |
| [pair-critical](../../artifacts/c5_excess_two_arc_pair_critical/observations.json) | 304168 | `38c817fbd42c6362a2eab02e251fa6a96f2783fe37e519d4a4fb40429fc798e7` |
| [component-slack](../../artifacts/c5_excess_two_arc_component_slack/observations.json) | 6250157 | `e57dd4e28b1029fb53fd740da3aa79378c67fe4a336ee146dd9fda2a49105d20` |
| [leaf-blocks](../../artifacts/c5_excess_two_arc_leaf_blocks/observations.json) | 621066 | `b048d567e287807c8eaafa5aeb17a229457ed9cac1a93c5bcdb802b17c7b206b` |
| [size-bound](../../artifacts/c5_excess_two_arc_size_bound/observations.json) | 981198 | `a63e2bd7ef6c32c6f983b54064371cba3d46e20c32e78e222d3a335d59c46291` |

本輪獨立只讀重播四份 checker，normal 及 `PYTHONHASHSEED=17` 都 exit0，
逐 byte 相等。pair-critical 重算179張固定圖、4138次刪邊、206 cores及4466次
minimality刪邊；component-slack核13010份完整外部投影及208160個刪邊後局部pins cells；
leaf-blocks重算28640個原局部cells，含3372空fibres；size-bound核480／90份
具名K₅／K₃,₃ minors及58份具名cacti。**所有完整目標來源均 not triggered**；
這些有限控制不承擔任意大小來源排除或來源實現。

E3 foundation normal 重播 exit0，SHA-256
`f98f8b2bb8090c8705bd3937b876a15c83e38473699d9f5dc2f9f48afcf9cd36`，
保留原951／935正控制。另獨立核全部32個 Q 子集及原域30個非空真子集：
右端≤3，右端≤2恰等價於三點弧及不含 D₅ 像的{0,1,3}；沒有枚舉來源圖。
兩份 corrupt 產物的 verify-only `--check --output ...` 均按預期 exit1、
`artifact mismatch`，原檔及失敗紀錄未改。

```bash
python3 -B scripts/c5_excess_two_arc_pair_critical.py --check
python3 -B scripts/c5_excess_two_arc_component_slack.py --check
python3 -B scripts/c5_excess_two_arc_leaf_blocks.py --check
uv run --offline --with networkx==3.5 python -B scripts/c5_excess_two_arc_size_bound.py --check
uv run --offline --with networkx==3.5 python -B scripts/c5_excess_two_e3_foundation.py --check
python3 -B scripts/check_docs.py
python3 -B tools/docgraph --include 'docs/**/*.md' check
lake build
git diff --check
```

size-bound／E3 的 NetworkX 鎖定3.5；`--offline` 使用本機既有 uv cache，
沒有 cache 的環境依各原報告移除 `--offline`。四份新 checker 的重播參數均為只讀，
不可用未帶 `--check` 的生成模式覆寫歷史產物。

pair-critical 的46個凍結輸入（19份C44、25份ER chunks與兩個helpers）
全部是 ordinary tracked files，hash及bytes與整理基準HEAD相同。
後繼checker的凍結輸入hash均相符；E3的三份資料亦為tracked且HEAD-identical。
因此本組新checker重播不依赖ignored scratch或audit payload，也不需重建上游封存。
本輪以`git archive`將暫存tree獨立還原至工作樹外，27個相連檔案逐byte對回index，
四份新checker及E3 foundation的normal重播全部exit0、bytes／SHA與原工作樹相同。
獨立還原的正式docs DocGraph亦通過；最後僅補本文驗證紀錄，不再改checker或產物。
原工作樹的最終`check_docs.py`通過（618 Markdown、7654 local links，
anchors／index／handoff均通過）；`git diff --check`及staged whitespace亦通過。

`lake build`已通過（8831 jobs，保留既有 AttachmentOrder／SymRelabel linter warnings）；
build不承擔新紙面證明。正式docs的DocGraph通過（62 documents、213 relations、0 errors）。
另實際執行全工作樹DocGraph，因保留audit／scratch快照的重複ID而exit1
（62 duplicate-id errors）；保留這項失敗，不刪快照或改稱全域通過。
未重跑上游低ε／44／N45／SD-A全部分類、來源rotation、ES／ER搜尋或所有歷史verifiers。

## 3. 文件反向核對與發布邊界

- Closure scope：只限上述完整 N2 的45／54真cores；原55只得到必要大小界。
- Updated：四份權威報告與checkers／產物、N45§2.13–2.15、Kempe guide、STATUS、
  degree-5 guide／interfaces、雙色唯一缺口的後續涵蓋，以及synthesis §8.1。
  README／HANDOFF保留研究線角色，將猜想E的現行入口說清楚；沒有新增研究線。
- 本輪措辭修正：刪邊後局部fibres全非空與外部full lifts空cells分開；
  pair-critical索引補完整N2的後續涵蓋；裸§2.14改為N45具名連結；
  原Σ933／941的ε≥3待證下界與給定ε≥3時E自動成立分開。
- Reviewed-unchanged：歷史audit／seal／失敗控制與所有上游凍結bytes；
  其他研究線、一般R31、一般出口及Lean既有定理。
- Propagation stop：完整N2收尾影響直接父題及已有E-ARC2跨線摘要，故同步相關L2／L3入口；
  父N2及E仍OPEN，停止於這些實際consumers，不擴全線重枚舉。

兩路只讀核對分別檢查紙面依賴／量詞與checker／hash；未發現阻擋本次整理的缺口。
這不新增一項封存採納流程，不把零來源觸發、checkers或build提升為Lean證明。
本輪只stage相連檔案後commit並push main；實際發布完成以
`HEAD=origin/main=remote main`及工作樹乾淨的readback為準。提交SHA由包含本文的commit定位。
