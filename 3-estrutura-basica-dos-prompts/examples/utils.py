from __future__ import annotations

from typing import Iterable, Mapping

from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


def _stringify_prompt(prompt_input) -> str:
    if isinstance(prompt_input, str):
        return prompt_input.strip()

    if isinstance(prompt_input, Iterable):
        lines: list[str] = []
        for item in prompt_input:
            if isinstance(item, tuple) and len(item) == 2:
                role, content = item
                lines.append(f"[{str(role).upper()}]\n{str(content).strip()}")
            elif isinstance(item, Mapping):
                role = item.get("role", "message")
                content = item.get("content", "")
                lines.append(f"[{str(role).upper()}]\n{str(content).strip()}")
            else:
                role = getattr(item, "type", "message")
                content = getattr(item, "content", str(item))
                lines.append(f"[{str(role).upper()}]\n{str(content).strip()}")
        return "\n\n".join(lines)

    return str(prompt_input).strip()


def print_llm_result(title: str, prompt_input, response, notes: str | None = None) -> None:
    console.rule(f"[bold yellow]{title}")
    console.print(Text("PROMPT:", style="bold green"))
    console.print(Text(_stringify_prompt(prompt_input), style="bold blue"), end="\n\n")

    console.print(Text("LLM RESPONSE:", style="bold green"))
    console.print(Text(getattr(response, "content", str(response)), style="bold blue"), end="\n\n")

    usage = getattr(response, "response_metadata", {}).get("token_usage", {})
    if usage:
        console.print(
            f"[bold white]Input tokens:[/bold white] [bright_black]{usage.get('prompt_tokens', '?')}[/bright_black]"
        )
        console.print(
            f"[bold white]Output tokens:[/bold white] [bright_black]{usage.get('completion_tokens', '?')}[/bright_black]"
        )
        console.print(
            f"[bold white]Total tokens:[/bold white] [bright_black]{usage.get('total_tokens', '?')}[/bright_black]"
        )

    if notes:
        console.print(Text("LEITURA:", style="bold green"))
        console.print(Text(notes.strip(), style="bold white"))


def print_metric_table(title: str, rows: list[dict[str, str]]) -> None:
    table = Table(title=title)
    table.add_column("Variante", style="bold cyan")
    table.add_column("Latência (s)", justify="right")
    table.add_column("Input", justify="right")
    table.add_column("Output", justify="right")
    table.add_column("Total", justify="right")

    for row in rows:
        table.add_row(
            row["name"],
            row["latency"],
            row["input_tokens"],
            row["output_tokens"],
            row["total_tokens"],
        )

    console.print(table)
