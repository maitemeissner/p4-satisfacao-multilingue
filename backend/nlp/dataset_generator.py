import random

LINGUAS = ["pt", "en", "es"]
PLATAFORMAS = ["Google Play", "App Store", "Web", "Facebook", "Instagram"]

TEXTOS_PT = {
    5: ["Ótimo produto, adorei!", "Excelente, superou expectativas!", "Maravilhoso, recomendo muito!", "Perfeito, funcionou muito bem!", "Simplesmente incrível!"],
    4: ["Muito bom, gostei bastante.", "Bom produto, atende bem.", "Satisfeito com a compra.", "Bom custo-benefício.", "Funciona como esperado."],
    3: ["Mais ou menos, poderia ser melhor.", "Regular, nada de especial.", "Atende mas não impressiona.", "Esperava um pouco mais.", "Razoável pelo preço."],
    2: ["Ruim, não gostei muito.", "Decepcionante, esperava mais.", "Não atendeu minhas expectativas.", "Qualidade baixa.", "Poderia ser muito melhor."],
    1: ["Péssimo, horrível!", "Não recomendo para ninguém.", "Terrível, perda de dinheiro.", "Frustrante, péssima experiência.", "Simplesmente horrível."],
}

TEXTOS_EN = {
    5: ["Amazing product, I love it!", "Excellent, exceeded expectations!", "Fantastic, highly recommend!", "Perfect, worked great!", "Absolutely incredible!"],
    4: ["Very good, I really liked it.", "Good product, works well.", "Satisfied with the purchase.", "Good value for money.", "Works as expected."],
    3: ["It's okay, could be better.", "Average, nothing special.", "Does the job but not impressive.", "Expected a bit more.", "Decent for the price."],
    2: ["Bad, didn't like it much.", "Disappointing, expected more.", "Didn't meet expectations.", "Low quality.", "Could be much better."],
    1: ["Terrible, horrible!", "Don't recommend to anyone.", "Awful, waste of money.", "Frustrating, terrible experience.", "Simply horrible."],
}

TEXTOS_ES = {
    5: ["¡Excelente producto, me encanta!", "¡Fantástico, superó expectativas!", "¡Maravilloso, lo recomiendo mucho!", "Perfecto, funcionó muy bien.", "¡Simplemente increíble!"],
    4: ["Muy bueno, me gustó bastante.", "Buen producto, cumple bien.", "Satisfecho con la compra.", "Buena relación calidad-precio.", "Funciona como esperaba."],
    3: ["Regular, podría ser mejor.", "Normal, nada especial.", "Cumple pero no impresiona.", "Esperaba un poco más.", "Aceptable por el precio."],
    2: ["Malo, no me gustó mucho.", "Decepcionante, esperaba más.", "No cumplió expectativas.", "Baja calidad.", "Podría ser mucho mejor."],
    1: ["¡Pésimo, horrible!", "No lo recomiendo a nadie.", "Horrible, pérdida de dinero.", "Frustrante, pésima experiencia.", "Simplemente horrible."],
}

TEXTOS_POR_IDIOMA = {"pt": TEXTOS_PT, "en": TEXTOS_EN, "es": TEXTOS_ES}

def gerar_dataset(qtd=200):
    textos = []
    labels = []
    for _ in range(qtd):
        lingua = random.choice(LINGUAS)
        score = random.choices([1, 2, 3, 4, 5], weights=[1, 2, 3, 3, 3])[0]
        texto = random.choice(TEXTOS_POR_IDIOMA[lingua][score])
        textos.append(texto)
        labels.append(score)
    return textos, labels

if __name__ == "__main__":
    t, l = gerar_dataset(50)
    for txt, lbl in zip(t, l):
        print(f"[{lbl}] {txt}")
