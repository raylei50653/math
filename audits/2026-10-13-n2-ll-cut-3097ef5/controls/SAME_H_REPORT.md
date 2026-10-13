# 無 root-h spoke 的 K5-H 原 bags 控制

本輪紙面 K5-H 取消舊 H 引理的 root-h spoke 前提。
[獨立 checker](same_h_minor_checker.py)／[原證書](same_h_minors.json)
提供 p,z owners 為 `(r,r),(r,s),(s,r),(s,s)` 的四個有限控制。
四份圖**沒有任何 root-boundary spoke**，所以不是沿用舊前提的空泛校準。
完整 target **not triggered**；局部新 K5-H 四次 **triggered and holds**。

固定 `B=(0,1,2,3,4)`、`r=5,s=6`。
C 的 leaf triangle 是 `p7-z8-a9-p7`，另接 bridge `a9-v10`。
原框附件 `p:0,z:0,a:1,v:23`，故 `h=0`。
p,z owners 按四份控制明列；v 在 p,z 同 owner 時取另一 root，
owners 不同時取 r，保證 C mixed。原 Q 是 edge `11-12`，
owners r,s，附件 `34,40`。每個原普通內點完整 degree4；
C、Q 連通且 mixed long，actual supports 分別0123、034。
root 完整 degrees 不等於5，且原圖非平面，不是完整原55來源。

選 Q 的實際附件 `a=3` 與 `C-{p,z}` 的實际附件 `b=1`。
兩条原 a-h 框弧為 `A=(3,4,0)`、`A'=(3,2,1,0)`；
前者避開 b，後者包含 b。

五個原 bags 為

```
{p7}, {z8}, {h0}, {3,4,5,6,11,12}, {1,2,9,10}.
```

第四袋包含 `R={r,s} union Q` 及 `A-{h}`，由 Q 的原 `3-11` 附件連通；
第五袋包含 `C-{p,z}` 及 `A'-{a,h}`，由原 `1-9` 附件連通。
checker 提供且核對各袋原 spanning trees、全部頂點互斥及下列十條原跨邊：

| bags | 原跨邊 |
| --- | --- |
| p,z | `7-8` |
| p,h；z,h | `0-7`；`0-8` |
| p,第四；z,第四 | 明列各自 owner 的原 root-contact 邊 |
| p,第五；z,第五 | `7-9`；`8-9` |
| h,第四；h,第五 | 原框邊 `0-4`；`0-1` |
| 第四,第五 | 原框邊 `2-3` |

共4份原 K5、20棵原 bag spanning trees、40條原跨邊。
每份刻意漏掉一對 K5 鄰接後 checker 拒絕；正常／seed17 逐 byte 一致，
執行前後正式產物 SHA 不變，見 [驗證](same_h_verification.json)。

```bash
python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/same_h_minor_checker.py --check
PYTHONHASHSEED=17 python3 -B audits/2026-10-13-n2-ll-cut-3097ef5/controls/same_h_minor_checker.py --check
```

本控制只校準原 minor，沒有為非平面圖編造 disk rotation，
沒有加入基本 S 接受格，也沒有認證完整 Sigma或 criticality。
完整 fibres、空 fibres 與同列同 pins 原邊回歸另见 [主控制](REPORT.md)。
