# Imports necessários
import scripts.similaridade as similaridade
import scripts.util as util
import scripts.imdb_to_db as imdb_to_db
import pandas as pd


# Funções para a recomendação
def recomendar_para_usuario(usuario):
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

    # Depois, vamos calcular os usuários mais similares. São 3 listas,
    # correspondente a 3 camadas de proximidade.
    mais_proximos = similaridade.mais_proximos(usuario)

    # Se o usuário não tem nenhum usuário proximo, retorna None
    if not mais_proximos:
        return None

    # Então, pegamos todas as notas de todos os filmes que tem pelo
    # menos 50 avaliações
    notas_dos_filmes_considerados = util.get_todas_as_notas().set_index("movieId").loc[util.get_filmes_50_votos_ou_mais().index]

    recomendacoes_camada1 = None
    recomendacoes_camada2 = None
    recomendacoes_camada3 = None
    for i, camada in enumerate(mais_proximos):
        # Resetamos o índice da DataFrame para restaurar a coluna "MovieId",
        # em seguida, setamos o índice para "userId" para buscar apenas
        # as notas dos usuários similares
        notas_dos_filmes_considerados = notas_dos_filmes_considerados.reset_index()
        notas_dos_similares = notas_dos_filmes_considerados.query("userId in @camada")
        # Calculamos a média de cada filme considerando apenas as notas dos usuários similares
        media_notas_dos_similares = notas_dos_similares.groupby("movieId").mean()[["rating"]]
        # Contamos a quantidade de avaliações de cada filme pelos usuários
        # similares
        qntd_visualizacoes = notas_dos_similares.groupby("movieId").count()[["rating"]]

        # Unificamos as tabela de média e quantidade de avaliações.
        recomendacoes = media_notas_dos_similares.join(qntd_visualizacoes, lsuffix="_media", rsuffix="_qntd_avaliacoes")

        # Filtramos os filmes que foram assistidos por, pelo menos, um quarto
        # dos usuários próximos e ordenamos pelas médias
        filtro = int(len(camada) / 4)
        recomendacoes = recomendacoes.query(f"rating_qntd_avaliacoes >= {filtro}")
        recomendacoes = recomendacoes.sort_values("rating_media", ascending=False)
        # Os filmes que já foram assistidos pelo usuário são removidos dessa
        # lista
        recomendacoes = recomendacoes.drop(filmes_ja_assistidos, errors="ignore")
        # Por fim, unimos à lista os titulos e demais informações dos filmes
        recomendacoes = recomendacoes.join(util.get_filmes_50_votos_ou_mais())
        notas_dos_filmes_considerados = notas_dos_filmes_considerados.set_index("movieId")

        if i == 0:
            recomendacoes_camada1 = recomendacoes.head(5)
            recomendados = recomendacoes_camada1.index
            notas_dos_filmes_considerados = notas_dos_filmes_considerados.drop(recomendados, errors='ignore')
        elif i == 1:
            recomendacoes_camada2 = recomendacoes.head(3)
            recomendados = recomendacoes_camada2.index
            notas_dos_filmes_considerados = notas_dos_filmes_considerados.drop(recomendados, errors='ignore')
        elif i == 2:
            recomendacoes_camada3 = recomendacoes.head(2)

    recomendacoes = pd.concat([recomendacoes_camada1, recomendacoes_camada2, recomendacoes_camada3])
    recomendacoes = [int(filme) for filme in recomendacoes.index]
    recomendacoes = [imdb_to_db.busca_por_id(filme) for filme in recomendacoes]

    # Retorna-se a lista de recomendações, sendo 5 da primeira camada,
    # 3 da segunda e 2 da terceira
    return recomendacoes
