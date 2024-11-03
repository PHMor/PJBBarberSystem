from datetime import datetime, timedelta
import os
import json
clear = lambda: os.system('cls')
if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/dados.json'):
    True
else:
    dados = {
    "clientes" : [],
    "caixadiario" : {},
    "dias_com_horarios" : {}
    }
    with open("dados.json", "w") as arquivo:
        json.dump(dados, arquivo)

with open("dados.json", "r") as arquivo:
    dados_carregados = json.load(arquivo)

def salvar_dados(clientes,caixadiario,dias_com_horarios):
    clientes_ps =  [cliente.viradici() for cliente in clientes]
    dias_ps = {
        data:{
            numero: [marcado.viradici() for marcado in horarios]
            for numero, horarios in horarios_dia.items()
        }
        for data, horarios_dia in dias_com_horarios.items()
    }
    
    dados = {
    "clientes" : clientes_ps,
    "caixadiario" : caixadiario,
    "dias_com_horarios" : dias_ps
    }
    
    with open("dados.json", "w") as arquivo:
        json.dump(dados, arquivo)
        
caixadiario = dados_carregados["caixadiario"]

def validar_data(data_str):
    try:
        data_str = datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False
def validar_cpf_e_numero(cpf):
    return len(cpf) == 11 and cpf.isdigit()
def validar_nome(nome):
    return all(caractere.isalpha() or caractere.isspace() for caractere in nome)

class cadastro:
    def __init__(self,nome,cpf,telefone,endereco,datanasc):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.datanasc = datanasc

    def mostrar_cadastro(self):
        print(f"Nome: {self.nome}\nCpf: {self.cpf}\nFone: {self.telefone}\nEndereço: {self.endereco}\nData de nascimento: {self.datanasc}")
        
    def puxar_nome(self):
        return self.nome
    
    def viradici(self):
        return {
            "nome": self.nome,
            "cpf": self.cpf,
            "telefone": self.telefone,
            "endereco": self.endereco,
            "datanasc": self.datanasc
        }
clientes = []
for dado in dados_carregados["clientes"]:
    cliente = cadastro(dado["nome"],dado["cpf"],dado["telefone"],dado["endereco"],dado["datanasc"])
    clientes.append(cliente)

class horario:
    def __init__(self,hora,data,nome,cod,descricao,sit):
        self.data = data
        self.hora = hora

        self.nome = nome
        self.cod = cod
        self.descricao = descricao
        self.sit = sit
        
    def viradici(self):
        return {
            "hora" : self.hora,
            "data" : self.data,
            "nome" : self.nome,
            "cod" : self.cod,
            "descricao" : self.descricao,
            "sit" : self.sit
        }

    def mostrar_horario(self):
        clear()
        if self.hora <=4:
            hora = f"0{self.hora+7}:00"
        else:
            hora = f"{self.hora+8}:00"
        print("=========================RESUMO=========================")
        print(f"Nome: {self.nome}\nCod: {self.cod}\nData: {self.data}\nHora: {hora}")
        if self.descricao == "1":
            print("Descrição: Cabelo")
        if self.descricao == "2":
            print("Descrição: Barba")
        if self.descricao == "3":
            print("Descrição: Cabelo e barba")
        if self.descricao == "1":
            self.valor = 35
            print("Valor : R$35,00")
        if self.descricao == "2":
            print("Valor : R$25,00")
            self.valor = 25
        if self.descricao == "3":
            print("Valor : R$45,00")
            self.valor = 45
        if self.sit == 0:
            print("Situação: Pendente")
        if self.sit == 1:
            print("Situação: Recebido")
        print("========================================================")
dias_com_horarios = {}

for data in dados_carregados["dias_com_horarios"]:
    for hora in dados_carregados["dias_com_horarios"][data]:
        for dado in dados_carregados["dias_com_horarios"][data][hora]:
            amigo = horario(dado["hora"],dado["data"],dado["nome"],dado["cod"],dado["descricao"],dado["sit"])
            dias_com_horarios[data] = {}
            dias_com_horarios[data][hora] = []
            dias_com_horarios[data][hora].append(amigo)

class produto:
    def __init__(self,nome,preco):
        self.nome = nome
        self.preco = preco

    def mostrar_produto(self):
        print(f"Nome do produto: {self.nome}\nPreço do produto: {self.preco}")
        
class kit(produto):
    def __init__(self,nome,preco,nome2,nome3,preco2,preco3):
        self.nome = nome
        self.preco = preco
        self.nome2 = nome2
        self.preco2 = preco2
        self.preco3 = preco3
        self.nome3 = nome3
    
    def mostrar_kit(self):
        clear()
        print(f"Nome do kit:{self.nome3}")
        print("Produto 1: ")
        super().__init__(self.nome,self.preco)
        super().mostrar_produto()
        print("Produto 2: ")
        super().__init__(self.nome2,self.preco2)
        super().mostrar_produto()
        print(f"Valor do kit: {self.preco3}")
        
produtos = []
kits = []

def cadastro_produto(produtos):
    nome_produto = input("Qual o nome do produto:")
    while True:
        preco_produto = input("Preço do produto: ")
        if preco_produto.isdigit():
            preco_produto = int(preco_produto)
            break
        else:
            print("Valor inválido.")
    prod = produto(nome_produto,preco_produto)
    produtos.append(prod)

def cadastro_kit(produtos,kits):
    nome_kit = input("Nome do kit: ")
    while True:
        cod1 = input("Código do 1º premio: ")
        if cod1.isdigit():
            cod1 = int(cod1)
            if len(produtos) == 0:
                print("Ainda nao possuí nenhum produto cadastrado.")
            else:
                if cod1 <= len(produtos) and cod1 > 0:
                    break
                else:
                    print("Código inválido.")
    while True:
        cod2 = input("Código do 2º premio: ")
        if cod2.isdigit():
            cod2 = int(cod2)
            if len(produtos) == 0:
                print("Ainda nao possuí nenhum produto cadastrado.")
            else:
                if cod2 <= len(produtos) and cod2 > 0 and not cod1 == cod2:
                    break
                else:
                    print("Código inválido.")
    while True:
        preco_kit = input("Preco do kit:")
        if preco_kit.isdigit():
            preco_kit = int(preco_kit)
            break
        else:
            print("Valor inválido.")
    kitp = kit(produtos[cod1-1].nome,produtos[cod1-1].preco,produtos[cod2-1].nome,nome_kit,produtos[cod2-1].preco,preco_kit)
    kits.append(kitp)
    kitp.mostrar_kit()
    input("")

def mostrar_clientes(clientes):
    clear()
    if len(clientes) == 0:
        print("Ainda não possuí nenhum cliente cadastrado.")
    print("Cod | Nome")
    for x in range(len(clientes)):
        print(f"{x+1} | {clientes[x].nome}")
    input("Pressione ENTER para continuar")

def cadastrar(clientes):
    clear()
    while True:
        while True:
            nome = input("Nome: ")
            if validar_nome(nome):
                clear()
                break
            else:
                clear()
                print("Nome inválido. Não utilize números ou símbolos.")
        while True:
            cpf = input("Cpf (Utilize apenas números): ")
            if validar_cpf_e_numero(cpf):
                clear()
                break
            else:
                clear()
                print("CPF inválido. Favor digitar novamente.")
        while True:
            telefone = input("Fone (Modelo: 00992345678): ")
            if validar_cpf_e_numero(telefone):
                clear()
                break
            else:
                clear()
                print("Número inválido. Favor digitar novamente.")
        endereco = input("Endereço completo: ")
        clear()
        while True:
            datanasc = input("Data de nascimento (dd/mm/aaaa): ")
            if validar_data(datanasc):
                clear()
                break
            else:
                clear()
                print("Data inválida. Utilize formato dd/mm/aaaa.")
        
        cliente = cadastro(nome,cpf,telefone,endereco,datanasc)
        clientes.append(cliente)
        clear()
        quer = int(input("Deseja criar outro cadastro?\n[1]Sim\n[0]Não\n"))
        if quer == 0:
            break
        elif quer == 1:
            clear()
            True
        else:
            quer = int(input("Comando incorreto.\nDeseja iniciar um novo cadastro?"))
    salvar_dados(clientes,caixadiario,dias_com_horarios)
    return(clientes)

def marcar_horario(dias_com_horarios,clientes):
    if len(clientes) == 0:
        print("Ainda não possuí nenhum cliente cadastrado.")
        input("Pressione ENTER para continuar")
    else:
        while True:
            cliente = input("Qual cliente deseja marcar? [Q]Visualizar códigos.\n\n")
            if cliente == "q" or cliente == "Q":
                mostrar_clientes(clientes)
            elif cliente.isdigit():
                clienteint = int(cliente)
                if clienteint <= len(clientes) and clienteint > 0:
                    break
            else:
                print("Código de cliente inválido.")
        if cliente.isdigit():
            clienteint = int(cliente)-1
        clear()
        data_atual = datetime.now()
        data_atualstr = data_atual.strftime("%d/%m/%Y")
        dia_atual = data_atual.strftime("%d")
        mes_atual = data_atual.strftime("%m")
        ano_atual = data_atual.strftime("%Y")

        while True:
            data_marcada = input("Data que deseja marcar (dd/mm): ")
            if validar_data(f"{data_marcada}/{ano_atual}"):
                data_marcada = f"{data_marcada}/{ano_atual}"
                data_marcadaobj = datetime.strptime(data_marcada, "%d/%m/%Y")
                data_limite = data_atual + timedelta(days=30)
                if (data_atual < data_marcadaobj or data_marcada == data_atualstr) and data_marcadaobj < data_limite:
                    if data_marcada not in dias_com_horarios:
                        dias_com_horarios[f"{data_marcada}"] = {}
                    break
                else:
                    clear()
                    print("Data inválida. Agende apenas para datas futuras e menores que 30 dias.")
            else:
                clear()
                print("Data inválida. Utilize formato dd/mm.")
        clear()

        while True:
            for x in range(8):
                x += 1
                xstr = f"{x}"
                if xstr not in dias_com_horarios[data_marcada]:
                    if x <=2:
                        xstr = f"0{x+7}:00"
                    elif x <=4:
                        xstr = f"{x+7}:00"
                    else:
                        xstr = f"{x+8}:00"
                    print(f"[{x}] {xstr}")
            horario_marcado = input("Qual horario voce gostaria?")
            if horario_marcado.isdigit():
                horario_marcadoint = int(horario_marcado)
            if horario_marcado.isdigit() and horario_marcadoint > 0 and horario_marcadoint < 9:
                if horario_marcado in dias_com_horarios[data_marcada]:
                    print("Horario ja preenchido")
                else:
                    clear()
                    descricao = input("[1]Cabelo\n[2]Barba\n[3]Cabelo e barba\n\n")
                    nominho = clientes[clienteint].puxar_nome()
                    hora = horario(horario_marcadoint,data_marcada,nominho,clienteint+1,descricao,0)
                    dias_com_horarios[data_marcada][horario_marcado] = []
                    dias_com_horarios[data_marcada][horario_marcado].append(hora)
                    break
            else:
                print("Valor incorreto.")
        dias_com_horarios[data_marcada][horario_marcado][0].mostrar_horario()
        salvar_dados(clientes,caixadiario,dias_com_horarios)
        input("")
        return(dias_com_horarios)

def venderprod(produtos,kits,caixadiario,clientes,dias_com_horarios):
    qual = input("Deseja vender produto ou kit? [1]Produto [2]Kit")
    if qual == "1":
        while True:
            qual = input("Qual produto deseja vender?")
            if qual.isdigit():
                qual = int(qual)
                if qual <= len(produtos) and qual > 0:
                    break
                else:
                    print("Código inválido.")
            else:
                print("Código inválido.")
        clear()
        while True:
            pgmnt = input("Qual a forma de pagamento?\n[1]Dinheiro [2]Crédito [3]Débito [4]Pix")
            if pgmnt.isdigit():
                pgmnt = int(pgmnt)
            if pgmnt > 0 and pgmnt < 5:
                break
            else:
                print("Forma de pagamento inválida.")
        if pgmnt == 1:
            print(f"Valor devido: {produtos[qual-1].preco}")
            while True:
                pago = input(f"Qual valor pago: ")
                if pago.isdigit():
                    pago = int(pago)
                    break
                else:
                    print("Valor incorreto")
            print(f"Troco : {pago - produtos[qual-1].preco}")
        dia = datetime.now()
        dia = dia.strftime("%d/%m/%Y")
        if dia not in caixadiario:
            caixadiario[dia] = {"Dinheiro" : 0,"Credito" : 0, "Debito" : 0,"Pix" : 0}
        if pgmnt == 1:
            caixadiario[dia]["Dinheiro"] += produtos[qual-1].preco
        if pgmnt == 2:
            caixadiario[dia]["Credito"] += produtos[qual-1].preco
        if pgmnt == 3:
            caixadiario[dia]["Debito"] += produtos[qual-1].preco
        if pgmnt == 4:
            caixadiario[dia]["Pix"] += produtos[qual-1].preco
        print("Recebido com sucesso")
        clear()
        print(caixadiario)
        salvar_dados(clientes,caixadiario,dias_com_horarios)
        input("Pressione ENTER para continuar")
        return(caixadiario)
    elif qual == "2":
        while True:
            qual = input("Qual kit deseja vender?")
            if qual.isdigit():
                qual = int(qual)
                if qual <= len(kits) and qual > 0:
                    break
                else:
                    print("Código inválido.")
            else:
                print("Código inválido.")
        clear()
        while True:
            pgmnt = input("Qual a forma de pagamento?\n[1]Dinheiro [2]Crédito [3]Débito [4]Pix")
            if pgmnt.isdigit():
                pgmnt = int(pgmnt)
            if pgmnt > 0 and pgmnt < 5:
                break
            else:
                print("Forma de pagamento inválida.")
        if pgmnt == 1:
            print(f"Valor devido: {kits[qual-1].preco3}")
            while True:
                pago = input(f"Qual valor pago: ")
                if pago.isdigit():
                    pago = int(pago)
                    break
                else:
                    print("Valor incorreto")
            print(f"Troco : {pago - kits[qual-1].preco3}")
        dia = datetime.now()
        dia = dia.strftime("%d/%m/%Y")
        if dia not in caixadiario:
            caixadiario[dia] = {"Dinheiro" : 0,"Credito" : 0, "Debito" : 0,"Pix" : 0}
        if pgmnt == 1:
            caixadiario[dia]["Dinheiro"] += kits[qual-1].preco3
        if pgmnt == 2:
            caixadiario[dia]["Credito"] += kits[qual-1].preco3
        if pgmnt == 3:
            caixadiario[dia]["Debito"] += kits[qual-1].preco3
        if pgmnt == 4:
            caixadiario[dia]["Pix"] += kits[qual-1].preco3
        print("Recebido com sucesso")
        clear()
        print(caixadiario)
        salvar_dados(clientes,caixadiario,dias_com_horarios)
        input("Pressione ENTER para continuar")
        return(caixadiario)
    else:
        print("Inválido")
        input("")

def receber(caixadiario,dias_com_horarios):
    clear()
    dia = datetime.now()
    dia = dia.strftime("%d/%m/%Y")
    if dia in dias_com_horarios:
        print("Horarios marcados nesse dia:")
        for chavestr in dias_com_horarios[dia].keys():
            chave = int(chavestr)
            if dias_com_horarios[dia][chavestr][0].sit == 0:
                sit = "Em aberto"
            if dias_com_horarios[dia][chavestr][0].sit == 1:
                sit = "Recebido"
            if chave <=4:
                chaveh = f"0{chave+7}:00 [{sit}]"
            else:
                chaveh = f"0{chave+8}:00 [{sit}]"
            print(f"[{chave}]{chaveh}")
        hora = input("\nQual hora deseja receber?")
        if hora in dias_com_horarios[dia]:
            if dias_com_horarios[dia][hora][0].sit == 0:
                dias_com_horarios[dia][hora][0].mostrar_horario()
                while True:
                    clear()
                    pgmnt = input("Qual a forma de pagamento?\n[1]Dinheiro [2]Crédito [3]Débito [4]Pix")
                    if pgmnt.isdigit():
                        pgmnt = int(pgmnt)
                    if pgmnt > 0 and pgmnt < 5:
                        break
                    else:
                        print("Forma de pagamento inválida.")
                if pgmnt == 1:
                    print(f"Valor devido: {dias_com_horarios[dia][hora][0].valor}")
                    while True:
                        pago = input(f"Qual valor pago: ")
                        if pago.isdigit():
                            pago = int(pago)
                            break
                        else:
                            print("Valor incorreto")
                    print(f"Troco : {pago - dias_com_horarios[dia][hora][0].valor}")
                if dia not in caixadiario:
                    caixadiario[dia] = {"Dinheiro" : 0,"Credito" : 0, "Debito" : 0,"Pix" : 0}
                if pgmnt == 1:
                    caixadiario[dia]["Dinheiro"] += dias_com_horarios[dia][hora][0].valor
                if pgmnt == 2:
                    caixadiario[dia]["Credito"] += dias_com_horarios[dia][hora][0].valor
                if pgmnt == 3:
                    caixadiario[dia]["Debito"] += dias_com_horarios[dia][hora][0].valor
                if pgmnt == 4:
                        caixadiario[dia]["Pix"] += dias_com_horarios[dia][hora][0].valor
                dias_com_horarios[dia][hora][0].sit = 1
                salvar_dados(clientes,caixadiario,dias_com_horarios)
                print("Recebido com sucesso")
                input("Pressione ENTER para continuar")
            else:
                print("Já recebido.")
                input("Pressione ENTER para continuar")
        else:
            print("Não possui nada marcado nesse horário.")
            input("Pressione ENTER para continuar")
    else:
        print("Não possui horários marcados nesse dia.")
        input("Pressione ENTER para continuar")

while True:
    clear()
    print("=============================POS============================\n[11]Marcar horário\n[12]Verificar horários\n[13]Excluir horário\n[14]Receber")
    print("====================CONFIGURAR CADASTROS====================\n[21]Cadastrar Cliente\n[22]Consultar cliente\n[23]Verificar códigos\n[24]Remover cadastro")
    print("=========================RELATÓRIOS=========================\n[31]Relatório de caixa")
    print("\n\n[X]Fechar sistema")
    menu = input("Digite a opção: ")
    if menu == "11":
        clear()
        dias_com_horarios = marcar_horario(dias_com_horarios,clientes)
    elif menu == "12":
        clear()
        dia = input("Qual dia deseja verificar? (dd/mm/aaaa)\n\n")
        if validar_data(dia):
            if dia in dias_com_horarios:
                print("Horarios marcados nesse dia:")
                for chave in dias_com_horarios[dia].keys():
                    chavestr = f"{chave}"
                    chave = int(chave)
                    if chave <=4:
                        chaveh = f"0{chave+7}:00 [Cliente: {dias_com_horarios[dia][chavestr][0].nome}]"
                    else:
                        chaveh = f"{chave+8}:00 [Cliente: {dias_com_horarios[dia][chavestr][0].nome}]"
                    print(f"[{chave}]{chaveh}")
                hora = input("\nQual hora deseja verificar?")
                if hora in dias_com_horarios[dia]:
                    dias_com_horarios[dia][hora][0].mostrar_horario()
                    input("Pressione ENTER para continuar")
                else:
                    print("Não possui nada marcado nesse horário.")
                    input("Pressione ENTER para continuar")
            else:
                print("Não possui horários marcados nesse dia.")
                input("Pressione ENTER para continuar")
        else:
            clear()
            print("Data inválida. Utilize formato dd/mm/aaaa.")
    elif menu == "13":
        clear()
        dia = input("Qual dia deseja excluir? (dd/mm/aaaa)\n\n")
        if validar_data(dia):
            if dia in dias_com_horarios:
                print("Horarios marcados nesse dia:")
                for chave in dias_com_horarios[dia].keys():
                    chave = int(chave)
                    if chave <=4:
                        chaveh = f"0{chave+7}:00 "
                    else:
                        chaveh = f"0{chave+8}:00"
                    print(f"[{chave}]{chaveh}")
                hora = input("\nQual hora deseja verificar?")
                if hora in dias_com_horarios[dia]:
                    if dias_com_horarios[dia][hora][0].sit == 0:
                        dias_com_horarios[dia][hora][0].mostrar_horario()
                        confirmar = input("Para confirmar a exclusão digite 'EXCLUIR'")
                        if confirmar == "EXCLUIR":
                            dias_com_horarios[dia][hora][0].pop
                            print("Horário excluido com sucesso")
                            input("Pressione ENTER para continuar")
                        else:
                            print("Digitação incorreta.")
                            input("Pressione ENTER para continuar")
                    else:
                        print("Impossível excluir um horário ja recebido.")
                        input("Pressione ENTER para continuar")
                else:
                    print("Não possui nada marcado nesse horário.")
                    input("Pressione ENTER para continuar")
            else:
                print("Não possui horários marcados nesse dia.")
                input("Pressione ENTER para continuar")
        else:
            clear()
            print("Data inválida. Utilize formato dd/mm/aaaa.")
    elif menu == "14":
        receber(caixadiario,dias_com_horarios)
    elif menu == "15":
        cadastro_produto(produtos)
    elif menu == "16":
        cadastro_kit(produtos,kits)
    elif menu == "17":
        caixadiario = venderprod(produtos,kits,caixadiario,clientes,dias_com_horarios)
    elif menu == "21":
        clientes = cadastrar(clientes)
    elif menu == "22":
        if len(clientes) == 0:
            clear()
            print("Ainda não possuí nenhum cliente cadastrado.")
            input("Pressione ENTER para continuar")
        else:
            while True:
                clear()
                escolha = input(f"Qual código do cliente que deseja consultar? [1 - {len(clientes)}]")
                if escolha.isdigit():
                    escolha = int(escolha)
                    if escolha <= len(clientes) and escolha > 0:
                        clear()
                        clientes[escolha-1].mostrar_cadastro()
                        input("Pressione ENTER para continuar")
                        break
                    else:
                        print("Código inválido.")
                        input("Pressione ENTER para continuar")
                else:
                        print("Código inválido.")
                        input("Pressione ENTER para continuar")
    elif menu == "23":
        mostrar_clientes(clientes)
    elif menu == "24":
        clear()
        if len(clientes) == 0:
            print("Ainda não possuí nenhum cliente cadastrado.")
            input("Pressione ENTER para continuar")
        else:
            while True:
                clear()
                cod = input("Qual o código do cliente que deseja remover?")
                if cod.isdigit():
                    cod = int(cod)
                    if cod <= len(clientes) and cod>0:
                        clientes.pop(cod-1)
                        break
                    else:
                        print("Código inválido.")
                        input("Pressione ENTER para continuar")
                else:
                    print("Código inválido.")
                    input("Pressione ENTER para continuar")
    elif menu == "31":
        while True:
            clear()
            dia = input("Qual dia você deseja tirar o relatório? (dd/mm/aaaa)")
            receb = 0
            if validar_data(dia):
                if dia in caixadiario:
                    if not len(dias_com_horarios) == 0:
                        print("==========================HORARIOS==========================")
                        print(f"Horarios marcados: {len(dias_com_horarios[dia])}")
                        for hora in dias_com_horarios[dia]:
                            if dias_com_horarios[dia][hora][0].sit == 1:
                                receb += 1
                        print(f"Horarios vazios: {8-len(dias_com_horarios[dia])}")
                        print(f"Horarios recebidos: {receb}")
                        print(f"Horarios com falta: {len(dias_com_horarios[dia])-receb}")
                    else:
                        print("===========================VALORES==========================")
                        for forma in caixadiario[dia]:
                            print(f"{forma}: {caixadiario[dia][forma]}")
                        input("Pressione ENTER para continuar")
                    break
                else:
                    print("Não possuí vendas nesse dia.")
                    input("Pressione ENTER para continuar")
                    break
            else:
                print("Data incorreta. Utilize dd/mm/aaaa")
                input("Pressione ENTER para continuar")
    elif menu == "X" or menu == "x":
        print("Fechando sistema")
        break
    else:
        print("Comando inválido.")
        input("Pressione ENTER para continuar")
