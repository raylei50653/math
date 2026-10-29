"""Exact integer labels in text and JSON without interpreter-wide overrides.

The solvers accept arbitrary Python integer vertex identities. Python's optional
decimal conversion limit must not change which of those graphs can be solved.
Ordinary JSON keeps the standard library's byte representation and fast path.
The fallback only replaces integer conversion, retaining JSON's other rules.
"""
from __future__ import annotations

import json
from json.encoder import _make_iterencode, encode_basestring, encode_basestring_ascii


def int_text(value):
    """Return the exact decimal spelling, even above the interpreter limit."""
    if not isinstance(value, int):
        raise TypeError("int_text expects an integer")
    value = int(value)
    try:
        return str(value)
    except ValueError:
        negative = value < 0
        remaining = abs(value)
        chunks = []
        while remaining:
            remaining, chunk = divmod(remaining, 1_000_000_000)
            chunks.append(chunk)
        digits = str(chunks.pop()) if chunks else "0"
        digits += "".join(f"{chunk:09d}" for chunk in reversed(chunks))
        return "-" + digits if negative else digits


def _parse_integer(text):
    try:
        return int(text)
    except ValueError:
        # json.loads has already checked the integer token's syntax.
        negative = text.startswith("-")
        digits = text[1:] if negative else text
        value = 0
        for start in range(0, len(digits), 9):
            chunk = digits[start:start + 9]
            value = value * (10 ** len(chunk)) + int(chunk)
        return -value if negative else value


class _ExactIntegerEncoder(json.JSONEncoder):
    def iterencode(self, value, _one_shot=False):
        markers = {} if self.check_circular else None
        encoder = encode_basestring_ascii if self.ensure_ascii else encode_basestring

        def float_text(number):
            if number != number:
                text = "NaN"
            elif number == float("inf"):
                text = "Infinity"
            elif number == float("-inf"):
                text = "-Infinity"
            else:
                return float.__repr__(number)
            if not self.allow_nan:
                raise ValueError("Out of range float values are not JSON compliant: " + repr(number))
            return text

        # The stdlib helper handles separators, escaping, dictionaries and
        # circular-reference detection. Only exact int-to-decimal conversion
        # differs; no monkeypatch or process-wide setting is involved.
        indent = self.indent if self.indent is None or isinstance(self.indent, str) else " " * self.indent
        encode = _make_iterencode(markers, self.default, encoder, indent,
                                  float_text, self.key_separator, self.item_separator,
                                  self.sort_keys, self.skipkeys, _one_shot,
                                  _intstr=int_text)
        return encode(value, 0)


def json_dumps(value, **options):
    """Serialize integer identities exactly; preserve normal JSON output."""
    try:
        return json.dumps(value, **options)
    except ValueError as error:
        if "integer string conversion" not in str(error) or "cls" in options:
            raise
        return json.dumps(value, cls=_ExactIntegerEncoder, **options)


def json_loads(text, **options):
    """Read arbitrary decimal integer labels without changing global limits."""
    options.setdefault("parse_int", _parse_integer)
    return json.loads(text, **options)


def browser_payload(value):
    """Keep large identities distinct in a JavaScript JSON consumer.

    Browser numbers cannot represent all Python integer IDs. Use exact decimal
    strings for values outside the safe integer range in the viewer payload;
    solver results and downloadable JSON keep their original integer types.
    """
    if type(value) is int and abs(value) > (1 << 53) - 1:
        return int_text(value)
    if isinstance(value, (list, tuple)):
        return [browser_payload(item) for item in value]
    if isinstance(value, dict):
        return {browser_payload(key): browser_payload(item) for key, item in value.items()}
    return value
