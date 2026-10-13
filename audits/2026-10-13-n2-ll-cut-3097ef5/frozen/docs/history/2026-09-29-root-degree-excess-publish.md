# 2026-09-29：Root 預算與 no-mixed t_z=2、t_w=1 成果發布核對

依使用者「整理目前進展後 commit + push」整理本輪完整證據包。
接手 main@`30a2e59`，變更均為本輪研究產物。沒有新增數學結論
或改動 checker／證書。SSH 驗證失敗後，使用現有 GitHub CLI 登入
及單次 HTTPS 設定成功 fetch；本地與 origin/main 同為此基準，
ahead／behind 均為零。原 remote 設定保持不變。

## 本次提交範圍

- [Root degree 超額預算](../c5_root_degree_excess.md)：同源完整消去、
  D+O+κ=degree−4、樹上 edge-minimal list 拒絕的邊色描述、完整半樹
  關係遞迴；三層跨列工作假設與已證結論分開。
- [t_z=2、t_w=1 支援覆蓋](../c5_adjacent_degree5_no_mixed_t2_t1.md)：
  原 136 份資料、同源實際支援與具名 rotations、完整 schemas、
  source 預算、逐候選拒絕原因及關閉機制。
- 兩套 checker、兩份 JSON、支援表、[研究紀錄](2026-09-29-root-degree-excess.md)，
  以及 README、STATUS、HANDOFF 的相連入口。

樹控制為 233,744 份 assignments、113 份 edge-minimal 拒絕。
原 136 份中 66 份有相容支援、70 份纖維空，得到 560 份必要支援；
1,002／1,120 個 target 已證，118 個查詢保留 146 組失敗候選。
empty_z／empty_w／same_singleton 分別為 60／68／18；這些是候選數，
不是來源圖數。必要支援未證可實現性，未新增 Lean theorem 或出口類別。

下一入口仍為 record 14／p₁，原 sides=(137,118)，原支援
(S_z,S_w,S_D)=(01,123,34)。唯一失敗候選要求同一 C_w 從
F_w(q)={0} 變為 F_w(p₁)={0,3}，使 E_w(p₁) 為空。
保留飽和 D_w 的原接點、支援與路徑；不將它替成 spoke。

## 驗證範圍

本次無程式、Lean 或證書內容變更；核對兩份 JSON 的 checker SHA256
及全部輸入 SHA256 均符合現檔。沿用同一對話前段已完成的五個
`--check` 逐 byte 重播及 `lake build`（8,827 jobs）：

```bash
python3 scripts/c5_root_degree_excess.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2_t1.py --check
python3 scripts/c5_adjacent_degree5_no_mixed_t2.py --check
python3 scripts/c5_adjacent_degree5_no_mixed.py --check
python3 scripts/c5_adjacent_degree5_interfaces.py --check
lake build
```

既有 build 僅有 SymRelabel／AttachmentOrder 的 style／unused simp
warnings。其餘已完成表、t=2 bridge／endpoints／path-palettes、雙拒絕
atlas、R 系列、profiles／閉包及 Lean axiom audit 未重跑。
發布整理後重跑文件、DocGraph、工作樹及暫存 diff 檢查；HANDOFF
維持 150 行以內。Git 發布狀態以實際 commit／push 及遠端回讀為準，
不在此紀錄預先聲稱尚未完成的遠端操作。
