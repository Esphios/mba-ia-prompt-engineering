"""Helpers for pairwise evaluation."""
from typing import Optional, Sequence

from langsmith.evaluation import comparison_evaluator
from langsmith.schemas import Example, Run

from shared.parsers import coerce_text_content


def create_pairwise_evaluator(judge_prompt_obj, oai_client):
    """
    Create pairwise evaluator function for evaluate_comparative.

    Args:
        judge_prompt_obj: Judge prompt template (PromptTemplate)
        oai_client: OpenAI client

    Returns:
        Evaluator function with signature:
        (inputs: dict, outputs: list, reference_outputs: dict) -> list[float]

    The evaluator returns:
    - [1.0, 0.0] if A is better
    - [0.0, 1.0] if B is better
    - [0.5, 0.5] if tie

    Example:
        >>> from shared.prompts import load_yaml_prompt
        >>> from shared.clients import get_openai_client
        >>>
        >>> judge = load_yaml_prompt("pairwise_judge.yaml")
        >>> client = get_openai_client()
        >>> evaluator = create_pairwise_evaluator(judge, client)
        >>>
        >>> # Use in evaluate_comparative
        >>> results = evaluate_comparative(
        ...     [exp_a, exp_b],
        ...     evaluators=[evaluator]
        ... )
    """
    from shared.clients import get_model_name, get_temperature

    @comparison_evaluator
    def evaluate_pairwise(runs: Sequence[Run], example: Optional[Example] = None) -> dict:
        """Pairwise comparison evaluator."""
        if len(runs) != 2:
            raise ValueError("Pairwise evaluation requires exactly 2 runs.")

        example_inputs = example.inputs or {} if example else {}
        outputs_a = runs[0].outputs or {}
        outputs_b = runs[1].outputs or {}
        code = example_inputs.get("code", "")
        answer_a = outputs_a.get("output", "")
        answer_b = outputs_b.get("output", "")

        # Format judge prompt
        judge_prompt = judge_prompt_obj.format(
            code=code,
            answer_a=answer_a,
            answer_b=answer_b
        )

        # Get judge decision
        response = oai_client.chat.completions.create(
            messages=[{"role": "user", "content": judge_prompt}],
            model=get_model_name(),
            temperature=get_temperature()
        )

        decision = coerce_text_content(response.choices[0].message.content).strip().upper()

        # Parse decision
        if "A" in decision and "B" not in decision:
            scores = {str(runs[0].id): 1.0, str(runs[1].id): 0.0}
        elif "B" in decision and "A" not in decision:
            scores = {str(runs[0].id): 0.0, str(runs[1].id): 1.0}
        else:
            scores = {str(runs[0].id): 0.5, str(runs[1].id): 0.5}

        return {"key": "ranked_preference", "scores": scores}

    return evaluate_pairwise
