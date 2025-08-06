import os, re, csv
from datetime import datetime
import duckdb
from fastapi import FastAPI, HTTPException, Query, Body

CSV_FILE = 'registros.csv'
app = FastAPI() # uvicorn app:app --reload -> para iniciar a aplicação

def limparTela():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def carregarAlunosCSV():
    # carrega todos os alunos do arquivo CSV.
    alunos = []
    if not os.path.exists(CSV_FILE):
        return alunos

    with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            alunos.append(row)
    return alunos

def salvarAlunoCSV(aluno: dict):
    # adiciona um novo aluno ao CSV.
    # carrega todos os alunos existentes, adiciona o novo e reescreve o arquivo.
    alunos = carregarAlunosCSV()
    alunos.append(aluno)
    reescreverCSV(alunos)

def reescreverCSV(alunos: list):
    # reescreve todo o arquivo CSV com a lista de alunos fornecida.
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        header = ['nome', 'nascimento', 'matricula', 'email', 'senha']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(alunos)

def deletarAlunoCSV(matricula: str):
    # deleta um aluno existente pela matrícula.
    # retorna True se o aluno foi encontrado e deletado, False caso contrário.
    alunos = carregarAlunosCSV()
    alunosFiltrados = [aluno for aluno in alunos if aluno.get('matricula') != matricula]
    if len(alunosFiltrados) < len(alunos): # se algum aluno foi removido
        reescreverCSV(alunosFiltrados)
        return True
    return False

def atualizarAlunoCSV(matricula: str, dadosAtualizados: dict):
    # atualiza os dados de um aluno existente pela matrícula.
    # retorna True se o aluno foi encontrado e atualizado, False caso contrário.

    alunos = carregarAlunosCSV()
    encontrado = False
    for i, aluno in enumerate(alunos):
        if aluno.get('matricula') == matricula:
            # atualiza apenas os campos fornecidos em dados_atualizados
            for key, value in dadosAtualizados.items():
                if key in aluno: # garante que apenas campos válidos sejam atualizados
                    alunos[i][key] = value
            encontrado = True
            break
    if encontrado:
        reescreverCSV(alunos)
        return True
    return False

def validarDados(dadosAlunos):
    erros = []

    if not dadosAlunos.get('nome'):
        erros.append('"NOME" NÃO PODE SER VAZIO!')

    nascimento = dadosAlunos.get('nascimento')
    if not nascimento:
        erros.append('"DATA DE NASCIMENTO" NÃO PODE SER VAZIA!')
    else:
        try:
            valorNascimento = datetime.strptime(nascimento, '%d/%m/%Y')
            if (valorNascimento > datetime.now()):
                erros.append('"DATA DE NASCIMENTO" NÃO PODE SER NO FUTURO!')
        except ValueError:
            erros.append('FORMATO DE "DATA DE NASCIMENTO" INVÁLIDO! USE DD/MM/AAAA.')

    if not dadosAlunos.get('matricula'):
        erros.append('"MATRÍCULA" NÃO PODE SER VAZIA!')

    email = dadosAlunos.get('email')
    if not email:
        erros.append('"E-MAIL" NÃO PODE SER VAZIO!')
    else:
        emailRegex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(emailRegex, email):
            erros.append('FORMATO DE "E-MAIL" INVÁLIDO!')

    if not dadosAlunos.get('senha'):
        erros.append('"SENHA" NÃO PODE SER VAZIA!')

    return erros # retorna a lista de erros

def executarQueryDUCKDB(queryTemplate: str, **kwargs) -> list:
    # função auxiliar para executar queries no DuckDB
    try:
        con = duckdb.connect(database=':memory:', read_only=False)
        columns_schema = "{'nome': 'VARCHAR', 'nascimento': 'VARCHAR', 'matricula': 'VARCHAR', 'email': 'VARCHAR', 'senha': 'VARCHAR'}"
        
        # formata a query usando o template e os argumentos adicionais
        query = queryTemplate.format(csv_file=CSV_FILE, columns_schema=columns_schema, **kwargs)
        
        result = con.execute(query).fetchall()
        con.close()
        return result
    except duckdb.CatalogException:
        # significa que o arquivo CSV não existe ou está vazio
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'ERRO INTERNO DO BANCO DE DADOS: {e}')

@app.post('/alunos')
async def cadastrar(dadosAlunos: dict):

    erros = validarDados(dadosAlunos)
    if erros:
        raise HTTPException(status_code=400, detail=', '.join(erros))

    alunosExistentes = carregarAlunosCSV()
    for registroExistente in alunosExistentes: 
        if registroExistente.get('matricula') == dadosAlunos.get('matricula'):
            raise HTTPException(status_code=409, detail=f'ERRO: MATRÍCULA {dadosAlunos.get('matricula')} JÁ CADASTRADA!')
        if registroExistente.get('email') == dadosAlunos.get('email'):
            raise HTTPException(status_code=409, detail=f'ERRO: "E-MAIL" {dadosAlunos.get('email')} JÁ CADASTRADO!')
    
    salvarAlunoCSV(dadosAlunos)
    return {'mensagem': 'CADASTRO ARMAZENADO COM SUCESSO!'}

@app.get('/alunos')
async def listar_alunos(nome: str = Query(None, description='PESQUISAR POR PARTE DO NOME')):
    baseQueryTemplate = """
        SELECT nome, nascimento, matricula, email, senha
        FROM READ_CSV_AUTO('{csv_file}', HEADER=true, ENCODING='UTF-8', columns = {columns_schema})
    """
    
    if nome:
        queryFinalTemplate = baseQueryTemplate + " WHERE LOWER(nome) LIKE '%{nomeParams}%';"
        alunosEncontrados = executarQueryDUCKDB(queryFinalTemplate, nomeParams=nome.lower())
    else:
        queryFinalTemplate = baseQueryTemplate + ';'
        alunosEncontrados = executarQueryDUCKDB(queryFinalTemplate)
    
    if not alunosEncontrados and nome:
        raise HTTPException(status_code=404, detail=f"NENHUM REGISTRO ENCONTRADO COM: '{nome}'.")
    elif not alunosEncontrados:
        return [] # retorna lista vazia se não há alunos e não houve pesquisa

    # converte a lista de tuplas para uma lista de dicionários
    # nomes das chaves dos dicionários formatados permanecem padrão JSON para consumo da API
    alunosFormatados = []
    for alunoT in alunosEncontrados:
        alunosFormatados.append({
            'nome': alunoT[0],
            'nascimento': alunoT[1],
            'matricula': alunoT[2],
            'email': alunoT[3],
            'senha': alunoT[4]
        })
    return alunosFormatados

@app.get('/alunos/count')
async def contarAlunos():
    query_template = """
        SELECT COUNT(*)
        FROM READ_CSV_AUTO('{csv_file}', HEADER=true, ENCODING='UTF-8', columns = {columns_schema});
    """
    quantidade = executarQueryDUCKDB(query_template)[0][0]
    return {'TOTAL DE ALUNOS CADASTRADOS': quantidade}

@app.get('/alunos/maiores')
async def listarAlunosMaioresDeIdade():
    queryTemplate = """
        SELECT nome, nascimento, matricula, email, senha
        FROM READ_CSV_AUTO('{csv_file}', HEADER=true, ENCODING='UTF-8', columns = {columns_schema})
        WHERE AGE(STRPTIME(nascimento, '%d/%m/%Y')) >= INTERVAL '18 year';
    """
    alunosEncontrados = executarQueryDUCKDB(queryTemplate)
    if not alunosEncontrados:
        raise HTTPException(status_code=404, detail='NENHUM ALUNO MAIOR DE 18 ANOS ENCONTRADO.')
    
    alunosFormatados = []
    for alunoT in alunosEncontrados:
        alunosFormatados.append({
            'nome': alunoT[0],
            'nascimento': alunoT[1],
            'matricula': alunoT[2],
            'email': alunoT[3],
            'senha': alunoT[4]
        })
    return alunosFormatados

@app.get('/aniversarios')
async def listarAniversariantesHoje():
    queryTemplate = """
        SELECT nome, nascimento, matricula, email, senha
        FROM READ_CSV_AUTO('{csv_file}', HEADER=true, ENCODING='UTF-8', columns = {columns_schema})
        WHERE STRFTIME(STRPTIME(nascimento, '%d/%m/%Y'), '%m-%d') = STRFTIME(CURRENT_DATE, '%m-%d');
    """
    alunosEncontrados = executarQueryDUCKDB(queryTemplate)
    if not alunosEncontrados:
        raise HTTPException(status_code=404, detail='NENHUM ALUNO FAZ ANIVERSÁRIO HOJE.')
    
    # mapeando apenas nome e nascimento
    aniversariantes = list(map(lambda aluno: {'nome': aluno[0], 'nascimento': aluno[1]}, alunosEncontrados))
    return aniversariantes

@app.put('/alunos/{matricula}')
async def atualizarAlunoCompleto(matricula: str, novosDados: dict):
    erros = validarDados(novosDados)
    if erros:
        raise HTTPException(status_code=400, detail=', '.join(erros))

    alunos = carregarAlunosCSV()
    alunoEncontrado = False

    for i, aluno in enumerate(alunos):
        if aluno['matricula'] == matricula:
            alunoEncontrado = True
            # verifica se novo e-mail pertence a outro aluno
            for outro in alunos:
                if outro['email'] == novosDados['email'] and outro['matricula'] != matricula:
                    raise HTTPException(status_code=409, detail=f'"E-MAIL" {novosDados["email"]} JÁ ESTÁ EM USO POR OUTRO ALUNO.')
            alunos[i] = novosDados  # substitui tudo
            break

    if not alunoEncontrado:
        raise HTTPException(status_code=404, detail=f'ALUNO COM "MATRÍCULA" {matricula} NÃO ENCONTRADO.')

    # reescreve o CSV com os dados atualizados
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        header = ['nome', 'nascimento', 'matricula', 'email', 'senha']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        writer.writerows(alunos)

    return {'mensagem': 'DADOS DO ALUNO ATUALIZADOS COM SUCESSO!'}

@app.patch('/alunos/{matricula}')
async def atualizarAlunoParcial(matricula: str, dadosAtualizados: dict = Body(...)):
    # endpoint para atualização parcial dos dados de um aluno.
    # apenas os campos fornecidos no corpo da requisição serão atualizados.

    alunos = carregarAlunosCSV()
    alunoEncontrado = next((a for a in alunos if a.get('matricula') == matricula), None)

    if not alunoEncontrado:
        raise HTTPException(status_code=404, detail=f'ALUNO COM "MATRÍCULA" {matricula} NÃO ENCONTRADO.')
    
    # validação de e-mail e matrícula duplicados para os dados atualizados
    for key, value in dadosAtualizados.items():
        if key == 'email' and value:
            for aluno in alunos:
                if aluno.get('matricula') != matricula and aluno.get('email') == value:
                    raise HTTPException(status_code=409, detail=f'ERRO: "E-MAIL" {value} JÁ CADASTRADO PARA OUTRO ALUNO!')
        if key == 'matricula' and value and value != matricula:
            for aluno in alunos:
                if aluno.get('matricula') == value:
                    raise HTTPException(status_code=409, detail=f'ERRO: "MATRÍCULA" {value} JÁ CADASTRADA!')
    
    if atualizarAlunoCSV(matricula, dadosAtualizados):
        return {'mensagem': f'ALUNO COM MATRÍCULA {matricula} ATUALIZADO COM SUCESSO!'}
    else:
        # isso não deve acontecer se a verificação acima for bem-sucedida, mas é um fallback seguro.
        raise HTTPException(status_code=500, detail='ERRO AO ATUALIZAR ALUNO.')
    
@app.delete('/alunos/{matricula}')
async def deletarAluno(matricula: str):
    # endpoint para deletar um aluno pela matrícula.
    alunos = carregarAlunosCSV()
    alunoEncontrado = next((a for a in alunos if a.get('matricula') == matricula), None)

    if not alunoEncontrado:
        raise HTTPException(status_code=404, detail=f'ALUNO COM MATRÍCULA {matricula} NÃO ENCONTRADO.')
    
    if deletarAlunoCSV(matricula):
        return {'mensagem': f'ALUNO COM MATRÍCULA {matricula} DELETADO COM SUCESSO!'}
    else:
        raise HTTPException(status_code=500, detail='ERRO AO DELETAR ALUNO.')