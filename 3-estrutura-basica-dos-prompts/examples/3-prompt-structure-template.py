from textwrap import dedent

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args, **_kwargs) -> bool:
        return False
from langchain_openai import ChatOpenAI

from utils import print_llm_result

load_dotenv()

structured_prompt = dedent(
    """
    [Persona e escopo]
    Você é um assistente especializado em Node.js 18 e testes com Jest.
    Não refatore o código original.

    [Objetivo]
    Gerar testes unitários para a função abaixo.

    [Entrada]
    function validateAge(age) {
      return age >= 18;
    }

    [Formato de saída]
    Responda apenas com um objeto JSON contendo:
    - test_file
    - coverage_notes
    - assumptions

    [Critérios de qualidade]
    - cobrir caso válido e inválido
    - manter Jest como framework
    - não usar bibliotecas externas

    [Ambiguidades]
    Se faltar versão de runtime, assuma Node 18 e registre em assumptions.

    [Instruções negativas]
    Não inclua comentários fora do JSON.

    [Tratamento de erro]
    Se a tarefa não puder ser concluída, retorne status=error e reason.
    """
).strip()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
response = llm.invoke(structured_prompt)

print_llm_result(
    "Template Estruturado Em Ação",
    structured_prompt,
    response,
    notes=(
        "- este exemplo transforma a estrutura teórica do capítulo em um artefato executável.\n"
        "- o valor pedagógico está em ver um prompt com seções produzir uma saída estruturada de verdade."
    ),
)
