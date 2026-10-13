# 2026-10-03：復用 t=1，完成 ε=2 t=2 全部分拆整型排除

**後續發布（2026-10-03）**：本輪成果納入
[整理與發布紀錄](2026-10-03-excess-two-two-spoke-publish.md)。下文保留
研究輪次當時的驗證及未提交語境；發布核對以後續紀錄及即時 Git 為準。

接手基準 `1d32997`，工作樹乾淨。使用者要求「盡可能 推進 t = 2，
並嘗試復用 t = 1」。先讀 HANDOFF、STATUS、Kempe 導覽及即時 Git，
確認前序 t=1 已全部排除，t=2 的整型 (2,2)、(3,1)、(4) 尚保留。
本輪沿用既有任意大小論證與小必要域，沒有重開來源圖 catalogue。
沒有 commit／push。

## 成果與適用前提

[t=2 合成報告](../c5_excess_two_two_spoke_complete.md)完成全部五分拆。
共同前提是固定完整 Σ 為 933／941 或整圖 D₅ 像、edge-minimal
induced-C₅ disk 來源、ε=2、唯一完整 degree-6 root，其餘有效內點
完整 degree 四。連同 t=1，現在同一前提下 **t∉{1,2}**。

三份以上原分量由前序短支援引理的固定支援跨度≥2 直接排除，
完成 (2,1,1)／四 unary。(3,1) 直接匯入 t=1 的 singleton profile
生成器；兩條原 spokes 的共同扇區限制，使必要域全空，不需要
新增 D 身份守恆 screen。(4) 則復用共同 D／τ active forest，
完整保留兩份固定原末端袋及其同一扇區支援次序。

(2,2) 的純 pair 路徑條件先留下 20 份抽象必要查詢。復用原
singleton 首橋引理後，固定色端點矛盾及兩首橋袋的共用 β 全部
排除；這次搬運的是每袋的局部 E={c,β}，不是整份分量 F={c}。
每個 singleton 列獨立選自己的 β，只在同一列同一原首橋兩端
共用。20 份較弱 screen 的完整十列 profiles、具名 sectors 及
ownership 均保存為控制，沒有把它們宣稱為 disk 實現。

原 contacts、完整有序 relations、字面色框、實際附件及包絡的
真實端點全程保留。不同原分量不獨立正規化；四接點 pair 沒有
冒充 binary。任意大小、原 tethers、block-tree 歸納及 crosscut
由紙面論證承擔，Python 核對有限必要域、原 minor skeletons
及完整 ordered-tuple 接合。共同下界仍 ε≥2，其他 t、雙 degree-5
roots、一般來源／出口及 K∞=K≤5 保留；未新增 Lean theorem。

## 固定域結果

| 原分拆／證書 | 本輪核對 |
| --- | --- |
| (2,2) | 40 具名扇區配置、400 目標查詢全空；純 pair 層的 20 個控制保存 |
| (2,2) 搜尋分類 | 618 節點、684 共同 profile 衝突、1,044 純 pair 兩框弧排除、211 首端固定色矛盾、335 全部逐列 β 組合排除 |
| (2,2) 完整關係 | 256 份 singleton tuple-pair fibers；65,535 非空原 binary relations 的精確避色投影；2,704 代表完整接合／spoke 色集控制 |
| (3,1) | 16 具名位置、107,296 完整十列 profiles 全無目標，不需 D 身份篩選 |
| (3,1) 完整關係 | 15,360 singleton 及 483,840 二元素 ternary relation 接合；兩個字面 spoke 座標均保留 |
| (4) | 200 查詢，100 份三禁色 K₅、100 份非空支援族的兩原末端袋不能並排 |
| (4) 原圖／關係 | 5,120 兩原 spoke K₅ 控制、80 份完整原邊代表；526,336 完整五接點接合 |

這些是必要域、搜尋操作及控制的數目，不是可實現來源圖的數目。
另作獨立讀碼／紙面審閱，核對 K 在 envelope 上計算是安全放寬、
首橋長度一／較長路徑的兩端公式、逐列獨立 β、同一原袋的 palette
唯一性、真實外部 anchors、共同 D／τ 及四接點袋的固定環序，
未發現阻斷問題。外部 Gallai 講義 Lemma 7／Theorem 10 本輪重讀，
確認無需整份 G 在每個被查 row 下 minimal。

## 本輪重播與沿用範圍

三份新增 checker 在最終 bytes 上各跑一般及 `PYTHONHASHSEED=17`
的 `--check`，全部通過：

```bash
python3 scripts/c5_excess_two_two_spoke_binary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_binary.py --check
python3 scripts/c5_excess_two_two_spoke_ternary.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_ternary.py --check
python3 scripts/c5_excess_two_two_spoke_four.py --check
PYTHONHASHSEED=17 python3 scripts/c5_excess_two_two_spoke_four.py --check
```

沿用的短支援與 t=1 運算／原首橋層另重播：

```bash
python3 scripts/c5_short_support_singleton.py --check
python3 scripts/c5_excess_two_four_one.py --check
python3 scripts/c5_excess_two_ternary_binary.py --check
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
python3 scripts/c5_excess_two_two_binary.py --check
python3 scripts/c5_excess_two_double_spoke.py --check
```

本輪沒有重播全部歷史 Gallai／degree-4 分類、其餘 t=1 整型表、
所有來源圖 catalogue、完整 weak-deletion／R-series／Kempe closure
或 Lean axiom audit。未重跑的前序任意大小依賴仍是明列的證據界線，
沒有將既有 Lean build 當成本輪 topology 的形式化。

`lake build` 通過 8,831 jobs，僅有既有 linter warnings。
兩份超过 1 MB 的新增 binary／four artifacts 依既有政策登錄：

```bash
uv run --with-requirements requirements.txt python tools/artifacts.py record \
  artifacts/c5_excess_two_two_spoke_binary/observations.json \
  artifacts/c5_excess_two_two_spoke_four/observations.json
uv run --with-requirements requirements.txt python tools/artifacts.py status
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

MANIFEST 保存 byte size、SHA256、producer 及依賴 fingerprint，新增
binary artifact 為 3,455,178 bytes，four 為 1,278,618 bytes；ternary
為 455,240 bytes，直接納入新檔。兩份大檔由 MANIFEST／producer
重建，保留本機產物並沿用生成的 `.gitignore` 政策。

HANDOFF 的研究線及進行中標記沒有變化，依文件治理維持薄索引；
本輪現況、五型覆蓋及下一入口在 Kempe 導覽、STATUS 與合成報告。
README 的研究入口同步更新；舊 t=1 總報告及 (2,2) 省略報告加
後續連結，保留正文當輪語境。最後產物驗證 `ok=116`；文件檢查
通過 460 份 Markdown、4,734 個本地連結及 anchors／index／handoff。
DocGraph 通過 62 documents、213 relations、5 families，零 errors／
notes；`git diff --check` 通過。兩份原省略前序 checker 亦重播通過，
沒有重新生成或改動其既有 artifacts。

## 跨對話接手摘要

> 已完成 933／941 固定完整 Σ、edge-minimal induced-C₅ disk 來源、
> ε=2、唯一 degree-6 root 的全部 t=2 五分拆整型排除，連同前序
> 得 t∉{1,2}。先讀 `docs/c5_excess_two_two_spoke_complete.md`、
> 本輪紀錄及三份 `c5_excess_two_two_spoke_{binary,ternary,four}.md`。
> 復用 t=1 的短支援、singleton profiles、共同 active forest 與
> 原首橋，保留原 ordered contacts、完整 relations、真實附件、
> 共同字面色框及 spokes 的原扇區；binary singleton 的局部 E
> 不等於整份 F，β 只在同一列同一首橋兩端共用。一般及 hashseed
> 重播通過，未新增 Lean theorem，共同 ε≥2 不變。下一窄題由
> Kempe 導覽維護，為 t=3、(2,1) 整型來源；不重開來源圖枚舉。
> 接手時乾淨，現在保留本輪未提交研究，沒有 commit／push。
