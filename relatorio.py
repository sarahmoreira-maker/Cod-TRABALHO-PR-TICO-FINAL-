# Geração de relatórios em arquivo texto.

from constantes import (
    ANO_INTERMEDIARIO, ANO_RECENTE,
    FILME_CURTO, FILME_LONGO, SERIE_CURTA, SERIE_MEDIA,
    PONTOS_MINIMOS_DESTAQUE, PONTOS_RECENCIA, PONTOS_GENERO,
    PONTOS_INTERNACIONAL, PONTOS_INFORMACAO, PONTOS_DURACAO_LONGA,
    MIN_TITULOS_PAIS
)


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
