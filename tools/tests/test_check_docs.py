"""The guide introduction routes readers without duplicating source status."""

from pathlib import Path
import sys
from tempfile import TemporaryDirectory
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from check_docs import check, check_guide_progress


HEADINGS = ("研究概況與閱讀入口", "最新進度")


def guide(summary, milestones=None, heading=HEADINGS[0]):
    text = f"# 研究導覽\n\n## {heading}\n\n" + summary + "\n"
    if milestones is not None:
        text += "\n### 近期里程碑\n\n" + milestones + "\n"
    return text + "\n## 研究契約\n\n這裡是唯一研究契約。\n"


class GuideProgressTests(unittest.TestCase):
    def errors(self, text):
        return check_guide_progress(text, "test_guide.md")

    def test_natural_introduction_needs_no_fields_or_milestones(self):
        for heading in HEADINGS:
            for destination in ("source.md", "source.md#停止點", "#研究契約"):
                with self.subTest(heading=heading, destination=destination):
                    self.assertEqual([], self.errors(guide(
                        f"本線先理解共同接口，再依[研究契約]({destination})接續。",
                        heading=heading)))

    def test_missing_empty_and_link_only_introductions_fail(self):
        for summary in ("", "- [現況](source.md)\n- [契約](#研究契約)",
                        "1. [現況](source.md)", "[現況][source]\n\n[source]: source.md",
                        "<!-- 說明藏在註解裡 -->\n[現況](source.md)"):
            with self.subTest(summary=summary):
                self.assertTrue(any("reader explanation" in error
                                    for error in self.errors(guide(summary))))
        self.assertTrue(any("missing guide introduction" in error
                            for error in self.errors("# 研究導覽\n")))

    def test_explanation_needs_local_markdown_or_section_link(self):
        for summary in ("本線先理解共同接口。",
                        "參考[來源](https://example.com/source.md)。",
                        "參考[資料](result.json)。",
                        "參考[來源](/tmp/source.md)。"):
            with self.subTest(summary=summary):
                self.assertTrue(any("local Markdown source or section" in error
                                    for error in self.errors(guide(summary))))

    def test_code_block_does_not_supply_explanation_or_link(self):
        text = guide("```md\n本線參考[來源](source.md)。\n```")
        self.assertTrue(any("reader explanation" in error for error in self.errors(text)))
        self.assertTrue(any("local Markdown" in error for error in self.errors(text)))

    def test_heading_must_be_unique_and_near_top(self):
        for heading in HEADINGS:
            text = guide("本線參考[來源](source.md)。", heading=heading)
            for duplicate in HEADINGS:
                with self.subTest(heading=heading, duplicate=duplicate):
                    self.assertTrue(any("exactly once" in error
                                        for error in self.errors(text + f"\n## {duplicate}\n")))
            with self.subTest(heading=heading):
                self.assertFalse(any("first 12" in error
                                     for error in self.errors("\n" * 9 + text)))
                self.assertTrue(any("first 12" in error
                                    for error in self.errors("\n" * 10 + text)))

    def test_summary_remains_bounded_in_length(self):
        text = guide("本線參考[來源](source.md)。\n" * 40)
        self.assertTrue(any("exceeds 40" in error for error in self.errors(text)))

    def test_optional_milestone_count_is_not_fixed(self):
        for count in (1, 2, 6):
            for kind in ("list", "table", "paragraph"):
                with self.subTest(count=count, kind=kind):
                    if kind == "table":
                        body = "| 階段 | 來源 |\n| --- | --- |\n" + "\n".join(
                            f"| 第{i}階段 | [來源](source.md) |" for i in range(count))
                    elif kind == "list":
                        body = "\n".join(f"- 成果{i}：[來源](source.md)" for i in range(count))
                    else:
                        body = "\n\n".join(f"成果{i}見[來源](source.md)。" for i in range(count))
                    self.assertEqual([], self.errors(guide("本線參考[契約](#研究契約)。", body)))

    def test_retained_milestones_cannot_be_empty_or_unsourced(self):
        for body in ("", "| 階段 | 來源 |\n| --- | --- |"):
            with self.subTest(body=body):
                self.assertTrue(any("must not be empty" in error for error in self.errors(
                    guide("本線參考[契約](#研究契約)。", body))))
        for body in ("- 已有[來源](source.md)\n- 尚無來源",
                     "| 階段 | 來源 |\n| --- | --- |\n| 一 | [來源](source.md) |\n| 二 | 無來源 |",
                     "已有[來源](source.md)。\n\n另一成果無來源。"):
            with self.subTest(body=body):
                self.assertTrue(any("each 近期里程碑" in error for error in self.errors(
                    guide("本線參考[契約](#研究契約)。", body))))

    def test_wrapped_milestone_item_uses_continuation_source(self):
        body = "- 一份具名成果，\n  證明見[來源](source.md)。"
        self.assertEqual([], self.errors(guide("本線參考[契約](#研究契約)。", body)))

    def test_milestone_table_does_not_make_closing_prose_an_event(self):
        body = ("| 階段 | 來源 |\n| --- | --- |\n| 一 | [來源](source.md) |\n\n"
                "下表依問題列出權威報告；各報告保留當輪數字。")
        self.assertEqual([], self.errors(guide("本線參考[契約](#研究契約)。", body)))

    def test_global_check_still_validates_source_paths_and_anchors(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "README.md").write_text("[研究入口](docs/HANDOFF.md)\n")
            (root / "docs/HANDOFF.md").write_text("- [研究線](test_guide.md)\n")
            (root / "docs/STATUS.md").write_text(
                "[研究入口](HANDOFF.md)\n[導覽](test_guide.md)\n[來源](source.md)\n")
            (root / "docs/source.md").write_text("# 來源\n\n## 停止點\n")
            target = root / "docs/test_guide.md"
            target.write_text(guide("本線參考[來源](source.md#停止點)。"))
            self.assertEqual([], check(root)[0])
            target.write_text(guide("本線參考[來源](source.md#錯誤錨點)。"))
            self.assertTrue(any("missing anchor" in error for error in check(root)[0]))
            target.write_text(guide("本線參考[來源](missing.md)。"))
            self.assertTrue(any("missing path" in error for error in check(root)[0]))


if __name__ == "__main__":
    unittest.main()
