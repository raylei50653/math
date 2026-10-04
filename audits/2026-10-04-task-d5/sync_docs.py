#!/usr/bin/env python3
"""Synchronize accepted D5 scopes while preserving each historical report body."""
import json
from pathlib import Path
import subprocess

from audit_bundle import digest, write

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / 'audits/2026-10-04-task-d5'


def main():
    acceptance = json.loads((BASE / 'final-integration-attempt1/replay_comparison.json').read_text())
    assert acceptance['all_checks_passed'], 'Integrate only accepted final replays'
    assert not (BASE / 'document_changes.json').exists(), 'Do not apply twice'
    baseline = json.loads((BASE / 'baseline.json').read_text())
    updates, prefixes = {}, {}

    def update(rel, transform):
        path = ROOT / rel
        assert digest(path) == baseline['files'][rel]['sha256'], f'Concurrent document update: {rel}'
        old = path.read_text()
        new = transform(old)
        assert old != new
        updates[rel] = (old, new)

    def prepend(rel, prefix):
        def transform(text):
            title, body = text.split('\n\n', 1)
            prefixes[rel] = body
            return title + '\n\n' + prefix + '\n\n' + body
        update(rel, transform)

    a_prefix = ('**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)\n'
                '核對原04／04及root交換、四rotations、actual C/U支援、完整三hub前提，\n'
                '整份C替換逐點保持全部外部，只主張(a,b,u)投影等式；六角色joint不等\n'
                '反例與01202 singleton1／3保持。逐身份ledger為16／20、40／58支援、\n'
                '50／84schedules；原A至A₃正文／artifacts及各輪數字保持當輪語境。\n'
                '未用D₅來源搬運，其他mixed12身份／ε≥3未證；現行入口由Kempe導覽維護。')
    for name in ('c5_excess_two_mixed_core_four_spoke_mixed12',
                 'c5_excess_two_mixed_core_four_spoke_mixed12_01_12',
                 'c5_excess_two_mixed_core_four_spoke_mixed12_01_01',
                 'c5_excess_two_mixed_core_four_spoke_mixed12_04_04'):
        prepend('docs/' + name + '.md', a_prefix)
    b_prefix = ('**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)\n'
                '只接受W933-129／04–12／長face{2,3,4}的指定shared原附件{4}支：\n'
                '六shared身份／八選擇、11tight pairs、連通K=C−v與完整degree握手式，\n'
                '五袋非空／互斥／連通及十對原邊均獨立核對。整份W933-129、整個長face、\n'
                '其他附件及原20／20表保留；B₂／B₃的兩primary閉合仍依前輪證據。\n'
                '以下正文／前綴保持各輪截點，現行具名入口由Kempe導覽維護。')
    for name in ('c5_excess_two_mixed_core_four_spoke_mixed22',
                 'c5_excess_two_mixed_core_four_spoke_mixed22_short_face',
                 'c5_excess_two_mixed_core_four_spoke_mixed22_long_face',
                 'c5_excess_two_mixed_core_four_spoke_mixed22_shared4'):
        prepend('docs/' + name + '.md', b_prefix)
    c_prefix = ('**獨立驗收（2026-10-04，D₅）**：[最終成果固定快照與稽核](../audits/2026-10-04-task-d5/REPORT.md)\n'
                '只新增關閉(CPP-134-1,34,60)、side IDs=(27,1)；九份自身支援配置、\n'
                '27份完整relation組合、contacts次序／原bridges及逐份2↔3 lift雙射均核對。\n'
                '未知w完整relation保持符號纖維；不以整側禁色聯集代替逐分量檢查。\n'
                '連同C₂／C₃合用恰三keys，3500key ledger及原36／140／900表不刪，\n'
                '其餘3497keys未關閉。以下各輪正文／artifacts保持，現行入口由weak-deletion導覽維護。')
    for name in ('c5_mixed_p3_common_endpoint', 'c5_mixed_p3_one_color_ternary_unary',
                 'c5_mixed_p3_two_frame_ternary_unary', 'c5_mixed_p3_two_frame_two_unary'):
        prepend('docs/' + name + '.md', c_prefix)

    def readme(text):
        old = ('正式返回 A₃／B₃／C₃ 的固定快照、獨立驗收及最新停止點見\n'
               '[D₄整合稽核](audits/2026-10-04-task-d4/REPORT.md)。前序\n')
        new = ('正式返回 A₄／B₄／C₄ 的固定快照、獨立驗收、精確scope ledger與最新停止點見\n'
               '[D₅整合稽核](audits/2026-10-04-task-d5/REPORT.md)。\n'
               '[D₄的A₃／B₃／C₃封存](audits/2026-10-04-task-d4/REPORT.md)及前序\n')
        assert old in text
        return text.replace(old, new, 1)
    update('README.md', readme)

    def status(text):
        marker = '| [D₄：正式返回A₃／B₃／C₃快照與整合稽核]'
        lines = text.splitlines(keepends=True)
        index = next(i for i, line in enumerate(lines) if line.startswith(marker))
        lines.insert(index + 1, '| [D₅：A₄／B₄／C₄最終快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md) | 逐身份A ledger降至16／20；B只關閉W933-129長face的shared-{4}支；C只新增geometry34／join60，3500keys及36／140／900表保持。三項最終重播、版本／實際依賴與歷史失敗分別封存；未commit／push |\n')
        text = ''.join(lines)
        marker = '- [2026-10-04：正式返回A₃／B₃／C₃的固定快照與D₄獨立整合稽核](history/2026-10-04-task-d4-returned-integration-audit.md)'
        assert marker in text
        return text.replace(marker, marker + '\n- [2026-10-04：A₄／B₄／C₄最終快照與D₅獨立整合稽核](history/2026-10-04-task-d5-final-integration-audit.md)', 1)
    update('docs/STATUS.md', status)

    def kempe(text):
        marker = '## 4. 閱讀與重播入口\n\n'
        text = text.replace(marker, marker +
            'A₄／B₄已由[D₅固定快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md)驗收：\n'
            'A逐身份16／20及全部保留support／schedules不變；B只登記W933-129的\n'
            'shared-{4}附件支，不刪骨架或長face。十二份producer兩seed byte-check、\n'
            '獨立最終重播與完整scope／版本／runtime inputs見D₅包；D₄封存不改写。\n\n', 1)
        old = ('在此窄支停止；可接續入口是同份W933-129長face的其餘contact附件，\n'
               '須保留這份原frame與七身份，另證其原leaf／bridge機制。')
        new = ('在此窄支停止；下一具名候選入口是同份W933-129、04／12長face{2,3,4}，\n'
               '指定shared頂點的實際框附件為空集；保留原frame、七身份及全部原bridges。\n'
               '此入口未分析、未排除，其他contact附件亦保持。')
        assert old in text
        return text.replace(old, new, 1)
    update('docs/c5_kempe_guide.md', kempe)

    def weak(text):
        marker = '## 4. 重播入口與驗證範圍\n\n'
        text = text.replace(marker, marker +
            'C₄已由[D₅固定快照與獨立稽核](../audits/2026-10-04-task-d5/REPORT.md)驗收：\n'
            '九份逐分量自身支援、27完整relation組合及原bridges／lifts保持。\n'
            '只新增(CPP-134-1,34,60)，連同C₂／C₃恰三keys，另外3497keys未關閉；\n'
            '3500keys與原36／140／900表完整保留，w完整relation仍未知。\n\n', 1)
        marker = '同一 ternary 引理對其他 w 角色的逐份覆蓋也未展開。'
        extra = ('下一具名未稽核入口為 **CPP-134-1／geometry35／join20、side IDs=(8,1)**：\n'
                 '自身支援A_z={b₁,b₂}、A_w={b₂,b₃,b₄}，各側一份ternary unary且無spokes，\n'
                 '禁色分別{0,2,3}／{0,2}。contacts順序及未知完整relations見D₅ scope ledger；\n'
                 '此處只定位原表entry，沒有分析或新增排除。\n')
        assert marker in text
        return text.replace(marker, extra + marker, 1)
    update('docs/c5_weak_deletion_guide.md', weak)

    def synthesis(text):
        title, rest = text.split('\n\n', 1)
        prefix = ('**最終成果獨立驗收（2026-10-04，D₅）**：\n'
                  '[固定快照、scope ledger與版本表](../audits/2026-10-04-task-d5/REPORT.md)驗收A₄／B₄／C₄。\n'
                  'A₄直接核對原04／04與root交換，01202 singleton1／3、完整C替換／外部逐點\n'
                  '保持及投影／六角色joint界線成立；18／22降至16／20，40／58支援與50／84\n'
                  'schedules完整保存，未用D₅來源搬運。B₄只關閉W933-129／04–12／長face{2,3,4}\n'
                  '的shared-{4}附件支；原K的完整degree奇數cut與十對原邊K₅不刪整份骨架。\n'
                  'C₄只新增(CPP-134-1,34,60)，逐份自身支援與完整lifts的2↔3雙射給矛盾；\n'
                  '未知w relation保持，九份配置／27完整組合、3500keys及36／140／900表不刪。\n'
                  '以下各輪數字保留當輪截點；紙面／外部定理／Python／Lean分開。\n'
                  '下一入口僅由兩份導覽維護，mixed12／mixed22整型、ε≥3及一般出口未證。')
        return title + '\n\n' + prefix + '\n\n' + rest
    update('docs/c5_research_synthesis.md', synthesis)

    for rel, (old, new) in updates.items():
        (ROOT / rel).write_text(new)
    history = ROOT / 'docs/history/2026-10-04-task-d5-final-integration-audit.md'
    assert not history.exists()
    history.write_text(
        '# 2026-10-04：A₄／B₄／C₄最終成果的D₅固定快照與獨立整合稽核\n\n'
        '接續[D₄封存](../../audits/2026-10-04-task-d4/REPORT.md)，完成\n'
        '[D₅固定快照、獨立稽核與文件整合](../../audits/2026-10-04-task-d5/REPORT.md)。\n'
        '起始2794份檔案SHA256、1383份凍結輸入、實際runtime依賴與版本分別保存。\n\n'
        'A₄原04／04及交換的四rotations／三hub、完整C替換與01202 singleton1／3\n'
        '獨立核對，逐身份18／22降至16／20；六角色joint不等反例保持。\n'
        'B₄只驗收W933-129／04–12長face的shared附件{4}支，六shared身份／八選擇、\n'
        '11tight pairs、完整degree奇數cut與五原bags／十對原邊成立；骨架不刪。\n'
        'C₄只新增(CPP-134-1,34,60)、side IDs=(27,1)；九份自身支援配置及27份\n'
        '完整relation組合逐分量排除，原bridges／未知w relation及36／140／900表保持。\n\n'
        '十二份producer default／seed17共24份byte-check及兩份A₄ helper重算通過，\n'
        '三項最終獨立重播／雙seed比較通過；既有lake build通過，無新Lean theorem。\n'
        '原四份文件hash漂移與D₄及更早成功／失敗紀錄均保持，不刷新舊證書。\n'
        '本輪adapter／版本表失敗與全部來源bytes亦保存；最終文件、DocGraph、artifact、\n'
        'diff、保存及交付封存結果和實際命令見D₅報告。\n\n'
        '停止於三項條件式驗收與整合。下一具名未稽核入口由\n'
        '[Kempe](../c5_kempe_guide.md#3-停止點與保留缺口)及\n'
        '[weak-deletion](../c5_weak_deletion_guide.md#3-精確停止點與下一個窄問題)維護。\n'
        '未擴張研究，未commit／push；mixed12／mixed22整型、ε≥3、來源實現、一般\n'
        '出口及K∞=K≤5仍未證。\n')
    rows, diagnostics = [], []
    patches = []
    for rel, (old, new) in updates.items():
        rows.append({'path': rel, 'before_sha256': baseline['files'][rel]['sha256'],
                     'after_sha256': digest(ROOT / rel),
                     'historical_body_preserved': new.endswith(prefixes[rel]) if rel in prefixes else None})
        proc = subprocess.run(['git', 'diff', '--no-index', '--check', str(BASE / 'snapshot' / rel), str(ROOT / rel)],
                              capture_output=True, text=True)
        diagnostics.append({'path': rel, 'exit_code': proc.returncode, 'stdout': proc.stdout,
                            'stderr': proc.stderr, 'passed': proc.returncode in (0, 1) and not proc.stdout and not proc.stderr})
        diff = subprocess.run(['git', 'diff', '--no-index', str(BASE / 'snapshot' / rel), str(ROOT / rel)],
                              capture_output=True, text=True)
        patches.append(diff.stdout)
    (BASE / 'integration_doc_changes.diff').write_text(''.join(patches))
    write(BASE / 'document_changes.json', {'existing_documents_changed': rows, 'count': len(rows),
          'new_history': str(history.relative_to(ROOT)), 'new_history_sha256': digest(history),
          'historical_report_bodies_preserved': all(r['historical_body_preserved'] is not False for r in rows),
          'HANDOFF_unchanged': digest(ROOT / 'docs/HANDOFF.md') == baseline['files']['docs/HANDOFF.md']['sha256']})
    write(BASE / 'checks/document_diff.json', {'all_checks_passed': all(r['passed'] for r in diagnostics),
          'records': diagnostics, 'exit_code_policy': 'no-index exit1 means differences, not whitespace failure; diagnostics must be empty'})
    assert all(r['passed'] for r in diagnostics)
    print(json.dumps({'updated_documents': len(rows), 'new_history': 1, 'historical_report_bodies_preserved': True}))


if __name__ == '__main__':
    main()
