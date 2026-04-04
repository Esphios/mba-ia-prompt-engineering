"""
Format evaluation: JSON validity and schema validation.

Demonstrates deterministic evaluation without LLM judges.
"""
from langsmith import evaluate
from pathlib import Path
import json
import jsonschema
import sys
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from shared.clients import get_openai_client
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.evaluators import create_run_evaluator, prepare_prediction_only
from langsmith.schemas import Example, Run

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
oai_client = get_openai_client()
prompt = load_yaml_prompt("format_eval.yaml")


def run_format_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, oai_client, input_key="code")


# JSON validity evaluator
json_eval = create_run_evaluator(
    "json_validity",
    prepare_data=prepare_prediction_only
)

# JSON schema validator
EXPECTED_SCHEMA = {
    "type": "object",
    "properties": {
        "findings": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "line": {"type": "number"},
                    "description": {"type": "string"},
                    "severity": {"type": "string"}
                },
                "required": ["type", "line", "description", "severity"]
            }
        },
        "summary": {"type": "string"}
    },
    "required": ["findings", "summary"]
}


def validate_schema(run: Run, example: Optional[Example]) -> dict:
    """Validate JSON against expected schema."""
    try:
        outputs = run.outputs or {}
        output = outputs.get("output", "")
        data = json.loads(output)
        jsonschema.validate(instance=data, schema=EXPECTED_SCHEMA)
        return {"score": 1.0, "comment": "Valid schema"}
    except json.JSONDecodeError as e:
        return {"score": 0.0, "comment": f"Invalid JSON: {str(e)}"}
    except jsonschema.ValidationError as e:
        return {"score": 0.0, "comment": f"Invalid schema: {e.message}"}


# Run evaluation
results = evaluate(
    run_format_evaluation,
    data=DATASET_NAME,
    evaluators=[json_eval, validate_schema],
    experiment_prefix="FormatEval",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)
