# 第四輪獨立核對與交叉審查

2026-10-23。原來源、紙證、固定有限證書與來源控制分開。
本輪root的獨立腳本不import本輪producer；三線循環審查及最後routing核對
均完成，未見阻塞。來源控制未觸發不計為來源存在或排除。

## root獨立核對

- **932群平均**：[932-independent.py](932-independent.py)只讀第三輪兩張
  凍結控制的有向面，直接枚舉每份whole vertex-colour tuple。不同／相同
  anchors的原完整矩陣皆非rank-one；column S2／S3群和皆rank-one。
  共四組控制的全部fibres與full lifts見[回執](932-independent.json)。
  這些控制不觸發原完整932來源。
- **932原row先行**：[932-row-first.py](932-row-first.py)從820份原C9 row
  的共同S4像重建folded座標，不引用本輪grid／刪除transcript。不同anchors
  的10×31格恰覆610原rows，相同anchors的4×10格覆210原rows；每一格是
  完整OR，不是選定其中一row。引用原已凍結全部Kempe options作必要條件，
  180份查詢／pair位置全刪空。[獨立回執](932-row-first.json)與本輪證書
  [對照](932-transcript-comparison.json)的920批、64,800次刪除完全一致。
  同一證明涵蓋一／二中心；不宣稱零pair或一般932已排。
- **933全部帽回填**：[933-independent.py](933-independent.py)獨立量化
  每份相關原D tuple的全部64個(r,x,y)候選。U、V各14個raw lifts，共24
  份相關D tuple；其中18份可回填原E零字01023012／01023021，必使整份
  原D fibre空。餘六份及共同兩份逐點xy-swap、其餘四份r=2均重現，見
  [回執](933-independent.json)。此有限檢查不承擔原D幾何及全域分量證明。
- **933從D端完整重建**：932 agent另寫
  [933-kernel-independent.py](933-kernel-independent.py)，從2461個canonical D
  的157,504份(r,x,y)候選開始，將完整13點tuple共同S4搬到canonical E。
  全部70,144份原tail fibres及274×2461 kernel逐份相等；2549個非零entries，
  總2672份literal lifts，含E二色stabilizer給出的兩份額外像。normal／seed17
  JSON一致，未import933程式，見[回執](933-kernel-independent.json)。
- **941完整link與錯誤補連通**：[941-independent.py](941-independent.py)
  從完整cyclic word核五度T、Z的各十份有向鄰色word及至少六度分支。
  另從第二輪既有rootless控制的全部原面與邊重建完整K交換，確認K的原0點
  不必全在同一後繼C12(U)。[回執](941-independent.json)保留這個
  `counterexample`，控制完整來源為`not triggered`。

root曾提出「最後K0出口的下一色1點必在C」作探索建議；941 agent指出
只能在該K0點自己的後繼12分量，root撤回額外的C-membership。
無條件最後出口屬原B13仍可保留；本輪不得把全部K0當成C，也不得把不同
原02分量或不同路上的標點識別。這項未採推論沒有進入已採來源結論。

## 循環交叉審查

- **933→932：PASS。** 審群和係數、stabilizer、OR正格的量詞、每份實際
  whole orbit的crossgrid必要性、每批同一before支持及全部options。fresh
  `check.py --negative`通過，15反控制拒絕、18immutable drift0。原Q簡單但
  可有弦、耳點矛盾成立，沒有抬高共同23或宣稱零pair已排。
- **941→933：PASS。** 審原nonedges／完整h、r stars排十點alias的來源鏈、
  真C10、全帽回填排整fibre、13三橋及兩組完整雙射，V交叉掛法保留。
  以首點block及間隔遞迴另生16,796份NC10，不用933的Bell過濾／checker；
  完整六份options及survivor集合一致，survivors為3、3、5、5、6、6。
  fresh negative通過、15反控制拒絕、13immutable drift0，無可行性升級。
- **932→941：PASS。** 審J−K全碰框分量的B側、同一尾路返K0不返C、
  同一K路最後C出口指定Z、完整link兩側／高階、03型4三私有非邊及03型9
  域。fresh normal／negative通過、16反控制拒絕、23immutable drift0。
  已將新路標點改名u⁻／u⁺，避免與原框literal v混淆；證書不變。

root對三份最終紙證逐段核對，並核933真D的alias authority及941新標點的
顏色／分量：R與u⁻、u⁺顏色不同，與s的C-membership不同；R=r尚未知。
完整來源控制均未觸發，一般三支、較小bad及Lean未升級。

## Routing與L2傳播

Closure scope是932原h=4、20個原collar的全部距四接點分支，canonical
source為本輪932紙證與180份固定證書；零pair父題仍OPEN。

Updated：Kempe導覽頁首、對應現況及精確停止點、STATUS對應直接索引；
932直接consumer `docs/c5_c8_peeling.md` §5及
`docs/tasks/c5_no4ct_handoff.md`狀態／窄任務，均由19模板改零pair原Q。
933、941只有具名原關係與分枝必要限制，未正式關閉一般父題。

Reviewed-unchanged：原HANDOFF研究線及活躍tag未變；共通語言接口無新語義，
兩檔均與本輪entry bytes相同。共同k≥23、h≥5、一般三支及原W7/J1/J2
仍OPEN，無上層結論改動，因此停在L2，不展開README或跨線synthesis。
前三輪390檔完整檔案域及bytes／SHA零漂移；舊報告保存歷史語境。

正式docs、正式DocGraph、現有索引artifact policy及whitespace均通過；全樹
DocGraph另列72項封存duplicate-ID錯誤，沒有計為通過。具體命令與scope
見本輪[整合回執](../verification.json)。
