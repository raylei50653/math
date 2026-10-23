# 941：Γ8 完整 rootless 星的共同六點界與對側八點界

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
承接[完整 M2／T 五度原星](../2026-10-23-941-gamma8-m2-stars-6b09cd4/REPORT.md)，
仍保同一原圖、原色框、rotation、完整原 stars／B14、全部 fibres（含空者）
與 full lifts。以下全部限 Γ8 **恰二內點**的11份必要型。

**原 T 五度時，L、R、O 全部至少有6個圈外 F 私有點。** 若完整 M2
不只含 T 的唯一原色2鄰點 m，則全部至少8個。因此前輪兩個對側分離子支
（h=c、m∈E；或穩定 C 框點且 E 碰框、m∈C）均由5／6升至 **8**。
同側接合亦已由完整 m-star 收緊至共同六點負擔，未排六點來源。

紙證先沿 d、x 的原外側 link 各取首次離開完整 N13 的點，得到兩個不同
K2 私有點 p_d、p_x。即使 d=U，前一 N 點私有，完整原面仍迫出口在 F。
完整 M2 的任意點 v，其全部原鄰點均私有；原 Γ 鄰點至多 T 加 r／s 之一。
於是圈外私有點集 X 滿足

`|X| ≥ |M2|+2+d_G(v)−bΓ(v)`。

再與 T 的完整原星接合，令 D=d_G(T)，得到

| 同一原圖中的條件 | 圈外私有點下界 |
| --- | --- |
| v∈M2 且 Tv 為原邊 | D+d_G(v)−4 ≥ D+1 |
| v∈M2 且 Tv 為原非邊 | D+d_G(v)−2 ≥ D+3 |
| T 五度，完整 M2 非單點 | 8 |
| T≥6，M2 非空 | D+1 ≥7 |
| M2 空，T≥8（必為偶度） | D−1 ≥7 |
| M2 空，T 六度 | L／R≥5，O≥6 |

相鄰／不相鄰兩星的重複分別由原 C3 的兩個實際面、原非邊最多兩共鄰
控制。這些是任意大小外側的紙面必要界，不是有限來源搜尋。

若 M2 非空且 |X|=6，必有 **M2={m}、m 五度、m 恰鄰 T 及 r／s 之一、
T 亦五度**。T 五度時連 |X|≤7 都迫完整 M2={m}。若框分離義務有觸發，
這個 m 必在所需側；E rootless 時不擅加 E 到框的分離義務。

[PROOF](PROOF.md)給完整紙證；[checker](check.py)獨立重建11型的外側
出口義務、104份前輪四面／T-star限制及12個首次離開 N 的符號轉移類。
104份逐列限制有88份不同投影；前輪完整證書逐字保留，未把投影去重
當成完整關係壓縮。有限核對不生成未知星點、任意外側 disk 或完整來源。

```sh
python3 -B audits/2026-10-23-941-gamma8-rootless-stars-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-rootless-stars-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-rootless-stars-6b09cd4/check.py --negative
```

[producer](produce.py)以 exclusive-create 產生正式[certificate-v2](certificate-v2.json)。
早先六／七點的較弱校準[certificate](certificate.json)保留原樣；新 v2 記完整
兩星公式及八點界，checker 預設 v2。凍結與原鏈保管見[INPUTS](INPUTS.json)，
實際重播、反控制及前輪重播見[VERIFICATION](VERIFICATION.json)，證明及
傳播審查見[REVIEW](REVIEW.md)，正式文件檢查見[DOC_CHECKS](DOC_CHECKS.json)。

正常／seed17一致，29項語義及2項外部反控制全部拒絕；前輪正常／seed17／
反控制通過，11份直接凍結輸入與442份前輪檔案零漂移。原完整 fibres、空列
及 full lifts 保留，本輪未重算全部原 caps。有限校準為 `triggered and holds`，
完整來源仍 `not triggered`；未新增 LP、Lean 或來源枚舉。全樹 DocGraph 未重跑。

下一窄義務優先取 **T 五度、M2={m}、|X|=6 的完整原外側接合**；另一窄支
為 **L／R、T 六度、M={T}**，保留框例外及 E rootless。11整型、更多內點、
較長 Γ、一般 wrong-side、八配對、941／W7／J1／J2 與較小 bad 仍 OPEN，
共同 k≥23 不變。本輪未 commit／push；當前入口見[Kempe導覽](../../docs/c5_kempe_guide.md)。
