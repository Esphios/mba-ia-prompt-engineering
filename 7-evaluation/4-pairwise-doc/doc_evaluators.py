"""Documentation-specific evaluators."""
from typing import Optional

from langsmith.schemas import Example, Run

from shared.evaluators import EvaluatorInput, create_run_evaluator


def create_evaluators_for_documentation():
    """
    Create suite of evaluators for documentation quality assessment.

    Returns 7 specialized evaluators that measure:
    1. Conciseness alignment with reference
    2. Detail level alignment with reference
    3. Tone and style alignment with reference
    4. Structure alignment with reference
    5. Content coverage alignment with reference
    6. Terminology consistency with reference
    7. Faithfulness to source code

    Returns:
        List of LangChainStringEvaluator instances

    Example:
        >>> evaluators = create_evaluators_for_documentation()
        >>> results = evaluate(
        ...     run_function,
        ...     data=dataset,
        ...     evaluators=evaluators
        ... )
    """
    def prepare_data_with_reference(
        run: Run,
        example: Optional[Example],
    ) -> EvaluatorInput:
        """Prepare data with reference for comparison."""
        example_inputs = example.inputs or {} if example else {}
        example_outputs = example.outputs or {} if example else {}
        return {
            "prediction": (run.outputs or {}).get("output", ""),
            "input": str(example_inputs.get("files", "")),
            "reference": str(example_outputs.get("reference", "")),
        }

    def prepare_data(run: Run, example: Optional[Example]) -> EvaluatorInput:
        """Prepare data without reference."""
        example_inputs = example.inputs or {} if example else {}
        return {
            "prediction": (run.outputs or {}).get("output", ""),
            "input": str(example_inputs.get("files", "")),
            "reference": None,
        }

    return [
        # 1. Conciseness alignment
        create_run_evaluator(
            "labeled_score_string",
            config={
                "criteria": {
                    "conciseness_alignment": (
                        "Does the prediction match the same verbosity level as the reference? "
                        "If reference is verbose (many sentences, detailed explanations), "
                        "prediction should also be verbose. If reference is concise "
                        "(few sentences, brief), prediction should also be concise. "
                        "Compare STYLES, not judging quality."
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data_with_reference
        ),

        # 2. Detail level alignment
        create_run_evaluator(
            "labeled_score_string",
            config={
                "criteria": {
                    "detail_alignment": (
                        "Does the prediction match the same technical detail level as the reference? "
                        "If reference includes technical details (types, parameters, code examples), "
                        "prediction should also include them. If reference is high-level "
                        "(concepts only), prediction should also be high-level. "
                        "Compare DEPTH, not judging quality."
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data_with_reference
        ),

        # 3. Tone and style alignment
        create_run_evaluator(
            "labeled_score_string",
            config={
                "criteria": {
                    "tone_style_alignment": (
                        "Does the prediction match the same tone and writing style as the reference? "
                        "Compare formality level (formal vs informal), language complexity "
                        "(technical jargon vs accessible), and format (narrative paragraphs vs "
                        "bullet points). Compare STYLE, not judging quality."
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data_with_reference
        ),

        # 4. Structure alignment
        create_run_evaluator(
            "labeled_score_string",
            config={
                "criteria": {
                    "structure_alignment": (
                        "Does the prediction follow the SAME STRUCTURE as the reference? "
                        "Same sections (e.g., Context, Objectives, Technologies, Critical Points)? "
                        "Same order? Same hierarchy (##, ###, ####)? "
                        "Compare section headers and organization."
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data_with_reference
        ),

        # 5. Content coverage
        create_run_evaluator(
            "labeled_score_string",
            config={
                "criteria": {
                    "content_coverage": (
                        "Does the prediction cover the SAME TOPICS as the reference? "
                        "If reference mentions 'Critical Points' (e.g., SQL injection, missing cache), "
                        "prediction should cover these. If reference lists specific technologies, "
                        "prediction should list them. Compare topic coverage."
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data_with_reference
        ),

        # 6. Terminology consistency
        create_run_evaluator(
            "labeled_score_string",
            config={
                "criteria": {
                    "terminology_consistency": (
                        "Does the prediction use the SAME TERMINOLOGY as the reference? "
                        "Same technical terms, same naming conventions, same abbreviations "
                        "(e.g., 'Text2SQL' vs 'text to SQL'). Compare vocabulary and "
                        "technical language."
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data_with_reference
        ),

        # 7. Faithfulness to code
        create_run_evaluator(
            "score_string",
            config={
                "criteria": {
                    "faithfulness": (
                        "Is the documentation grounded ONLY in the provided code? "
                        "Doesn't invent features, classes, or functionality that don't exist "
                        "in the code? Doesn't add assumptions about code behavior that "
                        "wasn't shown?"
                    )
                },
                "normalize_by": 10
            },
            prepare_data=prepare_data
        ),
    ]
