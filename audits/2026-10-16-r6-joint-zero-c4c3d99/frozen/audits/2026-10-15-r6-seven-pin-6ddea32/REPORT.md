# r6／319：貼 z 三角面的 partition 限制與弱命題反例

2026-10-15。凍結 BASE `6ddea32a81349821ad3724ae1652bddb9c6a7b04`。
本輪在獨占目錄研究完整七接點 `(z,s,v,w,t,p,q)`；未擴大 plantri 枚舉，
未改共享文件、歷史證書或 Git 提交。直接權威輸入見 [INPUTS](INPUTS.json)。

**得到一項精確方法界線及一個較弱命題的真圖反例；沒有新增來源排除。**

1. 把外 C5 與內三角面 zpq 的共點 z 正確切開，保留原 wedge rotation，
   再對八個邊界位置作 noncrossing partition 控制，投回原七接點後，與
   既有模型完全相同：60 種 proper 色軌道、180 個 row/pairing cases、
   1,080 份 partition options 都沒有額外刪除。來源 all-r 上界的26列
   仍留22列。這只限制本報告定義的 partition relaxation，不否定所有
   使用內面拓撲的證明方法。
2. 既有8點319小代表本身是 induced C5 三角化 disk，有貼 z 的內三角面，
   而且全部三角形皆為面。因此「319 + 這個內面 ⇒ 非面三角形」過強。
   已保存原邊、rotation、面、精確平面座標、全部216份具名完整染色、
   十列完整外框 fibres 與全部60種七接點 fibres（包含空格）。此控制
   違反來源的度數、pv/pw/qv/qw 非邊及 all-r 條件，不能反駁真正來源命題。

[完整推導](PROOF.md)明列切 z 時 component 可分成兩塊的理由。若強迫
兩份 z 保持連通，會錯誤排掉本來合法的 partition，製造假的來源矛盾。
新 checker 以兩種獨立 partition 建構比對完整集合；真圖染色另與4^8
直接枚舉逐字核對，沒有以 marginals 代替共同 lifts。

正常／`PYTHONHASHSEED=17` 重播及 corrupted-certificate 負控制見
[VERIFICATION](VERIFICATION.md)。[certificate](certificate.json)專屬生成，
同一 checker 重播時只讀；凍結輸入與原路徑 drift 均為零。

| 證據／命題 | 狀態 |
| --- | --- |
| 指定切 z partition 模型相對舊模型無新增限制 | finite identity，已完整驗證 |
| 319 + 貼 z 內三角面足以迫非面三角 | counterexample，8點真圖 |
| 完整原最小來源下，319必有禁止 pq palette | OPEN；本輪 genuine source 0，not triggered |
| 原 r6 的 k≥25、一般 K≤22、無界 K∞ | 原界線不變 |
| Lean、外部大枚舉、commit／push | 本輪未進行 |

下一步若沿此線，須加入本模型未保存的原度數／collar 接線，或不同色對
與 successive switches 的同圖 component 相容性。不能把本輪有限
partition identity 或小反例提升為一般來源排除。
