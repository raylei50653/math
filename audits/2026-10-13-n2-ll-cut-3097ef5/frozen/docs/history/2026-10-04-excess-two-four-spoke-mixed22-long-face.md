# 2026-10-04：B₃，mixed-(2,2) 同骨架原長 face 的 leaf bridge／原 K₅

使用者要求接續 B₂，固定 W933-101／W941-139 的原長 face {0,4,3}，
保持七種 contacts 身份、完整 C、actual attachments、四接點 fibre
及原 G 為 (5,5) q-core；研究 shared-contact leaf bridge 與原外部路徑，
完成長 face 窄引理或保存具名殘留即停。接手
HEAD=`0e3812712b68f57927df86f30a07bb8074e090f9`，
cwd=`/home/ray/developer/ai/math`；原工作樹多輪未提交成果全部保留。
本輪未 commit／push。

[B₃報告](../c5_excess_two_mixed_core_four_spoke_mixed22_long_face.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py)、
[helper](../../scripts/c5_excess_two_four_spoke_mixed22_long_face_controls.py)、
[observations](../../artifacts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face/observations.json)
構成獨立本層證據。原 B／B₂ producers、observations、全部舊具名 frames
與整合稽核歷史不改寫；README、B／B₂後續狀態、Kempe、STATUS 與
全線 synthesis 接入新報告。HANDOFF 研究線與 tags 未改變，依
DOCUMENTATION 保持薄導覽；不向 HANDOFF 塞入輪次成果或重播命令。

## 任意大小窄結論與停止點

**固定兩份長 face 的七種身份全部來源排除，零長-face 殘留。**
跨全部拒絕列／合法 root pairs 的同圖 tightness 迫 shared 點沒有
原框附件、C-degree 二。假設 shared private leaf bridge 內度一，
完整 degree 四迫額外接框；0／3／4三種原鄰點分別由 row6／row1／row1
的 exact list slack 排除。只排 degree 一的 shared leaf；degree 二
的 shared contact 可在原內部 bridge 鏈，本輪仍保留。

Terminal cycle 的 private exact lists 在原 pairs (3,1)、(2,3) 相同，
五個有序 signatures 區分 nonowner 04、nonowner 34、a0、b3、shared ab。
每型實際 hubs 相鄰；其原 X 減 hubs 連通，C 減相鄰 private u,w
保持連通且由剩餘原 contacts 或另一 terminal leaf 的實際框附件
接入。五袋及十對原鄰接提取原 K₅ minor，無須添加 apex 或換原 C。
K₄ blocks 沿 B₂ 的原四 tethers 論證排除，不依賴固定 root pair 的
逐邊 minimality。紙面引理經獨立 read-only 覆核。

外部依賴 live 核對 [Dvořák 原 PDF](https://iuuk.mff.cuni.cz/~rakdver/barevnost/gallai.pdf)
的 Lemma 7、Corollary 8、Theorem 10；同圖 exact degree lists 符合
其前提，不使用四色定理 oracle。

B₂ 短 face 與本輪長 face 是兩份獨立證明；合用後才封閉這兩W的
全部原 mixed-capable faces。原 B 的20／20必要骨架證書保持歷史層，
其他骨架未排，沒有把必要表改成來源 catalogue。完整 R_C、joint、
fibres、actual 附件與原 paths 保持；minor 不作其不變量。
未證 mixed22 整型、ε≥3、來源實現、一般出口或 K∞=K≤5，未新增
Lean theorem。**在此停止**；目前入口由 [Kempe導覽](../c5_kempe_guide.md)維護。
933原04／12長 face 的 shared 附件{4}是不同骨架，仍保留，不續做。

## 固定證書實際覆蓋

- 七身份 × root swap 的14份完整 degree 長-face 圖：840直接原圖 joins、
  13,440 fibres（10,024空）、560 spoke接回、420 swap checks、3,360
  獨立 global S₄ R_C、257,280完整 joint witness 搬運核對。
- 另2份 S00 shared internal bridge 正控制：共享點7在原鏈
  11–8–7–9–12，兩條 incident C 邊都是原 bridges，附件∅、C-degree二。
  120 joins、1,920 fibres（1,432空）、80接回、60swap checks、480
  S₄ R_C、16,656完整 witness 搬運核對，與14份 cycle controls 分開保存。
- 兩 masks 共52份 actual attachment候選、546份拒絕row／pair精確list
  算術；全部容許候選保留完整 lists，排除候選有同框slack witness。
  shared leaf bridge每mask三份，共6份；主ledger另列3份共同反證。
- 30份完整 degree 原leaf K₅：兩種nonowner支援的長3／5／7 cycles，
  a-only／b-only，以及Pstraight／Pcross shared葉接另一04／34 nonowner葉。
  原 bridge chain長1／3／5，300條原branch鄰接、42份actual外部路徑。
- 沿用兩份條件式原K₄四tethers證書，長度(1,1,1,1)／(2,3,4,5)，
  共20原鄰接；未補未用degree邊，與完整degree圖分開標示。

固定圖不宣稱disk、target Σ、criticality或來源實現。共16份relation圖
的完整R_C／six-role joints／四接點fibres均保留整份原coloring witnesses；
不以marginals、counts或獨立色框代替原relation。任意大小結果由紙面
引理承擔，沒有重開來源graph catalogue。

## 重播與驗證範圍

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_short_face.py --check
python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
uv run --with-requirements requirements.txt python tools/artifacts.py status
git diff --check
```

未重跑其他incidence、任務A／P₃、原D／D₂整合稽核、R系列、一般
出口／Kempe閉包或Lean axiom audit，沿用各原報告證據邊界。
原D／D₂中關於B₂停止點的當輪快照保留，沒有回寫新B₃結論。

## 貼用摘要

> B₃完成固定W933-101／W941-139、原01／23長face{0,4,3}的任意大小
> 原K₅窄引理，七contact身份零長-face殘留。shared degree一leaf bridge
> 由跨拒絕列slack排除，degree二internal shared bridges仍保留。
> 五leaf型nonowner04／34、a0、b3、sharedab由原外部路徑接成第五袋。
> 完整原C／四接點R_C／joint／空fibres與actual附件保持，不作minor不變量。
> 14cycle＋2internal-bridge完整degree圖，共960joins／15,360fibres，
> 30原leaf K₅；紙面＋Python、未Lean化。B₂短face與B₃長face各自證成，
> 僅兩W全部faces封閉；其他骨架、mixed22整型及ε≥3保留。在此停止。
> 重播 `python3 scripts/c5_excess_two_mixed_core_four_spoke_mixed22_long_face.py --check`。

## 最終檢查紀錄

B₃ default／`PYTHONHASHSEED=17` 兩次逐 byte `--check` 均通過；
既有 B／B₂ `--check` 通過。原 B artifact SHA256 保持
`f7168b09b9a19957e0c3be50cbd9382cc4fa650619a563c5819962c4a3c254de`，
原 B₂ 保持
`2164f870d128ee22ead68f8d7a4a900cddb06314ce52f97884ac86e08a6061bc`。
新 B₃ observations 為 **18,465,674 bytes**，SHA256
`513c582f1067306ae67d8ef1fab46ba6c6fe5889923c95923688ba4a2aaaebd7`。
依大型 artifact 政策記錄新路徑至 MANIFEST／生成 .gitignore；本輪
`record` 明列且只處理 B₃ 路徑，沒有刷新其他 artifact。
接手驗證快照的141個manifest舊file entries／136個fingerprints及
dependency entries均原樣；並行另一研究亦新增條目，未把它算成本輪成果。
記錄後 artifact status 為 **ok=143**。

`lake build` 通過（8,831 jobs，僅既有 lint warnings）；
DocGraph 通過：62 documents、213 relations、5 families，0 errors／0 notes。
兩個新 B₃報告的14個本地連結／錨點與 STATUS 直接索引均通過；
兩新scripts的py_compile及`git diff --check`通過。

全倉 docs 檢查第一次有7個缺失連結，指向並行A₃／C₃尚未完成的
歷史文件；後一次A₃文件已補齊，剩4個C₃歷史連結，528 Markdown
files、5,473 local links。本輪未代寫其他研究的歷史結論；收尾結果
另記如下。

最終全倉文件檢查通過：**529 Markdown files、5,477 local links**，
錨點、STATUS直接索引及薄HANDOFF全部通過；C₃歷史由並行原工作
補齊，本輪沒有修改其結論。

獨立read-only稽核以原edges自行BFS，驗證30minors／300原鄰接／42
actual paths、32份原block ledgers，以及全部16relation圖的degree、
actual附件、160rows／960variants／15,360fibres。逐份驗證2,646個
R_C witnesses、11,414個joint witnesses、11,414個fibre witnesses，
共25,474次原邊合法性／ports／shared相等座標核對，零artifact錯誤。
兩份S00各有兩條原shared incident bridge刪除後C斷開，共4checks；
沒有另枚舉solver或變更artifact。獨立稽核最初使用未排序owner順序的
斷言不適用root swap [6,5]；改為比較owner集合後通過，原payload保持。
