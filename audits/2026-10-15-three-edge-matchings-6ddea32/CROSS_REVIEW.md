# 第四輪交叉審查：J來源幾何與完整all-r橋接

審查 `../2026-10-15-j-source-geometry-6ddea32/` 的 PROOF、REPORT、
兩個checker及完整證書，並審 `route-round4/FULL_J_BRIDGE.md`。
對方目錄完全唯讀。本次審查結論：**明列範圍內通過，無阻斷問題**。

## 紙面幾何與來源接合

- 原C5 sector證明成立。新三角形的跨邊AB確實給五個互異原內點的
  `(r,s,A,B,t)`。原x,y在外框而不在環上，故不能進有界側；原rotation
  迫所有未落在環上的v,w在另一側。兩個在內違小C5，一個在內迫
  完整W5中心，並產生sw或vt禁邊。只留vw原面，不使用可染性。
- 短圈anchor推論成立。避m,z的圈逐點還原為原內點圈；r,s,t原度≥6，
  不可能成為被刪掉的五度中心，其餘被刪／拆點來自原外框。故空C4
  或空／W5的C5 cap完整保留。induced C4/C5排掉空cap的方法及對偶
  cyclic 4-cut定位正確，未把經m/z的圈納入小cap結論。
- 雙star介面保留原身份。J四連通使m,z的共同鄰點恰α,β、且αβ無邊；
  兩條link路徑除端點外不交。兩個closed stars的聯集為disk，外框長
  `M+Z−4=dG(s)+dG(t)+h−6`，刪m,z後的W保留其餘全部原邊。
  α=p或β=q的實際identification沒有被當作另增端點。
- 完成成本核對：W有k−3點，加m,z兩點、拆m一點、再由U恢復原G五點，
  回到k+5。薄cap只供應某份W染色，不能保證hub fibre非空或違規；
  文件沒有偷渡成較小bad source。

上述C5結論也支援本目錄的5割障礙接合：factor-critical component
的5-cut是bond，對應simple原C5；若避m,z，原兩星因與X相交而在
component外。空pentagon的三面對偶是樹，不能factor-critical，故
僅原W5的dual C5可留。這裡使用的是幾何證明§4第一段的非induced
cap敘述，沒有假定所有cut-cycles先驗induced，也沒有把7-cut當成C7。

## 全部lifts與完整來源謂詞

對同一份完整W染色，所有hub pairs必且只需缺色且m≠z，故
`K(χ)=A_m×A_z`去掉對角是精確完整fibre。空集合也必保留。
α,β異色時兩個缺色集合都含於同一補色對，任何合法hub pair便具有
唯一差值；這個量詞只針對非空fibre，紙面區分清楚。

新two-palette排除亦成立：兩條路徑各用兩色且其缺色二集合不等時，
共同端點必同色；兩集合交一色，三個合法hub pairs的差值遍歷三種
非零值。此時e≠f，恰一個pair使g=e，違反完整all-r。沒有為不同
hub pair另換W染色，也沒有由24個控制row推稱真正來源具備它們。
兩path長度皆偶及M,Z皆偶的必要條件正確；不是整個度數分支排除。

FULL_J_BRIDGE精確補上第二個bad event：唯一r lift下，z=r時pq須恰
為vw；z∈vw時pq須含另一色。逐情形得到 `(e=f) iff (e=g)`，兩個
bad patterns110、101互斥。固定state／色差pair的117個cycle cubes
已完整核對；一個switch suffices僅是該固定cube的量詞。

計數係數12也核同：固定共同Tait色的每M fibre有2^c個全染色，三種
共同色與四種原根色各作完整雙射。自身三標記證書另外直接將所有
Tait tuples積分成rooted J tuples，再與獨立全四色DFS逐tuple核同。
得W=(2,6)、(8,6)、(0,2)，相應bad counts=(24,72)、(96,72)、(0,24)。
普通PM counts沒有被當作權重或正值。

## 可重播交叉證據

[review_geometry.py](review_geometry.py)不import對方checker：

- 用hub-first、反字面boundary順序DFS重建全部patch染色；
- 對每份proper boundary row逐一試全部16種hub pairs，直接核每條
  原邊，與完整lift lists及空列比對；
- 四patch得到全染色2760、2760、2760、5688，空fibres17040、17040、
  17040、53712；最後恰24份異palette列，各有三個lift及唯一bad lift；
- 另用不同partition生成法核117個cube覆蓋及全部targets，並核432個
  proper六點列中恰240個完整all-r允許；
- `check_original_table.py`將新謂詞逐432列直接對回舊transfer.json，通過。

正式兩checker正常／seed17通過；漏完整lift及錯hub返回的既有損壞
證書均拒絕。完整指令、退出碼及輸入／輸出hash保存在
[CROSS_VERIFICATION.json](CROSS_VERIFICATION.json)，同輪authority文字
另存凍結副本。任意大小的Jordan與來源small-cap推導由上述紙面審查
負責；patch枚舉只核介面代數，沒有被用來認證假設來源。

原來源仍 `not triggered`。完整319排除、兩族偶補正值、一般主命題、
Lean與strict completed-source descent都沒有被此交叉審查升格。
