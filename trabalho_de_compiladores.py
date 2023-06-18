# Caso prefira usar regex para separar os tokens(parece estar funcionando):
# import re
# regex = r"([\s,;\)\(]+)"
# tokens = re.split(regex, comando)
# tokens = tratar_tokens(tokens) # descomente essa função
# print(tokens)

# Elimina os espaços em branco capturados na lista de tokens do regex.
# def tratar_tokens(tokens):
#     novos_tokens = []

#     for token in tokens:
#         if token == " " or token == "":
#             continue
        
#         novos_tokens.append(token.strip())

#     return novos_tokens


# TODO: lembrar de ler o token ";" no final das regras chamadas lá em REGRA_COMANDO 
# Gramática:
# REGRA_COMANDO -> "use" REGRA_USE; | "create" REGRA_CREATE; | "insert" REGRA_INSERT; | "select" REGRA_SELECT; | 
# "update" REGRA_UPDATE; | "delete" REGRA_DELETE; | "truncate" REGRA_TRUNCATE;
# REGRA_USE -> id
# REGRA_CREATE -> "database" id | "table" id (id tipo[, id tipo]*) 
# ETC

TIPOS = ["STRING", "INTEGER", "DOUBLE"] 
SEPARADORES = [" ", ",", "(", ")", ";"]
PALAVRAS_RESERVADAS = ["USE", "CREATE", "SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "DATABASE", "FROM", "INTO", "VALUES", "ORDER_BY", "WHERE", "*", "=", "SET", "TABLE"]
PALAVRAS_RESERVADAS.extend(SEPARADORES)
PALAVRAS_RESERVADAS.extend(TIPOS)

comando = "CREATE TABLE a(nome string, idade integer)"

token_atual_eh_separador = False
index_inicial = 0 # Marca o início de um token
index_final = 0 # Marca o final de um token

def eh_id(token):
    return token not in PALAVRAS_RESERVADAS

def eh_tipo(token):
    return token in TIPOS

# TODO: consertar problemas que ocorrem ao ler separadores diferentes de " " tipo "(", já que são tokens a serem analisados.
def ler_token():
    global index_inicial, index_final, token_atual_eh_separador

    # Pula espaços em branco até chegar no começo do próximo token
    while index_final <= len(comando) - 1 and comando[index_final] == " ":
        index_final += 1

    index_inicial = index_final

    if token_atual_eh_separador:
        index_final += 1
    
    # Enquanto não tiver lido toda a entrada
    while index_final <= len(comando) - 1:
        char = comando[index_final]

        if char in SEPARADORES:
            break

        index_final += 1

    # Se o token possuir um único caracter
    if index_inicial == index_final:
        char = comando[index_inicial : index_final + 1]

        if char in SEPARADORES:
            token_atual_eh_separador = True

        token = char

    else:
        token = comando[index_inicial : index_final]

    return token.upper()

def main():
    global index_final

    # REGRA_COMANDO foi executado com sucesso e a string completa foi lida
    if REGRA_COMANDO() and index_final == len(comando):
        print("Comando analisado com sucesso")
        return True

    else:
        print("Erro ao analisar comando")
        return False

def REGRA_COMANDO():
    token = ler_token()
    
    if token == "USE":
        token = ler_token()

        if eh_id(token):
            token = ler_token()

            if token == ";":
                return True
            
            return False

    elif token == "CREATE":
        return REGRA_CREATE()
    
    # elif OUTRAS REGRAS

    # Não bateu com nenhuma das regras acima
    else:
        return False 

def REGRA_USE():
    token = ler_token()
    return eh_id(token)


def REGRA_CREATE():
    token = ler_token()

    if token == "DATABASE":
        token = ler_token()

        if eh_id(token):
            return True
        
        return False
        #token = ler_token()
        #print(token)

    elif token == "TABLE":
        token = ler_token()

        if eh_id(token):
            token = ler_token()

            if token == "(":
                token = ler_token()
                # cha

                token = ler_token()

                if token == ")":
                    return True

        #print(token)

if __name__ == "__main__":
    main()