try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from utils import print_llm_result

load_dotenv()

task_input = """
Function to analyze:
def normalize_email(email: str) -> str:
    return email.strip().lower()

Task:
Generate unit tests for valid and invalid cases.
""".strip()

mixed_prompt = ChatPromptTemplate(
    [
        (
            "user",
            """
Você é um assistente de engenharia de software.
Seja técnico, direto e não refatore fora do escopo.
Sempre explicite pressupostos quando faltar contexto.
Agora analise a função abaixo e gere testes unitários apenas para os casos mais relevantes.

{task_input}
""".strip(),
        )
    ]
)

separated_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """
Você é um assistente de engenharia de software.
Seja técnico, direto e não refatore fora do escopo.
Sempre explicite pressupostos quando faltar contexto.
""".strip(),
        ),
        (
            "user",
            """
Analise a função abaixo e gere testes unitários apenas para os casos mais relevantes.

{task_input}
""".strip(),
        ),
    ]
)

messages_mixed = mixed_prompt.format_messages(task_input=task_input)
messages_separated = separated_prompt.format_messages(task_input=task_input)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

mixed_response = llm.invoke(messages_mixed)
separated_response = llm.invoke(messages_separated)

print_llm_result(
    "Prompt Misturando Regras E Tarefa",
    messages_mixed,
    mixed_response,
    notes=(
        "- tudo chega em um único bloco, o que dificulta separar regras globais do pedido local.\n"
        "- essa forma é mais difícil de manter e reaproveitar."
    ),
)

print_llm_result(
    "System Prompt Separado Do User Prompt",
    messages_separated,
    separated_response,
    notes=(
        "- a divisão deixa explícito o comportamento-base e a tarefa do momento.\n"
        "- o exemplo ajuda a enxergar prompt como arquitetura de instrução, não só texto."
    ),
)
