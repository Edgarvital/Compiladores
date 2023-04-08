def gerar(tabela_tokens):
    # Limpar arquivo
    limpar = open("CodigoIntermediario.txt", "w")
    limpar.write("")
    limpar.close

    # Geração de código intermediario
    identacao = ""
    linha = ""
    qntLabel = 0
    aux = -1

    arquivo = open("CodigoIntermediario.txt", "a")