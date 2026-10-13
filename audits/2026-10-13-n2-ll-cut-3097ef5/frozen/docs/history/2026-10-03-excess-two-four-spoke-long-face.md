# 2026-10-03：ε=2 四-spoke 同一長 face 的兩原 unary 次序排除

使用者要求「繼續推進 ε ≥ 3」。接手 HEAD=`0e38127`，
cwd=`/home/ray/developer/ai/math`，沿用既有未提交的短 face 成果，
沒有重開來源圖 catalogue，未 commit／push。記憶中的 mixed 省略
入口已被後續成果處理，本輪以即時 HANDOFF／STATUS／Kempe 導覽
的具名停止點選原01／04。

## 結果與同源身份

[新報告](../c5_excess_two_mixed_core_four_spoke_long_face.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_long_face.py)、
[joint helper](../../scripts/c5_excess_two_four_spoke_long_face_joint_controls.py)、
[artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_long_face/observations.json)
保存以下窄進展。

固定完整Σ=933／941或整圖D₅像、Σ edge-minimal、指定有序
induced-C₅ disk、有效H連通、ε=2；相鄰雙完整degree-5 roots，
其餘有效內點完整degree四。唯一mixed incidence=(1,1)，原C
contacts=(x,y)可共鄰但不複製頂點；各側一原單接點unary與兩spokes。
原C／U／V、所有原邊、actual attachments／supports、ownership、
環序及字面共同色框保持。

選定原a=5,b=6、spokes01／04，source indices98／135、
root交換126／195。Critical unary必離開兩個短incident faces，
同在原長face(a,1,2,3,4,b)。原connected U／V到actual support
的兩條原路徑不能有四個交錯face邊界端點，因此maxS_U≤minS_V，
允許共享端點。三段框弧使支援跨度和≤3，短支援引理與critical
witnesses迫各≥2，矛盾。固定選一份短unary，其contact coloring
逐列可避開root色，只替換這份原witness，其他原頂點逐點保持；
原au或bv省略不改變完整Σ。五角色投影相等，不稱六角色joint相等。
不需Σ(G−C)=Ω，不用逐列q-minimality，也不取C marginals。

| 原候選必要域 | 933 | 941 |
| --- | ---: | ---: |
| 前序unequal-pair框架 | 32 | 50 |
| 同一長face新排 | **10** | **10** |
| 剩餘共用一框點 | 8 | 22 |
| 剩餘不相交 | 14 | 18 |
| 剩餘合計 | **22** | **40** |

新排原indices：933=98,99,126,132,141,146,174,177,188,191；
941=135,136,195,203,216,223,283,287,303,307。
50份共用單點原骨架有4,800 rotation assignments／100 disk
rotations；20所排身份各256 actual support pairs，包括空支援、
單點及共用原端點，共5,120。1,280雙非短pair全部交錯，無相容
者；120明示apex K₃,₃ subdivisions保存全部九條互斥path及原
路徑收縮身份。另有20原root swaps、51,200共同D₅支援對、
2,000同框列與1,200搬運後subdivision path checks。

18張完整degree圖有C共鄰singleton／不同接點edge／triangle、
三種U／V配對及root交換。保存原完整relation與coloring witnesses，
九種原圖變體的1,620 joints／25,920 pinned fibres（含空）、
1,260原邊接回／810 swaps與獨立整圖回溯相同。U／V的66／90份
多contact色列核對五角色投影，保存680／1,012替換witnesses，
逐完整原邊及unary外逐點驗證；72／52 singleton投影失敗列、
C marginal假允許、au接回阻塞與18份原交錯path負控制保持。
這些完整degree圖不宣稱disk、候選Σ、criticality；固定拓撲
skeletons不補滿來源degree。任意大小來源排除由紙面證明承擔。

## 實際驗證與产物

新checker預設hashseed及17兩次逐byte replay通過；直接依賴
的短face與短支援hashseed17 replay通過。短支援local／three-hub
數學payload唯讀重算相同。外部degree-list講義重新取得，核對
Lemma7 connected degree assignment的slack／tightness及
Theorem10 Gallai tree／blockwise uniform前提。獨立紙面及程式
審查未發現實質問題。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_short_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

lake build通過8,831 jobs，只有既有AttachmentOrder／SymRelabel
linter warnings，没有新Lean theorem。新observations為
**19,091,926 bytes**，SHA256
`26a705db3b4ce938acb0a8ac996b4994f207659214c9fd14d20a0a8797232cec`，
本地保留，MANIFEST／.gitignore登錄producer、依賴及fingerprints；
前序artifacts原樣保留。README／STATUS／Kempe導覽／整合頁及
原短face後續說明同步；HANDOFF研究線及tags未變，維持薄索引。
文件檢查通過504份Markdown／5,170個本地連結，anchors、index、
handoff均通過。DocGraph通過62 documents／213 relations／5 families，
零errors／notes；artifact status為ok=134，無missing／changed／stale。
git diff --check通過。獨立審查另修正V替換必從G−bv開始的表述，
以及120份subdivisions與其每份九條paths的計數名稱；數學結論不變。

未重跑degree-6全分拆、舊單spoke byte-check、singles漂移audit、
R系列、weak-deletion／Kempe closure、全倉來源catalogue或Lean
axiom audit；不宣稱歷史研究全部重新驗證。lake build不形式化
本輪crosscut或短支援任意大小合成。

## 停止點與貼用摘要

**共同下界仍ε≥2；ε≥3未證。** 完成原01／04及同機制(1,3,1)
框架窄排除；整個(2,2)、mixed(1,1)+各側一unary剩22／40份。
下一941原入口01／03、indices134／174；933原01／13、
indices100／156同arc type，需整圖一次共同D₅搬運。保留完整
C／U／V、同一六角色joint與actual supports，分析原unary
crosscut封住C的位置與可保degree的少數hub化約。其他incidence、
較少spokes、單省略、(5,5)q-core、多mixed／no-mixed／非相鄰
及unary側例外均保留；來源實現、一般出口、新Lean theorem及
K∞=K≤5未證，最新停止點见[Kempe導覽](../c5_kempe_guide.md)。

```text
cwd=/home/ray/developer/ai/math；先讀HANDOFF/STATUS/Kempe導覽及即時Git。
HEAD=0e38127，沿用未提交short-face bundle；本輪未commit/push。
固定完整Σ=933/941、edge-minimal induced-C5 disk；共同ε≥2不變。
四spoke(2,2)、mixed(1,1)+各側一unary：原01/04與交換98/126、135/195全排。
兩原unary若critical必同在原三段長face；actual support次序迫跨度和≤3，短支援迫≥4。
固定原U或V可逐列避root色；整份C及另一unary witness保持，五角色投影相等。
各排10；unequal從32/50到22/40，共一點8/22、不相交14/18。
checker：python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check。
5120 actual support pairs、120 explicit apex K3,3、18degree圖1620joints/25920fibres。
新checker兩hashseed、直接short-face/short-support依賴與lake build通過。
下一94101/03 indices134/174；93301/13 indices100/156，保留literal joint/原crosscut/hubs。
其他incidence/較少spokes/單省略/(5,5)/多mixed/no-mixed/非相鄰仍保留。
紙面+固定Python；ε≥3、來源實現、一般出口及K∞=K≤5未證；沒有新Lean theorem。
```
