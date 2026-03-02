x = [1,2,3]
y = ['a','b','c']

dict = {}
dict['a'] = 1
dict['b'] = 2

print(dict)

dict['Joao'] = 123456

print(dict.keys()) #verifica as chaves do dicionário
print(dict.values()) #verifica os valores do dicionário

for k,v in dict.items(): #percorre o dicionário e imprime as chaves e os valores
    print(f'Chave: {k} - Valor: {v}')
    
print(list(dict.items())) #converte o dicionário em uma lista de tuplas, onde cada tupla é um par chave-valor do dicionário