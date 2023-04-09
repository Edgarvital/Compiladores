def gerar(tabela_lexica, tabela_sintatica, lista_escopo):
    global tokens, lexemas, numLinhas, tokens_lines, lexemas_lines, tabela_simbolos, arquivo, lexemas_funcoes, open_l, close_l;
    # Limpar arquivo
    arquivo = open("CodigoIntermediario.txt", "w")
    arquivo.write("")
    arquivo.close
    arquivo = open("CodigoIntermediario.txt", "a")

    tokens = (tabela_lexica[tabela_lexica.columns[0:1:]]).values
    lexemas = (tabela_lexica[tabela_lexica.columns[1:2:]]).values
    numLinhas = (tabela_lexica[tabela_lexica.columns[2:3:]]).values

    open_l = 1
    close_l = 0

    indices_funcoes = tabela_sintatica.loc[tabela_sintatica['Token'] == "funcao"].index.to_numpy()
    lexemas_funcoes = tabela_sintatica.loc[indices_funcoes, 'Lexema'].values

    tokens_lines = create_line_tokens()
    lexemas_lines = create_line_lexemas()

    loop_geracao(tabela_lexica, lista_escopo)


def loop_geracao(tabela, lista_escopo):
    aux = 0
    for index, linha in tabela.iterrows():
        adicionar_identificador_arquivo(linha, aux)
        adicionar_print(linha)
        determinar_abertura_escopo(linha)
        determinar_fechamento_escopo(linha, lista_escopo)
        aux += 1
        if (verificar_reset_aux(linha)):
            aux = 0
def adicionar_identificador_arquivo(linha, aux):
    lista_lexemas = get_line_lexemas(linha['linha'])
    lista_tokens = get_line_tokens(linha['linha'])

    if (linha['Token'] == 'identificador' and aux == 1 and lista_tokens[0] == 'tipo'):
        if (lista_lexemas[3] not in lexemas_funcoes):
            linha_lexemas = ' '.join(lista_lexemas)
            arquivo.write(linha_lexemas + '\n')
        else:
            lista_lexemas[2] = '= call'
            linha_lexemas = ' '.join(lista_lexemas)
            arquivo.write(linha_lexemas + '\n')

def adicionar_print(linha):
    lista_lexemas = get_line_lexemas(linha['linha'])
    if(linha['Token'] == 'impressao'):
        lista_lexemas[0] = 'call print'
        linha_lexemas = ' '.join(lista_lexemas)
        arquivo.write(linha_lexemas + '\n')


def verificar_reset_aux(linha):
    if (linha['Token'] == 'ponto_virgula' or linha['Token'] == 'abre_chave' or linha['Token'] == 'fecha_chave'):
        return True

def determinar_abertura_escopo(linha):
    global open_l, close_l
    lista_lexemas = get_line_lexemas(linha['linha'])

    if linha['Token'] == 'procedimento':
        arquivo.write(lista_lexemas[1] + ':\n')
        arquivo.write('BeginProc;\n')

    elif linha['Token'] == 'funcao':
        arquivo.write(lista_lexemas[1] + ':\n')
        arquivo.write('BeginFunc;\n')

    elif linha['Token'] == 'condicional' and linha['Lexema'] == 'if':
        arquivo.write('_L' + str(open_l) + ": ")
        condicional = ajustar_condicional(lista_lexemas[2:-2])
        arquivo.write(lista_lexemas[0] + ' ' + ' '.join(condicional))
        open_l += 2
        close_l = open_l - 1
        arquivo.write(' goto _L' + str(close_l) + ':\n')

    elif linha['Token'] == 'laco':
        arquivo.write('_L' + str(open_l) + ": ")
        condicional = ajustar_condicional(lista_lexemas[2:-2])
        arquivo.write('if ' + ' '.join(condicional))
        open_l += 2
        close_l = open_l - 1
        arquivo.write(' goto _L' + str(close_l) + ':\n')

def ajustar_condicional(lista_condicional):
    for index, valor in enumerate(lista_condicional):
        if valor == "!=":
            lista_condicional[index] = '=='
        elif valor == "==":
            lista_condicional[index] = '!='
        elif valor == "<=":
            lista_condicional[index] = '>'
        elif valor == ">=":
            lista_condicional[index] = '<'
        elif valor == "<":
            lista_condicional[index] = '>='
        elif valor == ">":
            lista_condicional[index] = '<='
        elif valor == 'true':
            lista_condicional[index] = 'false'
        elif valor == 'false':
            lista_condicional[index] = 'true'

    return lista_condicional

def determinar_fechamento_escopo(linha, lista_escopo):
    global open_l, close_l
    lista_tokens = get_line_tokens(linha['linha'])

    if linha['Token'] == 'fecha_chave' and len(lista_tokens) == 1:
        tipo_escopo = determinar_tipo_fechamento_escopo(linha['linha'], lista_escopo)
        if tipo_escopo == 'funcao':
            arquivo.write('EndFunc;\n')

        elif tipo_escopo == 'procedimento':
            arquivo.write('EndProc;\n')

        elif tipo_escopo == 'condicional':
            arquivo.write('_L' + str(close_l) + ':\n')
            close_l -= 2

        elif tipo_escopo == 'laco':
            arquivo.write('goto _L' + str(close_l-1) + '\n')
            arquivo.write('_L' + str(close_l) + ':\n')
            close_l -= 2
    elif linha['Token'] == 'fecha_chave' and len(lista_tokens) != 1:
        print(close_l)
        arquivo.write('goto _L' + str(close_l +1) + '\n')
        arquivo.write('_L' + str(close_l) + ':\n')
        close_l += 1
        open_l += 1
def determinar_tipo_fechamento_escopo(linha, lista_escopo):

    for escopo in lista_escopo:
        if escopo[3] == linha:
            return escopo[1]

    return "nao_encontrado"

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
    return tokens_lines[linha].copy()
