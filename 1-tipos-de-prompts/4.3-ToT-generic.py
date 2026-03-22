from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table


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
    rationale: str = Field(description="Why this candidate could work for the problem.")
    tradeoffs: str = Field(description="Main trade-offs, constraints, and limitations.")


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
    parser = argparse.ArgumentParser(
        description="Generic Tree of Thought search with configurable depth and evaluation criteria."
    )
    parser.add_argument(
        "--problem",
        help="Problem statement to solve. If omitted, the default example problem is used.",
    )
    parser.add_argument(
        "--problem-file",
        help="Path to a text file containing the problem statement.",
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI model name. Default: gpt-4o",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.3,
        help="Model temperature. Default: 0.3",
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=2,
        help="Maximum search depth. Default: 2",
    )
    parser.add_argument(
        "--branch-factor",
        type=int,
        default=2,
        help="Number of children generated per expanded node. Default: 2",
    )
    parser.add_argument(
        "--beam-width",
        type=int,
        default=2,
        help="Number of nodes kept per expansion round. Default: 2",
    )
    parser.add_argument(
        "--finalists",
        type=int,
        default=2,
        help="Number of top global candidates sent to final decision. Default: 2",
    )
    parser.add_argument(
        "--criterion",
        action="append",
        help=(
            "Evaluation criterion in the format name:weight:description. "
            "Repeat this flag to add multiple criteria."
        ),
    )
    return parser.parse_args()


def load_problem(args: argparse.Namespace) -> str:
    if args.problem_file:
        return Path(args.problem_file).read_text(encoding="utf-8").strip()
    if args.problem:
        return args.problem.strip()
    return DEFAULT_PROBLEM.strip()


def default_criteria() -> List[Criterion]:
    return [
        Criterion("scalability", 0.35, "Ability to handle large workload and spikes."),
        Criterion("cost_efficiency", 0.25, "Cost efficiency over time."),
        Criterion("operational_simplicity", 0.20, "Ease of operating with a reasonably sized team."),
        Criterion("feasibility", 0.20, "Practicality of implementation and maintenance."),
    ]


def parse_criteria(raw_criteria: List[str] | None) -> List[Criterion]:
    if not raw_criteria:
        return default_criteria()

    criteria: List[Criterion] = []
    for raw in raw_criteria:
        parts = raw.split(":", 2)
        if len(parts) != 3:
            raise ValueError(
                f"Invalid criterion '{raw}'. Use the format name:weight:description."
            )
        name, weight_text, description = parts
        criteria.append(Criterion(name.strip(), float(weight_text), description.strip()))

    total_weight = sum(criterion.weight for criterion in criteria)
    if total_weight <= 0:
        raise ValueError("Criterion weights must sum to more than zero.")

    return [Criterion(c.name, c.weight / total_weight, c.description) for c in criteria]


def criteria_prompt(criteria: List[Criterion]) -> str:
    return "\n".join(
        f"- {criterion.name}: weight={criterion.weight:.2f}; meaning={criterion.description}"
        for criterion in criteria
    )


def weighted_score(evaluation: Evaluation, criteria: List[Criterion]) -> tuple[float, str]:
    criterion_map = {criterion.name: criterion for criterion in criteria}
    score_map = {item.criterion_name: item.score for item in evaluation.criteria}

    score = 0.0
    parts: List[str] = []
    for criterion in criteria:
        raw_score = score_map.get(criterion.name, 0)
        score += criterion.weight * raw_score
        parts.append(f"{criterion.weight:.2f}*{raw_score}")

    return score, f"{' + '.join(parts)} = {score:.2f}"


def generate_root_candidates(llm: ChatOpenAI, problem: str, count: int) -> List[CandidateOption]:
    structured_llm = llm.with_structured_output(CandidateSet)
    prompt = f"""
You are the generator in a Tree of Thought search.
Produce {count} materially different candidate solutions for the problem below.

Rules:
- Return distinct options, not minor variations.
- Each option must include a concise rationale and clear trade-offs.
- Favor candidates that are concrete and actionable.

Problem:
{problem}
"""
    result = structured_llm.invoke(prompt)
    return result.candidates


def evaluate_candidate(
    llm: ChatOpenAI,
    problem: str,
    option: CandidateOption,
    criteria: List[Criterion],
) -> Evaluation:
    structured_llm = llm.with_structured_output(Evaluation)
    prompt = f"""
You are the evaluator in a Tree of Thought search.
Evaluate the candidate solution for the problem below.

Scoring rules:
- Return exactly one score entry for each criterion listed below.
- `criterion_name` values must match the criterion names exactly.
- Scores go from 1 to 10.
- Be critical and realistic.

Criteria:
{criteria_prompt(criteria)}

Problem:
{problem}

Candidate name: {option.name}
Description: {option.description}
Rationale: {option.rationale}
Trade-offs: {option.tradeoffs}
"""
    return structured_llm.invoke(prompt)


def expand_candidate(
    llm: ChatOpenAI,
    problem: str,
    option: CandidateOption,
    evaluation: Evaluation,
    criteria: List[Criterion],
    count: int,
) -> List[CandidateOption]:
    structured_llm = llm.with_structured_output(CandidateSet)
    prompt = f"""
You are the expansion step in a Tree of Thought search.
Refine the candidate below into {count} improved child candidates.

Rules:
- Each child should address the main weaknesses found during evaluation.
- Children must remain recognizably related to the parent, but should make concrete changes.
- Keep them distinct from each other.
- Optimize with respect to these criteria:
{criteria_prompt(criteria)}

Problem:
{problem}

Parent candidate name: {option.name}
Description: {option.description}
Rationale: {option.rationale}
Trade-offs: {option.tradeoffs}

Evaluation strengths: {evaluation.strengths}
Evaluation risks: {evaluation.risks}
Recommended improvement: {evaluation.next_improvement}
"""
    result = structured_llm.invoke(prompt)
    return result.candidates


def choose_winner(
    llm: ChatOpenAI,
    problem: str,
    finalists: List[SearchNode],
    criteria: List[Criterion],
) -> FinalDecision:
    structured_llm = llm.with_structured_output(FinalDecision)
    formatted_candidates = "\n\n".join(
        [
            (
                f"Candidate {idx + 1}\n"
                f"Node id: {node.node_id}\n"
                f"Name: {node.option.name}\n"
                f"Description: {node.option.description}\n"
                f"Rationale: {node.option.rationale}\n"
                f"Trade-offs: {node.option.tradeoffs}\n"
                f"Weighted score: {node.score:.2f}\n"
                f"Formula: {node.score_formula}\n"
                f"Strengths: {', '.join(node.evaluation.strengths)}\n"
                f"Risks: {', '.join(node.evaluation.risks)}"
            )
            for idx, node in enumerate(finalists)
        ]
    )
    prompt = f"""
You are the final decision step in a Tree of Thought search.
Compare the finalists below and choose the best trade-off for the problem.

Decision criteria:
{criteria_prompt(criteria)}

Requirements:
- Consider the candidate descriptions and their evaluation results.
- Prefer the strongest overall trade-off using the weighted criteria above.
- `final_answer` must be 10 words or less.

Problem:
{problem}

Finalists:
{formatted_candidates}
"""
    return structured_llm.invoke(prompt)


def build_node(
    node_id: str,
    depth: int,
    option: CandidateOption,
    evaluation: Evaluation,
    criteria: List[Criterion],
    parent_id: str | None = None,
) -> SearchNode:
    score, formula = weighted_score(evaluation, criteria)
    return SearchNode(
        node_id=node_id,
        depth=depth,
        option=option,
        evaluation=evaluation,
        score=score,
        score_formula=formula,
        parent_id=parent_id,
    )


def print_score_table(console: Console, title: str, nodes: List[SearchNode]) -> None:
    table = Table(title=title)
    table.add_column("Node")
    table.add_column("Depth")
    table.add_column("Candidate")
    table.add_column("Score", justify="right")
    table.add_column("Formula")

    for node in nodes:
        table.add_row(
            node.node_id,
            str(node.depth),
            node.option.name,
            f"{node.score:.2f}",
            node.score_formula,
        )

    console.print(table)


def print_ascii_tree(console: Console, root_nodes: List[SearchNode], children_by_parent: Dict[str, List[SearchNode]]) -> None:
    console.print("[bold cyan]Tree View[/bold cyan]")
    for root in root_nodes:
        print_subtree(console, root, children_by_parent, prefix="")
        console.print()


def print_subtree(
    console: Console,
    node: SearchNode,
    children_by_parent: Dict[str, List[SearchNode]],
    prefix: str,
) -> None:
    if prefix:
        console.print(f"{prefix}{node.node_id} {node.option.name} [{node.score:.2f}]")
        console.print(f"{prefix}formula: {node.score_formula}")
        console.print(f"{prefix}next: {node.evaluation.next_improvement}")
    else:
        console.print(f"{node.node_id} {node.option.name} [{node.score:.2f}]")
        console.print(f"  formula: {node.score_formula}")
        console.print(f"  next: {node.evaluation.next_improvement}")

    children = children_by_parent.get(node.node_id, [])
    for idx, child in enumerate(children):
        is_last = idx == len(children) - 1
        branch = "\\- " if is_last else "|- "
        child_prefix = f"{prefix}{branch}" if prefix else f"  {branch}"
        print_subtree(console, child, children_by_parent, child_prefix)


def print_criteria(console: Console, criteria: List[Criterion]) -> None:
    table = Table(title="Decision Criteria")
    table.add_column("Criterion")
    table.add_column("Weight", justify="right")
    table.add_column("Description")

    for criterion in criteria:
        table.add_row(criterion.name, f"{criterion.weight:.2f}", criterion.description)

    console.print(table)


def main() -> None:
    args = parse_args()
    load_dotenv()

    if args.max_depth < 1:
        raise ValueError("--max-depth must be at least 1.")
    if args.branch_factor < 1:
        raise ValueError("--branch-factor must be at least 1.")
    if args.beam_width < 1:
        raise ValueError("--beam-width must be at least 1.")
    if args.finalists < 1:
        raise ValueError("--finalists must be at least 1.")

    problem = load_problem(args)
    criteria = parse_criteria(args.criterion)

    console = Console()
    llm = ChatOpenAI(model=args.model, temperature=args.temperature)

    console.print("[bold green]GENERIC TREE OF THOUGHT SEARCH[/bold green]")
    console.print(problem)
    console.print()
    print_criteria(console, criteria)
    console.print(
        "[bold]Score formula:[/bold] weighted sum of selected criteria with 1-10 scores."
    )
    console.print(
        "[bold]Selection rule:[/bold] final finalists come from the best global nodes seen so far."
    )
    console.print(f"[bold]Search depth:[/bold] expand until depth {args.max_depth}")
    console.print(f"[bold]Branch factor:[/bold] {args.branch_factor} children per expanded node")
    console.print(f"[bold]Beam width:[/bold] keep top {args.beam_width} nodes per expansion round")
    console.print(f"[bold]Finalists:[/bold] top {args.finalists} global nodes go to final decision")
    console.print()

    root_candidates = generate_root_candidates(llm, problem, count=args.branch_factor)
    root_nodes: List[SearchNode] = []

    for idx, candidate in enumerate(root_candidates, start=1):
        evaluation = evaluate_candidate(llm, problem, candidate, criteria)
        root_nodes.append(build_node(f"R{idx}", 0, candidate, evaluation, criteria))

    root_nodes.sort(key=lambda node: node.score, reverse=True)
    print_score_table(console, "Depth 0: Root Candidates", root_nodes)

    active_nodes = root_nodes[: args.beam_width]
    all_nodes: List[SearchNode] = list(root_nodes)
    children_by_parent: Dict[str, List[SearchNode]] = {}

    for depth in range(1, args.max_depth + 1):
        depth_nodes: List[SearchNode] = []
        for parent in active_nodes:
            children = expand_candidate(
                llm,
                problem,
                parent.option,
                parent.evaluation,
                criteria,
                count=args.branch_factor,
            )
            parent_children: List[SearchNode] = []
            for idx, candidate in enumerate(children, start=1):
                evaluation = evaluate_candidate(llm, problem, candidate, criteria)
                child = build_node(
                    f"{parent.node_id}.{idx}",
                    depth,
                    candidate,
                    evaluation,
                    criteria,
                    parent_id=parent.node_id,
                )
                depth_nodes.append(child)
                parent_children.append(child)

            parent_children.sort(key=lambda node: node.score, reverse=True)
            children_by_parent[parent.node_id] = parent_children

        depth_nodes.sort(key=lambda node: node.score, reverse=True)
        all_nodes.extend(depth_nodes)
        print_score_table(console, f"Depth {depth}: Expanded Candidates", depth_nodes)
        active_nodes = depth_nodes[: args.beam_width]

        if not active_nodes:
            break

    print_ascii_tree(console, root_nodes, children_by_parent)

    global_pool = sorted(all_nodes, key=lambda node: node.score, reverse=True)
    finalists = global_pool[: args.finalists]

    console.print("[bold cyan]Best-So-Far Pool[/bold cyan]")
    for node in global_pool:
        origin = "root" if node.depth == 0 else f"child of {node.parent_id}"
        console.print(f"- {node.node_id}: {node.option.name} [{node.score:.2f}] ({origin})")

    console.print()
    console.print("[bold cyan]Finalists[/bold cyan]")
    for node in finalists:
        origin = "root" if node.depth == 0 else f"child of {node.parent_id}"
        console.print(f"- {node.node_id}: {node.option.name} [{node.score:.2f}] ({origin})")
        console.print(f"  formula: {node.score_formula}")

    decision = choose_winner(llm, problem, finalists, criteria)

    console.print()
    console.print("[bold cyan]Decision[/bold cyan]")
    console.print(f"Winner: {decision.winner_name}")
    console.print(f"Rationale: {decision.rationale}")
    console.print(f"Final Answer: {decision.final_answer}")


if __name__ == "__main__":
    main()
