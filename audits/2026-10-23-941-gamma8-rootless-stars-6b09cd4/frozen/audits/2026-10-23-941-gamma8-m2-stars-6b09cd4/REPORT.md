# 941：Γ8 的 T 五度原星與完整 M2 接合，條件外側界升至五／六

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
接續[Γ8 外側與 B14](../2026-10-23-941-gamma8-exterior-6b09cd4/REPORT.md)，
保同一原圖、色框、rotation、完整原 stars／B14、全 fibres（含空列）與 full lifts。

**恰二內點且原 T 五度時，外側原 stars 的四／五個必要私有點可以全部避開
另一側 M2。** T 外側 link 只有 r–a–b–sΓ；唯一原色2鄰點 m 在 C 或 E。
m∈C 時保護點避開完整 M2∩E，m∈E 時避開完整 M2∩C。

因此前輪完整 M2 分離義務在下列子支必**另添一個不同的 Γ 外私有點**：

- h=c、m∈E：L／R 至少5個、O至少6個。
- d=U 或 e∈{V,Y}，且 E 碰框、m∈C：同樣至少5／6個。

若外點恰達舊4／5界且 T 五度，唯一 m 必位於所需分離側；沒有把完整
分離集縮成 {m} 或 {v}。E rootless 的例外保留。這是同一外側 stars 與
完整分離集的條件接合界，未完成完整外側 disk，也未排11型。

[PROOF](PROOF.md)給逐分支紙證；[producer](produce.py)與獨立
[checker](check.py)從不同生成方式重建104份四面／T-star必要限制。
1,320個具名 set-partition 候選得到同樣104列；同圖八作用及六palette
共832／4,992份完整局部分量限制。全部22個型／T-star側別仍有必要列。
這些列不宣稱原圖來源、完整 collar 或完整 stars 已實現。

```sh
python3 -B audits/2026-10-23-941-gamma8-m2-stars-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-m2-stars-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-m2-stars-6b09cd4/check.py --negative
```

凍結及前輪保管見[INPUTS](INPUTS.json)，實際重播、反控制及前輪重播見
[VERIFICATION](VERIFICATION.json)；量詞／證明自審見[REVIEW](REVIEW.md)。
正常／seed17一致，16項語義及2項外部反控制全拒絕；前輪正常／seed17／
反控制重播通過，79份凍結輸入及328份前輪檔案零漂移。正式文件與scoped
DocGraph通過，全樹DocGraph未重跑；本輪未重算全部原caps。
有限校準為 `triggered and holds`，完整來源仍 `not triggered`。

下一窄義務是 T 五度且 m 在所需分離側的完整接合，或 T≥6 的外側 link。
一般 wrong-side、更多內點、較長Γ、八配對、941／W7／J1／J2、較小bad仍
OPEN，共同 k≥23不變。無新Lean、LP或來源枚舉。本輪未commit／push。
當前入口由[Kempe導覽](../../docs/c5_kempe_guide.md)維護。
