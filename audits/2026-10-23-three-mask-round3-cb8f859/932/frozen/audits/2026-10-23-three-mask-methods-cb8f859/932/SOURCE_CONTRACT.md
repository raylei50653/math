# 932 原 C9 第二層：固定來源合同

本輪 BASE 為 `cb8f8593e273a7426ecadd59797a6e643cc4768e`，只建立本 `932/`
目錄。三份入場時已修改的共享文件在本分工封存前保持原 bytes；不 commit／push。
`INPUTS.json` 與 `ADDITIONAL_INPUTS.json` 記錄 19 份 exact-BASE 輸入，副本在
`frozen/`，正常與 seed17 checker 同時核對 frozen／BASE／目前原檔。
數學 authority drift 永遠 fail closed；共享 routing drift 預設獨立報告，
不撤銷數學裁決。`--check-entry-shared` 另強制入場 dirty bytes 不變；本分工
封存時的兩份 strict receipts 均為零 drift，之後 root 可另行整合文件。

數學來源沿用 T2：G 在全部完整 C5 relation 位於 K132 外的 disk 圖中，
先最小化原內點數 k，再最大化邊數。固定同一有序外框
`B=(b0,b1,b2,b3,b4)`、完整 `Σ(G)=932`、`h=4`；不是固定 mask 內另取最小圖。
完整十列及共同色框 `{0,1,2,3}` 為

```text
0 01012    1 01021    2 01023    3 01201    4 01202
5 01203    6 01212    7 01213    8 01231    9 01232
```

原 932 恰接受第 2、5、7、8、9 列。五個原 apex `a_i` 恰接原
`b_i,b_(i+1)`，四個原私人點 `y_i_j` 恰接原 `b_i`。原 annulus、所有
有向面、rotation paths、全部 820 列、每列十個完整 annulus fibres（含空），
以及 full lifts 均凍結不變。`certificate.json` 的 20 份 `case_bindings`
逐一綁定完整原 case 的 SHA256；沒有獨立正規化附件或色列。

記原 induced C9 在其原方向上的次序為 `C=(c0,...,c8)`，每個 c 的真實
A／Y 名字由該 query 的 `C9_original_names` 給出；沒有把不同 query 的 c
當成同一來源。令 `H=G-B`，`I=V(H)\C`，`m=|I|=k-9`。對每條原邊
`c_i c_(i+1)`，`t_i` 精確指它在 C 內側的原三角面第三點，不是新添點。
繼承的必要事實是：

1. H 為有限簡單 disk near-triangulation；C 是 induced、所有有界面三角形。
2. 每個 c 的完整 H-degree 至少四；每個 I 點的完整 H-degree 至少五。
   I 不接原 B，故 I 點的 H-degree 與 G-degree 相等。
3. 原內部 C3 cap 空；原 C4 cap 空；原 C5 cap 空或恰為 W5。
4. 原 `t_0,...,t_8` 位於 I 且互異；任一 I 點的 C contacts 不含圓周距離二或三。
5. 由前項可得每個 I 點至多三個 C contacts；三接點恰為
   `A_i={c_i,c_(i+1),c_(i+5)}`。**這項分類已在 T2 §5，不是本輪新成果。**

本輪只推進不同 `A_i` 的同時嵌入、原面辨識、兩個 C6 cell 與封閉耳點論證。
沒有改變原完整色關係或任何來源頂點；沒有對一般內側大小設上界。

現行另有 C4 來源橋給共同 `k≥23`，見凍結的
`frozen/docs/tasks/c5_no4ct_handoff.md`。因此本輪局部耳點推得的 `k≥19`
及三接點時 `k≥20` **不提高現行全域下界**；其作用是記錄更精確的原第二層結構。
該 C4 結果及其外部枚舉信任是繼承 authority，本輪沒有重播外部計算。

本 checker 不提供任意來源 `--source` 接口；此旗標及未支援的具名來源提案
一律由 argparse 拒絕。兩個新圖只校準 degree／contact／disk 前提，未給定
完整原 G、原 B 與 `Σ=932`、全域最小性，因此完整來源狀態為 `not triggered`。
