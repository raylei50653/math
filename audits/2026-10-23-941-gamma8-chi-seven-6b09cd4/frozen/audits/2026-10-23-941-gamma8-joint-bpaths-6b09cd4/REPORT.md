# 941：原 z4–V 面排六外點與空 M2 五外點等號

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
承接[同U完整星接口](../2026-10-23-941-gamma8-u-link-6b09cd4/REPORT.md)，
保同一原圖、字面框、完整分量／stars、rotation、有序B14及全部空fibres／full lifts。

**Γ8另迫一個嚴格外側私有點χ。** 它是原boundary邊 z4–V 在F側的實際
三角面第三點，只能為原2的χ∈L02(z4)∩Cψ12，或原3的χ∈B13∩Aψ03。
框s／q例外分別由C≠D及原V/Y共鄰引理排除；Γ唯一原3點W*∈Q不能是χ。
原邊z4χ又使χ不能在Γ內。此新點引理對任意內點數Γ8成立，保外耳及Erootless。

χ避開完整M2、兩K2出口與T／任意M2點的完整rootless原星聯集。因此在
既有 **j=2** 保護集合域，所有原負擔共同加一，見 [PROOF](PROOF.md)：

- M2非空：全11型至少七外點；原邊Tm的雙星界為D(T)+d(m)−3≥D(T)+2。
- T五度、完整M2非單點，或已觸發的對側完整分離支：至少九外點。
- M2空：至少D(T)個外點，D(T)偶且至少六；T六度五外點等號整支排除。

本輪原先的兩出口共同B-path探索保留在 [JOINT_EXPLORATION](JOINT_EXPLORATION.json)
及 [ACTION_EXPLORATION](ACTION_EXPLORATION.json)。其66份部分接口尚未補
z4–V的F側實際面，**全都不是來源**；χ紙證直接排六外點假設，無需把部分
接口的必要palette門檻當成完整外側disk。

```sh
python3 -B audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-joint-bpaths-6b09cd4/check.py --negative
```

先驗上一輪final-manifest本子線29檔一致；[INPUTS-v2](INPUTS-v2.json)凍結12份
直接authority。[producer](produce.py)與獨立[checker](check.py)重建四份合同×
兩等號支的8份完整原面候選表，候選皆空；另保16份K6八內點固定cap的496份
完整有序框關係與所有lifts含空列，作獨立後續資料。[VERIFICATION](VERIFICATION.json)
記normal／seed17一致、15項語義及1項外部損壞拒絕、全部輸入零漂移。
有限校準為`triggered and holds`，完整來源仍`not triggered`。

下一窄義務是 **j=2、M2非空至少七外點時，χ2∈L∩C或χ3∈B∩A的完整原星
如何接同一K／B外側disk與完整後繼**；空M2／T六度處理至少六外點接合。
11整型、更多內點、一般wrong-side、較小bad、matching與新Lean仍OPEN；
共同k≥23不變。本輪未改舊產物或共享docs，未commit／push。
