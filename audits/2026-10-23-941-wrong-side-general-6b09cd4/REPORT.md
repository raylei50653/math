# 一般 wrong-side：全路割點、C 原橋與 b=c 子支排除

2026-10-23；BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
承接 [同一 P／B13](../2026-10-23-941-p-b13-6b09cd4/REPORT.md)，保同一原圖、
字面框、完整分量與所有空 fibres／full lifts；不再限 Γ8 或恰二內點。

**新排除：全局恰二真交且 P 的最後 K 出口後 b=c 時，兩 patch 不能共 b3。**
先證共同 b3 必是完整原 B13 的不可避 Y/b 割點，再用原 boundary 路
Y–q–c 迫 b3=q。真的改選同一 B 的這條路後，Γ 在 q 使用 F 的兩條
boundary 邊，q 的所有 F 實際面都在 Γ 同側，與兩 patch 中心一內一外矛盾。
這不需要 q 的 cyclic link 或度數，也不借用 G 在 F 外的面。
由同一簡單 P 的 h∈P[r,b]、終點 c，另有 h=c⇒b=c，故亦涵蓋此身份情況。
反向 b=c⇒任意 S 都有 h=c 未採用。

任意 Γ 長度、任意內點數還新增兩個全路結論。固定同一 B13 路 S 後，
每條 C 的 r→e 路 L 所構 Γ 的內部中心都恰為同一 β(p,n) 上的中心，所以
可固定一內一外兩 patch 再改 L。它們若共原01邊，該邊是完整 C 的 r/e
橋；若共13邊，只能是同一最後 C 橋 e–W*，boundary Yq 情況亦排。
共 k0／非端點 b1 的 C 割點結論由恰二真交推至任意真交數。

恰二真交若共 b3，該點更隔開完整 B 的全部 B∩C 與 b。若共同點私有，
b 所在 B 刪點後附枝無任何 B14 接點；若為 q，c 的框例外保留。這是精確
必要幾何，不是完整來源實現。共 k0／b1、兩 patch 不共點、b≠c 的共 b3
及四次以上真交仍未全排。E rootless、W*=q、h=c、重複共點與任意原度數保留。

[PROOF](PROOF.md)含量詞與 boundary 例外的全稱紙證。
[certificate](certificate.json)／[checker](check.py)以三份具名13圖、兩份12圖
及兩份實際三角化 disk 作獨立校準；boundary q 三個面全同側，內點 q
反控制則兩側各二面。逐條簡單路交集獨立對照刪點／刪邊 reachability。
11份破損反控制均拒絕。這些固定圖不是941來源，來源觸發仍 `not triggered`。
54份 authority 與完整舊 fibres／lifts 凍結於 [INPUTS](INPUTS.json)，原 cap
未重算；正常／seed17／負控制及前輪局部重播見 [VERIFICATION](VERIFICATION.json)。

```sh
python3 -B audits/2026-10-23-941-wrong-side-general-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-wrong-side-general-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-wrong-side-general-6b09cd4/check.py --negative
```

下一窄義務：一般長 Γ 的 C 割點／原橋能否接完整原 stars；共 b3 僅餘
b≠c 的完整 B 附枝；四次以上保兩個不同 K2∩Q 及原標記次序。
一般 wrong-side、B側、初始八配對、941／W7／J1／J2、較小 bad、Lean、
matching 仍 OPEN；共同 k≥23 不變。本輪只寫此專屬目錄，未 commit/push。
