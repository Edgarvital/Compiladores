import pandas as pd


def analise(tabela):
    global tokens, lexemas, numLinhas, tokens_lines, tabela_simbolos
    tokens = (tabela[tabela.columns[0:1:]]).values
    lexemas = (tabela[tabela.columns[1:2:]]).values
    numLinhas = (tabela[tabela.columns[2:3:]]).values

    tabela_simbolos = pd.DataFrame(
        columns=['Token', 'Lexema', 'Tipo', 'linha', 'valor',
                 'qntParametros', 'variaveis', 'tiposVar','escopo'])
#Exemplo  de add
#tabela_simbolos.loc[len(tabela_simbolos)] = ["IdVariavel", tabela_tokens["Lexema"][i], tabela_tokens["Lexema"][i - 1], tabela_tokens["linha"][i], valor,"-","-","-",escopo]

    tokens_lines = create_line_tokens()
    try:
        verificar_escopo(tokens_lines)
        verificar_parentese()

        verificar_ponto_virgula(tokens_lines)

        loop_verificacao()
    except Exception as e:
        print_error('Erro de sintaxe')

    print(tabela_simbolos.to_string())


def loop_verificacao():
    for index, token in enumerate(tokens):
        assinatura_if(token, numLinhas[index, 0], lexemas[index])
        assinatura_else(token, numLinhas[index, 0], lexemas[index])
        verificar_atribuicao(token, numLinhas[index, 0])
        assinatura_procedimento_funcao(token, numLinhas[index, 0], index)
        assinatura_while(token, numLinhas[index, 0])
        assinatura_print(token, numLinhas[index, 0])


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

def assinatura_if(token, linha, lexema):
    if (token == 'condicional' and lexema == 'if'):
        lista_tokens_linha = get_line_tokens(linha)
        if lista_tokens_linha.pop() == 'abre_chave':
            if lista_tokens_linha.pop() == 'fecha_parentese':
                if verificar_expressao_booleana(lista_tokens_linha, linha):
                    if lista_tokens_linha.pop() == 'abre_parentese':
                        if len(lista_tokens_linha) == 1 and lista_tokens_linha[0] == 'condicional':
                            return True
        print_error('Erro na assinatura do IF', linha)

def assinatura_print(token, linha):
    if (token == 'impressao'):
        lista_tokens_linha = get_line_tokens(linha)
        if lista_tokens_linha.pop() == 'ponto_virgula':
            if lista_tokens_linha.pop() == 'fecha_parentese':
                if lista_tokens_linha.pop() in ['numerico','identificador', 'booleano']:
                    if lista_tokens_linha.pop() == 'abre_parentese':
                        if len(lista_tokens_linha) == 1 and lista_tokens_linha[0] == 'impressao':
                            return True
        print_error('Erro na assinatura do PRINT', linha)

def assinatura_else(token, linha, lexema):
    if token == 'condicional' and lexema == 'else':
        lista_tokens_linha = get_line_tokens(linha)
        if len(lista_tokens_linha) == 3:
            if lista_tokens_linha.pop() == 'abre_chave':
                if lista_tokens_linha.pop() == 'condicional':
                    if lista_tokens_linha.pop() == 'fecha_chave':
                        if len(lista_tokens_linha) == 0:
                            return True
        print_error('Erro na assinatura do ELSE', linha)


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


def verifcar_abertura_chave(linha, posicao, tokens_validos, token, numero_linha):
    if token == 'abre_chave':
        if linha[0] not in tokens_validos and len(linha) > 1 and(
                linha[0] != 'fecha_chave' and linha[1] != 'condicional' and linha[2] != 'abre_chave'):
            print_error('Abertura de chave invalida.',numero_linha)
        if posicao != (len(linha) - 1):
            print_error('Abertura de chave invalida.',numero_linha)
        return True
    return False


def verifcar_fechamento_chave(token):
    if token == 'fecha_chave':
        return True
    return False


def verificar_escopo(tokens_lines):
    tokens_validos_inicio = ['condicional', 'funcao', 'procedimento', 'laco']
    chave_Count = []
    lista_escopo_fechado = []
    count_lexema = 0
    for numero_linha, linha in tokens_lines.items():
        for indice, token in enumerate(linha):
            # Verificar abertura de chave
            if verifcar_abertura_chave(linha, indice, tokens_validos_inicio, token,numero_linha):
                chave_Count.append([linha[-1], linha[0], numero_linha])

            # verificar fechamento de chave
            elif verifcar_fechamento_chave(token):
                try:
                    # Guardando valor do que foi retirado da pilha
                    aux = chave_Count.pop()
                    lista_escopo_fechado.append(aux)
                    # Verificando se o que foi retirado pertencia a assinatura de uma função, para então saber se ela tinha retorno
                    if aux[1] == 'funcao' and linha_anterior[0] != 'retorno':
                        print_error('A função necessita de um retorno.', aux[2])
                except Exception as e:
                    # Na erro ao retirar algo de uma pilha vazia, nos diz que temos mais fecha_chave do que abre_chave
                    print_error('A quantidade de fecha chave é superior ao de abre chave.', numero_linha)

            # Verificação de desvio incondicional
            elif token == 'desvio_incondicional':
                aux = 0
                for item in chave_Count:
                    if 'laco' in item:
                        aux += 1
                if aux == 0:
                    print_error('Desvios incondicionais devem estar presentes apenas em laços.', numero_linha)

            # Verificação de retorno
            elif token == 'retorno':
                aux = 0
                for item in chave_Count:
                    if 'funcao' in item:
                        aux += 1
                if aux == 0:
                    print_error('Retorno deve estar presente apenas em funções.', numero_linha)

             # Verificação de uso da condicional else
            elif token == 'condicional' and lexemas[count_lexema] == 'else':
                if len(lista_escopo_fechado) == 0 or lista_escopo_fechado[-1][1] != 'condicional':
                    print_error('Condicional ELSE deve ser aplicada somente após o IF.')

            count_lexema += 1

        # Guardando sempre a linha 'anterior' para validação do retorno da função
        linha_anterior = linha

    # Verificando se sobrou algum abre_chave na pilha
    if (len(chave_Count) > 0):
        aux = chave_Count.pop()
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


# Verificando se o ultimo token de cada linha é um token ponto_virgula, caso não seja, deve de forma obrigatória se iniciar a linha com [if,while,procedimento,funcao]
def verificar_ponto_virgula(tokens_lines):
    # Guardando os tokens que serão válidos para casos onde não se finaliza a linha com ponto_virgula
    tokens_validos_inicio = ['condicional', 'funcao', 'procedimento', 'laco']
    for numero_linha, linha in tokens_lines.items():
        if linha[-1] != 'ponto_virgula':
            if (linha[0] not in tokens_validos_inicio) and (len(linha)>=1 and linha[0] != 'fecha_chave'):
                print_error('Finalização de expressão incorreta.', numero_linha)


def assinatura_procedimento_funcao(token, numero_linha, index):
    tipo = ""
    qtd_parametros = 0
    # Verificação do primeiro token, para saber se corresponde ao padrão dado a função/procedimento
    if (token == 'procedimento') or (token == 'funcao'):

        # Recuperação da linha, após verificação de existencia da funcao/procedimento
        linha = get_line_tokens(numero_linha)

        # Verificação se possui um identificador para essa função/procedimento
        if linha[1] != 'identificador':
            print_error('Incorreta a assinatura da funcao/procedimento.', numero_linha)

        # Verificação do conteudo presente entre o '(' (abre_parentese) e ')' (fecha_parentese)
        if (linha[2] != 'abre_parentese') and (linha[-2] != 'fecha_parentese'):
            print_error('Incorreta a assinatura da funcao/procedimento.', numero_linha)

        #Adição na tabela de simbolos
        tabela_simbolos.loc[len(tabela_simbolos)] = [token[0], lexemas[index+1][0], '-', numero_linha, '-',"qtd_parametros","val 1, val 2","tipo delas",'-']

        # Utilização de função auxiliar os argumentos presentes na função/procedimento
        verificao_argumento_procedimento_funcao(linha[3:-2], numero_linha)


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
