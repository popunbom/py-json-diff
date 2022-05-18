#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from lib.json_diff import JSONdiff
from lib.diff import ColoredDiffGenerator, PlainDiffGenerator


json_a = json.dumps({
    "a": [
        {
            "b": 123,
            "c": "456",
            "d": True,
        }
    ],
    "b": None
})

json_b = json.dumps({
    "a": [
        {
            "b": 123,
            "c": 456,
            "d": True,
        }
    ],
    "b": ["xyz", "&&)"]
})

jd = JSONdiff(
    label_a="expect",
    label_b="actual",
    diff_generator=ColoredDiffGenerator(),
    # diff_generator=PlainDiffGenerator(),
)

print(jd.diff(
    json_a,
    json_b
))
