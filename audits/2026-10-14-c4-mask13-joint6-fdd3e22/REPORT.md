# C4-MASK13-JOINT6：共同 fibre 分解、較小介面與條件界

2026-10-14。BASE `fdd3e2289254e3f0844e2c595af50080b19f8a05`，起始工作樹乾淨。
本輪獨占 audit 的直接輸入與 SHA256 見 [INPUTS](INPUTS.json)。
**六接點無界殘題仍 OPEN；新增任意大小的 fibre 分解、r 五度的 mask7
化約，以及高 p,q 子域的 k≥28／更窄 k≥29。一般 K≤22、k≥23 不變。**

## 1. 固定來源與結果

G 沿用 no4ct 契約：在全部完整 C5 關係不屬 K132 的有限簡單 disk 圖中，
先全域最小化內點數 k，再最大化邊數。整份原圖共同對齊
`B=(x,y,a,b,c)=(b0,b1,b2,b3,b4)` 及 `Σ∈{932,933,941}`。
本輪只處理 `d_G(x)=d_G(y)=d_G(b)=4`；不加入 edge-critical、N2 或
固定 mask 最小性。原有界結果及其他分支的 OPEN 狀態均保留。

[前輪化約](frozen/audits/2026-10-14-c4-triangle-core-b66f592/ADJACENT4.md)
識別 a,c 為 z、刪 b，再刪 x,y，得到 R，外框 `Q=(z,s,r,t)`，
`|V(R)|=k+1`，p,q 是嚴格內點，zpq 是原指定三角面。
來源失敗的精確共同條件為：

| 固定 Q | 所有完整 R 染色的 pq palette |
| --- | --- |
| ABAB | {C,D} |
| ABAC | fibre 空 |
| ABCB | 前輪尚無限制 |
| ABCD | {B,D} |

R 的完整四框關係恰為 mask13，三個非空 fibres 不能丟棄。每項均在
**同一原 R、同一完整染色、同一色框**上比較。

| 本輪成果 | 精確範圍與證據 |
| --- | --- |
| ABCB 必含缺失色 D | 任意大小紙面 Kempe／Jordan 論證；只需原 C4 disk、zpq 的三條邊及上述共同條件 |
| 兩個完整 fibre 雙射 | `F(ABAB)≅F(ABCB;pq=CD)`、`F(ABCD)≅F(ABCB;pq=BD)`；第二個可能同時交換 p,q 色值 |
| 六接點必要條件閉包 | 有限抽象控制：10→8 份固定 Q 列，9→7 個 S4 軌道；剩餘閉包非空，不證實現 |
| 高 p,q 的界 | 原 `d_G(p),d_G(q)≥6 ⇒ k≥28`；紙面匹配同一外部 ≤28 計算 |
| 原 r 五度 | 刪 r 得 k 點、`k−4<k` 內點的 induced-C4 R'，完整 mask7 及新的精確六接點表 |
| 更窄交集的界 | `d_G(r)=5` 且 `d_G(p),d_G(q)≥6 ⇒ k≥29`；與上列已有 h=3／932 h=4 高 apex 子域分開 |

## 2. ABCB 的兩個共同分支

[完整證明](JOINT_FIBRES.md)使用實際 maximal Kempe components。若 ABCB
的 pq palette 是 BC，則 r 的 AC component 若避開 z，交換它會產生
仍帶錯誤 pq 的 ABAB；t 的 BD component 若避開 s，交換它會產生仍含 C
的 ABCD。因此必同時有 AC 的 z–r 路與 BD 的 s–t 路，違反外 C4 的
交錯端點分離。故原先的 BC／CB 兩列被排除。

其餘恰分為兩個非空 sectors：

- pq=CD：z,r 的 AC components 分開，s,t 的 BD components 相連。
  交換 r 的 AC component，與 ABAB 全 fibre 雙射，p,q 各自色值不變。
- pq=BD：z,r 的 AC components 相連，s,t 的 BD components 分開。
  交換 t 的 BD component，與 ABCD 全 fibre 雙射；若 component 含 pq，
  則兩點色值一起交換，不能把這個雙射寫成逐點固定 p,q。

所以 `|F(ABCB)|=|F(ABAB)|+|F(ABCD)|`；本輪保存的是較強的完整集合
雙射，沒有用計數或獨立可行列取代 full lifts。

[有限必要條件控制](INTERFACE_CONTROL.md)枚舉所有原六接點色列、
互補色對的 component partitions，以及每種 partition 的所有同步交換。
刪除不可能列後，8 份固定 Q 列仍有必要閉包；它們的 partitions 未證能由
同一個圖共同實現。舊三列抽象反控制的 ABCB/BC 已被排除，但四框 mask
本身會遺失 p,q 資訊的原結論仍正確。

補查七個軌道的全部128個子關係，恰有9個滿足此必要閉包與完整mask13，
其中4個極小者各含5軌道；因此八列只是上界，不宣稱每列必實際出現。
加入原可選邊tp或qs時各只剩一個閉包；這些仍都是必要抽象關係。

最初把 `z,s,r,t,z,p,q` 當普通 Jordan 邊界的模型錯誤排空所有列；原因是
切開重複的 z 會分裂 component。[失敗模型與輸出](rejected/README.md)
已保留並明示不採納。正式控制只使用真正外框 Q 的平面限制。

## 3. 原接線、較小候選與精確數量

[原幾何證明](SOURCE_GEOMETRY.md)保持五個原 apex
`(r,t,p,q,s)` 的身份與 rotation，排除 rp、rq、sp、tq、st；
tp、qs 恰分別對應 a、c 原四度，不能同時存在。
另由原 S6 五環限制證 `N_R(z)∩N_R(r)={s,t}`，所以外側識別 z=r
所得 k 點 J 確為簡單球面三角化圖。這項幾何補強不自行給目標延拓。

R 只有 p,q 可能是四度內點，而且 `d_R(p)=d_G(p)−1`，q 同理。
若兩者原 degree 都至少六，R 的全部內點至少五度，三角形皆為面，
induced Q 排除 diamond。它是 **k+1 點的 diagonal-forbidding 4-candidate**。
外部 [Dvořák–Lidický–Mohar §2、Table 1](https://arxiv.org/html/2504.08327v2#S2)
排除至多28總點的此型，因而 k≥28。

本輪實際核對原文定義與計算範圍，記於 [EXTERNAL](EXTERNAL.json)；
沿用其 C++ 至28點、獨立 Python/Sage 至25點的外部計算信任。
沒有重跑外部枚舉，也沒有引用未證無界猜想。

已採納的 apex 下界使上述條件確實涵蓋：

- 本分支 h=3：只剩 c04-941／c07-941 兩份必要 query，均 k≥28。
- 本分支 Σ=932、h=4：只剩 c09-induced-932，亦 k≥28。

這不把所有 h=3、所有 h=4 或所有932來源的共同下界提高到28。
若 r 原五度，[較小 R' 表](SOURCE_GEOMETRY.md#5-原-r-五度時的下一個精確小介面)
給 mask7 及 pq 的 `ABAB→CD、ABAC→BC、ABCB→CD` 精確共同殘題。
再加高 p,q 才得 k 點 rainbow-forbidding 4-candidate 及 k≥29。
上述 h=3／932 h=4 子域的 r 已至少六度，不能套這個29界。

## 4. 驗證與信任界線

完整實際命令、exit code 與 logs 見 [VERIFICATION](VERIFICATION.md)。

| 控制 | 實際檢查內容 |
| --- | --- |
| [六接點閉包](controls/check_interface.py) | 全部4^6指派；216→168標號列、9→7軌道；所有合法 partitions／完整 switch orbits；錯列、交錯路、拆原邊及篡改證書負控制 |
| [子關係及原可選邊](controls/check_subrelations.py) | 每個邊域全部128子集；無額外邊、tp、qs、兩邊的mask13必要閉包數分別9、1、1、0；最後一域已由來源h≥3排除 |
| [完整 fibres](controls/check_fibres.py) | 七張明列 plane disk 的42份完整固定框染色，含全部空 ABAC fibres；14份完整集合雙射及逆映射；漏 lift 負控制 |
| 同一 checker 的 r 表 | 四種 R' 框色與 r 的全部16指派；七種關係中只有7接成13；所有同份 r lifts 的 pq 交集 |
| [原幾何控制](controls/check_geometry.py) | 四張自含球面樣本、八個具名開口／r刪除；S6、原 apex 接線、degree 損失、共同鄰點及J；不測來源mask假設 |
| [獨立審閱](review/INTERFACE_REVIEW.md)及[原來源覆核](review/SOURCE_REVIEW.md) | fibre 證明與控制的範圍；原幾何、C8／C9接入與外部條件界 |

七張 full-fibre 控制有低度點並實際存在成功 cap lifts，均不是目標來源。
幾何控制同樣不具目錄外關係。**真正目標來源數為0；有限 PASS 不是來源
排除。** 沒有新增 Lean theorem；未重跑 Lean build、plantri 或外部≤28
完整枚舉。r 小介面是完整关系等價，不聲稱用普通 mask7 代表保留 p,q fibres。

## 5. 本輪停止點與文件接入

在 k≤27 的本分支來源，G28 迫 p 或 q 原 degree 恰五；否則研究需處理
新的高 degree k≥28 子域。所有情況仍須在同一原圖的完整染色中打破
ABAB/CD 或 ABCD/BD 的共同強迫；只排掉原 ABCB/BC 不足以完成此事。
r 五度時可使用已證 R' 精確表，不能只換成普通四框代表。
更一般 T／T0 延拓、932／933／941 整支排除及 K∞ 仍 OPEN。
目前接續入口由 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)維護。

Closure scope：完成新的 fibre 分解、原接點幾何與所列條件界；未完成
C4-MASK13-JOINT6 無界排除。
Updated：C4 權威入口、Kempe 導覽、STATUS 對應短索引及 no4ct 直接入口。
Reviewed-unchanged：一般 K≤22／k≥23、其他六份 h=3 查詢及其他 h≥4
來源、HANDOFF 研究線與 README。
Propagation stop：L1／直接父入口；跨線綜合只核對 C4 所屬摘要，不提高全域界。
本輪未 commit／push。
