# Catálogo: guarda os títulos e responde consultas (sem print/input).

import csv

from constantes import MIN_TITULOS_PAIS
from factory import TituloFactory
from titulo import Filme, Serie
from utils import normalizar, normalizar_tipo, contem_item


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
