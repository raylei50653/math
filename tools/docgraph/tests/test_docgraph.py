"""Acceptance tests for DocGraph. Run: python3 -m unittest discover tools/docgraph/tests"""
from __future__ import annotations

import contextlib
import io
import json
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from docgraph import render_d2  # noqa: E402
from docgraph.cli import main  # noqa: E402
from docgraph.parser import parse_repo  # noqa: E402
from docgraph.query import show, suggest  # noqa: E402
from docgraph.validate import validate  # noqa: E402


def doc(block: str, body: str = "# Title\n\nText.\n") -> str:
    return "---\n" + textwrap.dedent(block).strip() + "\n---\n" + body


TEMPS: list[tempfile.TemporaryDirectory] = []


def tearDownModule():
    for tmp in TEMPS:
        tmp.cleanup()


class Repo:
    def __init__(self, files: dict[str, str]):
        self.tmp = tempfile.TemporaryDirectory()
        TEMPS.append(self.tmp)
        self.root = Path(self.tmp.name)
        for name, text in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")

    def load(self):
        return validate(*parse_repo(self.root))

    def errors(self):
        return [d for d in self.load()[1] if d.level == "error"]

    def run(self, *argv) -> tuple[int, str]:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            code = main(["--repo", str(self.root), *argv])
        return code, buf.getvalue()

    def snapshot(self) -> dict[str, str]:
        return {str(p): p.read_text() for p in self.root.rglob("*.md")}


TWO_SPOKE = {
    "docs/adjacent.md": doc("""
        docgraph:
          id: c5.two-spoke-adjacent
          family: [c5, c5.two-spoke]
        """),
    "docs/nonadjacent.md": doc("""
        docgraph:
          id: c5.two-spoke-nonadjacent
          family:
            - c5
            - c5.two-spoke
        """),
    "docs/split.md": doc("""
        docgraph:
          id: c5.two-spoke-split
          family: c5.two-spoke   # a scalar is a one-element list
        """),
}


class ValidStates(unittest.TestCase):
    def test_id_only_node_is_valid_and_merely_noted(self):
        repo = Repo({"a.md": doc("docgraph:\n  id: notes.observation")})
        graph, diags = repo.load()
        self.assertIn("notes.observation", graph.nodes)
        self.assertEqual([d.code for d in diags], ["unconnected"])
        self.assertEqual(repo.run("check")[0], 0)

    def test_family_without_dependencies(self):
        repo = Repo(TWO_SPOKE)
        graph, _ = repo.load()
        self.assertEqual(repo.errors(), [])
        self.assertEqual(graph.edges, [])
        self.assertEqual(graph.families["c5.two-spoke"],
                         ["c5.two-spoke-adjacent", "c5.two-spoke-nonadjacent", "c5.two-spoke-split"])
        self.assertEqual(graph.family_members("c5"), ["c5.two-spoke-adjacent", "c5.two-spoke-nonadjacent"])
        self.assertEqual(len(graph.family_members("c5", recursive=True)), 3)

    def test_related_only_and_related_cycle_are_valid(self):
        repo = Repo({
            "a.md": doc("docgraph:\n  id: a\n  related: [b]"),
            "b.md": doc("docgraph:\n  id: b\n  related: [a]"),
        })
        self.assertEqual(repo.errors(), [])

    def test_documents_without_docgraph_are_ignored(self):
        repo = Repo({"plain.md": "# Plain\n", "hr.md": "---\n\ntext\n",
                     "other.md": "---\ntitle: x\n---\n# X\n"})
        graph, diags = repo.load()
        self.assertEqual((graph.nodes, diags), ({}, []))


class Errors(unittest.TestCase):
    def codes(self, files):
        return sorted(d.code for d in Repo(files).errors())

    def test_duplicate_id(self):
        self.assertEqual(self.codes({"a.md": doc("docgraph:\n  id: x"),
                                     "b.md": doc("docgraph:\n  id: x")}), ["duplicate-id"])

    def test_unknown_target_for_core_relations(self):
        for rel in ("requires", "derives_from", "related"):
            self.assertEqual(self.codes({"a.md": doc(f"docgraph:\n  id: a\n  {rel}: [nope]")}),
                             ["unknown-target"], rel)

    def test_extension_relation_targets_may_be_external(self):
        self.assertEqual(self.codes({"a.md": doc("docgraph:\n  id: a\n  verified_by: [checker:x]")}), [])

    def test_dependency_cycle_spans_requires_and_derives_from(self):
        self.assertEqual(self.codes({
            "a.md": doc("docgraph:\n  id: a\n  requires: [b]"),
            "b.md": doc("docgraph:\n  id: b\n  derives_from: [a]"),
        }), ["dependency-cycle"])
        self.assertEqual(self.codes({"a.md": doc("docgraph:\n  id: a\n  requires: [a]")}),
                         ["dependency-cycle"])

    def test_unparsable_metadata(self):
        for block in ("docgraph:\n  family: [c5]", "docgraph:\n  id: a\n   bad: x",
                      "docgraph: a", "docgraph:\n  id: a\n  family: [c5, c5]"):
            self.assertEqual(self.codes({"a.md": doc(block)}), ["parse"], block)
        self.assertEqual(self.codes({"a.md": "---\ndocgraph:\n  id: a\n"}), ["parse"])

    def test_check_exit_code(self):
        repo = Repo({"a.md": doc("docgraph:\n  id: a\n  requires: [b]")})
        self.assertEqual(repo.run("check")[0], 1)
        self.assertEqual(repo.run("build")[0], 1)
        self.assertFalse((repo.root / ".docgraph").exists())


class Derived(unittest.TestCase):
    def setUp(self):
        self.repo = Repo({
            "base.md": doc("docgraph:\n  id: base\n  family: [c5]"),
            "mid.md": doc("docgraph:\n  id: mid\n  family: [c5]\n  requires: [base]"),
            "top.md": doc("docgraph:\n  id: top\n  derives_from: [mid]\n  related: [base]"),
        })
        self.graph, _ = self.repo.load()

    def test_reverse_relations_and_closure(self):
        self.assertEqual(self.graph.reverse("base"), {"related_from": ["top"], "required_by": ["mid"]})
        self.assertEqual(self.graph.related("base"), ["top"])
        self.assertEqual(self.graph.ancestors("top"), ["base", "mid"])
        self.assertEqual(self.graph.descendants("base"), ["mid", "top"])

    def test_show_lists_derived_reverse_relations(self):
        text = show(self.graph, "base")
        for part in ("Related:\n  top", "Required by:\n  mid", "Family c5:\n  mid"):
            self.assertIn(part, text)

    def test_local_view_depth(self):
        self.assertEqual(self.graph.local("base", 1), {"base", "mid", "top"})
        self.assertEqual(self.graph.local("mid", 0), {"mid"})

    def test_build_writes_outputs_but_never_sources(self):
        before = self.repo.snapshot()
        code, _ = self.repo.run("build")
        self.assertEqual(code, 0)
        self.assertEqual(self.repo.snapshot(), before)
        out = self.repo.root / ".docgraph"
        for name in ("graph.json", "families.json", "reverse.json", "graph.d2",
                     "families.d2", "dependency.d2", "views/base.depth1.d2"):
            self.assertTrue((out / name).is_file(), name)
        data = json.loads((out / "graph.json").read_text())
        self.assertEqual([n["id"] for n in data["nodes"]], ["base", "mid", "top"])
        self.assertEqual(json.loads((out / "reverse.json").read_text())["mid"], {"derived_by": ["top"]})

    def test_d2_views(self):
        dep = render_d2.dependency_view(self.graph)
        self.assertIn('"mid" -> "base"', dep)
        self.assertNotIn("related", dep)
        rel = render_d2.relation_view(self.graph)
        self.assertIn('"top" -- "base"', rel)
        fam = render_d2.family_view(self.graph)
        self.assertIn('"family:c5": {', fam)
        self.assertIn("(no family)", fam)


class NoInference(unittest.TestCase):
    def test_links_and_names_never_become_relations(self):
        repo = Repo({
            "docs/a.md": doc("docgraph:\n  id: a", "# A\n\nSee [b](b.md).\n"),
            "docs/b.md": doc("docgraph:\n  id: b"),
            "docs/a2.md": doc("docgraph:\n  id: a2"),
        })
        graph, _ = repo.load()
        self.assertEqual(graph.edges, [])
        self.assertEqual(suggest(graph, repo.root), [("a", "b", 1)])
        code, out = repo.run("suggest")
        self.assertIn("nothing was written", out)

    def test_id_is_independent_of_path(self):
        files = {"docs/report/root.md": doc("docgraph:\n  id: c5.root"),
                 "x.md": doc("docgraph:\n  id: x\n  requires: [c5.root]")}
        moved = {"docs/c5/root_conservation.md": files["docs/report/root.md"], "x.md": files["x.md"]}
        for layout in (files, moved):
            self.assertEqual(Repo(layout).errors(), [])


if __name__ == "__main__":
    unittest.main()
