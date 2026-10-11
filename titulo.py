# Classes do domínio: Titulo (abstrata), Filme e Serie.

from abc import ABC, abstractmethod

from constantes import (
    ANO_INTERMEDIARIO, ANO_RECENTE,
    FILME_CURTO, FILME_LONGO, SERIE_CURTA, SERIE_MEDIA,
    PONTOS_MINIMOS_DESTAQUE, GENEROS_DESTAQUE,
    PONTOS_RECENCIA, PONTOS_GENERO, PONTOS_INTERNACIONAL,
    PONTOS_INFORMACAO, PONTOS_DURACAO_LONGA
)
from utils import normalizar, normalizar_tipo, contem_item


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# CLASSE BASE (ABSTRATA)
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

class Titulo(ABC):

    def __init__(
        self,
        show_id,
        titulo,
        pais,
        ano,
        classificacao,
        duracao,
        genero,
        diretor="",
        elenco="",
        sinopse=""
    ):
        self._id = show_id
        self._titulo = titulo
        self._pais = pais
        self._ano = ano
        self._classificacao = classificacao
        self._duracao = duracao
        self._genero = genero
        self._diretor = diretor
        self._elenco = elenco
        self._sinopse = sinopse

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # ENCAPSULAMENTO
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    @property
    def id(self):
        return self._id

    @property
    def titulo(self):
        return self._titulo

    @property
    def pais(self):
        return self._pais

    @property
    def ano(self):
        return self._ano

    @property
    def classificacao(self):
        return self._classificacao

    @property
    def duracao(self):
        return self._duracao

    @property
    def genero(self):
        return self._genero

    @property
    def diretor(self):
        return self._diretor

    @property
    def elenco(self):
        return self._elenco

    @property
    def sinopse(self):
        return self._sinopse

    @property
    def paises(self):
        return [p.strip() for p in self._pais.split(",") if p.strip()]

    @property
    def generos(self):
        return [g.strip() for g in self._genero.split(",") if g.strip()]

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # MÉTODOS QUE CADA SUBCLASSE É OBRIGADA A IMPLEMENTAR
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    @property
    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def classificar_duracao(self):
        pass

    @abstractmethod
    def duracao_longa(self):
        pass

    @abstractmethod
    def duracao_texto(self):
        pass

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # EXIBIÇÃO
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def mostrar_informacoes(self):

        print("\n· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")
        print("        INFORMAÇÕES DO TÍTULO")
        print("· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")

        print(f"ID: {self.id}")
        print(f"Título: {self.titulo}")
        print(f"Tipo: {self.tipo}")
        print(f"País: {self.pais or 'Não informado'}")
        print(f"Ano: {self.ano}")
        print(f"Classificação indicativa: {self.classificacao or 'Não informada'}")
        print(f"Gênero: {self.genero}")
        print(f"Diretor: {self.diretor or 'Não informado'}")
        print(f"Elenco: {self.elenco or 'Não informado'}")
        print(f"Sinopse: {self.sinopse}")
        print(f"Classificação por ano: {self.classificar_por_ano()}")

    def resumo(self):

        return f"{self.titulo} | {self.tipo} | {self.ano}"

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    #      CLASSIFICAÇÕES BASEADAS EM REGRAS
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def classificar_por_ano(self):

        if self.ano < ANO_INTERMEDIARIO:
            return "Antigo"

        if self.ano < ANO_RECENTE:
            return "Intermediário"

        return "Recente"

    def classificacao_internacional(self):

        if not self.paises:
            return "Não informado"

        if len(self.paises) > 1:
            return "Produção internacional"

        return "Produção de um país"

    def classificacao_destaque(self):

        pontos = 0

        if self.ano >= ANO_RECENTE:
            pontos += 1

        if self.genero:
            pontos += 1

        if self.diretor:
            pontos += 1

        if self.elenco:
            pontos += 1

        if self.sinopse:
            pontos += 1

        # a regra também depende do tipo: filme longo ou série longa
        if self.duracao_longa():
            pontos += 1

        if pontos >= PONTOS_MINIMOS_DESTAQUE:
            return "Título de destaque"

        return "Título comum"

    def classificacao_interesse_especifico(
        self,
        pais=None,
        genero=None,
        tipo=None,
        classificacao=None
    ):
       
        if pais and not contem_item(self.paises, pais):
            return False

        if genero and normalizar(genero) not in normalizar(self.genero):
            return False

        if tipo and normalizar_tipo(tipo) != self.tipo:
            return False

        if classificacao and normalizar(classificacao) != normalizar(self.classificacao):
            return False

        return True

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    #          BÔNUS - ÍNDICE DE DESTAQUE
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def calcular_indice_destaque(self):
        """
        Índice de 0 a 10 pontos, criado por regras para este trabalho.
        Não mede qualidade da obra, só combina recência, gênero,
        quantidade de países, completude da ficha e duração.
        """

        pontos = 0

        if self.ano >= ANO_RECENTE:
            pontos += PONTOS_RECENCIA

        genero = self.genero.lower()

        if any(g in genero for g in GENEROS_DESTAQUE):
            pontos += PONTOS_GENERO

        if len(self.paises) > 1:
            pontos += PONTOS_INTERNACIONAL

        if self.diretor:
            pontos += PONTOS_INFORMACAO

        if self.elenco:
            pontos += PONTOS_INFORMACAO

        if self.sinopse:
            pontos += PONTOS_INFORMACAO

        if self.duracao_longa():
            pontos += PONTOS_DURACAO_LONGA

        return pontos

    def classificacao_indice_destaque(self):

        indice = self.calcular_indice_destaque()

        if indice >= 8:
            return "Muito alto"

        if indice >= 6:
            return "Alto"

        if indice >= 4:
            return "Médio"

        return "Baixo"


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# FILME
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

class Filme(Titulo):

    @property
    def tipo(self):
        return "Filme"

    def classificar_duracao(self):

        if self.duracao < FILME_CURTO:
            return "Filme curto"

        if self.duracao <= FILME_LONGO:
            return "Filme médio"

        return "Filme longo"

    def duracao_longa(self):
        return self.duracao > FILME_LONGO

    def duracao_texto(self):
        return f"{self.duracao} min"

    def mostrar_informacoes(self):

        super().mostrar_informacoes()

        print(f"Duração: {self.duracao_texto()}")
        print(f"Classificação por duração: {self.classificar_duracao()}")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# SÉRIE
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

class Serie(Titulo):

    @property
    def tipo(self):
        return "Série"

    def classificar_duracao(self):

        if self.duracao <= SERIE_CURTA:
            return "Série curta"

        if self.duracao <= SERIE_MEDIA:
            return "Série média"

        return "Série longa"

    def duracao_longa(self):
        return self.duracao > SERIE_MEDIA

    def duracao_texto(self):

        if self.duracao == 1:
            return "1 temporada"

        return f"{self.duracao} temporadas"

    def mostrar_informacoes(self):

        super().mostrar_informacoes()

        print(f"Duração: {self.duracao_texto()}")
        print(f"Classificação por duração: {self.classificar_duracao()}")
