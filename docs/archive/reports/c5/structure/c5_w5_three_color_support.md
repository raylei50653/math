---
docgraph:
  id: c5.w5-three-color-support
  family: [c5, c5.w5]
  requires: [c5.degree5-link-reductions]
  derives_from: [c5.w5-marked-relation]
  verified_by:
    - audits/2026-10-13-w5-three-color-support-19209f4c/REPORT.md
    - audits/2026-10-13-w5-three-support-19209f4c/REPORT.md
    - audits/2026-10-13-w5-small-representatives-6cafdfb/REPORT.md
---

# 全內部 W5 的三色具名 support 與 annulus 代表界線

2026-10-13 整理：接續[五商圖完整重建](c5_w5_marked_relation.md)，本頁負責
三色支援的保存契約、私人森林排除及代表界線。
保 Σ、保 R³ 與完整 fibres/lifts 的區別，以及後續單環、雙環、圈秩三／四
覆蓋鏈，集中見[完整關係 §0](c5_w5_marked_relation.md#0-保存強度與私人圈秩覆蓋鏈)。
目前停止點由 [Kempe 導覽](../../../guides/c5_kempe_guide.md#3-停止點與保留缺口)維護。

**在所有完整 Σ∉K132 的 disk-C5 圖中先最小化內點、再最大化邊數的完整來源
前提下，任取合法全內部 induced W5，後續[圈秩四兩支排除](c5_w5_private_rank4.md)
已使私人 `ρ(F)≥5`。一般縮減、小代表及 K∞=K≤5 仍 OPEN。**
此下界涵蓋本頁森林排除給的 `ρ≥1`，不取代本頁獨立的三色 transport 契約。
metadata 的 `requires` 指森林及最小來源應用的[五輪來源](../degree5/c5_degree5_link_reductions.md)；
§1 的一般 annulus 染色命題不需最小性。

[小代表保存契約與合法替換](../../../../../audits/2026-10-13-w5-small-representatives-6cafdfb/REPORT.md)
明訂最弱條件為 `pr_B R³` 相等，即補中心後完整 Σ 相等；外部環境只沿 B 接入。
它不要求 U 色列、中心色、環帶染色數 χ 或完整染色數量相等。
對已認出 Σ∈K132 的 induced-B 來源，102 份實際合法環帶代表均有 `r′≤5`、
補中心後內點≤11；另有任意 `r=m→0` 的嚴格替換族，完整控制為 `16→6`
內點、Σ=1023、capped lifts `485→20`，R³ 不等。
另有私人 `1→0` 的同 Σ 替換，環帶 χ 為 `3→4`，區別 χ 與 lifts 數。

[K15](c5_k15_sphere.md)使目前門檻為 `r′≤9 ⇒ 6+r′≤15`。
一般九點代表及真正最小目錄外來源的嚴格縮減仍 **OPEN**；在允許合法橋面的
環帶類中，普遍九點代表與主命題 K∞=K≤5 條件等價，不由 K15 自動推出。
已認出關係的代表構造使用四色定理的共面非邊引理；來源專用 degree／
三角化前提不施加於代表，也未證一般保 R³ 的代表。

原輪次整合兩份凍結 BASE `19209f4cf68261fdce5e84a7804cfe04ae0957bf` 的
互補交付：[三色充分性與保存強度](../../../../../audits/2026-10-13-w5-three-color-support-19209f4c/REPORT.md)
及[私人森林排除與代表契約](../../../../../audits/2026-10-13-w5-three-support-19209f4c/REPORT.md)。
以下保留其 `k≥13`、`r≤6` 門檻與重播紀錄；後續 K13／K15 及更高圈秩
排除不改原證書或原輪次的 OPEN 語境。

三色充分性的觀察已在上游 THEORY 出現；兩份交付補足完整契約、雙向染色搬運、
保存強度與控制，不能重複計為兩項代表存在定理。

## 1. 同槽位契約與精確保存目標

固定色集 C={0,1,2,3}。B=(b0,…,b4)、U=(u0,…,u4) 是十個互異的原 pins，
各誘導有序 C5。A、A′ 是有限簡單 plane annuli，B 是原外面，U 是同一具名
槽位的空內面，其餘頂點與邊在兩圈之間。邊界次序、內外側與介面 attachments
須已對齊，沒有隱藏接點。各圖保留自身全部原邊、旋轉、ownership 及完整 fibres。
在各自 U 空面加入新中心 v，且只加入五條 vu_i，得 G、G′；中心沒有額外禁色。
這份命題不需最小性、edge-critical、N2 或 near-triangulation 身份。

以同一 literal 色名定義

\[
J_A(\beta,\tau)=\{\eta:\eta\text{ 是 A 的完整 proper 染色},
                    \eta(B)=\beta,\ \eta(U)=\tau\},\qquad
R_A^3=\{(\beta,\tau):J_A(\beta,\tau)\ne\varnothing,
                              |\operatorname{im}\tau|=3\}.
\]

十個外框代表與全部 120 個 proper 三色 U tuples 給出 1,200 個具名 cells。
完整證書另保留每列全部 1,024 格，包括空 fibres。共同 S4 換色涵蓋全部
240 個 literal beta；不能獨立正規化 U，或以 beta、tau 各自的 marginals 拼接。

U 是奇五環。每份能補中心的完整 A lift 恰用三色，v 必取唯一缺色，故

\[
\mathcal C_G(\beta)\cong
\bigsqcup_{\tau:\,|\operatorname{im}\tau|=3}J_A(\beta,\tau),\qquad
\Sigma(G)=\operatorname{pr}_B R_A^3.
\]

因此 R_A^3=R_A′^3 **當且僅當** G/G′ 的全部完整 lifts 存在保每個 B/U pin
及中心色的雙向 total 對照。每個共同非空 cell 的兩側 fibres 作 Cartesian
product 即得這個對照；也可各選一份完整目標 lift，給可執行的兩向函數。
它們未必互逆、單射或滿射，**不給 fibre 雙射、計數相等或私人 assignments
的可逆重建**。若只要求完整外框 Σ 相等，精確條件僅為上述 beta 投影相等。
詳細證明及同槽位幾何見
[充分性報告 §§1–4](../../../../../audits/2026-10-13-w5-three-color-support-19209f4c/REPORT.md)
與 [雙向 total 契約](../../../../../audits/2026-10-13-w5-three-support-19209f4c/t1/REPORT.md)。

原控制分別證明：相同 capped Σ 可以有不同 R³；相同 R³ 可以有不同 fibre
重數；相同 R³ 也可以有不同四色 U support。這些是更強保存宣稱的
`counterexample`，不反駁上述充分條件。五商圖的逐份無損重建仍沿用原定理。

## 2. 最小來源的私人森林已排除

來源限定為全部目錄外 disk C5 圖中先最小化內點數 k、再最大化邊數的 G。
取任一原全內部 induced W5，令 P=V(G)\(B∪U∪{v})、r=k−6。
使用上游 k≥13、內面三角化、內點 degree≥5、沒有 occupied triangle/C4、
原內點不接非相鄰 B 點，以及原 B/U 不交、U 內恰為中心的完整前提，已證

\[
\boxed{G[P]\text{ 必含環。}}
\]

若私人圖是森林，原面與 degree 計數先將任意大小、多分量及分支樹化成
單一七／八點路徑。保原旋轉的完備分類只剩 70 個必要模板，直接全染色及
獨立重算均得 Σ=1023∈K，與目錄外身份矛盾。普遍量詞來自紙面完備化約，
不是有限搜尋大小的外推。完整論證與前提見
[FOREST-EXCLUSION](../../../../../audits/2026-10-13-w5-three-support-19209f4c/forest/REPORT.md)
及 [獨立審核](../../../../../audits/2026-10-13-w5-three-support-19209f4c/t1/forest_independent.md)。

這限制來源私人圖；沒有限制代表私人圖，也沒有排除含環來源壓成小森林代表。
留下的環可能 contractible，尚不能要求環繞 U；不能挪用此結論到 N2 或任意
edge-critical 圖。

## 3. 已構造的 r_min=2 與來源專用商圖障礙

一般 annulus 的具名三色 support「b0=u0，其餘 proper B/U 色列自由」有
精確 r_min=2。兩個私人點 x,y 與 b1 成三角形，b0、u0 皆接其三點，給出
合法同槽位代表；完整定向面、旋轉及雙向 lifts 見
[構造與下界](../../../../../audits/2026-10-13-w5-three-support-19209f4c/representatives/REPORT.md)。
任意單一普通代表若 r≤1，總有一份使用三色且 b0≠u0 的 pin 指派通過全部
sound pin 邊，唯一私人點再取第四色，所以必洩漏；此下界甚至不需平面性。
因此一般 r≤1 代表存在命題已被否定，r=2,…,6 沒有被否定。

在該圖三角面反覆插入三度點，可任意放大來源而保持全部 support；固定控制
保存 r7→r2、補中心後 13→8 內點的完整搬運。這類含可移除三度點及 occupied
triangle 的來源不符合真正最小來源前提，不能供應其 r≤6 存在義務。

另對同一假定最小 933／941 來源，五份較小單對商圖均落在 K。目錄中包含於
933 的 masks 僅 165，包含於 941 的僅 165、424、429，全部缺原接受列 `01232`。
故依來源挑選 sound 商圖分支、甚至再加合法平面邊後，普通正聯集都不能還原
原 Σ。保 `01232` 的分支必洩漏 `{01021,01202,01212}` 中至少一列；原 wheel
lift 落在兩個相鄰商圖，迫至少兩份不同的拒絕列 H lifts。詳細量詞及原映射見
[來源專用 no-go](../../../../../audits/2026-10-13-w5-three-support-19209f4c/conditional/REPORT.md)。
此結論保留帶重數的完整共同 lift 重建、私人部分替換及其他較大區域縮減。
兩份抽象 support 控制僅證投影限制可同時成立，沒有聲稱具 annulus 圖實現。

<a id="4-實際重播證據層與剩餘義務"></a>

## 4. 原輪次重播、證據層與停止點

本輪下列九條只讀重播全數通過；主三色 checker 的 normal/seed17 證書相同。

```bash
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/controls/check_three_color_support.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/controls/check_three_color_support.py --check --seed 17
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/review/independent_check.py
python3 -B audits/2026-10-13-w5-three-color-support-19209f4c/review/strict_support_check.py --check audits/2026-10-13-w5-three-color-support-19209f4c/review/strict_support.json
python3 -B audits/2026-10-13-w5-three-support-19209f4c/t1/check.py
python3 -B audits/2026-10-13-w5-three-support-19209f4c/representatives/check.py --check
python3 -B audits/2026-10-13-w5-three-support-19209f4c/conditional/check.py --check
python3 -B audits/2026-10-13-w5-three-support-19209f4c/forest/check.py --check
python3 -B audits/2026-10-13-w5-three-support-19209f4c/t1/forest_independent.py
```

三色主域為 34 圖、348,160 cells、3,250 H/1,620 G lifts；兩個補充圖另存
20,480 cells。森林域為已證完備的 70 模板、716,800 cells、701,956 空格、
18,282 H/9,308 G lifts，獨立逐份重算一致。代表與 no-go checks 分別核對
具名 equality 圖及全部 132 目錄 masks；沒有新增一般 annulus 枚舉。

另以獨立臨時輸出重播森林 seed17 與刪一份 full lift 的破損證書控制：正常
通過、破損被拒絕。原三色 MANIFEST 66 項與另一包 DELIVERY 47 項的 hashes/
bytes 均相符，沒有改動凍結證據。兩包隔離當輪紀錄分别见
[R³ verification](../../../../../audits/2026-10-13-w5-three-color-support-19209f4c/verification.json)
及 [森林 verification](../../../../../audits/2026-10-13-w5-three-support-19209f4c/verification.json)；
正式發布的文件核對見[本輪發布紀錄](../../../../history/2026-10-13-progress-publish.md)，不覆寫上述紀錄。

普遍 transport 與來源化約是紙面證明；有限圖控制為 `triggered and holds`，
更強保存候選有明列 `counterexample`。真正最小 933／941 來源為
`not triggered`；零目標控制不構成來源排除。沒有新增 Lean theorem；發布的
Lean 回歸另記於上述歷史，不表示本頁紙面論證已形式化。未重跑上游外部計數。

當時接後續單環、雙環及[圈秩三排除](c5_w5_private_rank3_contractible.md)，剩餘來源私人圈秩至少四。當輪仍需對該域構造合法同槽位 A′，
保原 R³ 或明列較弱的完整 Σ 目標，且嚴格減少私人點數 r′<r；這已足以與
全域最小內點性矛盾。若更做到 r′≤6，才另接 5+r′+1≤12 與 K≤12=K≤5。
一般代表存在、其他合法縮減、十四內點以上來源排除及 K∞=K≤5 均仍 **OPEN**。
各子結論採納停在其明列域，不提升為父命題完成。

2026-10-13 覆蓋核對：單環與雙環已排 `ρ=1,2`，圈秩三 essential／contractible
已排 `ρ=3`，[圈秩四兩支](c5_w5_private_rank4.md)再排 `ρ=4`；
上述當輪「剩餘圈秩至少四」由完整最小來源下的 `ρ≥5` 涵蓋。
十四／十五內點來源另由 K14／K15 涵蓋，當前一般目錄外來源須 `k≥16`；
原 `r′≤6` 是 K12 的充分門檻，K15 的 `r′≤9` 只是放寬充分門檻。
這些後續皆未解決一般私人 `ρ≥5` 來源的合法嚴格縮減或一般小代表存在。
