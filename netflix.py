# Sistema de análise do catálogo Netflix (filmes e séries)
# Trabalho Prático Final - Programação Orientada a Objetos
#
# Para executar: deixe este arquivo na mesma pasta do
# netflix_titles.csv e rode  python netflix_completo.py

import csv
import unicodedata
from abc import ABC, abstractmethod



# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# CONSTANTES (limites e regras)
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

# Limites e regras usados nas classificações do sistema.
# Ficam todos aqui para ser fácil justificar e alterar no relatório.

# Classificação por ano
ANO_INTERMEDIARIO = 2000   # antes disso: antigo
ANO_RECENTE = 2016         # a partir disso: recente

# Classificação por duração
FILME_CURTO = 90           # minutos (abaixo disso: curto)
FILME_LONGO = 120          # minutos (acima disso: longo)
SERIE_CURTA = 1            # temporadas (até 1: curta)
SERIE_MEDIA = 3            # temporadas (até 3: média, acima: longa)

# Validação do ano de lançamento
ANO_MINIMO = 1900
ANO_MAXIMO = 2030

# Regras de destaque
# Gênero e sinopse vêm preenchidos em toda a base, então valem ponto para
# todos. Com limite 4, 89% dos títulos viravam destaque; com 6 (todos os
# critérios) são 5,4%, o que torna o rótulo realmente seletivo.
PONTOS_MINIMOS_DESTAQUE = 6
GENEROS_DESTAQUE = ["drama", "comed", "action", "documentar"]

# Índice de destaque (bônus)
PONTOS_RECENCIA = 2
PONTOS_GENERO = 2
PONTOS_INTERNACIONAL = 2
PONTOS_INFORMACAO = 1      # vale para diretor, elenco e sinopse (cada um)
PONTOS_DURACAO_LONGA = 1

# Países com poucos títulos distorcem percentuais
MIN_TITULOS_PAIS = 10



# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# FUNÇÕES AUXILIARES
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

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



# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# CLASSES: TÍTULO, FILME E SÉRIE
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

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


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# CATÁLOGO
# Só guarda os dados e responde consultas. Não usa print nem
# input: a interação com o usuário fica no menu.py.
#  · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

class CatalogoNetflix:

    def __init__(self):

        self._titulos = []
        self._por_id = {}      # acesso direto pelo show_id
        self._invalidos = []   # (id, título, motivo)

        self.registros_lidos = 0
        self.registros_validos = 0
        self.registros_invalidos = 0

    @property
    def titulos(self):
        return list(self._titulos)

    @property
    def invalidos(self):
        return list(self._invalidos)

    #  · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # CARREGAMENTO
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def adicionar(self, titulo):

        if titulo.id in self._por_id:
            raise ValueError("ID repetido")

        self._titulos.append(titulo)
        self._por_id[titulo.id] = titulo

    def carregar_csv(self, nome_arquivo):

        self._titulos = []
        self._por_id = {}
        self._invalidos = []

        self.registros_lidos = 0
        self.registros_validos = 0
        self.registros_invalidos = 0

        with open(nome_arquivo, "r", encoding="utf-8-sig", newline="") as arquivo:

            for linha in csv.DictReader(arquivo):

                self.registros_lidos += 1

                try:
                    self.adicionar(TituloFactory.criar_titulo(linha))
                    self.registros_validos += 1

                except (ValueError, KeyError) as erro:
                    self.registros_invalidos += 1

                    self._invalidos.append((
                        linha.get("show_id", ""),
                        linha.get("title", ""),
                        str(erro)
                    ))

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # QUANTIDADES E ESTATÍSTICAS
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def quantidade(self):
        return len(self._titulos)

    def quantidade_filmes(self):
        return sum(1 for t in self._titulos if isinstance(t, Filme))

    def quantidade_series(self):
        return sum(1 for t in self._titulos if isinstance(t, Serie))

    def percentual_filmes(self):

        if not self._titulos:
            return 0

        return self.quantidade_filmes() / self.quantidade() * 100

    def percentual_series(self):

        if not self._titulos:
            return 0

        return self.quantidade_series() / self.quantidade() * 100

    def ano_medio(self):

        if not self._titulos:
            return 0

        return sum(t.ano for t in self._titulos) / len(self._titulos)

    def titulo_mais_antigo(self, tipo=None):

        lista = self._filtrar_tipo(tipo)

        if not lista:
            return None

        return min(lista, key=lambda t: t.ano)

    def titulo_mais_recente(self, tipo=None):

        lista = self._filtrar_tipo(tipo)

        if not lista:
            return None

        return max(lista, key=lambda t: t.ano)

    def _filtrar_tipo(self, tipo):

        if tipo is None:
            return self._titulos

        return [t for t in self._titulos if t.tipo == tipo]

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # BUSCAS
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def buscar_por_id(self, show_id):
   
        return self._por_id.get(str(show_id).strip().lower())

    def buscar_por_nome(self, nome):

        nome = normalizar(nome)

        return [t for t in self._titulos if normalizar(t.titulo) == nome]

    def buscar_por_parte_titulo(self, texto):

        texto = normalizar(texto)

        return [t for t in self._titulos if texto in normalizar(t.titulo)]

    def buscar_por_diretor(self, diretor):

        diretor = normalizar(diretor)

        return [
            t for t in self._titulos
            if t.diretor and diretor in normalizar(t.diretor)
        ]

    def buscar_por_ator(self, ator):

        ator = normalizar(ator)

        return [
            t for t in self._titulos
            if t.elenco and ator in normalizar(t.elenco)
        ]

    def buscar_por_pais(self, pais):
        # compara o nome inteiro do país (assim "Niger" não traz "Nigeria")
        return [t for t in self._titulos if contem_item(t.paises, pais)]

    def buscar_por_genero(self, genero):
        # para gênero aceita parte do nome: "comedies" acha também "TV Comedies"
        genero = normalizar(genero)

        return [t for t in self._titulos if genero in normalizar(t.genero)]

    def listar_filmes(self):
        return self._filtrar_tipo("Filme")

    def listar_series(self):
        return self._filtrar_tipo("Série")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # FILTROS
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def filtrar_por_tipo(self, tipo):

        tipo = normalizar_tipo(tipo)

        if tipo is None:
            return []

        return self._filtrar_tipo(tipo)

    def filtrar_por_pais(self, pais):
        return self.buscar_por_pais(pais)

    def filtrar_por_genero(self, genero):
        return self.buscar_por_genero(genero)

    def filtrar_por_classificacao(self, classificacao):
        # igualdade exata: "PG" não pode trazer "PG-13" nem "TV-PG"
        classificacao = normalizar(classificacao)

        return [
            t for t in self._titulos
            if t.classificacao and normalizar(t.classificacao) == classificacao]

    def filtrar_por_ano(self, ano_inicial, ano_final):

        return [
            t for t in self._titulos
            if ano_inicial <= t.ano <= ano_final]

    def filtrar_por_duracao(self, tipo, duracao_minima):
        # a duração tem unidades diferentes (minutos x temporadas),
        # por isso o filtro sempre é feito dentro de um tipo só

        tipo = normalizar_tipo(tipo)

        if tipo is None:
            return []

        return [
            t for t in self._filtrar_tipo(tipo)
            if t.duracao >= duracao_minima]

    def busca_combinada(
        self,
        tipo=None,
        pais=None,
        genero=None,
        classificacao=None,
        ano_inicial=None,
        ano_final=None
    ):

        resultados = self.titulos

        if tipo:
            tipo = normalizar_tipo(tipo)
            resultados = [t for t in resultados if t.tipo == tipo]

        if pais:
            resultados = [t for t in resultados if contem_item(t.paises, pais)]

        if genero:
            genero = normalizar(genero)
            resultados = [t for t in resultados if genero in normalizar(t.genero)]

        if classificacao:
            classificacao = normalizar(classificacao)
            resultados = [
                t for t in resultados
                if normalizar(t.classificacao) == classificacao]

        if ano_inicial is not None:
            resultados = [t for t in resultados if t.ano >= ano_inicial]

        if ano_final is not None:
            resultados = [t for t in resultados if t.ano <= ano_final]

        return resultados

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # REGRAS DE CLASSIFICAÇÃO
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def listar_internacionais(self):

        return [
            t for t in self._titulos
            if t.classificacao_internacional() == "Produção internacional"]

    def listar_destaques(self):

        return [
            t for t in self._titulos
            if t.classificacao_destaque() == "Título de destaque"]

    def filtrar_interesse(self, pais=None, genero=None, tipo=None, classificacao=None):

        return [
            t for t in self._titulos
            if t.classificacao_interesse_especifico(pais, genero, tipo, classificacao)]

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # ORDENAÇÃO
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def ordenar_por_titulo(self):
        return sorted(self._titulos, key=lambda t: normalizar(t.titulo))

    def ordenar_por_ano(self):
        return sorted(self._titulos, key=lambda t: (t.ano, normalizar(t.titulo)))

    def ordenar_por_ano_decrescente(self):
        return sorted(
            self._titulos,
            key=lambda t: (-t.ano, normalizar(t.titulo)))

    def ordenar_por_duracao(self, tipo):

        return sorted(
            self._filtrar_tipo(tipo),
            key=lambda t: (-t.duracao, normalizar(t.titulo)))

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    # CONTAGENS E RANKINGS
    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

    def _contar(self, extrair, tipo=None):
        """Conta quantas vezes cada item aparece. Desempata em ordem alfabética."""

        contagem = {}

        for t in self._filtrar_tipo(tipo):

            for item in extrair(t):
                contagem[item] = contagem.get(item, 0) + 1

        return sorted(contagem.items(), key=lambda i: (-i[1], i[0]))

    def ranking_paises(self, tipo=None):
        return self._contar(lambda t: t.paises, tipo)

    def ranking_generos(self, tipo=None):
        return self._contar(lambda t: t.generos, tipo)

    def ranking_classificacoes(self):
        return self._contar(lambda t: [t.classificacao] if t.classificacao else [])

    def ranking_duracao(self, tipo, quantidade=10):
        return self.ordenar_por_duracao(tipo)[:quantidade]

    def ranking_indice_destaque(self):

        return sorted(
            self._titulos,
            key=lambda t: (-t.calcular_indice_destaque(), -t.ano, normalizar(t.titulo)))

    def quantidade_por_decada(self):

        contagem = {}

        for t in self._titulos:

            decada = (t.ano // 10) * 10
            contagem[decada] = contagem.get(decada, 0) + 1

        return dict(sorted(contagem.items()))

    def distribuicao_tipo_pais(self):

        resultado = {}

        for t in self._titulos:

            for pais in t.paises:

                if pais not in resultado:
                    resultado[pais] = {"Filme": 0, "Série": 0}

                resultado[pais][t.tipo] += 1

        return resultado

    def paises_com_mais_series(self, minimo=MIN_TITULOS_PAIS):
        """Países com mais séries do que filmes (só os com 'minimo' títulos ou mais)."""

        resultado = []

        for pais, d in self.distribuicao_tipo_pais().items():

            total = d["Filme"] + d["Série"]

            if total >= minimo and d["Série"] > d["Filme"]:
                resultado.append((pais, d["Série"] / total * 100, d["Série"], d["Filme"]))

        return sorted(resultado, key=lambda i: -i[1])



# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# RELATÓRIOS EM ARQUIVO
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def _secao(linhas, titulo):

    linhas.append("")
    linhas.append("=" * 50)
    linhas.append(titulo)
    linhas.append("=" * 50)


def gerar_relatorio(catalogo, nome_arquivo):
    """Grava o relatório completo da base em arquivo texto."""

    linhas = []

    linhas.append("RELATÓRIO FINAL - CATÁLOGO NETFLIX")
    linhas.append("Resultados válidos apenas para a base analisada (títulos")
    linhas.append("adicionados até setembro de 2021), sem generalizar para o")
    linhas.append("catálogo atual da Netflix.")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "CARREGAMENTO DA BASE")

    linhas.append(f"Registros lidos: {catalogo.registros_lidos}")
    linhas.append(f"Registros válidos: {catalogo.registros_validos}")
    linhas.append(f"Registros inválidos: {catalogo.registros_invalidos}")

    for show_id, titulo, motivo in catalogo.invalidos:
        linhas.append(f"  - {show_id} | {titulo} | {motivo}")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "ESTATÍSTICAS GERAIS")

    antigo = catalogo.titulo_mais_antigo()
    recente = catalogo.titulo_mais_recente()

    linhas.append(f"Total de títulos: {catalogo.quantidade()}")
    linhas.append(f"Filmes: {catalogo.quantidade_filmes()} ({catalogo.percentual_filmes():.2f}%)")
    linhas.append(f"Séries: {catalogo.quantidade_series()} ({catalogo.percentual_series():.2f}%)")
    linhas.append(f"Ano médio de lançamento: {catalogo.ano_medio():.2f}")

    if antigo:
        linhas.append(f"Título mais antigo: {antigo.titulo} ({antigo.ano})")

    if recente:
        linhas.append(f"Título mais recente: {recente.titulo} ({recente.ano})")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "TÍTULOS POR PAÍS (um título conta em cada país)")

    for pais, qtd in catalogo.ranking_paises():
        linhas.append(f"{pais}: {qtd}")

    _secao(linhas, "TÍTULOS POR GÊNERO")

    for genero, qtd in catalogo.ranking_generos():
        linhas.append(f"{genero}: {qtd}")

    _secao(linhas, "GÊNEROS MAIS FREQUENTES EM FILMES (top 10)")

    for genero, qtd in catalogo.ranking_generos("Filme")[:10]:
        linhas.append(f"{genero}: {qtd}")

    _secao(linhas, "GÊNEROS MAIS FREQUENTES EM SÉRIES (top 10)")

    for genero, qtd in catalogo.ranking_generos("Série")[:10]:
        linhas.append(f"{genero}: {qtd}")

    _secao(linhas, "TÍTULOS POR CLASSIFICAÇÃO INDICATIVA")

    for classificacao, qtd in catalogo.ranking_classificacoes():
        linhas.append(f"{classificacao}: {qtd}")

    _secao(linhas, "TÍTULOS POR DÉCADA")

    for decada, qtd in catalogo.quantidade_por_decada().items():
        linhas.append(f"{decada}s: {qtd}")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "DISTRIBUIÇÃO POR TIPO E PAÍS")

    distribuicao = catalogo.distribuicao_tipo_pais()

    for pais in sorted(distribuicao):
        d = distribuicao[pais]
        linhas.append(f"{pais}: Filmes = {d['Filme']} | Séries = {d['Série']}")

    _secao(
        linhas,
        f"PAÍSES COM MAIS SÉRIES DO QUE FILMES (mínimo de {MIN_TITULOS_PAIS} títulos)")

    for pais, percentual, series, filmes in catalogo.paises_com_mais_series():
        linhas.append(f"{pais}: {percentual:.1f}% séries ({series} séries, {filmes} filmes)")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "MAIORES DURAÇÕES (filmes em minutos)")

    for i, t in enumerate(catalogo.ranking_duracao("Filme", 10), start=1):
        linhas.append(f"{i}º - {t.titulo} | {t.duracao_texto()}")

    _secao(linhas, "MAIORES DURAÇÕES (séries em temporadas)")

    for i, t in enumerate(catalogo.ranking_duracao("Série", 10), start=1):
        linhas.append(f"{i}º - {t.titulo} | {t.duracao_texto()}")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "BÔNUS - TOP 10 PELO ÍNDICE DE DESTAQUE")

    for i, t in enumerate(catalogo.ranking_indice_destaque()[:10], start=1):
        linhas.append(
            f"{i}º - {t.titulo} | {t.tipo} | {t.ano} | "
            f"Índice {t.calcular_indice_destaque()} "
            f"({t.classificacao_indice_destaque()})")

    # · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
    _secao(linhas, "REGRAS DE CLASSIFICAÇÃO")

    linhas.append(f"Por ano: antes de {ANO_INTERMEDIARIO} = antigo; "
                  f"de {ANO_INTERMEDIARIO} a {ANO_RECENTE - 1} = intermediário; "
                  f"a partir de {ANO_RECENTE} = recente.")
    linhas.append(f"Filme: menos de {FILME_CURTO} min = curto; "
                  f"{FILME_CURTO} a {FILME_LONGO} min = médio; "
                  f"mais de {FILME_LONGO} min = longo.")
    linhas.append(f"Série: até {SERIE_CURTA} temporada = curta; "
                  f"até {SERIE_MEDIA} = média; mais de {SERIE_MEDIA} = longa.")
    linhas.append("Produção internacional: título com mais de um país.")
    linhas.append(f"Título de destaque: pelo menos {PONTOS_MINIMOS_DESTAQUE} de 6 "
                  "critérios (recente, gênero, diretor, elenco, sinopse, duração longa).")

    _secao(linhas, "ÍNDICE DE DESTAQUE (BÔNUS)")

    linhas.append(f"+{PONTOS_RECENCIA} lançado a partir de {ANO_RECENTE}")
    linhas.append(f"+{PONTOS_GENERO} gênero de drama, comédia, ação ou documentário")
    linhas.append(f"+{PONTOS_INTERNACIONAL} produção em mais de um país")
    linhas.append(f"+{PONTOS_INFORMACAO} para cada: diretor, elenco e sinopse informados")
    linhas.append(f"+{PONTOS_DURACAO_LONGA} filme longo ou série longa")
    linhas.append("Categorias: 0-3 baixo; 4-5 médio; 6-7 alto; 8-10 muito alto.")
    linhas.append("")
    linhas.append("O índice é uma regra criada para este trabalho. Não mede a")
    linhas.append("qualidade dos títulos e depende do preenchimento da ficha.")

    _gravar(nome_arquivo, linhas)


def salvar_lista(resultados, nome_arquivo):
    """Grava uma lista de títulos (por exemplo, o resultado de um filtro)."""

    linhas = [f"Títulos encontrados: {len(resultados)}", ""]

    for t in resultados:
        linhas.append(f"{t.id} | {t.titulo} | {t.tipo} | {t.ano} | "
                      f"{t.pais or '-'} | {t.classificacao or '-'} | {t.duracao_texto()}")

    _gravar(nome_arquivo, linhas)


def _gravar(nome_arquivo, linhas):

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(linhas) + "\n")



# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# MENUS
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

# guarda a última lista exibida, para a opção "salvar última consulta"
estado = {"ultimo": []}


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# FUNÇÕES AUXILIARES
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def ler_inteiro(mensagem):

    while True:

        try:
            return int(input(mensagem))

        except ValueError:
            print("Digite apenas números inteiros.")


def perguntar_tipo():

    return input("Tipo (Filme ou Série): ").strip()


def perguntar_quantidade(total):

    print("\nQuantos resultados deseja visualizar?")
    print("1 - 20 resultados")
    print("2 - 50 resultados")
    print("3 - 100 resultados")
    print("4 - 500 resultados")
    print("5 - Todos os resultados")

    opcao = input("\nEscolha uma opção: ").strip()

    opcoes = {"1": 20, "2": 50, "3": 100, "4": 500, "5": total}

    if opcao not in opcoes:
        print("\nOpção inválida. Mostrando 20 resultados.")
        return 20

    return opcoes[opcao]


def mostrar_resultados(resultados):

    estado["ultimo"] = resultados

    if not resultados:
        print("\nNenhum título encontrado.")
        return

    print(f"\nForam encontrados {len(resultados)} títulos.")

    quantidade = perguntar_quantidade(len(resultados))

    print(f"\nMostrando {min(quantidade, len(resultados))} resultados:\n")

    for t in resultados[:quantidade]:
        print(f"{t.id} - {t.titulo} | {t.tipo} | {t.ano} | {t.duracao_texto()}")

    if len(resultados) > quantidade:
        print(f"\nAinda existem {len(resultados) - quantidade} resultados não exibidos.")


def mostrar_primeiros(resultados, quantidade=10):

    estado["ultimo"] = resultados

    if not resultados:
        print("\nNenhum título encontrado.")
        return

    print(f"\nPrimeiros {min(quantidade, len(resultados))} registros:\n")

    for t in resultados[:quantidade]:
        print(f"{t.titulo} | {t.tipo} | {t.ano} | {t.duracao_texto()}")


def mostrar_ranking(titulo, ranking, quantidade=10):

    print("\n· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")
    print(                 titulo)
    print("· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")

    for posicao, (nome, qtd) in enumerate(ranking[:quantidade], start=1):
        print(f"{posicao}º - {nome}: {qtd} títulos")


def mostrar_lista_completa(titulo, ranking):

    print(f"\n· ═══════ · {titulo} · ═══════ ·")

    for nome, qtd in ranking:
        print(f"{nome}: {qtd}")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# MENU DE CONSULTAS
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def menu_consultas(catalogo):

    while True:

        print("\n· ═══════ · ═══════ ·· ═══════ · ═══════ ·")
        print("                CONSULTAS")
        print("· ═══════ · ═══════ ·· ═══════ · ═══════ ·")

        print("1 - Buscar por ID")
        print("2 - Buscar por nome exato")
        print("3 - Buscar por parte do título")
        print("4 - Buscar por diretor")
        print("5 - Buscar por ator/atriz")
        print("6 - Buscar por país")
        print("7 - Buscar por gênero")
        print("8 - Listar filmes")
        print("9 - Listar séries")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":

            resultado = catalogo.buscar_por_id(input("Digite o ID: "))

            if resultado:
                resultado.mostrar_informacoes()
            else:
                print("\nNenhum título encontrado.")

        elif opcao == "2":
            mostrar_resultados(catalogo.buscar_por_nome(input("Digite o nome completo: ")))

        elif opcao == "3":
            mostrar_resultados(catalogo.buscar_por_parte_titulo(input("Digite parte do título: ")))

        elif opcao == "4":
            mostrar_resultados(catalogo.buscar_por_diretor(input("Digite o nome do diretor: ")))

        elif opcao == "5":
            mostrar_resultados(catalogo.buscar_por_ator(input("Digite o nome do ator/atriz: ")))

        elif opcao == "6":
            mostrar_resultados(catalogo.buscar_por_pais(input("Digite o país (em inglês): ")))

        elif opcao == "7":
            mostrar_resultados(catalogo.buscar_por_genero(input("Digite o gênero: ")))

        elif opcao == "8":
            mostrar_resultados(catalogo.listar_filmes())

        elif opcao == "9":
            mostrar_resultados(catalogo.listar_series())

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# MENU DE FILTROS
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def menu_filtros(catalogo):

    while True:

        print("\n· ═══════ ·❀· ═══════ ·❀· ═══════ ·")
        print("               FILTROS")
        print("· ═══════ ·❀· ═══════ ·❀· ═══════ ·")

        print("1 - Filtrar por tipo")
        print("2 - Filtrar por país")
        print("3 - Filtrar por gênero")
        print("4 - Filtrar por classificação indicativa")
        print("5 - Filtrar por intervalo de ano")
        print("6 - Filtrar por duração mínima")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            mostrar_resultados(catalogo.filtrar_por_tipo(perguntar_tipo()))

        elif opcao == "2":
            mostrar_resultados(catalogo.filtrar_por_pais(input("Digite o país (em inglês): ")))

        elif opcao == "3":
            mostrar_resultados(catalogo.filtrar_por_genero(input("Digite o gênero: ")))

        elif opcao == "4":
            mostrar_resultados(
                catalogo.filtrar_por_classificacao(input("Digite a classificação (ex.: TV-MA, PG-13): ")))

        elif opcao == "5":
            ano_inicial = ler_inteiro("Ano inicial: ")
            ano_final = ler_inteiro("Ano final: ")
            mostrar_resultados(catalogo.filtrar_por_ano(ano_inicial, ano_final))

        elif opcao == "6":
            print("(filmes em minutos, séries em temporadas)")
            tipo = perguntar_tipo()
            minimo = ler_inteiro("Duração mínima: ")
            mostrar_resultados(catalogo.filtrar_por_duracao(tipo, minimo))

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
#  MENU DE ESTATÍSTICAS
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def mostrar_estatisticas(catalogo):

    antigo = catalogo.titulo_mais_antigo()
    recente = catalogo.titulo_mais_recente()

    print("\n· ═══════ · ═══════ ·· ═══════ · ═══════ ·")
    print("           ESTATÍSTICAS DA BASE")
    print("· ═══════ · ═══════ ·· ═══════ · ═══════ ·")

    print(f"Total de títulos: {catalogo.quantidade()}")
    print(f"Filmes: {catalogo.quantidade_filmes()} ({catalogo.percentual_filmes():.2f}%)")
    print(f"Séries: {catalogo.quantidade_series()} ({catalogo.percentual_series():.2f}%)")
    print(f"Ano médio: {catalogo.ano_medio():.2f}")

    if antigo:
        print(f"Título mais antigo: {antigo.titulo} ({antigo.ano})")

    if recente:
        print(f"Título mais recente: {recente.titulo} ({recente.ano})")


def menu_estatisticas(catalogo):

    while True:

        print("\n· ═══════ · ═══════ ·· ═══════ · ═══════ ·")
        print("                ESTATÍSTICAS")
        print("· ═══════ · ═══════ ·· ═══════ · ═══════ ·")

        print("1 - Estatísticas gerais")
        print("2 - Quantidade por década")
        print("3 - Distribuição tipo x país")
        print("4 - Quantidade por país (lista completa)")
        print("5 - Quantidade por gênero (lista completa)")
        print("6 - Quantidade por classificação indicativa")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            mostrar_estatisticas(catalogo)

        elif opcao == "2":

            print("\n· ═══════ · TÍTULOS POR DÉCADA · ═══════ ·")

            for decada, qtd in catalogo.quantidade_por_decada().items():
                print(f"{decada}s: {qtd} títulos")

        elif opcao == "3":

            print("\n· ═══════ · TIPO X PAÍS · ═══════ ·")

            distribuicao = catalogo.distribuicao_tipo_pais()

            for pais in sorted(distribuicao):
                d = distribuicao[pais]
                print(f"{pais}: Filmes = {d['Filme']} | Séries = {d['Série']}")

        elif opcao == "4":
            mostrar_lista_completa("TÍTULOS POR PAÍS", catalogo.ranking_paises())

        elif opcao == "5":
            mostrar_lista_completa("TÍTULOS POR GÊNERO", catalogo.ranking_generos())

        elif opcao == "6":
            mostrar_lista_completa("TÍTULOS POR CLASSIFICAÇÃO", catalogo.ranking_classificacoes())

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# MENU DE RANKINGS
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def menu_rankings(catalogo):

    while True:

        print("\n· ═══════ · ═══════ ·· ═══════ · ═══════ ·")
        print("                RANKINGS")
        print("· ═══════ · ═══════ ·· ═══════ · ═══════ ·")

        print("1 - Países com mais títulos")
        print("2 - Gêneros mais frequentes")
        print("3 - Classificações mais frequentes")
        print("4 - Maiores durações (por tipo)")
        print("5 - Gêneros mais frequentes em filmes")
        print("6 - Gêneros mais frequentes em séries")
        print("7 - Países com mais séries do que filmes")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            mostrar_ranking("TOP PAÍSES", catalogo.ranking_paises())

        elif opcao == "2":
            mostrar_ranking("TOP GÊNEROS", catalogo.ranking_generos())

        elif opcao == "3":
            mostrar_ranking("TOP CLASSIFICAÇÕES", catalogo.ranking_classificacoes())

        elif opcao == "4":

            tipo = perguntar_tipo()
            resultados = catalogo.ranking_duracao(tipo)

            if not resultados:
                print("\nTipo inválido.")
                continue

            print("\n· ═══════ · ═══════ ·· ═══════ · ═══════ ·")
            print("             MAIORES DURAÇÕES")
            print("· ═══════ · ═══════ ·· ═══════ · ═══════ ·")

            for posicao, t in enumerate(resultados, start=1):
                print(f"{posicao}º - {t.titulo} | {t.duracao_texto()}")

        elif opcao == "5":
            mostrar_ranking("GÊNEROS EM FILMES", catalogo.ranking_generos("Filme"))

        elif opcao == "6":
            mostrar_ranking("GÊNEROS EM SÉRIES", catalogo.ranking_generos("Série"))

        elif opcao == "7":

            print("\n· ═══════ ·· ═══════ ·· ═══════ ·")
            print("PAÍSES COM MAIS SÉRIES DO QUE FILMES")
            print("(somente países com 10 ou mais títulos)")
            print("· ═══════ ·· ═══════ ·· ═══════ ·")

            for pais, percentual, series, filmes in catalogo.paises_com_mais_series():
                print(f"{pais}: {percentual:.1f}% séries ({series} séries x {filmes} filmes)")

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# MENU DE ORDENAÇÃO
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def menu_ordenacao(catalogo):

    while True:

        print("\n· ═══════ ·· ═══════ ·· ═══════ ·")
        print("           Ordenação")                      
        print("· ═══════ ·· ═══════ ·· ═══════ ·")

        print("1 - Por título")
        print("2 - Por ano crescente")
        print("3 - Por ano decrescente")
        print("4 - Por duração (decrescente, por tipo)")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            mostrar_primeiros(catalogo.ordenar_por_titulo())

        elif opcao == "2":
            mostrar_primeiros(catalogo.ordenar_por_ano())

        elif opcao == "3":
            mostrar_primeiros(catalogo.ordenar_por_ano_decrescente())

        elif opcao == "4":

            tipo = perguntar_tipo()

            tipo = normalizar_tipo(tipo)

            if tipo is None:
                print("\nTipo inválido.")
            else:
                mostrar_primeiros(catalogo.ordenar_por_duracao(tipo))

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# CLASSIFICAÇÕES BASEADAS EM REGRAS
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def classificar_titulo(catalogo):

    titulo = catalogo.buscar_por_id(input("\nDigite o ID do título: "))

    if not titulo:
        print("\nTítulo não encontrado.")
        return

    print("\n· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")
    print("                CLASSIFICAÇÃO")
    print("· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")

    print(f"Título: {titulo.titulo}")
    print(f"Tipo: {titulo.tipo}")
    print(f"Ano: {titulo.ano}")
    print(f"Classificação por ano: {titulo.classificar_por_ano()}")
    print(f"Classificação por duração: {titulo.classificar_duracao()}")
    print(f"Classificação internacional: {titulo.classificacao_internacional()}")
    print(f"Classificação de destaque: {titulo.classificacao_destaque()}")
    print(f"Índice de destaque: {titulo.calcular_indice_destaque()} "
          f"({titulo.classificacao_indice_destaque()})")


def mostrar_ranking_indice(catalogo):

    resultados = catalogo.ranking_indice_destaque()

    estado["ultimo"] = resultados

    print("\n· ═══════ ·❀· ═══════ ·❀· ═══════ ·")
    print("     ÍNDICE DE DESTAQUE - BÔNUS")
    print("· ═══════ ·❀· ═══════ ·❀· ═══════ ·")

    print(f"Total de títulos avaliados: {len(resultados)}")

    quantidade = perguntar_quantidade(len(resultados))

    for posicao, t in enumerate(resultados[:quantidade], start=1):
        print(
            f"{posicao}º - {t.id} - {t.titulo} | {t.tipo} | "
            f"Índice: {t.calcular_indice_destaque()} | "
            f"Categoria: {t.classificacao_indice_destaque()}")


def menu_classificacoes(catalogo):

    while True:

        print("\n· ═══════ ·❀· ═══════ ·❀· ═══════ ·")
        print(" CLASSIFICAÇÕES BASEADAS EM REGRAS")
        print("· ═══════ ·❀· ═══════ ·❀· ═══════ ·")

        print("1 - Ver classificação de um título")
        print("2 - Listar títulos internacionais")
        print("3 - Listar títulos de destaque")
        print("4 - Buscar interesse específico")
        print("5 - Índice de destaque (BÔNUS)")
        print("0 - Voltar")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            classificar_titulo(catalogo)

        elif opcao == "2":
            mostrar_resultados(catalogo.listar_internacionais())

        elif opcao == "3":
            mostrar_resultados(catalogo.listar_destaques())

        elif opcao == "4":

            print("\nPreencha apenas os critérios que deseja utilizar.")

            pais = input("País ou Enter para ignorar: ").strip()
            genero = input("Gênero ou Enter para ignorar: ").strip()
            tipo = input("Tipo (Filme/Série) ou Enter para ignorar: ").strip()
            classificacao = input("Classificação ou Enter para ignorar: ").strip()

            mostrar_resultados(
                catalogo.filtrar_interesse(
                    pais=pais or None,
                    genero=genero or None,
                    tipo=tipo or None,
                    classificacao=classificacao or None
                )
            )

        elif opcao == "5":
            mostrar_ranking_indice(catalogo)

        elif opcao == "0":
            break

        else:
            print("\nOpção inválida.")


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# BUSCA COMBINADA
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def ler_ano_opcional(mensagem):
    """Devolve (valido, valor). Enter vazio = ignorar."""

    texto = input(mensagem).strip()

    if not texto:
        return True, None

    try:
        return True, int(texto)

    except ValueError:
        print("\nAno inválido.")
        return False, None


def menu_busca_combinada(catalogo):

    print("\n· ═══════ ·· ═══════ ·· ═══════ ·")
    print("         BUSCA COMBINADA")
    print("· ═══════ ·· ═══════ ·· ═══════ ·")

    tipo = input("Tipo (Filme/Série ou Enter para ignorar): ").strip()
    pais = input("País ou Enter para ignorar: ").strip()
    genero = input("Gênero ou Enter para ignorar: ").strip()
    classificacao = input("Classificação ou Enter para ignorar: ").strip()

    valido, ano_inicial = ler_ano_opcional("Ano inicial ou Enter para ignorar: ")

    if not valido:
        return

    valido, ano_final = ler_ano_opcional("Ano final ou Enter para ignorar: ")

    if not valido:
        return

    mostrar_resultados(
        catalogo.busca_combinada(
            tipo=tipo or None,
            pais=pais or None,
            genero=genero or None,
            classificacao=classificacao or None,
            ano_inicial=ano_inicial,
            ano_final=ano_final
        )
    )


# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
#              MENU PRINCIPAL
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def menu(catalogo):

    while True:

        print("\n")
        print("· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")
        print("                SISTEMA NETFLIX")
        print("· ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·")

        print(f"Títulos carregados: {catalogo.quantidade()}")

        print()
        print("1 - Consultar título")
        print("2 - Filtrar títulos")
        print("3 - Ver estatísticas")
        print("4 - Ver rankings")
        print("5 - Ordenar títulos")
        print("6 - Classificações baseadas em regras")
        print("7 - Busca combinada")
        print("8 - Gerar relatório completo")
        print("9 - Salvar última lista exibida em arquivo")
        print("0 - Sair")

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            menu_consultas(catalogo)

        elif opcao == "2":
            menu_filtros(catalogo)

        elif opcao == "3":
            menu_estatisticas(catalogo)

        elif opcao == "4":
            menu_rankings(catalogo)

        elif opcao == "5":
            menu_ordenacao(catalogo)

        elif opcao == "6":
            menu_classificacoes(catalogo)

        elif opcao == "7":
            menu_busca_combinada(catalogo)

        elif opcao == "8":
            gerar_relatorio(catalogo, "relatorio_final_netflix.txt")
            print("\nRelatório salvo em: relatorio_final_netflix.txt")

        elif opcao == "9":

            if not estado["ultimo"]:
                print("\nNenhuma lista para salvar. Faça uma consulta primeiro.")
            else:
                salvar_lista(estado["ultimo"], "ultima_consulta.txt")
                print(f"\n{len(estado['ultimo'])} títulos salvos em: ultima_consulta.txt")

        elif opcao == "0":
            print("\nPrograma encerrado.")
            break

        else:
            print("\nOpção inválida.")



# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·
# PROGRAMA PRINCIPAL
# · ═══════ ·❀· ═══════ ·· ═══════ ·❀· ═══════ ·

def main():

    catalogo = CatalogoNetflix()

    arquivo_csv = "netflix_titles.csv"

    try:
        catalogo.carregar_csv(arquivo_csv)

    except FileNotFoundError:
        print("\nERRO: arquivo CSV não encontrado.")
        print(f"Verifique se '{arquivo_csv}' está na mesma pasta do programa.")
        return

    except Exception as erro:
        print("\nERRO ao carregar o arquivo:")
        print(erro)
        return

    print("\n· ═══════ ·❀ · ═══════ ·❀ · ═══════ ·")
    print("        CARREGAMENTO DA BASE")
    print("· ═══════ ·❀ · ═══════ ·❀ · ═══════ ·")

    print(f"Registros lidos: {catalogo.registros_lidos}")
    print(f"Registros válidos: {catalogo.registros_validos}")
    print(f"Registros inválidos: {catalogo.registros_invalidos}")

    for show_id, titulo, motivo in catalogo.invalidos:
        print(f"  - {show_id} | {titulo} | {motivo}")

    print("\nBase carregada com sucesso!")

    menu(catalogo)


if __name__ == "__main__":
    main()