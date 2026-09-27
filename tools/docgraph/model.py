"""Core data model. Generic: nothing here knows about any particular repository."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class RelationType:
    name: str
    inverse: str            # label for the derived reverse direction
    dag: bool = False       # participates in the dependency projection
    symmetric: bool = False  # displayed without direction (A~B == B~A)
    checked: bool = True    # targets must be existing node ids


CORE_RELATIONS = {
    r.name: r
    for r in (
        RelationType("requires", "required_by", dag=True),
        RelationType("derives_from", "derived_by", dag=True),
        RelationType("related", "related_from", symmetric=True),
    )
}

# Keys of the docgraph block that are not relations.
FIELDS = ("id", "family")


def relation_type(name: str) -> RelationType:
    """Core relations are checked; any other list-valued key is an extension
    relation (verified_by, formalized_by, ...) whose targets may be external."""
    return CORE_RELATIONS.get(name) or RelationType(name, f"{name}_of", checked=False)


NAME = re.compile(r"^[^\s,\[\]{}#\"'`]+$")


@dataclass
class Node:
    id: str
    path: str                                   # repository-relative, POSIX
    title: str = ""
    families: tuple[str, ...] = ()
    relations: dict[str, tuple[str, ...]] = field(default_factory=dict)


@dataclass(frozen=True)
class Edge:
    source: str
    type: str
    target: str


@dataclass(frozen=True)
class Diagnostic:
    level: str      # "error" or "info"
    code: str
    message: str
    path: str = ""

    def __str__(self) -> str:
        where = f"{self.path}: " if self.path else ""
        return f"{self.level.upper()} [{self.code}] {where}{self.message}"
