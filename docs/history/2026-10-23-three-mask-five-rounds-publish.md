# 932／933／941五輪進展整理與發布

2026-10-23；發布前BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。
依使用者「整理目前進展並commit + push」要求，保存五輪相連紙證、完整
fibres／full lifts、來源反控制及正常／seed17重播；不改歷史報告的當輪語境。
本次發布不增加數學結論，一般932／933／941、實際較小bad與新Lean仍OPEN。

| 原來源範圍 | 五輪累積成果 | 下一個窄義務 |
| --- | --- | --- |
| 原全域最小Σ932、h=4、20份C9 collar | 三接點與距四雙接點全排；完整環帶排s=0，得s≥1、深點d≥2、原Q長9+s≥10。真弦兩側皆有深點，端點C contacts距離≥3 | 保同一原Q、可變single contacts、全空band及全部lifts，追完整relation或合法原弦cell回填；Q仍可有弦，h≥5亦OPEN |
| 原全域最小r6／933、p/h兩五度星 | 固定Q1／Q2／fan-B完整支持方法關閉；兩個新k−2填片縮至六D fibres。同D兩次共面識別另得合法k−8新外框圖H*，支持限271／314／319，迫兩個16-fibre OR正族 | 追兩個OR正族、六fibre全空或非crossed掛橋C的原02長路／induced C7；H*在K132，尚非bad |
| 原941 ordinary short Type-I、初始02型13／36，同一F | 完整分量樹與最後橋點後繼已固定；wrong-side迫兩次真界面橫穿、兩份共同四色原面patch，任兩不同中心patch合至少六原點 | 追兩patch沿同一界面的次序與共點；僅各k2必私有。B側、一般wrong-side及初始八配對未排，R/r可同可異尚未知 |

932未平均的C6／C7計數仍僅rank≤2／3；第四輪只對unused-color群和使用
folded rank-one。一般s的proper Q row即使無C環帶lift，也不能從原J刪去。
933的H*外框改為`(A,s,v,w,t)`，不宣稱保存原B十列；前兩個正D族對全部
原rxy帽皆空，不代表D fibre空。其非crossed長路引理針對同一完整E著色，
不預設bph可回填原G，V crossed例外保留。941不能把兩palette獨立見證接成
同源patch，也不能把至少六原點算作六私有點。共同k≥23未提高。

五輪權威入口依序為：

1. [第一輪：三條方法與來源契約](../../audits/2026-10-23-three-mask-methods-cb8f859/REPORT.md)。
2. [第二輪：三接點排除、固定三圖方法關閉及原路徑瓶頸](../../audits/2026-10-23-three-mask-round2-cb8f859/REPORT.md)。
3. [第三輪：單pair、兩個新填片及最後橋點](../../audits/2026-10-23-three-mask-round3-cb8f859/REPORT.md)。
4. [第四輪：距四全排、六D fibre及原分枝二分](../../audits/2026-10-23-three-mask-round4-cb8f859/REPORT.md)。
5. [第五輪：非空single層、新換框圖及共同原面](../../audits/2026-10-23-three-mask-round5-cb8f859/REPORT.md)。

本批五輪原域為738檔、69,861,223 bytes；精確bytes／SHA見
[發布BASE](../../audits/2026-10-23-three-mask-publish-cb8f859/BASE.json)。
所有原檔及歷史「未commit／push」敘述均保留，後續發布狀態以Git為準。
另納入原先已變動的[共通語言單向回填接口](../reference/c5/c5_common_language.md#31-保壞下降一份接受見證與三個單向回填)，
其來源存在性仍OPEN；同一實際外側的接受見證與三個單向完整回填必須兼容。

發布核對、精確命令及失敗／適配邊界由
[本批發布報告](../../audits/2026-10-23-three-mask-publish-cb8f859/REPORT.md)承擔。
正常／seed17、來源負控制、frozen SHA、lake build、94項工具測試、文件與
Git index生成檔政策分開記錄；lake build不把新紙證或Python證書形式化。
正式docs DocGraph與全樹封存duplicate-ID診斷分列；push與遠端CI亦分列。

```sh
python3 -B audits/2026-10-23-three-mask-publish-cb8f859/verify.py
python3 -B audits/2026-10-23-three-mask-round5-cb8f859/check.py
```

Closure scope：只採納上述來源限定子義務，未關閉一般三支或較小bad。
Canonical Source + Evidence：五輪原報告與原證書；發布BASE／回執只負責保存與重播。
Updated：Kempe導覽、C8剝層與no4ct直接父入口、STATUS簡短索引、共通語言接口及本發布紀錄。
Reviewed-unchanged：README用途／閱讀路徑、HANDOFF研究線／進行中標記、全部原738檔。
Remaining OPEN：h=4的一般s≥1來源、h≥5、933六fibres與兩OR族、941八配對、W7／J1／J2及一般主命題。
Propagation stop：L2；直接父題已同步，較高層共同界與主命題狀態未變。
目前接續由[Kempe導覽](../archive/guides/c5_kempe_guide.md)維護。
