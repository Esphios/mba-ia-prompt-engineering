try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from utils import print_llm_result

load_dotenv()

bug_context = """
Repository context:
- Service: customer-access-api
- Goal: fix a production bug with minimal diff
- Rule: reviewers reject refactors outside scope

Function:
def is_eligible(age: int) -> bool:
    return age > 18

Bug report:
Users with exactly 18 years old should be eligible, but they are being rejected.
""".strip()

vague_prompt = ChatPromptTemplate(
    [
        ("user", "Valide a função, entenda o problema e faça a correção para mim.\n\n{bug_context}"),
    ]
)

scoped_prompt = ChatPromptTemplate(
    [
        (
            "system",
            """
Você é um engenheiro de software sênior especializado em correções cirúrgicas.
Corrija apenas o bug relatado.
Não refatore arquivos adjacentes.
Não mude nomenclatura sem necessidade.
Explique pressupostos explicitamente.
""".strip(),
        ),
        (
            "user",
            """
Analise o bug abaixo e responda em 3 blocos:
1. causa raiz
2. patch mínimo sugerido
3. riscos ou pressupostos

{bug_context}
""".strip(),
        ),
    ]
)

messages_vague = vague_prompt.format_messages(bug_context=bug_context)
messages_scoped = scoped_prompt.format_messages(bug_context=bug_context)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

vague_response = llm.invoke(messages_vague)
scoped_response = llm.invoke(messages_scoped)

print_llm_result(
    "Prompt Vago",
    messages_vague,
    vague_response,
    notes=(
        "- o pedido é amplo e deixa espaço para a IA extrapolar o escopo.\n"
        "- o estudante consegue observar se a resposta começa a sugerir mudanças além do bug."
    ),
)

print_llm_result(
    "Prompt Com Escopo Delimitado",
    messages_scoped,
    scoped_response,
    notes=(
        "- o prompt forte restringe comportamento, formato e foco.\n"
        "- a comparação deixa mais claro por que limites explícitos reduzem ruído operacional."
    ),
)
