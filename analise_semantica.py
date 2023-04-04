import pandas as pd


def analise(tabela_lexica, tabela_sintatica):
    global tokens, lexemas, numLinhas, tokens_lines, lexemas_lines, tabela_simbolos
    tokens = (tabela_lexica[tabela_lexica.columns[0:1:]]).values
    lexemas = (tabela_lexica[tabela_lexica.columns[1:2:]]).values
    numLinhas = (tabela_lexica[tabela_lexica.columns[2:3:]]).values

    tokens_lines = create_line_tokens()
    lexemas_lines = create_line_lexemas()

    try:
        loop_verificacao(tabela_sintatica)
    except Exception as e:
        print_error(e)


def loop_verificacao(tabela):
    for index, linha in tabela.iterrows():
        verificar_identificador(linha, index, tabela)


def verificar_identificador(linha, index, tabela):
    verificar_tipo_identificador_repetido(linha, index, tabela)
    verificar_variaveis_atribuicao(linha, index, tabela)


def verificar_variaveis_atribuicao(linha, index, tabela):
    if (linha['Token'] == 'identificador'):
        verificar_tokens_lexemas_atribuicao(linha, index, tabela)


def verificar_tokens_lexemas_atribuicao(linha, index, tabela):
    lexemas = get_lexema_identificadores_atribuicao(linha)
    linha_boolean = None
    count = 0
    if (lexemas):
        for i in range(index):
            linha_tabela = tabela.iloc[i]
            if linha_tabela['Lexema'] in lexemas:
                if linha['Tipo'] == linha_tabela['Tipo']:
                    count += 1
                else:
                    print_error('Tipo de variavel incompativel na atribuição', linha['Linha'])
                if linha_tabela['Tipo'] == 'boolean':
                    #Salva o boolean que está dentro do valor da linha atual da tabela que estamos verificando
                    linha_boolean = linha_tabela
        if count != len(lexemas):
            #Verificar os parametros da função antes de retornar o erro:
                #print_error('Identificador invalido, ele ainda não foi declarado!', linha['Linha'])
            return False

    verificar_tipo_inteiro_atribuicao(linha)
    #Verifica se o formato do boolean é valido, passando o lexema que tem o tipo boolean que salvamos anteriormente
    verificar_tipo_boolean_atribuicao(linha, linha_boolean)
    return True




def verificar_tipo_inteiro_atribuicao(linha):
    if linha['Tipo'] == 'int':
        if 'true' in linha['Valor'] or 'false' in linha['Valor']:
            print_error('Não é possivel atribuir um boolean à um inteiro', linha['Linha'])

def verificar_tipo_boolean_atribuicao(linha, linha_boolean):
    if linha['Tipo'] == 'boolean' and linha['Valor'] not in ['true', 'false']:
        if linha_boolean is not None:
            if linha_boolean['Lexema'] and linha_boolean['Lexema'] != linha['Valor']:
                    print_error('Não é possivel realizar operações com um boolean em uma atribuição', linha['Linha'])
        else:
            print_error('O identificador é do tipo boolean, só é possivel atribuir um boolean a ele', linha['Linha'])


def get_lexema_identificadores_atribuicao(linha):
    line = linha['Linha']
    tokens = get_line_tokens(line)
    lexemas = get_line_lexemas(line)
    lista_lexemas = []
    while (tokens[-1] != 'operador_atribuicao'):
        if (tokens.pop() == 'identificador'):
            lista_lexemas.append(lexemas[len(tokens)])
    return lista_lexemas


def verificar_tipo_identificador_repetido(linha, index, tabela):
    if (linha['Token'] == 'identificador'):
        for linha_tabela in range(index):
            if (tabela.iloc[linha_tabela]['Token'] == 'identificador'):
                if (linha['Lexema'] == tabela.iloc[linha_tabela]['Lexema']):
                    if (verificar_escopo_identificador_repetido(linha, tabela.iloc[linha_tabela])):
                        if (linha['Tipo'] == tabela.iloc[linha_tabela]['Tipo']):
                            return True
                        else:
                            print_error('Atribuição de tipos diferentes no mesmo identificador', linha['Linha'])
    return False


def verificar_escopo_identificador_repetido(linha, linha_tabela):
    if (linha_tabela['Escopo'] == 'global'):
        return True;
    escopo = linha_tabela['Escopo'].split('[')[1].split(']')[0].split(',')

    if (escopo):
        if int(escopo[0]) <= int(linha['Linha']) <= int(escopo[1]):
            return True
    return False


def print_error(mensagem, linha=None):
    if linha != None:
        print("Erro de Semantica:", mensagem, 'Linha:', linha)
    else:
        print("Erro de Semantica:", mensagem)
    exit()


def create_line_lexemas():
    lista_lexemas = {}
    lexemas_line = []
    linha_aux = [1]
    last_position = -1
    for index, linha in enumerate(numLinhas):
        if (linha_aux == linha):
            lexemas_line.append(lexemas[index, 0])
        else:
            lista_lexemas[linha_aux[0]] = lexemas_line
            linha_aux = linha
            lexemas_line = []
            lexemas_line.append(lexemas[index, 0])

    lista_lexemas[numLinhas[last_position, 0]] = [lexemas_line[last_position]]
    return lista_lexemas


def get_line_lexemas(linha):
    try:
        return lexemas_lines[linha].copy()
    except Exception as e:
        print('linha vazia ou não encontrada')


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


def get_line_tokens(linha):
    try:
        return tokens_lines[linha].copy()
    except Exception as e:
        print('linha vazia ou não encontrada')
