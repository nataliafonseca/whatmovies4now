from lib.interface import *
from lib.arvore import Arvore
from prettytable import PrettyTable
from datetime import datetime
from jsonpickle import encode, decode
from colorama import Fore, init as color
from copy import deepcopy
from random import shuffle

color()


class Grafo:
    """
    Classe para implementação da representação e algorítmos de grafos.
    """

    def __init__(self, digrafo, valorado, vertices, arestas):
        """
        Construtor da Classe
        :param digrafo: True se o grafo for direcionado, False se não.
        :param valorado: True se o grafo for valorado, False se não.
        :param vertices: Lista de Vértices do grafo.
        :param arestas: Lista de Arestas do grafo.
        """
        self._id_grafo = f"{datetime.now().strftime('%Y%m%d%H%M%S')}"
        self._digrafo = digrafo
        self._valorado = valorado
        self._vertices = vertices
        self._arestas = arestas
        self._max_peso = 1

    def imprimir_informacoes(self):
        """
        Método que imprime as informações do grafo (vértices, arestas,
        se é digrafo, se é valorado, se é regular, se é completo, se é
        conexo, fortemente conexo, a quantidade de componentes conexos
        e fortemente conexos, se aplicável).
        """
        cabecalho(Fore.BLUE + f"{self._id_grafo}" + Fore.RESET)
        print(f"{Fore.YELLOW}Vertices:{Fore.RESET} {self._vertices}")
        print(f"{Fore.YELLOW}Arestas:{Fore.RESET} {self._arestas}")
        print(f"{Fore.YELLOW}Digrafo:{Fore.RESET} {self._digrafo}")
        print(f"{Fore.YELLOW}Valorado:{Fore.RESET} {self._valorado}")
        print(f"{Fore.YELLOW}Regular:{Fore.RESET} {self.regular()}")
        print(f"{Fore.YELLOW}Completo:{Fore.RESET} {self.completo()}")
        print(f"{Fore.YELLOW}Conexo:{Fore.RESET} {self.conexo()}")
        if not self.conexo():
            print(f"{Fore.YELLOW}Quantidade de componentes conexos: "
                  f"{Fore.RESET}{self.get_q_componentes_conexos()}")
        if self._digrafo:
            print(f"{Fore.YELLOW}Fortemente Conexo:{Fore.RESET} "
                  f"{self.fortemente_conexo()}")
            if not self.fortemente_conexo():
                print(f"{Fore.YELLOW}Quantidade de componentes fortemente "
                      f"conexos:{Fore.RESET} "
                      f"{self.get_q_componente_fortemente_conexos()}")

    @staticmethod
    def retorna_grafo():
        """
        Método que retorna o grafo correspondente à id, caso este esteja
        no arquivo grafo.json
        """
        with open("grafo.json", "r") as grafos_json:
            for line in grafos_json:
                grafo = decode(line)
        return grafo

    def estrutura_adjacencia(self):
        """
        Método que retorna um dicionário correspondente à estrutura de
        adjacencia que representa o grafo.
        """
        estrutura_adjacencia = {}
        for i in range(len(self._vertices)):
            estrutura_adjacencia.update({self._vertices[i]: []})
        arestas = self._arestas
        if self._valorado:
            for trio in arestas:
                i, j, p = trio.strip().split("-")
                p = float(p)
                estrutura_adjacencia[i].append({'vertice_id': j, 'peso': p})
                if not self._digrafo:
                    estrutura_adjacencia[j].append({'vertice_id': i,
                                                    'peso': p})
                if p > self._max_peso:
                    self._max_peso = p
        else:
            for par in arestas:
                i, j = par.strip().split("-")
                estrutura_adjacencia[i].append({'vertice_id': j, 'peso': 1})
                if not self._digrafo:
                    estrutura_adjacencia[j].append({'vertice_id': i,
                                                    'peso': 1})
        return estrutura_adjacencia

    def imprimir_estrutura_adjacencia(self):
        """
        Metodo que imprime a estutura de adjacencia do grafo, formatada
        para facilitar a leitura.
        """
        estrutura_adjacencia = self.estrutura_adjacencia()
        wg = len((max(estrutura_adjacencia, key=len)))
        wp = len(str(self._max_peso))
        for i in estrutura_adjacencia:
            print(f"{Fore.YELLOW}{i:<{wg}}", end=' -> ')
            for j in estrutura_adjacencia[i]:
                print(f"{Fore.RESET}{j['vertice_id']:<{wg}}"
                      f"_P{j['peso']:<{wp}}", end=' | ')
            print()

    def matriz_adjacencia(self):
        """
        Método que retorna uma matriz correspondente à matriz de
        adjacencia que representa o grafo.
        """
        matriz_adjacencia = []
        for i in range(len(self._vertices)):
            matriz_adjacencia.append([0] * len(self._vertices))
        arestas = self._arestas
        if self._valorado:
            for trio in arestas:
                i, j, p = trio.replace(" ", "").split("-")
                i, j = self._vertices.index(i), self._vertices.index(j)
                p = float(p)
                matriz_adjacencia[i][j] = p
                if not self._digrafo:
                    matriz_adjacencia[j][i] = p
        else:
            for par in arestas:
                i, j = par.replace(" ", "").split("-")
                i, j = self._vertices.index(i), self._vertices.index(j)
                matriz_adjacencia[i][j] = 1
                if not self._digrafo:
                    matriz_adjacencia[j][i] = 1
        return matriz_adjacencia

    def imprimir_matriz_adjacencia(self):
        """
        Metodo que imprime a matriz de adjacencia do grafo, formatada
        para facilitar a leitura.
        """
        grafo = self.matriz_adjacencia()

        x = PrettyTable([Fore.YELLOW + "*" + Fore.RESET] +
                        [f"{Fore.YELLOW}{vertice}{Fore.RESET}"
                         for vertice in self._vertices])
        for idx, vertice in enumerate(self._vertices):
            x.add_row([f"{Fore.YELLOW}{vertice}{Fore.RESET}"] + grafo[idx])
        print(x)

    def get_adjacentes(self, vertice):
        """
        Método que recebe um vértice do grafo e retorna uma lista
        contendo os vértices adjacentes a ele.
        """
        grafo = self.estrutura_adjacencia()
        adjacentes = []
        for i in grafo[vertice]:
            adjacentes.append(i['vertice_id'])
        return adjacentes

    def _get_adjacentes_e_pesos(self, vertice):
        """
        Método privado que recebe um vértice do grafo e retorna uma
        lista contendo os vértices adjacentes a ele e uma outra lista
        contendo seus respectivos pesos.
        """
        grafo = self.estrutura_adjacencia()
        adjacentes = []
        pesos = []
        for i in grafo[vertice]:
            adjacentes.append(i['vertice_id'])
            pesos.append(i['peso'])
        return adjacentes, pesos

    def regular(self):
        """
        Método que retorna verdadeiro se o grafo for regular ou falso se
         não for.
        """
        regular = True
        for idx, vertice in enumerate(self._vertices):
            if len(self.get_adjacentes(self._vertices[0])) != \
                    len(self.get_adjacentes(self._vertices[idx])):
                regular = False
        return regular

    def completo(self):
        """
        Método que retorna verdadeiro se o grafo for completo ou falso
        se não for.
        """
        completo = True
        for vertice in self._vertices:
            if len(self.get_adjacentes(vertice)) != len(self._vertices) - 1:
                completo = False
        return completo

    def conexo(self):
        """
        Método que retorna verdadeiro se o grafo for conexo ou falso se
        não for.
        """
        conexo = True
        if self.get_q_componentes_conexos() > 1:
            conexo = False
        return conexo

    def _largura(self, vertice_inicial):
        """
        Método privado que aplica a lógica da busca em largura,
        recebendo um vértice inicial e buscando até que se zere a fila,
         o retorno é a árvore de vértices visitados, em ordem.
        """
        fila = [vertice_inicial]
        vertices_visitados = Arvore(vertice_inicial)

        while fila:
            vertice = fila[0]
            fila.pop(0)
            for w in self.get_adjacentes(vertice):
                if not vertices_visitados.localizar_nodo(w):
                    vertices_visitados.inserir_nodo(vertice, w)
                    fila.append(w)

        return vertices_visitados

    def busca_largura(self, vertice_inicial="nao_informado"):
        """
        Método para repetição da lógica de busca em largura até que
        todos os vértices do grafo tenham sido visitados. Recebe,
        opcionalmente, o vértice inicial. Retorna a árvore completa de
        vértices visitados.
        """
        if vertice_inicial == "nao_informado":
            vertice = self._vertices[0]
        else:
            vertice = vertice_inicial
        q_componentes = 0
        vertices_visitados = []
        q_vertices_visitados = 0

        while q_vertices_visitados < len(self._vertices):

            if q_componentes > 0:
                for v in self._vertices:
                    visitado = False
                    for arvore in vertices_visitados:
                        if arvore.localizar_nodo(v):
                            visitado = True
                            break
                    if not visitado:
                        vertice = v
                        break

            vertices_visitados.append(self._largura(vertice))
            q_componentes += 1
            # soma-se a q_vertices_visitados a quantidade de vértices
            # presentes na árvore adicionada à lista!
            q_vertices_visitados += vertices_visitados[-1].quantidade

        return {'visitados': vertices_visitados,
                'q_componentes': q_componentes}

    def imprimir_busca_largura(self, vertice_inicial="nao_informado"):
        """
        Método para impreção da árvore de busca em largura, formatada
        para falicitar a leitura.
        """
        vertices_visitados = self.busca_largura(vertice_inicial)['visitados']
        # vertices_visitados = self._busca_geral('largura', vertice_inicial)[0]
        for i in range(len(vertices_visitados)):
            vertices_visitados[i].imprimir()

    def _profundidade(self, vertice_inicial):
        """
        Método privado que aplica a lógica da busca em profunidade,
        recebendo um vértice inicial e buscando até que se zere a pilha,
         o retorno é a lista de vértices visitados, em ordem.
        """
        pilha = [vertice_inicial]
        vertices_visitados = Arvore(vertice_inicial)
        lista_posordem = []

        while pilha:
            vertice = pilha[-1]
            explorado = True
            for w in self.get_adjacentes(vertice):
                if not vertices_visitados.localizar_nodo(w):
                    explorado = False
                    break
            if explorado:
                lista_posordem.append(pilha[-1])
                pilha.pop(-1)
            for w in self.get_adjacentes(vertice):
                if not vertices_visitados.localizar_nodo(w):
                    vertices_visitados.inserir_nodo(vertice, w)
                    pilha.append(w)
                    break

        return {'visitados': vertices_visitados, 'posordem': lista_posordem}

    def busca_profundidade(self, vertice_inicial="nao_informado"):
        """
        Método para repetição da lógica de busca em profundidade até que
        todos os vértices do grafo tenham sido visitados. Recebe,
        opcionalmente, o vértice inicial. Retorna a árvore completa de
        vértices visitados.
        """
        if vertice_inicial == "nao_informado":
            vertice = self._vertices[0]
        else:
            vertice = vertice_inicial
        q_componentes = 0
        vertices_visitados = []
        lista_posordem = []
        q_vertices_visitados = 0

        while q_vertices_visitados < len(self._vertices):

            if q_componentes > 0:
                for v in self._vertices:
                    visitado = False
                    for arvore in vertices_visitados:
                        if arvore.localizar_nodo(v):
                            visitado = True
                            break
                    if not visitado:
                        vertice = v
                        break

            vertices_visitados.append(self._profundidade(vertice)['visitados'])
            lista_posordem += self._profundidade(vertice)['posordem']
            q_componentes += 1
            # soma-se a q_vertices_visitados a quantidade de vértices
            # presentes na árvore adicionada à lista!
            q_vertices_visitados += vertices_visitados[-1].quantidade

        return {'visitados': vertices_visitados,
                'q_componentes': q_componentes,
                'posordem': lista_posordem}

    def imprimir_busca_profundidade(self, vertice_inicial="nao_informado"):
        """
        Método para impreção da árvore de busca em profundidade,
        formatada para falicitar a leitura.
        """
        vertices_visitados = \
            self.busca_profundidade(vertice_inicial)['visitados']
        for i in range(len(vertices_visitados)):
            vertices_visitados[i].imprimir()

    def get_q_componentes_conexos(self):
        """
        Retorna a quantidade de componentes conexos no grafo.
        """
        q_conexos = self.busca_largura()['q_componentes']
        if self._digrafo:
            self._digrafo = False
            q_conexos = self.busca_largura()['q_componentes']
            self._digrafo = True
        return q_conexos

    def dijkstra(self, v_origem):
        """
        Implementação do algoritmo de djikstra. Recebe o vértice de
        origem e retorna listas de distância e 'path' para todos os
        vértices do grafo.
        """
        dist = [float('inf') for i in range(len(self._vertices))]
        path = ['-' for i in range(len(self._vertices))]
        s = [v_origem]
        not_s = deepcopy(self._vertices)
        not_s.remove(v_origem)
        dist[self._vertices.index(v_origem)] = 0

        v_atual = v_origem

        while not_s:
            _adj, _p = self._get_adjacentes_e_pesos(v_atual)
            adjacentes, pesos = [], []
            for idx, vertice in enumerate(_adj):
                if vertice in not_s:
                    adjacentes.append(_adj[idx])
                    pesos.append(_p[idx])

            for idx, vertice in enumerate(adjacentes):
                if dist[self._vertices.index(vertice)] > \
                        dist[self._vertices.index(v_atual)] + pesos[idx]:
                    dist[self._vertices.index(vertice)] = \
                        dist[self._vertices.index(v_atual)] + pesos[idx]
                    path[self._vertices.index(vertice)] = v_atual

            min_dist = float('inf')
            for vertice in not_s:
                if dist[self._vertices.index(vertice)] < min_dist:
                    min_dist = dist[self._vertices.index(vertice)]
                    v_atual = vertice

            s.append(v_atual)
            not_s.remove(v_atual)

        return dist, path

    def get_menor_caminho(self, v_origem, v_destino):
        """
        Utiliza o retorno do método djikstra para retornar o menor
        caminho completo entre dois vértices. Devem ser informados
        vértice de origem e vértice de destino.
        """
        path = self.dijkstra(v_origem)[1]
        caminho = [v_destino]
        v = v_destino
        while v != v_origem:
            v = path[self._vertices.index(v)]
            caminho.append(v)
        caminho = caminho[::-1]
        return caminho

    def _caminho_format(self, v_origem, v_destino):
        """
        Método privado que formata a saída do método get_menor_caminho.
        """
        caminho = self.get_menor_caminho(v_origem, v_destino)
        c_form = f"{Fore.YELLOW}{caminho[0]}{Fore.RESET} > "
        for vertice in caminho[1:-1:]:
            c_form += f"{vertice} > "
        c_form += f"{Fore.YELLOW}{caminho[-1]}{Fore.RESET}"
        return c_form

    def imprimir_menor_caminho(self, v_origem, v_destino="todos"):
        """
        Método utilizado para formatar e imprimir o resultado do
        algoritmo de dijskstra. Deve receber o vértice de origem e,
        opcionalmente, o vértice de destino. Se o vértice de destino
        for informado, será impresso o caminho entre os dois vértices e
        a distância entre eles. Caso não seja informado, será impressa
        uma tabela com essas informações para cada vértice do grafo.
        """
        dist, path = self.dijkstra(v_origem)

        if v_destino == "todos":
            x = PrettyTable([f"{Fore.BLUE}vertice{Fore.RESET}",
                             f"{Fore.BLUE}distância{Fore.RESET}",
                             f"{Fore.BLUE}caminho{Fore.RESET}"])
            x.align[f"{Fore.BLUE}caminho{Fore.RESET}"] = "l"

            x.add_row([f"{Fore.YELLOW}{v_origem}{Fore.RESET}",
                       f"{Fore.YELLOW}0{Fore.RESET}",
                       f"{Fore.YELLOW}-{Fore.RESET}"])
            for idx, vertice in enumerate(self._vertices):
                if vertice != v_origem:
                    x.add_row([f"{Fore.YELLOW}{self._vertices[idx]}"
                               f"{Fore.RESET}", dist[idx],
                               f"{self._caminho_format(v_origem, vertice)}"])

            print(x)
        else:
            print(self._caminho_format(v_origem, v_destino))
            print(f"Distância = {dist[self._vertices.index(v_destino)]}")

    def _inverter_arestas(self):
        """
        Método privado para inverter as arestas de um digrafo. Retorna
        uma copia do grafo com as arestas invertidas.
        """
        arestas_invertidas = []
        if self._valorado:
            for trio in self._arestas:
                i, j, p = trio.replace(" ", "").split("-")
                arestas_invertidas.append(f"{j}-{i}-{p}")
        else:
            for par in self._arestas:
                i, j = par.replace(" ", "").split("-")
                arestas_invertidas.append(f"{j}-{i}")
        grafo_invertido = Grafo(self._digrafo, self._valorado, self._vertices,
                                arestas_invertidas)
        return grafo_invertido

    def get_q_componente_fortemente_conexos(self):
        """
        Retorna a quantidade de componentes fortemente conexos no grafo.
        """
        posordem = self.busca_profundidade()['posordem']
        grafo_invertido = self._inverter_arestas()
        q_componentes = 0
        while posordem:
            explorados = \
                grafo_invertido._profundidade(posordem[-1])['posordem']
            for vertice in explorados:
                if vertice in posordem:
                    posordem.remove(vertice)
            q_componentes += 1
        return q_componentes

    def fortemente_conexo(self):
        """
        Método que retorna verdadeiro se o grafo for fortemente conexo
        ou falso se não for.
        """
        forte = True
        if self.get_q_componente_fortemente_conexos() > 1:
            forte = False
        return forte

    def _coloracao(self, cores_iniciais=None):
        """
        Método para colorir ao grafo. O resultado obtido é UMA das
        soluções possíveis, visto que não existe algoritmo ótimo para
        coloração.
        """
        if cores_iniciais is None:
            cores = [[]]
        else:
            cores = deepcopy(cores_iniciais)

        lista_vertices = deepcopy(self._vertices)
        for vertice in lista_vertices:
            for cor in cores:
                if vertice in cor:
                    lista_vertices.remove(vertice)
        shuffle(lista_vertices)

        for vertice in lista_vertices:
            ha_adjacente = False
            for idx, cor in enumerate(cores):
                ha_adjacente = False
                for adjacente in self.get_adjacentes(vertice):
                    if adjacente in cores[idx]:
                        ha_adjacente = True
                        break
                if not ha_adjacente:
                    cor.append(vertice)
                    break
            if ha_adjacente:
                cores.append([vertice])
        return cores

    def coloracao(self, cores_iniciais=None, limite=float("Inf")):
        """
        Método para aplicar a coloração ao grafo. Permite que o usuário
        informe cores iniciais ou um limite de cores (caso seja
        conhecido) e, caso não encontre uma solução dentro do limite
        da primeira vez, repete o algoritmo, embaralhando a ordem dos
        vértices até encontrá-la.
        """
        lista_cores = self._coloracao(cores_iniciais)
        while len(lista_cores) > limite:
            lista_cores = self._coloracao(cores_iniciais)
        return lista_cores

    def imprimir_coloracao(self, cores_iniciais=None, limite=float("Inf")):
        """
        Imprime a coloração do grafo, formatada para facilitar a
        leitura.
        """
        for idx, cor in enumerate(self.coloracao(cores_iniciais,
                                                 limite)):
            print(f"{Fore.YELLOW}COR {idx + 1}:{Fore.RESET} {cor}")

    def obter_grau_de_entrada(self, vertice_de_entrada):
        """
        Encontra o grau de entrada do vértice solicitado.
        """
        grau_entrada = 0
        for vertice in self._vertices:
            if vertice_de_entrada in self.get_adjacentes(vertice):
                grau_entrada += 1
        return grau_entrada

    def remover_do_grafo(self, vertice):
        """
        Método para remover uma aresta do grafo
        """
        self._vertices.remove(vertice)
        for aresta in self._arestas:
            if aresta.find(vertice) >= 0:
                self._arestas.remove(aresta)

    def ordenacao_topologica(self):
        """
        Ordena topologicamente os vértices do grafo.
        """
        vertices_backup = deepcopy(self._vertices)
        arestas_backup = deepcopy(self._arestas)
        lista_de_listas = []
        while self._vertices:
            graus_entrada_por_vertice = {}
            for vertice in self._vertices:
                graus_entrada_por_vertice[vertice] = \
                    self.obter_grau_de_entrada(vertice)
            lista_de_saida = []
            for vertice, grau_de_entrada in graus_entrada_por_vertice.items():
                if grau_de_entrada == 0:
                    lista_de_saida.append(vertice)
                    self.remover_do_grafo(vertice)
            lista_de_listas.append(lista_de_saida)
        self._vertices = vertices_backup
        self._arestas = arestas_backup
        return lista_de_listas

    def imprimir_ordenacao_topologica(self):
        """
        Imprime a ordenação topológica do grafo, formatada para
        facilitar a leitura
        """
        for idx, lista in enumerate(self.ordenacao_topologica()):
            print(f"{Fore.YELLOW}ETAPA {idx + 1}:{Fore.RESET} {lista}")

        print(f"\nPS.: A etapa corresponde aos elementos que estão aptos "
              f"para a utilização logo na primeira iteração. A etapa 2 "
              f"corresponde àqueles disponíveis, no mínimo, na segunda, "
              f"e assim por diânte...")
