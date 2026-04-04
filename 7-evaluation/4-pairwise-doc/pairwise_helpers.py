"""Helpers for documentation pairwise evaluation."""
from typing import Any, Dict, Optional, Sequence

from langsmith.evaluation import comparison_evaluator
from langsmith.schemas import Example, Run

from shared.parsers import coerce_text_content, parse_json_response


def create_pairwise_judge(judge_prompt_obj, oai_client):
    """
    Create pairwise judge with detailed reasoning for documentation quality.

    Similar to 3-pairwise but handles structured JSON responses with reasoning.

    Args:
        judge_prompt_obj: Judge prompt template
        oai_client: OpenAI client

    Returns:
        Evaluator function for evaluate_comparative
    """
    from shared.clients import get_model_name, get_temperature

    @comparison_evaluator
    def pairwise_judge(runs: Sequence[Run], example: Optional[Example] = None) -> dict:
        """Pairwise judge with reasoning."""
        if len(runs) != 2:
            raise ValueError("Pairwise evaluation requires exactly 2 runs.")

        example_inputs = example.inputs or {} if example else {}
        outputs_a = runs[0].outputs or {}
        outputs_b = runs[1].outputs or {}
        code = example_inputs.get("files", "")
        answer_a = outputs_a.get("output", "")
        answer_b = outputs_b.get("output", "")
        reference_outputs = example.outputs if example else {}
        reference = reference_outputs.get("reference", "") if reference_outputs else ""

        # Format judge prompt
        judge_prompt = judge_prompt_obj.format(
            code=code,
            answer_a=answer_a,
            answer_b=answer_b,
            reference=reference
        )

        # Get judge response
        response = oai_client.chat.completions.create(
            messages=[{"role": "user", "content": judge_prompt}],
            model=get_model_name(),
            temperature=get_temperature()
        )

        full_response = coerce_text_content(response.choices[0].message.content).strip()

        # Try to parse structured response
        try:
            result = parse_json_response(full_response)
            decision = result.get("decision", "").upper()
            reasoning = result.get("reasoning", {})

            # Format reasoning for display
            comment = format_reasoning_as_text(decision, reasoning)
            run_id_a = str(runs[0].id)
            run_id_b = str(runs[1].id)

            if decision == "A":
                scores = {run_id_a: 1.0, run_id_b: 0.0}
            elif decision == "B":
                scores = {run_id_a: 0.0, run_id_b: 1.0}
            else:
                scores = {run_id_a: 0.5, run_id_b: 0.5}

            return {
                "key": "ranked_preference",
                "scores": scores,
                "comment": comment
            }

        except Exception:
            # Fallback if JSON parsing fails
            decision = full_response.upper()
            run_id_a = str(runs[0].id)
            run_id_b = str(runs[1].id)

            if "A" in decision and "B" not in decision:
                scores = {run_id_a: 1.0, run_id_b: 0.0}
            elif "B" in decision and "A" not in decision:
                scores = {run_id_a: 0.0, run_id_b: 1.0}
            else:
                scores = {run_id_a: 0.5, run_id_b: 0.5}

            return {
                "key": "ranked_preference",
                "scores": scores,
                "comment": f"[Fallback] {full_response[:200]}"
            }

    return pairwise_judge


def format_reasoning_as_text(decision: str, reasoning: Dict[str, Any]) -> str:
    """
    Format structured reasoning dictionary as human-readable text.

    Args:
        decision: Judge decision ("A", "B", or "TIE")
        reasoning: Reasoning dictionary with scores and justifications

    Returns:
        Formatted text string
    """
    lines = [f"DECISION: {decision}", ""]

    # Total scores
    if "score_total_a" in reasoning and "score_total_b" in reasoning:
        lines.append("TOTAL SCORES:")
        lines.append(f"- Prompt A: {reasoning['score_total_a']}/50")
        lines.append(f"- Prompt B: {reasoning['score_total_b']}/50")
        lines.append("")

    # Dimension breakdown
    lines.append("METRIC BREAKDOWN:")
    lines.append("")

    dimensions = [
        ("structural_completeness", "STRUCTURAL COMPLETENESS"),
        ("technical_precision", "TECHNICAL PRECISION"),
        ("clarity_and_utility", "CLARITY AND UTILITY"),
        ("reference_alignment", "REFERENCE ALIGNMENT"),
        ("conciseness_vs_detail", "CONCISENESS VS DETAIL")
    ]

    for key, label in dimensions:
        if key in reasoning:
            dim = reasoning[key]
            score_a = dim.get("score_a", "N/A")
            score_b = dim.get("score_b", "N/A")
            justification = dim.get("justification", "N/A")

            lines.append(f"{label}:")
            lines.append(f"   - Score A: {score_a}/10")
            lines.append(f"   - Score B: {score_b}/10")
            lines.append(f"   - Justification: {justification}")
            lines.append("")

    # Final decision
    if "final_decision" in reasoning:
        lines.append("FINAL DECISION:")
        lines.append(reasoning["final_decision"])

    return "\n".join(lines)
