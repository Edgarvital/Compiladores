import analise_lexica
import analise_sintatica

#df.loc e df.iterrows funções importantes pra usar no dataframe

codigo = open('Codigo.txt', 'r')

lexica = analise_lexica.analise(codigo)
#print(lexica.to_string())

sintatica = analise_sintatica.analise(lexica)
print(sintatica)

