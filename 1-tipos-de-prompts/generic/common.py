from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from langchain_openai import ChatOpenAI


CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.append(str(PARENT_DIR))

from utils import print_llm_result  # noqa: E402


DEFAULT_TASK = "Explain recursion in simple terms with one example."


class SimpleResponse:
    def __init__(self, content: str):
        self.content = content
        self.response_metadata = {
            "token_usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0,
            }
        }


def resolve_text(inline_text: str | None, file_path: str | None, default: str) -> str:
    if file_path:
        return Path(file_path).read_text(encoding="utf-8").strip()
    if inline_text:
        return inline_text.strip()
    return default.strip()


def build_llm(model: str, temperature: float) -> ChatOpenAI:
    return ChatOpenAI(model=model, temperature=temperature)


def resolve_message_text(content: Any) -> str:
    """Normalize LangChain/OpenAI message content into plain text."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part for part in parts if part)

    return str(content)
