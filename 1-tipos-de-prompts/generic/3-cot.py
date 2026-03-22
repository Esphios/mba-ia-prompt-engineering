from __future__ import annotations

import argparse

from dotenv import load_dotenv

from common import DEFAULT_TASK, build_llm, print_llm_result, resolve_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chain of Thought example.")
    parser.add_argument("--task", help="Task to solve.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--answer-label", default="Answer:")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    prompt = f"""
Solve the task below.
Think step by step before giving the final result.
After your reasoning, write only the final answer after "{args.answer_label}".

Task:
{task}
"""
    llm = build_llm(args.model, args.temperature)
    response = llm.invoke(prompt)
    print_llm_result(prompt, response)


if __name__ == "__main__":
    main()
