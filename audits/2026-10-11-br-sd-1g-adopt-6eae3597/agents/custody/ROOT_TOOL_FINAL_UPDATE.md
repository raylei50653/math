# BR-SD-1g-ADOPT：root 工具最終 delta 審查

2026-10-11；reviewer `/root/custody`。保留[上一份工具審查](ROOT_TOOL_REVIEW.md)原bytes，
本更新只審查其後的新receipt digest／retained-failure block及`aggregate_checks.py`。
沒有修改root code或CHECKS，也沒有執行會寫CHECKS的aggregation工具。

**裁決：接受以下最終code bytes；未處理阻斷finding＝0。**

| 工具 | 最終SHA256 |
| --- | --- |
| verify.py | `be7f8e24ee350c3fdece9cdce2ca5ee9367ad5ad7712cfdc99c8a0c611efcac8` |
| record_check.py | `1e90e58f0d27b93d79dc73d8b0f81b7382224758ac5b5600ba256ba74fddfe9b` |
| aggregate_checks.py | `1cf053f33bc15fa094eb8ea1a1348bc996dada1699849bd1c1ee9d58c71ed4a6` |

獨立從current verify刪除這次新增的block後，逐byte重建上一份已接受verify SHA
`4e2de6c8e27874175241d869f9f6246b8a114c12bb009c9f5a4ce8ba64d98b9d`。
因此這次不是未經重審的其他工具改動；logger bytes保持不變。
重建與實際receipt回讀由[唯讀readback工具](root_tool_final_readback.py)完成，
[实际命令receipt](ROOT_TOOL_FINAL_READBACK.json)保存argv／cwd／stdout／stderr／exit0。

## 1. 新 block 與 aggregation 的一致性

Aggregation只枚舉本輪root `logs/*.json`的receipt，原样保留其欄位及每份原JSON bytes的SHA／path。
Final verify重驗recorded output hashes及原receipt digest；完整payload acceptance／seal
又固定CHECKS本身，因此封存後不能單獨修改aggregate欄位而保持byte接受。
本次readback亦逐項核對v1／v2 enriched欄位與原receipt的一致性。
新block不引入寫入分支，原workspace、完整payload、final acceptance、
seal／delivery、mode、link及negative-control义務保持上一份review已接受的行为。

只有具名`audit-precheck-v1`的actual／expected不符可移入`retained_failed_commands`。
其他unexpected failures仍留在commands，令all_recorded_expectations_met為false，
不能取得final seal。retained資料須保持actual≠expected，原stdout／stderr及原receipt SHA
另核對，沒有將actual1改成expected1以變成通過。

若retained failure存在，非precheck模式必須在commands有具名`audit-precheck-v2.json`
actual0成功紀錄；正常receipt檢查另要求其expected也為0。
`--precheck`暫時容許v2尚未生成，避免「執行v2前先要求v2已有成功receipt」的循環。
這個暫時例外不適用seal／sealed check／delivery建立或final require-delivery檢查。

`aggregate_checks.py`會寫本新audit的CHECKS，正確用途是final acceptance／seal前彙整。
封存後再运行它會改主payload，之後完整byte接受／seal檢查將拒絕；
不能把它當成唯讀postseal入口。

## 2. 實際 v1 failure 與 v2 success 回讀

| 原紀錄 | Actual／Expected | 當前group與核對 |
| --- | --- | --- |
| audit-precheck-v1 | **1／0** | retained_failed_commands；原receipt、原stdout／stderr digest相符，未出現在正常commands |
| audit-precheck-v2 | **0／0** | 正常commands；原receipt、原stdout／stderr digest相符，所有enriched欄位與原receipt逐項相符 |

v1是當時planned `ROOT_TOOL_REVIEW.md`尚未交付而造成的實際exit1，保留原stderr及空stdout；
本更新不將它列作PASS，也不將此文件交付時間問題誤稱數學漏洞。
v2成功是已實際執行的結果，不是「預計修復後應通過」。

兩份原receipt SHA分別為：

- v1：`92947223aa6a070752058552a682e5431f656743a3f4188fcc47bf4c860439e1`
- v2：`ac8d5b71a95bd827394a2ac881d938cdd72ca9ae93a9516a32157d1a840c72c5`

回讀工具实际exit0，stderr空；[stdout](root-tool-final-readback.stdout.log)提供完整code hashes、
prior-byte reconstruction及兩份receipt／output核對結果。
這些是工具與實際紀錄一致性證據，不重新證明Gallai／J2／任意大小排除。

## 3. 停止點

本reviewer此後停止寫入。Root需再安排完整最終payload的另一reviewer對最終bytes接受，
完成exclusive seals、postseal實際commands、sealed readback、DELIVERY及final唯讀驗證。
本code接受不冒充那些尚未完成的義務；若最終code再改動，須另行review。

父身份OPEN、完整OPEN身份新增無條件關閉數0、actual source `not triggered`、未新增Lean；
沒有formal adoption／commit／push／merge授權。
