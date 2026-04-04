from textwrap import dedent


stable_prefix = dedent(
    """
    Voce e um classificador de logs.
    Responda em JSON com id, severity e should_open_issue.
    Nao explique seu raciocinio.
    """
).strip()

logs = [
    {"id": "log-1", "message": "INFO healthcheck completed in 12ms"},
    {"id": "log-2", "message": "ERROR database timeout while creating order"},
    {"id": "log-3", "message": "WARN retrying payment webhook"},
]

print("Exemplo: cache e batch prompting\n")
print("Prefixo estavel que pode se beneficiar de cache:\n")
print(stable_prefix)

print("\nLote de logs enviado em uma chamada:\n")
for log in logs:
    print(f'- {log["id"]}: {log["message"]}')

print(
    "\nSaida esperada por item:\n"
    '{"id":"log-1","severity":"info","should_open_issue":false}\n'
    '{"id":"log-2","severity":"error","should_open_issue":true}\n'
    '{"id":"log-3","severity":"warning","should_open_issue":false}'
)

print(
    "\nLeitura:\n"
    "- cache ajuda quando o prefixo do prompt se repete;\n"
    "- batch ajuda quando varios itens semelhantes podem ser processados juntos;\n"
    "- os dois conceitos se complementam em fluxos de alto volume."
)
