from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table

from common import build_llm


DEFAULT_PROBLEM = """
Design a service that processes millions of images daily.

Constraints:
- The workload may spike significantly during some hours.
- The system should be cost-conscious.
- The architecture should remain operable by a reasonably sized engineering team.
"""


@dataclass
class Criterion:
    name: str
    weight: float
    description: str


class CandidateOption(BaseModel):
    name: str = Field(description="Short name for the candidate solution.")
    description: str = Field(description="Concise summary of the candidate solution.")
    rationale: str = Field(description="Why this candidate could work.")
    tradeoffs: str = Field(description="Main trade-offs and limitations.")


class CandidateSet(BaseModel):
    candidates: List[CandidateOption]


class CriterionScore(BaseModel):
    criterion_name: str
    score: int = Field(ge=1, le=10)
    justification: str


class Evaluation(BaseModel):
    criteria: List[CriterionScore]
    strengths: List[str]
    risks: List[str]
    next_improvement: str


class FinalDecision(BaseModel):
    winner_name: str
    rationale: str
    final_answer: str


@dataclass
class SearchNode:
    node_id: str
    depth: int
    option: CandidateOption
    evaluation: Evaluation
    score: float
    score_formula: str
    parent_id: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Tree of Thought search.")
    parser.add_argument("--problem", help="Problem statement.")
    parser.add_argument("--problem-file", help="File containing the problem.")
    parser.add_argument("--criterion", action="append", help="Criterion as name:weight:description")
    parser.add_argument("--max-depth", type=int, default=2)
    parser.add_argument("--branch-factor", type=int, default=2)
    parser.add_argument("--beam-width", type=int, default=2)
    parser.add_argument("--finalists", type=int, default=2)
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.3)
    return parser.parse_args()


def resolve_problem(args: argparse.Namespace) -> str:
    if args.problem_file:
        return Path(args.problem_file).read_text(encoding="utf-8").strip()
    if args.problem:
        return args.problem.strip()
    return DEFAULT_PROBLEM.strip()


def parse_criteria(raw_criteria: list[str] | None) -> list[Criterion]:
    if not raw_criteria:
        return [
            Criterion("scalability", 0.35, "Ability to handle scale and spikes."),
            Criterion("cost_efficiency", 0.25, "Cost efficiency over time."),
            Criterion("operational_simplicity", 0.20, "Ease of operation with a small team."),
            Criterion("feasibility", 0.20, "Practicality of implementation and maintenance."),
        ]
    criteria: list[Criterion] = []
    for raw in raw_criteria:
        name, weight_text, description = raw.split(":", 2)
        criteria.append(Criterion(name.strip(), float(weight_text), description.strip()))
    total = sum(item.weight for item in criteria)
    return [Criterion(item.name, item.weight / total, item.description) for item in criteria]


def criteria_prompt(criteria: list[Criterion]) -> str:
    return "\n".join(
        f"- {criterion.name}: weight={criterion.weight:.2f}; meaning={criterion.description}"
        for criterion in criteria
    )


def weighted_score(evaluation: Evaluation, criteria: list[Criterion]) -> tuple[float, str]:
    scores = {item.criterion_name: item.score for item in evaluation.criteria}
    total = 0.0
    parts: list[str] = []
    for criterion in criteria:
        score = scores.get(criterion.name, 0)
        total += criterion.weight * score
        parts.append(f"{criterion.weight:.2f}*{score}")
    return total, f"{' + '.join(parts)} = {total:.2f}"


def generate_candidates(llm, problem: str, count: int) -> list[CandidateOption]:
    structured = llm.with_structured_output(CandidateSet)
    return structured.invoke(
        f"""
You are the generator in a Tree of Thought search.
Produce {count} materially different candidate solutions for the problem below.

Problem:
{problem}
"""
    ).candidates


def evaluate_candidate(llm, problem: str, option: CandidateOption, criteria: list[Criterion]) -> Evaluation:
    structured = llm.with_structured_output(Evaluation)
    return structured.invoke(
        f"""
Evaluate the candidate below.
Return exactly one score entry per criterion.

Criteria:
{criteria_prompt(criteria)}

Problem:
{problem}

Candidate name: {option.name}
Description: {option.description}
Rationale: {option.rationale}
Trade-offs: {option.tradeoffs}
"""
    )


def expand_candidate(llm, problem: str, node: SearchNode, criteria: list[Criterion], count: int) -> list[CandidateOption]:
    structured = llm.with_structured_output(CandidateSet)
    return structured.invoke(
        f"""
Refine the candidate below into {count} improved child candidates.
Children should remain related to the parent but address weaknesses.
Optimize for these criteria:
{criteria_prompt(criteria)}

Problem:
{problem}

Parent name: {node.option.name}
Description: {node.option.description}
Rationale: {node.option.rationale}
Trade-offs: {node.option.tradeoffs}
Strengths: {node.evaluation.strengths}
Risks: {node.evaluation.risks}
Recommended improvement: {node.evaluation.next_improvement}
"""
    ).candidates


def build_node(node_id: str, depth: int, option: CandidateOption, evaluation: Evaluation, criteria: list[Criterion], parent_id: str | None = None) -> SearchNode:
    score, formula = weighted_score(evaluation, criteria)
    return SearchNode(node_id, depth, option, evaluation, score, formula, parent_id)


def print_table(console: Console, title: str, nodes: list[SearchNode]) -> None:
    table = Table(title=title)
    table.add_column("Node")
    table.add_column("Depth")
    table.add_column("Candidate")
    table.add_column("Score", justify="right")
    table.add_column("Formula")
    for node in nodes:
        table.add_row(node.node_id, str(node.depth), node.option.name, f"{node.score:.2f}", node.score_formula)
    console.print(table)


def print_tree(console: Console, node: SearchNode, children_by_parent: Dict[str, list[SearchNode]], prefix: str = "") -> None:
    if prefix:
        console.print(f"{prefix}{node.node_id} {node.option.name} [{node.score:.2f}]")
        console.print(f"{prefix}formula: {node.score_formula}")
    else:
        console.print(f"{node.node_id} {node.option.name} [{node.score:.2f}]")
        console.print(f"  formula: {node.score_formula}")
    children = children_by_parent.get(node.node_id, [])
    for idx, child in enumerate(children):
        branch = "\\- " if idx == len(children) - 1 else "|- "
        child_prefix = f"{prefix}{branch}" if prefix else f"  {branch}"
        print_tree(console, child, children_by_parent, child_prefix)


def choose_winner(llm, problem: str, finalists: list[SearchNode], criteria: list[Criterion]) -> FinalDecision:
    structured = llm.with_structured_output(FinalDecision)
    formatted = "\n\n".join(
        (
            f"Node: {node.node_id}\n"
            f"Name: {node.option.name}\n"
            f"Description: {node.option.description}\n"
            f"Rationale: {node.option.rationale}\n"
            f"Trade-offs: {node.option.tradeoffs}\n"
            f"Weighted score: {node.score:.2f}\n"
            f"Formula: {node.score_formula}"
        )
        for node in finalists
    )
    return structured.invoke(
        f"""
Choose the best finalist using the weighted criteria below.

Criteria:
{criteria_prompt(criteria)}

Problem:
{problem}

Finalists:
{formatted}
"""
    )


def main() -> None:
    args = parse_args()
    load_dotenv()

    problem = resolve_problem(args)
    criteria = parse_criteria(args.criterion)
    llm = build_llm(args.model, args.temperature)
    console = Console()

    root_nodes: list[SearchNode] = []
    for idx, candidate in enumerate(generate_candidates(llm, problem, args.branch_factor), start=1):
        root_nodes.append(build_node(f"R{idx}", 0, candidate, evaluate_candidate(llm, problem, candidate, criteria), criteria))
    root_nodes.sort(key=lambda node: node.score, reverse=True)
    print_table(console, "Depth 0: Root Candidates", root_nodes)

    active_nodes = root_nodes[: args.beam_width]
    all_nodes = list(root_nodes)
    children_by_parent: Dict[str, list[SearchNode]] = {}

    for depth in range(1, args.max_depth + 1):
        depth_nodes: list[SearchNode] = []
        for parent in active_nodes:
            parent_children: list[SearchNode] = []
            for idx, candidate in enumerate(expand_candidate(llm, problem, parent, criteria, args.branch_factor), start=1):
                child = build_node(
                    f"{parent.node_id}.{idx}",
                    depth,
                    candidate,
                    evaluate_candidate(llm, problem, candidate, criteria),
                    criteria,
                    parent.node_id,
                )
                parent_children.append(child)
                depth_nodes.append(child)
            parent_children.sort(key=lambda node: node.score, reverse=True)
            children_by_parent[parent.node_id] = parent_children
        if not depth_nodes:
            break
        depth_nodes.sort(key=lambda node: node.score, reverse=True)
        print_table(console, f"Depth {depth}: Expanded Candidates", depth_nodes)
        all_nodes.extend(depth_nodes)
        active_nodes = depth_nodes[: args.beam_width]

    console.print("[bold cyan]Tree View[/bold cyan]")
    for root in root_nodes:
        print_tree(console, root, children_by_parent)
        console.print()

    finalists = sorted(all_nodes, key=lambda node: node.score, reverse=True)[: args.finalists]
    decision = choose_winner(llm, problem, finalists, criteria)
    console.print("[bold cyan]Finalists[/bold cyan]")
    for finalist in finalists:
        console.print(f"- {finalist.node_id}: {finalist.option.name} [{finalist.score:.2f}]")
    console.print("[bold cyan]Decision[/bold cyan]")
    console.print(f"Winner: {decision.winner_name}")
    console.print(f"Rationale: {decision.rationale}")
    console.print(f"Final Answer: {decision.final_answer}")


if __name__ == "__main__":
    main()
