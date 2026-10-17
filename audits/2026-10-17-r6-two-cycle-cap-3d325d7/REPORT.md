# 七-cap 接觸排除與兩完整補圈分支

2026-10-17；凍結 BASE `3d325d7197aa05815c71bedc52c1b253d736c7bb`。
原本地／tracking／遠端 main 在開始時一致，工作樹乾淨。
權威為 [完整紙證](PROOF.md) 與三路獨立審核；身份見 [INPUTS](INPUTS.json)。

保留同一原全域最少、次級最多邊的 no4ct C5 來源，原 x,y,b 四度、r 六度、
支持 932/933/941、ordered frame、rotation、所有私人接觸與完整 U319 fibres
（包括空 fibres）、全部五點及 r lifts。J,D 與字面 e,f,g 不變；無原 v=5 前提。
任取實際 M101，假設 D−M 有含 f 的非面七圈 C；不要求奇圈數最小。

| 新採納結果 | 精確範圍／證據 |
| --- | --- |
| cap–m 接觸整個子類排除 | `N_J(m)∩V(K)={z}`，不限大小、不需參考或兩圈假設；[A](A/PROOF.md) |
| 完整 m-面距離 | `dist_D(X,V(∂F_m))≥2`；仍不推出 SEP |
| 全部偶補參考的區域奇偶 | 每個完整 L_R 區域含偶數個 F 奇圈；恰兩奇圈必同區，可有額外偶圈；[B](B/PROOF.md) |
| 恰兩個完整補圈 | 每個偶補 R 的 L_R 皆連通；固定 M 的 `|W_g|=|V(D)|`，不能改參考得到 SEP |
| 兩圈的 primal 結構 | M* 恰三分量：中心 K2、含 vw 的樹、含 Q5,mz 的單圈分量；唯一圈為 Q5 |
| SEP 的精確存在性物件 | 同一實際完整全異染色中，S_R 的簡單 z-圈，指定 rays 分居兩側，且全圈同 α；[C](C/PROOF.md) |
| 指定短圈排除 | p 中心的分隔 C4 不能用 zq；c0=5 時長至少六；q 中心、a0=5 反射。一般情況未排 C4 |

這修正的是[前輪發布紀錄](../../docs/history/2026-10-17-r6-active-f-seven-publish.md)
的後續存在性任務。原 R100 **條件下降定理保留正確**；舊封存與發布記錄保留
當輪語境及精確 bytes。兩圈子類尚未排除，不能對其要求固定 M 改參考得到 SEP。
此外，若恰兩奇圈且 g 端點在另一奇圈，即使有偶圈，R100 仍全被阻斷。

優先下一題為**兩個完整補圈的實際匹配修復**：固定
`D−M=C7⊔O_odd`，保留實際五 spokes、三分量及新接觸排除，找彼此頂點
不交的 M-交替圈批次，避 e 並同時翻／不翻 f,g，得 `N∈P101∪P110` 且
全部完整補圈皆偶。其他未被全參考阻斷的 M 才續找指定實際共同色 z-圈。
詳細義務見 [紙證 §5](PROOF.md#5-優先修復義務與停止點)。

證據層：以上是任意大小紙證，經三路獨立推導與交叉審查；不是有限來源排除。
[小型完整證書](certificate.json) 只校準區域奇偶量詞：七稜柱的 28 個偶補參考
全部連通；另一個有兩奇圈加一偶圈的連通 cubic 圖有 5 個偶補參考，其中
1 個交換圖不連通。兩圖的 R=M 反控制顯示不能刪掉偶補參考前提。
這些圖不是具名最小來源；真正來源供應 **not triggered**。
沒有新增外部定理、沒有新增 Lean theorem；`lake build` 只驗既有 Lean 庫。

驗證命令、結果及污染／覆寫拒絕見 [VERIFICATION](VERIFICATION.md)。

```sh
python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-17-r6-two-cycle-cap-3d325d7/check.py
python3 -B scripts/check_docs.py
lake build
```

Closure scope：cap 除 z 外與 m 的所有接觸排除；全參考奇偶、兩圈結構及 SEP
等價判準已證，**未**排除兩圈匹配本身，未構造匹配修復。
Updated：本 audit、Kempe 導覽的現況／停止點／直接父題路由、STATUS 對應索引。
Reviewed-unchanged：README／HANDOFF 研究線及 tag、前輪全部 77 檔封存與發布紀錄、
原條件下降定理、一般界與 k+5 接回成本。
Remaining OPEN：兩圈匹配修復、剩餘 active-f 七圈、其他奇補圈、H 相連殘案、
`W110+W101>0`、`omega_e=0`、完整319、一般 T/T0 及主命題。
Propagation stop：父題仍 PARTIAL／OPEN，停在直接導覽；不提高跨線 closure。
本次未 commit、未 push；目前接續入口見 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。
