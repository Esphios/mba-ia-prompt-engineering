"""
Demonstrates best F1 SCORE (balance between Precision and Recall).
"""
from langsmith import evaluate
from langsmith.evaluation.evaluator import EvaluationResults
from langsmith.schemas import Example, Run
from pathlib import Path
import sys
from typing import Sequence

BASE_DIR = Path(__file__).resolve().parent
PARENT_DIR = BASE_DIR.parent
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from shared.clients import get_openai_client
from shared.prompts import load_yaml_prompt, execute_text_prompt
from metrics import calculate_precision_recall_f1, extract_findings_comparable

# Configuration
DATASET_NAME = "evaluation_precision_dataset"
BASE_DIR = Path(__file__).parent

# Setup
oai_client = get_openai_client()
prompt = load_yaml_prompt("balanced.yaml")


def run_balanced_analysis(inputs: dict) -> dict:
    """Target function for evaluate()."""
    return execute_text_prompt(prompt, inputs, oai_client, input_key="code")


def bug_detection_summary(
    runs: Sequence[Run],
    examples: Sequence[Example],
) -> EvaluationResults:
    """
    Summary evaluator comparing (type, severity) pairs.

    A finding is correct only if BOTH type AND severity match.
    This ensures fair evaluation of bug detection quality.
    """
    def extract_expected(example: Example):
        findings = set()
        expected_outputs = example.outputs or {}
        for f in expected_outputs.get("expected_findings", []):
            finding_tuple = (
                f["type"],
                f["severity"].lower()
            )
            findings.add(finding_tuple)
        return findings

    return calculate_precision_recall_f1(
        list(runs),
        list(examples),
        extract_predicted=extract_findings_comparable,
        extract_expected=extract_expected
    )


if __name__ == "__main__":
    # Run evaluation using balanced prompt
    results = evaluate(
        run_balanced_analysis,
        data=DATASET_NAME,
        evaluators=[],
        summary_evaluators=[bug_detection_summary],
        experiment_prefix="Balanced_BestF1",
        max_concurrency=2
    )

    print(f"Experiment: {results.experiment_name}")
    print("\nStrategy: Balanced (best F1 score)")
    print("Balance between precision and recall with standardized nomenclature")
