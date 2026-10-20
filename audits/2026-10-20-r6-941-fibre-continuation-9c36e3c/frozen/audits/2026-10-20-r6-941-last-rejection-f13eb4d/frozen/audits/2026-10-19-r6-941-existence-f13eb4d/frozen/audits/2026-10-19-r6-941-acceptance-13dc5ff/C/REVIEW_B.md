# C 對 B 的獨立審查

審查 `B/PROOF.md`、`B/check.py`、`B/certificate.json`、
`B/cap-lifts.json`，不修改其數學證據。量詞採完整原 r6／941、原
`h=ell` 五度位置，保留同一 G 與原字面框，沒有移入 active-f matching。

結論：`d_G(n)=5 => d_G(a)>=7` 及 `dist_G(t,R)>=3` 的紙面化約與
有限證書通過。它們沒有完成 Q1／Q2 的同候選拒絕，也不排除 n 五度本身。

* 原 n link 的已知連續鄰點為 a,p,h,R；五度恰補唯一 u。
  u 對舊 rim 的 aliases 由 induced C10 排除；對已刪 cap 的 aliases
  分別由原 link 互異、nb 非邊及完整 x,y,r stars 排除。因此新框
  `(a,u,R,L,q,c,s,v,w,t)` 是同一實際 disk 的簡單十圈。
* a=6 時，原 a 已失 b,p,y，剩 t,n,u 三點，旋轉確實迫原邊 ut。
  此邊留在新 F 中；將 u=t 的完整 fibres 置零有真來源邊權威。
  程式並未把新十圈擅自當成 induced。
* 七個 cap 點全部列出，n 的第五條邊 nu 沒有遺漏；兩側不存在私有交叉
  附件。原框固定，core 內點數為 `(k+5)-7-10=k-12`；這不是已完成的
  C5 候選，B 也沒有據此聲稱嚴格較小 bad。
* C 另以 26 條直接原邊獨立枚舉全部 2461 份 core 左／右 cap，
  重建 2352 份完整 joint assignments。為避免重用 B 的階乘除法，
  C 將每一份完整 17 元組按固定原 C5 字面框統一換色，再以完整元組
  去重，得到相同全部十列矩陣。canonical JSON 的矩陣 SHA256 是
  `689e2a78ed705e5b7fa902449fa172d265490956fb00e85df6308ae9ed546008`。
  因此未用顏色 stabilizer 的整除在獨立固定框算法下也成立。
* 交換閉包每輪 witness 只引用前一輪空格；a=6 分支最後 756 格的
  alpha 係數逐一為零。n=5 一般分支仍有 36 個 alpha 正格，B 沒有
  將其誤稱來源實現或完整正計數控制。
* 共同鄰 z 必為舊核心私有點。五圈 `(t,a,n,R,z)` 的 pocket 在 D10
  有界內側；a,n 的 core 鄰點皆困於該 pocket。空填的三條其他候選
  對角線都是舊 C10 chord，僅 z 扇形可用；W5 例外也逐項保留。
  兩種情況都給原 a=6,n=5。再逐項排除已刪六個 cap 點是共同鄰，
  故距離結論確實量化原 G，而非只量化核心。

實際執行
`python3 -B audits/2026-10-19-r6-941-acceptance-13dc5ff/B/check.py`
成功，八項負控制全部拒絕。獨立直接邊／固定框去重重建也成功。

審查時另要求首段用 `d_G(p)=d_G(h)=5，h=ell` 明寫原五度身份，
避免簡寫 `p=h=ell=5` 被誤讀為點識別；此為記號澄清，不影響上述
完整 stars、相異點、cap 矩陣或有限排除。

舊 allK 控制不帶本分支的新私有 u／新 F fibres，故 n=5 證書對它
是 not triggered。B 保留此界線，沒有據此聲稱一般控制或來源已被排除。
