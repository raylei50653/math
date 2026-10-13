# 2026-10-03：ε=2 四-spoke 原 unary crosscut 與 mixed 二／三 hub 排除

使用者要求「繼續推進 ε ≥ 3」，並在工作中要求「繼續」。接手
HEAD=`0e38127`，cwd=`/home/ray/developer/ai/math`，沿用未提交的短／長
face 成果；記憶停止點已落後，以即時 HANDOFF／STATUS／Kempe 導覽
選具名 941 原 01／03、933 原 01／13。沒有重開來源 catalogue，
未 commit／push，既有 artifacts 保留。

## 窄結果與原來源身份

[報告](../c5_excess_two_mixed_core_four_spoke_crosscut.md)、
[checker](../../scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py)、
[joint helper](../../scripts/c5_excess_two_four_spoke_crosscut_joint_controls.py)、
[artifact](../../artifacts/c5_excess_two_mixed_core_four_spoke_crosscut/observations.json)
保存 fixed complete Σ=933／941、Σ edge-minimal induced-C₅ disk 的
任意大小窄排除。有效 H 連通、ε=2、相鄰雙完整 degree-5 roots，
其餘有效內點完整 degree 四；唯一 mixed incidence-(1,1)，原
contacts=(x,y) 可同頂點，各側一原單接點 unary 與兩 spokes。
所有原 C／U／V、attachments／actual supports、bridges、旁支、
ownership、環序及共同字面色框保持。

Critical U 的實際支援迫原 a–U–b₃ crosscut，C 的原 b-contact 使它
只能留在 b-side，支援封到 {3}；另一位置是原 0ab 三角。固定原外部
coloring，C 拒絕時 exact lists tight、K₄-free Gallai；同一原 U 路徑
提供三個相鄰 hubs。a 與 b₃ 色不同時用三-hub 引理；同色時先以
tightness 排除 C 共鄰碰撞，再保 degree 合併為兩 hubs，兩種都給原
K₅。因此每份原 G−C coloring 可接回完整 C，外部頂點逐點固定；
四角色投影相等，原 ax 非 critical，不需 Σ(G−C)=Ω。
沒有宣稱六角色 joints 相等，沒有把 topology contraction 當作染色操作。

| 必要框架 | 933 | 941 |
| --- | ---: | ---: |
| 前序 unequal | 22 | 40 |
| 本輪原 crosscut 排除 | **8** | **16** |
| 剩餘共用框點 | 0 | 6 |
| 剩餘不相交 pairs | 14 | 18 |
| 剩餘合計 | **14** | **24** |

新排 indices：933=100,113,116,127,156,162,172,190；
941=134,137,156,160,174,181,196,222,237,245,262,266,280,281,305,306。
選定原 identities=100／156 與134／174含 root 交換。整圖幾何
搬運 g(i)=1−i mod5 將933原01／13送至01／03，但完整Σ933送到
940而非941；全列共同搬運與來源mask區別已保存。

30原骨架有2,880rotation assignments／60disk rotations；24所排
框架各8份actual U、C support子集，各共192。Critical U相容48，
C crosscut相容48。48明示apex K₃,₃ subdivisions保存九條paths。
720合法列／root-color cases分192同色二-hub、528異色三-hub；
5,760局部tightness／degree子集，24root swaps，3,840共同D₅支援
子集、7,200列／root-color搬運、480搬運後subdivision檢查。

18完整degree手建圖包含W₄相鄰／相對contacts與原共鄰subdivided-K₄
contact、三種unary配對與root交換；720整圖joins／11,520pinned fibres
含空纖維，540四角色projection等式、7,752整份C替換witnesses，
360mixed邊接回及360swaps均由逐原邊完整coloring核對。
完整六角色joint不相等負控制保留。固定圖不宣稱disk、候選Σ或criticality；
有限拓撲骨架不補滿degree，無界覆蓋由紙面定理合成承擔。

## 實際驗證

新checker生成、預設seed及seed17逐byte重播均通過，直接依賴的
同一長face及短支援seed17重播通過。lake build通過8,831jobs，
只有既有AttachmentOrder／SymRelabel linter warnings，沒有新增Lean theorem。
短支援local／three-hub數學payload已唯讀重算相同。Dvořák講義
重新下載並核對Lemma7、Theorem10：connected degree assignment的
slack／tightness與blockwise-uniform Gallai刻畫不需critical-graph前提。
紙面與程式獨立審查通過，已補齊F內短支援的原a–b₀外路徑說明。

```bash
python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_mixed_core_four_spoke_long_face.py --check
PYTHONHASHSEED=17 python3 scripts/c5_short_support_singleton.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
python3 tools/artifacts.py status
git diff --check
```

未重跑degree-6全分拆、原singles docs漂移audit、R系列、全倉來源
catalogue、其他出口／Kempe歷程或Lean axiom audit；lake build
不形式化本輪crosscut／Gallai合成。HANDOFF研究線與tags未變，
維持薄索引；README、STATUS、Kempe導覽、整合頁與原長face的
後續說明同步。文件檢查通過506份Markdown／5,195個本地links，
anchors／index／handoff通過；DocGraph為62documents／213relations／
5families、0errors／0notes，git diff --check通過。

新artifact為38,737,018bytes，SHA256
`dae9101d20470dc24cad8d87c2e78a8596a26764c778428aed3f4f125cd26d0d`，
本地保留，MANIFEST／.gitignore記錄producer、依賴及fingerprints；
artifact status為ok=135，無missing／changed／stale。這些為本輪
crosscut bundle完成時的驗證；後续續研另記，未覆寫此原證書。

## 停止點與貼用摘要

**完成原 `(1,2,2)` 具名框架排除；共同下界仍ε≥2，ε≥3未證。**
下一941原02／03、index155／root swap175，六份共用框點殘留為
155,175,179,239,243,263。Critical U／V分居原外faces，actual
supports必含{0,2}／{0,3}；C在原0ab三角或共同短框弧{2,3}。
本輪原owner-to-far-end crosscut不適用；需保留完整原六角色joint，
研究mixed與兩unary的共同限制。其他incidence、較少spokes、單省略、
(5,5)q-core、多mixed／no-mixed／非相鄰與unary側例外保留。
來源實現、新Lean theorem、一般出口及K∞=K≤5仍未證。
即時停止點見[Kempe導覽](../c5_kempe_guide.md)。

```text
cwd=/home/ray/developer/ai/math；先讀HANDOFF/STATUS/Kempe導覽與即時Git。
HEAD=0e38127；沿用短／長face未提交bundle，本輪未commit/push。
固定完整Σ933/941、edge-minimal induced-C5 disk；共同ε≥2不變。
四spoke(2,2)、mixed(1,1)+各側一unary：941原01/03、933原01/13及交換全排。
Critical unary的actual支援給原a–U–3crosscut，C支援封到{3}或原三角{0}。
同列tightness、K4free Gallai與同一外路徑給保degree二／三hub K5。
只替換完整C、外部全固定；四角色projection相等，原ax非critical。
新排8/16；unequal從22/40到14/24，共用點0/6、不相交14/18。
933整圖幾何搬運Σ→940不是941，所有原relations及色框共同搬運。
checker：python3 scripts/c5_excess_two_mixed_core_four_spoke_crosscut.py --check。
48 apex subdivisions；720完整joints/11520fibres/7752完整C replacement witnesses。
下一941原02/03 indices155/175；U/V在不同外faces，C共同支援{2,3}。
其他分支與來源實現保留；紙面+固定Python，ε≥3與一般出口仍未證。
```
