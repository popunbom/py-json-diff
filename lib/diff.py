#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import Any, List


from colorama import Fore, Style


@dataclass
class Diff:
    PREFIX_A = "-"
    PREFIX_B = "+"
    WRAPPER_RANGE = "@@"

    label_a: str
    label_b: str
    range: str
    a: Any
    b: Any


class DiffGenerator:
    def generate(self, diff: Diff) -> List[str]:
        raise NotImplementedError()


class PlainDiffGenerator(DiffGenerator):
    def generate(self, diff: Diff) -> List[str]:
        return [
            "{prefix_a} {label_a}".format(prefix_a=diff.PREFIX_A * 3, label_a=diff.label_a),
            "{prefix_b} {label_b}".format(prefix_b=diff.PREFIX_B * 3, label_b=diff.label_b),
            "{wrapper} {range} {wrapper}".format(
                wrapper=diff.WRAPPER_RANGE,
                range=diff.range,
            ),
            "{prefix_a} {diff_a!r}".format(prefix_a=diff.PREFIX_A, diff_a=diff.a),
            "{prefix_b} {diff_b!r}".format(prefix_b=diff.PREFIX_B, diff_b=diff.b),
            ""
        ]


class ColoredDiffGenerator(DiffGenerator):
    def generate(self, diff: Diff) -> List[str]:
        return [
            Style.BRIGHT + Fore.WHITE + "{prefix_a} {label_a}".format(
                prefix_a=diff.PREFIX_A * 3, label_a=diff.label_a
            ) + Style.RESET_ALL,
            Style.BRIGHT + Fore.WHITE + "{prefix_b} {label_b}".format(
                prefix_b=diff.PREFIX_B * 3, label_b=diff.label_b
            ) + Style.RESET_ALL,
            Fore.CYAN + "{wrapper} {range} {wrapper}".format(
                wrapper=diff.WRAPPER_RANGE,
                range=diff.range,
            ) + Style.RESET_ALL,
            Fore.RED + "{prefix_a} {diff_a!r}".format(
                prefix_a=diff.PREFIX_A, diff_a=diff.a
            ) + Style.RESET_ALL,
            Fore.GREEN + "{prefix_b} {diff_b!r}".format(
                prefix_b=diff.PREFIX_B, diff_b=diff.b
            ) + Style.RESET_ALL,
            ""
        ]
