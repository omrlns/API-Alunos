import os, re, csv
from datetime import datetime
from functools import reduce

CSV_FILE = 'registros.csv'

def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def exibirMenu():
    print('=' * 15 + ' MENU ' + '=' * 15)
    print('''
    [ 1 ] - CADASTRAR ALUNO
    [ 2 ] - LISTAR ALUNOS
    [ 3 ] - PESQUISAR ALUNO POR NOME
    [ 4 ] - QUANTIDADE DE ALUNOS CADASTRADOS
    [ 5 ] - SAIR
    ''')

def selecionarMenu():
    limparTela()
    exibirMenu()

    while True:
        try:
            opcao = int(input('ESCOLHA UMA OPÇÃO PARA PROSSEGUIR: '))
            if (opcao >= 1 and opcao <= 5):
                return opcao
            else:
                print('OPÇÃO INVÁLIDA! POR FAVOR, ESCOLHA UMA DAS OPÇÕES DO MENU.')
        except ValueError:
            print('ENTRADA INVÁLIDA! POR FAVOR, DIGITE UM NÚMERO.')

def capturarDados():
    limparTela()
    
    print('=' * 10 + ' FORMULÁRIO DE CADASTRO DE ALUNO ' + '=' * 10)
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

    if not nome:
        erros.append('"NOME" NÃO PODE SER VAZIO!')

    try:
        valorNascimento = datetime.strptime(nascimento, '%d/%m/%Y')
        if (valorNascimento > datetime.now()):
            erros.append('"DATA DE NASCIMENTO" NÃO PODE SER NO FUTURO!')
    except ValueError:
        erros.append('FORMATO DE "DATA DE NASCIMENTO" INVÁLIDO! USE DD/MM/AAAA.')

    if not matricula:
        erros.append('"MATRÍCULA" NÃO PODE SER VAZIA!')

    emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(emailRegex, email):
        erros.append('FORMATO DE "E-MAIL" INVÁLIDO!')

    if not senha:
        erros.append('"SENHA" NÃO PODE SER VAZIA!')

    if erros: 
        return False, '\nERROS NA VALIDAÇÃO DOS DADOS:\n' + '\n'.join(erros)
    else:
        return True, '\nDADOS VALIDADOS COM SUCESSO!'
    
def carregarAlunosCSV():
    alunos = []
    if not os.path.exists(CSV_FILE):
        return alunos

    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            alunos.append(row)
    return alunos

def salvarAlunoCSV(aluno):
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        fieldnames = ['nome', 'nascimento', 'matricula', 'email', 'senha']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        writer.writerow(aluno)

def cadastrar(dadosAlunos):
    print('\n' + '=' * 10 + ' PROCESSO DE CADASTRO ' + '=' * 10)
    print('NOME: {}'.format(dadosAlunos['nome']))
    print('DATA DE NASCIMENTO: {}'.format(dadosAlunos['nascimento']))
    print('MATRÍCULA: {}'.format(dadosAlunos['matricula']))
    print('E-MAIL: {}'.format(dadosAlunos['email']))     
    print('SENHA: {}'.format(dadosAlunos['senha']))

    alunosExistentes = carregarAlunosCSV()

    for registroExistente in alunosExistentes:
        if registroExistente['matricula'] == dadosAlunos['matricula']:
            print(f'\nERRO: Matrícula {dadosAlunos["matricula"]} já cadastrada!')
            return False

    for registroExistente in alunosExistentes:
        if registroExistente['email'] == dadosAlunos['email']:
            print(f'\nERRO: E-mail {dadosAlunos["email"]} já cadastrado!')
            return False

    salvarAlunoCSV(dadosAlunos)
    print('\nCADASTRO ARMAZENADO COM SUCESSO')
    return True

def listarAlunos():
    limparTela()
    alunosCadastrados = carregarAlunosCSV()

    if not alunosCadastrados:
        print('NÃO HÁ NENHUM REGISTRO!')
        input('\nPRESSIONE "ENTER" PARA CONTINUAR...')
        return
    
    print('=' * 10 + ' REGISTROS DE ALUNOS ' + '=' * 10)
    for i, aluno in enumerate(alunosCadastrados):
        print(f'\nALUNO #{i+1}:')
        print('NOME: {}'.format(aluno['nome']))
        print('DATA DE NASCIMENTO: {}'.format(aluno['nascimento']))
        print('MATRÍCULA: {}'.format(aluno['matricula']))
        print('E-MAIL: {}'.format(aluno['email']))     
        print('SENHA: {}'.format(aluno['senha']))

    input('\nPRESSIONE "ENTER" PARA CONTINUAR...')

def pesquisarPorNome():
    limparTela()
    alunos = carregarAlunosCSV()
    if not alunos:
        print('NÃO HÁ NENHUM REGISTRO PARA PESQUISAR!')
        input('\nPRESSIONE "ENTER" PARA CONTINUAR...')
        return

    valorPesquisa = input('DIGITE O NOME OU PARTE DO NOME PARA PESQUISAR: ').strip().lower()
    
    alunosEncontrados = list(filter(lambda aluno: valorPesquisa in aluno['nome'].lower(), alunos))

    if not alunosEncontrados:
        print(f'\nNENHUM REGISTRO ENCONTRADO COM: "{valorPesquisa}".')
    else:
        print(f'\nREGISTRO(S) ENCONTRADO COM "{valorPesquisa}":')
        for i, aluno in enumerate(alunosEncontrados):
            print(f'\nALUNO #{i+1}:')
            print('NOME: {}'.format(aluno['nome']))
            print('DATA DE NASCIMENTO: {}'.format(aluno['nascimento']))
            print('MATRÍCULA: {}'.format(aluno['matricula']))
            print('E-MAIL: {}'.format(aluno['email']))     
            print('SENHA: {}'.format(aluno['senha']))
    
    input('\nPRESSIONE "ENTER" PARA CONTINUAR...')

def contarAlunos():
    limparTela()

    alunos = carregarAlunosCSV()

    if not alunos:
        quantidade = 0
    else:
        quantidade = reduce(lambda contador, aluno: contador + 1, alunos, 0)

    print('=' * 10 + ' QUANTIDADE DE ALUNOS ' + '=' * 10)
    if quantidade == 0:
        print('\nNÃO HÁ NENHUM ALUNO CADASTRADO!.')
    else:
        print(f'\nTOTAL DE ALUNOS CADASTRADOS: {quantidade}')
    
    input('\nPRESSIONE "ENTER" PARA CONTINUAR...')


def executarSistema():

    while True:
        opcao = selecionarMenu()
        if (opcao == 1):
            dadosAlunos = capturarDados()

            valido, mensagem = validarDados(dadosAlunos) 
            if valido:
                if cadastrar(dadosAlunos):
                    print(mensagem)
            else:
                print(mensagem)

            input('\nPRESSIONE "ENTER" PARA CONTINUAR...')

        elif (opcao == 2):
            listarAlunos()
        
        elif (opcao == 3):
            pesquisarPorNome()

        elif (opcao == 4):
            contarAlunos()

        elif (opcao == 5):
            limparTela()
            print('\nSAINDO DO PROGRAMA...')
            break

executarSistema()