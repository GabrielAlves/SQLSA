import re

TIPOS = ["STRING", "INTEGER", "DOUBLE"]
SEPARADORES = [" ", ",", "(", ")", ";"]
PALAVRAS_RESERVADAS = ["USE", "CREATE", "SELECT", "INSERT", "UPDATE", "DELETE", "TRUNCATE", "DATABASE", "FROM", "INTO",
                       "VALUES", "ORDER_BY", "WHERE", "*", "=", "SET", "TABLE"]
PALAVRAS_RESERVADAS.extend(SEPARADORES)
PALAVRAS_RESERVADAS.extend(TIPOS)

class Analisador:
    def __init__(self):
        self.historico = ""
        self.sucesso = True

    def acrescentar_mensagem_ao_historico(self, mensagem):
        self.historico += f"{mensagem}\n"

    def analisar_comando(self, comando):
        self.comando = comando
        self.lista_de_tokens = self.getTokens(comando)
        print(self.lista_de_tokens)
        self.next_token = self.lista_de_tokens.pop(0)
        self.REGRA_COMANDO()

    def retornar_resultado(self):
        return self.sucesso
        # return self.next_token == "$"

        ## Recebe um comando retorna uma lista de tokens, utiliza regex
    def getTokens(self, comando):
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
        
        while ');' in lista_de_tokens:
            index = lista_de_tokens.index(');')
            lista_de_tokens[index] = ')'
            lista_de_tokens.insert(index+1, ';')

        # Adicionando um $ ao final
        lista_de_tokens.append("$")

        return lista_de_tokens

    ## Verifica se o token/sequencia de tokens está de acordo com as regras de produção
    def verifica_token(self, token):
        self.acrescentar_mensagem_ao_historico(f"Verificando token {token}")

        if self.next_token.upper() == token:
            self.next_token = self.lista_de_tokens.pop(0)
        else:
            print(f"ERRO, Token {self.next_token} não era esperado!, ao invés disso era esperado {token}")
            self.sucesso = False

    # Verifica se o next token é um ID ou não
    def next_token_is_id(self):
        if self.next_token.upper() not in PALAVRAS_RESERVADAS and self.next_token[0] != ">" and self.next_token[0] != "<" \
                and self.next_token[0] != "!" and not self.next_token[0].isnumeric() and self.next_token[0] not in SEPARADORES:
            return True
        else:
            return False

    ## Verifica Token mas para IDs
    # Altere aqui a definição de um ID
    def verifica_token_id(self):
        if self.next_token_is_id():
            self.next_token = self.lista_de_tokens.pop(0)
        else:
            print(f"ERRO, Token {self.next_token} não era esperado!, ao invés disso era esperado <id>")
            self.sucesso = False

    ## Verifica Token mas para Tipos
    def verifica_token_tipo(self):
        if self.next_token.upper() in TIPOS:
            self.next_token = self.lista_de_tokens.pop(0)
        else:
            print(f"ERRO, Token {self.next_token} não era esperado!, ao invés disso era esperado <tipo>")
            self.sucesso = False

    # verifica se o proximo token é um value ou não
    # Altere aqui a definição do que é um value
    def next_token_is_value(self):
        if self.next_token.isalnum() and self.next_token not in PALAVRAS_RESERVADAS:
            return True
        else:
            return False

    # verifica token mas para values
    def verifica_token_value(self):
        if self.next_token_is_value():
            self.next_token = self.lista_de_tokens.pop(0)
        else:
            print(f"ERRO, Token {self.next_token} não era esperado!, ao invés disso era esperado <value>")
            self.sucesso = False

    # REGRA_USE -> id
    def REGRA_USE(self):
        # Esperando um <id>, se este for o caso apenas passe para o proximo token
        self.verifica_token_id()

    # REGRA_ID_TIPO_EXTRA -> , id tipo REGRA_ID_TIPO_EXTRA | 'vazio'
    def REGRA_ID_TIPO_EXTRA(self):
        # , id tipo REGRA_ID_TIPO_EXTRA
        if self.next_token == ',':
            self.verifica_token(',')
            self.verifica_token_id()
            self.verifica_token_tipo()
            self.REGRA_ID_TIPO_EXTRA()
        # 'vazio'
        else:
            return

    # REGRA_CREATE -> "database" id | "table" id (<id> <tipo> REGRA_ID_TIPO_EXTRA)
    def REGRA_CREATE(self):
        # "database" id
        if self.next_token.upper() == "DATABASE":
            self.verifica_token("DATABASE")
            self.verifica_token_id()
        # "table" id ( <id> <tipo> REGRA_ID_TIPO_EXTRA )
        if self.next_token.upper() == "TABLE":
            self.verifica_token("TABLE")
            self.verifica_token_id()
            self.verifica_token('(')
            self.verifica_token_id()
            self.verifica_token_tipo()
            self.REGRA_ID_TIPO_EXTRA()
            self.verifica_token(')')


    # REGRA_VALUES_EXTRA -> , <valor> REGRA_VALUES_EXTRA | 'vazio'
    def REGRA_VALUES_EXTRA(self):
        # , <valor> REGRA_VALUES_EXTRA
        if self.next_token == ',':
            self.verifica_token(',')
            self.verifica_token_value()
            self.REGRA_VALUES_EXTRA()
        # 'vazio'
        else:
            return
    # REGRA_VALUES -> (<valor> REGRA_VALUES_EXTRA)
    def REGRA_VALUES(self):
        # (<valor> REGRA_VALUES_EXTRA)
        if self.next_token == '(':
            self.verifica_token('(')
            self.verifica_token_value()
            self.REGRA_VALUES_EXTRA()
            self.verifica_token(')')

    # REGRA_ID_EXTRA -> , <id> REGRA_ID_EXTRA | 'vazio'
    # Verifica o padrão ", <id>"
    def REGRA_ID_EXTRA(self):
        # , <id> REGRA_ID_EXTRA
        if self.next_token == ',':
            self.verifica_token(',')
            self.verifica_token_id()
            self.REGRA_ID_EXTRA()
        # 'vazio'
        else:
            return

    # REGRA_INSERT -> "INTO" <id> (<id> REGRA_ID_EXTRA) "VALUES" REGRA_VALUES
    def REGRA_INSERT(self):
        if self.next_token.upper() == 'INTO':
            self.verifica_token('INTO')
            self.verifica_token_id()
            self.verifica_token('(')
            self.verifica_token_id()
            self.REGRA_ID_EXTRA()
            self.verifica_token(')')
            self.verifica_token('VALUES')
            self.REGRA_VALUES()

    # REGRA_all_FROM_ID -> "ORDER" "BY" <id> | "WHERE" <id> = <valor>
    def REGRA_all_FROM_ID(self):
        # "ORDER" "BY" <id>
        if self.next_token.upper() == 'ORDER':
            self.verifica_token('ORDER')
            self.verifica_token('BY')
            self.verifica_token_id()
        # "WHERE" <id> = <valor>
        elif self.next_token.upper() == 'WHERE':
            self.verifica_token('WHERE')
            self.verifica_token_id()
            self.verifica_token('=')
            self.verifica_token_value()

    # REGRA_SELECT -> "FROM" <id> | <id> REGRA_ID_EXTRA "FROM" <id> | * "FROM" <id> REGRA_*_FROM_ID
    def REGRA_SELECT(self):
        # "FROM" <id>
        if self.next_token.upper() == 'FROM':
            self.verifica_token('FROM')
            self.verifica_token_id()
        # <id> REGRA_ID_EXTRA "FROM" <id>
        elif self.next_token_is_id():
            self.verifica_token_id()
            self.REGRA_ID_EXTRA()
            self.verifica_token('FROM')
            self.verifica_token_id()
        # * "FROM" <id> REGRA_*_FROM_ID
        elif self.next_token == '*':
            self.verifica_token('*')
            self.verifica_token('FROM')
            self.verifica_token_id()
            self.REGRA_all_FROM_ID()

    # REGRA_UPDATE -> <id> 'SET' <id> = <valor> WHERE <id> = <valor>
    def REGRA_UPDATE(self):
        if self.next_token_is_id():
            self.verifica_token_id()
            self.verifica_token('SET')
            self.verifica_token_id()
            self.verifica_token('=')
            self.verifica_token_value()
            self.verifica_token('WHERE')
            self.verifica_token_id()
            self.verifica_token('=')
            self.verifica_token_value()

    # REGRA_DELETE -> "FROM" <id> "WHERE" <id> = <valor>
    def REGRA_DELETE(self):
        if self.next_token.upper() ==  "FROM":
            self.verifica_token('FROM')
            self.verifica_token_id()
            self.verifica_token('WHERE')
            self.verifica_token_id()
            self.verifica_token('=')
            self.verifica_token_value()

    # REGRA_TRUNCATE -> "TABLE" <id>
    def REGRA_TRUNCATE(self):
        if self.next_token.upper() == "TABLE":
            self.verifica_token('TABLE')
            self.verifica_token_id()

    ## Regra inicial da gramatica
    # REGRA_COMANDO -> "use"; REGRA_USE REGRA_COMANDO | "create" REGRA_CREATE; REGRA_COMANDO | "insert" REGRA_INSERT; REGRA_COMANDO
    # "select" REGRA_SELECT; REGRA_COMANDO| "update" REGRA_UPDATE; REGRA_COMANDO | "delete" REGRA_DELETE; REGRA_COMANDO|
    # "truncate" REGRA_TRUNCATE REGRA_COMANDO;
    def REGRA_COMANDO(self):
        # "use" REGRA_USE;
        self.acrescentar_mensagem_ao_historico("Entrando em REGRA_COMANDO")

        if self.next_token.upper() == 'USE':
            self.verifica_token('USE')
            self.REGRA_USE()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        # "create" REGRA_CREATE;
        elif self.next_token.upper() == 'CREATE':
            self.verifica_token('CREATE')
            self.REGRA_CREATE()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        # "insert" REGRA_INSERT;
        elif self.next_token.upper() == 'INSERT':
            self.verifica_token('INSERT')
            self.REGRA_INSERT()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        # "select" REGRA_SELECT;
        elif self.next_token.upper() == 'SELECT':
            self.verifica_token('SELECT')
            self.REGRA_SELECT()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        # "update" REGRA_UPDATE;
        elif self.next_token.upper() == 'UPDATE':
            self.verifica_token('UPDATE')
            self.REGRA_UPDATE()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        # "delete" REGRA_DELETE;
        elif self.next_token.upper() == 'DELETE':
            self.verifica_token('DELETE')
            self.REGRA_DELETE()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        # "truncate" REGRA_TRUNCATE;
        elif self.next_token.upper() == 'TRUNCATE':
            self.verifica_token('TRUNCATE')
            self.REGRA_TRUNCATE()
            self.verifica_token(';')
            self.REGRA_COMANDO()
        else:
            return