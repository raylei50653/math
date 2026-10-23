# 第四輪 rootless／K 資源獨立審查

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
只寫本目錄，保同一原 G／F、rotation、字面框、完整分量、附件、全部空
fibres 與 full lifts。完整論證及框例外見 [REVIEW](REVIEW.md)。

- 核准 `N_G(R)⊆R∪K`：G版本明用 R 私有點的完整原星在 F；U 保留，
  q、其他框分量及 ψ-rootless E 不增例外。
- 核准任意完整 M2 非單點的 **|Z|≥|M2|+7、|X|≥10**，不限 T 五度。
  更強同式可取整個 R 的原2總數 Q；非空 M2、|Z|≤8 時 R 的唯一原02
  分量是 M，且其中只有一個原2點。
- 獨立核非空 |Z|=7：完整 M={T,m}、T/m 同五度，唯一 ω 只可能
  N1／N3／K0／K2；N1/K2 另迫 Uu、m∈C、d≠U，N1 的完整原星只有
  `(d,p_d,U,p_x,w)`、w=n 或 v 兩份。N3/K0 保 C／E，不能沿用舊60列。
- 獨立核空 M2／T6、|Z|=6：ω 的新 rootless 分量、N1 及 N3 全支排除；
  N3 的五列完整星覆蓋有紙面推導。剩餘 ω 只能 K0／K2。

上述都是具名條件來源的原星／資源結論。有限控制與來源權限分開；沒有
新增來源實現或填片候選。兩支 ω 的剩餘原星及同一外側接合仍 OPEN，
11整型、一般wrong-side與父題仍OPEN，共同k≥23、W7排38／40不變。

[獨立 checker](check.py)核21份兩星接點集合算術、四份N1容量取等與
d=U例外。十份原 authority SHA 見 [INPUTS](INPUTS.json)；三子線最終
proof/checker/certificate 共九份另逐byte凍結於 [REVIEWED-INPUTS](REVIEWED-INPUTS.json)。
正常、seed17及兩項反控制一致；主線兩星及空／非空兩子線各一次獨立
正常重播均通過，原 authority 及九份新產物零漂移，見 [VERIFICATION](VERIFICATION.json)。
來源完整星、所有權、同一原實際面及列表覆蓋的紙面交叉審查無發現問題。
未commit／push。
