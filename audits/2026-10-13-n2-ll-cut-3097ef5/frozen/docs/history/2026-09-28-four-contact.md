# 2026-09-28：single-spoke (4) 排除與全部 t=1 接合

接手 HEAD `2de13f78602b2267376c5eb08ee2957603d549b5`。工作樹已有未提交
的 residual-locality、three-one checker／artifacts／報告／歷史及相關文件
修改，本輪全部保留；沒有 commit／push 或讀取遠端 SHA。優先序見
[HANDOFF](../HANDOFF.md)。

## 結果與推理界線

[新報告](../c5_single_spoke_four.md) 完成 single-spoke (4) 任意大小排除。
先在同一原 C 的三份拒絕 lists 上，由 block incidence matrix 欄獨立性
證三組差異共用 τ。τ=+1 的 palette 必為 A\{d}，故正 block 不能是
bridge；四葉共同樹遂只剩兩個正 triangle 與一條負 bridge，沒有外臂，
也沒有共用 triangle cut vertex。

四個原接點各自保留：兩個在左 triangle、兩個在右 triangle。右 triangle
與 z 合成 Z，左 triangle 各點的唯一其餘邊通向實際 boundary tether；
以 slack-list 延拓排除沒有 boundary 附件的旁支。左 triangle 三點、Z、
B 加 tethers 五組給 K5。此 minor 只作非平面性反證，不保持完整 Σ。

結論不需 T4、第二列拒絕或來源大小界。t=1 的 (3,1)、(4) 無來源，
(2,1,1)、(2,2) 接受出口所需指定 p，故 [條件式出口](../c5_single_sided_exit.md)
第五類已刪去分拆限制。失敗側唯一 degree-5 現只剩 t=0 六型。
既有 (2,2) 的 278 筆來源排除、102 筆／51 型雙列及 (2,1,1) 的 114 筆
雙列結果不變；未重寫前序 artifacts。

外部 degree-list 講義 Lemma 7／Theorem 10 已重讀核對。任意大小的
共同係數、共同樹、旁支 tether 與 branch sets 都由紙面證明承擔；
Python 是有限控制，未新增 Lean theorem。

## 新證書

- 1,120 組 palette triples 全測，52 組相容 block 型、188 個局部
  incidence 型、104 個 tight attachment 型，保留共同色框與反射。
- 1,280 個連通四葉及 49 個雙路徑控制；只有兩 triangle／單 bridge／
  零臂通過三列限制。有限長度控制不取代任意大小的葉數及符號證明。
- 四份完整四接點關係各有 24 tuples，F=A，逐色／逐座標解除 witnesses
  均保存；只是同一抽象 residual 圖的關係，不宣稱 disk 可實現。
- 960 份具名 K5 skeletons、960 份反射核對，含全部 24 種接點角色排列、
  五個 spoke 位置、不同 tether 長度與共用 boundary 終點。
- 八個負控制，包含缺 central bridge、Z 不連通及兩列正 bridge 無法
  延伸第三列；不把指定 witness 失效誤述為整張修改圖必平面。

輸入 SHA256 綁定前序 three-one／cores 的 checker 與 artifact。

## 驗證範圍

本輪重播：

```bash
python3 scripts/c5_single_spoke_four.py --check
python3 scripts/c5_single_spoke_three_one.py --check
python3 scripts/c5_single_spoke_cores.py --check
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_single_contact_bounds.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 JSON 逐 byte 重算一致；three-one／cores 重播通過，後者保留原必要
支援表的歷史 unresolved 數字，不是當前 target 狀態。接合重播確認
residual-locality 剩 102 筆全部 accept/accept、0 查詢；single-contact
bounds 給 (2,1,1) 的 114 筆雙列全部完成。

全部檢查通過。`lake build` 成功（8,827 jobs），只有既有 AttachmentOrder／
SymRelabel linter warnings。文件檢查通過 209 份 Markdown、2,467 個本地
連結；DocGraph 通過 29 份 metadata 文件、68 條關係、4 families。
`git diff --check` 通過；HANDOFF 保持 150 行。

未重跑整條 (2,2)／(2,1,1) 中間 checker 鏈、two-spoke 全表、雙拒絕
atlas、R 系列大覆蓋、一般 profiles／閉包或 Lean axiom audit。
文件檢查不驗證數學，build 不將本輪新紙面圖層定理形式化。

## 下一個窄問題

t=0 的外部連通與 K4 block：保留五個原接點、六種必要分拆、全部實際
boundary 支援及完整禁色覆蓋，先核對另一原分量何時提供避開指定 block
的 z–B 路徑，使 K4 的四條 tethers 可接成同一外部 hub。單分量 (5)
另保留，不能沿用原 spoke。未新增 t=0 排除；高 degree、多 degree-5、
一般核心存在／分離、共同出口與 `K∞=K≤5` 仍未證。
