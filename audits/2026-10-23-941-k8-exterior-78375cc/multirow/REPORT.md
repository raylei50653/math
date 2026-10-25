# 七列 Kempe 固定點：同一排除，無新增傳播

BASE `78375cc0e995c868c221605c24835d7e622f0091`。
四份代表合83,304個初始字面狀態，最終83,280個。只刪去隔一弧 cap
在 `01232` 列中 `01023213` 的24個字面 palette 狀態；六個其他外框列
均保留全部原 cap 支持。這重現主分支同一項排除，沒有新增來源排除。

四份代表的目標列規範殘餘仍為30／85／115／108。將其餘六個非拒絕
C5 列納入全部 Kempe 後繼後，必要閉包仍非空。控制依舊不是同一實際
外側的來源實例；共同可實現性仍 `OPEN`。

量詞與同步刪除的必要性見 [PROOF.md](PROOF.md)，結果與證書 SHA 見
[RESULTS.json](RESULTS.json)。完整壓縮證書為
[cap 0](CAP_0_COMPACT.json)、[cap 1](CAP_1_COMPACT.json)、
[cap 2](CAP_2_COMPACT.json)、[cap 3](CAP_3_COMPACT.json)。每份保留全部
最終字面狀態、六個 partition 選擇及全部刪除輪，並封定同一 BASE、
原輸入 SHA 及 `strong=true`。

[獨立 checker](check.py) 不 import 兩份 explorer；由原邊重算274個
完整 fibres 及全部 lifts，核每個保留狀態全部六個 partition、所有
cap lifts 與完整分量子集的後繼，並重新窮盡被刪狀態的外側 partitions。
[正常重播](CHECK_NORMAL.json)與 [seed17 重播](CHECK_SEED17.json)均為
全四代表 `PASS`，使用同一份最終 checker SHA。每次獨立重建1096個
fibres／818個 full lifts，核499680個保留狀態二色 partition，並核實
24個刪除。[十項反控制](NEGATIVE.json)全部拒絕；
[只給 cap 0 的範圍控制](CHECK_PARTIAL_SCOPE.json)正確只回 `PARTIAL_PASS`。
以上 finite controls 均 triggered and holds；實際外側來源仍未觸發。

原始及封定前輸出已無損 gzip，原 bytes 的 SHA 與壓縮檔 SHA 保留在
[RAW_ARCHIVE.json](RAW_ARCHIVE.json)。重播最終證書的指令為：

```sh
python audits/2026-10-23-941-k8-exterior-78375cc/multirow/check.py
PYTHONHASHSEED=17 python audits/2026-10-23-941-k8-exterior-78375cc/multirow/check.py --seed 17
```
