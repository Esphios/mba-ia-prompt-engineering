tasks = [
    ("Sumarizar historico longo", "medio", "media"),
    ("Responder duvida tecnica complexa", "alto", "alta"),
    ("Classificar milhares de entradas simples", "baixo", "baixa"),
]

profiles = {
    "modelo-menor": {"cost": 1, "latency": 1, "quality": 2},
    "modelo-intermediario": {"cost": 2, "latency": 2, "quality": 3},
    "modelo-maior": {"cost": 3, "latency": 3, "quality": 5},
}

print("Exemplo: escolha de modelo, custo e latencia\n")
for task, complexity, tolerance in tasks:
    print(f"Tarefa: {task}")
    print(f"- complexidade: {complexity}")
    print(f"- tolerancia a erro: {tolerance}")
    if task == "Responder duvida tecnica complexa":
        chosen = "modelo-maior"
    elif task == "Classificar milhares de entradas simples":
        chosen = "modelo-menor"
    else:
        chosen = "modelo-intermediario"
    profile = profiles[chosen]
    print(
        f"- sugestao: {chosen} "
        f"(custo={profile['cost']}, latencia={profile['latency']}, qualidade={profile['quality']})\n"
    )

print(
    "Leitura:\n"
    "- Prompt Engineering tambem envolve escolher o modelo adequado para cada etapa;\n"
    "- nem toda tarefa precisa do modelo mais forte;\n"
    "- custo e latencia fazem parte da decisao."
)
