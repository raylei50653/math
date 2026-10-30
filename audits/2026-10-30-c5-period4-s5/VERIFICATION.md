# S5／週期四研究的驗證與停止點

2026-10-30。權威來源為 [研究報告](../../docs/c5_kempe_period4_s5.md)。
沒有以有限無見證或 checker PASS 宣告一般候選成立。

## 數學與證據範圍

- 紙面：S34 下的五個原附件身份；S5 外部三邊捷徑；完整附件五環的單點帽矛盾；
  同一完整著色的實際 buffer 分量接合；固定五環的單點側著色剛性。
- 有限詞表：28 個一輪詞、五面各二詞、32 聯合 phase、2,090 個閉四輪詞；
  兩個完整附件環 phase 均不能接共同帽點。producer 與無 producer imports 的獨立 checker 均核對。
- 真圖控制：獨立重播 Errera 二十次完整 O 分量交換、全部六色對的完整 Kempe 閉包；
  100 商態／2,400 字面態／1,000 商態上的實際 actions，有三色框，非封鎖。
  四輪六時刻的兩種 buffer 分別有 48 份遠端重接；近 buffer 投影週期二，第二 buffer 四。
- 有限來源：保存 plantri 12–24 總點的 9,733 張原 rotation，逐圖重核 S5 得 7,690 合法來源；
  全部 114,669 五度中心、5,507,014 完整固定字面 ABACD fibre 著色、41,476 成功單輪 h；
  每個部分 h 均無週期。框架為每個保存 rotation 顯示的首點與方向，未另搜全部十種框架。
- 獨立搜尋重播：從同一原輸入重核球面、頂點刪除短環分隔、bit-domain 完整 fibre、
  bitset 完整分量及 Kahn 無週期判定，逐中心數量全部一致，
  見 [獨立收據](search-independent-n24.json)。不匯入 producer。

分類完整性仍依賴外部 plantri 生成；本輪對具體保存輸入的驗證不需要其分類正確性。
沒有新 Lean theorem，沒有 4CT oracle。沒有找到合法 S5 四週期，沒有新的全封鎖分量反例。

## 執行與保管

實際完成：

```bash
python3 scripts/c5_period4_s5_search.py --generate
python3 scripts/c5_period4_s5_search_review.py
python3 scripts/c5_period4_face_constraints.py --check
python3 scripts/c5_period4_s5_replay.py --check
python3 scripts/c5_period4_s5_search.py --controls --check
```

搜尋 producer 生成並掃描全部保存輸入；獨立搜尋 checker 另完整重算一次。
本輪未再執行耗時且重複覆蓋的 producer 全域 `--check`；該命令保留供未來重播。
逐命令文件／控制檢查與輸出見 [verification.json](verification.json)。

主搜尋證書 47,784,504 bytes、n24 原 rotation 1,086,447 bytes 依既有
`tools/audit_archive.py append --paths` 保存為兩個 gzip blobs，原始 bytes 保留；
索引與 ignore 規則只追加這兩個指定路徑。新 checkout 先
`python3 tools/audit_archive.py restore --artifacts`。保管核對不代替數學驗證。

## 文件傳播與 OPEN

Updated：新增權威報告、證據及重播；原封鎖報告頁首指向後續，Kempe guide 與 STATUS 新增入口。
Reviewed-unchanged：原短週期定理、932 停止點與 Q5 量詞保持；沒有新的一般 closure，
所以未變更其他父題的數學裁決。HANDOFF／README 的研究線路由仍適用。
Propagation stop：L1，新增必要條件沒有解決原父命題。

Remaining OPEN：w 環缺邊時的合法四週期；如何迫出固定的違規分隔五環；
封鎖分量中的四週期排除；封鎖分量存在性、週期六以上及原 Q5。
完整工作樹原已有其他研究變更；本輪未提交或推送，未覆寫無關研究產物。

最終文件連結檢查通過（800 Markdown／10,688 本地連結），`git diff --check` 通過。
正式 docs DocGraph 通過（98 documents／386 relations）；
全樹 DocGraph 有保留快照的 72 個 duplicate-id 錯誤，未刪快照以隱藏失敗。
早期檢查在其他工作尚寫入及本輪驗證文件尚未建立時的缺連結診斷亦保留於 verification.json。
