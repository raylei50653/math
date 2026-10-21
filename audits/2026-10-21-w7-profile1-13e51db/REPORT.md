# profile 1：555 patch 縮減的精確障礙

exclusive BASE `13e51db3ec3d8d7ec7eeef60167afdc19ad956c4`。

原完整 p/h/n 三個五度 star 給同一六點界面
`S=(a,b,q,L,R,u4)`、三內點 patch。完整31份 proper normalized界面色列中，
14份有延伸、17份空。每份全部 lifts 與九份非弦同色見證見
[certificate](certificate.json)；幾何與任意外側接合合同見 [PROOF](PROOF.md)。

完成兩個局部 negative results：

- 同一界面、至多兩內點的完整關係相等替換不存在；有直接兩色紙證。
- 允許任意界面弦後，全部14／84／504份零／一／二內點三角化候選，無一
  滿足完整關係子集。每個至少引入三份原空列。非三角化候選亦由補邊歸入。

這排除此特定通用最小性縮減路線，**沒有排除 profile 1**。原完整外側 E
相對的有條件替換、較大界面替換及來源矛盾仍 OPEN。無新來源實現、LP或Lean。

三份 authority 的原 bytes 保存在 frozen/，逐次與 Git BASE 及原檔核對。
證書建立使用 exclusive-create，既有檔不覆寫。

重播：[normal](runs/normal.log)、[seed17](runs/seed17.log)、
[seed17 optimized](runs/seed17-optimized.log)。另有
[外部污染證書拒絕](runs/corrupted-certificate.log)及
[exclusive-write 拒絕](runs/exclusive-write.log)。
