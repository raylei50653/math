# 十五內點完整關係界

2026-10-13 整理補註：[無四色定理前提交接](tasks/c5_no4ct_handoff.md)另接
零內點 cap 下降、受限 `s<k` C4 代表與直接球面覆蓋，得到同一 `K≤15=K≤5`。
[替代度數與球面依賴](../audits/2026-10-13-c5-no4ct-degrees-6cafdfb/REPORT.md)
保留 932／933／941 三支、外部 Corollary 20 及 plantri 信任；不提高有界大小。
下文保留原 K15 證明鏈；無界三支、K∞ 及新論證 Lean 化仍 OPEN。

2026-10-13。固定 BASE `6cafdfb`；本頁是 K15-SPHERE 的權威入口。
完整前提、紙面覆蓋、全部原圖／fibres及獨立審閱見
[隔離報告](../audits/2026-10-13-k15-sphere-6cafdfb/REPORT.md)。
目前停止點由 [Kempe 導覽](c5_kempe_guide.md#3-停止點與保留缺口)維護。

對有限簡單 disk 圖、固定有序原 C5 外框與完整十列關係，

\[
\boxed{K_{\le15}=K_{\le5}=K132.}
\]

反設至多十五內點的目錄外來源存在，先全域最小化內點数、再最大化邊數。
[K14](c5_k14_sphere.md)及既有正規形／度數界使其恰十五內點、原框度數至少四、
內部至少五、內面三角化。外加只接原框的 cone 點，得到二十一點最小度五
球面三角剖分；列出全部這類球面圖並刪每個五度 root，覆蓋所有來源。

plantri 的 min5 及 min4加輸出端過濾兩路各得192份嵌入類，完整集合一致。
全部2,714份根圖、27,140列、624,617份完整染色由固定次序搜尋與獨立
domain propagation逐字比對，**完整Σ全部1023**，完成此有界排除。
原邊、rotation、指定外面、十個D5框及完整lifts均保存，生成沒有外圈剪枝。

```bash
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/compare.py
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/negative.py
```

兩路完整生成、normal／seed17、負控制及完整命令見隔離報告。
此為紙面完備化約＋有限完整證書，保留plantri生成定理／實作及上游外部
依賴；沒有新增Lean theorem。真正933／941來源未觸發，排除依據是完備
覆蓋與完整Σ驗證。一般來源至少十六內點；`K≤16=K≤5`、933／941任意大小
排除及`K∞=K≤5`仍 **OPEN**。
