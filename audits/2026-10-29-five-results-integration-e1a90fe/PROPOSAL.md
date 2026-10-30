# 五份回報的核對與接續整理

2026-10-29，基線 `e1a90fe` 加現有未提交研究。使用者要求五份任務結果全部返回後才整理；本輪在第五份返回後開始。

範圍：對回五份原報告，分辨一般紙證、具名來源／接線排除、抽象接口控制及固定域重播；將仍待證的窄問題與驗收標準整理在既有四路 synthesis。保留唯一主攻契約與各專題權威來源，不啟動新研究或擴大枚舉。

- [三步來源](../../docs/four_color_three_step_source_invariant.md)
- [Bernhart retained 交會](../../docs/ck_bernhart_retained_intersection.md)
- [五參考共同輪轉](../../docs/c5_five_reference_common_rotation.md)
- [十二割來源](../../docs/four_color_twelve_cut_c6_sources.md)
- [飽和共同 hub](../../docs/four_color_saturated_hub_continuation.md)

只修改直接 synthesis 與必要入口；[來源快照](source-before.json)保留修改前 bytes。五份專題報告及 frozen 證書不改。正式 docs 與全工作樹檢查分開報告；不改歷史快照 ID。未獲 commit／push 授權。

整合檢查的範圍調整：候選索引檢查發現五參考 verification.json 超過既有1 MB門檻，
依既有 audit archive 政策補封存該檔；只追加 registry／ignore／blob，原始證書 bytes 不變。
[封存驗證](storage-verification.json)保存舊紀錄逐項不變及壓縮還原相等的核對。
