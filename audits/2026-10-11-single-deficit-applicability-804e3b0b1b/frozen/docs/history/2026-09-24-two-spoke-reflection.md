# 2026-09-24：q-preserving 反射與下一相鄰 orbit

本輪接手時工作樹乾淨。成果見 [專題報告](../c5_two_spoke_reflection.md)，
優先序見 [HANDOFF](../HANDOFF.md)。研究階段未 commit／push；後續依使用者
要求將 Lean、checker、artifact、證明與 README／HANDOFF／STATUS 整包提交發布。
提交識別與遠端同步以 Git 為準。

## 結果與界線

- ρ(i)=3−i mod 5 與 π=(0 1) 同時作用，固定 q=01012；搬運同一來源的
  實際 attachments、完整 ordered contact relations、禁色與每個 z query。
  C₂/C₁ 的具名接點不交換、不拆成 marginals。
- S={b2,b3} 的兩種禁色次序由既有 S={b0,b1} 排除搬運；不重證舊 K5 cases。
  原 18 個 (2,1) 表項累計六項排除，剩四相鄰、八非相鄰；原必要表不覆寫。
- S={b3,b4} 中禁 0 的 A 必恰接 {b1,b2,b3}，禁 3 的 D 必恰接 {b0,b1,b4}；
  S={b4,b0} 是其反射。任意大小 support 證明用 crosscut 與既有 two-hub
  palette/tether extraction。此紙面結論未 Lean 化。
- 既有 R10 source indices 12–15、32–35 共八個 disk witnesses 皆為 C₂=A、
  C₁=D，只缺 q。這個 orbit 不能整體排除；一般 order I 的單缺失分離、
  order II 的實現／排除與完整列關係仍開放。

## 證據與驗證

新增 [Lean 模組](../../Math/TwoSpokeReflection.lean)、
[axiom audit](../../Math/TwoSpokeReflectionAudit.lean)、
[checker](../../scripts/c5_two_spoke_reflection.py) 及
[artifact](../../artifacts/c5_two_spoke_reflection/observations.json)。

有限控制：兩個 q-stabilizer elements、18 項 involutive table transport、
八組 support screening，八個既有 disk rotations 及其 reflection，
1,920 列完整圖 relation／接合與 3,840 列反射分量 relation，以及
120 份 q 刪邊 coloring 和相應反射 coloring。新 checker 僅讀取已存在來源，
不做 graph enumeration、planarity search 或新的 fixed-point 計算。

本輪實際通過：

```bash
python3 scripts/c5_two_spoke_reflection.py --check
python3 scripts/c5_two_spoke_adjacent_21.py --check
python3 scripts/c5_two_spoke_middle_21.py --check
python3 scripts/c5_degree5_two_spoke_sectors.py --check
lake build
lake env lean Math/TwoSpokeReflectionAudit.lean
python3 scripts/check_docs.py
git diff --check
```

`lake build` 成功（8824 jobs）；既有模組的 linter warnings 保留。
新 transport 證明不用 `sorry`、自訂 axioms 或 `native_decide`；audit 只有
普通 Lean 的 `propext`、`Classical.choice`、`Quot.sound`。
這不代表 disk reflection、support 分離或 K5 紙面證明已在 Lean 形式化。

未重跑完整 R10 checker、3703、雙拒絕 atlas、(3) 大覆蓋或 R 系列枚舉。
603 profiles、原 necessary-position artifact 與固定點皆未改寫。
下一個窄問題是 split-support pair 在同圖、同色框下的兩種接點次序與
全 boundary-row 行為；不重開已完成的三組相鄰排除。
