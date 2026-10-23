# 空 M2 七資源：T8 等號排除、兩 K 支縮到完整 K8

2026-10-23；Git BASE `6b09cd4f8476ca93af8cb51e3a95a632c3f05fcd`。
固定同一原 G／F、rotation、附件、有序 B14、字面 φ／ψ、完整原分量、
全部空 fibres 與 full lifts；只寫本 exclusive 目錄，未 commit／push。

**空支全 D 有 |Z|≥2D−7、|X|≥2D−6；d=U 時再加一。**
T 的每條完整 link 邊在非 T 側有不同的實際原02面點；它們全在 R∪K，
但本輪沒有把它們預設成 K。扣除 D−3 個已耗用的外側 N 點，只能由
d,x,ζ,U 及餘下 Z 資源供應，得到紙面全稱計數。
特別 **T8 至少九資源、十外點；d=U 時十資源、十一外點**，
排新的七資源等號，連八資源域也排。此計數與既有空支八外點界取較強者。

**D6／七資源的兩個額外點，只能各屬 K0／K2／N1／N3。**
任何新增且不屬 K 的原02點，完整原星至多接兩個連續 T-link N 點及
另一個額外資源，原度≤3<5；因此沒有新 R02，也不能接入新的 R13 分量。
額外 N 點至多接原 N 六圈一點；一 K一 N及兩 N 的完整接合仍 OPEN。

若額外兩點都在 K，六份 N 全星在同一 rotation 上接成簡單 K6或K8。
K6沿凍結的四候選定理作同 H三拒絕列回填，嚴降7／9點，故排除。
餘支必為 **d≠U、額外 K0+K2，完整 K8 collar**；兩 K0、兩 K2及
所有兩 K且d=U子支皆排。K8全星只餘單七度／雙六度兩種 N 度數型，
七內點、八接點、34邊、20份共同實際面；安全替換與同一外側仍 OPEN。

完整紙證見 [PROOF](PROOF.md)。[checker](check.py)獨立核全星／面控制、
21個抽象 K8 cap、兩個完整 K6整圖雙射、全部62個舊 fibres／24空列／104 lifts，
及4096字面六框的四候選完整關係。21個 cap 不是21份原來源實現；
K6完整關係沒有被冒稱適用於 K8。10份直接 authority 的 bytes／SHA零漂移。

```sh
python3 -B audits/2026-10-23-941-gamma8-empty-seven-6b09cd4/check.py
PYTHONHASHSEED=17 python3 -B -O audits/2026-10-23-941-gamma8-empty-seven-6b09cd4/check.py --seed 17
python3 -B audits/2026-10-23-941-gamma8-empty-seven-6b09cd4/check.py --negative
```

正常／seed17、13項語義及外部破壞反控制收據見 [VERIFICATION](VERIFICATION.json)。
有限控制為 `triggered and holds`；實際完整來源為 `not triggered`。
沒有新增 Lean、LP、matching 或 K8 安全替換。

空 M2及11型共同至少八外點、非單 M2至少十外點、共同k≥23不變。
下一義務為 D6／七資源的 K0+K2／完整 K8安全候選，以及一 K一 N／兩 N
共同原星。11整型、一般wrong-side、941／W7／J1／J2及一般較小bad仍OPEN。
