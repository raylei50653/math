# 2026-10-03：ε=2、t=1 全部分拆整型排除

接手基準 `bbd900a`。使用者要求「把 t=1 剩餘分支都排除」。先讀
HANDOFF／STATUS／Kempe 導覽及 Git 狀態，確認這是 933／941 固定
完整 Σ、edge-minimal disk 來源，ε=2、唯一 degree-6 root 的主線。
接手時已有多輪未提交成果，均保留；本輪沒有 commit／push。

## 成果與證據邊界

[t=1 合成報告](../c5_excess_two_single_spoke_complete.md)列出全部七個
原接點分拆，均作整型來源排除。核心共同工具是
[短支援兩／三 hubs](../c5_short_support_singleton.md)：原 degree-4
分量不能只有單條框邊支援，否則原外部路徑與 Gallai leaf block
給 K₅。每份原分量因而至少耗兩段，三份以上原分量均不可能。

單分量 (5) 由共同五葉 active tree 的兩形狀排除。
(3,2) 由 ternary 的跨列 D 守恆及原 binary 路徑塊共同支援排除。
(4,1) 則保留原四接點共同 active forest，兩 triangle 情形（含共用
cut vertex）構造原 K₅；兩條 bridge 路徑保留兩份固定末端區塊的
完整 rooted residual，聯立同一色框、原支援及 spoke 切口後全排。

最後 (4,1) 的支援族核對抓到 tuple／frozenset 交集會假空的表示問題；
正式 checker 已統一型別，並用全部 24 色置換獨立重建每份支援族。
每份完整 C 包絡都仍留在支援族，實際排除是兩份原末端區塊無法有
相容的支援區間；另保存能容納兩份區塊的正控制。修正後 100 查詢
仍全空，不沿用錯誤 scratch 的假空計數。

另外保存三份獨立小域／結構證書：五 unary 的四容量子覆蓋、
binary 加三 unary 的 2,200 同源 profiles、ternary 加兩 unary 的
146,496 同源 profiles。四接點短 pair 亦有獨立 leaf-block 證明。
這些結果不依賴把「無全 degree-4 子核心」誤升為整型排除。

所有結論為任意大小紙面推導＋Python 固定域控制，外部 degree-list
與既有分類仍是明列依賴。未新增 Lean theorem；未重跑全部歷史
Gallai／degree-4 topology、全來源圖 catalogue 或一般出口證據。
共同引理另直接排除 t=2、(2,1,1) 的三分量來源；未作新枚舉。
共同下界維持 ε≥2；其他 t 的完整分類、雙 degree-5 roots 與 K∞=K≤5 仍保留。

## 固定域結果

| 新證書 | 本輪核對 |
| --- | --- |
| 通用短支援 | 135 個兩-hub K₅；1,201 份三-hub 接線中 28 份拒絕皆 K₅；3,000 份原 C₅ skeletons |
| 四接點短 pair 獨立證明 | 96 palettes、240 原 minor、12 份完整四接點 relations |
| (5) | 26 active-tree 控制、4,800 原 minor 控制 |
| (4,1) | 100 查詢、216 完整 profiles、8 份非空支援族皆無相容兩區間；1,280 原 minor、134,400 完整六接點控制 |
| (3,2) | 100 查詢全排、90 次共同兩框弧 K₅；241,920 完整 relation 接合 |
| (3,1,1) 獨立 profiles | 168 具名配置、146,496 同源 profiles 全排 |
| (2,1,1,1) 獨立 profiles | 2,200 同源 profiles、50 固定弧比較全排 |
| 五 unary 獨立子覆蓋 | 3,000 覆色配置、8,400 全部四因子子覆蓋 |

這些數字是有限必要域、接合或 minor controls，不是來源圖數或
可實現 graph classes。所有非空原 relations 保留有序 tuples；
任意大小及 topology 仍由各紙面論證涵蓋。

## 本輪重播

新增 checker 各跑一般及 `PYTHONHASHSEED=17` 的 `--check`：

```bash
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_short_support_four_contact.py --check
python3 scripts/c5_excess_two_five_contact.py --check
python3 scripts/c5_excess_two_four_one.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
python3 scripts/c5_excess_two_ternary_two_unary.py --check
python3 scripts/c5_excess_two_binary_three_unary.py --check
python3 scripts/c5_excess_two_five_unary.py --check
```

沿用的有限運算另重播 `c5_single_spoke_four.py`、
`c5_single_spoke_three_one.py`、`c5_single_spoke_frame_arc.py`、
`c5_single_spoke_cross_row.py`、`c5_single_spoke_two_arc.py` 的 `--check`。
這些是相關依賴的局部重播，並未重驗其全部歷史拓撲。

```bash
lake build
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 完成 8,831 jobs，僅有既有 linter warnings。產物檢查
`ok=114`；新增短支援大檔已依既有 MANIFEST／producer 政策登錄。
文件檢查通過 454 份 Markdown、4,664 個本地連結及 anchors／index／
handoff；DocGraph 通過 62 documents、213 relations、5 families，
零 errors／notes；`git diff --check` 通過。
HANDOFF 的研究線及進行中標記沒有變化，依文件治理維持薄索引；
本輪現況、完整表及下一入口在 Kempe 導覽、STATUS 與合成報告。

## 跨對話接手摘要

> 已完成 933／941 固定完整 Σ edge-minimal C₅ disk 來源、ε=2、
> 唯一 degree-6 root 的全部 t=1 七分拆整型排除。先讀
> `docs/c5_excess_two_single_spoke_complete.md`、
> `docs/c5_short_support_singleton.md`、`docs/c5_excess_two_four_one.md`
> 與 `docs/c5_excess_two_ternary_binary.md`。保留同一原分量、有序
> contacts、完整 relations、實際 support、共同色框及原 spoke
> 切口；不要把四接點 pair 當成 binary。全部新證據是紙面＋Python，
> 未 Lean 化，共同 ε≥2 不變。下一窄題由 Kempe 導覽維護。
> 工作樹含接手前與本輪未提交研究；未作 commit／push。
