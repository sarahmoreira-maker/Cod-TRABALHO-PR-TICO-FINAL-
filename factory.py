# Factory: transforma uma linha do CSV em Filme ou Serie.

from constantes import ANO_MINIMO, ANO_MAXIMO
from titulo import Filme, Serie


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# FACTORY - decide se a linha do CSV vira Filme ou Série
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

class TituloFactory:

    @staticmethod
    def criar_titulo(linha):

        show_id = linha.get("show_id", "").strip()
        titulo = linha.get("title", "").strip()
        tipo = linha.get("type", "").strip()
        pais = linha.get("country", "").strip()
        ano_texto = linha.get("release_year", "").strip()
        classificacao = linha.get("rating", "").strip()
        duracao_texto = linha.get("duration", "").strip()
        genero = linha.get("listed_in", "").strip()
        diretor = linha.get("director", "").strip()
        elenco = linha.get("cast", "").strip()
        sinopse = linha.get("description", "").strip()

        if not show_id:
            raise ValueError("ID vazio")

        if not titulo:
            raise ValueError("Título vazio")

        if not tipo:
            raise ValueError("Tipo vazio")

        if not genero:
            raise ValueError("Gênero vazio")

        try:
            ano = int(ano_texto)

        except ValueError:
            raise ValueError("Ano inválido")

        if ano < ANO_MINIMO or ano > ANO_MAXIMO:
            raise ValueError("Ano fora do intervalo aceito")

        if tipo == "Movie":

            # na base, 3 filmes têm a duração escrita no campo rating
            if not duracao_texto and "min" in classificacao.lower():
                duracao_texto = classificacao
                classificacao = ""

            duracao = TituloFactory.converter_duracao(duracao_texto, "min")

            return Filme(
                show_id, titulo, pais, ano, classificacao,
                duracao, genero, diretor, elenco, sinopse)

        if tipo == "TV Show":

            duracao = TituloFactory.converter_duracao(duracao_texto, "season")

            return Serie(
                show_id, titulo, pais, ano, classificacao,
                duracao, genero, diretor, elenco, sinopse)

        raise ValueError("Tipo desconhecido")

    @staticmethod
    def converter_duracao(texto, unidade):
        """Aceita '90 min' ou '2 Seasons'. Qualquer outra coisa é erro."""

        partes = texto.lower().split()

        if len(partes) != 2 or unidade not in partes[1]:
            raise ValueError("Duração inválida")

        try:
            valor = int(partes[0])

        except ValueError:
            raise ValueError("Duração inválida")

        if valor <= 0:
            raise ValueError("Duração inválida")

        return valor
