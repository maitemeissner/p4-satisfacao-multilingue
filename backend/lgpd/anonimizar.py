import re

PII_PATTERNS = {
    'email': r'[\w\.-]+@[\w\.-]+\.\w+',
    'ip': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    'nome': r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',
}

def anonimizar(texto: str) -> str:
    for tipo, pattern in PII_PATTERNS.items():
        texto = re.sub(pattern, f'[{tipo.upper()}_OFUSCADO]', texto)
    return texto