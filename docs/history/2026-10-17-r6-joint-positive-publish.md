# 聯合偶補續進：整理、封存與發布

2026-10-17；研究與提交父 BASE `113e41f7023aa00c8257b815ce8727035b648f26`。
使用者授權「整理目前進展 commit + push」。本次提交一份完整研究 audit、
三份直接導覽／索引更新、必要封存與本發布紀錄。原 audit 的「沒有 commit
或 push」保留研究交付當時語境；提交及遠端狀態以 Git 為準。

## 採納結果與精確停止點

契約固定原 no4ct 全域最小、次級最大邊數的 C5 來源 G，原 x,y,b 四度、
r 六度、同一 U319、合法 J、實際對偶 D、具名 e,f,g、原有序附件與全部
完整 fibres，包括空格及每個合法 r lift。原支持932／933／941逐圖固定。
權威入口為[本輪整合報告](../../audits/2026-10-17-r6-joint-positive-113e41f/REPORT.md)。

| 本輪來源 | 採納結果 | 保留界線 |
| --- | --- | --- |
| [完整分量阻斷](../../audits/2026-10-17-r6-joint-positive-113e41f/C/PROOF.md) | E/F完整染色迫相反AD(z,v)、BC(s,t)連通；實際CD分量的原D點命中全部舊AD路與新BC路。每份F另有到指定111子fibre的完整雙射及必要重連 | 尚未迫CD分離或避路存在；不能把必要阻斷當成違規出口 |
| [七長缺陷](../../audits/2026-10-17-r6-joint-positive-113e41f/A/PROOF.md) | 非面七長奇補圈恰為相鄰四／五面聯合邊界；五根M spokes給跨原扇區induced C5 | 保留面七圈、遠處奇圈及九長以上；省略mark不一定在奇圈上 |
| [原v5六圈修正版](../../audits/2026-10-17-r6-joint-positive-113e41f/B/PROOF.md) | 含e,f六圈只餘mq跨扇區型，迫原c4、a≥7；因此v5且c≥5時排除此類六圈及cyclic六割 | 初稿全排宣稱已拒絕；933反射成940，不能偷用未採納的反射來源 |
| [全九框共同計數](../../audits/2026-10-17-r6-joint-positive-113e41f/integration/COUNT_PROOF.md) | 保留a≠c、原五點全lift及共同palette計數後，三支仍有精確有理解，且58列H全正；932支另獨立展開8688字面列核對 | 放寬域可行不是來源實現，亦非排除來源或迫列消失 |

**`W110+W101>0`、`omega_e=0` 與完整319排除仍 OPEN。** 只要求聯合正值，
不要求兩項各自正。普通101已知非空，但沒有證明其補圖全偶，也沒有保壞的
嚴格完成來源下降。原v/w五度排除、一般T/T0及r≥7仍OPEN；一般K≤22、
固定r6的k≥25及接回成本k+5均未提高。無新Lean theorem；來源實例0、not triggered。

接續須使用同一原圖的實際分量相容性排除阻斷，或沿跨扇區五割構造保持聯合
身份的奇數下降；目前入口由[Kempe導覽](../archive/guides/c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 封存與文件傳播

[發布初始盤點](2026-10-17-r6-joint-positive-publication/initial-state.json)記錄原 audit
全部359檔、20,466,470 bytes及mode，包括研究root清單未列出的B及frozen manifests。
本次不改寫任何原證明、seal、失敗紀錄或研究時的routing快照。

依現行大型產物政策，六份≥1MB JSON與四份含歷史whitespace的凍結原文追加至
主ARCHIVE：10個原路徑、10個gzip blobs、154,307 compressed bytes。
原3507個path records與2163個blob records不變。每份gzip均獨立還原核對原bytes、
大小及SHA；本地未壓縮副本保留，Git以索引、gzip及精確ignore規則交付。
詳見[封存核對](2026-10-17-r6-joint-positive-publication/archive-verification.json)。

Updated：Kempe現況卡、里程碑與停止點；STATUS直接索引與本發布紀錄；C4直接父題。
Reviewed-unchanged：README與HANDOFF入口／研究線tag；一般界與父題OPEN語義。
Propagation stop：L2直接父入口，沒有向一般主命題傳播closure。

## 本次驗證與提交後重播

[發布重播](2026-10-17-r6-joint-positive-publication/replays.json)記錄A、修正版B、C與
三份共同計數證書的正常／seed17重播；另保留篡改弦、跨扇區lift、空格及共享
計數四項負控制。各項成功與預期拒絕分開記錄，不把負控的exit1稱為來源排除。
[工程檢查](2026-10-17-r6-joint-positive-publication/engineering/summary.json)中，
`lake build`通過8832 jobs，保留30項既有warnings；Python3.14工具測試94項通過。
既有Lean build不形式化本輪紙面定理。

文件、formal/scoped DocGraph、staged artifact policy及whitespace的實際收據放在
`2026-10-17-r6-joint-positive-publication/submission-checks.json`。
全樹DocGraph仍有70組歷史duplicate IDs，不能稱全樹PASS；本輪研究時的
全樹比較原紀錄保留。未擴大來源枚舉或重建整批generated artifacts。

新checkout先還原封存，再執行紙面校準證書；以下不覆寫原證書：

```sh
python3 tools/audit_archive.py restore --artifacts
python3 -B docs/history/2026-10-17-r6-joint-positive-publication/check_custody.py
sha256sum -c audits/2026-10-17-r6-joint-positive-113e41f/SHA256SUMS
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/A/check.py
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/B/check.py --check audits/2026-10-17-r6-joint-positive-113e41f/B/certificate.json
python3 -B audits/2026-10-17-r6-joint-positive-113e41f/C/check.py
python3 scripts/check_docs.py
python3 tools/docgraph --include 'docs/**/*.md' check
```

發布封存checker亦可直接從gzip核對缺少的原路徑。它接受HEAD為研究BASE的後繼，
對206份數學權威核對原Git物件與凍結bytes，對更新routing保留研究交付快照；
不要求發布後仍HEAD=BASE或工作樹空白。它驗證保存身份，不驗證數學定理。
其餘計數／seed17／負控命令見上方重播收據與原研究VERIFICATION。
