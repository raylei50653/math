# 932 round3：原距四雙接點共同嵌入合同

BASE `cb8f8593e273a7426ecadd59797a6e643cc4768e`。唯一寫入範圍為本`932/`
子目錄；不改前兩輪、共享文件、他人產物或Lean，不commit／push。
[INPUTS.json](INPUTS.json)凍結18份immutable exact bytes／SHA，另保留六份routing
入場快照；immutable live drift fail closed，live routing drift獨立報告。

來源是全部完整C5 relations位於K132外的disk圖中，先最小化原內點數k、再
最大化原邊數的同一原G，完整Σ(G)=932、h=4。不是932內局部最小圖。
十列完整原B順序為

`01012 01021 01023 01201 01202 01203 01212 01213 01231 01232`。

932接受零起算第2、5、7、8、9列。保留原有序B、五個A、四個Y、原induced
C9、attachments、全部原有向面／rotation與所有full lifts、空fibres。
二十份case按query_id、完整canonical SHA、原C9真名逐份綁定；不同case的c_i
不是同一原點。原820列順序不變。本輪不重跑舊180項三接點證書。

繼承T2的原d_H(C)≥4、d_H(I)≥5、接點距離只可能1或4；原C3／C4 cap空，
原C5空或W5。第二輪已排所有三接點，因此九個原面第三點恰各接原邊兩端。
本輪證明所有距四二接點只可能落在一種pair P_i={c_i,c_(i+4)}，該pair至多
兩個原中心；若有兩個，原中心邊被迫存在。得到每case19份必要接觸模板，
共380份；不宣稱這些模板都有原來源。

同一原H的單／雙中心C6／C7分解保留原頂點、原邊、原color anchors、完整
空／非空fibres及全full lifts。固定不同色anchors時是兩個outer products
之和，不能借用三色anchor時的rank-one rectangle。本輪沒有count cone、
無條件row deletion、source realization或新較小patch。

兩個具體控制圖只有局部degree/contact/cap與full-lift接合前提，沒有原B、
完整Σ932、全域最小性；完整來源一律`not triggered`。checker不接受`--source`；
未支援具名來源提案由argparse拒絕。所有語義負控制明列`counterexample`。

一般932、無三接點h=4、h≥5、smaller bad、K∞及Lean仍OPEN，共同k≥23不變。
