import anytree


class Arvore:
    def __init__(self, conteudo):
        self.raiz = anytree.Node(conteudo)
        self.nodos = []
        self.quantidade = 1

    def imprimir(self):
        for pre, fill, node in anytree.RenderTree(self.raiz):
            print("%s%s" % (pre, node.name))

    def localizar_nodo(self, conteudo):
        return anytree.search.find_by_attr(self.raiz, value=conteudo)

    def inserir_nodo(self, pai, filho):
        self.nodos.append(anytree.Node(filho, self.localizar_nodo(pai)))
        self.quantidade += 1
