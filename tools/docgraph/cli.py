"""docgraph command line. Source documents are only read; `build` and
`render` write generated files under the output directory (default .docgraph/)."""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from . import query, render_d2
from .parser import parse_repo
from .validate import validate


def repo_root(start: Path) -> Path:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=start,
                             capture_output=True, text=True, check=True)
        return Path(out.stdout.strip())
    except (OSError, subprocess.CalledProcessError):
        return start


def load(args):
    nodes, parse_diags = parse_repo(args.repo, args.include)
    return validate(nodes, parse_diags)


def report(diags, verbose: bool) -> int:
    errors = [d for d in diags if d.level == "error"]
    for d in diags:
        if d.level == "error" or verbose:
            print(d, file=sys.stderr)
    return len(errors)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def to_svg(d2_path: Path) -> bool:
    d2 = shutil.which("d2")
    if not d2:
        print("d2 not found on PATH; wrote .d2 only (https://d2lang.com)", file=sys.stderr)
        return False
    subprocess.run([d2, str(d2_path), str(d2_path.with_suffix(".svg"))], check=True,
                   capture_output=True)
    return True


def view_path(out: Path, root: str, depth: int) -> Path:
    return out / "views" / f"{root.replace('/', '_')}.depth{depth}.d2"


def cmd_check(args) -> int:
    graph, diags = load(args)
    errors = report(diags, args.verbose)
    infos = len(diags) - errors
    print(f"{'FAIL' if errors else 'OK'}: {len(graph.nodes)} documents, "
          f"{len(graph.edges)} relations, {len(graph.families)} families; "
          f"{errors} errors, {infos} notes" + ("" if args.verbose or not infos else " (-v to list)"))
    return 1 if errors or (args.strict and infos) else 0


def cmd_build(args) -> int:
    graph, diags = load(args)
    if report(diags, args.verbose):
        print("FAIL: not writing output while errors remain", file=sys.stderr)
        return 1
    out = args.out
    views = out / "views"
    if views.is_dir():
        for stale in views.glob("*.d2"):
            stale.unlink()
        for stale in views.glob("*.svg"):
            stale.unlink()
    dump = lambda data: json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    write(out / "graph.json", dump(graph.to_json()))
    write(out / "families.json", dump(graph.families))
    write(out / "reverse.json", dump(graph.reverse_json()))
    files = {
        out / "graph.d2": render_d2.relation_view(graph),
        out / "families.d2": render_d2.family_view(graph),
        out / "dependency.d2": render_d2.dependency_view(graph),
    }
    for node_id in graph.nodes:
        files[view_path(out, node_id, 1)] = render_d2.local_view(graph, node_id, 1)
    for path, text in files.items():
        write(path, text)
    if args.svg:
        for path in files:
            if not to_svg(path):
                break
    print(f"OK: wrote {out} ({len(graph.nodes)} documents, {len(files)} D2 views)")
    return 0


def cmd_show(args) -> int:
    graph, diags = load(args)
    report(diags, False)
    if args.id not in graph.nodes:
        print(f"unknown id: {args.id}", file=sys.stderr)
        return 2
    print(query.show(graph, args.id))
    return 0


def cmd_family(args) -> int:
    graph, diags = load(args)
    report(diags, False)
    if not args.name:
        print(query.families(graph))
        return 0
    if not graph.family_members(args.name, args.recursive):
        print(f"no documents in family: {args.name}", file=sys.stderr)
        return 2
    print(query.family(graph, args.name, args.recursive))
    return 0


def cmd_render(args) -> int:
    graph, diags = load(args)
    if report(diags, False):
        return 1
    if args.root:
        if args.root not in graph.nodes:
            print(f"unknown id: {args.root}", file=sys.stderr)
            return 2
        text = render_d2.local_view(graph, args.root, args.depth)
        default = view_path(args.out, args.root, args.depth)
    else:
        text = {
            "relation": render_d2.relation_view,
            "family": render_d2.family_view,
            "dependency": render_d2.dependency_view,
        }[args.view](graph)
        default = args.out / {"relation": "graph.d2", "family": "families.d2",
                              "dependency": "dependency.d2"}[args.view]
    if args.output == "-":
        sys.stdout.write(text)
        return 0
    path = Path(args.output) if args.output else default
    write(path, text)
    print(path)
    if args.svg and to_svg(path):
        print(path.with_suffix(".svg"))
    return 0


def cmd_suggest(args) -> int:
    graph, diags = load(args)
    report(diags, False)
    candidates = query.suggest(graph, args.repo)
    if args.id:
        candidates = [c for c in candidates if args.id in c[:2]]
    for source, target, count in candidates:
        print(f"{source} links to {target} ({count}x); no relation declared")
    if candidates:
        print(f"\n{len(candidates)} candidates. Suggestions only; nothing was written.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="docgraph", description=__doc__)
    parser.add_argument("--repo", type=Path, help="repository root (default: git top level)")
    parser.add_argument("--include", action="append",
                        help="glob of Markdown files to scan, relative to the repo (repeatable)")
    parser.add_argument("--out", type=Path, help="output directory (default: <repo>/.docgraph)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("check", help="validate metadata and graph integrity")
    p.add_argument("-v", "--verbose", action="store_true", help="also list informational notes")
    p.add_argument("--strict", action="store_true", help="fail on informational notes too")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("build", help="write graph index, reverse edges, families and D2 views")
    p.add_argument("-v", "--verbose", action="store_true")
    p.add_argument("--svg", action="store_true", help="also run d2 to produce SVG")
    p.set_defaults(func=cmd_build)

    p = sub.add_parser("show", help="local relations of one document")
    p.add_argument("id")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("family", help="members of a family (no name: list families)")
    p.add_argument("name", nargs="?")
    p.add_argument("-r", "--recursive", action="store_true",
                   help="include dotted sub-families (NAME.*)")
    p.set_defaults(func=cmd_family)

    p = sub.add_parser("render", help="write one D2 view")
    p.add_argument("--view", choices=("relation", "family", "dependency"), default="relation")
    p.add_argument("--root", help="render the neighbourhood of this id instead")
    p.add_argument("--depth", type=int, default=1)
    p.add_argument("-o", "--output", help="output file, or - for stdout")
    p.add_argument("--svg", action="store_true", help="also run d2 to produce SVG")
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("suggest", help="print candidate relations from Markdown links")
    p.add_argument("id", nargs="?")
    p.set_defaults(func=cmd_suggest)

    args = parser.parse_args(argv)
    args.repo = (args.repo or repo_root(Path.cwd())).resolve()
    args.out = (args.out or args.repo / ".docgraph").resolve()
    return args.func(args)
