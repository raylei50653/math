# 新相鄰異 owner 私有 contacts 的原 K3,3 校準

本目錄 [supplemental checker](supplemental_minor_checker.py) 與
[完整有限證書](supplemental_minors.json) 校準本輪新紙面 minor 引理：
C 的同一 leaf 奇環有相鄰私有 contacts p、z，分別只由 r、s 擁有；
各有唯一原框附件，且 `k_C^s>=2`。C、另一 mixed Q 都 long，
`C-{p,z}` 連通。此處只驗證明列有限原圖，無有限全來源覆蓋主張。

## 1. 全部原資料及實際前提

固定 `B=(0,1,2,3,4)`、`r=5,s=6`。
原 C 是 triangle `p7-z8-a9-p7` 加原 bridge `a9-v10`；
owners 為 `p:r,z:s,v:s`，框附件為 `p:0,z:1,a:2,v:23`。
原 Q 是 path `11-12-13-14-15`，owners `r,r,r,s,s`，
框附件為 `34,4,4,0,40`。另加原 spokes `r0,s3` 和五條原框邊。

兩 roots 均完整 degree5，其餘九個原內點均完整 degree4；
H 二連通、full B-touch、沒有 shared contacts 或 unary。
`k_C=(1,2), k_Q=(3,2)`；actual supports `0123`、`034`。
p、z 是同一原 leaf triangle 的相鄰私有點，唯一非私有點是 a；
`C-{p,z}={a,v}` 由原 `a-v` 連通，並有原 s-contact v。
checker 從原邊重新計算以上條件，沒有將名字當作資格。

有限圖保留原55及實际degree4，卻**非平面**；完整 Sigma933／941及
每條非框邊 criticality 沒有認證，所以完整 target **not triggered**。
不因 actual supports 能寫成兩個弧就聲稱有 disk rotation。

## 2. 原 bags 及全部九條跨邊

```
left:  {p},       {s}, B
right: {r} union Q, {z}, C minus {p,z}
```

首個字面控制的九條原跨邊：

| left bag | `{r} union Q` | `{z}` | `C-{p,z}` |
| --- | --- | --- | --- |
| `{p}` | `5-7` | `7-8` | `7-9` |
| `{s}` | `6-14` | `6-8` | `6-10` |
| `B` | `3-11` | `1-8` | `2-9` |

最後一行第一格特意使用紙面引理要求的 Q 實際附件 `3-11`，
不用固定圖額外存在的原 spoke。本控制保留原 Q 的 long／mixed／connected 前提。
每個 bag 的原 spanning tree、互斥性及全部跨邊由 checker 獨立核對。

四份變式只對**整張具名圖**作 roots 5↔6、contacts 7↔8 的兩個交換；
JSON 明列每個原頂點的整圖 image。B 字面次序保持原樣，
沒有逐 piece 或逐列重標；這四份圖是不同具名校準，不是可合併 witnesses。
共4次局部觸發、24棵原 bag trees、36條原跨邊，皆 **triggered and holds**。

## 3. 負控制與重播

每份證書另刪掉一項 K3,3 鄰接記錄，checker 因欠一對必要 bags 拒絕；
再刪掉實際 `s-Crest` 原跨邊，checker 因證書所需原邊不存在拒絕。
共8項負控制。這測的是原圖 minor 證據，沒有用染色同／異關係代替原邊。

```bash
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/supplemental_minor_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/supplemental_minor_checker.py --check
```

正常／seed17 逐 byte 相符，見 [verification](supplemental_verification.json)。
本有限控制不新增完整 fibres；全 fibres／空 fibres／同列同 pins 的回歸由
[主控制](REPORT.md) 保留的原固定圖另行完成。
沒有新增 Lean theorem 或外部發布。
