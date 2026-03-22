from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from pydantic import BaseModel, Field


DEFAULT_ADVISOR_MODEL = "gpt-4o"
DEFAULT_ADVISOR_TEMPERATURE = 0.2
DEFAULT_BRANCH_FACTOR = 3
DEFAULT_BEAM_WIDTH = 2
DEFAULT_FINALISTS = 2


@dataclass(frozen=True)
class TechniqueInfo:
    key: str
    label: str
    script_name: str
    summary: str


@dataclass(frozen=True)
class Recommendation:
    technique: TechniqueInfo
    score: int
    reason: str
    suggested_args: list[str]
    cautions: list[str]

    def direct_command(self) -> str:
        return shell_join(
            [
                r".\venv\Scripts\python.exe",
                fr".\1-tipos-de-prompts\generic\{self.technique.script_name}",
                *self.suggested_args,
            ]
        )

    def runner_command(self) -> str:
        return shell_join(
            [
                r".\venv\Scripts\python.exe",
                r".\1-tipos-de-prompts\generic\prompt_runner.py",
                "run",
                "--technique",
                self.technique.key,
                *self.suggested_args,
            ]
        )


@dataclass(frozen=True)
class ProblemPreparation:
    normalized_problem: str
    enriched_problem: str
    domain: str
    complexity: str
    explicit_constraints: list[str]
    implied_constraints: list[str]
    expected_output: list[str]
    missing_information: list[str]
    safe_assumptions: list[str]
    hygiene_notes: list[str]


@dataclass(frozen=True)
class AdvisorAnalysis:
    preparation: ProblemPreparation
    recommendations: list[Recommendation]
    selection_rationale: str
    usage_notes: list[str]


class PreparedProblemModel(BaseModel):
    normalized_problem: str = Field(description="Problema higienizado, sem ruído ou repetições desnecessárias.")
    enriched_problem: str = Field(description="Problema reescrito de forma mais clara, completa e autocontida.")
    domain: str = Field(description="Domínio principal do problema.")
    complexity: str = Field(description="Baixa, média ou alta complexidade, com uma breve justificativa.")
    explicit_constraints: list[str] = Field(description="Restrições explicitamente mencionadas pelo usuário.")
    implied_constraints: list[str] = Field(description="Restrições inferidas sem inventar fatos.")
    expected_output: list[str] = Field(description="Sinais sobre a saída esperada.")
    missing_information: list[str] = Field(description="Informações faltantes que afetam a escolha da técnica.")
    safe_assumptions: list[str] = Field(description="Suposições seguras e reversíveis para seguir adiante.")
    hygiene_notes: list[str] = Field(description="Ruídos, ambiguidades ou problemas corrigidos na higienização.")


class TechniqueSuggestionModel(BaseModel):
    technique_key: str = Field(description="Uma chave válida do catálogo de técnicas.")
    score: int = Field(ge=1, le=100, description="Pontuação relativa da técnica dentro do plano final.")
    reason: str = Field(description="Por que essa técnica é adequada ao problema.")
    suggested_args: list[str] = Field(
        description=(
            "Lista plana de tokens CLI para o script da técnica. Cada flag e cada valor deve ocupar um item separado. "
            "Não use aspas shell no conteúdo."
        )
    )
    cautions: list[str] = Field(description="Cuidados práticos ao usar a técnica nesse contexto.")


class CandidateBranchModel(BaseModel):
    branch_name: str = Field(description="Nome curto do ramo de decisão.")
    strategy_summary: str = Field(description="Resumo da estratégia recomendada por esse ramo.")
    recommended_techniques: list[TechniqueSuggestionModel] = Field(
        description="Técnicas recomendadas por este ramo, ordenadas da mais útil para a menos útil."
    )
    tradeoffs: list[str] = Field(description="Principais trade-offs do ramo.")


class CandidateBranchSetModel(BaseModel):
    candidates: list[CandidateBranchModel]


class BranchEvaluationModel(BaseModel):
    fit_to_problem: int = Field(ge=1, le=10)
    cost_efficiency: int = Field(ge=1, le=10)
    auditability: int = Field(ge=1, le=10)
    resilience_to_ambiguity: int = Field(ge=1, le=10)
    execution_readiness: int = Field(ge=1, le=10)
    rationale: str
    improvements: list[str]


class FinalPlanModel(BaseModel):
    selection_rationale: str = Field(description="Justificativa final da escolha.")
    usage_notes: list[str] = Field(description="Notas finais de uso.")
    recommended_techniques: list[TechniqueSuggestionModel] = Field(
        description="Técnicas finais escolhidas, ordenadas por prioridade."
    )


TECHNIQUES: dict[str, TechniqueInfo] = {
    "role": TechniqueInfo("role", "Role Prompting", "0-role-prompting.py", "Define papel, persona ou tom."),
    "zero-shot": TechniqueInfo("zero-shot", "Zero-shot", "1-zero-shot.py", "Executa a tarefa sem exemplos."),
    "few-shot": TechniqueInfo("few-shot", "One-shot / Few-shot", "2-one-few-shot.py", "Ensina padrão com exemplos."),
    "cot": TechniqueInfo("cot", "Chain of Thought", "3-cot.py", "Pede raciocínio passo a passo."),
    "self-consistency": TechniqueInfo(
        "self-consistency",
        "Self-Consistency",
        "3.1-self-consistency.py",
        "Executa várias amostras e escolhe a resposta mais consistente.",
    ),
    "tot": TechniqueInfo("tot", "Tree of Thought", "4-tot.py", "Explora alternativas e escolhe a melhor."),
    "sot": TechniqueInfo("sot", "Skeleton of Thought", "5-sot.py", "Cria um esqueleto antes de expandir."),
    "react": TechniqueInfo("react", "ReAct", "6-react.py", "Alterna Thought, Action e Observation."),
    "chaining": TechniqueInfo("chaining", "Prompt Chaining", "7-prompt-chaining.py", "Encadeia várias etapas."),
    "least-to-most": TechniqueInfo(
        "least-to-most",
        "Least-to-Most",
        "8-least-to-most.py",
        "Decompõe o problema do mais simples ao mais difícil.",
    ),
}


def available_techniques() -> Iterable[TechniqueInfo]:
    return TECHNIQUES.values()


def get_technique(key: str) -> TechniqueInfo:
    return TECHNIQUES[key]


def shell_quote(value: str) -> str:
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._/\\:=+"
    if value and all(char in safe_chars for char in value):
        return value
    return '"' + value.replace('"', '\\"') + '"'


def shell_join(tokens: list[str]) -> str:
    return " ".join(shell_quote(token) for token in tokens)


def technique_catalog_prompt() -> str:
    return "\n".join(
        f"- {item.key}: {item.label}. Script={item.script_name}. Uso típico: {item.summary}"
        for item in TECHNIQUES.values()
    )


def preparation_to_dataclass(model: PreparedProblemModel) -> ProblemPreparation:
    return ProblemPreparation(
        normalized_problem=model.normalized_problem,
        enriched_problem=model.enriched_problem,
        domain=model.domain,
        complexity=model.complexity,
        explicit_constraints=model.explicit_constraints,
        implied_constraints=model.implied_constraints,
        expected_output=model.expected_output,
        missing_information=model.missing_information,
        safe_assumptions=model.safe_assumptions,
        hygiene_notes=model.hygiene_notes,
    )


def weighted_branch_score(evaluation: BranchEvaluationModel) -> tuple[float, str]:
    weights = {
        "fit_to_problem": 0.30,
        "resilience_to_ambiguity": 0.20,
        "execution_readiness": 0.20,
        "auditability": 0.15,
        "cost_efficiency": 0.15,
    }
    total = (
        evaluation.fit_to_problem * weights["fit_to_problem"]
        + evaluation.resilience_to_ambiguity * weights["resilience_to_ambiguity"]
        + evaluation.execution_readiness * weights["execution_readiness"]
        + evaluation.auditability * weights["auditability"]
        + evaluation.cost_efficiency * weights["cost_efficiency"]
    )
    formula = (
        f"0.30*{evaluation.fit_to_problem} + "
        f"0.20*{evaluation.resilience_to_ambiguity} + "
        f"0.20*{evaluation.execution_readiness} + "
        f"0.15*{evaluation.auditability} + "
        f"0.15*{evaluation.cost_efficiency} = {total:.2f}"
    )
    return total, formula


def normalize_suggested_args(tokens: list[str]) -> list[str]:
    normalized: list[str] = []
    for token in tokens:
        compact = " ".join(token.split())
        if compact:
            normalized.append(compact)
    return normalized


def has_flag(tokens: list[str], flag: str) -> bool:
    return flag in tokens


def ensure_minimum_args(technique_key: str, tokens: list[str], preparation: ProblemPreparation) -> list[str]:
    enriched_problem = preparation.enriched_problem
    ensured = list(tokens)

    if technique_key == "tot":
        if not has_flag(ensured, "--problem") and not has_flag(ensured, "--problem-file"):
            ensured.extend(["--problem", enriched_problem])
    else:
        if not has_flag(ensured, "--task") and not has_flag(ensured, "--task-file"):
            ensured.extend(["--task", enriched_problem])

    if technique_key == "self-consistency" and not has_flag(ensured, "--samples"):
        ensured.extend(["--samples", "5"])
    if technique_key == "self-consistency" and not has_flag(ensured, "--answer-label"):
        ensured.extend(["--answer-label", "Answer:"])
    if technique_key == "cot" and not has_flag(ensured, "--answer-label"):
        ensured.extend(["--answer-label", "Answer:"])
    if technique_key == "react" and not has_flag(ensured, "--context") and not has_flag(ensured, "--context-file"):
        ensured.extend(
            [
                "--context",
                "Use apenas as evidências fornecidas. Se algo estiver faltando, diga isso explicitamente.",
            ]
        )
    if technique_key == "sot" and not has_flag(ensured, "--bullet-range"):
        ensured.extend(["--bullet-range", "4 to 6"])
    if technique_key == "chaining" and not has_flag(ensured, "--output-file"):
        ensured.extend(["--output-file", r".\1-tipos-de-prompts\generic\generic_chain_result.md"])

    return ensured


def normalize_recommendation(item: TechniqueSuggestionModel, preparation: ProblemPreparation) -> Recommendation | None:
    if item.technique_key not in TECHNIQUES:
        return None
    suggested_args = ensure_minimum_args(
        item.technique_key,
        normalize_suggested_args(item.suggested_args),
        preparation,
    )
    return Recommendation(
        technique=TECHNIQUES[item.technique_key],
        score=item.score,
        reason=item.reason,
        suggested_args=suggested_args,
        cautions=item.cautions,
    )


def dedupe_recommendations(items: list[TechniqueSuggestionModel], preparation: ProblemPreparation) -> list[Recommendation]:
    deduped: dict[str, Recommendation] = {}
    for item in items:
        recommendation = normalize_recommendation(item, preparation)
        if recommendation is None:
            continue
        current = deduped.get(recommendation.technique.key)
        if current is None or recommendation.score > current.score:
            deduped[recommendation.technique.key] = recommendation
    return sorted(deduped.values(), key=lambda entry: entry.score, reverse=True)


def sanitize_problem_input(problem: str) -> str:
    cleaned_lines = [line.strip() for line in problem.replace("\r\n", "\n").split("\n")]
    cleaned_lines = [line for line in cleaned_lines if line]
    return "\n".join(cleaned_lines).strip()


def prepare_problem(llm, raw_problem: str) -> ProblemPreparation:
    structured = llm.with_structured_output(PreparedProblemModel)
    prepared = structured.invoke(
        f"""
Você é um especialista em intake de problemas para prompt engineering.
Sua tarefa é higienizar e enriquecer o problema abaixo antes de qualquer decisão.

Regras:
- Preserve a intenção do usuário.
- Remova ruídos, duplicações, informalidades irrelevantes e ambiguidades evitáveis.
- Não invente requisitos factuais; se algo estiver faltando, registre em missing_information.
- Torne o problema mais autocontido, explícito e utilizável por outra IA.
- Separe restrições explícitas, restrições implícitas e suposições seguras.
- Destaque o tipo de saída esperada.

Problema bruto:
{raw_problem}
"""
    )
    return preparation_to_dataclass(prepared)


def generate_candidate_branches(llm, preparation: ProblemPreparation, branch_factor: int) -> list[CandidateBranchModel]:
    structured = llm.with_structured_output(CandidateBranchSetModel)
    result = structured.invoke(
        f"""
Você está executando uma busca em Tree of Thought para escolher as melhores técnicas de prompt.
Gere {branch_factor} ramos de decisão materialmente diferentes.

Catálogo de técnicas:
{technique_catalog_prompt()}

Problema higienizado:
{preparation.normalized_problem}

Problema enriquecido:
{preparation.enriched_problem}

Restrições explícitas:
{preparation.explicit_constraints}

Restrições implícitas:
{preparation.implied_constraints}

Saída esperada:
{preparation.expected_output}

Lacunas:
{preparation.missing_information}

Suposições seguras:
{preparation.safe_assumptions}

Regras:
- Cada ramo deve propor uma estratégia diferente de decisão.
- Recomende de 1 a 6 técnicas por ramo.
- Não recomende tudo ao mesmo tempo.
- Considere o uso de tokens por técnica para evitar planos não executáveis.
- Em suggested_args, devolva uma lista plana de tokens CLI. Não use aspas shell.
- Garanta que a primeira técnica do ramo seja executável com os argumentos sugeridos.
- Se recomendar combinações, deixe claro o papel de cada técnica.
"""
    )
    return result.candidates


def evaluate_branch(llm, preparation: ProblemPreparation, branch: CandidateBranchModel) -> BranchEvaluationModel:
    structured = llm.with_structured_output(BranchEvaluationModel)
    return structured.invoke(
        f"""
Avalie o ramo abaixo para o problema preparado.
Pontue cada critério de 1 a 10 e justifique.

Critérios:
- fit_to_problem: aderência real ao problema.
- cost_efficiency: equilíbrio entre qualidade e custo/latência.
- auditability: facilidade de entender e revisar o processo.
- resilience_to_ambiguity: robustez diante de ambiguidades e lacunas.
- execution_readiness: quão pronto está para o usuário rodar.

Problema enriquecido:
{preparation.enriched_problem}

Saída esperada:
{preparation.expected_output}

Lacunas:
{preparation.missing_information}

Ramo:
Nome: {branch.branch_name}
Resumo: {branch.strategy_summary}
Técnicas: {branch.recommended_techniques}
Trade-offs: {branch.tradeoffs}
"""
    )


def refine_branch(llm, preparation: ProblemPreparation, branch: CandidateBranchModel, evaluation: BranchEvaluationModel) -> CandidateBranchModel:
    structured = llm.with_structured_output(CandidateBranchModel)
    return structured.invoke(
        f"""
Refine o ramo abaixo com base na avaliação recebida.
Produza uma versão melhorada, mais executável e mais aderente ao problema.

Catálogo de técnicas:
{technique_catalog_prompt()}

Problema enriquecido:
{preparation.enriched_problem}

Saída esperada:
{preparation.expected_output}

Lacunas:
{preparation.missing_information}

Ramo atual:
Nome: {branch.branch_name}
Resumo: {branch.strategy_summary}
Técnicas: {branch.recommended_techniques}
Trade-offs: {branch.tradeoffs}

Avaliação:
{evaluation}

Regras:
- Mantenha o ramo materialmente diferente dos demais.
- Melhore argumentos, clareza e ordenação das técnicas.
- Use ToT se isso continuar sendo a melhor técnica principal.
- Em suggested_args, devolva uma lista plana de tokens CLI, sem aspas shell.
"""
    )


def choose_final_plan(llm, preparation: ProblemPreparation, finalists: list[tuple[CandidateBranchModel, BranchEvaluationModel, float, str]]) -> FinalPlanModel:
    structured = llm.with_structured_output(FinalPlanModel)
    finalists_text = "\n\n".join(
        (
            f"Nome: {branch.branch_name}\n"
            f"Resumo: {branch.strategy_summary}\n"
            f"Técnicas: {branch.recommended_techniques}\n"
            f"Trade-offs: {branch.tradeoffs}\n"
            f"Avaliação: {evaluation}\n"
            f"Score ponderado: {score:.2f}\n"
            f"Fórmula: {formula}"
        )
        for branch, evaluation, score, formula in finalists
    )
    return structured.invoke(
        f"""
Escolha o melhor plano final para o problema abaixo a partir dos finalistas.
Você pode manter a melhor opção como está ou combinar elementos compatíveis dos finalistas,
mas sem perder executabilidade.

Catálogo de técnicas:
{technique_catalog_prompt()}

Problema enriquecido:
{preparation.enriched_problem}

Saída esperada:
{preparation.expected_output}

Finalistas:
{finalists_text}

Regras:
- Ordene as técnicas finais por prioridade.
- Não devolva técnicas redundantes.
- Se usar ToT, justifique por que ela merece prioridade.
- Em suggested_args, devolva uma lista plana de tokens CLI, sem aspas shell.
"""
    )


def analyze_problem(
    problem: str,
    *,
    model: str = DEFAULT_ADVISOR_MODEL,
    temperature: float = DEFAULT_ADVISOR_TEMPERATURE,
    branch_factor: int = DEFAULT_BRANCH_FACTOR,
    beam_width: int = DEFAULT_BEAM_WIDTH,
    finalists: int = DEFAULT_FINALISTS,
) -> AdvisorAnalysis:
    from dotenv import load_dotenv

    from common import build_llm

    load_dotenv()
    normalized_input = sanitize_problem_input(problem)
    llm = build_llm(model, temperature)

    preparation = prepare_problem(llm, normalized_input)
    root_candidates = generate_candidate_branches(llm, preparation, branch_factor)

    scored_candidates: list[tuple[CandidateBranchModel, BranchEvaluationModel, float, str]] = []
    for branch in root_candidates:
        evaluation = evaluate_branch(llm, preparation, branch)
        score, formula = weighted_branch_score(evaluation)
        scored_candidates.append((branch, evaluation, score, formula))
    scored_candidates.sort(key=lambda item: item[2], reverse=True)

    refined_candidates: list[tuple[CandidateBranchModel, BranchEvaluationModel, float, str]] = []
    for branch, evaluation, _, _ in scored_candidates[:beam_width]:
        refined_branch = refine_branch(llm, preparation, branch, evaluation)
        refined_evaluation = evaluate_branch(llm, preparation, refined_branch)
        refined_score, refined_formula = weighted_branch_score(refined_evaluation)
        refined_candidates.append((refined_branch, refined_evaluation, refined_score, refined_formula))

    all_candidates = sorted(scored_candidates + refined_candidates, key=lambda item: item[2], reverse=True)
    chosen_finalists = all_candidates[:finalists]
    final_plan = choose_final_plan(llm, preparation, chosen_finalists)

    return AdvisorAnalysis(
        preparation=preparation,
        recommendations=dedupe_recommendations(final_plan.recommended_techniques, preparation),
        selection_rationale=final_plan.selection_rationale,
        usage_notes=final_plan.usage_notes,
    )


def recommend_techniques(
    problem: str,
    *,
    model: str = DEFAULT_ADVISOR_MODEL,
    temperature: float = DEFAULT_ADVISOR_TEMPERATURE,
    branch_factor: int = DEFAULT_BRANCH_FACTOR,
    beam_width: int = DEFAULT_BEAM_WIDTH,
    finalists: int = DEFAULT_FINALISTS,
) -> list[Recommendation]:
    analysis = analyze_problem(
        problem,
        model=model,
        temperature=temperature,
        branch_factor=branch_factor,
        beam_width=beam_width,
        finalists=finalists,
    )
    return analysis.recommendations
