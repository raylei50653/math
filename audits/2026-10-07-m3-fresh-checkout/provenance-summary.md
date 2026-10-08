# M3 前序依賴、歷史 provenance 與 whitespace 核對

受驗候選：`ba0b447f09617591d9f2ba81c988f537af771791`；Oct05 review：`a484d4cdaeb069702de0c40acf83bc6a05dea3b3`。
fresh checkout 為 `/tmp/math-m3-ba0b447`。此子項不修改候選 source 或原證書，不做 Lean、紙面證明、k 擴張或 commit／push。

最終 [dependency inventory](dependency-inventory-v2.json) 列出665份來源、producer與證據 corpus 的保守清單；663份大小及 SHA256 與review一致，無缺失review reference，僅兩份來源文件改變。每份實際 hash、review hash、來源分類及引用均在該JSON，並涵蓋本機 Python import 閉包。Git未存原bytes的大型依賴另以review的 MANIFEST／ARCHIVE 鎖定hash對照fresh還原bytes。

| 變動依賴 | Review SHA256 | 候選 SHA256 | 影響 |
| --- | --- | --- | --- |
| `docs/c5_kempe_guide.md` | `b3f6a45327df869e4e0cf893f6a3ce2a113aec1b28c1a8bf371ebbe26003505c` | `7cbad5d926f8d92a3fa2d4c83256833713608adba15d6013d9b413dfbe8d2778` | E4C |
| `docs/c5_excess_two_mixed_core_spokes.md` | `a829d98ebf84a952445e9aebb443cca1b8e0d7129ceaf1a5353b51379f059061` | `2fe0780d75175f1ccee38a20939eb29f89048a67a82c07fb20afb59ac7680136` | E5_branches |

ES／ES acceptance／ER、E3四項、E4 control、E5 local、E6三項、K′及D8的來源與證據hash均一致，沿用既有有限驗證；本輪未重跑這些checkers。Oct05本來未重跑ES完整主搜尋或全套seed17，這個界線照留，不將ER對照混稱ES主搜尋。沿用結果只涵蓋原有限domain與具名前提，不增加紙面、拓撲或一般定理結論。

以下四份普通 strict replay 實跑皆exit1；各完整fresh JSON已重算，逐leaf差異精確等於明列allowlist，沒有忽略整個provenance map。完整 [provenance summary](provenance-summary.json) 保存來源／fresh產物SHA256、精確差異值、命令與logs。

| 檢查 | 判定 | 唯一允許差異 |
| --- | --- | --- |
| E4 reductions | 歷史 byte FAIL 保持 FAIL | E3 REPORT 的 `/sources/.../bytes` 與 `/sources/.../sha256` 兩leaf |
| E5 controls | 歷史 byte FAIL 保持 FAIL | `/source_sha256/artifacts/c5_excess_two_e3/REPORT.md` |
| E4C | 歷史 byte FAIL 保持 FAIL；現guide hash另漂移 | `/source_hashes/docs/c5_kempe_guide.md`；54份控制全部逐byte相同 |
| E5 branches | 本候選新增 byte FAIL，具名 `M3-PROV-E5-BRANCHES` | `/sources_sha256/docs/c5_excess_two_mixed_core_spokes.md` |

四份數學payload均與原證書完整相等。新增E5 branches finding必須由M4 findings ledger獨立記錄文件provenance例外；不得重寫原證書或併入Oct05三份歷史失敗。E3 REPORT的歷史bytes／hash差異完全重現Oct05紀錄。E4C guide的原證書hash為 `bd0502e091973b50a9ec02b8f0d39716cdc3bf5cb7144d4da62df741f57d34b4`，Oct05重算為 `b3f6a45327df869e4e0cf893f6a3ce2a113aec1b28c1a8bf371ebbe26003505c`，本候選現hash見上表。

整分支 `git diff --check 2ddc6b4a4e412ab2cb7917fe4fb6fdeef2e86090 ba0b447f09617591d9f2ba81c988f537af771791` exit2；86項診斷的12380-byte raw輸出與Oct05逐byte相同，SHA256 `2868ebd2cf8e43057913481873577faa91a9f85a2df61b408f3b8707a6bad4d3`。全部精確路徑／行號及每份例外source的review／candidate hash列於 [whitespace comparison](whitespace-comparison.json)，每份source bytes均未變。零新增／零消失診斷；沒有改寫舊86項紀錄。候選parent diff另跑exit0。

fresh命令／exit／耗時／logs／SHA256分存於 `commands/provenance_*.json`。最初保守清單曾多納D8整份delivery metadata，該fresh結果留存為 [deterministic gzip](dependency-inventory-first-pass.json.gz)，原大小／SHA256及gzip SHA256見 [seal](dependency-inventory-first-pass-seal.json)；使用v2作最終沿用依據。原raw副本留在 `/tmp/math-m3-provenance-first-pass-dependency-inventory.json`。

驗收界線：此子項確認具名hash漂移均只限文件provenance，沒有新增數學payload差異。其他M3重播、還原、LC與整體來源零byte漂移由主驗收包各自回報；此結果不替代M2紙面獨立稽核或M4最終SHA／遠端CI。
