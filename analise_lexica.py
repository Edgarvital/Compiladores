import pandas as pd

tabela_tokens = pd.DataFrame(columns=['Token', 'Lexema', 'linha']) #DataFrame que vai ser a tabela de tokens

caracteres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
              "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",]

caracteres_numericos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

caracteres_especiais = [";", "(", ")", "=", "\n", "{", "}", "!", ","]

operadores_booleano = ['==', ">=", "<=", "!=", ">", "<"]

operadores_aritmeticos = ['+', "-", "*", "/"]

condicionais = ["if", "else"]

desvio_incondicional = ['continue', "break"]

retorno = ['return']

impressao = ['print']

laco = ["while"]

tipo = ['int', 'boolean']

booleano = ['true', 'false']

def analise(codigo):
    global tabela_tokens

    for linha in codigo:
        palavras = linha.split()
        for palavra in palavras:
            if verificar_palavra_reservada(palavra) != False:
                token = verificar_palavra_reservada(palavra)
                inserir_token(token, palavra, tabela_tokens)



def verificar_palavra_reservada(palavra):
    if verificar_tipo(palavra):
        return 'tipo'


def verificar_tipo(palavra):
    if palavra in tipo:
        return True
    else:
        return False

def verificar_condicional(palavra):
    if palavra in condicionais:
        return True
    else:
        return False

def inserir_token(token, palavra, tabela_tokens, numero_linha=1):
    tabela_tokens.loc[len(tabela_tokens)] = [token, palavra, numero_linha]  # salva o lexema



