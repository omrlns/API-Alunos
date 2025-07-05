import os, re, csv
from datetime import datetime

CSV_FILE = 'registros.csv'

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
    nascimento = str(input('DATA DE NASCIMENTO (DD/MM/AAAA): ')).strip()
    matricula = str(input('MATRÍCULA: ')).strip()
    email = str(input('E-MAIL: ')).strip()
    senha = str(input('SENHA: ')).strip()
    
    dadosAlunos = {
        'nome': nome,
        'nascimento': nascimento,
        'matricula': matricula,
        'email': email,
        'senha': senha
        }
    
    return dadosAlunos

def validarDados(dadosAlunos):
    erros = []

    nome = dadosAlunos['nome']
    nascimento = dadosAlunos['nascimento']
    matricula = dadosAlunos['matricula']
    email = dadosAlunos['email']
    senha = dadosAlunos['senha']

    # validação do nome
    # verificando se a variável "nome" está vazia
    if not nome: # .strip() remove os espaços em branco do início e fim
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

    # validação do email
    # regex para validação de e-mail com um padrão básico, como caracteres@caracteres.domínio
    emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(emailRegex, email):
        erros.append('FORMATO DE "E-MAIL" INVÁLIDO!')

     # validação da senha
    if not senha.strip():
        erros.append('"SENHA" NÃO PODE SER VAZIA!')

    # retorno da validação
    if erros: 
        return False, '\nDADOS INVÁLIDOS: \n' + '\n'.join(erros)
    else:
        return True, '\nDADOS VALIDADOS COM SUCESSO!'

def carrgarAlunoCSV():
    alunos = []
    
    if not os.path.exists(CSV_FILE):
        return alunos # se não existir, o sistema vai retornar uma lista vazia
    
    with open(CSV_FILE, mode = 'r', newline = '', encoding = 'utf-8') as file:
        reader = csv.DictReader(file) #lê o csv como dicionários
        for row in reader:
            alunos.append(row)
    return alunos

def salvarAlunoCSV(aluno):
    # verifica se o arquivo já existe para saber se precisa escrever o cabeçalho
    fileExists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, mode = 'a', newline = '', encoding = 'utf-8') as file:
        # define os nomes dos campos (cabeçalhos) para o CSV
        fieldnames = ['nome', 'nascimento', 'matricula', 'email', 'senha']
        writer = csv.DictWriter(file, fieldnames = fieldnames)

        # se o arquivo não existe, escreve a linha do cabeçalho
        if not fileExists:
            writer.writeheader()

        writer.writerow(aluno) # escreve o dicionário do aluno como uma linha no CSV

def cadastrar(dadosAlunos):
    print('\n' + '=' * 10  + ' PROCESSO DE CADASTRO ' + '=' * 10)
    print('NOME: {}'.format(dadosAlunos['nome']))
    print('DATA DE NASCIMENTO: {}'.format(dadosAlunos['nascimento']))
    print('MATRÍCULA: {}'.format(dadosAlunos['matricula']))
    print('E-MAIL: {}'.format(dadosAlunos['email']))    
    print('SENHA: {}'.format(dadosAlunos['senha']))

    alunosExistentes = carrgarAlunoCSV() # carrega os alunos existentes para verificar a duplicidade antes de salvar

    # validação de duplicidade de matricula e email
    for alunoExistente in alunosExistentes:
        if alunoExistente['matricula'] == dadosAlunos['matricula']:
            print('\nERRO: MATRÍCULA {} JÁ CADASTRADA!'.format(dadosAlunos['matricula']))
            return False # retorna falso para indicar falha no cadastro
    for alunoExistente in alunosExistentes:
        if alunoExistente['email'] == dadosAlunos['email']:
            print('\nERRO: E-MAIL {} JÁ CADASTRADO!'.format(dadosAlunos['email']))
            return False # retorna falso para indicar falha no cadastro
        
    salvarAlunoCSV(dadosAlunos) # salva o aluno no CSV
    print('\nCADASTRO REALIZADO COM SUCESSO!')
    return True # retorna true para indicar sucesso no cadastro

def listarAlunos():
    limparTela()

    alunosCadastrados = carrgarAlunoCSV() # carrega os alunos do CSV

    if not alunosCadastrados:
        print('NÃO HÁ NENHUM REGISTRO!')
        input('\nPRESSIONE "ENTER" PARA CONTINUAR...')
        return
    
    print('\n' + '=' * 10  + ' REGISTRO DE ALUNOS ' + '=' * 10)
    for i, aluno in enumerate(alunosCadastrados):
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
            dadosAlunos = capturarDados()

            # validar dados
            valido = validarDados(dadosAlunos)
            if valido:
                cadastrar(dadosAlunos)
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