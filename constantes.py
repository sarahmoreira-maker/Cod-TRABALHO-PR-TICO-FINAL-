# Limites e regras usados nas classificações do sistema.


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
