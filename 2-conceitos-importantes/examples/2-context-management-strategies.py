messages = [
    "Sistema: voce e um assistente de suporte tecnico.",
    "Usuario: meu sistema falhou na importacao de planilhas.",
    "Assistente: perguntei sobre formato e volume.",
    "Usuario: sao 20 mil linhas e alguns campos vazios.",
    "Assistente: investiguei validacao e filas.",
    "Usuario: agora tambem preciso correlacionar com o job de cobranca.",
]


def truncate(history, keep=3):
    return history[-keep:]


def summarize(history):
    return [
        "Resumo: conversa anterior tratou de importacao de planilhas, volume alto, campos vazios e relacao com filas e cobranca."
    ]


def sliding_window(history, size=4):
    return history[-size:]


print("Exemplo: truncamento, sumarizacao e sliding window\n")

print("Truncamento:")
for item in truncate(messages):
    print(f"- {item}")

print("\nSumarizacao + janela atual:")
for item in summarize(messages[:-2]) + messages[-2:]:
    print(f"- {item}")

print("\nSliding window:")
for item in sliding_window(messages):
    print(f"- {item}")

print(
    "\nLeitura:\n"
    "- truncamento corta;\n"
    "- sumarizacao preserva a linha geral, mas perde detalhes;\n"
    "- sliding window mantem apenas a fatia ativa do historico."
)
