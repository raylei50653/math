# 932：原 C9 第二層的唯一三接點

本輪新證：在 T2 原完整 932、h=4 的 20 份同源合同下，**整張 H 至多一個
內點同時接三個原 C9 點**。若它存在，必是原邊面第三點 t_i，contacts
恰為 `{c_i,c_(i+1),c_(i+5)}`，其三條原 spoke 把內側分成一個空原三角面及
兩個 induced C6 cell；每個六圈 cell 至少五個嚴格內點。

**現行共同 k≥23 保持不變，沒有新增來源排除。** 局部封閉耳點另給
`m≥10`（k≥19）、三接點時 `m≥11`（k≥20），數值上被現行共同界包含。
本輪的可用增量是同時嵌入／cell 限制，不是提高一般頂點下界。

研究 BASE：`cb8f8593e273a7426ecadd59797a6e643cc4768e`。
[來源合同](SOURCE_CONTRACT.md)、[任意大小紙證](paper/PROOF.md)及
[固定有限證書](certificate.json)均只位於本專用目錄。

原 T2 已分類全部單點 contact sets；本輪沒有把這項舊結果算成新發現。
新增的是對任意兩個不同三接點型，逐份找出四個不同交錯原 C 端點。
兩個實際原內點的二邊路會違反 Jordan 分離，故九條可選相反 contact
只能全無或出現一條。全部 512 個形式子集因而縮成十個必要模板；每份
原 query 都單獨綁定原 C9 名字、attachments、rotation、有向面及完整
annulus case 的 SHA，合計 200 份必要模板，未假定其中任何一份是來源。

耳點推論保留完整原 star：若無三接點且 m=9，九個面第三點封閉成一個
沒有額外內點的原九邊形，耳點的原完整 degree 為四。三接點情況下，每個
C6 cell 若只有其四個必需面第三點，便封閉成含 t_i 的原五邊形；至少一個
非 t_i 耳點也只有完整 degree 四。兩者均違反原 I 點至少五度。

有限 checker 不 import producer；它獨立重建全部 36 份交錯 pair、512
contact 子集及 429／5 份九／五邊形三角剖分。另保存兩張具體有向 disk
控制圖，分別達 m=10／11；逐邊 side、每點 link、Euler、完整 degree 及
contacts 均核對。控制圖沒有原 B 或完整 932，所以來源狀態為
`not triggered`。八項語義負控制包含相反 contacts 同時出現、錯原附件、
局部反轉面、漏 polygon、m=9 的四度耳點與未支援 `--source`。

19 份權威輸入均凍結 exact BASE bytes／SHA。兩次正常／seed17 唯讀重播
及 frozen-input／三份既有 dirty 共享檔 strict drift 見 `VERIFICATION.json`。
預設唯讀重播對後續 routing drift 獨立報告；`--check-entry-shared` 才另行
要求三份 entry dirty bytes 不變，避免 root 文件整合使數學證書失效。
本輪不重跑舊 100 份低度來源排除、外部 C4 枚舉或 broad source search。

```bash
python3 -B audits/2026-10-23-three-mask-methods-cb8f859/932/check.py --check --negative
PYTHONHASHSEED=17 python3 -B audits/2026-10-23-three-mask-methods-cb8f859/932/check.py --check --negative
```

全部 820 列與原十列完整 fibres（含空）保持原樣，**零個新色列刪除**。
沒有新計數可行解、沒有原來源圖、沒有新 Lean；一般 932／h≥5／主命題
仍 OPEN。下一個窄目標是讓一份保留的原 C6 cell 模板提供完整同色框 relation
及接回證明，避免用可選接點枚舉替代原圖共同實現。
