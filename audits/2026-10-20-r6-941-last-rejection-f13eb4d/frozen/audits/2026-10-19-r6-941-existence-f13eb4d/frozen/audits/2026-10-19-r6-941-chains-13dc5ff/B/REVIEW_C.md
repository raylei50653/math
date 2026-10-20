# B 對 C 的獨立交叉審查

審查者只寫 B；未改寫 C 或任何凍結輸入。審查的 C bytes：

| 檔案 | SHA256 |
| --- | --- |
| C/PROOF.md | 1921b39d57c9c73a6a15ae743df00e562aa02617c638233552a6944ef91f6dd8 |
| C/check.py | 8168ab52c78878fb3b63665d442dbba0eb04b51a479032dd59257e266057682b |
| C/certificate.json.gz | 4ca10c8ac98e45d346b2b47beb87f9c97204a0065f231db135492e7fa96d6c71 |
| C/cap-lifts.json.gz | 00512a28c5d12e0dd481fd4389c488cce96724dfc858d75aba9324013593d98e |

**結論：通過；未見來源／框／成本／共同性缺口。**

獨立核對原 c=5 的完整 link 路徑 `(b,q,u,s,x)`：五個表列邊組正是
該五邊形全部三角化。qx、ux 由原完整 x star 排除，bu、bs 由原完整
b star 排除，qs 由舊 induced rim 排除，故新邊不會撞到既有原邊。
每組在同一刪 c 所露外面中添加，分別以 q、u、s 為第五框點，其餘兩點
留內；各圖頂點總數 k+4、五框，完成成本確為 k−1。沒有把暴露七框
或共同核心本身當作完成 C5。

以原 b,p,h,x,y,r 的完整 stars 及原 c 的五鄰點獨立重建邊表，
[review_c.py](review_c.py) 不 import C/check.py，對全部 2461 個核心格：

* 逐份重建原 c 各色及五候選的完整左右 assignments，空者保留；
* 對全部 10784 個完整 cap products 重新核對直接原邊／新增邊；
* 按每張實際新框獨立 canonicalize，精確除 core unused-color factorial，
  重建六份十列矩陣，與 C 證書完全一致；
* 重新投影全部 660 份個別比較、32 份共同比較的 live 集，核對原七個
  正列及每個候選所有假定正列，並重得八個 zero-bit patterns。

core-only 新邊 qs 的不 proper 情況可把任一 cap factor 置空；C 統一放在
左 factor，右 factor 可以保留，完整 product 仍空。審查保留此約定，
沒有誤要求兩側同時空或把不同 core 的非空側相乘。

另外執行 C/check.py 正常重播，重建完整交換 family 與閉包，八負控制
均拒絕。H1 的 1023 不可能係其自身應正 01012 全空，而非僅以原 alpha
為唯一檢查；此點在證明與 checker 一致。五圖的32組零假設共同施於
同一 F' 的完整向量，未用五份獨立可行邊際替代。八型仍只為未被必要
零閉包排除，不能視作正計數向量、真圖實現或較小 bad。

```bash
python3 -B audits/2026-10-19-r6-941-chains-13dc5ff/C/check.py
python3 -B audits/2026-10-19-r6-941-chains-13dc5ff/B/review_c.py
```

共同 H0、H2 至少一張1023與 H1 恰1022之結論，在原 c=5 的完整來源域
中成立；本審查不把它升為單獨 c=5 排除或原 Q1/Q2 三拒絕證明。
