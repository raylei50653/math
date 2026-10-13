# 十五內點完整來源排除

2026-10-13。BASE `6cafdfb`，完整 SHA 與凍結輸入見 [BASE](BASE.json)。
本輪證明

\[
\boxed{K_{\le15}=K_{\le5}=K132.}
\]

一般目錄外 disk-C5 來源至少十六內點。933／941 任意大小來源及
`K∞=K≤5` 仍 **OPEN**，沒有新增 Lean theorem。
目前停止點由 [Kempe 導覽](../../docs/c5_kempe_guide.md#3-停止點與保留缺口)維護。

## 1. 完備來源契約

反設至多十五內點的目錄外來源存在，在**全部目錄外來源**先最小化內點數、
再最大化邊數。既有 K14、共面正規形與度數界使其恰十五內點、原 C5
無 chord、內面三角化、原框 degree≥4、內點 degree≥5。外面加原框 cone
點，恰得二十一點最小度五球面三角剖分。

完整列出全部球面嵌入類，刪每一個五度 root，保留其原 rotation 中的五個
有序鄰點及十個整圖 D5 搬運，必覆蓋全部可能來源。没有 h、collar、C8、
mask 或私人圈秩剪枝；沒有套用 edge-critical、N2、ε=2 或 Gallai 前提。
完整論證及外部信任見 [PROOF](PROOF.md)，獨立審閱見
[REVIEW](../2026-10-13-source-followup-6cafdfb/REVIEW.md)。

## 2. 完整生成與關係結果

從 BASE 凍結的 plantri 5.8 C 原始碼編譯。`-m5 21` 直接得192份；第二路
`-m4 21` 的375,126,827份候選只在輸出端檢查 degree≥5，同樣得192份。
逐 dart、兩個整圖方向的完整嵌入編碼核對兩集合相等、各自無重複。
生成 recursion 不加入過濾。兩路共享部分 plantri 實作，不称完全獨立生成器。

| 項目 | 實際結果 |
|---|---:|
| 二十一點球面嵌入類 | 192 |
| 全部五度根點刪除圖 | 2,714 |
| literal 原框列 | 27,140 |
| 完整染色 lifts | 624,617 |
| 原框完整關係 | 全部 1023∈K132 |

h 根圖分布為 `0:56,1:211,2:563,3:947,4:717,5:188,6:27,7:3,8:2`。
這是具名根圖計數，可能含同構重複，沒有當作互異未標號 disk 數。

所有原點對照、原 edges、rotation、有向 faces、指定外面、degree、原 B、
全部十列 full lifts 和 D5 maps 都保存在 [certificate.json.gz](certificate.json.gz)。
主程式使用固定頂點次序完整搜尋；獨立程式從 sphere 原 labels 重新解析、
檢查拓撲，並用 domain propagation／MRV 搜尋所有 lifts，最後才作共同標號
搬運。兩套完整 lifts 逐字相等，沒有以數量相等取代集合相等。

完整 payload SHA256：
`24e3e89af3d800fcc84128ad90304d9797f21d967429b358f16b3c1e725c465d`。
實際最小933／941來源為 `not triggered`；排除理由是紙面完備覆蓋接完整
有限關係驗證，不能僅以零觸發推論排除。

## 3. 重播與驗證範圍

```bash
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k15-sphere-6cafdfb/check.py --check
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/compare.py
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/compare.py
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/negative.py
python3 -B audits/2026-10-13-k15-sphere-6cafdfb/independent/calibration.py
```

生成初次使用 [generate.py](generation/generate.py)，拒絕覆寫輸出；兩路命令、
耗時、輸出及 hashes 見 [receipt](generation/receipt.json)。既有輸出可用
`python3 -B audits/2026-10-13-k15-sphere-6cafdfb/generation/replay.py`
在臨時目錄重建並逐 byte 比較。本輪已實際執行兩路完整生成一次，不把
提供 replay 指令說成另行重跑過生成。

主程式及獨立程式的 normal／seed17 均 PASS。負控制拒絕漏 lift、偽空 fibre、
漏列、漏 root、錯原邊、錯 pin、錯 rotation，另以主程式拒絕漏 lift。
C5、W5、C5+chord02 三份小控制比對直接 product，含真正空 fibres。
實際記錄保存於 `logs/`。`lake build` 通過8831 jobs，只是既有Lean回歸。
新證明仍為紙面化約、外部生成定理及Python完整有限證書，沒有新Lean形式化。

## 4. 剩餘範圍及文件接入

一般十六內點以上、任意大小933／941、W5私人圈秩≥5的縮減及一般主命題
保持 OPEN。C8後續結論見 [獨立小cap／內圈報告](../2026-10-13-c8-followup-6cafdfb/REPORT.md)，
它不作為本次球面生成的剪枝或完備性前提。

Closure scope：只排除一般至多十五內點的目錄外關係；權威證據為本報告、
PROOF、完整球面／fibres及獨立審閱。文件接入與檢查見
[研究紀錄](../../docs/history/2026-10-13-c5-k15-c8-progress.md)。
未 commit／push，未修改既有數學證書。
