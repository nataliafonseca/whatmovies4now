from colorama import Fore, init as color


color()


def leiaint(msg):
    while True:
        try:
            n = int(input(msg))
        except (ValueError, TypeError):
            print(Fore.RED + "ERRO: por favor, digite um número inteiro"
                  + Fore.RESET)
        except KeyboardInterrupt:
            print(Fore.RED + "Usuário preferiu não digitar esse número" +
                  Fore.RESET)
            return 0
        else:
            return n


def linha(tam=50):
    return "-" * tam


def cabecalho(txt):
    print(linha())
    print(txt)
    print(linha())


def menu(lista):
    cabecalho("MENU PRINCIPAL")
    for i, item in enumerate(lista):
        print(Fore.YELLOW + f"{i + 1} - " + Fore.BLUE + f"{item}" + Fore.RESET)
    print(linha())
    opc = leiaint("Sua opção: ")
    return opc


def teste_grafo_definido(grafo):
    from grafo import Grafo
    grafo_exemplo = Grafo(False, False, ["A", "B", "C", "D", "E", "F", "G",
                                         "H", "I", "J", "K", "L"],
                          ["A-B", "A-C", "B-C", "B-E", "B-F", "C-D", "C-F",
                           "D-G", "E-F", "E-J", "E-I", "F-G", "F-K", "G-H",
                           "G-L", "H-L"])
    grafo_exemplo._id_grafo = 'simples'
    if not grafo:
        print(Fore.RED + "ATENÇÃO! Você ainda não definiu um grafo, "
                         "serão impressas as informações correspondentes "
                         "ao grafo representado em 'exemplo/simples.png'. "
                         "Para adicionar seu proprio grafo, selecione a "
                         "opção 1."
              + Fore.RESET)
        print()
        return grafo_exemplo, False
    return grafo, True
