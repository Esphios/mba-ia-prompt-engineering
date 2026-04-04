from time import perf_counter

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from langchain_openai import ChatOpenAI

from utils import print_llm_result, print_metric_table

load_dotenv()

task = """
Resuma o ticket abaixo para handoff de engenharia:

"Após a última atualização, clientes premium não conseguem salvar alterações no perfil.
O erro acontece mais no app mobile. Ainda não sabemos se o problema está na API ou na camada de validação."
""".strip()

variants = [
    {
        "name": "Prompt curto",
        "prompt": task,
    },
    {
        "name": "Prompt com critérios",
        "prompt": f"""
Você é um engenheiro de software preparando handoff técnico.
Resuma o ticket abaixo em 3 bullets:
- problema principal
- impacto para o usuário
- hipótese inicial de investigação

{task}
""".strip(),
    },
    {
        "name": "Prompt com few-shot e formato",
        "prompt": f"""
Você é um engenheiro de software preparando handoff técnico.
Resuma o ticket abaixo em JSON com:
- summary
- user_impact
- investigation_hint

Exemplo:
Ticket: "Checkout falha para cartões internacionais."
Resposta:
{{"summary":"Falha no checkout com cartões internacionais.","user_impact":"Usuários não concluem compra.","investigation_hint":"Validar integração com gateway e regras antifraude."}}

{task}
""".strip(),
    },
]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

results = []
metric_rows = []

for variant in variants:
    started = perf_counter()
    response = llm.invoke(variant["prompt"])
    elapsed = perf_counter() - started
    usage = response.response_metadata.get("token_usage", {})

    results.append((variant["name"], variant["prompt"], response))
    metric_rows.append(
        {
            "name": variant["name"],
            "latency": f"{elapsed:.2f}",
            "input_tokens": str(usage.get("prompt_tokens", "?")),
            "output_tokens": str(usage.get("completion_tokens", "?")),
            "total_tokens": str(usage.get("total_tokens", "?")),
        }
    )

for name, prompt, response in results:
    print_llm_result(
        name,
        prompt,
        response,
        notes=(
            "- observe como o aumento de estrutura altera a resposta e o custo.\n"
            "- a pergunta útil não é apenas qual resposta parece melhor, mas qual ganho compensa no contexto."
        ),
    )

print_metric_table("Comparação De Custo, Latência E Tamanho", metric_rows)
