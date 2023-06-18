import re
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
# REGRA_ID_TIPO_EXTRA -> , id tipo REGRA_ID_TIPO_EXTRA | 'vazio'
# REGRA_INSERT -> "INTO" <id> (<id> REGRA_ID_EXTRA) "VALUES" REGRA_VALUES
# REGRA_ID_EXTRA -> , <id> REGRA_ID_EXTRA | 'vazio'
# REGRA_VALUES -> (<valor> REGRA_VALUES_EXTRA)
# REGRA_VALUES_EXTRA -> , <valor> REGRA_VALUES_EXTRA | 'vazio'
# REGRA_SELECT -> "FROM" <id> | <id> REGRA_ID_EXTRA "FROM" <id> | * "FROM" <id> REGRA_*_FROM_ID
# REGRA_*_FROM_ID -> "ORDER" "BY" <id> | "WHERE" <id> = <valor>
# REGRA_UPDATE -> <id> 'SET' <id> = <valor> WHERE <id> = <valor>
# REGRA_DELETE -> "FROM" <id> "WHERE" <id> = <valor>
# REGRA_TRUNCATE -> "TABLE" <id>

# USE <id>;
# CREATE DATABASE <id>;
# CREATE TABLE <id> (<id> <tipo> [, <id> <tipo>]);
# INSERT INTO <id> (<id> [, <id>]) VALUES (<valor> [, <valor>]) [, (<valor> [, <valor>])];
# SELECT FROM <id>;
# SELECT <id> [, <id>]* FROM <id>;
# SELECT * FROM <id> ORDER BY <id>;
# SELECT * FROM <id> WHERE <id> = <valor>;
# UPDATE <id> SET <id> = <valor> WHERE <id> = <valor>;
# DELETE FROM <id> WHERE <id> = <valor>;
# TRUNCATE TABLE <id>;

TIPOS = ["STRING", "INTEGER", "DOUBLE"]
SEPARADORES = [" ", ",", "(", ")", ";"]
PALAVRAS_RESERVADAS = ["USE", "CREATE", "SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "DATABASE", "FROM", "INTO",
                       "VALUES", "ORDER_BY", "WHERE", "*", "=", "SET", "TABLE"]
PALAVRAS_RESERVADAS.extend(SEPARADORES)
PALAVRAS_RESERVADAS.extend(TIPOS)

## Recebe um comando retorna uma lista de tokens, utiliza regex
def getTokens(comando):
    ## Obtenção dos tokens via regex
    regex = r"([\s,;\)\(]+)"
    lista_de_tokens = re.split(regex, comando)

    ## Tratamento dos Tokens
    # Removendo Espaços em Branco
    while ' ' in lista_de_tokens:
        lista_de_tokens.remove(' ')
    while '' in lista_de_tokens:
        lista_de_tokens.remove('')

    # Removendo espaços em branco nos tokens
    for token_index in range(0, len(lista_de_tokens)):
        lista_de_tokens[token_index] = lista_de_tokens[token_index].replace(' ', '')
    if lista_de_tokens[-1] == ');':
        lista_de_tokens[-1] = ')'
        lista_de_tokens.append(";")

    # Adicionando um $ ao final
    lista_de_tokens.append("$")

    return lista_de_tokens

## Verifica se o token/sequencia de tokens está de acordo com as regras de produção
def verifica_token(token):
    global next_token

    if next_token.upper() == token:
        next_token = lista_de_tokens.pop(0)
    else:
        print(f"ERRO, Token {next_token} não era esperado!, ao invés disso era esperado {token}")
        exit(1)

# Verifica se o next token é um ID ou não
def next_token_is_id():
    if next_token.upper() not in PALAVRAS_RESERVADAS and next_token[0] != ">" and next_token[0] != "<" \
            and next_token[0] != "!" and not next_token[0].isnumeric() and next_token[0] not in SEPARADORES:
        return True
    else:
        return False

## Verifica Token mas para IDs
# Altere aqui a definição de um ID
def verifica_token_id():
    global next_token
    if next_token_is_id():
          next_token = lista_de_tokens.pop(0)
    else:
        print(f"ERRO, Token {next_token} não era esperado!, ao invés disso era esperado <id>")
        exit(1)

## Verifica Token mas para Tipos
def verifica_token_tipo():
    global next_token
    if next_token.upper() in TIPOS:
        next_token = lista_de_tokens.pop(0)
    else:
        print(f"ERRO, Token {next_token} não era esperado!, ao invés disso era esperado <tipo>")
        exit(1)

# verifica se o proximo token é um value ou não
# Altere aqui a definição do que é um value
def next_token_is_value():
    if next_token.isalnum() and next_token not in PALAVRAS_RESERVADAS:
        return True
    else:
        return False

# verifica token mas para values
def verifica_token_value():
    global next_token
    if next_token_is_value():
        next_token = lista_de_tokens.pop(0)
    else:
        print(f"ERRO, Token {next_token} não era esperado!, ao invés disso era esperado <value>")
        exit(1)

# REGRA_USE -> id
def REGRA_USE():
    # Esperando um <id>, se este for o caso apenas passe para o proximo token
    verifica_token_id()

# REGRA_ID_TIPO_EXTRA -> , id tipo REGRA_ID_TIPO_EXTRA | 'vazio'
def REGRA_ID_TIPO_EXTRA():
    # , id tipo REGRA_ID_TIPO_EXTRA
    if next_token == ',':
        verifica_token(',')
        verifica_token_id()
        verifica_token_tipo()
        REGRA_ID_TIPO_EXTRA()
    # 'vazio'
    else:
        return

# REGRA_CREATE -> "database" id | "table" id (<id> <tipo> REGRA_ID_TIPO_EXTRA)
def REGRA_CREATE():
    # "database" id
    if next_token.upper() == "DATABASE":
        verifica_token("DATABASE")
        verifica_token_id()
    # "table" id ( <id> <tipo> REGRA_ID_TIPO_EXTRA )
    if next_token.upper() == "TABLE":
        verifica_token("TABLE")
        verifica_token_id()
        verifica_token('(')
        verifica_token_id()
        verifica_token_tipo()
        REGRA_ID_TIPO_EXTRA()
        verifica_token(')')


# REGRA_VALUES_EXTRA -> , <valor> REGRA_VALUES_EXTRA | 'vazio'
def REGRA_VALUES_EXTRA():
    # , <valor> REGRA_VALUES_EXTRA
    if next_token == ',':
        verifica_token(',')
        verifica_token_value()
        REGRA_VALUES_EXTRA()
    # 'vazio'
    else:
        return
# REGRA_VALUES -> (<valor> REGRA_VALUES_EXTRA)
def REGRA_VALUES():
    # (<valor> REGRA_VALUES_EXTRA)
    if next_token == '(':
        verifica_token('(')
        verifica_token_value()
        REGRA_VALUES_EXTRA()
        verifica_token(')')

# REGRA_ID_EXTRA -> , <id> REGRA_ID_EXTRA | 'vazio'
# Verifica o padrão ", <id>"
def REGRA_ID_EXTRA():
    # , <id> REGRA_ID_EXTRA
    if next_token == ',':
        verifica_token(',')
        verifica_token_id()
        REGRA_ID_EXTRA()
    # 'vazio'
    else:
        return

# REGRA_INSERT -> "INTO" <id> (<id> REGRA_ID_EXTRA) "VALUES" REGRA_VALUES
def REGRA_INSERT():
    if next_token.upper() == 'INTO':
        verifica_token('INTO')
        verifica_token_id()
        verifica_token('(')
        verifica_token_id()
        REGRA_ID_EXTRA()
        verifica_token(')')
        verifica_token('VALUES')
        REGRA_VALUES()

# REGRA_all_FROM_ID -> "ORDER" "BY" <id> | "WHERE" <id> = <valor>
def REGRA_all_FROM_ID():
    # "ORDER" "BY" <id>
    if next_token.upper() == 'ORDER':
        verifica_token('ORDER')
        verifica_token('BY')
        verifica_token_id()
    # "WHERE" <id> = <valor>
    elif next_token.upper() == 'WHERE':
        verifica_token('WHERE')
        verifica_token_id()
        verifica_token('=')
        verifica_token_value()

# REGRA_SELECT -> "FROM" <id> | <id> REGRA_ID_EXTRA "FROM" <id> | * "FROM" <id> REGRA_*_FROM_ID
def REGRA_SELECT():
    # "FROM" <id>
    if next_token.upper() == 'FROM':
        verifica_token('FROM')
        verifica_token_id()
    # <id> REGRA_ID_EXTRA "FROM" <id>
    elif next_token_is_id():
        verifica_token_id()
        REGRA_ID_EXTRA()
        verifica_token('FROM')
        verifica_token_id()
    # * "FROM" <id> REGRA_*_FROM_ID
    elif next_token == '*':
        verifica_token('*')
        verifica_token('FROM')
        verifica_token_id()
        REGRA_all_FROM_ID()

# REGRA_UPDATE -> <id> 'SET' <id> = <valor> WHERE <id> = <valor>
def REGRA_UPDATE():
    if next_token_is_id():
        verifica_token_id()
        verifica_token('SET')
        verifica_token_id()
        verifica_token('=')
        verifica_token_value()
        verifica_token('WHERE')
        verifica_token_id()
        verifica_token('=')
        verifica_token_value()

# REGRA_DELETE -> "FROM" <id> "WHERE" <id> = <valor>
def REGRA_DELETE():
    if next_token.upper() ==  "FROM":
        verifica_token('FROM')
        verifica_token_id()
        verifica_token('WHERE')
        verifica_token_id()
        verifica_token('=')
        verifica_token_value()

# REGRA_TRUNCATE -> "TABLE" <id>
def REGRA_TRUNCATE():
    if next_token.upper() == "TABLE":
        verifica_token('TABLE')
        verifica_token_id()

## Regra inicial da gramatica
# REGRA_COMANDO -> "use"; REGRA_USE REGRA_COMANDO | "create" REGRA_CREATE; REGRA_COMANDO | "insert" REGRA_INSERT; REGRA_COMANDO
# "select" REGRA_SELECT; REGRA_COMANDO| "update" REGRA_UPDATE; REGRA_COMANDO | "delete" REGRA_DELETE; REGRA_COMANDO|
# "truncate" REGRA_TRUNCATE REGRA_COMANDO;
def REGRA_COMANDO():
    # "use" REGRA_USE;
    if next_token.upper() == 'USE':
        verifica_token('USE')
        REGRA_USE()
        verifica_token(';')
        REGRA_COMANDO()
    # "create" REGRA_CREATE;
    elif next_token.upper() == 'CREATE':
        verifica_token('CREATE')
        REGRA_CREATE()
        verifica_token(';')
        REGRA_COMANDO()
    # "insert" REGRA_INSERT;
    elif next_token.upper() == 'INSERT':
        verifica_token('INSERT')
        REGRA_INSERT()
        verifica_token(';')
        REGRA_COMANDO()
    # "select" REGRA_SELECT;
    elif next_token.upper() == 'SELECT':
        verifica_token('SELECT')
        REGRA_SELECT()
        verifica_token(';')
        REGRA_COMANDO()
    # "update" REGRA_UPDATE;
    elif next_token.upper() == 'UPDATE':
        verifica_token('UPDATE')
        REGRA_UPDATE()
        verifica_token(';')
        REGRA_COMANDO()
    # "delete" REGRA_DELETE;
    elif next_token.upper() == 'DELETE':
        verifica_token('DELETE')
        REGRA_DELETE()
        verifica_token(';')
        REGRA_COMANDO()
    # "truncate" REGRA_TRUNCATE;
    elif next_token.upper() == 'TRUNCATE':
        verifica_token('TRUNCATE')
        REGRA_TRUNCATE()
        verifica_token(';')
        REGRA_COMANDO()
    else:
        return


# REGRA_DELETE -> "FROM" <id> "WHERE" <id> = <valor>
if __name__ == "__main__":
    comando = "CREATE database tabela; INSERT INTO tabela(nomes) values (carlso);"

    global lista_de_tokens
    lista_de_tokens = getTokens(comando)
    print(f"Lista de Tokens = {lista_de_tokens}")
    global next_token
    next_token = lista_de_tokens.pop(0)

    REGRA_COMANDO()

    if next_token == "$":
        print("Comando Aceito!")
    else:
        print(f"Comando Rejeitado! {next_token} não deveria estar ali!")
