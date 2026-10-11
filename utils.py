# Funções auxiliares de texto usadas nas buscas e filtros.

import unicodedata


def normalizar(texto):
    """Minúsculas e sem acento, para as buscas não dependerem da digitação."""

    texto = unicodedata.normalize("NFKD", str(texto))

    texto = "".join(
        letra for letra in texto
        if not unicodedata.combining(letra))

    return texto.lower().strip()


def normalizar_tipo(texto):
    """Converte o que o usuário digitou para 'Filme' ou 'Série'."""

    texto = normalizar(texto)

    if texto in ("filme", "filmes", "movie", "movies"):
        return "Filme"

    if texto in ("serie", "series", "tv show", "tv shows"):
        return "Série"

    return None


def contem_item(itens, busca):
    """True se 'busca' for exatamente um dos itens da lista."""

    busca = normalizar(busca)

    return any(normalizar(item) == busca for item in itens)
