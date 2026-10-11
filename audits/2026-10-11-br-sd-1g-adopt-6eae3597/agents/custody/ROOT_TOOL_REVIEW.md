# BR-SD-1g-ADOPT：新 root custody 工具獨立 code review

2026-10-11；reviewer `/root/custody`。本 reviewer 只新增本 `agents/custody/` 的
review、工具快照及隔離 probes；沒有修改 root `verify.py`／`record_check.py`。

**裁決：接受下列新 root 工具 code bytes；未處理阻斷 finding＝0。**
這是 seal 前的工具審查，不聲稱已審查當時尚不存在的完整 root payload、最終 acceptance、
SEAL、DELIVERY 或其實際執行。完整最終bytes及數學／量詞仍由root安排另一reviewer獨立接受。

| 接受的新 root 工具 | SHA256 |
| --- | --- |
| verify.py | `4e2de6c8e27874175241d869f9f6246b8a114c12bb009c9f5a4ce8ba64d98b9d` |
| record_check.py | `1e90e58f0d27b93d79dc73d8b0f81b7382224758ac5b5600ba256ba74fddfe9b` |

## 1. Custody 覆蓋與唯讀性

1. WORKSPACE_BEFORE 原bytes由硬編碼SHA固定，task HEAD／main固定於c15a635e。
   全15743 tracked entries的index OID／Git mode、filesystem bytes／size／mode及symlink target
   均逐項回讀。baseline中gitlinks數為0。working porcelain只准本新audit未追蹤，
   staged及tracked diff均須空；沒有修改Git refs／index的程式路徑。
2. 完整歷史custody另實際呼叫本reviewer的独立工具，保留原160、publication6、authority31、
   舊313之內容義務。該工具本身是最終完整payload／review接受／seal hash inventory的一項，
   final模式不能在修改其bytes後沿用原接受或seal。它不mock任一歷史checker。
3. 主payload inventory完整枚舉檔案，核path／SHA／size／filesystem mode，遇任意symlink即拒絕。
   只有兩個自述envelopes `SEAL.json`／`DELIVERY.json`和頂層 `postseal/`從主payload清單排除；
   final acceptance另外只排除它自己。其他review、failed probes、archives、stdout／stderr
   都是正式清單的一部分，不能刪減或新增而保持最終byte接受／seal成功。
4. final acceptance須精確schema、BASE、ACCEPTABLE、OPEN／0及0阻斷finding；
   完整accepted_payloads必須等於actual inventory。SEAL也須等於精確產生的完整物件，
   不只是核某些marginal hashes。兩個envelope的filesystem mode固定644；
   SEAL bytes再由DELIVERY固定，DELIVERY的全部欄位由目前內容重新計算比較。
5. postseal只准固定16個檔名，DELIVERY建立時必須完整齊備。五項receipt各自固定argv、
   seed env、actual／expected exit0及自己的stdout／stderr paths；stdout須符合各項
   checker／negative／boundary的具名JSON contract，stderr必須空。
   reviewer readback另對BASE、ACCEPTABLE、無finding、sealed-byte verdict、seal SHA及
   主payload manifest SHA重新核對。未recognize的postseal資料不能納入最終DELIVERY。
6. `--check`／`--precheck`沒有本audit寫入分支；subprocess設定不寫Python bytecode。
   `--seal`及`--seal-delivery`只有exclusive-create自己envelope的寫入與mode設定，不能覆寫舊seal。
   Link checks按階段容許尚未建立的指定envelopes；final `--check --require-delivery`
   仍必須有完整DELIVERY。原／新Markdown local targets與anchors核對，新增md／py無尾隨空白。

Generic receipt helper容許`expected_exit_code=1`，以保留真正負控制的預期拒絕；
最終postseal命令再受具名exit0合同限制。CHECKS及其中task-required commands的語義完整性
仍是final whole-payload reviewer的義務；工具code review不冒充該尚未完成的檢查。

## 2. Findings 與 root 修復

| Finding | 最小失效步驟與修復後裁決 |
| --- | --- |
| postseal receipt只信自述expected exit | 原版本可把無關command或checker失敗寫成「符合自己expected」；root已加label-specific argv／env／exit0／paths／output JSON合同。最終code通過 |
| 初次seal的planned links | 原`--seal`先用final link檢查，要求尚未exclusive-create的SEAL／DELIVERY先存在。root已分開precheck、pending seal、pending delivery與require-delivery階段；不放行缺少final acceptance。通過 |
| logger只預檢receipt collision | 原版本若stdout／stderr已有檔，仍先執行command才因exclusive log creation失敗。root已在執行前預檢三個輸出路徑；stale-log replay在command前exit2，無副作用marker。通過 |
| dangling output symlink與directory symlink | 存在性檢查漏dangling symlink；logs symlink亦能把receipt寫到自己的audit外。隔離舊code重播分別出現「先exec再exit1」及「越自己audit目錄寫入後exit0」。root已拒絕directory symlink／resolved escape，並把output symlink視為occupied。三項修復後replay全在exec前exit2。通過 |
| 自述envelope未封mode | 主payload清單排除SEAL／DELIVERY，原code只驗其JSON內容。root已在seal／delivery objects列明644並檢查其actual modes，creation亦固定mode。通過 |

審查過程中的版本與failed controls沒有改寫成最終結果。
[ROOT_TOOL_PROBES](ROOT_TOOL_PROBES.json)保留早期local-helper probes與工具快照hashes；
其中generic receipt接受無關command／expected1只驗局部helper，不聲稱最終完整checker接受。
當該probe凍結logger時，root已修正stale-log preflight；實際exit2而probe當時預期exit1，
這個本reviewer的錯誤expectation與原stdout／stderr也原樣保留。

具體symlink counterexamples及修復後控制分開保存：

- [修復前完整結果](pre-boundary-LOGGER_BOUNDARY_PROBES.json)：logger SHA `581f86365fbac498a54c97b6b1a360364537c36ab3c933a10fd5b3fdb93be9eb`；stale檔已擋，兩種symlink尚未擋。
- [修復後完整結果](repaired-boundary-LOGGER_BOUNDARY_PROBES.json)：logger SHA `1e90e58f0d27b93d79dc73d8b0f81b7382224758ac5b5600ba256ba74fddfe9b`；三項均exit2且command markers都不存在。
- [可重播control source](logger_boundary_probes.py)：`--input`可選保留的verbatim logger snapshot，`--label`須使用新名以exclusive保存新的紀錄。

所有replay均使用原root logger code的verbatim copies，stdout／stderr／argv／cwd／exit／時間／hashes
逐項保存；一切command side effects都在本 `agents/custody/`，沒有修改root tools或原證據。
Runtime symlink fixtures執行後移除，target及建立方式保存在原始結果与可重播工具；
失敗command markers、partial logs及被redirect的產物保留。沒有留下可redirect最終audit scan的symlink。

## 3. 信任邊界與尚待root完成

這些controls只處理新工具的實際拒絕路徑，不是actual source realization或任意大小數學證明。
原publication normal／hashseed17的exit1仍須如實呈現；本工具通過不能重命名那些舊入口為PASS。

Root還需完成主文件／CHECKS、required checks、完整最終payload的另一reviewer接受，
再exclusive-create SEAL、normal／hashseed17唯讀check、seal negatives、boundary readback、
獨立sealed-byte readback、DELIVERY與final require-delivery check。
工具接受不表示這些尚未執行的義務已完成。若上述兩個root code hashes之後改變，
本接受不能冒充對新bytes的審查，需另行review。

父身份仍OPEN，完整OPEN身份新增無條件關閉數0；actual source `not triggered`，
沒有新增Lean theorem，沒有formal adoption／commit／push／merge授權。
