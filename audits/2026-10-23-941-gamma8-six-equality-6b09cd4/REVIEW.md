# 論證與範圍核對

2026-10-23；此為本輪自行逐項核對，沒有另行代理審查。

- 六點等號的點集用前輪完整 M2／m 星等號得出；p_d、p_x 是同一外側
  的不同實際 K2 出口，沒有令它們等於其他舊面角色。
- m 的原五度 link 按 rotation 固定後，只保三種原色型。含 M0 的兩型
  以完整原星、原 Jordan 圈及原同色非邊的最多二共鄰排除，非局部度數推全度數。
- u／y 的可能框鄰點 U 由完整 J−K rootless 支及原 K 唯一框接點得出。
  沒有把 rootless N 說成其全部鄰點私有；U 框例外完整保留。
- Uu／Uy 的存在用被原面固定的 cyclic link 與同色 K2 點不能相鄰；
  未使用 U 的完整 cyclic link 或把其 F-link 當 cyclic。
- u∈E 時 Uu 會合併 C、E，故排；E 是否碰框完全無關。d=U 別名另行
  核對，不把不同名頂點假定永久相異來避開例外。
- M={T,m} 用完整 M02 連通及 M2={m}，不是從某個限制圖的連通分量推得。
- 六份 u-link 及48份 L／R y-link 只是必要限制，尚未接合完整外側 disk、
  B14、原來源、全部原 stars 或原八配對。原完整 fibres／空列／full lifts
  保存在前輪整份證書中；本輪未重算全部 caps。
- checker 用例外拋出作 fail-closed，正常及 `-O`／seed17 均會檢查；
  正式 certificate exclusive-create，19項語義及2項外部反控制見重播紀錄。

## 傳播核對

Closure scope：只排「j=2、完整 M2 非空、|X|=6、m∈E」及該六點型的 d=U
子支；另排「M2 空、T 六度、|X|=5、d=U」子支。未完成 C 側六點接合。
Canonical Source + Evidence：[PROOF](PROOF.md)、[certificate](certificate.json)、
[check.py](check.py)、[VERIFICATION](VERIFICATION.json)。

Updated：Kempe 導覽的相關現況／停止點及 STATUS 直接索引，指向本輪報告。
Reviewed-unchanged：直接父問題的11整型、一般 Γ8、wrong-side、八配對及941
仍 OPEN；共同 k≥23、W7的38／40、J1／J2、較小 bad 與 Lean 狀態不變。
前輪8份直接 authority 及490份前輪輸出全部不改寫；前輪當時的 OPEN 記錄
保留，後續範圍由目前導覽與 STATUS 索引說明。
Remaining OPEN：C 側六點型的完整 U 接合；空 M2、T 六度、d≠U 的 L／R
五點接合；更多內點、較長 Γ 及父來源問題。
Propagation stop：L2。新條件排除未改變父問題的 OPEN／CLOSED；HANDOFF
研究線及 tag 不變，README／共通語言無新命題需要更新。全樹 DocGraph 不作
整體 PASS 宣稱；只記實際執行的正式文件範圍檢查。
