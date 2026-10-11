# BR-SD-1g-ADOPT：獨立 custody／publication 審查

2026-10-11；reviewer `/root/custody`。本審查固定 task HEAD
`c15a635e17d4be814e19aeeeeb765f3d6024099a`，只寫本任務 `agents/custody/`。
數學 proof／原來源 mapping 由其他 reviewer 重建，本檔不沿用或證成舊 paper review 的數學結論。

**Custody 裁決：未發現原資料漂移；未處理阻斷 finding＝0。**
原 160 檔、publication 6 檔的完整 working inventory、HEAD blobs、index blobs
及 Git modes 相符；31 份 authority 的 frozen／原研究 BASE blob／live／HEAD／index
bytes 相符；三舊 audits 全部 313 檔的 paths／size／SHA256／filesystem modes／symlink
與原 frozen custody manifest 相符。本輪所有舊資料、seals、canonical、STATUS／HANDOFF 未修改。
這是 byte custody 結論，不是數學 ACCEPTABLE，也不授權正式採納或 publication。

## 1. 舊入口的實際拒絕

使用未修改的 publication entry 實際重跑：

```sh
python3 -B audits/2026-10-11-br-sd-1g-publication/verify.py --check --require-tracked
env PYTHONHASHSEED=17 python3 -B audits/2026-10-11-br-sd-1g-publication/verify.py --check --require-tracked
```

**兩者實際 exit 1；不可列作 PASS。** stdout 空；stderr 都是：

```text
FAIL: unexpected working/index state: b'?? audits/2026-10-11-br-sd-1g-adopt-6eae3597/TASK.md'
```

Publication verifier 的 working 白名單只容許原 audit 與 publication companion。
本輪 owner 明確授權的新 ADOPT audit 不在歷史白名單；故這是 **workflow-boundary mismatch**，
不是原 bytes 污損。本 reviewer 沒有暫時移走新 evidence、staging、修改或 monkeypatch 歷史 checker
以取得成功結果。此歷史入口的原兩目錄 committed-addition、tracked coverage 和 byte 義務
由下節獨立工具逐項重新檢查。

另實際執行原研究入口：

```sh
python3 -B audits/2026-10-11-br-sd-1g-dbdc4c35/verify.py --check
```

實際 exit 1，stderr `FAIL: fresh audit HEAD drifted from fixed BASE`。
它固定研究時 `dbdc4c35f785519c8e3cb0260807f0d2feb82469`，publication 後的 c15a635e
本來就不符合 fresh-only 合同。原研究 entry **沒有** `--require-tracked` option；
上述具此 option 的兩項命令正確使用 publication entry。

實際 argv／cwd／stdout／stderr／exit／時間及輸出 hashes 均保存在
[v2 命令紀錄](final-v2-COMMAND_RECEIPTS.json)。正常與 hashseed17 的失敗輸出分別保存；
沒有把預期拒絕從交付中刪除，也沒有以獨立 adapter 的成功覆蓋歷史 checker 的 exit 1。

## 2. 本任務獨立唯讀 adapter

[independent_immutable_check.py](independent_immutable_check.py) 全新實作於本任務目錄。
它不 import、呼叫、修改或 mock 任一歷史 verifier；只用唯讀 Git／檔案檢查。
本輪工作邊界固定 actual HEAD＝task BASE、無 staged／tracked 工作修改，僅准本新 audit
未追蹤；歷史 research BASE..HEAD 仍只准原 audit／publication 的 additions。
新 audit 的 HEAD／index listings 必須为空，沒有將本輪結果偽裝成 committed 或 adopted。

工具 normal 及 `PYTHONHASHSEED=17` 各實際 exit 0，stdout **逐 byte 相同**；
這兩项成功稱為「獨立 immutable custody 通過」，不稱歷史 publication entry 通過。

| 獨立重檢對象 | 完整覆蓋與結果 |
| --- | --- |
| 原 seal | SHA256 `d3952f60eaba362762d3555b800ba9a03eeaf5171c0404fbea70cfc330ec8edc`；exact keys、candidate claim、research BASE、OPEN／0 均相符 |
| 原 payload | 全159 payload的清單digest與逐檔bytes／size／mode／symlink相符；加seal完整160檔，HEAD／index清單精確160且每blob／Git mode相符 |
| Publication | MANIFEST exact keys／5 payload digest與全6檔相符；HEAD／index精確6檔且每blob／Git mode相符；manifest bytes亦固定於task BASE |
| Authority | 固定INPUTS原SHA、research BASE、精確31項；每項frozen／research BASE blob／live／HEAD／index bytes一致，HEAD／index mode與研究BASE相符 |
| 三舊 audits | 固定OLD-CUSTODY原SHA、精確三目錄，全89＋115＋109＝313檔filesystem inventory完全相符；其歷史tracked子集合另外核對 |
| Paper exact-byte binding | PROOF／MAPPING／REPORT三hashes與舊ACCEPTANCE相符，REVIEW hash亦相符；保留candidate／source not triggered／未新增Lean／採納未授權 |
| Publication binding | verify.py／PUBLICATION.md兩hashes與舊ACCEPTANCE相符，REVIEW hash亦相符；只接受歷史custody，不當作本輪數學結論 |
| 原22项checks | 既錄expected／actual exit及每份原stdout／stderr digest相符；这是內容核對，沒有宣稱重跑22項 |
| PRECHECKS | 固定研究BASE及8項歷史紀錄exit0相符；未把其舊output欄位重新解釋成分開的stdout／stderr或本輪execution |
| Local links | 原／publication非authority文件共68項local link／anchor存在；frozen authority保持歷史相對連結語境 |

獨立工具的輸出與原始紀錄見
[normal stdout](final-v2-independent-immutable-check.stdout.log)、
[hashseed17 stdout](final-v2-independent-immutable-hashseed17.stdout.log)及
[完整receipts](final-v2-COMMAND_RECEIPTS.json)。

## 3. 313 filesystem 與 309 tracked 的區別；保留初次失敗

初版獨立 adapter 額外假設三舊 audits 的313檔全部已tracked，故在舊1a目錄
HEAD coverage檢查exit1。這是 **本輪adapter的過強假設**，不是歷史custody漏洞。
已保留[初版adapter](independent_immutable_check.py.initial.v1)、
[初版runner](run_receipts.py.initial.v1)、[初次全部命令紀錄](COMMAND_RECEIPTS.json)
及原始失敗stdout／stderr，能重播最小失效步驟。

舊1a的89 filesystem檔只有85 tracked；下列四份檔在研究BASE及task BASE皆未tracked，
当前仍為既有 `.gitignore` 第2567–2570行四項具名規則匹配的 local-only evidence：

- `audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.corrupted.json`
- `audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.normal.json`
- `audits/2026-10-11-br-sd-1a-0f181045/agents/controls/certificate.seed17.json`
- `audits/2026-10-11-br-sd-1a-0f181045/negative-controls/missing-full-fibre-tuple.json`

其byte／size／filesystem mode仍被313项 frozen custody清單完整固定並重驗。
修正版分開核對**完整313 filesystem**和**309個歷史tracked HEAD／index blobs**，
不刪清單項目，不force-add舊檔，不宣稱這四份已發布。
實際 `git check-ignore -v --no-index` argv／stdout／stderr／exit0保存在
[metadata receipts](METADATA_RECEIPTS.json)。

## 4. 舊歷史措辭、範圍與限制

原 REPORT／TASK 的 fresh BASE、未commit／push措辭記錄原研究交付時點；
publication PUBLICATION.md記錄後續owner授權。其 REVIEW／ACCEPTANCE中的
`root_actual_publication_pending` 等欄位亦是當時review時間的歷史記錄，
不能當作當前published／unpublished判斷。本輪fixed HEAD／HEAD blobs／index blobs
提供當前readback；本審查沒有改寫任何歷史欄位，也沒有延用先前publication授權。

`PRECHECKS.json`及兩種舊ACCEPTANCE保留證據分層：任意大小紙面證明、六個synthetic fixtures、
actual source、Lean、canonical採納與Git publication不是同一義務。這次工具沒有驗證Gallai
推論或J2 barrier，也不將舊「accepted scoped paper exclusion」直接升成正式定理。

**actual source仍 `not triggered`；沒有新增Lean theorem；父N45-S-NOU-LS-PAIR仍OPEN；
新增完整OPEN身份無條件關閉數0。** 數學裁決及canonical delta proposal由root綜合另兩份
獨立審查處理。新audit最終bytes的封存與最後獨立review尚由root在payload完成後執行；
本檔不聲稱已review當時尚不存在的root最終seal。
