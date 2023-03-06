import pandas as pd


def analise(tabela):
    global tokens, lexemas, numLinhas, tokens_lines
    tokens = (tabela[tabela.columns[0:1:]]).values
    lexemas = (tabela[tabela.columns[1:2:]]).values
    numLinhas = (tabela[tabela.columns[2:3:]]).values
    tokens_lines = create_line_tokens()

    verificar_quantidade(tokens_lines)
    verificar_ponto_virgula(tokens_lines)

    loop_verificacao()
    print('Analise sintática finalizada, sem erros.')

def loop_verificacao():
    for index, token in enumerate(tokens):
        assinatura_if(token, numLinhas[index, 0])
        verificar_atribuicao(token, numLinhas[index, 0])
        assinatura_while(token, numLinhas[index, 0])


def print_error(mensagem, linha=None):
    if linha != None:
        print("Erro de Sintaxe:", mensagem, 'Linha:', linha)
    else:
        print("Erro de Sintaxe:", mensagem)
    exit()


def get_line_tokens(linha):
    try:
        return tokens_lines[linha].copy()
    except Exception as e:
        print('linha vazia ou não encontrada')


def verificar_atribuicao_expressao(lista_tokens, linha):
    if lista_tokens.pop() == 'ponto_virgula':
        expressao = []
        while (lista_tokens[-1] != 'operador_atribuicao'):
            try:
                expressao.append(lista_tokens.pop())
            except Exception as e:
                print_error('Erro na expressão', linha)
        if len(expressao) == 1 and expressao.pop() in ['booleano', 'numerico', 'identificador']:
            return True
        elif expressao.pop() in ['numerico', 'identificador']:
            if expressao.pop() == 'operador_aritmetico':
                if len(expressao) == 1 and expressao[0] in ['numerico', 'identificador']:
                    return True
        return False


def verificar_atribuicao_funcao(lista_tokens, linha):
    virgula = True
    if lista_tokens.pop() == 'ponto_virgula':
        if lista_tokens.pop() == 'fecha_parentese':
            if lista_tokens.pop() in ['identificador', 'numerico']:

                while (lista_tokens[-1] != 'abre_parentese'):
                    token_vez = lista_tokens.pop()
                    try:
                        if token_vez == 'virgula' and virgula:
                            virgula = False
                        elif token_vez in ['identificador', 'numerico'] and virgula == False:
                            virgula = True
                        else:
                            return False

                    except Exception as e:
                        print_error('Erro na expressão', linha)
                if lista_tokens.pop() == 'abre_parentese':
                    if lista_tokens.pop() == 'identificador':
                        return True
    return False


def verificar_atribuicao(token, linha):
    if (token == 'operador_atribuicao'):
        lista_tokens_linha = get_line_tokens(linha)
        if verificar_atribuicao_expressao(lista_tokens_linha, linha):
            if lista_tokens_linha.pop() == 'operador_atribuicao':
                if lista_tokens_linha.pop() == 'identificador':
                    if lista_tokens_linha.pop() == 'tipo':
                        return True
        else:
            lista_tokens_linha = get_line_tokens(linha)
            if verificar_atribuicao_funcao(lista_tokens_linha, linha):
                if lista_tokens_linha.pop() == 'operador_atribuicao':
                    if lista_tokens_linha.pop() == 'identificador':
                        if lista_tokens_linha.pop() == 'tipo':
                            return True
        print_error('Erro na atribuicao', linha)


def verificar_expressao_booleana(lista_tokens, linha):
    expressao = []
    while (lista_tokens[-1] != 'abre_parentese'):
        try:
            expressao.append(lista_tokens.pop())
        except Exception as e:
            print_error('Erro na expressão', linha)

    if expressao.pop() in ['booleano', 'numerico', 'identificador']:
        if expressao.pop() == 'operador_booleano':
            if len(expressao) == 1 and expressao[0] in ['booleano', 'numerico', 'identificador']:
                return True
    return False

def assinatura_while(token, linha):
    if (token == 'laco'):
        lista_tokens_linha = get_line_tokens(linha)
        if lista_tokens_linha.pop() == 'abre_chave':
            if lista_tokens_linha.pop() == 'fecha_parentese':
                if verificar_expressao_booleana(lista_tokens_linha, linha):
                    if lista_tokens_linha.pop() == 'abre_parentese':
                        if len(lista_tokens_linha) == 1 and lista_tokens_linha[0] == 'laco':
                            return True
        print_error('Erro na assinatura do While', linha)

def assinatura_if(token, linha):
    if (token == 'condicional'):
        lista_tokens_linha = get_line_tokens(linha)
        if lista_tokens_linha.pop() == 'abre_chave':
            if lista_tokens_linha.pop() == 'fecha_parentese':
                if verificar_expressao_booleana(lista_tokens_linha, linha):
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


def verificar_chave(tokens_lines):
    # Guardando os tokens que serão válidos
    tokens_validos_inicio = ['condicional', 'funcao', 'procedimento', 'laco']
    # Pilha auxiliar para contagem de chaves
    chaveCount = []

    for chave, valor in tokens_lines.items():
        if valor[-1] == 'abre_chave':
            # Verificando se a abertura de chave está sendo utilizada no padrão correto
            if valor[0] not in tokens_validos_inicio:
                print_error('A abertura de chaves deve ocorrer apenas em procedimenos, funções, condicionais e laços.',chave)
            # Armazenando na pilha o primeiro token, ultimo token e a linha
            chaveCount.append([valor[-1], valor[0], chave])
        elif valor[-1] == 'fecha_chave':
            try:
                # Guardando valor do que foi retirado da pilha
                aux = chaveCount.pop()
                # Verificando se o que foi retirado pertencia a assinatura de uma função, para então saber se ela tinha retorno
                if aux[1] == 'funcao' and linha_anterior[0] != 'retorno':
                    print_error('A função necessita de um retorno.', aux[2])
            except Exception as e:
                # Na erro ao retirar algo de uma pilha vazia, nos diz que temos mais fecha_chave do que abre_chave
                print_error('A quantidade de fecha chave é superior ao de abre chave.', chave)

        # Guardando sempre a linha 'anterior' para validação do retorno da função
        linha_anterior = valor

    # Verificando se sobrou algum abre_chave na pilha
    if (len(chaveCount) > 0):
        aux = chaveCount.pop()
        print_error('A quantidade de abre chave é superior ao de fecha chave.', aux[2])


def verificar_parentese():
    parenteseCount = []
    for index, token in enumerate(tokens):
        if token == 'abre_parentese':
            parenteseCount.append(['(', numLinhas[index]])
        elif token == 'fecha_parentese':
            try:
                parenteseCount.pop()
            except Exception as e:
                print_error('A quantidade de fecha parentese é superior ao de abre parentese.', numLinhas[index])
    if (len(parenteseCount) > 0):
        aux = parenteseCount.pop()
        print_error('A quantidade de abre parentese é superior ao de fecha parentese.', aux[1])


def verificar_quantidade(tokens_lines):
    verificar_chave(tokens_lines)
    verificar_parentese()


# Verificando se o ultimo token de cada linha é um token ponto_virgula, caso não seja, deve de forma obrigatória se iniciar a linha com [if,while,procedimento,funcao]
def verificar_ponto_virgula(tokens_lines):
    # Guardando os tokens que serão válidos para casos onde não se finaliza a linha com ponto_virgula
    tokens_validos_inicio = ['condicional', 'funcao', 'procedimento', 'laco']

    for chave, valor in tokens_lines.items():
        if valor[-1] != 'ponto_virgula':
            if (valor[0] not in tokens_validos_inicio) and (
                    valor[0] != 'fecha_chave' and valor[-1] != 'fecha_chave' and len(valor) != 1):
                print_error('Finalização de expressão incorreta.', chave)


def assinatura_procedimento_funcao(token, linha):
    # Verificaçã do primeiro token, para saber se corresponde ao padrão dado a função/procedimento
    if (token == 'procedimento') or (token == 'funcao'):

        # Recuperação da linha, após verificação de existencia da funcao/procedimento
        lista_tokens_linha = get_line_tokens(linha)

        # Verificação se possui um identificador para essa função/procedimento
        if lista_tokens_linha[1] != 'identificador':
            print_error('Incorreta a assinatura da funcao/procedimento.', linha)

        # Verificação do conteudo presente entre o '(' (abre_parentese) e ')' (fecha_parentese)
        if (lista_tokens_linha[2] != 'abre_parentese') and (lista_tokens_linha[-2] != 'fecha_parentese'):
            print_error('Incorreta a assinatura da funcao/procedimento.', linha)

        # Utilização de função auxiliar os argumentos presentes na função/procedimento
        verificao_argumento_procedimento_funcao(lista_tokens_linha[3:-2], linha)


def verificao_argumento_procedimento_funcao(argumentos, linha):
    # Separação dos argumentos, separando a lista em sub-listas a partir do token 'virgula'
    lista_tokens = []
    sublista = []
    for token in argumentos:
        if token == 'virgula':
            lista_tokens.append(sublista)
            sublista = []
        else:
            sublista.append(token)

    lista_tokens.append(sublista)

    # Verificando se é respeitada a padronização de tokens na passagem dos argumentos
    for intervalo_tokens in lista_tokens:
        if len(intervalo_tokens) == 2:
            if intervalo_tokens[0] != 'tipo' or intervalo_tokens[1] != 'identificador':
                print_error('Incorreta a passagem dos argumentos.', linha)
        else:
            print_error('Incorreta a passagem dos argumentos.', linha)
