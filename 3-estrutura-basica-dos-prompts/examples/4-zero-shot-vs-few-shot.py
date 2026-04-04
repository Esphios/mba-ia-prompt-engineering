try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from langchain_openai import ChatOpenAI

from utils import print_llm_result

load_dotenv()

zero_shot = """
Classifique o ticket abaixo como bug, dúvida ou feature request.
Responda apenas com a classe.

Ticket:
"Não consigo salvar meu perfil depois da última atualização."
""".strip()

few_shot = """
Classifique o ticket abaixo como bug, dúvida ou feature request.
Responda apenas com a classe.

Exemplo 1:
Ticket: "Como altero minha senha?"
Classe: dúvida

Exemplo 2:
Ticket: "Depois do deploy, o botão salvar gera erro 500."
Classe: bug

Exemplo 3:
Ticket: "Seria útil exportar os relatórios em CSV."
Classe: feature request

Ticket:
"Não consigo salvar meu perfil depois da última atualização."
""".strip()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

zero_shot_response = llm.invoke(zero_shot)
few_shot_response = llm.invoke(few_shot)

print_llm_result(
    "Zero-shot",
    zero_shot,
    zero_shot_response,
    notes=(
        "- zero-shot é menor, mais barato e mais direto.\n"
        "- ele funciona melhor quando a tarefa é simples e o padrão já é claro para o modelo."
    ),
)

print_llm_result(
    "Few-shot",
    few_shot,
    few_shot_response,
    notes=(
        "- few-shot compra previsibilidade usando exemplos.\n"
        "- a comparação mostra por que exemplos ajudam quando o formato ou o domínio importam mais."
    ),
)
