# 932 round5：排s=0，至少一single、兩深點；Q弦保留

**新定理：同一全域最小no4ct、完整932、h=4的二十份原collar中，s≥1，
原Q內至少兩個深點；每條真Q弦兩端的原C contacts最小距離至少3。**
一般s≥1來源仍OPEN，共同k≥23不變，沒有宣稱Q induced。

[來源合同](SOURCE_CONTRACT.md)、[任意大小紙證與有限排除soundness](paper/PROOF.md)、
[完整證書](certificate.json.gz)、[獨立唯讀checker](check.py)。
BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。

任意s的原Q弦若有兩端contacts距離0／1／2，原C3／C4／C5 pocket由small-cap
前提迫成原Q邊或矛盾；相鄰Q邊例外完整保留。真弦兩側各需深點，否則一側
無內點polygon有非弦端耳點，其完整J-degree2撞原下界。若只有一深點，Q必
induced且J為wheel，所有Q點度3，迫s=0；合下列排除遂得深點至少2。

實質s=0排除來自**同一原C9–Q9完整annulus**。它不要求Q induced，也不限制
未知J大小。全部820個Q rows皆有C lift；完整672400 fibres含661743空格，
10657非零entries、10798份18點full lifts。若某J Qrow正，其**每份**C lift
都成同一H coloring，故全數C輸出必在原必要支持。二十query拉回後初始Q
支持只餘6／13／18列，各用一批完整whole-Kempe刪空，共250次條件Q-row刪除。

獨立checker不import producer，從C-first反向列Q lifts，再對整份18tuple
作共同S4搬運，逐份重建所有空／非空fibres；另重建4862份NC partitions與
49356份whole options。原二十collar的完整SHA、真名、rotation、attachments
及原B–C full fibres全保留。不帶s=0時沒有無條件C9 row deletion。

可變s的完整band另得9個4×4 allowed-color／unequal矩陣的trace公式，逐原
link保留所有single contacts。s=1的proper交替Q10可有空band，是明列護欄：
一般Q row不能只因無C lift便從J刪去。本輪未擴成s>0枚舉或LP。

保留一張23點、s=3、Q長12、兩深點、三條Q弦的有向disk。完整degree/contact、
原links、各邊兩側、Euler及所有small caps都核對；它反駁從本輪局部必要
結構推出Q induced。控制沒有原B、完整932、全域最小性，來源`not triggered`，
不是來源實現。literal空band為`counterexample`，非空trace控制為
`triggered and holds`。

16份immutable輸入與六份routing快照見[ledger](INPUTS.json)。normal／seed17
一致，13項語義反控制拒絕，immutable drift=0；詳見[VERIFICATION](VERIFICATION.json)。

```bash
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/932/check.py --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-round5-cb8f859/932/check.py --negative
```

下一窄義務是同一原Q、可變single contacts與空band狀態的完整J relation，或
contact-distance≥3的原弦cell可回填化約。一般零pair s≥1、932、h≥5、較小bad、
K∞及新Lean仍OPEN；未改前四輪／共享文件，未commit／push。
