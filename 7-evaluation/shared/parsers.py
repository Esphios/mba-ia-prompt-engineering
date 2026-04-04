"""JSON and markdown parsing utilities."""
import json
from typing import Any, Dict


def coerce_text_content(content: Any) -> str:
    """Normalize text or multimodal content blocks into plain text."""
    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text")
                if isinstance(text, str):
                    parts.append(text)
        return "\n".join(part for part in parts if part)

    return str(content)


def parse_json_response(text: Any) -> Dict[str, Any]:
    """
    Parse JSON from LLM response, removing markdown blocks if present.

    LLMs often wrap JSON in markdown code blocks like:
    ```json
    {"key": "value"}
    ```

    This function handles both raw JSON and markdown-wrapped JSON.

    Args:
        text: Raw text from LLM (may contain markdown)

    Returns:
        Parsed dictionary, or empty dict {} if parsing fails

    Example:
        >>> parse_json_response('```json\\n{"a": 1}\\n```')
        {'a': 1}
        >>> parse_json_response('{"a": 1}')
        {'a': 1}
        >>> parse_json_response('invalid')
        {}
    """
    normalized_text = coerce_text_content(text).strip()

    # Remove markdown code blocks
    if normalized_text.startswith("```"):
        start = normalized_text.find("{")
        end = normalized_text.rfind("}") + 1
        if start != -1 and end > start:
            normalized_text = normalized_text[start:end]

    try:
        parsed = json.loads(normalized_text)
        return parsed if isinstance(parsed, dict) else {}
    except (json.JSONDecodeError, ValueError):
        return {}
