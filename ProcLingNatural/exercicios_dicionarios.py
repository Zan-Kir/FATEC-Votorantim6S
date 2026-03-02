chaves = ['Leon', 'Jill', 'Chris', 'Claire', 'Carlos']
valores = [24699, 13555, 15678, 22222, 33333]

dicionario = {}
for i in range(len(chaves)):
    dicionario[chaves[i]] = valores[i]
print(dicionario)

print(dicionario.keys())

print(dicionario.values())

print(dicionario.items())

print(list(dicionario.items())[1])

print(dicionario)

for k,v in dicionario.items(): 
    print(f'Chave: {k} - Valor: {v}')
