# D₃ C／C₂：完整 P₃ 關係、側身份與 geometry 30 範圍獨立稽核

本子稽核只寫此目錄，以 D₂ 整合後的 C／C₂ 凍結資料為輸入；未改
production scripts、原 artifacts、共享文件或 Git HEAD，未 commit／push。
初次 live-input PASS 保存在 [attempt1/results.json](attempt1/results.json)，
加入具名負控制後的凍結-input PASS 見 [final/results.json](final/results.json)。
兩次實跑均無失敗；D／D₂ 的既有失敗紀錄沒有改写。

[audit_relations.py](audit_relations.py)只用標準函式庫，沒有匯入 production
enumerator、join helper 或 witness validator。P₃ 染色由具名原邊重建，
固定同一個 q=01012，用獨立 MRV 回溯列出全部染色。側角色、必要接合及
幾何由 degree／禁色條件與原文件的 (7)–(9) 重新導出；保存的排除原因、
retained flags 與計數皆不作判定 oracle。保存的 masks 只在完整 tuple
集合已獨立相等之後核對。

## 完整 C 覆蓋

500 份 actual `(S₀,S₁,S₂)` 的 (3,2,1) 附件域逐份無重複；其具名
原邊、lists、2,472 份完整三座標 tuples、root fibres 均保存於
[local_relations.json](final/local_relations.json)。完整三座標集合與原 artifact
逐份相等，112 份有非空 F*；三座標及 x₂ 同一原頂點身份始終保留。

| 獨立核對域 | 全部字面 fibres | 空 fibres |
| --- | ---: | ---: |
| 500 份原 P₃，含 zx₂／wx₂，未加 zw | 8,000 | 224 |
| 同一 500 份原圖加回 zw | 8,000 | 2,224 |
| 336 份 root 交換／路徑反向具名原邊控制 | 5,376 | 672 |
| 14,000 完整側角色接合，未加 zw | 224,000 | 207,200 |
| 同一 14,000 完整側角色接合加回 zw | 224,000 | 224,000 |
| 其中 retained 36 cases／900 側角色接合，未加 zw | 14,400 | 13,300 |

這些 fibre 域重疊，不能相加稱為來源圖數。每份 fibre 完整列出 16 組
具名 `(z,w)`，域外根對亦明寫空陣列，未以缺鍵或邊際資料代替空 fibre。
原 P₃ 未加 zw 的 complete root-P₃ relation 共 22,248 rows；每 row
結合同一 q 及原邊就是一份完整原 P₃ 控制染色。

101 份完整側角色、每種 a 的全部 125 組有序 join、560 份具名 cases
及每份的 25 組 side_join IDs 均自行導出後逐項深比較。
[role_joints.json](final/role_joints.json)保存 14,000 份完整
`(z,w,x₀,x₁,x₂)` rows 及所有字面 fibres，保留兩 root 的 spoke colors、
各原 unary 接點數、禁色集合、殘留及 side-role IDs；未將各 unary
合併成一份禁色 union 來代替原身份。這些是原 C 完整 P₃ relation 上的
**必要側角色語義接合**；C 沒有序列化任意 unary 原圖，故不稱它們為
完整 source graph coloring 或 unary 實現。

[symmetry_relations.json](final/symmetry_relations.json)另保存所有 336 份
root／path 控制，以及 112 份整體框反射與共同色置換後的完整 triples。
反射是搬運原附件、共同色框與根身份，並非各分量獨立正規化。

## 完整幾何與 C₂ 窄身份

114,048 份必要 actual-side-support 候選由完整色框 stabilizer 與兩層
原框扇區／triangle-tether 次序重新篩選，得到 524 empty cases、36 retained
cases／18 local attachments／140 geometries；每份幾何的完整 JSON（具名
Az／Aw、I／J、共同 lifts、child、原 case ID）與原資料相等。
[derived_geometries.json](final/derived_geometries.json)不沿用原 reason flag。
retained 36 cases 的全部 25 side joins 各保留，故原 900 case-side joins
完整不刪列。此子稽核不重證 Jordan 任意大小紙面論證，也不以必要幾何
當作 source degree／minimality 實現。

[narrow_scope.json](final/narrow_scope.json)逐欄核對 C₂ 與原 C 的完整 local、
case、geometry、parent_entry JSON，並從原側角色重建
`CPP-134-1／geometry 30／side_join_id 20／side IDs (8,1)`：

- `S₀=014、S₁=14、S₂=4`，完整 triples=`{(3,0,1),(3,0,3)}`。
- 原根對 `(1,3)` 及 `(3,1)` 的完整 fibre 都是空；`(1,1)` 的完整 fibre
  是 `{(3,0,3)}`。z 側 `{1}`／w 側 `{1,3}` 的 side_join 20 未加 zw
  接合只有 `(1,1)`，加回原 zw 後完整接合空。
- Az=`{b₁}`、Aw=`{b₂,b₄}`；兩側都無 spoke、各保留一份三接點 unary，
  原禁色分別 `{0,2,3}`／`{0,2}`，完整 P₃、外路 `z–x₂–b₄`、原 B
  與 zw／wx₂ 邊在原 context 中逐條保留。

**排除只關閉 geometry 30／side_join 20。** 原 case 的六份 geometries
`[30,31,32,33,34,35]` 與全部 25 side IDs
`[20,21,22,23,24,60,61,62,63,64,70,71,72,73,74,95,96,97,98,99,120,121,122,123,124]`
仍完整；geometry 30 的其餘 24 joins 另列。這份 case 的 geometry×side
必要笛卡兒域有 150 個 keys，僅一個 key 關閉、149 個保留；不是 150
份實現原圖，亦不是把全局 900 的歷史角色列刪成 899。
geometry 34／同一 side_join 20 的 Az=`{b₁,b₂}`、Aw=`{b₂,b₄}` 與完整
兩側 unary 角色保留；本子稽核沒有研究或排除此 successor。

## 具名負控制

[negative_controls.json](final/negative_controls.json)保存三份可核對 witness：

1. 對 local 134／根對 `(1,3)`，z 單獨允許 x₂=3，w 單獨允許 x₂=1，
   兩個邊際 fibre 均非空；同一原 x₂ 的完整 fibre 卻空。假複製 shared
   contact 會接受 `(3,0,3)`／`(3,0,1)` 這組不可能同時成立的 tuple。
2. 只對 C 的 triples 交換色 0／1，而保持原 q 及根對不動，會產生
   假 fibre `(3,1,0)`；重建原邊立即抓到 x₁–b₁ 同色。此 witness 明確
   排除各分量自行正規化後再接合的作法。
3. C₂ 原 triangle 六份完整接點 triples 各座標邊際皆 `{0,2,3}`。
   邊際的笛卡兒積有 27 rows，會假接受 `(0,0,0)`，且使原禁色
   `{0,2,3}` 丟失為空；故未拿 marginals 代替完整 ternary relation。

## 重播與證據邊界

最終凍結-input 實跑 exit code=0，stdout／stderr 分別保存為
[final-run.stdout.json](final-run.stdout.json)／[final-run.stderr](final-run.stderr)。
輸入 SHA256 與 root 保存的 D₃ frozen snapshot 一致，run 前後 bytes 相同；
最終 results 亦記錄本獨立程式 SHA256。初次成功輸出另留在 attempt1。

```bash
python3 audits/2026-10-04-task-d3/relations/audit_relations.py \
  --repo audits/2026-10-04-task-d3/snapshot \
  --output /tmp/task-d3-relations
```

刪邊 coloring 與 K₅ 原 paths 的獨立核對由 D₃ 的另外子稽核交付，此處
不宣稱已重證它們。未查詢 target、未重開來源 catalogue、未新增 Lean
theorem；任意 unary 大小的 Gallai／leaf-block、disk topology、完整來源
實現、一般／共同出口及 `K∞=K≤5` 仍按原文分層。A₃／B₃／C₃ 的研究
成果回收與共用文件同步由根任務處理，本子任務沒有更改停止點。
