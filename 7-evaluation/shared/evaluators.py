"""Helper functions for creating prepare_data functions."""
from typing import Any, Callable, Dict, Optional

from langsmith.evaluation import LangChainStringEvaluator
from langsmith.evaluation.evaluator import RunEvaluator
from langsmith.evaluation.integrations._langchain import SingleEvaluatorInput
from langsmith.schemas import Example, Run

EvaluatorInput = SingleEvaluatorInput


def create_run_evaluator(
    evaluator: str,
    *,
    config: Optional[Dict[str, Any]] = None,
    prepare_data: Optional[Callable[[Run, Optional[Example]], SingleEvaluatorInput]] = None,
) -> RunEvaluator:
    """Create a LangChain evaluator converted to LangSmith RunEvaluator."""
    return LangChainStringEvaluator(
        evaluator,
        config=config,
        prepare_data=prepare_data,
    ).as_run_evaluator()


def prepare_prediction_only(run: Run, example: Optional[Example]) -> EvaluatorInput:
    """
    Prepare data with only prediction (for evaluators that don't need input/reference).

    Use for:
    - json_validity
    - json_schema

    Args:
        run: LangSmith run object
        example: Dataset example

    Returns:
        {"prediction": str}
    """
    outputs = run.outputs or {}
    return {
        "prediction": outputs.get("output", ""),
        "input": None,
        "reference": None,
    }


def prepare_with_input(
    run: Run,
    example: Optional[Example],
    input_key: str = "code",
) -> EvaluatorInput:
    """
    Prepare data with prediction + input (for evaluators without reference).

    Use for:
    - criteria (binary)
    - score_string (continuous)
    - Custom criteria

    Args:
        run: LangSmith run object
        example: Dataset example
        input_key: Key to extract from inputs (default: "code")

    Returns:
        {"prediction": str, "input": str}
    """
    outputs = run.outputs or {}
    example_inputs = example.inputs or {} if example else {}
    return {
        "prediction": outputs.get("output", ""),
        "input": str(example_inputs.get(input_key, "")),
        "reference": None,
    }


def prepare_with_reference(
    run: Run,
    example: Optional[Example],
    input_key: str = "code",
) -> EvaluatorInput:
    """
    Prepare data with prediction + input + reference (for labeled evaluators).

    Use for:
    - labeled_criteria
    - labeled_score_string
    - embedding_distance

    Args:
        run: LangSmith run object
        example: Dataset example
        input_key: Key to extract from inputs (default: "code")

    Returns:
        {"prediction": str, "input": str, "reference": dict}
    """
    outputs = run.outputs or {}
    example_inputs = example.inputs or {} if example else {}
    return {
        "prediction": outputs.get("output", ""),
        "input": str(example_inputs.get(input_key, "")),
        "reference": example.outputs if example else None,
    }
