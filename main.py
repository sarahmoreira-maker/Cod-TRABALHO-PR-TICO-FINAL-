# Programa principal: carrega a base e abre o menu.
# Para executar:  python main.py
# (deixe netflix_titles.csv na mesma pasta)

from catalogo import CatalogoNetflix
from menu import menu


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
