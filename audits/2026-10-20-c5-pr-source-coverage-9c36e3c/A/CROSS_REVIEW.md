# A 交叉審核：主報告、整數逆式與 B／C

2026-10-20。所讀版本的 SHA 見 [cross_review_inputs.json](cross_review_inputs.json)。
主報告仍由 root 整理；這份清單記錄交叉審核當時版本，不要求後續授權的文字補充
與該 draft SHA 一致。A 不修改主報告或 B／C 檔案。

## 1. 主報告 §1、§2、§4

- 四列 tuple 的全字串行為與完整十列支援的雙向命題正確。
  三探測反向不依賴 K132 來源假設；正向僅用任意 disk 合法的 P/R。
- 一般覆蓋化約到 `K∞=K132` 正確；接到 `K∞=K≤5` 時已單列原
  bounded census authority，沒有把 132 個 witness 的重播偷當完備性。
- 零支援及 932 均保留；no4ct 的限制已明示。
- `Q=2M_P^-1` 的七個搬運座標及三個半和公式逐項正確。
  `QM_P=M_PQ=2I` 給唯一有理前像；三角不等式加偶和恰給非負整數前像。
  這個形式像沒有宣稱任意符合條件的向量具有實圖來源。
- 葉點全 3 向量是合法一般 disk 的實圖反例；用最後 P 加任意 trailing R
  的奇偶矛盾排除所有大小的 count 代表，零 P 種子另行排除。
  不能將該反例跨用到 near-triangulation／critical／r6，主報告已有界線。

本輪直接執行 root `check_integer_inverse.py --check`，結果 PASS：
determinant `-2`，Boolean image 640，前像 histogram `512×1+128×4`。
A 自身 checker 在 `/tmp`、`PYTHONHASHSEED=17` 下重播亦 PASS。

## 2. B：發現並修正的共同字串量詞

最初 B draft 對非零 basin 的文字只保留 `forall m exists w`，
並寫「沒有給 exists w forall m」。A 指出，有限非零態皆可達吸收集合 K，
加上 P/R 保非零，已可透過逐步消除尚未入 K 的原狀態得到一個共同字串。
這項修正已傳給 root 與 B，B 後續提供更強、具體的固定字串

```text
W = RRR(PPR)^4P(PRP)^4
```

把每個非零 mask 直接送到 1023。
已審更新後 `B/REPORT.md` §2.1 與補充 checker：
十 singleton 在同一 W 後全部為 1023，加上 Boolean 線性作用保聯集，
充分證明全部 1023 個非零 masks 的共同結論。checker 另逐態交叉核對。
不需要外側 4CT，因為命題明定初始支援非空。
17 次 P 是這份構造成本，沒有最優性聲稱；也不構成來源下降或原框代表。

兩個 B checker 均直接只讀重播 PASS。主轉移證書 SHA：
`c5a128a4de09fece8f3dd42d90372c4af49b3fe476a1d3a242f48c0b43a06349`；
共同 collar 證書 SHA：
`f776a67219bc023157ee1a034f9ebcf6478613b6c1f110737d32db4690a8e224`。
933／941 的 first-P 定理與 932 六態 quotient 的形式／實圖界線正確。

## 3. C：逆 P／I 與完整限制映射

已讀 C 紙面報告 §1–4、完整 checker 及圖證書，並直接重播 PASS。

逆 P 的必要／充分條件保留：框點 degree 3、第三鄰點為內點、
兩個**實際空三角面**。這些條件使刪除的 collar 無私有結構遺失，
新框五點相異；不是只見三角圈或三條鄰接即判可剝。
在內面全三角的簡單 disk 域，後兩個 incident 面確由 degree 3 強制。

I 的 restriction/unique-fourth-colour 是完整 fibre 雙射，空 rows 同樣成立。
對交錯的 P/R/I 構造，C 的強版本可直接成立：
I 點出生後一直是內點，後續 P 不接任何 I 點；依 I 插入次序的反序刪除，
後 I 造成的額外鄰點先被刪除，當前點恢復其原三角星。
留下的圖恰為略去 I 的 P/R 骨架，最終有序框相同。
所以結論是同一來源的真正完整染色限制雙射，強於僅比較 count vectors。
此理由已傳給 root，建議主報告明寫，避免將「略 I」讀成無序任意刪點。

五輪五面各插點的 degree-5 框阻止逆 P，逆 I 則逐次回 FP；
這給任意大小子類與純 P/R 圖族嚴格包含的紙面證明。
正二十面體去點圖的 degree-4 框、degree-5 內點阻止兩種逆步，
十列計數全 2 且支援 1023，完整枚舉與拓撲檢查一致。
它不屬 P/R/I 生成族也可由「最後非 R 步必產生一個 degree-3 點」直接確認；
此結果不排除它有其他計數文法代表，C 正確保留這個邊界。

重播摘要：6 個初始圖、60 個完整 fibres（18 空）、57 份完整染色；
5 個逆 I 逐列完整限制雙射、4 個 P/逆 P 圖 roundtrips、
4 項非法操作拒絕，全通過。

## 4. 最終審核判定

本輪已讀範圍沒有未修正的實質錯誤。共同 collar 的量詞修正已落實於 B；
主報告略 I 的來源級理由由 C 補足。
一般來源覆蓋仍 OPEN；本輪沒有把任何 K 外形式 mask 實現為 disk、
沒有給 r6 success／smaller-bad 構造，也沒有以有限支援轉移代替原來源存在性。
