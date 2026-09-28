# 2026-09-28：局部 residual、record 90 與 (2,2) 完成

接手基準 `2de13f78602b2267376c5eb08ee2957603d549b5`，當時工作樹乾淨，
HEAD 與本地 origin/main 相同；本輪未讀取遠端 SHA，也未 commit／push。
目前優先序以 [HANDOFF](../HANDOFF.md) 為準。

## 本輪成果與證據界線

[新報告](../c5_single_spoke_residual_locality.md) 證同一原路徑塊上若 boundary
列相同，旁支 palette 唯一性與 root 實際附件給相同局部 residual E。
record 90 的 q／p₂ 只差 b2；首橋 β=0 兩端的 E 不同，故兩塊必接 b2，
配必接 b3 給原圖 K5。β=2 沿用 b3、b4；交換分量涵蓋 record 282。

重算兩個未決查詢的 36 組完整拒絕候選：34 組沿用，2 組新排除。
來源排除仍 278，保留 102 筆／51 型全部 A/A，0 個未決查詢。
新證書保存全部原記錄及前層證據，不改寫舊 artifact 或 `joint_supports` guard。

新有限控制：1,944 個歸納扣除／換色、250 個 root residual、32 個支援／β、
576 個具名 minor、13 個負控制，另核對交換及字面反射。
任意大小來自紙面 rooted-block 歸納與原圖 branch sets，外部 degree-list
定理原文已重讀；finite skeletons 不是 degree/list 來源或可實現性證書。
未新增 Lean theorem。

[出口接合](../c5_single_sided_exit.md) 新增 single-spoke (2,1,1)／(2,2)
核心類；完整 Σ=Ω\{q} 使用來源雙缺失及刪邊繼承，不只靠 T4 acceptance。
失敗側唯一 degree-5 現剩 t=0 六型、t=1 的 (3,1)／(4)。

## 驗證紀錄

全部通過：

```bash
python3 scripts/c5_single_spoke_residual_locality.py --check
python3 scripts/c5_single_spoke_first_bridge.py --check
python3 scripts/c5_single_spoke_two_arc.py --check
python3 scripts/c5_single_spoke_cross_row.py --check
python3 scripts/c5_single_spoke_frame_arc.py --check
python3 scripts/c5_single_spoke_two_two_external.py --check
python3 scripts/c5_single_spoke_two_two_minor.py --check
python3 scripts/c5_single_spoke_two_two.py --check
python3 scripts/c5_single_spoke_bridge_path.py --check
python3 scripts/c5_single_spoke_branch_palettes.py --check
python3 scripts/c5_single_spoke_single_contact_bounds.py --check
lake build
python3 scripts/check_docs.py
python3 tools/docgraph check
git diff --check
```

新 JSON 與表格重算逐 byte 相同；前序 (2,2) artifact 全部保持原內容。
`lake build` 成功（8,827 jobs），只有既有 AttachmentOrder／SymRelabel
linter warnings；未新增 Lean 證明。文件檢查與 DocGraph 都通過。

(2,1,1) 本輪只重播最後的單接點上界 checker；更早的 completion、root
掃描等沿用既有證據，未重跑整條鏈。雙拒絕 atlas、R 系列大覆蓋、一般
profiles／閉包、two-spoke 大枚舉及 Lean axiom audit 均未重跑。
文件檢查不驗證數學，build 不驗證本輪紙面引理或拓撲。

## 下一個窄問題

single-spoke (3,1)：保留三個原有序接點與全部實際附件，研究兩份拒絕
palettes 在最小三接點 block subtree 的第一個分叉／odd-cycle block。
不直接套用二接點 bridge 路徑定理，不重啟已完成表的圖枚舉。
來源可實現性、完整 Σ、其他核心、一般單側／共同出口及主命題仍未證。
