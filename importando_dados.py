"""
Código disponibilizado pelo professor Adolfo Pinto
"""

# Import necessários para esta seção
import pandas as pd
idx = pd.IndexSlice

# Preparando o Dataset
links = pd.read_csv("dados/links.csv",  index_col=['movieId'])
movies = pd.read_csv("dados/movies.csv", sep=",", index_col=['movieId'])
ratings = pd.read_csv("dados/ratings.csv", index_col=['userId', 'movieId'])
tags = pd.read_csv("dados/tags.csv", index_col=['userId', 'movieId'])
