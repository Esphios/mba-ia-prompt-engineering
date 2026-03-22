from __future__ import annotations

import argparse
from pathlib import Path

from prompt_advisor import (
    DEFAULT_ADVISOR_MODEL,
    DEFAULT_ADVISOR_TEMPERATURE,
    analyze_problem,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sugere técnicas de prompt com apoio de IA, após higienizar e enriquecer o problema."
    )
    parser.add_argument("--task", help="Problema ou tarefa a analisar.")
    parser.add_argument("--task-file", help="Arquivo com a tarefa.")
    parser.add_argument("--top", type=int, default=3, help="Quantidade de sugestões a exibir.")
    parser.add_argument("--model", default=DEFAULT_ADVISOR_MODEL, help="Modelo usado pelo advisor.")
    parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_ADVISOR_TEMPERATURE,
        help="Temperatura usada pelo advisor.",
    )
    parser.add_argument("--branch-factor", type=int, default=3, help="Quantidade de ramos iniciais no ToT.")
    parser.add_argument("--beam-width", type=int, default=2, help="Quantidade de ramos refinados.")
    parser.add_argument("--finalists", type=int, default=2, help="Quantidade de finalistas da decisão.")
    return parser.parse_args()


def resolve_task(task: str | None, task_file: str | None) -> str:
    if task_file:
        return Path(task_file).read_text(encoding="utf-8").strip()
    if task:
        return task.strip()
    raise ValueError("Informe --task ou --task-file.")


def main() -> None:
    args = parse_args()
    task = resolve_task(args.task, args.task_file)
    analysis = analyze_problem(
        task,
        model=args.model,
        temperature=args.temperature,
        branch_factor=args.branch_factor,
        beam_width=args.beam_width,
        finalists=args.finalists,
    )
    recommendations = analysis.recommendations[: args.top]

    print("# Sugestões de Técnica")
    print()
    print("Problema original:")
    print(task)
    print()
    print("Problema higienizado:")
    print(analysis.preparation.normalized_problem)
    print()
    print("Problema enriquecido:")
    print(analysis.preparation.enriched_problem)
    print()

    if analysis.preparation.explicit_constraints:
        print("Restrições explícitas:")
        for item in analysis.preparation.explicit_constraints:
            print(f"- {item}")
        print()

    if analysis.preparation.implied_constraints:
        print("Restrições implícitas:")
        for item in analysis.preparation.implied_constraints:
            print(f"- {item}")
        print()

    if analysis.preparation.expected_output:
        print("Saída esperada:")
        for item in analysis.preparation.expected_output:
            print(f"- {item}")
        print()

    if analysis.preparation.missing_information:
        print("Informações faltantes:")
        for item in analysis.preparation.missing_information:
            print(f"- {item}")
        print()

    if analysis.preparation.safe_assumptions:
        print("Suposições seguras:")
        for item in analysis.preparation.safe_assumptions:
            print(f"- {item}")
        print()

    print("Decisão final do advisor:")
    print(analysis.selection_rationale)
    print()

    for index, recommendation in enumerate(recommendations, start=1):
        print(f"## {index}. {recommendation.technique.label}")
        print(f"- Score sugerido pela IA: {recommendation.score}")
        print(f"- Motivo: {recommendation.reason}")
        print(f"- Script: {recommendation.technique.script_name}")
        if recommendation.cautions:
            print("- Cuidados:")
            for caution in recommendation.cautions:
                print(f"  - {caution}")
        print("- Comando direto:")
        print(f"  {recommendation.direct_command()}")
        print("- Comando via runner:")
        print(f"  {recommendation.runner_command()}")
        print()

    if analysis.usage_notes:
        print("Notas finais:")
        for item in analysis.usage_notes:
            print(f"- {item}")
        print()


if __name__ == "__main__":
    main()
