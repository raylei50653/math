# 941：兩 patch 次序與共點，加入原路標記

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`，數學前提承接
[第五輪941](../2026-10-23-three-mask-round5-cb8f859/941/REPORT.md)。本輪只追普通短型I、
02型13／36的wrong-side；兩個初始03型4／9均保留，未排初始八配對。

同一原圖、同一完整K交換後，現在可用原路標記指定兩對patch：原P最後K
出口選出沿α連續的Q側一對，原u⁻–Z橋選出沿β連續的Ω內一對。兩對不預先
識別。任兩不同中心patch若共兩點，這兩點必是一條原四色圈邊；圈邊又強迫
相應界面直接連兩中心。P標記對不能共01或23，Z標記對不能共13。

**最窄新增結論：若恰有兩次真橫穿，兩patch或合至少七原點，或恰共指定原邊
u⁻–Z而合六原點。** 後者若兩中心皆為21，迫原Z度數至少六；Z五度時仍保留
其他中心型。共13或共01的任意對則迫全局至少四次真橫穿。

另可證存在同時沿α／β相鄰的耳透鏡，但不保證含任一原路標記，內部也可有
其他完整分量界面；不能當原空cap或用來消除兩種標記義務。完整論證及精確
前提見[PROOF](PROOF.md)。

[certificate](certificate.json)的24份恰共兩角色schema，分2同中心、4 K4、
2雙非邊C4、16共圈邊；16份逐實際面重建零線連接、32份共點link核對一致。
同／異中心類型均保留局部四面disk，局部disk不提供完整來源。
原完整四份target／02資料、全部空fibres及full lifts逐字保留；35份authority
凍結、routing另記，見[INPUTS](INPUTS.json)。

```sh
python3 -B audits/2026-10-23-941-patch-order-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-patch-order-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-patch-order-6b09cd4/check.py --negative
```

實際重播及反控制見[VERIFICATION](VERIFICATION.json)，獨立紙證審查與文件傳播
見[REVIEW](REVIEW.md)。一般拓撲由紙證承擔；finite為`triggered and holds`，
完整941來源／wrong-side為`not triggered`。沒有來源枚舉、LP、新Lean或較小bad。
原五度兩側、高度、rootless、tip、U／VY／q例外、R=r未知均保留。

下一窄義務：恰二真交的六點指定共邊／至少七點分支，與同一P及B13最後C橋
接合；四次以上保兩種標記對的完整次序。一般wrong-side與B側、八配對及
941／W7／J1／J2仍OPEN。接續由[Kempe導覽](../../docs/c5_kempe_guide.md)維護。
本輪未commit／push。
