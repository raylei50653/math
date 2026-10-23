# 941第二輪：兩個外點等號支已排，原面新點與一般附枝

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
從[上一輪封存](../2026-10-23-941-types-wrong-side-6b09cd4/REPORT.md)接續三線。
入口245份最終檔案全驗 SHA、零漂移；完整同原 G／F、字面框、rotation、
有序接點、原附件、完整分量、空 fibres 與 full lifts 全部保留。

**Γ8內恰二點時，M2非空的六外點整支與M2空、T六度的五外點整支均已排。**
全11必要型共同至少六外點；M2非空至少七外點。T五度時，完整M2非單點或
真的觸發對側分離支至少九外點。這些是條件來源排除，11整型本身仍 OPEN。

- [原 z4–V 面的新私有點 χ](../2026-10-23-941-gamma8-joint-bpaths-6b09cd4/REPORT.md)：
  任意內點數的此Γ8，都必有圈外私有 χ2∈L02∩Cψ12 或 χ3∈B13∩Aψ03。
  j=2 時 χ 避開完整 M2、兩K2出口與完整rootless原星保護集合，既有負擔
  全部加一：原邊Tm時至少D+d(m)−3，非邊Tv時至少D+d(v)−1，M2空時至少D。
  前輪60列的六外點共同B-path停止點已被整支排除；有限部分接口保留作歷史。
- [七內點K6的四候選縮減](../2026-10-23-941-gamma8-k6-exterior-6b09cd4/REPORT.md)：
  空M2五外點另有獨立來源反證。兩份中央三角形與兩份共面三點識別，各自
  完整關係包含於原R19，聯集恰覆蓋R19。由一份原 G 的真正01232完整
  witness 只選一次 H；此同一 H 的三拒絕列均可拉回原外側、補回七點。
  合法原 C5 disk 完成尺寸為k−7／k−9，與全域最小性矛盾。
- [一般 wrong-side 無框附枝與共點星](../2026-10-23-941-wrong-side-branches-6b09cd4/REPORT.md)：
  恰二真交共b3時，刪共同點後的b分量一律無B14接點，連q框例外也不含c。
  私有共同b3原度至少6+m，q的F度至少7+m；兩個b1皆非Y時至少9+m。
  一般真交數下共U的C兩支不能分別含V/Y，並迫原d(U)≥6+m，故U五度共點支已排。
  m是所選兩中心中的D0數；q/U只用F側link路，沒有冒充完整cyclic星。

四候選通用證明見 [PROOF](PROOF.md)。本輪 [reduction-certificate](reduction-certificate.json)
及 [checker](check_reduction.py)直接由原13點邊獨立窮盡七內點4⁷賦色、
完整31個有序proper六框及各52份原lifts／12個空fibre，從四份實際候選
圖／商映射重建支援5／8／5／8，逐候選全列回填且聯集恰原19非空列。
另直接核132目錄無一符合這張同一H的四列條件；不重跑目錄枚舉。
空M2 agent 的第二路校準另把全部4096字面六框及2400份字面舊 lifts 核回
原30邊，與root的原邊重建互補。平面合法性、真正接受見證及嚴格完成尺寸
由紙證承擔，沒有由固定控制 PASS 推出來源排除。

```sh
python3 -B audits/2026-10-23-941-types-wrong-side-round2-6b09cd4/check_reduction.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-types-wrong-side-round2-6b09cd4/check_reduction.py --seed 17
python3 -B audits/2026-10-23-941-types-wrong-side-round2-6b09cd4/check_reduction.py --negative
```

[REDUCTION_VERIFICATION](REDUCTION_VERIFICATION.json)記正常／seed17一致、8語義及
2外部破壞拒絕、36份凍結入口零漂移。三線重播、交叉紙審與保管索引見
[REVIEW](REVIEW.md)；完整來源控制仍 `not triggered`，有限校準為
`triggered and holds`。沒有給出一張實際目錄外原圖，不混同條件縮減與來源實現。

下一窄義務：非空M2的至少七外點須把 χ 的兩色／完整分量身份接回同一
原外側；空M2、T六度則是至少六外點。一般長Γ追無框B附枝、同一P的
避B/K/C原01逃逸及C其他割點／原橋。現在的下一步由
[Kempe導覽](../../docs/c5_kempe_guide.md)維護。

**11整型、更多Γ內點、較長Γ、一般wrong-side、初始八配對、941／W7／J1／J2、
一般較小bad、Lean及matching仍OPEN；共同k≥23、W7排38／40不變。**
本輪未 commit／push，所有上一輪檔案保留。
