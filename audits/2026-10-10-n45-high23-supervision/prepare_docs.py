#!/usr/bin/env python3
"""Prepare a reviewable propagation draft from the saved shared-before files."""
from pathlib import Path

OUT = Path(__file__).resolve().parent


def replace_once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new, 1)


def main():
    paths = [
        "docs/c5_excess_two_nonadjacent_unit_core45.md",
        "docs/c5_kempe_guide.md",
        "docs/STATUS.md",
        "docs/c5_phase_b_common_lemmas.md",
        "artifacts/c5_excess_two_e4/REPORT.md",
    ]
    texts = {p: (OUT / "shared-before" / p).read_text() for p in paths}
    source = paths[0]
    text = texts[source]
    text = replace_once(text,
        "完成完整 H1–H13 內的限定採納。\n",
        "完成完整 H1–H13 內的限定採納。\n"
        "後續 [HIGH2](../audits/2026-10-10-n45-s-high2/REPORT.md)經\n"
        "[H2A 紙面／覆蓋](../audits/2026-10-10-n45-h2a/REPORT.md)、\n"
        "[H2R 原圖／完整 lifts](../audits/2026-10-10-n45-h2r/REPORT.md)、\n"
        "[H2C 工具／封存](../audits/2026-10-10-n45-h2c/REPORT.md)及\n"
        "[HIGH2／HIGH3 監督驗收](../audits/2026-10-10-n45-high23-supervision/REPORT.md)，\n"
        "在完整契約內採納；未用色接回構造明限 proper 三色列，原過寬量詞保留 finding。\n"
        "[H3A](../audits/2026-10-10-n45-h3a/REPORT.md)、\n"
        "[H3R](../audits/2026-10-10-n45-h3r/REPORT.md)、\n"
        "[H3G](../audits/2026-10-10-n45-h3g/REPORT.md)獨立核回完整 HIGH3 契約到 BASE no-spoke 排除，\n"
        "由同輪監督採納；兩支與既有 HIGH1／LOW 合成的精確覆蓋見§2.8。\n")
    text = replace_once(text,
        "HIGH2／HIGH3、long等其餘必要化約不宣稱實現或排除。N2、45／54 全型、原55及猜想 E 均仍 OPEN。",
        "**N45-S-HIGH2／HIGH3 已排除：** 原 U 在 s 的 incidence／s-spokes 為(2,1)／(3,0)，\n"
        "各自完整契約與 X=M 保留；HIGH2 未用色構造限定三色列，HIGH3 接回 BASE no-spoke (3,2)。\n"
        "HIGH1–HIGH3 窮盡限定 HIGH；與 LOW 合成，**§1 精確 S 身份的兩 short 分支已全排**。\n"
        "含 long、其他45／54身份、原55、無45／54來源、一般 N2／E及ε≥3均仍 OPEN。")
    text = replace_once(text,
        "限定 LOW 已由 LOW1／LOW2 覆蓋排除；HIGH1另經完整契約排除，HIGH2／HIGH3仍OPEN",
        "限定 LOW／HIGH 分別由 LOW1–LOW2／HIGH1–HIGH3 覆蓋排除；只關§1精確 S 的兩 short 分支")
    marker = "\nU-CAP 恢復原 U"
    pos = text.find(marker)
    assert pos > 0
    table_add = (
        "| HIGH2-CORE／COMP／JOIN／RESTORE／F／K33／ARC／MAP／BRIDGE／SPLIT／PALETTE | "
        "原雙 U-contact／single s-spoke；完整(2,2)接合保 r fibres，原 O′ 補 K₃,₃、完整 W 支援及 rooted assignments 成立 | "
        "全部 H1–H13；H2A／H2R 紙面核對，H2C 只核工具，原錯量詞另列 finding |\n"
        "| HIGH2-EXCLUSION（精化） | 每 proper 三色 γ 在原 U 三點 T 見三色時，原 r=s=Dγ 的完整 G lifts 含恢復 e；Q(G)⊆B−T，故至多兩拒點 | "
        "只縮窄接回構造的 γ 量詞；JOIN／RESTORE／PALETTE 仍保全部 proper γ；不改原 worker |\n"
        "| HIGH3 scoped exclusion | X自己 minimal、s無spoke、實際 C/U contacts=(2,3)，完整覆蓋迫三接點 U 至少兩禁色；原 X K₅ 排除 | "
        "完整 K1–K13；H3A／H3R／H3G 獨立核 BASE no-spoke §§1–3、5，無新充分前提 |\n"
        "| S-SHORT scoped composition | §1精確 S 的 LOW兩支與 HIGH三支互斥窮盡，各自完整契約排除，故兩原 mixed 都 short 的身份不存在 | "
        "H2A及父端核覆蓋；含long、其他core身份、一般N2／E均未關 |\n"
    )
    text = text[:pos].rstrip() + "\n" + table_add + text[pos:]
    section = """
### 2.6 N45-S-HIGH2：原雙 contact 與恢復 e 的 G lifts

只取§1精確 S 身份，另有原 U 只接 s 的兩個相異 contacts、無 U–r；
P/Q 支援真框邊、(m_r,m_s)=(3,2)。原 r 兩 spokes 只刪 e=rb_i 留 rb_j，
s 唯一 spoke sb_k 全留；U/P/Q 全原邊、原 cycle 及全部 assignments 保留。
X=G−e=M 自己是 β inclusion-minimal45／54 core。完整 H1–H13逐字見
[HIGH2 原交付](../audits/2026-10-10-n45-s-high2/REPORT.md)。

H_X−s恰C={r}∪P∪Q及U、contacts(2,2)。全部 proper literal γ、ambient tuples、
r/s pins及空 fibres 的完整 restriction／union保留原 r 投影；G 只再加 r≠γ(b_i)。
X自己的 minimality／incident-edge witnesses與局部 N-diagonal迫C/U禁色角色(1,2)。
原 U-critical-contact witness先證盾長≥2；P/Q共端且等於唯一s-spoke端點時，
原 O′=(B−v)∪U的六 bags 九鄰接補齊 K₃,₃，故兩支援邊頂點互斥。
原 U support因而恰連續三點 T，C碰 T 外原框點；這些均在原 G／X 各自原邊中核對。

同一 U 的雙拒 palettes給奇數原 bridge 路徑，每個完整旁支塊 W 必見兩供應色。
任意兩 W 的 frame-arc原五 bags／十鄰接及鴿籠原理迫該路徑恰一原邊，
兩完整 W 的 actual supports為 T 左右真框邊；W大小仍無上界。
β完整交換pair關係先證兩 W 的完整 rooted assignments可取色恰其支援pair補集；
再用實際附件的色等變，在同一 γ 框保全部 W assignments及原 bridge接合。

**採納的量詞精化。** JOIN／RESTORE／PALETTE仍對全部 proper γ成立；
未用色接回構造只對 **proper 三色 γ**：若 T看到其三個已用色，取兩 W 的完整
assignments並置原 r=s=Dγ，P/Q的完整 N-diagonal lifts接回原 G，包含恢復 e。
所以 singleton三色拒點 Q(G)⊆B−T、至多兩點，矛盾完整933四拒點／941三拒點。
原文§8及H2-EXCLUSION將此構造寫成所有 proper γ，四色列可能在 T見三色卻無未用Dγ；
兩 paper稽核及父端保此 finding與四色literal witness。四色列的接受原由H2的T4前提保證。
原worker及其封存不改，不採納過寬接回量詞；主排除範圍仍是完整 H1–H13。

[H2A](../audits/2026-10-10-n45-h2a/REPORT.md)與[H2R](../audits/2026-10-10-n45-h2r/REPORT.md)
獨立裁紙面／原圖及全部 fibres；[H2C](../audits/2026-10-10-n45-h2c/REPORT.md)只裁封存與有限工具。
這是任意大小 paper＋BASE＋明列外部 Gallai，沒有 finite HIGH2 source、trigger數或新Lean。

### 2.7 N45-S-HIGH3：原 X 的 no-spoke (3,2) 排除

只取§1精確 S 身份，原 U在s恰三個相異contacts且無U–r，s無spoke；
P/Q真框邊支援、(m_r,m_s)=(3,2)，r兩spokes只刪e留rb_j、X=M自己minimal。
全部原件與具名ordered/shared資料、十列完整 relations、空fibres及孤立自由因子保留；
[完整K1–K13](../audits/2026-10-10-n45-h3a/frozen/authority/common-contract.md)限制本輪採納範圍。

X的唯一完整degree5點是s，其餘有效原內點degree4；H_X−s實際分量恰C={r}∪P∪Q與U，
ordered contacts數(2,3)。完整同列接合、X自己的minimality及slack給F_C∪F_U=Col、
各private非空、|F_C|≤2，從而|F_U|≥2；不預設指定禁色角色。
原拒絕三色β以一次共同整圖D5／S4搬到q，逐前提接回BASE no-spoke §§1–3、5的(3,2)來源排除。
避整U的s–P–r–rb_j原路恢復外hub；U的K4-free、active triangle、任意／零長arms及原tethers
給五個互斥連通bags及十原鄰接，Z–O用另一分量的原s-contact；全部在X、不用省略e。
這是原X非平面反證，不是X指定延拓提升成G，也不是必要表項的來源實現。

[H3A](../audits/2026-10-10-n45-h3a/REPORT.md)、[H3R](../audits/2026-10-10-n45-h3r/REPORT.md)、
[H3G](../audits/2026-10-10-n45-h3g/REPORT.md)各自獨立核回，父端另核原圖／全lifts及封存。
任意大小結論依賴BASE及外部Gallai；抽象toy／bags只校準語義，無有限HIGH3來源或新Lean。

### 2.8 限定 HIGH 與兩 short S 身份的完整覆蓋

在§1精確S身份的两原mixed都short時，已採納S05／S06迫唯一原U、兩mixed真框邊支援，
unary側／另一側mixed incidence=2／3。LOW已由§2.4的兩支窮盡排除。
HIGH令u為原U在s的contact數、t_s為原s-spokes，完整degree5给2+u+t_s=5，
u≥1、t_s≥0，故(u,t_s)恰(1,2)、(2,1)、(3,0)。原r三mixed+兩spokes中只省略e。
這三支逐項滿足HIGH1／HIGH2／HIGH3的各自完整契約、X自己β-minimal性及所有同源資料。
它們互斥窮盡，不另加入充分前提，也不從G遺傳X minimality。

[H2A覆蓋稽核](../audits/2026-10-10-n45-h2a/REPORT.md)與
[父端接受紀錄](../audits/2026-10-10-n45-high23-supervision/acceptance.json)核回三支及LOW／HIGH合成。
故只關 **§1精確S身份的兩原mixed都short分支**；含long、其他省略／core身份、原55、
無45／54來源、一般N2／E及ε≥3仍OPEN，沒有新增有限來源或Lean。

"""
    open_start = text.index("## 3. 精確 OPEN 與下一個窄分支")
    evidence_start = text.index("## 4. 證據、重播與保留失敗")
    text = text[:open_start] + section + """## 3. 精確 OPEN 與下一個窄分支

§1指定整U省略身份已由§2.2全排；精確S身份的兩short分支已由§2.8全排。
目前S殘留至少有一份原long mixed；既有S05只給原unary至多一份，不給long來源排除。
下一個窄入口先選取保留完整原U／long／short及spoke省略身份的同源原支援／完整跨列joint核對；
此選定分支並非所有含long殘留的完整分類。
先從已有原盾弧費與zero-slack義務立契約，不擴graph/k或重開已採分支。
這個殘留尚未派新worker；具體任務須保X=M自己minimal、原contacts／attachments／rotation、
同一literal框、r/s全pins、完整relations／空fibres及恢復e條件，不能沿用整U刪除的圖類映射。
其他45／54身份、原55、無45／54來源、一般N2／E及ε≥3均仍OPEN。

""" + text[evidence_start:]
    text = replace_once(text, "## 4. 證據、重播與保留失敗\n",
        "## 4. 證據、重播與保留失敗\n\n"
        "本輪HIGH2完整118 regular=115payload＋3 exact top-level metadata、41inputs／8pins於採納前核回；\n"
        "HIGH3三份完整tree、receipts及父端normal／seed17重播亦核回。H2C獨立有限重算只校準toy／工具，\n"
        "H2A／H2R與父端共同保proper三色γ精化finding；封存不裁無界paper。\n"
        "同期新增audit造成的原outside custody FAIL、四nested-repository directory markers只核presence的界線、\n"
        "歷史62duplicate-ID／BASE缺檔／E4provenance FAIL均保留；不宣稱完整worktree零漂移。\n"
        "本輪共享文件採納後，舊live-current pins不再是重播入口；原worker／reviewer bytes不改。\n"
        "凍結證據、允許五shared變更及當前文件的只讀入口：\n\n"
        "```sh\npython3 -B audits/2026-10-10-n45-high23-supervision/verify.py\n"
        "PYTHONHASHSEED=17 python3 -B audits/2026-10-10-n45-high23-supervision/verify.py\n```\n\n"
        "此入口核artifact／採納custody，不以tool證paper；完整範圍見[監督報告](../audits/2026-10-10-n45-high23-supervision/REPORT.md)。\n")
    texts[source] = text

    guide = paths[1]
    text = texts[guide]
    start = text.index("BASE／外部Gallai、paper與toy分層，沒有新HIGH1有限來源或Lean。HIGH2／HIGH3、long與一般N2／E仍OPEN。")
    end = text.index("精確N2目標45／54控制仍0觸發", start)
    text = text[:start] + """BASE／外部Gallai、paper與toy分層，沒有新HIGH1有限來源或Lean。
**HIGH2／HIGH3與限定兩short覆蓋（2026-10-10）：**
[監督驗收](../audits/2026-10-10-n45-high23-supervision/REPORT.md)採納完整HIGH2／HIGH3契約。
HIGH2保雙U-contact／cycle、全部r fibres與恢復e，原兩W完整assignments給三色列的原G lifts；
未用Dγ構造明限proper三色γ，原「全部properγ」過寬量詞由H2A／H2R及父端保finding，原worker不改。
HIGH3原s無spoke、實際C/U=(2,3)逐項接回BASE no-spoke原K₅排除。
在上述限定HIGH身份中，原U incidence／s-spokes只有(1,2)/(2,1)/(3,0)，由HIGH1–HIGH3窮盡；加LOW兩支，
[§1精確S身份的兩原mixed都short分支](c5_excess_two_nonadjacent_unit_core45.md)已全排。
目前窄殘留為S含至少一份原long；尚未發布新long worker，不擴枚舉。
原[HIGH2派工](history/2026-10-10-n45-high1-adoption.md)保留當輪語境；
兩支的採納／finding／完整tree與custody界線見[本輪紀錄](history/2026-10-10-n45-high23-adoption.md)。
來源paper依BASE／外部Gallai，無新finite來源或Lean，其他cores／一般N2／E仍OPEN，傳播停止L2。
""" + text[end:]
    texts[guide] = text

    status = paths[2]
    text = texts[status]
    text = replace_once(text, "更新：2026-10-10（HIGH1完整契約限定採納）。", "更新：2026-10-10（HIGH2／HIGH3與限定兩short S覆蓋採納）。")
    text = replace_once(text,
        "指定整U省略X=M身份已全排；LOW1／LOW2合成全排§1精確S-SHORT-U-LOW；HIGH1完整H1–H13另已排；HIGH2／HIGH3、long、其他cores及一般N2／E仍OPEN；HIGH2八pins已備未啟動",
        "指定整U省略X=M身份已全排；LOW兩支／HIGH三支窮盡，全排§1精確S的兩原mixed都short身份；HIGH2三色γ量詞精化保finding；含long、其他cores／原55及一般N2／E仍OPEN")
    text = replace_once(text,
        "只採完整HIGH1；下一原U雙contact在s／sole spoke、實際(2,2)完整join與r色fibres；八pins與全文已備未啟動，HIGH3／long及一般N2／E仍OPEN，停止L2",
        "保當轮HIGH1採納／HIGH2八pins及完整派工；HIGH2／HIGH3後續已限定採納並核兩short覆蓋，見最新紀錄；歷史正文不改")
    text = replace_once(text,
        "後續限定LOW已由LOW1／LOW2全排，HIGH／long仍OPEN；來源控制0觸發，文件FAIL保留",
        "後續LOW／HIGH五支合成全排§1精確兩short S身份；含long仍OPEN；原來源控制0觸發，文件FAIL保留")
    marker = "| [N45-S-LOW2交付]"
    pos = text.index(marker)
    rows = """| [HIGH2交付](../audits/2026-10-10-n45-s-high2/REPORT.md)、[H2A紙面／覆蓋](../audits/2026-10-10-n45-h2a/REPORT.md)、[H2R原圖／lifts](../audits/2026-10-10-n45-h2r/REPORT.md) | 完整H1–H13排除採納；原O′／W支援與全assignments恢復e；未用色構造限定proper三色γ，原過寬量詞保finding，JOIN／RESTORE／PALETTE仍全properγ |
| [H2C封存／有限](../audits/2026-10-10-n45-h2c/REPORT.md)、[HIGH2／HIGH3監督](../audits/2026-10-10-n45-high23-supervision/REPORT.md) | 115payload／3exact metadata、41inputs／8pins及完整receipts核回；toy不裁paper；同期outside custody FAIL／62duplicates與historical FAIL保留，無完整worktree零漂移宣稱 |
| [H3A前提](../audits/2026-10-10-n45-h3a/REPORT.md)、[H3R完整關係](../audits/2026-10-10-n45-h3r/REPORT.md)、[H3G原K₅](../audits/2026-10-10-n45-h3g/REPORT.md) | 完整K1–K13的HIGH3任意大小排除採納；X自己minimal、原s無spoke、實際C/U=(2,3)接BASE no-spoke (3,2)，外路及十原鄰接不用e；無新來源或Lean |
| [HIGH2／HIGH3採納與覆蓋](history/2026-10-10-n45-high23-adoption.md) | HIGH三支互斥窮盡，加LOW兩支只關§1精確兩short S身份；目前long／其他cores／一般N2／E仍OPEN，尚未派新long worker；五shared同步、停止L2 |
"""
    text = text[:pos] + rows + text[pos:]
    text = replace_once(text,
        "- [2026-10-10：HIGH1限定採納與HIGH2任務](history/2026-10-10-n45-high1-adoption.md)；三獨立稽核已驗收，HIGH2八pins與完整任務已備、未啟動",
        "- [2026-10-10：HIGH2／HIGH3採納、量詞finding與限定兩short覆蓋](history/2026-10-10-n45-high23-adoption.md)；六獨立稽核與父端驗收，停止L2\n"
        "- [2026-10-10：HIGH1限定採納與HIGH2任務](history/2026-10-10-n45-high1-adoption.md)；原派工／pins保當輪語境，後續採納見上列最新紀錄")
    texts[status] = text

    phase = paths[3]
    text = texts[phase]
    text = replace_once(text,
        "與同列未用D的完整G lifts給矛盾；BASE／外部Gallai明列。仍留HIGH2／HIGH3與long，沒有新finite來源或Lean。",
        "與同列未用D的完整G lifts給矛盾；BASE／外部Gallai明列。\n"
        "後續[HIGH2／HIGH3與限定兩short覆蓋](c5_excess_two_nonadjacent_unit_core45.md)\n"
        "另核原雙U-contact、完整W assignments／r fibres恢復e，未用Dγ構造只限proper三色γ；\n"
        "原過寬量詞保finding，全部properγ的JOIN／RESTORE／PALETTE不縮窄。HIGH3原s無spoke、\n"
        "實際(2,3)接回BASE no-spoke原K₅排除。LOW兩支及HIGH三支逐契約窮盡，\n"
        "只關§1精確S的兩原mixed都short身份；含long、其他cores／一般N2／E仍OPEN，無新finite來源或Lean。")
    texts[phase] = text

    parent = paths[4]
    texts[parent] = replace_once(texts[parent], "# 任務 E4：猜想 E 的 ε=2 層，非相鄰雙 degree-5 roots\n",
        "# 任務 E4：猜想 E 的 ε=2 層，非相鄰雙 degree-5 roots\n\n"
        "**後續（2026-10-10，HIGH2／HIGH3及限定兩short S覆蓋採納）。**\n"
        "[本輪監督驗收](../../audits/2026-10-10-n45-high23-supervision/REPORT.md)\n"
        "在[N45各自完整契約](../../docs/c5_excess_two_nonadjacent_unit_core45.md)內排除HIGH2／HIGH3。\n"
        "HIGH2保完整雙U-contact／W assignments與r fibres，原G lifts恢復e；未用Dγ構造明限proper三色γ，\n"
        "原過寬量詞由兩paper稽核及父端保finding。HIGH3原s無spoke、實際C/U=(2,3)接回BASE原K₅排除。\n"
        "LOW兩支與HIGH三支逐契約互斥窮盡，只全排§1精確spoke省略X=M的兩原mixed都short身份。\n"
        "S含long、其他省略／core、原55、無45／54來源及一般N2／E仍OPEN；無新來源或Lean。\n"
        "同期outside custody FAIL、62duplicate-ID及歷史FAIL保留；下列有日期正文與本頁原三列量詞不改。\n")

    for p, text in texts.items():
        draft = OUT / "draft" / p
        draft.parent.mkdir(parents=True, exist_ok=True)
        with draft.open("x") as handle:
            handle.write(text)
    print("prepared five shared-file drafts; no shared files changed")


if __name__ == "__main__":
    main()
