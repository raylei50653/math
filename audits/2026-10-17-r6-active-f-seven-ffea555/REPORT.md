# 主動 f 非面七圈：度數子類採納與換參考義務

2026-10-17；凍結 BASE `ffea555fc2a896d8166ce198ca28ed9262912f25`。
同一原來源、同一 J,D、原支持及全部 fibres/lifts 保留；不增加原 v=5。
權威論證為[整合紙證](PROOF.md)，輸入身份為 [INPUTS](INPUTS.json)。

本輪任取 M101，額外假設 D−M 有含 f 的非面七圈；不要求奇數最小性、
111 參考或三-spoke。新採納範圍如下。

| 結果 | 精確範圍／證據 |
| --- | --- |
| a0=4 或 c0=4 的整個指定子類排除 | 真實面強制匹配邊，與 p/q 七-cap 邊界矛盾；[A](A/PROOF.md) |
| 指定中心下 a0=6／c0=6 排除 | p,n_a 中心迫 a0≥7；q,n_c 中心迫 c0≥7；真實面上的 spoke 與 g 相撞 |
| 五割及標記定位 | Q5 在 {m,z,v,w} 中恰只經過 z；e,g 端點全在 X 外，距 X 至少二；[B](B/PROOF.md) |
| R100 的充分條件 | 若存在真實完整全異參考使 W_C≠W_g，整區交換得 N101，完整奇圈數至少下降二；[C](C/PROOF.md) |

四個殘餘中心位置及必要原度數見 [紙證 §3](PROOF.md#3-六度端點的指定中心位置排除)。
這些必要範圍不表示來源實現。R100 的分離存在性仍 OPEN；固定111參考下的
Q=H 阻斷仍有效。局部距離不替代完整區域分離。一／三-spoke 都保留，不能
任意指定三-spoke 的色類為 R100。只換 R100 偶補的 β/γ 不會改善區域。

下一輪窄義務是：在全部實際完整全異染色上最小化 |W_g|，使用真正改變
R100 的安全整圈交換，證出七-cap 區域與 g 分離。完整動作及 L_R 更新式
見 [C 的接續分析](C/PROOF.md)；本輪沒有證出嚴格縮小步。

證據層：任意大小紙面推論與三路獨立審核；A的128個完整局部匹配賦值僅作校準。
真正最小來源供應 **not triggered**，無新外部定理、無新 Lean theorem。
驗證範圍與收據見 [VERIFICATION](VERIFICATION.md)。

```sh
python3 -B audits/2026-10-17-r6-active-f-seven-ffea555/check.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-17-r6-active-f-seven-ffea555/check.py
python3 -B audits/2026-10-17-r6-active-f-seven-ffea555/A/check.py --certificate audits/2026-10-17-r6-active-f-seven-ffea555/A/certificate.json
python3 -B audits/2026-10-17-r6-seven-five-repair-5b9a7b3/check.py --check
python3 -B scripts/check_docs.py
lake build
```

Closure scope：僅上述四度端點整個子類與六度端點指定中心位置；父題仍 PARTIAL。
Updated：本輪 audit、Kempe 導覽現況／停止點、STATUS 對應索引。
Reviewed-unchanged：原 ffea555 發布與全部舊封存證據；README／HANDOFF 的研究線
路由及 tag；其他奇圈及父題 OPEN、一般界與 k+5 接回成本。
Remaining OPEN：剩餘主動 f 七圈、其他奇圈、H 相連修復、聯合正性、omega_e=0、
完整319、一般 T/T0 及主命題。未 commit、未 push。
Propagation stop：同步直接父題入口後停止；未提升父題 closure 或跨線摘要。
目前接續入口見 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)。
