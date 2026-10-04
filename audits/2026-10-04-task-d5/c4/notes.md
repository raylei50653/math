# D₅ C₄ 獨立稽核筆記

本包讀取 D₅ 固定快照，稽核正式返回的
`docs/c5_mixed_p3_two_frame_two_unary.md`、checker 與 artifact。
固定身份為 **CPP-134-1／geometry34／join60、side IDs=(27,1)**。
不匯入任何 producer checker；D₄ 的獨立 `independent_front`、`solve` 和通用
witness validator 以原 bytes 重用。來源、實際使用 symbols 及 SHA256 見
`independent_reuse_provenance.json`，每次 attempt 保存自己的執行來源 bytes。

## 任意大小紙面論證

1. 同一原圖中，D_z2、D_z1 是 H−{z,w} 的兩個不同原分量。
   各自外部 incidence 僅有自己的 z-contact 邊與自己的框附件；與另一份 unary、
   w、P₃ 間沒有邊。完整原 relations 由各份所有原頂點染色 lifts 投影，
   z-contact 邊留待局部 root pin 查詢。完整 relation 非空來自原 M−zw 的
   q 延拓限制，沒有假设原 M 可染。
2. 原自身 support A₂、A₁ 未知；只能保留各自包含於 {b₁,b₂}，且其 union
   恰為 {b₁,b₂}。獨立枚舉含空 support 的四個候選與九個 ordered covers，
   沒有把整側 support 分配給某一原分量，也沒有聲稱候選實現。
3. 固定 σ=(2 3)。對一份 Dᵢ 的完整 coloring φ，將每個原頂點的顏色同時
   施以 σ。每條原內邊兩端原本不同，施以同一雙射後仍不同；原 bridge
   正是這種原內邊，其端點和所有內點一同變色，沒有分拆 blocks 或拼接 marginals。
   每條自身框附件的外端只可能是 b₁=1 或 b₂=0，均被 σ 固定。
   原頂點及 contacts 次序不換位。σ²=id 給出完整 lift 集合的雙射，
   進而給完整 ordered relation 的封閉性、禁色 intersection 的穩定性，
   以及 Tᵢ[h] 與 Tᵢ[σ(h)] 的雙射。
4. 因禁色數等於 contact 數，D_z2 的非空完整 relation 必為
   {(0,3)}、{(3,0)}、或兩者皆有。三者的 σ 像均包含原 relation 缺少的
   (0,2) 或 (2,0)，與指定 f₂={0,3} 矛盾；同時原 h=2 fibre 非空、
   h=3 fibre 為空。D_z1 的完整 relation 必為 {(2)}，σ 迫出 (3)，
   與 f₁={2} 矛盾；其 h=3 fibre 非空、h=2 fibre 為空。
   因此九個 support covers × 三個 binary relations × 一個 unary relation
   的 27 個必要組合均被逐原分量排除，兩份分量各自即不可能。
5. σ 僅作用於一份 detached unary；原外部每個頂點保持，包括另一份 unary、
   原 B、P₃、zw、wx₂ 和 D_w。特別是 b₄=2 不改，所以不能把 σ 套到碰 b₄
   的 D_w，也不能把局部 root fibre 双射解釋為整份 M 的 root 換色延拓。
   這段逐邊論證適用任意有限分量大小及所有實際原 bridges。

完整 owned product 的三個候選均有穩定的整側禁色 union {0,2,3}，但其第三
座標保持 D_z1 ownership，σ 像均不在原完整 product relation。
因此整側禁色穩定子測試不能取代逐分量檢查。

## 獨立 Python 與 witnesses

從原報告邊定義重新建立兩個不同 ownership 的固定負控制：二接點原 edge
20–21，以及由 bridge 30–33 相連的兩個原 triangles。逐邊檢查原附件、
完整 degree 四、connectedness、contacts 次序、完整 relation、全部完整 lifts、
σ 影像、四個原 root pins（包括空 fibres）和兩條實際原 bridges。
完整 relations 恰為 {(2,3),(3,2)} 與 {(0)}；全部 component lifts 為 2＋4，
完整 owned joint lifts 為 8。這與 join60 指定逐份禁色不同，明確不能回填來源。

刪各原 bridge，逐四 root pins 保存八份完整 ordered endpoint relations 及
全部 34 份同一刪邊模型 lifts；再逐一查詢全部 128 個 ordered endpoint pins，
包括每個空 fibre。驗證 producer 的每一份 witness 的原頂點域、同一框色、
每條保留原邊和實際附件；完整 lift 集合與獨立枚舉精確相等。
另保存 intact／刪 zw 的 32 個原 context root fibres；其中未知 D_w 始終是
同一來源的符號 relation，沒有發明它的 tuples 或 lifts。

負控制的 K₅ 五袋逐袋非空、互斥、連通與十對實際原邊鄰接均獨立驗證。
這只顯示控制非平面，不參與 C₄ 主證明，也不證成 disk realization 或整份
M 的逐邊 minimality。七項 malformed-data controls 驗證錯邊、重疊袋、
不連通 hub、錯誤 bridge lift、擦除非空 fibre、marginal product 新造 tuples，
以及錯把單 key 完成提升成整 case 完成都被檢出。

## 精確 scope 與停止點

重建前層全部 side roles、500 個具名 local configurations、560 個 cases、
完整 geometry records 與原 join rows。保留 **36 cases／140 geometries／900
case joins**，完整 geometry/join ledger 共 **3500 keys**。繼承 C₂ 的
(CPP-134-1,30,20) 與 C₃ 的 (CPP-134-1,34,20)，只新增關閉
**(CPP-134-1,34,60)**；另外 3497 keys 未經本稽核關閉。不刪原資料，
不對 root-swapped keys 推定完成。

從原 ledger 取出的下一個具名入口為 **CPP-134-1／geometry35／join20、
side IDs=(8,1)**：A_z={b₁,b₂}、A_w={b₂,b₃,b₄}，雙側各一份 ternary
unary、無 spokes，f_z={0,2,3}、f_w={0,2}，E_z={1}、E_w={1,3}。
因各側僅一份 unary 且無 spoke，這裡每份 unary 自身 support 就是各側 support。
其 contacts 保留 ledger 的 ordered 來源符號；完整 relations／原圖／bridges
仍未知。這只是既有未關閉 entry 的導航，**本包未分析或排除此 key**。

本成果的任意大小結論是上述紙面 lift 論證；不需 Gallai、minor 或其他外部
定理。Python 只核對固定 relations、models、witnesses 和 ledger。
未新增 Lean theorem；根代理另執行的 `lake build` 不形式化此論證。
沒有 complete Σ、target extension、一般共同出口或 K∞=K≤5 結論。

## attempts 與保存

- `attempt1-default` 保留執行來源、log 與 exception：誤以為 producer parent
  有 `summary` 欄；修正後從獨立 ledger 推導 36／140／900。
- `attempt2-default` 保留執行來源、log 與 exception：D₅ snapshot 不含原 D₄
  稽核路徑；改由已核對的 verbatim copies 和 immutable provenance metadata
  作為實際執行依賴，重播不需要 live D₄ source。
- `inspection_failures.json` 另保留初次 metadata 讀取同樣的 KeyError。
- 後續成功 attempts 的 SHA、比較與最終重播均以新目錄保存；不覆寫上述
  失敗或 D₄ 封存資料。

重播：

```bash
python3 audits/2026-10-04-task-d5/c4/audit_c4.py \
  --repo audits/2026-10-04-task-d5/snapshot --output /tmp/d5-c4-new-output
```

執行輸出目錄必須尚不存在。本子包不修改 producer、artifacts 或 D₄。
