# 第三輪獨立重播與交叉審查

2026-10-15，BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
各組自驗之後，主 agent 另執行正常、seed17與損壞證書重播，保存
命令、完整輸出、退出碼及重播前後 SHA256。所有重播均不寫證書。

## 1. 原組證書的主 agent 重播

```sh
python3 -B audits/2026-10-15-xor-batch-descent-6ddea32/check.py --check audits/2026-10-15-xor-batch-descent-6ddea32/certificate.json
python3 -B audits/2026-10-15-six-pin-lifts-6ddea32/check.py
python3 -B audits/2026-10-15-kempe-common-graph-6ddea32/check.py
python3 -B audits/2026-10-15-kempe-common-graph-6ddea32/verify.py
```

以上正常與 seed17 均通過。三份收據：

- [匹配重播](matching-replay.json)：正常、seed17；漏雙環交換及錯聯合
  奇偶兩份證書均拒絕。覆蓋28024條基本交換、76294對構造路徑，
  同一36點圖的兩份標記分列，沒有把重複PM當新來源。
- [六接點重播](six-pin-replay.json)：正常、seed17；刪完整lift、刪空fibre、
  錯返回側均拒絕。三張圖的 J 全染色240／288／24，U全染色864／960／96；
  完整4^6與4^7 fibres及全部r lifts均保留。
- [Kempe重播](kempe-replay.json)：重建器與獨立proof-tree verifier皆正常、
  seed17通過；漏函數、加假邊、漏搜尋分支三種損壞均被兩程式拒絕。
  18變數／53約束的完整47節點搜尋樹給25弱函數、41邊、1056處斷開。

各組另有 exclusive-create 拒覆寫自驗收據；主 agent 沒有重新生成
或覆寫原組證書。所有輸入／checker的重播前後雜湊一致。

## 2. 主 agent 的三份獨立實作

三個程式都不 import 被審組的 checker。

1. [check_marked_patterns.py](check_marked_patterns.py)：窮盡432份 proper
   六點賦色（96 E）與165個三標記cycle partition，獨立核三邊色差等價、
   safe cube公式及「可返回即有單環返回」。完整小證書見
   [marked-patterns.json](marked-patterns.json)。
2. [check_common_graph_independent.py](check_common_graph_independent.py)：只從
   canonical source transitions建約束，以固定變數順序與前向過濾搜尋，
   429節點得到同25個函數。再直接核全432個literal states的102000項
   交換條件，41邊最大圖與首個t/q斷開一致；見
   [common-graph-independent.json](common-graph-independent.json)。
3. [check_vertex_kempe.py](check_vertex_kempe.py)：以固定頂點順序重枚240份
   12點球面完整染色，直接在原頂點圖算普通Kempe分量。216份E-free
   染色的全部1296次單分量交換都封閉；另核全部度五、所有三角皆面及
   split-U的(z,s,t)度數(6,4,2)。見
   [vertex-kempe-independent.json](vertex-kempe-independent.json)。

這三份也各做正常、seed17與損壞拒絕，收據見
[independent-replay.json](independent-replay.json)與
[vertex-kempe-replay.json](vertex-kempe-replay.json)。合計本目錄記錄28次
主 agent 重播，14次接受與14次預期拒絕，全部符合預期。

## 3. 循環交叉審查與紙面採納

- [Kempe組審匹配](../2026-10-15-kempe-common-graph-6ddea32/CROSS_REVIEW.md)：
  接受最多兩環連通、批次手術及局部色involution。另以獨立程式重枚
  全部PM、28024條交換、完整Tait fibres與起點聯合delta。具名83→187
  的獨翻delta為0、0，聯合為+2，補強不可誤相加的界線。
- [六接點組審Kempe](../2026-10-15-six-pin-lifts-6ddea32/CROSS_REVIEW.md)：
  核S4自由軌道、完整函數域、原圖到最大type graph的homomorphism及
  路徑投影；比對主agent不同搜尋的完整函數與邊表。接受任意有限原點數
  的single-valued equivariant lift障礙，保留hidden-state covers。
- [匹配組審六接點](../2026-10-15-xor-batch-descent-6ddea32/CROSS_REVIEW.md)：
  核三邊等價、雙色環一側平移的完整原圖lift、safe cube量詞與平面控制
  的來源缺失，另以原邊及完整染色資料獨立核對。

主 agent 也逐步審查三份紙面證明，未發現上述採納域內的阻斷缺口。
一般引理由紙面證明；數字與特定模型排除由明列有限證書支持，未宣稱
Lean形式化。沒有用控制的零來源實例證任何來源排除。

## 4. 不變性與文件界線

[check_bundle.py](check_bundle.py) 核前兩輪234份檔案的內容及成員集合、
五份原權威與凍結副本、HEAD、tracked diff、十二個新舊audit的untracked
範圍、新增文件連結、Python語法與空白。最終收據見
[bundle-check.json](bundle-check.json)，本輪成果封存見[MANIFEST.json](MANIFEST.json)。
`git diff --check`亦通過。

舊輪workspace whitelist不包含本輪四目錄，本輪明確使用擴充scope的
新checker；舊checker與舊收據不改。沒有重跑或宣稱全樹DocGraph、
Lean build、外部來源全集或新點數界。無commit／push。
