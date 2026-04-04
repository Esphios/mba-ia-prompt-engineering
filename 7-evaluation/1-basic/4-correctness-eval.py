"""
Correctness evaluation: Comparing predictions against reference outputs.

Demonstrates labeled evaluators that use reference outputs for comparison.
"""
from langsmith import evaluate
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from shared.clients import get_openai_client
from shared.prompts import load_yaml_prompt, execute_text_prompt
from shared.evaluators import create_run_evaluator, prepare_with_reference

# Configuration
DATASET_NAME = "evaluation_basic_dataset"
BASE_DIR = Path(__file__).parent

# Setup
oai_client = get_openai_client()
prompt = load_yaml_prompt("correctness_eval.yaml")


def run_correctness_evaluation(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, oai_client, input_key="code")


# Labeled evaluators with reference outputs
evaluators = [
    create_run_evaluator(
        "labeled_score_string",
        config={"criteria": "correctness", "normalize_by": 10},
        prepare_data=prepare_with_reference
    ),
    create_run_evaluator(
        "labeled_score_string",
        config={"criteria": "relevance", "normalize_by": 10},
        prepare_data=prepare_with_reference
    )
]

# Run evaluation
results = evaluate(
    run_correctness_evaluation,
    data=DATASET_NAME,
    evaluators=evaluators,
    experiment_prefix="CorrectnessEval",
    max_concurrency=2
)

print("="*80)
print(f"EXPERIMENT: {results.experiment_name}")
print("="*80)
