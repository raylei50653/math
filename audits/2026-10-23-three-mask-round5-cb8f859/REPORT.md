# 932／933／941 第五輪：非空single層、新換框圖與共同原面

2026-10-23；Git BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
[START](START.md)從[第四輪](../2026-10-23-three-mask-round4-cb8f859/REPORT.md)的
原Q、六個完整D fibre與原分枝二分接續。[BASE](BASE.json)凍結前四輪563檔
（50,009,990 bytes）及六份routing入口；原有使用者修改保留，未commit／push。

## 結論與邊界

| 原來源分支 | 本輪新增 | 仍未解 |
| --- | --- | --- |
| [932：完整Σ932、h=4、20份collar](932/REPORT.md) | single contacts總數s≥1、深點d≥2；原Q長至少10，真弦端點的原C contacts間距至少3，每弦兩側皆深點 | s≥1的一般零pair來源、h≥5及一般932仍OPEN；Q可有弦，共同k≥23不變 |
| [933：原r6、p/h兩五度星](933/REPORT.md) | 以同一原D兩次共面識別得到合法k−8換框圖H*；其完整支持限271／314／319，迫三個原D完整fibre族正；另得掛橋C的原長02路義務 | H*已在K132，未得較小bad；兩個新16-fibre OR正族尚未排，一般933仍OPEN |
| [941：普通短型I、02型13／36](941/REPORT.md) | 若T的原02分量不在B側，兩條真界面至少兩次橫穿，迫兩份同一原圖的四色原面patch；任兩份合至少六原點 | B側及其餘wrong-side未排，八配對與一般941／W7／J1／J2仍OPEN |

## 932：完整環帶排s=0，保一般s的空band

原C9–Q環帶沿原完整rotation固定，Q不先當induced。任何真Q弦若兩端原C
contacts最小距離≤2，會形成原C3／C4／C5 pocket；原空cap或W5與無三接點
前提矛盾，故距離必≥3。每條Q弦兩側若有無深點polygon，非端點耳點的
完整J-degree便為2，撞原度數。只有一深點時因此Q無弦、J是wheel，會迫s=0。

s=0時，固定Q的820個原C9 row，完整環帶有672,400份Q×C fibres，其中
661,743空、10,657非空，合10,798份完整18點lifts。每Q row的**全部**C輸出
必落同一原H的必要支持，不能只挑good lift。拉回20份合同後，Q支持只餘
6／13／18列；完整whole-Kempe必要條件各一批刪空，故s=0全排。於是

`s≥1，d≥2，|Q|=9+s≥10，k=18+s+d≥20+s`。

這不提高共同k≥23。任意s的完整環帶公式仍保留原Q全字面色與所有空fibres；
single多時可能整份band無C lift，此類Q row須真空地保留於必要拉回。
例如s_0=1、其餘s_i=0的交替二色Q10得到空band。另有23點真局部disk，s=3、d=2而Q
有三條弦，核全部小cap與度數後仍成立，反駁「Q必induced」的過強推論；
該圖沒有完整原B／Σ932／最小性，來源控制為`not triggered`。

## 933：新合法換框圖迫原帽看不見的正fibre

同一原D有序框仍為`(a,n,R,L,q,c,s,v,w,t)`，全部原附件與full lifts保留。
原來源幾何給ac、aR、Rc非邊。先在D真外面識別a=c=A，使
`(A,n,R,L,q)`成新空五面、`(A,s,v,w,t)`為新指定外框；再於該空面識別A=R。
保原指定外框副本、僅簡化重複邊。新圖H*完成內點數為k−8；新外框與原B
不同，這是對一張具名合法競爭圖的完整關係，未宣稱保存原B十列。

H*的完整染色恰對應原D的a=R=c子關係。全部原帽回填與原E零fibre給
`Σ(H*)⊆319`；原全域最小性與K132完整目錄遂限為271、314或319。
三者都包含01021、01201、01231，故同一原D的三個相應完整fibre族都必正。
前兩族對**所有**n,L,q及全部(r,x,y)都沒有原帽lift；這不表示D fibre空，
而是H*迫出兩個原E看不見的正D族。第三輪兩新填片的六fibre零值義務未解。

對前兩族各18個原D words只作具名36-target停止測試：三種split、全部
NC10選項及完整子集交換，僅用原552個D零字。各排2個，故餘兩個16-fibre
OR族必正；未排不算可行，不展開全D多輪閉包或LP。原b,p,h完整回填則
精確為n=q iff可回填，此時唯一p=L、b=h為第四色。

第四輪單側漏色的非crossed掛橋C支另迫同一完整E著色的原02 r→a或r→c路，
不預設其bph可接回原G。
原r與x/y完整rotation排其三邊路；最短路至少五邊，D段至少三個strict
private點。五邊時接原a–y–r或c–x–r得到原induced C7，否則至少七邊。
V的唯一crossed掛法仍保留，不能套這個a/c長路引理；C7本身亦未排。

## 941：兩份四色patch必須共同存在

固定同一完整K交換後，原K–B零界面α的兩端在UV／UY，後繼C–Q零界面β
的兩端在原K側外。wrong-side給K內原C–Q邊，故β必進出α圍住的U側。
逐原三角面區分真橫穿與相切，至少兩個不同原中心邊是真橫穿；每次同時給

`k0∈K∩C，k2∈K∩Q，b3∈B∩Q，b1∈B∩C`，

原4圈`k0–k2–b3–b1–k0`及一條中心對角，兩側皆同一原圖的實際三角面。
這把兩palette限制落在同一原面，不能用獨立可行witness替代。原C3空排K4，
原C4空與兩對角原非邊排掉兩patch合在至多五原點的可能，故任兩不同中心
patch合至少六個原點。只有各k2必私有；U、V/Y、q框身分例外仍保留。

有限核對是8種局部四臂turns（4橫穿、4相切）及20個同色小合併schema
（6同中心、10 K4、4無對角C4）。任意大小界面進出由紙證承擔。
R與r不預先識別、可同可異尚未知；K0不全在C、M不自動認L。兩份patch
可如何共點、與原P／B13路接合，仍是下一窄義務。

## 驗證與交接

獨立核對、循環審查及routing傳播見[REVIEW](review/REVIEW.md)，最終命令與
範圍見[整合回執](verification.json)。唯讀入口：

```sh
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/check.py
```

三線正常／seed17及13／16／16項語義反控制通過，941另有兩項外部破壞／
缺欄反控制。root整合重播成功；前四輪563檔及六份routing快照零漂移，
live routing四檔變更獨立報告。原HANDOFF與共通語言本輪入場bytes不變。
獨立完整環帶、H*十列矩陣／目錄與界面小schema核對皆通過。

正式docs檢查通過：711份Markdown／9409個本地連結；正式DocGraph為97
文件／383關係、零錯誤。全樹DocGraph仍另報72項封存duplicate-ID錯誤，
未計為通過。現有索引artifact policy與whitespace通過；前者是8815 indexed
files、113 documented large exceptions、166 registered outputs，不是全部
未提交新檔的發布審核。

一般三支、實際較小bad、K∞、新Lean及matching未升級。
當前接續入口由[Kempe導覽](../../docs/c5_kempe_guide.md)維護；前四輪封存內容
保留歷史語境。本輪未commit／push。
