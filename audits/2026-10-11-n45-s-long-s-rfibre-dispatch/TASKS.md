# N45-S-LONG-S：下一輪全 r-fibre 缺口派工

2026-10-11。以下四個任務可以同時發布，不需要等其他 worker 結果。
每份任務檔都包含完整共同契約、權威 pins、專屬輸出、交付格式及停止點，可各自整份貼出。

| 任務 | 可發布全文 | 精確工作域 |
| --- | --- | --- |
| A | [T1 原邊恢復](TASK_A_T1.md) | t_s=1；14 schedules × b0/b2 两 spoke，共28個查詢 |
| B | [T2／β=q0](TASK_B_T2_Q0.md) | t_s=2、β=q0；3 schedules |
| C | [T2／β=q2](TASK_C_T2_Q2.md) | t_s=2、β=q2；7 schedules |
| D | [完整 block transfer](TASK_D_TRANSFER.md) | 任意大小精確接合＋至多8個具名 interface cases；不分配來源排除 |

A/B/C 無重疊覆蓋剩下24個必要 schedules；D 是可獨立支援三者的工具／紙面介面。
優先攻 q0 的三件與 q2 的七件，T1同時保 b0/b2與兩β身份。全域以 [tasks.json](tasks.json)
保存，不能把必要 schedules 稱來源圖數。

本輪 Git BASE 為 `f2692089ad4259808e27d9b7e882ac09505b180a`。
新採納 review 用另行封存的 physical SHA256，[input-pins.json](input-pins.json)精確區分。
前輪 [驗收報告](../2026-10-11-n45-s-long-s-review/REPORT.md)及更正被 frozen於本派工包。
沒有依賴缺失 observations 的 BASE blob，也不修改前輪交付。

只新增本派工目錄；未啟動四項研究、未更新共享 docs、未 commit/push/PR。
結果返回後，再獨立驗收所交 paper scope／full fibres／finite controls及新增充分前提。
