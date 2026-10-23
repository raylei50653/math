# 第五輪獨立核對、來源邊界與直接傳播

2026-10-23。所有source結論限定本輪三份原合同，完整來源控制均未觸發。
root獨立程式不import本輪producer；有限PASS不替代任意大小紙證。

## root獨立重建

- **932完整原環帶**：[932-s0-independent.py](932-s0-independent.py)從固定
  Q word的literal lists出發，保每份原C lift。820×820 fibres的10,798個
  full tuples與20份原合同的support pullback／完整whole-orbit刪除一致，
  見[原重建](932-s0-independent.json)及[逐證書對照](932-certificate-comparison.json)。
  原完整Kempe options取凍結authority，932自己的獨立checker另從NC9重建。
  沒有挑一份good C lift，也沒有刪一般s的空band row。
- **933完整H*關係**：[933-hstar-independent.py](933-hstar-independent.py)
  從2461個原D words與完整rxy帽重建552個原D零字，以及H*全部十列投影。
  上界319及K132三選271／314／319完全一致，必正01021／01201／01231；
  前兩族對全rxy都空，bph回填iff n=q且唯一。見[獨立回執](933-hstar-independent.json)
  及[24,610矩陣entries與640指派對照](933-certificate-comparison.json)。
  正D但無E lift不矛盾；實際兩次共面操作及最小性量詞仍由紙證承擔。
- **941真橫穿與五點合併**：[941-interface-independent.py](941-interface-independent.py)
  以兩原三角面的實際座標求兩條零線出口，依中點四臂的圓周順序分橫穿／
  相切，8份配置中各4。另生20種同色身份schema，得到6同中心、10 K4及
  4雙對角缺的C4，見[回執](941-interface-independent.json)。全域α／β進出
  與原C3／C4 cap的有界側由紙證承擔，不把raw 4cycle直接當矛盾。

root逐段核三份最終紙證。932的近owner pocket、非端點耳點與原Q完整degree、
all-lift universal量詞和空band保留sound。933的兩步共面操作確保新空五面與
指定outer；k−8成本、全bph×rxy回填、最小性三支持及OR正族未混拼見證。
其長02路只需同一完整E著色，不預設bph能接回G；原G的uncoloured幾何及
小cap仍適用。941用同一原Y∈B∩C給兩03型皆可用的B13橋，且真橫穿patch
的K／B／C／Q角色來自同一原面，不識別其k2與Z或b1與R/r。

## 循環交叉審查

- **933→932：PASS，無阻塞。** fresh `check.py --negative` exit0，13項語義
  反控制拒絕、16immutable drift0。審all-lift pullback的全稱量詞、每批同步
  before支持及完整whole options、空band的真空保留邊界；Q仍可有弦、單深點
  wheel排除及s≥1／d≥2推論正確，沒有提升共同k≥23或一般來源。
- **941→933：PASS，無阻塞。** fresh `check.py --negative` exit0，16項語義
  反控制拒絕、13immutable drift0。審原非邊、實際新outer／k−8、Cartesian
  回填、E-invisible正D族及16-OR量詞、四個原C5 bounded sectors、至少三個
  strict private D點、induced C7與V crossed例外。另以首block／間隔遞迴
  獨立生成NC10，核36 targets×3 splits的全部options與literal subset輸出；
  僅用原552零字，精確重現四新零461／482、470／491與兩個16-OR族。
- **932→941：PASS，無阻塞。** fresh normal／negative通過，16項語義反控制
  拒絕、28immutable drift0。核α含K側、β兩端外但穿K內、至少兩次真橫穿，
  原面角色與K4／無對角C4的五點排除；至少六是原點，不是六私有點。
  k2可共享，U/VY/q框例外、03型9適用界及高階均保留。

## L2傳播與未改項目

Closure scope：932原h=4二十份collar的s=0，以及941 wrong-side的至多一次
橫穿／至多五原點合併子支。Canonical Source + Evidence為本輪各線紙證及
固定證書。s≥1父題、一般wrong-side及原B側均OPEN；933只完成新圖合法性、
支持分類與具名正義務，沒有一般來源closure。

Updated：Kempe導覽頁首及相關現況／停止點、STATUS對應直接索引；932的
直接consumer `docs/c5_c8_peeling.md` §5及
`docs/tasks/c5_no4ct_handoff.md`狀態／窄入口，更新s≥1、d≥2、真弦與空band
界線。933／941詳細新正族與原面接合由所屬導覽及本輪來源負責。

Reviewed-unchanged：原HANDOFF研究線／活躍tag未變；共通語言接口無新語義，
兩檔均與本輪entry bytes相同。no4ct交接的R6一般來源、嚴格下降仍須目錄外
壞性的界線仍正確，H*在K132不改其父義務。共同k≥23、W7 38／40與J1/J2
未升級，停在L2；不展開README或跨線synthesis。前四輪563檔完整域／bytes
不變，歷史報告保留當輪語境。

正式docs、正式DocGraph、現有索引artifact policy及whitespace通過。
全樹DocGraph另報72個封存duplicate-ID錯誤，未算通過；具體命令與scope
見[整合回執](../verification.json)。未commit／push。
