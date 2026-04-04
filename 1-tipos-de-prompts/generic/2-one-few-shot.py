from __future__ import annotations

import argparse
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False

from common import DEFAULT_TASK, build_llm, print_llm_result, resolve_text


DEFAULT_EXAMPLE = "Input: What is France's capital?\nOutput: Paris"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="One-shot / Few-shot prompting example.")
    parser.add_argument("--task", help="Task to solve.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--instruction", default="Use the examples to infer the expected pattern.")
    parser.add_argument("--example", action="append", help="Example block. Repeat to add more.")
    parser.add_argument("--example-file", action="append", help="Path to a file containing one example.")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0)
    return parser.parse_args()


def load_examples(args: argparse.Namespace) -> list[str]:
    examples = list(args.example or [])
    for file_path in args.example_file or []:
        examples.append(Path(file_path).read_text(encoding="utf-8").strip())
    return examples or [DEFAULT_EXAMPLE]


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    examples = load_examples(args)
    prompt = (
        f"{args.instruction}\n\nExamples:\n"
        + "\n\n".join(examples)
        + f"\n\nNow solve:\n{task}"
    )
    llm = build_llm(args.model, args.temperature)
    response = llm.invoke(prompt)
    print_llm_result(prompt, response)


if __name__ == "__main__":
    main()
