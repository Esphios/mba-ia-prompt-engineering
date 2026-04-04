from __future__ import annotations

import argparse

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from langchain.prompts import ChatPromptTemplate

from common import DEFAULT_TASK, build_llm, print_llm_result, resolve_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Role prompting example.")
    parser.add_argument("--task", help="User task.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--role", help="System role/persona.")
    parser.add_argument("--role-file", help="File containing the role/persona.")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    role = resolve_text(
        args.role,
        args.role_file,
        "You are a pragmatic senior engineer who explains concepts clearly and concisely.",
    )

    prompt = ChatPromptTemplate(
        [
            ("system", role),
            ("user", task),
        ]
    )
    llm = build_llm(args.model, args.temperature)
    response = llm.invoke(prompt.format_messages())
    print_llm_result(f"System role:\n{role}\n\nUser task:\n{task}", response)


if __name__ == "__main__":
    main()
