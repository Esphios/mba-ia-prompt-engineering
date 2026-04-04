"""Correctness evaluation for Go code analyzer using Langfuse with LangChain."""
from datetime import datetime
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from langfuse.langchain import CallbackHandler
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from shared.clients import get_langfuse_client
from shared.parsers import coerce_text_content, parse_json_response
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
import yaml
import os

load_dotenv()

langfuse = get_langfuse_client()

DATASET_NAME = "go-ds"
PROMPT_FILE = "prompts/1-correctness-langfuse.yaml"
timestamp = datetime.now().strftime("%H%M")

script_dir = os.path.dirname(os.path.abspath(__file__))


def load_prompt_from_yaml(filename):
    """Load prompt from YAML file and convert to ChatPromptTemplate."""
    with open(os.path.join(script_dir, filename), "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    messages = [(msg["role"], msg["content"]) for msg in config["messages"]]
    return ChatPromptTemplate.from_messages(messages)


# Load prompt from YAML
prompt = load_prompt_from_yaml(PROMPT_FILE)

# Create LLM and chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = prompt | llm


def compare_findings(predicted, expected):
    """Compare findings by type and severity only."""
    pred_set = {(f.get("type", ""), f.get("severity", "")) for f in predicted}
    exp_set = {(f.get("type", ""), f.get("severity", "")) for f in expected}

    matched = len(pred_set & exp_set)
    total = len(exp_set)

    return matched / total if total > 0 else 0


if __name__ == "__main__":
    dataset = langfuse.get_dataset(DATASET_NAME)

    for idx, item in enumerate(dataset.items, 1):
        langfuse_handler = CallbackHandler()

        response = chain.invoke(
            item.input,
            config={
                "callbacks": [langfuse_handler],
                "run_name": f"1-correctness-eval_{timestamp}_item_{idx}"
            }
        )

        # Parse findings
        parsed = parse_json_response(coerce_text_content(response.content))
        predicted_findings = parsed.get("findings", []) if parsed else []
        expected_output = item.expected_output or {}
        expected_findings = expected_output.get("findings", [])

        # Calculate score
        score = compare_findings(predicted_findings, expected_findings)

        # Register score using the trace created by the handler
        trace_id = langfuse_handler.last_trace_id
        if trace_id:
            langfuse.create_score(
                trace_id=trace_id,
                name="Code findings",
                value=score,
                data_type="NUMERIC"
            )
