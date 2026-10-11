# BR-SD-1g：原 audit 發布與 custody 重播

2026-10-11。Owner 明確授權「整理後 commit + push」。本階段只發布
[原 BR-SD-1g audit](../2026-10-11-br-sd-1g-dbdc4c35/REPORT.md)及本專屬 publication companion。
研究 BASE 是 `dbdc4c35f785519c8e3cb0260807f0d2feb82469`，初始 HEAD／origin/main／遠端 main
均同此值，工作樹只原 audit 未追蹤。正式 canonical 採納、上層文件傳播未獲授權。

原 audit 的160檔（159 payloads加SEAL）全部保持原 bytes／modes，包含 PROOF、MAPPING、REPORT、
獨立 REVIEW／ACCEPTANCE、全部 controls、負輸入、失敗 generation、原舊稿、seal及凍結輸入。
原 SEAL SHA256 固定為 `d3952f60eaba362762d3555b800ba9a03eeaf5171c0404fbea70cfc330ec8edc`。
原 REPORT／TASK 中「沒有 commit／push」及 fresh BASE 的條款保存研究交付時點，
本 publication 文檔記錄這次後續 owner 授權，不回寫其封存歷史。

紙面仍是 **candidate scoped exclusion**；任意大小 proof 的獨立接受不等於 canonical 採納。
actual source finite status為 `not triggered`，沒有新增 Lean theorem。
完整 N45-S-NOU-LS-PAIR 父身份仍 **OPEN**，新增完整 OPEN 身份無條件關閉數為 **0**。
N45 canonical、degree-5 guide、interfaces、STATUS、HANDOFF及三舊 audits 不改。

## 發布後的唯讀入口

原 `verify.py` 刻意要求 HEAD／origin/main同BASE，且工作樹只有原audit未追蹤；
staging及commit後該 fresh-mode條件不再成立，不能把它的預期拒絕稱作證據漂移，
也不修改或 mock它以求PASS。本companion獨立重做所有內容custody檢查，另外核：
實際HEAD是BASE descendant、BASE..HEAD與index均只新增本兩專屬目錄，working狀態合法，
原160檔及publication全檔的HEAD／index blobs各自與工作檔匹配。
它不只比較工作檔，因此不能用本機undo隱藏已提交的越界修改。

```sh
python3 -B audits/2026-10-11-br-sd-1g-publication/verify.py --check --require-tracked
PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1g-publication/verify.py --check --require-tracked
```

31份 authority 與原 frozen／BASE git blob／live path三方比對，三舊 audits全部313檔
原清單及159payload／精確paper接受hashes／22項原checks及其outputdigests均核對。
publication code與本頁另由獨立 [REVIEW](agents/REVIEW.md)及 [ACCEPTANCE](agents/ACCEPTANCE.json)
接受最終bytes；[MANIFEST](MANIFEST.json)另封存本publication全部payload，不改原seal。
此入口只驗本次publication的bytes／Git身份，不承擔新數學、來源存在、Lean或採納。
未來別的提交若改動本次白名單之外檔案，這個精確publication入口會拒絕；
不將它描述成可接受任意後續canonical改動的通用verifier。

發布前原fresh verifier、normal／hashseed17 finite controls、independent solver、舊1e verifier、
正式 docs／DocGraph／whitespace均exit0，紀錄見 [PRECHECKS](PRECHECKS.json)。
新companion的preseal／sealed／staged／descendant重播與Git發布結果依實際執行回報，
只有成功讀回 HEAD=origin/main=遠端main及乾淨工作樹才完成發布。
沒有Lean變更，本輪不重跑lake build；沒有general theorem或新增採納宣稱。
