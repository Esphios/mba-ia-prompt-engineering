from __future__ import annotations

from dataclasses import dataclass
from typing import List

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from rich.console import Console
from rich.table import Table


class ArchitectureOption(BaseModel):
    name: str = Field(description="Short name for the architecture option.")
    description: str = Field(description="Concise summary of the architecture.")
    scalability_notes: str = Field(description="Scalability analysis.")
    cost_notes: str = Field(description="Cost analysis.")
    complexity_notes: str = Field(description="Complexity analysis.")


class CandidateSet(BaseModel):
    candidates: List[ArchitectureOption]


class Evaluation(BaseModel):
    scalability_score: int = Field(ge=1, le=10)
    cost_score: int = Field(ge=1, le=10)
    complexity_score: int = Field(ge=1, le=10)
    feasibility_score: int = Field(ge=1, le=10)
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
    option: ArchitectureOption
    evaluation: Evaluation
    score: float
    parent_id: str | None = None


PROBLEM = """
Design a service that processes millions of images daily.

Constraints:
- The workload may spike significantly during some hours.
- The system should be cost-conscious.
- The architecture should remain operable by a reasonably sized engineering team.
"""


def weighted_score(evaluation: Evaluation) -> float:
    return (
        evaluation.scalability_score * 0.35
        + evaluation.cost_score * 0.25
        + evaluation.complexity_score * 0.20
        + evaluation.feasibility_score * 0.20
    )


def generate_root_candidates(llm: ChatOpenAI, problem: str, count: int) -> List[ArchitectureOption]:
    structured_llm = llm.with_structured_output(CandidateSet)
    prompt = f"""
You are the generator in a Tree of Thought search.
Produce {count} materially different architecture options for the problem below.

Rules:
- Return distinct options, not minor variations.
- Each option must include analysis for scalability, cost, and complexity.
- Good candidates include concrete building blocks such as queue, object storage,
  autoscaling workers, Kubernetes, serverless, or batch pipelines when relevant.

Problem:
{problem}
"""
    result = structured_llm.invoke(prompt)
    return result.candidates


def evaluate_candidate(llm: ChatOpenAI, problem: str, option: ArchitectureOption) -> Evaluation:
    structured_llm = llm.with_structured_output(Evaluation)
    prompt = f"""
You are the evaluator in a Tree of Thought search.
Score the candidate architecture for the problem below.

Scoring rules:
- Higher scalability_score means better ability to handle millions of images per day.
- Higher cost_score means better cost efficiency.
- Higher complexity_score means easier operational complexity.
- Higher feasibility_score means easier to implement and maintain in practice.
- Be critical and realistic.

Problem:
{problem}

Candidate name: {option.name}
Description: {option.description}
Scalability notes: {option.scalability_notes}
Cost notes: {option.cost_notes}
Complexity notes: {option.complexity_notes}
"""
    return structured_llm.invoke(prompt)


def expand_candidate(
    llm: ChatOpenAI,
    problem: str,
    option: ArchitectureOption,
    evaluation: Evaluation,
    count: int,
) -> List[ArchitectureOption]:
    structured_llm = llm.with_structured_output(CandidateSet)
    prompt = f"""
You are the expansion step in a Tree of Thought search.
Refine the candidate below into {count} improved child candidates.

Rules:
- Each child should address the main risk or weakness found during evaluation.
- Children must remain recognizably related to the parent, but should make concrete
  architectural changes.
- Keep them distinct from each other.

Problem:
{problem}

Parent candidate name: {option.name}
Description: {option.description}
Scalability notes: {option.scalability_notes}
Cost notes: {option.cost_notes}
Complexity notes: {option.complexity_notes}

Evaluation strengths: {evaluation.strengths}
Evaluation risks: {evaluation.risks}
Recommended improvement: {evaluation.next_improvement}
"""
    result = structured_llm.invoke(prompt)
    return result.candidates


def choose_winner(llm: ChatOpenAI, problem: str, finalists: List[SearchNode]) -> FinalDecision:
    structured_llm = llm.with_structured_output(FinalDecision)
    formatted_candidates = "\n\n".join(
        [
            (
                f"Candidate {idx + 1}\n"
                f"Name: {node.option.name}\n"
                f"Description: {node.option.description}\n"
                f"Scalability notes: {node.option.scalability_notes}\n"
                f"Cost notes: {node.option.cost_notes}\n"
                f"Complexity notes: {node.option.complexity_notes}\n"
                f"Weighted score: {node.score:.2f}\n"
                f"Strengths: {', '.join(node.evaluation.strengths)}\n"
                f"Risks: {', '.join(node.evaluation.risks)}"
            )
            for idx, node in enumerate(finalists)
        ]
    )
    prompt = f"""
You are the final decision step in a Tree of Thought search.
Compare the finalists below and choose the best trade-off for the problem.

Requirements:
- Consider the candidate descriptions and their evaluation results.
- The winner should balance scale, cost, and operational simplicity.
- `final_answer` must be 6 words or less.

Problem:
{problem}

Finalists:
{formatted_candidates}
"""
    return structured_llm.invoke(prompt)


def print_nodes(console: Console, title: str, nodes: List[SearchNode]) -> None:
    table = Table(title=title)
    table.add_column("Node")
    table.add_column("Depth")
    table.add_column("Architecture")
    table.add_column("Score", justify="right")
    table.add_column("Improvement")

    for node in nodes:
        table.add_row(
            node.node_id,
            str(node.depth),
            node.option.name,
            f"{node.score:.2f}",
            node.evaluation.next_improvement,
        )

    console.print(table)


def main() -> None:
    load_dotenv()
    console = Console()
    llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

    branch_factor = 3
    beam_width = 2

    console.print("[bold green]REAL TREE OF THOUGHT SEARCH[/bold green]")
    console.print(PROBLEM.strip())
    console.print()

    root_candidates = generate_root_candidates(llm, PROBLEM, count=branch_factor)
    root_nodes: List[SearchNode] = []

    for idx, candidate in enumerate(root_candidates, start=1):
        evaluation = evaluate_candidate(llm, PROBLEM, candidate)
        root_nodes.append(
            SearchNode(
                node_id=f"R{idx}",
                depth=0,
                option=candidate,
                evaluation=evaluation,
                score=weighted_score(evaluation),
            )
        )

    root_nodes.sort(key=lambda node: node.score, reverse=True)
    print_nodes(console, "Depth 0: Root Candidates", root_nodes)

    active_nodes = root_nodes[:beam_width]
    child_nodes: List[SearchNode] = []

    for parent in active_nodes:
        children = expand_candidate(
            llm,
            PROBLEM,
            parent.option,
            parent.evaluation,
            count=branch_factor,
        )
        for idx, candidate in enumerate(children, start=1):
            evaluation = evaluate_candidate(llm, PROBLEM, candidate)
            child_nodes.append(
                SearchNode(
                    node_id=f"{parent.node_id}.{idx}",
                    depth=1,
                    option=candidate,
                    evaluation=evaluation,
                    score=weighted_score(evaluation),
                    parent_id=parent.node_id,
                )
            )

    child_nodes.sort(key=lambda node: node.score, reverse=True)
    print_nodes(console, "Depth 1: Expanded Candidates", child_nodes)

    finalists = child_nodes[:beam_width]
    decision = choose_winner(llm, PROBLEM, finalists)

    console.print("[bold cyan]Finalists[/bold cyan]")
    for node in finalists:
        console.print(f"- {node.node_id}: {node.option.name} ({node.score:.2f})")

    console.print()
    console.print("[bold cyan]Decision[/bold cyan]")
    console.print(f"Winner: {decision.winner_name}")
    console.print(f"Rationale: {decision.rationale}")
    console.print(f"Final Answer: {decision.final_answer}")


if __name__ == "__main__":
    main()
