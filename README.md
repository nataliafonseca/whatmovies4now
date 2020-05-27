# What movies 4 now?
Implementação de um sistema de recomendação da disciplina Teoria dos Grafos ministrada pelo professor Adolfo Guimarães na Universidade Tiradentes - UNIT.
Desenvolvedores: Natália Braga da Fonseca  e Vinícius José Santana de Mendonça

## Instalação dos requisitos
Para a instalação dos requisitos do projeto através do promp de comando, navegue até a pasta do projeto e insira o seguinte comando:

```
pip install -r requirements.txt
```

## Inicialização do sistema
Para a  inicialização do sistema, execute o arquivo "whatmovies4now.py" na pasta raiz do projeto e clique na rota fornecida pelo sistema que o redirecionará para página inicial.
O sistema também pode ser acessado através do link: https://whatmovies4now.herokuapp.com/

## Sistema de recomendação por Collaborative Filtering
O sistema What movies 4 now? Utiliza técnicas de Collaborative Filtering, ou Filtragem Colaborativa, que exploram a ideia de que existem relações entre os produtos e os interesses das pessoas. Muitos sistemas de recomendação usam o Collaborative Filtering para entender essas relações e para dar uma precisa recomendação de um produto que o usuário pode gostar ou mesmo desfrutar.

Para isso filtragem colaborativa baseia esses relacionamentos nas escolhas que um usuário faz ao comprar, assistir, ou curtir alguma coisa. Em seguida, faz conexões com outros usuários de interesses semelhantes para produzir uma previsão.

## Back-end

## Front-end
O desenvolvimento do Front-end foi feito a partir do framework Flask, em python. Integrando o back-end com o front em HTML. Foi utilizado o Bootstrap v4.5.0 como framework para as bibliotecas de CSS.
O front-end foi dividido em duas rotas. A rota padrão que leva a página "index.html" onde  foi adicionado um jumbotron com um input e um button, onde o usuário deve inserir o "User ID" que deve ser um valor entre 1 a 610 (Valores da base de dados utilizada do movielens). Se o usuário informar qualquer outro dados não reconhecido, é emitido um alert configurado via JavaScript informando que o dado está incorreto, tratando possiveis erros.
A rota é uma rota dinâmica (/recommend/user_id) onde o "user_id" é o valor passado pelo usuário que irá compôr a rota final que levará até o arquivo "recommend.html". Este arquivo possui toda base de recomendação, onde possui um input group, com a mesma função do input button da página "index.html".
A página possui quatro conteiners sendo eles divididos em "filmes assistidos pelo usuário" e "filmes recomendados para o usuário" onde, ambos são integrados com o back-end, trazendo as informações de filmes assistidos e recomendações.
No final da página "recommend.html" possui um Footer com os nomes dos desenvolvedores e seus respectivos contatos (Linkedin e Github).

<b>Seguem imagens das páginas:</b>


<b>Index.html:</b>

![Index](https://imgur.com/zn0KSHZ)

<b>Recommend.html:</b>

![Recommend](https://imgur.com/hK8Fgpe)