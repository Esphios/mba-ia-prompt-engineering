from __future__ import annotations

import argparse
import json
from collections import Counter

from dotenv import load_dotenv

from common import DEFAULT_TASK, SimpleResponse, build_llm, print_llm_result, resolve_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CoT with self-consistency example.")
    parser.add_argument("--task", help="Task to solve.")
    parser.add_argument("--task-file", help="File containing the task.")
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--answer-label", default="Answer:")
    parser.add_argument("--model", default="gpt-4o")
    parser.add_argument("--temperature", type=float, default=0.7)
    return parser.parse_args()


def extract_answer(text: str, marker: str) -> str:
    if marker in text:
        return text.split(marker, 1)[1].strip().splitlines()[0].strip()
    return text.strip().splitlines()[-1].strip()


def main() -> None:
    args = parse_args()
    load_dotenv()

    task = resolve_text(args.task, args.task_file, DEFAULT_TASK)
    prompt = f"""
Solve the task below.
Generate one full reasoning path.
At the end, write the final answer after "{args.answer_label}".

Task:
{task}
"""

    llm = build_llm(args.model, args.temperature)
    samples: list[str] = []
    final_answers: list[str] = []
    for _ in range(args.samples):
        response = llm.invoke(prompt)
        samples.append(response.content)
        final_answers.append(extract_answer(response.content, args.answer_label))

    counts = Counter(final_answers)
    chosen_answer, votes = counts.most_common(1)[0]
    if votes == 1 and len(counts) == len(final_answers):
        chosen_answer = "I can't find a consistent answer"

    content = (
        "SELF-CONSISTENCY RUN\n\n"
        + "\n\n".join(f"Sample {idx + 1}:\n{sample}" for idx, sample in enumerate(samples))
        + "\n\nSummary:\n"
        + json.dumps(
            {
                "answers": final_answers,
                "vote_counts": dict(counts),
                "chosen_answer": chosen_answer,
            },
            indent=2,
            ensure_ascii=True,
        )
    )
    print_llm_result(prompt, SimpleResponse(content))


if __name__ == "__main__":
    main()
