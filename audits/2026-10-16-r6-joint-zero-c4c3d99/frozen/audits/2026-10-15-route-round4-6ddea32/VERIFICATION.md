# 第四輪重播、獨立原邊驗證與交叉審查

BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。各組自驗後，主 agent
以 [run_replays.py](run_replays.py) 另執行唯讀重播；每份收據保存完整
命令、輸出、退出碼、耗時及重播前後SHA256。沒有重寫原組證書。

## 1. 主 agent 的正式重播

| 證據 | 接受 | 預期拒絕 | 範圍 |
| --- | ---: | ---: | --- |
| [matching-replay.json](matching-replay.json) | 2 | 2 | 正常、seed17；錯W權重、漏Tutte障礙 |
| [geometry-replay.json](geometry-replay.json) | 4 | 4 | 兩checker正常／seed17；漏lift、漏空fibre、錯all-r、錯hub返回 |
| [kempe-replay.json](kempe-replay.json) | 2 | 3 | 正常、seed17；漏全染色、錯monodromy、錯cover rank |
| [independent-replay.json](independent-replay.json) | 6 | 2 | root三程式正常／seed17；兩份損壞證書 |

合計25項正式重播，14次接受、11次預期拒絕，全部符合預期；輸入與
checker雜湊前後一致。各組另留exclusive-create拒覆寫自驗收據。

首次Kempe正式checker重播曾因diamond邊表的tuple/list表示差異而
比較失敗，見[cover-preliminary-failure.json](cover-preliminary-failure.json)。
原組將checker輸出正規化為JSON list，保留原證書；上表是修正後的
完整重播。沒有把該初次失敗記成PASS。

正式命令的入口為：

```sh
python3 -B audits/2026-10-15-three-edge-matchings-6ddea32/check.py --check audits/2026-10-15-three-edge-matchings-6ddea32/certificate.json
python3 -B audits/2026-10-15-j-source-geometry-6ddea32/check.py
python3 -B audits/2026-10-15-j-source-geometry-6ddea32/check_two_palette.py
python3 -B audits/2026-10-15-kempe-state-covers-6ddea32/check.py
```

各plan檔列出seed17與全部損壞證書的精確參數。正常驗證是完整重建後
與證書比較，並非只看證書內的PASS字樣。

## 2. 主 agent 的獨立實作

三程式均不import被審組的checker。

1. [check_full_j.py](check_full_j.py)：直接由兩三角與mz原邊重建432個
   proper六點列及唯一r lift，核完整接回式、240允許列、兩組各96禁止列；
   另窮盡117個cycle-partition cubes與所有子集交換。對前三張J控制的
   完整染色重新分類，完整證書為[full-j-certificate.json](full-j-certificate.json)。
2. [check_original_table.py](check_original_table.py)：把上述每列運回同一
   原字面色框，直接查原transfer.json。三個原框的允許數分別為96/144、
   96/144、48/144，全部432列逐份相等；原表與新證書hash記在收據。
3. [check_cover_graph.py](check_cover_graph.py)：從121點711原邊重枚全部
   染色。以不同的單點DSATUR搜尋，2834節點得到36份固定三角染色，
   全域展開恰864份，與二層432態逐份雙射。直接BFS原圖核8160個
   分量／單交換、26112個整體cube，七個pin不同、沒有hidden component。
   [cover-graph-independent.json](cover-graph-independent.json)保留完整36份
   固定三角染色與輸入hash；原圖及舊狀態資料另凍結於root目錄。

root自己的圖驗證不依賴512類探索的搜尋覆蓋率。兩份明列原圖的全部
染色、交換及單值section障礙，與一般cover分類或平面實現分開判定。

## 3. 循環交叉審查

- [匹配組審來源幾何與root橋接](../2026-10-15-three-edge-matchings-6ddea32/CROSS_REVIEW.md)：
  紙面核原C5 sector、短圈保留cap、兩star disk、完成成本及完整hub fibres；
  另以獨立hub-first DFS和每列全部16個hub assignments重建四patch，保留
  所有空fibre，核24份異palette列及117 cubes、12W係數。
- [六接點組審Kempe covers](../2026-10-15-j-source-geometry-6ddea32/CROSS_REVIEW.md)：
  從75點353原邊以另一實作重枚36份固定三角染色，完整展開864份，
  核8160單交換、26112 cubes與無equivariant section的奇偶衝突。
  hidden計數的量詞必以literal-pin-row fibre為準；只有base由該row唯一
  決定或另加hidden-loop投影假設，才可直接界單一state的sheet數。
- [Kempe組審三標記匹配](../2026-10-15-kempe-state-covers-6ddea32/CROSS_REVIEW.md)：
  核普通匹配與殘圖的雙射、缺額二、factor-critical極大障礙、原割預算
  及偶補權重的區分。普通存在性不升格成偶補存在性。

主 agent 亦讀三份紙面證明及原邊checker，採納上述明列範圍。任意大小
來源的Jordan／small-cap推論與Tutte障礙是紙面論證；有限證書校準精確
介面、控制及指定模型，未冒稱對假設最小來源完成枚舉。

## 4. 封存與授權範圍

[check_bundle.py](check_bundle.py)核前十二audit的388份檔案內容及成員
集合、五份權威輸入與凍結副本、HEAD、tracked diff、新增Markdown連結、
Python語法與空白、十六個新舊audit的untracked白名單。它亦把四份正式
重播收據的checker／輸入hash逐份對回最終檔案，排除重播後又改內容。
新四目錄的
內容與成員另由[MANIFEST.json](MANIFEST.json)封存；最終收據
[bundle-check.json](bundle-check.json)。`git diff --check`亦通過。

沒有修改共享文件或舊證書，也沒有宣稱全樹DocGraph、Lean build、
新點數界、全來源排除或一般定理。ω=0、完整319、完整720平面來源
實現與完成後嚴格下降仍OPEN。無commit／push。
