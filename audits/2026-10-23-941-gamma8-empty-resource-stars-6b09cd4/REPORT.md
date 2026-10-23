# 空 M2 第四輪：六資源點新增原點只餘 K0／K2

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
只接[第三輪停止點](../2026-10-23-941-types-wrong-side-round3-6b09cd4/REPORT.md)
的完整原星，保同一 G／F、rotation、原附件、B14 字面框、完整原分量、
空 fibres 與 full lifts；未改舊證書或共享文件，未 commit／push。

**空 M2、原 T 六度、|Z|=6 時，新增原點 ω 必屬同一原 K02，原色只餘0／2。**
其中 Z=X∩(V(R)∪V(K))，R 是原 J−K 中含 M 的完整 rootless 支；此結論
允 X\Z 有任意多其他點，不靠把全部外側點數限制成七。

[紙證](PROOF.md)排完整 R02 新分量、R13 新分量、N1、N3 四種身份。
N1 用同一 ω,y 的完整原星迫三個共鄰；N3 先由完整 a/b/y 星窮盡五種
必要接合，再用完整 ω-link 或原度數排除。11型×2個 U 身份的獨立
[checker](check.py)重建20份 partial 接合，完整 N3-star 全為空。沒有以
局部存留或數值／有限控制宣稱來源存在。

所以完整 R 仍恰 M={T} 與 N={r,τ,sΓ,a,y,b}，K 的原 Γ 外私有點恰
{p_d,p_x,ω}。在真正七外點等號 X=Z∪{χ} 下，[紙證第6節](PROOF.md)
列出 K0／K2 的完整必要鄰點包絡；χ2 不能補 K02 星，χ3 原 B13 附件仍保留。
包絡的 frame13 是同一字面原 B14 的完整實際1／3點集合，先按實際別名去重，
不表示每個列入的鄰點可實現。[scope](CERTIFICATE-SCOPE.json)明定這份 K 包絡
額外要求 |X|=7；未知完整 cyclic stars／同一 U collar 仍 OPEN。

[直接 authority](INPUTS.json)9份及第三輪173份最終檔案已凍結／驗 SHA：
171份 immutable live 文件與兩份正式文件的進入時快照均零漂移。原完整
fibres／full lifts 所在證書留存，沒有把本地星接口代換原完整關係。
正常、seed17、6項語義反控制及外部破壞反控制見[VERIFICATION](VERIFICATION.json)。

```sh
python3 -B audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-empty-resource-stars-6b09cd4/check.py --negative
```

下一窄義務：**K0／K2 各自的一份完整原 ω-star，接回同一 U 的 F 側有序
link、完整 B14 原 stars 及同一外側 disk**。尚未完成實際來源，控制仍
`not triggered`；有限接口核對為 `triggered and holds`。

D≥8 保前輪 |X|≥D；空 M2 至少7、非空 M2 至少8、共同至少7、k≥23 均不變。
11整型、空 M2 七外點、非空 M2 八外點、更多 Γ 內點、長 Γ、一般 wrong-side、
初始八配對、941／W7／J1／J2、一般較小 bad、Lean 與 matching 仍 OPEN。
