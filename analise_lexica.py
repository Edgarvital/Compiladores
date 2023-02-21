import numpy as np
import pandas as pd
import re

tabela_tokens = pd.DataFrame(columns=['Token', 'Lexema', 'linha'])  # DataFrame que vai ser a tabela de tokens

caracteres = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U",
              "V", "W", "X", "Y", "Z",
              "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
              "v", "w", "x", "y", "z", ]

caracteres_numericos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

caracteres_especiais = [";", "(", ")", "=", "{", "}", "!", ",", ' ']

dicionario_caracteres_especiais = {
    ';': 'ponto_virgula',
    '(': 'abre_parentese',
    ')': 'fecha_parentese',
    '=': 'operador_atribuicao',
    '{': 'abre_chave',
    '}': 'fecha_chave',
    '!': 'negacao',
    ',': 'virgula'
}

operadores_aritmeticos = ['+', "-", "*", "/"]

operadores_booleano = ['==', ">=", "<=", "!=", ">", "<"]

operadores = np.concatenate((operadores_booleano, operadores_aritmeticos))

condicionais = ["if", "else"]

desvio_incondicional = ['continue', "break"]

retorno = ['return']

impressao = ['print']

laco = ["while"]

tipo = ['int', 'boolean']

booleano = ['true', 'false']

procedimento = ['procedimento']

funcao = ['funcao']


def analise(codigo):
    global tabela_tokens
    for numero_linha, linha in enumerate(codigo):

        padrao = r'(' + '|'.join([re.escape(c) for c in caracteres_especiais]) + ')'
        palavras = [x for x in re.split(padrao, linha) if x if " " not in x if "\n" not in x]

        for palavra in palavras:
            token = verificar_palavra(palavra)
            if token != False and token != 'Error':
                inserir_token(token, palavra, tabela_tokens, (numero_linha + 1))
            else:
                print('Erro Léxico, numero da linha: ' + str(numero_linha + 1) + ' lexema: ' + palavra)
                exit()
    print(tabela_tokens.to_string())
    exit()


def verificar_palavra(palavra):
    if verificar_tipo(palavra):
        return 'tipo'
    elif verificar_condicional(palavra):
        return 'condicional'
    elif verificar_desvio_incondicional(palavra):
        return 'desvio_incondicional'
    elif verificar_laco(palavra):
        return 'laco'
    elif verificar_booleano(palavra):
        return 'booleano'
    elif verificar_impressao(palavra):
        return 'impressao'
    elif verificar_retorno(palavra):
        return 'retorno'
    elif verificar_operador_booleano(palavra):
        return 'operador_booleano'
    elif verificar_caracter_numerico(palavra):
        return 'numerico'
    elif verificar_procedimento(palavra):
        return 'procedimento'
    elif verificar_funcao(palavra):
        return 'funcao'
    elif verificar_identificador(palavra) is not False:
        return verificar_identificador(palavra)
    elif verificar_operador_aritmetico(palavra):
        return 'operador_aritmetico'
    elif verificar_caracter_especial(palavra) is not False:
        return verificar_caracter_especial(palavra)

    else:
        return False


def inserir_token(token, palavra, tabela_tokens, numero_linha):
    tabela_tokens.loc[len(tabela_tokens)] = [token, palavra, numero_linha]

def verificar_caracter_especial(palavra):
    token = dicionario_caracteres_especiais[palavra]
    if token is not None:
        return token
    else:
        return False

def verificar_operador_aritmetico(palavra):
    if palavra in operadores_aritmeticos:
        return True
    else:
        return False

def verificar_identificador(palavra):
    primeiro_caracter = palavra[0]
    if (len(palavra) > 1):
        if (primeiro_caracter in caracteres_numericos):
            return 'Error'
    else:
        if (palavra in caracteres_especiais) or (palavra in operadores):
            return False

    for caracter in palavra:
        if (verificar_caracter_valido(caracter)):
            continue
        else:
            return 'Error'
    return 'identificador'

def verificar_caracter_numerico(palavra):
    if palavra in caracteres_numericos:
        return True
    else:
        return False

def verificar_caracter_valido(caracter):
    if (
            caracter in caracteres or caracter in caracteres_numericos or caracter in caracteres_especiais or caracter in operadores):
        return True
    else:
        return False

def verificar_procedimento(palavra):
    if palavra in procedimento:
        return True
    else:
        return False

def verificar_funcao(palavra):
    if palavra in funcao:
        return True
    else:
        return False

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


def verificar_desvio_incondicional(palavra):
    if palavra in desvio_incondicional:
        return True
    else:
        return False


def verificar_laco(palavra):
    if palavra in laco:
        return True
    else:
        return False


def verificar_booleano(palavra):
    if palavra in booleano:
        return True
    else:
        return False


def verificar_impressao(palavra):
    if palavra in impressao:
        return True
    else:
        return False


def verificar_retorno(palavra):
    if palavra in retorno:
        return True
    else:
        return False


def verificar_operador_booleano(palavra):
    if palavra in operadores_booleano:
        return True
    else:
        return False
