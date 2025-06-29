import os, re
from datetime import datetime

alunosCadastrados = []

def limparTela():
    os.system('cls')

def exibirMenu():
    print('=' * 15  + ' MENU ' + '=' * 15)
    print('''
    [ 1 ] - CADASTRAR ALUNO
    [ 2 ] - LISTAR ALUNOS
    [ 3 ] - SAIR
    ''')

def selecionarMenu():
    limparTela()
    exibirMenu()

    while True:
        try:
            opcao = int(input('ESCOLHA UMA OPÇÃO PARA PROSSEGUIR: '))
            if (opcao >= 1 and opcao <= 3):
                return opcao
            else:
                print('OPÇÃO INVÁLIDA! POR FAVOR, ESCOLHA 1, 2 OU 3.')
        except ValueError:
            print('ENTRADA INVÁLIDA! POR FAVOR, DIGITE UM NÚMERO.')


def capturarDados():
    limparTela()
    
    print('=' * 10  + ' FORMULÁRIO DE CADASTRO DE ALUNO ' + '=' * 10)
    nome = str(input('NOME: ')).strip()
    nascimento = str(input('DATA DE NASCIMENTO: ')).strip()
    matricula = str(input('MATRÍCULA: ')).strip()
    email = str(input('E-MAIL: ')).strip()
    senha = str(input('SENHA: ')).strip()
    return nome, nascimento, matricula, email, senha
    
def validarDados(nome, nascimento, matricula, email, senha):
    erros = []

    # validação do nome
    # verificando se a variável "nome" está vazia
    if not nome.strip(): # .strip() remove os espaços em branco do início e fim
        erros.append('"NOME" NÃO PODE SER VAZIO!')

    # validação da data de nascimento
    try:
        valorNascimento = datetime.strptime(nascimento, '%d/%m/%Y') # '%d/%m/%Y' é o formato esperado para DD/MM/AAAA

        if (valorNascimento > datetime.now()):
            erros.append('"DATA DE NASCIMENTO" NÃO PODE SER NO FUTURO!')

    except ValueError:
        erros.append('FORMATO DE "DATA DE NASCIMENTO" INVÁLIDO! USE DD/MM/AAAA.')

    # validação da matrícula
    if not matricula.strip():
        erros.append('"MATRÍCULA" NÃO PODE SER VAZIA!')
    # verifica se a matrícula informada já existe na lista de cadastro
    for aluno in alunosCadastrados:
        if aluno['matricula'] == matricula:
            erros.append('"MATRÍCULA" {} JÁ CADASTRADA!'.format(matricula))

    # validação do email
    # regex para validação de e-mail com um padrão básico, como caracteres@caracteres.domínio
    emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(emailRegex, email):
        erros.append('FORMATO DE "E-MAIL" INVÁLIDO!')
    # verifica se o e-mail informado já existe na lista de cadastro
    for aluno in alunosCadastrados:
        if aluno['email'] == email:
            erros.append('"E-MAIL" {} JÁ CADASTRADO!'.format(email))

     # validação da senha
    if not senha.strip():
        erros.append('"SENHA" NÃO PODE SER VAZIA!')

    # retorno da validação
    if erros: 
        return False, '\nDADOS INVÁLIDOS: \n' + '\n'.join(erros)
    else:
        return True, '\nDADOS VALIDADOS COM SUCESSO!'
    
def cadastrar(nome, nascimento, matricula, email, senha):
    print('\n' + '=' * 10  + ' PROCESSO DE CADASTRO ' + '=' * 10)
    print('NOME: {}'.format(nome))
    print('DATA DE NASCIMENTO: {}'.format(nascimento))
    print('MATRÍCULA: {}'.format(matricula))
    print('E-MAIL: {}'.format(email))    
    print('SENHA: {}'.format(senha))

def armazenar(nome, nascimento, matricula, email, senha):
    aluno = {
        'nome': nome,
        'nascimento': nascimento,
        'matricula': matricula,
        'email': email,
        'senha': senha
    }

    alunosCadastrados.append(aluno)
    print('\nCADASTRO ARMAZENADO COM SUCESSO')

def listarAlunos():
    limparTela()

    if not alunosCadastrados:
        print('NÃO HÁ NENHUM REGISTRO!')
        input('\nPRESSIONE "ENTER" PARA CONTINUAR...')
        return
    
    for i, aluno in enumerate(alunosCadastrados):
        print('=' * 10  + ' REGISTROS ' + '=' * 10)
        print(f'\aALUNO #{i+1}:')
        print('NOME: {}'.format(aluno['nome']))
        print('DATA DE NASCIMENTO: {}'.format(aluno['nascimento']))
        print('MATRÍCULA: {}'.format(aluno['matricula']))
        print('E-MAIL: {}'.format(aluno['email']))    
        print('SENHA: {}'.format(aluno['senha']))

    input('\nPRESSIONE "ENTER" PARA CONTINUAR...')

def executarSistema():

    while True:
        opcao = selecionarMenu()
        if (opcao == 1): # cadastrar aluno
            nome, nascimento, matricula, email, senha = capturarDados()

            # validar dados
            valido = validarDados(nome, nascimento, matricula, email, senha)
            if valido:
                cadastrar(nome, nascimento, matricula, email, senha)
                armazenar(nome, nascimento, matricula, email, senha)
            else:
                print('\nCADASTRO NÃO REALIZADO DEVIDO A ERROS NOS DADOS!')

            input('\nPRESSIONE "ENTER" PARA CONTINUAR...')

        # listar os alunos
        elif (opcao == 2):
            listarAlunos()
        
        elif (opcao == 3):
            limparTela()
            print('\nSAINDO DO PROGRAMA...')
            break

executarSistema()