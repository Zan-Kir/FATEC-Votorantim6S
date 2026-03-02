infile = open('exemplo.txt','r')
conteudo = infile.read()
lista = infile.readlines()
infile.close()
print(conteudo)
print(lista)

outfile = open('exemplo.txt','w')
outfile.write('Exemplo')

outfile.close()

outfile_append = open('exemplo.txt','a')
outfile_append.write('\nExemplo 2')
outfile_append.close()