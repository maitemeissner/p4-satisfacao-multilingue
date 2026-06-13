import re

class Anonymizer:
    def __init__(self):
        self.patterns = [
            (re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"), "[CPF]"),
            (re.compile(r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b"), "[CNPJ]"),
            (re.compile(r"\b[\w.-]+@[\w.-]+\.\w+\b"), "[EMAIL]"),
            (re.compile(r"\b\d{10,11}\b"), "[TELEFONE]"),
            (re.compile(r"\b\d{5}-?\d{3}\b"), "[CEP]"),
            (re.compile(r"(?:Rua|Av\.|Avenida|Travessa|Alameda)\s[\w\s]+", re.IGNORECASE), "[ENDERECO]"),
        ]

    def anonymize(self, texto: str) -> str:
        if not texto:
            return texto
        resultado = texto
        for pattern, replacement in self.patterns:
            resultado = pattern.sub(replacement, resultado)
        return resultado
