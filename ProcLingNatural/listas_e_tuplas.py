# Lista são mutáveis, ou seja, é possível alterar seus valores
x = [0,1,2]
x[0] = 5

# Tupla são imutáveis, ou seja, não é possível alterar seus valores
y = ('Fundamental','Médio','Superior')
# y[0] = 5
# erro não é possível alterar um valor de uma tupla, pois ela é imutável

# Alguns métodos de listas
l = list(range(5)) # gera uma lista com os números de 0 a 4
print(l)
l.append(10) # adiciona o valor 10 ao final da lista
print(l)
l.insert(0,5) # insere o valor 5 na posição 0 da lista
print(l)
l.reverse() # inverte a ordem dos elementos da lista
print(l)
l.sort() # ordena alfabeticamente ou numericamente os elementos da lista
print(l)
l.remove(1) # remove o valor 1 da lista
print(l)
l.index(5) # retorna o índice do valor 5 na lista
print(l.index(5))
l.count(10) # conta quantas vezes o valor 10 aparece na lista
print(l.count(10))

# Slicing de listas
# o slice pega um pedaço da lista, ou seja, uma sublista, e é definido por [início:fim:passo]
l = list(range(10))
print(l)
print(l[2:5]) # imprime os elementos de índice 2 a 4
print(l[:5]) # imprime os elementos de índice 0 a 4
print(l[5:]) # imprime os elementos de índice 5 até o final
print(l[::2]) # imprime os elementos de índice par
print(l[::-1]) # imprime os elementos na ordem inversa

# Alguns métodos de tuplas
meses = ('Janeiro','Fevereiro','Março')
# meses.append('Abril') # erro não é possível adicionar um valor a uma tupla, pois ela é imutável
meses.index('Janeiro') # retorna o índice do valor 'Janeiro'
print(meses.index('Janeiro'))
meses.count('Janeiro') # conta quantas vezes o valor 'Janeiro' aparece na tupla
print(meses.count('Janeiro'))
print(meses[0]) # imprime o elemento de índice 0 da tupla