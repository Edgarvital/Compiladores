import analise_lexica
import analise_sintatica
import analise_semantica

codigo = open('Codigo.txt', 'r')

tabela_lexica = analise_lexica.analise(codigo)

#print(tabela_lexica)


tabela_sintatica = analise_sintatica.analise(tabela_lexica)

print(tabela_sintatica.to_string())


semantico = analise_semantica.analise(tabela_lexica, tabela_sintatica)

#print(semantico)


