# C9 完整介面獨立覆核

2026-10-13。BASE `6943561e644e7598342d1ccd7df44dac0ebcd5cf`。
覆核對象為 [最終 v2 證書](../finite/certificate.v2.json.gz) 及
[幾何採納](../geometry/ADOPTION.md)。本 checker 不 import producer、舊 generic
collar checker 或其算法；只讀父包凍結輸入清單、最終證書，並獨立重建。
全部命令與 SHA256 見 [VERIFICATION.json](VERIFICATION.json)。

**結論：PASS。** 全部435份完整查詢、原 annulus full fibres、Kempe
obligations、quotient masks、原有向面及 rotation paths 均逐項一致。
正常與 `PYTHONHASHSEED=17` 重播均通過，八個語義負控制均拒絕。

## 1. 原圖／色框及獨立方法

[check.py](check.py) 自行用 restricted-growth DFS 生成有序 C9／C5 proper
色軌道，得820／10列；C9 三色85列、四色735列，全部 literal proper 指派
共19680。色名只對整份字詞取一次全域商；保存的 annulus lifts 仍是原
literal B 色及固定 literal C 色，沒有分別正規化 pieces。

以八個位置選四個 bars 生成70份有序 e，而非 producer 的遞迴 compositions。
各原 C 順序依五個 a、四個 y 的具名 attachment 重建；每個 support 從實際
annulus 邊取得。support 本身是原 B 點集合，故比較具名集合並拒絕重複，
不把 `{b4,b0}` 的列舉次序當成新幾何；C 原點順序則逐點完整比較。

自行建立14份有向三角面，逐原邊檢查內部兩側有反向 darts，B 以正向
cyclic order 定外框、C 以反向定內孔。從有向面的一個頂點後繼鄰點到前驅
鄰點，重建 clockwise rotation path；B 點從下一 B 鄰點走到上一 B 鄰點，
C 點从上一 C 鄰點走到下一 C 鄰點。每條 path 含所有原鄰點恰一次。
其 oriented triangle sets（只允許面內 cyclic rotation）及全部14條原
rotation paths 與 v2 證書一致。

對每份固定 literal C9 指派，把所有 C–B 原邊變成 B 點的實際禁色；以
五點 DFS 枚舉全部 proper literal B 指派，閉合原 B cycle。只用整份 B
字詞的 S4 商來定位十列，仍保存14個原點的 literal full lift。每個 fibre
包括空集，且逐份比對完整 lifts；不是只比較 column support 或總數。

## 2. 獨立 noncrossing 與 Kempe 重建

非交叉 partitions 不使用 Bell partitions 加 crossing 篩選。取首點所在
block 的全部可能點集；該 block 相鄰點之間的各開區間獨立遞迴，再與
首 block 黏合。任一 noncrossing partition 的其他 block 必完全落在其中
一個 gap，否則與首 block 交錯，故此遞迴既完備且表示唯一。得到4862份
原九點 partitions；排除含相鄰原 C 點於同一 block，留下232份 independent
quotient partitions。

對每份 C9 列與三份互補色對 split，保留每個 block 同屬一個色對，且
相鄰同色對原 C 點屬同一 block的全部 partitions。各 block 依同一 literal
色框獨立 flip，對**整份**所得 C9 字詞全域正規化，取得該 partition 的
完整 joint orbit。820×3份全部 option sets 與 producer 完整 table 相等。
這些 options 是必要上界；沒有宣稱每份 partition 在某個原 H 可實現。

逐查詢以普通 support sets 重建同時刪除的每一輪，而非使用 producer 的
bit-mask 演算法。初始集合只收完整 column 包含於目標的原列；ear 分支
再交同一原 chord／W5 row mask。若某 split 沒有一份完整 component orbit
全部包含於目前上界，就刪該列。重建所有 initial、每輪 before/removals、
fixed point、完整外列 union、缺少的 quotient indices 與最終 status。

每份 quotient mask 從原九點 block 的同色條件重建，不同 blocks 可同色。
ear 幾何另排除識別原 chord 兩端的 blocks，以免產生 loop。mask 和 ear
条件使用同一 C9 指派，沒有只把各自可行的 marginals 相乘。

## 3. 覆核結果

* 70份原具名 collars；75份候選 W5 ears；合计145份幾何、435個查詢。
* 574000個 annulus fibres，530845空，48450份完整 literal annulus lifts。
* 全部225份 ear 查詢由 transfer／Kempe 排除；非空 fixed point 亦未被
  當成完整 target 實現。
* induced C9：932排50留20；933排44留26；941由 transfer／Kempe 排28，
  source-relative quotient 再排4，留38。共84份必要條件殘留。

另獨立核對採納文的具名残留範圍：三支 h=4 殘留均有 `max e_i≤3`；932
恰為兩份2位於非相鄰原 B 位置的5份 e，或三個連續正项 {2,1,1} 的15份 e。
這給 h=4 下三支原 B degree≤7、932 原 B degree≤6 的窄必要界；不推廣到
h≥5，亦不把這20／26／38項當作同圖來源。

## 4. 紙面接入與界線

核讀 [geometry/PROOF.md](../geometry/PROOF.md) 的原小 cap／degree 論證：
C9 chord 短距2／3給空 C3／C4 的非端點 degree2耳；短距4則必為 W5，
其中三個短弧中點皆為 A。兩條不同 noncrossing 距4 chords 會需要六個
不同 A，中間只有五個，故最多一條。由此70 induced＋75 ears確實覆蓋
同一原 h=4 来源，不依賴有限來源圖搜尋。

全部225 ear 必要查詢排除，加這個紙面幾何覆蓋，足以採納
`h=4 ⇒ 原內 C9 induced`。本覆核不另重證父包的 no4ct 下降引理；商圖
可染性仍只在固定最小來源的 `N≤k+5` 使用，C9 q-block quotient 的點數
是 `k−9+q≤k`。沒有使用普遍四色定理，沒有刪除932的一般分支。

84份殘留只是完整必要條件上界。其同圖共同實現／排除、h≥5任意來源及
一般 `K∞=K≤5` 仍 OPEN；实际目標來源 `not triggered`，不能以此排除。
沒有新增 Lean 定理，也沒有把 paper topology 當作已形式化。

## 5. 語義負控制與保留的失敗紀錄

八種變更皆由與獨立重建資料的相同比較拒絕：原 C 名字逆序、刪 literal
full lift、忘原 ear chord／中心 mask、容許 loop-producing endpoint
識別、刪一份 joint Kempe orbit、把殘留誤標來源排除、反轉一個原三角
面的方向、反轉一條原 rotation path。

接手時 partial checker 有一處未閉合的 f-string；首次語法失敗保留在
`normal-negative.log`。修復後，prototype 的正常／seed17 比對因 support
`[4,0]` 與 `[0,4]` 的單纯集合列舉次序不同而失敗，保留於
`normal-negative-v2.log`、`seed17-negative-v2.log`；改為具名集合加無重複
檢查。上述都屬本 reviewer 修復，不改數學查詢狀態。

producer 後續將原 unordered face triples 改成實際有向面，另加 rotation
paths，並 exclusive-create v2 證書；舊 prototype 留存。本 reviewer 的
最後正常／seed17 logs 是 `v2-final-normal-negative.log`、
`v2-final-seed17-negative.log`，只以此最終 schema 和逐項比對結果作採納。

```bash
python3 -B audits/2026-10-13-c5-no4ct-frontier-6943561/c9/review/check.py --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-c5-no4ct-frontier-6943561/c9/review/check.py --negative
```
