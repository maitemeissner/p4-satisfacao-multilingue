import pandas as pd
import random

def gerar_dataset(qtd=200):
    reviews = []
    for _ in range(qtd):
        idioma = random.choice(["pt-BR", "en-US", "es-ES"])
        score = random.randint(1, 5)
        if score >= 4:
            texto = random.choice([
                "Excelente atendimento, recomendo!", "Ótimo serviço, voltarei com certeza",
                "Great experience, very professional", "Amazing service, highly recommended",
                "Excelente servicio, muy recomendable", "Buena atención, volveré pronto"
            ])
        elif score >= 3:
            texto = random.choice([
                "Serviço ok, nada excepcional", "Bom, mas pode melhorar",
                "It was fine, average experience", "Good but not great",
                "Estuvo bien, nada especial", "Buen servicio en general"
            ])
        else:
            texto = random.choice([
                "Péssimo experiência, não recomendo", "Horrível atendimento, frustrante",
                "Terrible experience, very disappointed", "Worst service ever",
                "Mala experiencia, no vuelvo", "Horrible atención al cliente"
            ])
        reviews.append({"texto": texto, "score": score, "idioma": idioma})
    return pd.DataFrame(reviews)