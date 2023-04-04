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
        verificar_chamada_funcao_procedimento(linha, index, tabela)

def verificar_chamada_funcao_procedimento(linha, index, tabela):
    # Recuperação dos indices das funcoes
    indices_funcoes = tabela.loc[tabela['Token'] == "funcao"].index.to_numpy()
    # Recuperacao dos lexemas das funcoes
    lexemas_funcoes = tabela.loc[indices_funcoes, 'Lexema']

    # Recuperação dos indices dos procedimentos
    indices_procedimentos = tabela.loc[tabela['Token'] == "procedimento"].index.to_numpy()
    # Recuperacao dos lexemas dos procedimentos
    lexemas_procedimentos = tabela.loc[indices_procedimentos, 'Lexema']

    # Verificação de atribuição com procedimento
    for lexema in lexemas_procedimentos:
        if lexema+'(' in linha['Valor']:
            print_error('Procedimento não pode estar presente em uma atribuição', linha['Linha'])
            exit()

    # Verificação de função
    for lexema in lexemas_funcoes:
        if lexema+'(' in linha['Valor']:
            lista_argumentos = linha['Valor'].split('(')[1].split(')')[0].split(',')
            validar_parametros(lista_argumentos, lexema, tabela, linha)

def validar_parametros(lista_argumentos, nome, tabela, linha):
    # Nome varia entre os possiveis nome de uma funcao e procedimento
    linha_funcao = tabela.loc[tabela['Lexema'] == nome]
    tipos_parametros = linha_funcao['TiposVar'].values[0]

    # Quantidade de argumento e parametros tem que ser os mesmos
    if len(tipos_parametros) != len(lista_argumentos):
        print_error('Quantidade de argumentos passados está incorreta', linha['Linha'])
        exit()

    # Tipos de cada argumento tem que ser o correto
    for index, argumento in enumerate(lista_argumentos):
        # Verifica se o argumento é uma variavel
        linha_argumento = tabela.loc[tabela['Lexema'] == argumento]
        if not linha_argumento.empty:
            # Verifica se o tipo da variavel bate com o tipo esperado pela função
            if tipos_parametros[index] != linha_argumento['Tipo'].values[0]:
                print_error('Tipo do argumento ' + str(index + 1) + 'º está incorreto', linha['Linha'])
                exit()
        else:
            # Se não for uma varivel só pode ser um valor numero ou boolean

            # Verifica se é boolean
            if argumento == 'true' or argumento == 'false':
                # Verifica se o tipo da variavel bate com o tipo esperado pela função
                if tipos_parametros[index] != 'boolean':
                    print_error('Tipo do ' + str(index + 1) + 'º argumento está incorreto', linha['Linha'])
                    exit()
            else:
                # Só nos sobra verificar se o tipo é inteiro
                if tipos_parametros[index] != 'int':
                    print_error('Tipo do ' + str(index + 1) + 'º argumento está incorreto', linha['Linha'])
                    exit()


def verificar_identificador(linha, index, tabela):
    verificar_tipo_identificador_repetido(linha, index, tabela)


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
                            exit()
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
