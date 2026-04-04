from textwrap import dedent


def estimate_tokens(text: str) -> int:
    return len(text.split())


parts = {
    "system": "Voce e um assistente tecnico focado em analise de codigo e arquitetura.",
    "history": dedent(
        """
        Usuario: explique a regra do modulo de faturamento.
        Assistente: explicou faturamento.
        Usuario: agora compare com o fluxo de cobranca recorrente e detalhe edge cases.
        """
    ).strip(),
    "code": dedent(
        """
        def charge_subscription(customer, amount, status):
            if status != "active":
                raise ValueError("inactive subscription")
            return {"customer": customer, "amount": amount}
        """
    ).strip(),
    "question": "Quais partes ainda faltam para eu documentar esse fluxo sem perder o contexto?",
}

print("Exemplo: janela de contexto e orcamento de tokens\n")
total = 0
for name, content in parts.items():
    count = estimate_tokens(content)
    total += count
    print(f"{name:>8}: {count:>3} tokens aproximados")

print(f"\nTotal aproximado: {total} tokens")
print(
    "\nLeitura:\n"
    "- a pergunta isolada e pequena;\n"
    "- o custo real vem da soma de system prompt, historico, codigo e pergunta atual;\n"
    "- esse mesmo raciocinio explica por que conversas longas exigem sumarizacao, truncamento ou sliding window."
)
