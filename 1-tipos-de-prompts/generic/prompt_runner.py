from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from prompt_advisor import (
    DEFAULT_ADVISOR_MODEL,
    DEFAULT_ADVISOR_TEMPERATURE,
    analyze_problem,
    available_techniques,
    get_technique,
)


CURRENT_DIR = Path(__file__).resolve().parent


def add_common_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task", help="Tarefa principal.")
    parser.add_argument("--task-file", help="Arquivo com a tarefa.")
    parser.add_argument("--model", help="Modelo a usar.")
    parser.add_argument("--temperature", type=float, help="Temperatura do modelo.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Runner para executar ou sugerir tecnicas de prompt da pasta generic."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list", help="Lista as tecnicas disponiveis.")
    list_parser.set_defaults(handler=handle_list)

    suggest_parser = subparsers.add_parser("suggest", help="Sugere tecnicas para um problema.")
    suggest_parser.add_argument("--task", help="Problema ou tarefa.")
    suggest_parser.add_argument("--task-file", help="Arquivo com a tarefa.")
    suggest_parser.add_argument("--top", type=int, default=3, help="Quantidade de sugestoes.")
    suggest_parser.add_argument("--model", default=DEFAULT_ADVISOR_MODEL, help="Modelo usado pelo advisor.")
    suggest_parser.add_argument(
        "--temperature",
        type=float,
        default=DEFAULT_ADVISOR_TEMPERATURE,
        help="Temperatura usada pelo advisor.",
    )
    suggest_parser.add_argument("--branch-factor", type=int, default=3, help="Quantidade de ramos iniciais no ToT.")
    suggest_parser.add_argument("--beam-width", type=int, default=2, help="Quantidade de ramos refinados.")
    suggest_parser.add_argument("--finalists", type=int, default=2, help="Quantidade de finalistas.")
    suggest_parser.set_defaults(handler=handle_suggest)

    run_parser = subparsers.add_parser("run", help="Executa um dos scripts da pasta.")
    run_parser.add_argument("--technique", required=True, choices=[item.key for item in available_techniques()])
    add_common_arguments(run_parser)
    run_parser.add_argument("--role", help="Role/persona.")
    run_parser.add_argument("--role-file", help="Arquivo com role/persona.")
    run_parser.add_argument("--instruction", help="Instrucao para one-shot/few-shot.")
    run_parser.add_argument("--example", action="append", help="Exemplo adicional.")
    run_parser.add_argument("--example-file", action="append", help="Arquivo contendo um exemplo.")
    run_parser.add_argument("--answer-label", help="Marcador da resposta final.")
    run_parser.add_argument("--samples", type=int, help="Numero de amostras.")
    run_parser.add_argument("--problem", help="Problema para ToT.")
    run_parser.add_argument("--problem-file", help="Arquivo com problema para ToT.")
    run_parser.add_argument("--criterion", action="append", help="Criterio no formato nome:peso:descricao.")
    run_parser.add_argument("--max-depth", type=int, help="Profundidade maxima da arvore.")
    run_parser.add_argument("--branch-factor", type=int, help="Numero de ramos por nivel.")
    run_parser.add_argument("--beam-width", type=int, help="Quantidade de ramos mantidos por nivel.")
    run_parser.add_argument("--finalists", type=int, help="Quantidade de finalistas.")
    run_parser.add_argument("--bullet-range", help='Faixa de bullets do esqueleto, ex: "3 to 7".')
    run_parser.add_argument("--context", help="Contexto adicional.")
    run_parser.add_argument("--context-file", help="Arquivo com contexto adicional.")
    run_parser.add_argument("--step", action="append", help="Template de etapa para prompt chaining.")
    run_parser.add_argument("--step-model", action="append", help="Modelo por etapa em prompt chaining.")
    run_parser.add_argument("--output-file", help="Arquivo de saida.")
    run_parser.set_defaults(handler=handle_run)

    return parser


def resolve_task(task: str | None, task_file: str | None) -> str:
    if task_file:
        return Path(task_file).read_text(encoding="utf-8").strip()
    if task:
        return task.strip()
    raise ValueError("Informe --task ou --task-file.")


def add_flag(args: list[str], flag: str, value: object | None) -> None:
    if value is None:
        return
    args.extend([flag, str(value)])


def add_repeatable_flag(args: list[str], flag: str, values: list[str] | None) -> None:
    if not values:
        return
    for value in values:
        args.extend([flag, value])


def build_run_command(args: argparse.Namespace) -> list[str]:
    technique = get_technique(args.technique)
    command = [sys.executable, str(CURRENT_DIR / technique.script_name)]

    if args.technique == "tot":
        add_flag(command, "--problem", args.problem or args.task)
        add_flag(command, "--problem-file", args.problem_file or args.task_file)
    else:
        add_flag(command, "--task", args.task)
        add_flag(command, "--task-file", args.task_file)

    add_flag(command, "--model", args.model)
    add_flag(command, "--temperature", args.temperature)

    if args.technique == "role":
        add_flag(command, "--role", args.role)
        add_flag(command, "--role-file", args.role_file)
    elif args.technique == "few-shot":
        add_flag(command, "--instruction", args.instruction)
        add_repeatable_flag(command, "--example", args.example)
        add_repeatable_flag(command, "--example-file", args.example_file)
    elif args.technique == "cot":
        add_flag(command, "--answer-label", args.answer_label)
    elif args.technique == "self-consistency":
        add_flag(command, "--samples", args.samples)
        add_flag(command, "--answer-label", args.answer_label)
    elif args.technique == "tot":
        add_repeatable_flag(command, "--criterion", args.criterion)
        add_flag(command, "--max-depth", args.max_depth)
        add_flag(command, "--branch-factor", args.branch_factor)
        add_flag(command, "--beam-width", args.beam_width)
        add_flag(command, "--finalists", args.finalists)
    elif args.technique == "sot":
        add_flag(command, "--bullet-range", args.bullet_range)
    elif args.technique == "react":
        add_flag(command, "--context", args.context)
        add_flag(command, "--context-file", args.context_file)
    elif args.technique == "chaining":
        add_repeatable_flag(command, "--step", args.step)
        add_repeatable_flag(command, "--step-model", args.step_model)
        add_flag(command, "--output-file", args.output_file)

    return command


def handle_list(_: argparse.Namespace) -> int:
    print("# Tecnicas disponiveis")
    print()
    for technique in available_techniques():
        print(f"- {technique.key}: {technique.label} -> {technique.script_name}")
    return 0


def handle_suggest(args: argparse.Namespace) -> int:
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

    print("# Sugestoes")
    print()
    print("Problema original:")
    print(task)
    print()
    print("Problema enriquecido:")
    print(analysis.preparation.enriched_problem)
    print()
    print("Decisao final do advisor:")
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
    return 0


def handle_run(args: argparse.Namespace) -> int:
    command = build_run_command(args)
    completed = subprocess.run(command, check=False)
    return completed.returncode


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(args.handler(args))


if __name__ == "__main__":
    main()
