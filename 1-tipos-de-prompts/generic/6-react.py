from __future__ import annotations

import argparse

from dotenv import load_dotenv

from common import DEFAULT_TASK, build_llm, print_llm_result, resolve_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="ReAct prompting example.")
    parser.add_argument("--task", help="Task to solve.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--context", help="Extra context or evidence.")
    parser.add_argument("--context-file", help="File containing extra context.")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.2)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    context = resolve_text(
        args.context,
        args.context_file,
        "Use only the provided information. If something is missing, say so instead of inventing it.",
    )
    prompt = f"""
Use ReAct style reasoning.
Alternate between:
- Thought:
- Action:
- Observation:

Rules:
- Keep actions concrete and relevant.
- Do not fabricate evidence missing from the context.
- Finish with "Final Answer:".

Context:
{context}

Task:
{task}
"""
    llm = build_llm(args.model, args.temperature)
    response = llm.invoke(prompt)
    print_llm_result(prompt, response)


if __name__ == "__main__":
    main()
