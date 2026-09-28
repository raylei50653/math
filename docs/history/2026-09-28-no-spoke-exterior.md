# 2026-09-28：no-spoke 外部連通與六型收窄為兩型

接手 HEAD `2de13f78602b2267376c5eb08ee2957603d549b5` 的既有未提交工作樹，保留 residual-locality、
three-one、four 的 checker／artifacts／報告／歷史及文件修改。
本輪沒有 commit／push；研究優先序見 [HANDOFF](../HANDOFF.md)。

## 結果與信任界線

[新報告](../c5_no_spoke_exterior.md) 完成 t=0 的任意大小必要化約：

1. 多分量的每份 F 非空且非全四色。沒有 boundary 支援的分量有完整
   S₄ 對稱，故不可能；另一原分量遂提供避開指定 C 的實際 z–B 路徑。
2. 這條路徑把 K4 的四條原 tethers 接到同一外部 hub，排除所有
   多分量來源的 K4 block，不借用不存在的 z-spoke。
3. 單分量 (5) 另以四份 palettes 的共同係數證：正 block 只能是 K4，
   負 block 只能是 bridge，active forest 接點數為 2h+2k，與五接點矛盾。
4. 在多分量的 K4-free 分量中，既有三／四接點 active triangle
   與原 tethers 證明仍適用；以外部路徑首邊取代 minor 的 spoke 鄰接，
   再排除 (4,1)、(3,2)、(3,1,1)。

所以 t=0 只剩 (2,2,1)、(2,1,1,1)，各分量 K4-free。
完整禁色覆蓋只剩 48、24 份具名必要配置；尚未證來源可實現性、
平面支援／次序分類或指定 p 分離。不需 T4 或第二列拒絕。
一般單側出口、共同出口、高 degree／多 degree-5 與 `K∞=K≤5` 未證。

外部 Dvořák degree-list 講義 Lemma 7／Theorem 10 本輪已重讀。
任意大小結論為紙面＋外部定理；Python 僅有限控制，未新增 Lean theorem。
既有 (2,2) 的 278 來源排除、102 筆／51 型雙列及 (2,1,1) 的 114 筆
雙列結果均未變，不修改前序 artifacts。

## 新證書

- 111 份原六型不可刪減禁色覆蓋，保留 72 份，逐份核對反射。
- 1,808 組四列 palettes、16 個相容型、52 個 local incidence 型，
  35 個葉數公式控制；任意大小公式另有紙面證明。
- 四接點／六接點 K4 樹的完整有序關係及五接點負控制；沒有將
  抽象正控制當平面來源，也核對 marginals 乘積會遺失所有禁色。
- 560 份 K5 branch-set 證書及 560 份反射，其中 K4 hub 160、
  三接點 160、四接點 240。三／四接點骨架由實際 edges 讀回五個
  原 contacts 的分量分拆，逐份確認零 spoke。
- 九個指定 minor witness 失效負控制；不推論受損整圖必平面。

## 驗證範圍

本輪重播全部通過：

```bash
python3 scripts/c5_no_spoke_exterior.py --check
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_cores.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 JSON 逐 byte 重算一致；four／three-one 既有證書一致。cores 的
原必要表保留歷史 unresolved 數字，不代表當前 t=1 target 狀態。
`lake build` 成功（8,827 jobs），只有既有 AttachmentOrder／SymRelabel
linter warnings。文件檢查通過 211 份 Markdown、2,495 個本地連結；
DocGraph 通過 30 份 metadata 文件、71 條關係、5 families。
HANDOFF 保持 150 行；whitespace 檢查通過。

未重跑 (2,2)／(2,1,1) 中間 checker 鏈、two-spoke 全表、雙拒絕 atlas、
R 系列大覆蓋、一般 profiles／閉包或 Lean axiom audit。
文件檢查不驗證數學；`lake build` 不形式化本輪新紙面定理。

## 下一個窄問題

固定 (2,2,1)、(2,1,1,1) 的 72 份必要禁色覆蓋，保留同一來源的五個
原接點、全部 boundary 支援及完整有序 relation，推導平面支援／次序
必要條件，再處理 p₁=01021、p₂=01212。無 spoke 的框架須重新核對，
不能直接把 single-spoke slit 表當作 t=0 的可實現性分類。
