import re
from datetime import datetime


def validar_email(email: str) -> bool:
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(padrao, email))


def validar_valor(valor_str: str) -> float | None:
    try:
        valor = float(valor_str.replace(',', '.'))
        if valor <= 0:
            return None
        return valor
    except ValueError:
        return None


def validar_data(data_str: str) -> str | None:
    formatos = ['%d/%m/%Y', '%Y-%m-%d']
    for fmt in formatos:
        try:
            data = datetime.strptime(data_str, fmt)
            return data.strftime('%Y-%m-%d')
        except ValueError:
            continue
    return None


def validar_tipo(tipo_str: str) -> str | None:
    tipo = tipo_str.strip().lower()
    if tipo in ('receita', 'r', '1'):
        return 'receita'
    if tipo in ('despesa', 'd', '2'):
        return 'despesa'
    return None
