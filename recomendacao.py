# Imports necessários
import similaridade
import util


# Funções para a recomendação
def recomendar_para_usuario(usuario, qntd_usuarios_analisados=None, qntd_usuarios_mais_proximos=10, qntd_recomendacoes=10):
    """
    Retorna os filmes recomendados para o usuário informado.

    Keyword arguments:
    usuario_raiz -- id do usuário raiz
    qntd_usuarios_analisados -- Número de usuários a serem analisados,
        default: 610 (Todos os usuários)
    qntd_usuarios_mais_proximos -- Número de usuários similares
    considerados, default: 10
    qntd_recomendacoes -- Quantidade de filmes que serão recomendados ao
        usuário, default: 10 filmes
    """

    # Primeiro, pegamos todas as notas dadas pelo usuário raiz
    notas_do_usuario = util.get_notas_por_usuario(usuario)
    # Os indices dessa DataFrame corresponderão às ids dos filmes já
    # assistidos pelo usuário
    filmes_ja_assistidos = notas_do_usuario.index

    # Depois, vamos calcular os usuários mais similares ao raiz, por
    # padrão, selecionam-se 10
    usuarios_mais_similares = similaridade.mais_proximos(usuario, qntd_usuarios_analisados=qntd_usuarios_analisados, qntd_usuarios_mais_proximos=qntd_usuarios_mais_proximos)
    # Os índices desta DataFrame corresponderão às ids dos usuários
    # similares que estão sendo considerados
    usuarios_mais_similares_lista_ids = usuarios_mais_similares.index
    # Atualizamos a qntd_usuarios_mais_proximos para corresponder ao real utilizado
    qntd_usuarios_mais_proximos = usuarios_mais_similares['usuario_raiz'].count()

    # Então, pegamos todas as notas de todos os filmes que tem pelo
    # menos 50 avaliações
    notas_filmes_50_ou_mais = util.get_todas_as_notas().set_index("movieId").loc[util.get_filmes_50_votos_ou_mais().index]

    # Resetamos o índice da DataFrame para restaurar a coluna "MovieId",
    # em seguida, setamos o índice para "userId" para buscar apenas
    # as notas dos usuários similares
    notas_filmes_50_ou_mais = notas_filmes_50_ou_mais.reset_index()
    notas_dos_similares = notas_filmes_50_ou_mais.set_index("userId").loc[usuarios_mais_similares_lista_ids]
    # Calculamos a média de cada filme considerando apenas as notas dos usuários similares
    media_notas_dos_similares = notas_dos_similares.groupby("movieId").mean()[["rating"]]
    # Contamos a quantidade de avaliações de cada filme pelos usuários
    # similares
    qntd_visualizacoes = notas_dos_similares.groupby("movieId").count()[["rating"]]

    # Unificamos as tabela de média e quantidade de avaliações.
    recomendacoes = media_notas_dos_similares.join(qntd_visualizacoes, lsuffix="_media", rsuffix="_qntd_avaliacoes")

    # Filtramos os filmes que foram assistidos por, pelo menos, um terço
    # dos usuários próximos e ordenamos pelas médias
    filtro = int(qntd_usuarios_mais_proximos / 3)
    recomendacoes = recomendacoes.query(f"rating_qntd_avaliacoes >= {filtro}")
    recomendacoes = recomendacoes.sort_values("rating_media", ascending=False)
    # Os filmes que já foram assistidos pelo usuário são removidos dessa
    # lista
    recomendacoes = recomendacoes.drop(filmes_ja_assistidos, errors="ignore")
    # Por fim, unimos à lista os titulos e demais informações dos filmes
    recomendacoes = recomendacoes.join(util.get_filmes_50_votos_ou_mais())

    # Retorna-se a lista gerada, na quantidade solicitada na chamada do
    # método
    return recomendacoes.head(qntd_recomendacoes)


