# M4-R：最終分支發布、PR與CI驗收

依賴：M4-L完整回報已由監督端驗收，取得真正最終SHA。
本任務供使用者發布；監督端目前没有push／PR／CI dispatch／merge。

**可直接發布的任務：** 將已驗收最終提交發布至`integrate-kprime-e3`，
建立或更新base為main的PR；核對相同最終SHA的Lean CI及文件證據，停止於回報。
不merge、不設定auto-merge。Push授權不包含force push；遇遠端新進展先核對，
保留其他工作，不以舊refs當即時remote狀態。

PR說明以部分研究成果為範圍，明列U1前提、M2／M3證據、兩項新增provenance例外、
三份歷史byte FAIL、原86whitespace、上游NetworkX／分類信任與LC顯式local target。
不能宣稱純Lean一般定理、搜尋完備性、來源構造或全部strict checks通過。
U2–U4、E5新證明、三列推廣、ε≥3及一般缺口保留。

發布後核對local／tracking／remote同名分支SHA一致，重新讀PR head／base及mergeability。
main若前進，交代新增差異並重新評估驗證；不是用本地舊origin/main完成驗收。
Lean CI必須對真正最終head成功，舊SHA成功或空checks不算。
文件workflow目前僅workflow_dispatch：回傳最終SHA的本地文件證據，
或手動觸發後核對該SHA的文件run。預設Lean CI不包含LC，不能混稱。

回傳PR URL、head／base完整SHA、local／tracking／remote SHA、CI run URL／headSHA／結論、
最終正式驗證包路徑、工作樹留存資料及所有未完成事項。
監督端收齊後才判可合併；merge另依使用者的明確指示進行。
