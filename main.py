import analise_lexica
import analise_sintatica
import analise_semantica
import gerador_codigo_intermediario

codigo = open('Codigo.txt', 'r')

tabela_lexica = analise_lexica.analise(codigo)

print(tabela_lexica.to_string())


tabela_sintatica = analise_sintatica.analise(tabela_lexica)

#print(tabela_sintatica.to_string())


semantico = analise_semantica.analise(tabela_lexica, tabela_sintatica[0])

gerador_codigo_intermediario.gerar(tabela_lexica, tabela_sintatica[0], tabela_sintatica[1])


