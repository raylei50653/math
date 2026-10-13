# N2原55雙long的同來源 LL-CUT

2026-10-13，BASE `3097ef5be241b7777451a5ef8a663f3987d6b866`。
[正式來源入口](../../docs/c5_excess_two_n2_ll_cut.md)、
[完整來源契約](CONTRACT.md)、[BASE hashes](BASE.json)。

## 結果

**LL-CUT+diag 已證，完整原55 `(ℓ,u)=(2,0)` 來源排除。**
任意大小紙面論證覆蓋原剩餘 `(t_r,t_s)=(2,0)、(1,1)、(2,1)`，含支援
`{3,3}` 與允許的 `{3,4}`。與凍結前已採納 t=0／1 接回完整雙long分支。
本輪沒有重新證 t=0／1，也沒有混用其他研究線的新前提。

**基本 LL-CUT 未獨立證成。** 僅從指定基本 S 仍有共同可行抽象profiles；
本輪不稱它們為來源或反例。加強版使用原topology／degree lists證出的完整diagonal
接受資訊。來源排空後，不以邏輯真空性冒稱基本矩陣機制已完成。

[紙面證明](paper/TOPOLOGY.md)由root逐一核對原bags、所有原跨邊、各root degree、
leaf／sole-block／shared分支與共同色框；[獨立審查及父分類](review/ROOT_REVIEW.md)
將採納限制在完整Σ933／941原55契約。九格在此完整契約內全覆蓋；
較廣N2、N1、相鄰／單-root、契約外來源、E-ARC2仍OPEN。

## 紙面增量與可讀cuts

- **K5-H**：相鄰私有cycle contacts共用同一原框附件h；另一long與兩條原框弧
  構造五個互斥連通bags，不需h有spoke，逐項提供十條原跨邊。
- **K33-O**：相鄰私有contacts分屬r／s且一側尚餘incidence。
  bags為 `({p},{s},B)` 與 `({r}∪C′,{z},C−{p,z})`，九條原跨邊全部列出。
- 三列基本矩陣皆可行迫 `k_C^other≥2⇒W_C^v⊆Z(T_v)`；shared／碰色機制
  完全保持基本定義。row／column總量先排極端接線分拆。
- (1,1) 的雙側高接線piece每列diagonal皆接；(2,1)、(2,0) 指定高接線piece
  由leaf必需接線數證每列diagonal皆接。另一份低接線long在同一列接回。
- (2,0) 最後 `(1,3)/(2,2)` 如三列不接，原兩leaf-bridge附件必覆蓋一份三點弧；
  一個指定列見齊三色，矩陣每行三個固定零，觸發精確 **2≤行和≤1** cut。

上述最後接回總取同列、同pins的兩份原完整lifts，原root-spokes因D未用而合法；
兩pieces無原跨邊，全部原邊被覆蓋，自由座標乘積因子保留。

## 同來源必要介面與抽象殘留

[覆蓋論證及完整列表](profiles/REPORT.md)保留同一原支援弧、spokes、兩側incidences、
shared身份及每contact的owners／實際附件。由原資料共同投影到85份字面幾何；
Z條件外有參數化基本行／列cut。Z條件內不把三列各自的profile拼成來源。

| 支援／spokes | Z內投影候選 | 基本cut | contact不相容 | 三列共同可行投影 |
| --- | ---: | ---: | ---: | ---: |
| {3,3}／(2,0) | 17,056 | 13,234 | 2,748 | 1,074 |
| {3,3}／(1,1) | 132,165 | 108,018 | 18,584 | 5,563 |
| {3,3}／(2,1) | 77,962 | 56,918 | 15,132 | 5,912 |
| {3,4}／(1,1) | 194,740 | 151,720 | 36,340 | 6,680 |

保留19,229份共同可行投影；1,378份contact目錄展開為3,764份局部成員，
相容piece配對為64,408份。每列固定格由原附件與signature重建。
2,455份可行矩陣保留精確數量與witness；604份cut形狀保存代表固定格來源、
容量上下界及精確不等式。所有候選stream另有hash與逐byte生成重播。

這些是有限必要介面，**沒有完整來源實現**。原內邊、rotation、bridges、block角色、
普通點附件及完整Sigma／criticality witnesses保留在來源ledger，不能由投影反推。
紙面K5/K33與leaf論證正用到投影尚未保證的原結構，排除其全部合格原來源實現。
基本機制的尚未用入介面條件與可反駁窄題 BASIC-11-SAME-SITE 見root review。

## 有限證據與實際驗證

| 證據入口 | 保存與核對內容 |
| --- | --- |
| [獨立checker](checker.py) | 不import生成器／上游矩陣；完整binary枚舉、同原資料重建S及bounds、cut不等式、獨立owner分組contact計數；容量界／固定格改錯被拒。 |
| [原圖完整fibres](controls/REPORT.md) | 320局部cells／80空／856tuples；160joint cells／126空／181全圖lifts；十列16pins全保留，獨立全圖DFS與同列product相等，逐原邊驗證。 |
| [新K33控制](controls/SUPPLEMENTAL_REPORT.md) | 四種整體交換，24棵bag樹、36條原跨邊、8項負控制；root5／其餘4仍不代表合格來源。 |
| [無spoke K5-H控制](controls/SAME_H_REPORT.md) | 四種owners，20棵bag樹、40條原跨邊；沒有spoke亦觸發minor。 |
| [框與容量算術](paper/topology_arithmetic.json) | 全五個unused-edge位置、10份有序弧配置、五份三色支援witness、九份(1,1)incidence分拆、總量與最後行cut。 |
| [統一驗證](verification.json)、[文件驗證](verification/documentation.json) | 七組normal／seed17均通過、frozen零漂移、毀損負控制被拒；check_docs、正式docs DocGraph及diff檢查通過。 |

局部 S重疊／minor控制為 **triggered and holds**；舊兩piece同時拒diagonal卻有
off-diagonal joint的控制完整保留。其完整關係1023且有原K3,3，資格checker拒絕
將其升為Sigma933／941 planar來源。完整目標有限觸發仍為 **not triggered**。
零觸發沒有被用作來源排除證明。

輸入從指定Git BASE凍結；原BASE及歷史失敗不改寫。profile生成初稿的dict共用
註記滲漏已保留為 `profiles.pre-copy-isolation.json`，修正後另有正式產物；
數學欄位／計數不變。原全域DocGraph歷史duplicate-ID未處理。
沒有新增Lean theorem，未修改Lean、未執行lake build；紙面證明沒有被宣稱形式化。
沒有來源圖枚舉、上游大枚舉重跑、commit、push、PR、issue或留言。

可從[正式入口](../../docs/c5_excess_two_n2_ll_cut.md)的命令及統一驗證逐項重播。
