---
title: fmol 1
---
Earley parser:

```python
from dataclasses import dataclass
from enum import Enum
from typing import Self
from collections import deque
from pprint import pprint


@dataclass(eq=True, frozen=True)
class DotRule:
    lhs: str
    rhs: tuple[str, ...]
    dot_index: int


@dataclass(eq=True, frozen=True)
class EarleyEdge:
    rule: DotRule
    span: tuple[int, int]
    hist: tuple[Self, ...] | None

    def is_complete(self):
        return self.rule.dot_index == len(self.rule.rhs)

    def is_waiting_on(self, other: Self):
        complete_nt = other.rule.lhs
        completed_span_start, completed_span_end = other.span
        if self.rule.dot_index < len(self.rule.rhs):
            waiting_nt = self.rule.rhs[self.rule.dot_index]
            _, potential_span_end = self.span
            return (waiting_nt == complete_nt) and (
                potential_span_end == completed_span_start
            )
        return False


@dataclass
class Grammar:
    terminals: set[str]
    nonterminals: set[str]
    privileged_nts: set[str]
    rules: dict[str, list[tuple[str, ...]]]
    start_symbol: str = "start"

    def earley_parse(self, input: list[str]):
        # initialise the chart
        chart = set(
            [
                EarleyEdge(
                    rule=DotRule(
                        self.start_symbol, self.rules[self.start_symbol][0], dot_index=0
                    ),
                    span=(0, 0),
                    hist=None,
                )
            ]
        )
        recognized = False
        while not recognized:
            old_len = len(chart)
            # ok let's do prediction now
            new_edges: set[EarleyEdge] = set([])
            for edge in chart:
                # find all unexplored tree nodes i.e. nonterminals with a dot to
                # their left
                if (
                    edge.rule.dot_index < len(edge.rule.rhs)  # dot might be at the end
                    and edge.rule.rhs[edge.rule.dot_index]
                    in self.nonterminals  # dont want to expand terminals
                ):
                    nt = edge.rule.rhs[edge.rule.dot_index]
                    edge_start, edge_end = edge.span
                    # we /forward/ lookup to the scan step for privileged nonterminals
                    if nt not in self.privileged_nts:
                        for expansion in self.rules[nt]:
                            new_edge = EarleyEdge(
                                rule=DotRule(lhs=nt, rhs=expansion, dot_index=0),
                                span=(edge_end, edge_end),
                                hist=None,
                            )
                            # set handles duplicates for us, and dataclasses handle the
                            # equality checking
                            new_edges.add(new_edge)

            chart.update(new_edges)

            # scanning...
            new_edges.clear()
            for edge in chart:
                if edge.rule.dot_index < len(edge.rule.rhs):
                    # dot is not at the end
                    next_symbol = edge.rule.rhs[edge.rule.dot_index]
                    i, j = edge.span
                    if next_symbol in self.privileged_nts:
                        # this is the forwarded lookup
                        a = input[j]
                        rule_rhs = self.rules[next_symbol]
                        if (a,) in rule_rhs:
                            # we only add the edge if a_j is consistent with the
                            # nonterminal
                            new_edge = EarleyEdge(
                                rule=DotRule(
                                    edge.rule.lhs,
                                    edge.rule.rhs,
                                    edge.rule.dot_index + 1,
                                ),
                                span=(i, j + 1),
                                hist=None,
                            )
                            new_edges.add(new_edge)
                    elif next_symbol in self.terminals:
                        if input[j] == next_symbol:
                            new_edge = EarleyEdge(
                                rule=DotRule(
                                    edge.rule.lhs,
                                    edge.rule.rhs,
                                    edge.rule.dot_index + 1,
                                ),
                                span=(i, j + 1),
                                hist=None,
                            )
                            new_edges.add(new_edge)
            chart.update(new_edges)
            # completing...
            new_edges.clear()

            # need to keep a queue so that we can propagate completed edges
            completed_edges = deque([edge for edge in chart if edge.is_complete()])
            while completed_edges:
                # above is implicitly false when the deque is empty
                completed_edge = completed_edges.popleft()
                if completed_edge.span == (0, len(input)):
                    recognized = True
                for potential_edge in chart:
                    # horrendously inefficient, perhaps these should be indexed by
                    # span or something
                    if potential_edge.is_waiting_on(completed_edge):

                        # this rule was waiting
                        new_edge = EarleyEdge(
                            rule=DotRule(
                                lhs=potential_edge.rule.lhs,
                                rhs=potential_edge.rule.rhs,
                                dot_index=potential_edge.rule.dot_index + 1,
                            ),
                            span=(potential_edge.span[0], completed_edge.span[1]),
                            hist=(
                                tuple(
                                    list(list(potential_edge.hist) + [completed_edge])
                                )
                                if (potential_edge.hist is not None)
                                else (completed_edge,)
                            ),
                        )
                        if new_edge not in chart:
                            new_edges.add(new_edge)
                            if new_edge.is_complete():
                                completed_edges.append(new_edge)
            chart.update(new_edges)
            if old_len == len(chart):
                # chart didn't change, so we have terminated
                break

        return (recognized, chart)

    def number_parses(self, chart: set[EarleyEdge], input: list[str]):
        return max(
            [
                len(edge.hist)
                for edge in chart
                if edge.hist is not None and edge.span == (0, len(sentence))
            ]
        )


if __name__ == "__main__":

    grammar = Grammar(
        nonterminals=set(["S", "NP", "VP", "PP", "N", "V", "P"]),
        terminals=set(["can", "fish", "in", "rivers", "they", "December"]),
        privileged_nts=set(["N", "V", "P"]),
        start_symbol="S",
        rules={
            "S": [("NP", "VP")],
            "NP": [("N", "PP"), ("N",)],
            "PP": [
                ("P", "NP"),
            ],
            "VP": [("VP", "PP"), ("V", "VP"), ("V", "NP"), ("V",)],
            "N": [("can",), ("fish",), ("rivers",), ("they",), ("December",)],
            "P": [("in",)],
            "V": [("can",), ("fish",)],
        },
    )
    # pprint(chart)
    sentence = ["they", "can", "fish", "in", "rivers"]
    recognized, chart = grammar.earley_parse(sentence)
    number_parses = grammar.number_parses(chart, sentence)
    print(f"found {number_parses} parses for sentence \"{' '.join(sentence)}\"")

    sentence = ["they", "can", "fish", "in", "rivers", "in", "December"]
    recognized, chart = grammar.earley_parse(sentence)
    number_parses = grammar.number_parses(chart, sentence)
    print(f"found {number_parses} parses for sentence \"{' '.join(sentence)}\"")

```