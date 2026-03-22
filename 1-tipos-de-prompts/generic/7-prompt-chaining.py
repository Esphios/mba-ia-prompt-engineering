from __future__ import annotations

import argparse
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from common import DEFAULT_TASK, SimpleResponse, print_llm_result, resolve_text
from common import build_llm


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prompt Chaining example.")
    parser.add_argument("--task", help="Initial task.")
    parser.add_argument("--task-file", help="File containing the initial task.")
    parser.add_argument("--step", action="append", help="Chain step template using {input}.")
    parser.add_argument("--step-model", action="append", help="Model for the corresponding step.")
    parser.add_argument("--temperature", type=float, default=0)
    parser.add_argument("--output-file", help="Optional file to store the final chain result.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    steps = args.step or [
        "Extract the key requirements from the task below.\n\nInput:\n{input}",
        "Based on the extracted requirements, propose a concise solution.\n\nInput:\n{input}",
        "Write a final implementation plan from the solution below.\n\nInput:\n{input}",
    ]
    step_models = args.step_model or ["gpt-4o"] * len(steps)
    if len(step_models) != len(steps):
        raise ValueError("--step-model count must match --step count.")

    parser = StrOutputParser()
    current = task
    sections: list[str] = []

    for idx, (template, model_name) in enumerate(zip(steps, step_models), start=1):
        chain = PromptTemplate.from_template(template) | build_llm(model_name, args.temperature) | parser
        current = chain.invoke({"input": current})
        sections.append(f"## Step {idx} ({model_name})\n{current}")

    content = "# Prompt Chaining Result\n\n" + "\n\n".join(sections) + "\n"
    if args.output_file:
        Path(args.output_file).write_text(content, encoding="utf-8")
    print_llm_result("Prompt chaining pipeline", SimpleResponse(content))


if __name__ == "__main__":
    main()
