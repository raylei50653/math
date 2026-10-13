# 2026-09-28：no-spoke 原外部路徑 K5 與 record 599 來源排除

接手 HEAD `2de13f78602b2267376c5eb08ee2957603d549b5` 的既有未提交工作樹；
保留此前 residual-locality、three-one、four、no-spoke-exterior、
no-spoke-supports 的產物與文件修改。本輪沒有 commit／push。
最新優先序見 [HANDOFF](../HANDOFF.md)。

## 結果

[新報告](../c5_no_spoke_path_minor.md) 接續 record 599／p₂，得到更強結論：
q 下 C₁ 的 pair {0,2} 與實際支援 04 迫使所有原路徑塊都碰 b0、b4。
C₀ 到 b1 的原路徑將 z 接到補框弧，構成來源 K5；因此 record 599
直接排除，不另計 p₂ 延拓。任意大小、原五接點與完整分量身份均保留。

616 筆必要配置中，500 筆有 q 下來源 K5；264 筆原條件式 A/A 亦移出，
全部 96 個條件式 reject 查詢都屬被排除來源。保留 116 筆中原有 4 筆
A/A；再新增 104 個指定列延拓（88 個不需跨列置換，16 個需要），現為
108 筆 A/A、2 筆 A/?、2 筆 ?/A、4 筆 ?/?，共 12 個未決查詢。
148 組完整拒絕候選排除 136 組，剩 12 組；未證保留型可實現性或完整 Σ。

checker 另存新層，不改前序 artifacts；逐筆保留來源 ID、具名分量、
接點順序、環狀 lifts、全部 F 候選與舊 target 證據。核對反射的字面
target／支援／禁色／框弧及交換二接點分量後狀態一致。

新控制有 1,368 份零 spoke、五接點／三分量 minor skeletons 與其反射，
12 個負控制；重播 48 個 residual、576 個單列支援、2,304 個跨列支援、
1,944 個 residual 換色代數控制。拓撲 skeletons 不是 degree/list 來源圖。
紙面 bridge／palette 歸納和原圖 branch sets 承擔任意大小結論。
本輪核對 Dvořák degree-list 講義 Lemma 7／Theorem 10；未新增 Lean theorem。

## 驗證範圍

下列六支 checker 全部通過；新 JSON 與保留表逐 byte 重算一致。

```bash
python3 scripts/c5_no_spoke_path_minor.py --check
python3 scripts/c5_no_spoke_supports.py --check
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

`lake build` 成功（8,827 jobs），只有既存 SymRelabel／AttachmentOrder
linter warnings；這不形式化本輪任意大小拓撲與外部定理。
文件檢查通過 216 份 Markdown／2,540 個本地連結；DocGraph 通過 32 份
metadata 文件／79 條關係／5 families。HANDOFF 維持 150 行；
`git diff --check` 及本輪新增五檔的逐行 whitespace 檢查均通過。

未重跑 single-spoke (2,2) 全部中間鏈、two-spoke 全表、雙拒絕 atlas、
R 系列大覆蓋、一般 profiles／閉包、完整來源圖枚舉或 Lean axiom audit。
新 checker 的 input SHA256 與前序輸入雜湊均核對；文件檢查不驗證數學。

## 停止點

record 84／p₁，支援 (014,123,34)、q 禁色 ({0},{2,3},{1})，p₂ 可取 z=2。
p₁ 的七組完整拒絕候選剩 ({0,1},{3},{2})；C₀ 的 target 原路徑塊支援
只能為 01、04、014。q 在 C₀ 為 singleton，不能套雙列 pair 引理。
下一步比較同一 C₀ 的 source palette 與 target bridge，保留五接點、
C₁／C₂ 的實際外部路徑；本輪沒有證該候選可實現或 p₁ 不可延拓。
