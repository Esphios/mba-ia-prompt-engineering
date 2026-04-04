"""LLM and observability platform clients."""
import importlib
import os
from typing import Any

from langfuse import Langfuse
from langsmith import Client as LangSmithClient
from langsmith.wrappers import wrap_openai
from openai import OpenAI
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False

# Load environment variables
load_dotenv()


def get_openai_client() -> Any:
    """
    Returns OpenAI client with LangSmith tracing.

    Model and temperature are configurable via environment variables:
    - LLM_MODEL (default: gpt-4o-mini)
    - LLM_TEMPERATURE (default: 0)

    Returns:
        OpenAI client wrapped with LangSmith tracing
    """
    return wrap_openai(OpenAI())


def get_model_name() -> str:
    """
    Get configured model name from environment.

    Returns:
        Model name (default: gpt-4o-mini)
    """
    return os.getenv("LLM_MODEL", "gpt-4o-mini")


def get_temperature() -> float:
    """
    Get configured temperature from environment.

    Returns:
        Temperature value (default: 0)
    """
    return float(os.getenv("LLM_TEMPERATURE", "0"))


def get_langsmith_client() -> LangSmithClient:
    """
    Returns LangSmith client.

    Returns:
        LangSmith Client instance
    """
    return LangSmithClient()


def get_langfuse_client() -> Langfuse:
    """
    Returns Langfuse client.

    Returns:
        Langfuse client instance
    """
    return Langfuse()


def get_openai_client_langfuse() -> Any:
    """
    Returns OpenAI client with Langfuse tracing.

    Model and temperature are configurable via environment variables:
    - LLM_MODEL (default: gpt-4o-mini)
    - LLM_TEMPERATURE (default: 0)

    Returns:
        OpenAI client wrapped with Langfuse tracing
    """
    langfuse_openai = importlib.import_module("langfuse.openai")

    return getattr(langfuse_openai, "OpenAI")()
