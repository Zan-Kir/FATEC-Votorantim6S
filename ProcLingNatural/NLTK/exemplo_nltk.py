import nltk

# nltk.download()
print('Python NLTK', nltk.__version__)

texto = 'Era uma vez, em um vale encantado, 7 anões... 😍😍'
# O token é a menor unidade de um texto, ou seja, uma palavra, um número, um símbolo, etc.
# Podemos configurar o tokenizador para considerar ou não os símbolos, por exemplo, ou para separar as palavras de acordo com a pontuação.

### Exemplo de tokenização ###
print(nltk.word_tokenize(texto))

from nltk.tokenize import RegexpTokenizer
# O RegexpTokenizer é um tokenizador que utiliza expressões regulares para definir os tokens. 
# No exemplo abaixo, estamos utilizando a expressão regular \w+ para definir os tokens como palavras, ou seja, sequências de caracteres alfanuméricos. Isso significa que os símbolos de pontuação e os emojis serão ignorados na tokenização.
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(texto)
print(f'tokens sem simbolos = {tokens}')
# Também podemos usar o regex para remover números, por exemplo, usando a expressão regular \D+ para definir os tokens como sequências de caracteres que não são dígitos. Ou só considerar A-z
tokenizer = RegexpTokenizer(r'[A-z]\w*')
tokens = tokenizer.tokenize(texto)
print(f'tokens sem simbolos e numeros = {tokens}')

### Corpus ###
nltk.download('gutenberg')
from nltk.corpus import gutenberg
# O corpus é um conjunto de textos que pode ser utilizado para treinamento e teste de modelos de processamento de linguagem natural. O NLTK possui diversos corpora disponíveis, como o Gutenberg, que contém uma coleção de livros clássicos em inglês.

# print(gutenberg.fileids())

# Quando vamos trabalhar com um corpus, podemos acessar os textos e as palavras de cada texto. No exemplo abaixo, estamos acessando as palavras do texto "Emma" de Jane Austen, que está disponível no corpus Gutenberg.
# O método words() retorna uma lista de palavras presentes no texto, incluindo pontuação e símbolos.
palavras = gutenberg.words('austen-emma.txt')
print(f'Algumas palavras do corpus: {palavras[:20]}')

# Podemos também tokenizar frases do corpus utilizando o método sents que retorna uma lista de frases, onde cada frase é uma lista de palavras. No exemplo abaixo, estamos acessando as frases do texto "Emma" e imprimindo as primeiras 3 frases.
frases = gutenberg.sents('austen-emma.txt')
print(f'Algumas frases do corpus: {frases[:3]}')

# Por fim, podemos acessar o texto completo do corpus utilizando o método raw(), que retorna uma string com todo o conteúdo do texto. No exemplo abaixo, estamos acessando o texto completo de "Emma" e imprimindo os primeiros 500 caracteres.
texto = gutenberg.raw('austen-emma.txt')
tokens = nltk.word_tokenize(texto[:500])
print(f'Alguns caracteres do texto completo: {tokens}')

### Frequência - Contagem de Tokens ###
# A frequência é uma medida que indica quantas vezes um token aparece em um texto ou corpus. O NLTK possui a classe FreqDist, que é utilizada para calcular a frequência dos tokens.
# No exemplo abaixo, estamos utilizando o método FreqDist para calcular a frequência dos tokens do texto completo de "Emma" e imprimindo os 10 tokens mais comuns.
frequencia = nltk.FreqDist(tokens)
print(f'Frequência dos tokens: {frequencia.most_common(10)}')

# Tokens com letra maiúscula e minúscula são considerados diferentes, por isso, por exemplo, "Emma" e "emma" são contados como tokens distintos. Para evitar isso, podemos converter todos os tokens para minúsculas antes de calcular a frequência.
tokens = [token.lower() for token in tokens]
frequencia = nltk.FreqDist(tokens)
print(f'Frequência dos tokens (sem distinção de maiúsculas e minúsculas): {frequencia.most_common(10)}')

### Stopwords ###
# As stopwords são palavras que são consideradas irrelevantes para a análise de texto, como
# artigos, preposições, conjunções, etc. O NLTK possui uma lista de stopwords em diversos idiomas, incluindo o português.
stopwords = nltk.corpus.stopwords.words('english')
# No exemplo abaixo, estamos utilizando a lista de stopwords em português para remover as stopwords do texto completo de "Emma". O método stopwords.words() retorna uma lista de stopwords para o idioma especificado.
print(f'Stopwords em inglês: {stopwords}')
# Frequencia dos tokens sem stopwords
texto = 'Era uma vez, em um vale encantado, 7 anões, e uma princesa, quem será o príncipe? 😍😍'
tokenizer = RegexpTokenizer(r'[A-z]\w*')
tokens = tokenizer.tokenize(texto)
stopwords = nltk.corpus.stopwords.words('portuguese')
tokens_sem_stopwords = [word.lower() for word in tokens if word.lower() not in stopwords]
frequencia = nltk.FreqDist(tokens_sem_stopwords)
print(f'Frequência dos tokens sem stopwords: {frequencia.most_common(10)}')

# 10 Palavras mais comuns sem stopwords
from nltk.corpus import gutenberg
from nltk.probability import FreqDist

nltk.download('gutenberg')
# Outro exemplo porem sem usar o regex para tokenizar as palavras, apenas usando o método words() do corpus Gutenberg.
# O método words() retorna uma lista de palavras presentes no texto, incluindo pontuação e símbolos, por isso, estamos utilizando a expressão isalpha() para filtrar apenas as palavras alfabéticas e convertendo todas as palavras para minúsculas antes de calcular a frequência.
palavras = [palavra.lower() for palavra in gutenberg.words('austen-emma.txt') if palavra.isalpha()]
frequencia = FreqDist(palavras)
print(f'10 palavras mais comuns: {frequencia.most_common(10)}')

### N-grams ###
# unigramas são tokens individuais, bigramas são pares de tokens consecutivos, trigramas são trios de tokens consecutivos, e assim por diante. Ex. Eu/gosto/de/python
# bigramas são pares de tokens consecutivos em um texto. Eles são úteis para capturar relações entre palavras que ocorrem juntas com frequência, como expressões idiomáticas ou colaborações frequentes entre palavras. Ex. "eu gosto, "gosto de", "de python", etc.
# trigramas são trios de tokens consecutivos em um texto. Ex. "eu gosto de", "gosto de python", etc.
# n-gramas são sequências de n tokens consecutivos em um texto. O NLTK possui a função ngrams() para gerar n-gramas a partir de uma lista de tokens.

from nltk import bigrams, trigrams, ngrams
texto = gutenberg.raw('austen-emma.txt')
tokens = nltk.word_tokenize(texto)
lista = list(bigrams(tokens))
print(f'Alguns bigramas: {lista}')

### Stemming e Lemmatization ###
# Stemming - reduzir a palavra ao radical (formas flexionadas para a forma base) #
# Ex. "amigo, amigos, amiga, amigão, etc." -> "amig" 
# "estudando, estudou, estudo, etc." -> "estud"
# "propoer, propôs, propondo, etc." -> "prop"
# O Stemming é uma técnica de processamento de linguagem natural que tem como objetivo reduzir as palavras ao seu radical, ou seja, à sua forma base. O objetivo do stemming é agrupar palavras que têm a mesma raiz, mas que podem ter formas flexionadas diferentes, para que elas sejam tratadas como a mesma palavra em análises de texto. 
# O stemming é mais simples e rápida do que a lemmatization, mas pode resultar em palavras que não são reconhecíveis como palavras reais, como "amig" em vez de "amigo". 
# RSLP - removedor de sufixos para a língua portuguesa, é um algoritmo de stemming específico para o português, que utiliza regras para remover sufixos das palavras. O NLTK possui o RSLPStemmer, que é um stemmer baseado no algoritmo RSLP.

# Lemmatization - reduzir a palavra à sua forma canônica (lemmas), considera-se a classe gramatical #
# Ex. "amigo, amigos, amiga, amigão, etc." -> "amigo"
# "estudando, estudou, estudo, etc." -> "estudar"
# "propoer, propôs, propondo, etc." -> "propor"
# A lemmatization é uma técnica de processamento de linguagem natural que tem como objetivo reduzir as palavras à sua forma canônica, ou seja, ao seu lema. O lema é a forma base de uma palavra, que pode ser encontrada em um dicionário.
# A lemmatization leva em consideração a classe gramatical da palavra, o que significa que ela pode diferenciar entre palavras com a mesma raiz, mas com significados diferentes, como "amigo" e "amiga".
# O NLTK nao tem uma biblioteca de lemmatization para o português. 
# O pos é um parâmetro no lemmatize que indica a classe gramatical. 
# Exemplos de uso do pos:
# pos="n" - substantivo
# pos="v" - verbo
# pos="a" - adjetivo
# pos="r" - advérbio

stemmer = nltk.stem.RSLPStemmer()
print (f'Stemming: {stemmer.stem("amigos")}')

lemmatizer = nltk.stem.WordNetLemmatizer()
print (f'Lemmatization: {lemmatizer.lemmatize("studying", pos="v")}') # pos="v" indica que a palavra é um verbo, o que é importante para a lemmatization, pois ela leva em consideração a classe gramatical da palavra.

### Etiquetadores - pos tagging ###
# O pos tagging é a tarefa de atribuir uma etiqueta gramatical a cada palavra em um texto, como substantivo, verbo, adjetivo, etc.
# Exemplos de etiquetas gramaticais:
# NN - substantivo comum
# VB - verbo
# JJ - adjetivo
# O gato preto correu de medo

# nltk.pos_tag() # etiquetador de palavras em inglês
# floresta e mac morpho

from nltk.corpus import mac_morpho
from nltk.tag import UnigramTagger

# tokens = nltk.word_tokenize()
print(mac_morpho.tagged_sents()[0]) # O método tagged_sents() retorna uma lista de sentenças, onde cada sentença é uma lista de tuplas, onde cada tupla contém uma palavra e sua respectiva etiqueta gramatical. No exemplo abaixo, estamos imprimindo a primeira sentença do corpus mac_morpho, que é um corpus de português anotado com etiquetas gramaticais.