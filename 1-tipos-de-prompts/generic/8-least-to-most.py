from __future__ import annotations

import argparse

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from pydantic import BaseModel, Field

from common import (
    DEFAULT_TASK,
    SimpleResponse,
    build_llm,
    print_llm_result,
    resolve_message_text,
    resolve_text,
)


class SubproblemList(BaseModel):
    subproblems: list[str] = Field(description="Ordered subproblems from easiest to hardest.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Least-to-Most prompting example.")
    parser.add_argument("--task", help="Task to solve.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    llm = build_llm(args.model, args.temperature)
    structured = llm.with_structured_output(SubproblemList)
    structured_response = structured.invoke(
        f"""
Break the task below into an ordered list of subproblems from easiest to hardest.
Keep the list concise and actionable.

Task:
{task}
"""
    )
    if isinstance(structured_response, SubproblemList):
        subproblems = structured_response.subproblems
    else:
        subproblems = list(structured_response.get("subproblems", []))

    solved: list[str] = []
    progress_lines: list[str] = []
    for index, subproblem in enumerate(subproblems, start=1):
        solution = resolve_message_text(
            llm.invoke(
            f"""
Solve subproblem {index} below.
You may use the previously solved subproblems as context.

Original task:
{task}

Previous solutions:
{chr(10).join(solved) if solved else 'None'}

Current subproblem:
{subproblem}
"""
            ).content
        )
        solved.append(f"Subproblem {index}: {subproblem}\nSolution: {solution}")
        progress_lines.append(f"[x] {subproblem}\n{solution}")

    final_answer = resolve_message_text(
        llm.invoke(
        f"""
Combine the solved subproblems below into one final integrated answer.

Original task:
{task}

Solved subproblems:
{chr(10).join(solved)}
"""
        ).content
    )

    content = "TO-DO LIST AND SOLUTIONS\n\n" + "\n\n".join(progress_lines) + "\n\nFINAL INTEGRATED ANSWER\n\n" + final_answer
    print_llm_result(task, SimpleResponse(content))


if __name__ == "__main__":
    main()
