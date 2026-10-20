# 精確 residual 與 phase：獨立複核

**PASS，範圍限固定 cell95。** 使用凍結輸入的原邊、
原五點有序框與字面四色，枚舉全部 `4^8` 指派；逐邊過濾 proper
後，以 adjacency BFS 重建每份染色的 maximal 二色分量及完整交換。
在這個獨立系統上建立 `J`、完整 fibres 和 residual 集合 BFS，
未使用主實驗的既存轉移表來產生結果。

直接圖輸入來自上一輪尚未提交證書的凍結位元組，SHA256
`feed98beeb5f83e29bf9c690283aff5d768d4f1e8ba0504f0422560fddeea6dc`；
它不是 Git BASE `af0df8081e79b51f8b24e17e01b2bd5572e46a0a`
已提交的內容。

## 有限閉包與逐項比較

全部 264 份 proper 染色重建後，完整 `J` 有 192 個初始 fibres：
120 個 singleton、72 個 doubleton。
依

```
R' = {T_a(c) : c in R, T_a(c) defined, J(T_a(c)) = observed_J}
```

得到閉包 `192 → 288 → 336`。最終有 264 個 singleton、
72 個 doubleton，含吸收空拒絕態共 337 態。
5,040 個合法 residual/action 組合有 5,136 個非空觀測後繼；
其中 4,944 組只有一種觀測，96 組有兩種。

[交叉複核](cross_review.json) 對主證書所有
`337 × 30 × 192 = 1,941,120` 個輸入格逐項比較，
包含省略項的空結果、非法 action 的獨立標記及空態的吸收行為；
沒有把非法 action 當作圖上的有效自迴圈。
閉包集合、全部初始 fibres 及轉移均相同。

獨立重建兩步真路徑及 quotient 邊合成路徑後：

| 核對 | 數量 |
|---|---:|
| 真路徑接受 | 45,888／45,888 |
| 假路徑拒絕 | 384／384 |
| 逐歷史核對原始見證傳輸與當前 residual 相等 | 46,272 |

保存的 384 條拒絕路徑亦逐條相等。
原始見證索引須連同其沿 action 歷史的傳輸保留；
直接拿未傳輸的原染色與新觀測相交會誤拒真路徑，
獨立證書另存此負控制。

## 同通道 phase 與中途觀測

以獨立完整交換表重新計算並核對：

- 同通道有序兩 action 完整染色檢查 19,800 次，各通道 6,600 次；
  兩種順序的完整終點一致。
- 初始完整 `J` fibres 的兩步 observed phase 分支共 15,264 個。
- 192 個 observed phase 的淨傳輸為 identity，存活候選卻真有縮減。
- `phase.json` 保存的三步負例逐步重播：精確 residual 為空，
  省略前兩步觀測的 parity-only 方法卻得到非空。

同一互補通道內，完整分量可在**每份入口候選**上固定，
將翻轉次數按分量取奇偶；共同接框 block 不能取代各候選的
私有頂點身份。phase 壓縮仍須保留通過全部中途觀測的入口候選。
`P_a D_j P_a` 可以是有資訊的篩選，不能因 `P_a²` 的對合性刪掉它。

主報告另示範 `c=01012132`、`d=01012233`、
`a=(12,root1)`；此命名例已使用獨立表讀取核對。
按「c 分支的第一步觀測、原始觀測、d 分支的第一步觀測」要求，
精確 residual 依次為

```
{02012231} → {01012132} → ∅.
```

若丟掉前兩步觀測，第三步錯誤保留 `{02012233}`。
獨立證書的觀測 ID 依次是 `17,0,16`。
`phase.json` 的自動首例使用 `(23,root4)`；
兩例都已核對，屬同一種「傳輸抵消、篩選未抵消」機制。

## 探測後回復原染色

後續 [check_probe.py](check_probe.py) 直接使用上述獨立圖重建資料，
以 pair-state BFS 求每個 double fibre 的最短共同合法區分序列，
再逐一模擬兩種實際染色：觀測完整 `J`、更新精確 residual，
最後逆序執行同一批對合 action。
[probe_review.json](probe_review.json) 以 exclusive-create 另存，
未改動既有證書。

48 個 double fibre 的最短 probe 長度為 1，24 個長度為 2。
全部 144 個實際分支都回到原始完整染色，且最終 residual
恰為該染色的 singleton。這個構造使用 2 或 4 次 action，
上界為 4；此處核對了最短 **probe**，未宣稱整趟回復方案最短。
原有 120 個 singleton 初始 fibre 不需探測。

另逐步比較根目錄 `probe.json` 的全部 144 分支：
action、實際完整染色、共同觀測及 residual 全部一致。
該主證書 SHA256 為
`58492d3930606a204e35abe534c4f3e973c7812cdc16a468e57ad0a2732a6bcc`。

## 保存、重播與邊界

本輪新證書均以 exclusive-create 首次產生，未覆寫開發版本。
[獨立證書](independent_residual_certificate.json) 的 SHA256：
`87cd3e409139ea7f020eb7545043c3c80a2a63780dba87d74efcab26c1d34c8a`。
[交叉證書](cross_review.json) 記錄主證書及 phase 證書的精確雜湊。
三個 `--check` 均通過；11 份凍結輸入的原雜湊未變。

```sh
python3 -B audits/2026-10-20-kempe-residual-iteration-af0df80/review/check_residual.py --check
python3 -B audits/2026-10-20-kempe-residual-iteration-af0df80/review/compare_residual_phase.py --check
python3 -B audits/2026-10-20-kempe-residual-iteration-af0df80/review/check_probe.py --check --compare-root
```

已只讀核對主 `REPORT.md` 的計數、來源權威與語義；未發現計數或來源錯誤。
候選至多 2 依賴此圖的完整 `J` 初始 fibre 及單射傳輸，
不能推廣為任意圖或任意初始觀測的界。
精確 residual 的歷史語義不提供一般小摘要、一般儲存改善、
嚴格下降或終止性，也不觸發完整 r6／941／J1 來源；無新 Lean。
未修改正式文件，未 commit／push。
