#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from typing import Any, Dict, List, Type

from lib.diff import Diff, DiffGenerator


class JSONdiff:
    label_a: str
    label_b: str
    diff_generator: DiffGenerator

    _data_path: str

    def __init__(self,
                 label_a: str,
                 label_b: str,
                 diff_generator: DiffGenerator) -> None:
        self.label_a = label_a
        self.label_b = label_b
        self.diff_generator = diff_generator

        self._reset()

    def _reset(self):
        self._data_path = ""

    def _isinstance(self, a: Any, b: Any, type: Type):
        return isinstance(a, type) and isinstance(b, type)

    def _gen_diff(self, a: Any, b: Any,
                  data_path: str) -> List[str]:
        return self.diff_generator.generate(
            Diff(
                label_a=self.label_a,
                label_b=self.label_b,
                range=data_path, a=a, b=b,
            )
        )

    def _diff_dict(self, a: Dict, b: Dict) -> List[str]:
        if set(a.keys()) != set(b.keys()):
            return self._gen_diff(
                list(a.keys()), list(b.keys()),
                "{data_path} | keys".format(data_path=self._data_path),
            )

        diffs: List[str] = []
        self_data_path = self._data_path
        for key in a:
            v_a, v_b = a[key], b[key]
            self._data_path = "{path_a}.{path_b}".format(
                path_a=self_data_path,
                path_b=key,
            )

            if self._isinstance(v_a, v_b, dict):
                diffs += self._diff_dict(v_a, v_b)
            elif self._isinstance(v_a, v_b, list):
                diffs += self._diff_list(v_a, v_b)
            elif v_a != v_b:
                diffs += self._gen_diff(
                    v_a, v_b,
                    self._data_path
                )

        return diffs

    def _diff_list(self, a: Dict, b: Dict) -> List[str]:
        if len(a) != len(b):
            return self._gen_diff(
                len(a), len(b),
                "len({data_path})".format(data_path=self._data_path),
            )

        diffs: List[str] = []
        self_data_path = self._data_path
        for idx in range(len(a)):
            v_a, v_b = a[idx], b[idx]
            self._data_path = "{data_path}[{idx}]".format(
                data_path=self_data_path,
                idx=idx,
            )

            if self._isinstance(v_a, v_b, dict):
                diffs += self._diff_dict(v_a, v_b)
            elif self._isinstance(v_a, v_b, list):
                diffs += self._diff_list(v_a, v_b)
            elif v_a != v_b:
                diffs += self._gen_diff(
                    v_a, v_b,
                    self._data_path
                )

        return diffs

    def diff(self,
             json_a: str,
             json_b: str) -> str:
        a = json.loads(json_a)
        b = json.loads(json_b)

        self._reset()

        if self._isinstance(a, b, dict):
            return "\n".join(self._diff_dict(a, b))
        if self._isinstance(a, b, list):
            return "\n".join(self._diff_list(a, b))
        if a != b:
            return "\n".join(self._gen_diff(
                a, b,
                data_path="."
            ))
