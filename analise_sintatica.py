import pandas as pd

#Variaveis Globais
abreParenteseCount = 0
fechaParenteseCount = 0
abreChaveCount = 0
fechaChaveCount = 0

def analise(tabela):
    global tokens, lexemas, numLinhas, tokens_lines
    tokens = (tabela[tabela.columns[0:1:]]).values
    lexemas = (tabela[tabela.columns[1:2:]]).values
    numLinhas = (tabela[tabela.columns[2:3:]]).values
    tokens_lines = create_line_tokens()
    verificar_quantidade()
    verificar_ponto_virgula(tokens_lines)

    #assinatura_procedimento_funcao('funcao',9)
    #exit()

    loop_verificacao()

def loop_verificacao():
    for index, token in enumerate(tokens):
        assinatura_if(token, numLinhas[index, 0])


def print_error(mensagem, linha=None):
    if linha != None:
        print("Erro de Sintaxe:", mensagem, 'Linha:', linha)
    else:
        print("Erro de Sintaxe:", mensagem)
    exit()

def get_line_tokens(linha):
    try:
        return tokens_lines[linha]
    except Exception as e:
        print('linha vazia ou não encontrada')

def verificar_expressao(lista_tokens, linha):
    expressao = []
    while (lista_tokens[-1] != 'abre_parentese'):
        try:
            expressao.append(lista_tokens.pop())
        except Exception as e:
            print_error('Erro na expressão', linha)
            exit()


    if expressao.pop() in ['booleano', 'numerico', 'identificador']:
        if expressao.pop() == 'operador_booleano':
            if len(expressao) == 1 and expressao[0] in ['booleano', 'numerico', 'identificador']:
                return True
    return False


def assinatura_if(token, linha):
    if (token == 'condicional'):
        lista_tokens_linha = get_line_tokens(linha)
        if lista_tokens_linha.pop() == 'abre_chave':
            if lista_tokens_linha.pop() == 'fecha_parentese':
                if verificar_expressao(lista_tokens_linha, linha):
                    if lista_tokens_linha.pop() == 'abre_parentese':
                        if len(lista_tokens_linha) == 1 and lista_tokens_linha[0] == 'condicional':
                            return True
        print_error('Erro na assinatura do IF', linha)

def create_line_tokens():
    lista_tokens = {}
    tokens_line = []
    linha_aux = [1]
    last_position = -1
    for index, linha in enumerate(numLinhas):
        if (linha_aux == linha):
            tokens_line.append(tokens[index, 0])
        else:
            lista_tokens[linha_aux[0]] = tokens_line
            linha_aux = linha
            tokens_line = []
            tokens_line.append(tokens[index, 0])

    lista_tokens[numLinhas[last_position, 0]] = [tokens_line[last_position]]
    return lista_tokens

def verificar_quantidade():
    global abreParenteseCount, fechaParenteseCount, abreChaveCount, fechaChaveCount
    for token in tokens:
        verificar_parentese(token)
        verificar_chave(token)

    if abreParenteseCount != fechaParenteseCount:
        print_error('A quantidade de abre parentese é diferente da de fecha parentese')
    elif abreChaveCount != fechaChaveCount:
        print_error('A quantidade de abre chave é diferente da de fecha chave')

def verificar_parentese(token):
    global abreParenteseCount, fechaParenteseCount
    if token == 'abre_parentese':
        abreParenteseCount += 1
    elif token == 'fecha_parentese':
        fechaParenteseCount += 1

def verificar_chave(token):
    global abreChaveCount, fechaChaveCount
    if token == 'abre_chave':
        abreChaveCount += 1
    elif token == 'fecha_chave':
        fechaChaveCount += 1


# Verificando se o ultimo token de cada linha é um token ponto_virgula, caso não seja, deve de forma obrigatória se iniciar a linha com [if,while,procedimento,funcao]
def verificar_ponto_virgula(tokens_lines):
    #Guardando os tokens que serão válidos para casos onde não se finaliza a linha com ponto_virgula
    tokens_validos_inicio = ['condicional','funcao','procedimento','laco']

    for chave, valor in tokens_lines.items():
        if valor[-1] != 'ponto_virgula':
            if (valor[0] not in tokens_validos_inicio) and (valor[0] != 'fecha_chave' and valor[-1] != 'fecha_chave' and len(valor) != 1 ) :
                print_error('Finalização de expressão incorreta.',chave)
                exit()


def assinatura_procedimento_funcao(token,linha):
    #Verificaçã do primeiro token, para saber se corresponde ao padrão dado a função/procedimento
    if (token == 'procedimento') or (token == 'funcao'):

        #Recuperação da linha, após verificação de existencia da funcao/procedimento
        lista_tokens_linha = get_line_tokens(linha)

        #Verificação se possui um identificador para essa função/procedimento
        if lista_tokens_linha[1] != 'identificador':
            print_error('Incorreta a assinatura da funcao/procedimento.', linha)
            exit()

        #Verificação do conteudo presente entre o '(' (abre_parentese) e ')' (fecha_parentese)
        if (lista_tokens_linha[2] != 'abre_parentese') and (lista_tokens_linha[-2] != 'fecha_parentese'):
            print_error('Incorreta a assinatura da funcao/procedimento.', linha)
            exit()

        #Utilização de função auxiliar os argumentos presentes na função/procedimento
        verificao_argumento_procedimento_funcao(lista_tokens_linha[3:-2],linha)

  
def verificao_argumento_procedimento_funcao(argumentos,linha):
    #Separação dos argumentos, separando a lista em sub-listas a partir do token 'virgula'
    lista_tokens = []
    sublista = []
    for token in argumentos:
        if token == 'virgula':
            lista_tokens.append(sublista)
            sublista = []
        else:
            sublista.append(token)

    lista_tokens.append(sublista)

    #Verificando se é respeitada a padronização de tokens na passagem dos argumentos
    for intervalo_tokens in lista_tokens:
        if len(intervalo_tokens) == 2:
            if intervalo_tokens[0] != 'tipo' or intervalo_tokens[1] != 'identificador':
                print_error('Incorreta a passagem dos argumentos.', linha)
                exit()
        else:
            print_error('Incorreta a passagem dos argumentos.', linha)
            exit()



