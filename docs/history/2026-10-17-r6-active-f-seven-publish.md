# 主動 f 非面七圈：度數排除與 R100 條件下降整理發布

2026-10-17；研究與提交父 BASE `ffea555fc2a896d8166ce198ca28ed9262912f25`。
使用者授權「整理目前進展 commit + push」。本次交付研究audit、Kempe導覽、
STATUS及本發布驗證紀錄。研究封存中的「未commit／未push」保留研究交付當時
語境；提交狀態以Git為準。

## 已採納範圍與停止點

保留同一原全域最少內點、次級最多邊的no4ct C5來源G，原有序外框
`(x,y,a,b,c)`、原x,y,b四度、r六度、原支持S∈{932,933,941}，原rotation、
私人頂點、完整U319 fibres（包括空fibres）、全部五點接回及原r lifts。
`J=U/(s=t)`、`m=[s=t]`、`D=J*`及字面`e=(vw)*,f=(pq)*,g=(mz)*`不變。
沒有增加原v五度假設。

權威入口為[整合報告](../../audits/2026-10-17-r6-active-f-seven-ffea555/REPORT.md)
與[完整紙證](../../audits/2026-10-17-r6-active-f-seven-ffea555/PROOF.md)。
任取M101，額外假設D−M有含f的非面七圈C，X=V(C)；不要求奇數最小性。

| 項目 | 已證結果 | 邊界 |
| --- | --- | --- |
| 四度端點整個子類 | a0=4或c0=4時，此種七圈不可能存在；兩個真實三角面強制匹配邊，與cap邊界矛盾 | 任意大小紙證，不需111參考、三-spoke或新cyclic六割 |
| 六度端點指定中心位置 | 中心p,n_a迫a0≥7；中心q,n_c迫c0≥7 | n_a/n_c是原a/c扇區緊鄰p/q的點；不把另一私人中心位置升為七度 |
| 五割與標記定位 | V(Q5)∩{m,z,v,w}={z}；e,g端點均在X外且dist_D(X,V(e)∪V(g))≥2 | 同一原圖非邊可共同使用；不拼接兩份染色，局部距離不保證交換區域分離 |
| R100條件下降 | 實際完整全異染色若給W_C(R100)≠W_g(R100)，整區交換得N101，完整奇圈數至少下降二 | 全部外側補圈保留；分離參考存在性仍OPEN，一／三-spoke皆保留 |
| 真正改動參考的交換 | 安全αβ／αγ整圈K交換後，E(L_R′)=E(L_R)△(M∩E(K)) | 只增加L邊不能縮小g區域；尚未構造必然改善步，β/γ交換固定R100 |

**剩餘主動f七圈、其他奇圈、H相連修復、W110+W101>0、omega_e=0及完整319仍OPEN。**
固定111參考下Q=H的阻斷保留；R001／R010對這種完整區域策略有既定標記阻斷。
四個剩餘中心位置的度數表只列必要條件，不宣稱來源實現。
下一輪窄義務為在實際完整全異染色中最小化|W_g|，找到真正改動R100並使
七-cap與g分離的完整交換。接續見[Kempe導覽](../archive/guides/c5_kempe_guide.md#3-停止點與保留缺口)。
一般K≤22、固定r6的k≥25與原completed-source接回成本k+5不變。

## 封存與發布驗證

[發布盤點](2026-10-17-r6-active-f-seven-publication/initial-state.json)保存77份研究audit的
精確bytes／SHA256，包含原OUTPUTS.sha256、17份凍結輸入、完整紙證、三路互審、
A完整128個局部匹配賦值與污染／覆寫拒絕收據。原76項seal與全部77份檔案保持原始bytes。
另以`.md.snapshot`保存研究交付時STATUS與Kempe導覽，STATUS只增加本發布紀錄索引。
新檔案皆小於1 MB，不新增產物政策例外。

[有效發布檢查收據](2026-10-17-r6-active-f-seven-publication/checks-v2.json)記錄實際命令、exit code與log hash。
研究時的正常／seed17、污染及exclusive-create拒絕與三路互審見
[原驗證紀錄](../../audits/2026-10-17-r6-active-f-seven-ffea555/VERIFICATION.md)。
出版前另作獨立只讀封存／局部證書核對；新紙證與有限局部校準分開，真正最小來源
供應仍為not triggered。沒有新增Lean theorem，`lake build`只驗既有Lean庫。

只讀重播：

```sh
python3 -B docs/history/2026-10-17-r6-active-f-seven-publication/check_custody.py
python3 -B audits/2026-10-17-r6-active-f-seven-ffea555/check.py
python3 -B audits/2026-10-17-r6-active-f-seven-ffea555/A/check.py --certificate audits/2026-10-17-r6-active-f-seven-ffea555/A/certificate.json
python3 -B scripts/check_docs.py
python3 -B tools/check_generated_artifacts.py
```

本次重播與產物政策檢查以實際收據為準。formal／scoped DocGraph分開記錄，
不宣稱全樹歷史文件零錯誤；不重跑舊大型來源枚舉、九框計數或前輪大型固定圖控制。
所有研究封存bytes保持不變，發布checker只驗custody，不驗數學拓撲。

首輪工具測試因系統Python缺少networkx而未能匯入一個模組，保留在
[首輪收據](2026-10-17-r6-active-f-seven-publication/checks.json)。使用專案固定的
`uv run --with-requirements requirements.txt`環境重跑後，94項工具測試全部通過。
root／A正常及seed17重播、兩個污染拒絕、76項seal、17份BASE輸入、formal／scoped
DocGraph與既有Lean庫8832 jobs均符合預期；新紙證未因此升為形式化。
明確stage後，Git index產物政策及`git diff --cached --check`皆通過；
最終正式文件檢查為695份Markdown、9143條本地連結，research custody零變動。

Updated：本發布紀錄與STATUS歷史索引；研究時導覽與索引一併交付。
Reviewed-unchanged：README／HANDOFF的研究線與tag、原封存證據與一般界。
Propagation stop：父題仍OPEN；沒有提升closure或改寫跨線摘要。
