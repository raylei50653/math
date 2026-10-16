# R6-101-NONWHEEL-SEVEN-CUT 研究報告

2026-10-16。BASE `main / 120aae90cab8bc4881916adc598cf344f2f20f4b`。
**分級 B：取得任意大小結構定理，101 普通匹配存在性仍 OPEN。**

## 結果

在使用者固定的同一原始最小來源 G、同一 J、實際 D 與任意最大違反集 S 下，
新的紙面定理證明：

1. 非輪七割 C 的補集必連通，故 C 是實際簡單七邊形 disk，三角孔配置不可能。
2. C 二連通，有七個不同內度二 ports；其他點內度三。邊界所有弦在盤外，
   m,z,v,w,p,q 均非盤內點。
3. 若 I 是奇度盤內點數、B 是奇 inward-degree 邊界點數，則 `I+B≥12`。
   因此 `I≥5`，且 `|C|≥15`。
4. 任意大小、至多四個奇度盤內點的**整個無界子類**被排除。
   這允許任意多偶度盤內點，故不只是有限小圖排除。
5. 保留所有 matching lifts 與空 fibres 的 tight 七埠 registry 有 560 格，
   其中 140 格由 parity 必空，最多 420 種有效簽名；全 ordinary 介面
   為 1206 格、最多 904 種有效簽名。內部 matching 數與圖大小仍可無界。

核心新不等式來自原 m 的實際扇區面字串：若 m 不被奇 inward incidence flip，
兩個原 s/t 度都須奇且至少七，於 m 強迫兩個 excess 單位；若被 flip，
weighted charge 已付兩單位。這將純 Euler 下界再提高，
而不是把有限枚舉提升成任意大小結論。

[PROOF](PROOF.md) 提供完整紙面推導；獨立路線是 [GEOMETRY](GEOMETRY.md)
及 [MATCHING](MATCHING.md)，[REVIEW](REVIEW.md) 記錄獨立數學審查。

## 精確剩餘問題

**R6-101-SEVEN-DISK-ODD5**：排除以下同來源配置，或提出保全完整來源 fibres 的合法下降：

- 真正七邊界三角剖分 disk R，內部至少五個奇度點，C 至少十五點；
- 內部六具名點皆缺席，七個有序 ports，外部弦及所有原 rotation 保留；
- 同一外部含原 X、f、S 與其餘 singleton，cut budget 為零；
- `Δ=I+B-2ε-10`、`Δ≥2(1-ε)`，以及原 m/z 扇區、小 C4/C5 限制；
- 非空共同 P111 的全部 matching lifts，以及全部原染色空 fibres 和 r lifts。

本輪沒有證明這些 420 個有效簽名在來源上全部為空；也未建立能以固定 gadget
取代任意內部、同時保全原染色關係與具名邊的 theorem。
固定狀態數不代表內部圖有限，更不代表完成來源嚴格下降。
接續工作可把來源限制加在此有序介面上，或從至少五個奇 bounded dual faces
尋找必然的原小圈／原扇區衝突。

## 證據與範圍

| 層級 | 本輪身份 |
| --- | --- |
| 任意大小結構與子類排除 | 紙面證明，獨立審查 PASS |
| 七埠 matching/Tait 介面 | 紙面精確 bijection；固定局部 controls 重播 |
| 有限校準 | 三個明列局部 patch；完整 fibres、正常／seed17／負控制 |
| 真正最小來源數值測試 | 0，not triggered |
| Lean | 既有 `lake build` 通過；沒有新增 theorem |
| 版本管理 | 僅獨立 audit；未 commit、未 push |

13 面 synthetic patch 有四個奇度內點，factor-critical 且通過局部 Euler 校準，
但不能滿足原 m 扇區新必要條件。它說明原來源前提不可省略，
不是 source 反例。所有計算域與失敗紀錄見 [VERIFICATION](VERIFICATION.md)。

101 普通 PM、101 偶補正值、`W110+W101>0`、完整319與一般無界主命題均 OPEN。
`K≤22=K≤5`、固定 r6 的 `k≥25`、接回成本 `k+5` 全部保持原狀。

## 封存與文件邊界

[BASE](BASE.json) 記錄原乾淨 HEAD 及 531 個前輪／權威輸入 hashes；
[MANIFEST](MANIFEST.json) 封存本輪成員。前輪四個 audits 的內容與成員名單不變。
未覆寫既有 frozen audit；本輪初版及修正後證書與失敗啟動紀錄均保留。

已核對 Kempe guide、STATUS、直接 C4 父題的當前七割 OPEN 說法。
本輪交付為獨立 audit，未將 B 級新引理自行採納成父題 closure；
故共用 routing 保持原樣。HANDOFF／README 的研究線和使用方式沒有改變。
文件檢查與 scoped DocGraph 通過；全樹仍有 70 個歷史重複 ID，
與 BASE 類型／ID 相同，未刪除歷史證據換取 PASS。
