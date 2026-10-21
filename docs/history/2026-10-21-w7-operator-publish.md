# W7 完整計數、可復用結構與專用算子發布

2026-10-21；來源 BASE `d5b8a8605bcbcef7aebbcf1934dad7ba255ccf02`。
本批發布相連的[完整必要模型](../../audits/2026-10-20-w7-count-cone-d5b8a86/REPORT.md)、
[原數值探索與交接](../../audits/2026-10-20-w7-count-opt-d5b8a86/HANDOFF.md)、
[六模板、精確秩及專用算子](../../audits/2026-10-21-w7-reuse-d5b8a86/REPORT.md)。
原報告的「未提交」保留當時語境；發布保存核對見
[本批紀錄](../../audits/2026-10-21-w7-publish-d5b8a86/REPORT.md)。

全部307197個交換欄精確重建於六種模板與335種受限形狀；rank(D)≤103787，
至少18829條方程相依，尚未選出全域獨立方程組。兩個CPU後端保原座標及
十項正量，獨立算子測速合計約快1.44／1.26倍；不宣稱整體求解同比加速。
60秒可行性修整13207次迭代，最佳取樣殘差2.99e-8→2.60e-9，支援卻由
170466增至262687，沒有精確primal／dual、來源排除或新Lean定理。
嚴格W7計數錐、一般C7多內點、J1／J2與較小bad均維持OPEN。

35份大型或歷史whitespace輸出依既有ARCHIVE格式追加32個去重blobs，
原111777792 bytes與全部舊records保留；沒有刪改原數據。新checkout先還原：

```bash
python3 -B tools/audit_archive.py restore --artifacts
python3 -B audits/2026-10-21-w7-publish-d5b8a86/verify.py
audits/2026-10-20-w7-count-opt-d5b8a86/py -B \
  audits/2026-10-21-w7-publish-d5b8a86/verify.py --numerical
```

發布核對保留既有69份算子證據seal、88份計數模型seal及2649份來源輸入。
共享routing文件的授權變動以publication的routing-before快照對照，沒有重寫舊BASE。
數學完整性、精確證書與數值試跑的意義分開；normal／seed17、反控制與實際
發布檢查結果見本批紀錄。算子用法及重播見
[README](../../audits/2026-10-21-w7-reuse-d5b8a86/specialized/README.md)。

Closure scope：固定必要模型的精確表示、秩界與數值算子交付完成；計數錐仍OPEN。
Updated：Kempe導覽、STATUS、README發布連結與audits還原入口。
Reviewed-unchanged：HANDOFF研究線列表、一般來源與Lean狀態。
Remaining OPEN：精確共同證書、共享Z獨立基底、來源排除及一般主命題。
Propagation stop：L1；數值與有限表示的改善沒有關閉父數學義務。
