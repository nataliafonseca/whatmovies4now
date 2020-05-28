# What movies 4 now?
Implementação de um sistema de recomendação da disciplina Teoria dos Grafos ministrada pelo professor Adolfo Guimarães na Universidade Tiradentes - UNIT.
Desenvolvedores: Natália Braga da Fonseca e Vinícius José Santana de Mendonça

## Instalação dos requisitos
Para a instalação dos requisitos do projeto através do promp de comando, navegue até a pasta do projeto e insira o seguinte comando:

```
pip install -r requirements.txt
```

## Inicialização do sistema
Para a inicialização da interface do sistema, execute o arquivo "whatmovies4now.py" na pasta raiz do projeto e, uma vez iniciado o servidor, faça o acesso pelo endereço `127.0.0.1:5000`, que o levará para página inicial.
O sistema também pode ser acessado através do link: https://whatmovies4now.herokuapp.com/
Se preferir executar o sistema pelo console, execute o arquivo "console.py".

## Sistema de recomendação por Collaborative Filtering
O sistema What movies 4 now? Utiliza técnicas de Collaborative Filtering, ou Filtragem Colaborativa, que exploram a ideia de que existem relações entre os produtos e os interesses das pessoas. Muitos sistemas de recomendação usam o Collaborative Filtering para entender essas relações e para dar uma precisa recomendação de um produto que o usuário pode gostar ou mesmo desfrutar.

Para isso filtragem colaborativa baseia esses relacionamentos nas escolhas que um usuário faz ao comprar, assistir, ou curtir alguma coisa. Em seguida, faz conexões com outros usuários de interesses semelhantes para produzir uma previsão.

## Back-end
O back-end do trabalho foi desenvolvido em Python. De início, foi utilizada a biblioteca Pandas para importar o dataset "Small" de usuários e filmes do site "movielens.org". Uma vez importados, foram utilizadas as noções de filtragem colaborativa e métodos da biblioteca NumPy para calcular a similaridade entre os usuários.
A partir desse calculo, foi gerado um grafo cujos vértices representam cada usuário e as arestas conectam aqueles que tem grande similaridade. 
Para definir as recomendações, é realizada uma busca em largura neste grafo, a partir do usuário raiz, e são consideradas as 3 camadas de usuários mais próximos a ele. Uma camada por vez, é feita uma média das notas dos filmes avaliados pelos usuários similares, excluem-se aqueles com menos de 50 votos no total ou menos de 1/4 dos votos entre os usuários da camada, além dos filmes já vistos pelo usuário.
Então, são recomendados 5 filmes a partir das médias da primeira camada, 3 filmes a partir das médias da segunda e 2 filmes correspondentes à terceira.

## Front-end
O desenvolvimento do Front-end foi feito a partir do framework Flask, em python. Integrando o back-end com o front em HTML. Foi utilizado o Bootstrap v4.5.0 como framework para as bibliotecas de CSS.
O front-end foi dividido em duas rotas. A rota padrão que leva a página "index.html" onde  foi adicionado um jumbotron com um input e um button, onde o usuário deve inserir o "User ID" que deve ser um valor entre 1 a 610 (Valores da base de dados utilizada do movielens). Se o usuário informar qualquer outro dados não reconhecido, é emitido um alert configurado via JavaScript informando que o dado está incorreto, tratando possiveis erros.
A rota é uma rota dinâmica (/recommend/user_id) onde o "user_id" é o valor passado pelo usuário que irá compôr a rota final que levará até o arquivo "recommend.html". Este arquivo possui toda base de recomendação, onde possui um input group, com a mesma função do input button da página "index.html".
A página possui quatro conteiners sendo eles divididos em "filmes assistidos pelo usuário" e "filmes recomendados para o usuário" onde ambos são integrados com o back-end, trazendo as informações de filmes assistidos e recomendações.
No final da página "recommend.html" há um Footer com os nomes dos desenvolvedores e seus respectivos contatos (Linkedin e Github).

<b>Seguem imagens das páginas:</b>


<b>Index.html:</b>

![Index](https://i.imgur.com/zn0KSHZ.jpg)


<b>Recommend.html:</b>

![Recommend](https://i.imgur.com/hK8Fgpe.jpg)
