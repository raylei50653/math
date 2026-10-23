# 短路型 I：同一 F 的 03 二選一與 02 四型

2026-10-21；exclusive BASE `2c38d1dcb4490017312467deb19d9da02b7bb2a6`。

**尚未證明共同來源相容，也沒有排除任何一組初始配對。**
本輪把兩個 target 各自的八組候選收窄為明確的長路與交會義務：全部替代路
至少四邊；四組混合選擇必有原 F 私有的色 2 或色 3 交錯點。完整的
03→02 與 02→03 二步必要審核仍各保留全部 2／4 個初始型，不能用這個
覆蓋結果替代同源的分量更新。

## 固定來源與適用範圍

[BASE.json](BASE.json)凍結十份 authority 的原 bytes／SHA；本輪只研究
profile0、K=1、Y 位於 H_L、三邊路的普通六度型 I，且 **U、V 均為原 E 私有點**。
完整承接原941、Q1接受零、J1 type III、strict only-R/W7
[來源契約](frozen/audits/2026-10-20-r6-941-j1-five-edge-417732f/SOURCE_CONTRACT.md)
及[上輪六度完整報告](frozen/audits/2026-10-21-w7-L-path-30dde27/six_degree/REPORT.md)。
原有序 C5 框、rotation、所有原 stars／附件／非邊／私有點、空 fibres 與全部
full lifts 均保留；不用四色定理或 matching。

固定同一份實際完整著色，令

```text
P=(n,u4,u3,u2,u1,L)，色121212；F=D−(P,z5)。
∂F=(a,z1,z2,z3,z4,V,U,Y,q,c,s,v,w,t)，
φ =(0, 3, 0, 3, 0,1,0,1,3,1,2,e0,e1,2)。
target A44459：(e0,e1)=(0,1)；B44466：(e0,e1)=(1,0)。
N_G(z5)=(L,u1,z4,V,U,Y)，d_G(z5)=6。
```

`Y` 的程式名是 `HL_0`。`03` 等指完整雙色分量；「boundary singleton」只指
碰框接點唯一，仍容許任意原私有點。以下型號是凍結六度證書中
`complete_specific_F_types` 的 **0-based index**，不是原 E 的 column id。

## 八組配對的精確必要條件

03 的兩型為：

| 型號 | 同一 F 的完整分量義務 |
| --- | --- |
| 4 | U 的03塊接整條 a–z1–z2–z3–z4 弧；V 的12塊只有 V 這個 boundary contact。 |
| 9 | U 的03塊只有 U 這個 boundary contact；V 的12塊接 Y、t，A另含 w。 |

02 四型分成兩個原 E 型，各再分成兩種：12／35 的 U02 塊接 z4、V13 塊
為 boundary singleton；13／36 的 U02 塊為 boundary singleton、V13 塊接 Y。
完整 blocks 逐份保存在[根證書](certificate-v2.json)，不以表中的端點摘要代替。

兩 target 各自都必滿足下表中的一格；目前沒有一格被整組排除：

| 03型 ＼ 02型 | 12 | 13 | 35 | 36 |
| --- | --- | --- | --- | --- |
| 4：U03接 a 弧 | U→z4 的03與02兩路 | 私有色3交錯點 | U→z4 的03與02兩路 | 私有色3交錯點 |
| 9：V12接 Y | 私有色2交錯點 | V→Y 的12與13兩路 | 私有色2交錯點 | V→Y 的12與13兩路 |

**每格中的兩條替代路都至少四邊，且長度為偶數。** 這不是任意附加的
搜尋下界：[原圖紙證](geometry/PROOF.md)證明

```text
N_F(U)∩N_F(z4)={V}，N_F(V)∩N_F(Y)={U}。
```

例如若另有 X≠V 在 F 同鄰 U、z4，原四圈 U–V–z4–X 不包已位於 E 邊界的 z5。
原 C4 空內部與 U–z4 非邊迫 V–X；原 C3 面性再與已有的 z5UV、z5Vz4
兩面封滿 V 的四度星，違反原內點最低五度。另一式交換兩端同理。
已知的共鄰 V 色1、U色0皆不在對應替代路的 palette，故不能作兩邊短接；
這些接合也不能靠新增另一個共鄰點完成。

混合選擇的兩條路端點在 ∂F 上按 `z4,V,U,Y` 交替，且兩個完整 blocks 的
boundary contacts 互不相交，所以必在 F 私有點相交。03／13 的交會只能色3，
12／02 的交會只能色2。可選一處四條支邊在原 rotation 中交錯，其對端色
為0、1、0、1。若該點原度恰五，第五原鄰點分別必色2／3；若沒有該剩餘色
鄰點，完整 link 只能二染，故原度須為偶數且至少六。這些都是同一原圖的
必要結構，尚未產生矛盾。

## 完整二步作用仍未排除初始型

[二步審核](transport/REPORT.md)對原03兩型的每個完整分量作用像，覆蓋該
字面像的全部02必要NC型；反向對原02四型的每個像覆蓋全部03型。每個
第二型再作用全部碰框的完整實際分量，固定同一 F 像，枚舉七個原點的
**全部共同延拓**，再接原 G／Q1／J1 的完整 cap assignments。

兩 target 的結果相同：03→02 保留 2／2 個初始03型；02→03 保留 4／4 個
初始02型。精確證書保存214份歸一後的中間字面／split家族、99,009個作用
字面像、23,152份七點完整kernel（含1,186空 fibre）及28,987份原cap states。
每個歸一參照使用同一個全域逆色置換還原 boundary、七點及cap，不逐片換框。

另有一項較強的**同源後繼強迫**：初始02型13／36（第2／4型）若只翻
完整 U02 分量，boundary 恰 U 由0變2，其餘原點連同全分量私有點按實際
動作處理。此像的03必要型唯一：

```text
A：{a,z1,z2,z3,z4} | {V,U,Y,w,t} | {q,v} | {c,s}
B：{a,z1,z2,z3,z4} | {V,U,Y,t}   | {q,w} | {c,s,v}。
```

這是對真實交換結果的必要限制；目前仍未與初始03二型導出矛盾。

此結果只表示這項二步必要測試沒有矛盾。它**沒有檢查八組初始配對的完整
共同實現**：初始兩個 partition 並未記錄完整分量在私有點的相交情形；第一次
交換後，另一 split 的真實分量如何重接仍取決於那些原邊。每個像各有某個
必要型可選，不表示這些選擇能來自同一原圖，亦不能每步補滿初始 fibre。

## 同圖正控制與來源反控制

[固定盤圖控制](controls/REPORT.md)給出同一份著色中同時符合兩個 split 的
小型 triangulated disk：A的03型9配02型12或35，各可用一個色2私有點。
這說明兩份完整 boundary partitions 的條件本身並不互相矛盾。

這兩張圖都沒有通過原01 gate；將原 z5 與 strip 加回後，U、V又各成原四度點，
違反最低五度，且該色2點正是上述禁止的共鄰。它們是**同圖02／03條件的
正控制，完整來源契約的反控制**；沒有提供941來源、較小bad或某格的來源實現。
0／1私有點的完整有限控制也不限制一般來源的私有點數。

## 驗證、證據層與停止點

根[check.py](check.py)直接重建兩 target 全16格的完整 blocks、二選一、偶路
及混合分支的端序／palette／boundary分離；幾何推論由紙證負責。二步及固定盤圖
各有自己的 checker、完整證書、normal／seed17與負控制；逐份驗證與SHA見
[verification.json](verification.json)。原六度 checker 本輪亦已只讀重播通過。

根首版[certificate.json](certificate.json)保留為拒絕控制：初稿把「沒有額外共同
鄰點」誤記成「沒有共同鄰點」，漏了原 V／U 例外；獨立審查後改建
`certificate-v2.json`，未覆寫首證。替代路的至少四邊下界不受影響，因兩個
已知共鄰均不在指定 palette。現行 checker 必須拒絕首版。

文件檢查通過；正式 `docs/**/*.md` DocGraph 為97份文件、383關係、零錯誤。
全工作樹 DocGraph 另報72項歷史／凍結副本的重複ID，原診斷保存於
[docgraph-whole.stderr](runs/docgraph-whole.stderr)，沒有以正式範圍通過替代全樹通過。

```sh
python3 -B audits/2026-10-21-w7-I-joint-2c38d1d/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-21-w7-I-joint-2c38d1d/check.py
python3 -B audits/2026-10-21-w7-I-joint-2c38d1d/transport/check.py
python3 -B audits/2026-10-21-w7-I-joint-2c38d1d/controls/check.py
```

紙面層新增無額外共同鄰點、替代路至少四邊及混合分支的原私有交錯點；Python
只核對具名有限必要家族與控制，沒有形式化紙證。共同來源實現與逐格排除均
**OPEN**。精確缺口是上述長路及私有交錯點在原附件與原01四型之下如何共同
存在，尤其五度交錯點的剩餘色鄰點與偶數高度數分支。

V=原w的pinched-F、型II、原L其餘型、長01路、profile1與K≥2均未由本輪
涵蓋；原40 profiles仍排38型，一般W7、完整必要計數錐、J1／J2與較小bad仍
OPEN。沒有新LP、Lean或matching結論；未commit／push。目前接續由
[Kempe導覽](../../docs/c5_kempe_guide.md)維護。
