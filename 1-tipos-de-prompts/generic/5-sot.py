from __future__ import annotations

import argparse

from dotenv import load_dotenv

from common import DEFAULT_TASK, SimpleResponse, build_llm, print_llm_result, resolve_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Skeleton of Thought example.")
    parser.add_argument("--task", help="Task to solve.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--bullet-range", default="3 to 7")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    llm = build_llm(args.model, args.temperature)
    skeleton_prompt = f"""
Create only the skeleton for the task below.
Return {args.bullet_range} concise bullet points.
Do not expand them yet.

Task:
{task}
"""
    skeleton = llm.invoke(skeleton_prompt).content

    expansion_prompt = f"""
Expand the skeleton below into a clear, well-structured final answer.

Task:
{task}

Skeleton:
{skeleton}
"""
    expansion = llm.invoke(expansion_prompt).content
    content = f"STEP 1: SKELETON\n\n{skeleton}\n\nSTEP 2: EXPANDED ANSWER\n\n{expansion}"
    print_llm_result(task, SimpleResponse(content))


if __name__ == "__main__":
    main()
