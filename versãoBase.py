alunos = []

while True:
    print('\n===== MENU =====')
    print('1. cadastrar aluno')
    print('2. listar alunos')
    print('3. sair')
    opcao = input('\nescolha uma opção: ')

    if opcao == '1':
        print('\n----- Cadastro de Aluno -----')
        nome = input('Nome: ')
        nascimento = input('Data de Nascimento (dd/mm/aaaa): ')
        email = input('Email: ')
        senha = input('Senha: ')

        aluno = {'nome': nome, 'nascimento': nascimento, 'email': email, 'senha': senha}

        alunos.append(aluno)
        print('aluno cadastrado com sucesso!')

    elif opcao == '2':
        print('\n--- Lista de Alunos Cadastrados ---')
        if len(alunos) == 0:
            print('nenhum aluno cadastrado.')
        else:
            for i, aluno in enumerate(alunos, start=1):
                print(
                    '{}. Nome: {}, Nascimento: {}, Email: {}'.format(
                        i, aluno['nome'], aluno['nascimento'], aluno['email']
                    )
                )

    elif opcao == '3':
        print('\nsaindo do programa...')
        break

    else:
        print('opção inválida, tente novamente!')