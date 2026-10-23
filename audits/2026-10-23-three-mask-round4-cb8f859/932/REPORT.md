# 932 round4：原C9全部距四接點排除，轉入原Q下一層

**新定理：同一全域最小no4ct、完整932、h=4的全部二十份原C9合同中，
嚴格內點不存在距四雙接點。每個雙接點恰為原邊面第三點t_i，第三輪19份
必要模板只餘零pair。** 零pair及一般932仍OPEN，共同k≥23不變。

[原來源合同](SOURCE_CONTRACT.md)、[任意大小接合與刪除soundness紙證](paper/PROOF.md)、
[完整證書](certificate.json.gz)、[獨立唯讀checker](check.py)。
BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

新輸入是同一原C6／C7 cells的**群平均OR接合**：保留原中心色乘積和，raw
counts仍只rank≤2／3；固定anchors後對unused-color群求和，才得到folded
rank-one矩陣。不同／相同anchors分別是10×31／4×10格，覆原610／210 rows。
每格只要求其中至少一列正，沒有誤套raw rectangle或把支持上界當實際支持。
只有一份必須全正的完整whole-Kempe orbit迫出的某整格，在當時必要支持
全空，才拒絕該orbit；某split所有完整options皆拒絕，才刪其原row。

完整證書排全部20×9=180個case/pair假設，同時覆蓋360個單／雙中心分支：
920個同步批次、64800次帶pair假設的row刪除。獨立checker不import producer，
literal-first重建18份folded map、4862份NC partitions、49356份whole options，
並重算164000份原annulus fibres（151605空）與13990份full lifts。原名、
attachments、原面、rotation及full case SHA逐份綁定。

兩張具名原cell控制逐tuple核Cartesian sector union與direct whole lifts，
包含不同／同色anchors全部1220／1260份空／非空fibres。群和係數逐格核為
單中心1／2、雙中心1／4，包含非自由群軌道的multiplicity。raw count minors
仍有行列式±16，raw rank-one誤用明記`counterexample`。完整接合控制為
`triggered and holds`；它們沒有原B、完整932、全域最小性，完整來源仍
`not triggered`，不以控制圖承擔原來源排除。

原rotation另給明確下一層：設s為只接一個C點的原內點總數，全部C內鄰點
依原link接成簡單原圈Q，長9+s；原J=H−C是Q-disk，Q可有弦。九個t_i在J
度≥3，其他Q點度≥4；若Q內無點則多邊形耳點degree2矛盾。因此至少一個
原點完全不接C，局部k≥19+s；這不提高共同23。

18份immutable輸入及六份routing快照見[ledger](INPUTS.json)。normal／seed17
唯讀重播一致，15項語義反控制全部拒絕，immutable drift=0；見
[VERIFICATION.json](VERIFICATION.json)。失敗的前置freeze generation保留，
尚未寫certificate便中止；恢復時只驗既有bytes，最終證書exclusive-create。

```bash
python3 -B audits/2026-10-23-three-mask-round4-cb8f859/932/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round4-cb8f859/932/check.py --check --negative
```

下一窄義務是同一原Q、九t_i、全部single contacts與深點的完整relation或
可回填化約。零pair h=4、一般932、h≥5、smaller bad、K∞及新Lean仍OPEN。
沒有無條件C9 row deletion、新來源圖、廣泛圖枚舉或LP；不改前三輪／共享
文件，不commit／push。
