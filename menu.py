# Menus e interação com o usuário (print/input).

from relatorio import gerar_relatorio, salvar_lista
from utils import normalizar_tipo


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
