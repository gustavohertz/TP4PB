import json
import pandas as pd
import sqlite3

# Carregar os dados
funcionarios = pd.read_csv('Funcionários - Página1.csv')
cargos = pd.read_csv('Cargos - Página1.csv')
departamentos = pd.read_csv('Departamentos - Página1.csv')
historico_salarios = pd.read_csv('Histórico de Salários - Página1.csv')
dependentes = pd.read_csv('Dependentes - Página1.csv')

# Corrigir a leitura de 'Projetos Desenvolvidos' para ignorar a primeira linha
projetos = pd.read_csv('Projetos Desenvolvidos - Página1.csv', skiprows=1)
projetos.columns = ["Unnamed: 0", "IDProjeto", "NomeProjeto", "Descricao", "DataInicio", "DataConclusao", "FuncionarioResponsavelID", "Custo", "Status"]
projetos = projetos.drop(columns=["Unnamed: 0"])  # Remover coluna não necessária

recursos = pd.read_csv('Recursos do Projeto - Página1.csv')

# Criar a conexão com o banco de dados SQLite em memória
conn = sqlite3.connect(':memory:')

# Carregar os dataframes no banco de dados SQLite
funcionarios.to_sql('funcionarios', conn, index=False, if_exists='replace')
cargos.to_sql('cargos', conn, index=False, if_exists='replace')
departamentos.to_sql('departamentos', conn, index=False, if_exists='replace')
historico_salarios.to_sql('historico_salarios', conn, index=False, if_exists='replace')
dependentes.to_sql('dependentes', conn, index=False, if_exists='replace')
projetos.to_sql('projetos', conn, index=False, if_exists='replace')
recursos.to_sql('recursos', conn, index=False, if_exists='replace')

# Consulta 1: Média Salarial por Departamento
query1 = '''
SELECT d.NomeDepartamento, AVG(hs.Salario) AS MediaSalario
FROM projetos p
JOIN funcionarios f ON p.FuncionarioResponsavelID = f.ID
JOIN departamentos d ON f.DepartamentoID = d.IDDepartamento
JOIN historico_salarios hs ON f.ID = hs.FuncionarioID
WHERE p.Status = 'Concluído' AND (hs.Ano || hs.Mes) = (
    SELECT MAX(h2.Ano || h2.Mes)
    FROM historico_salarios h2
    WHERE h2.FuncionarioID = hs.FuncionarioID
)
GROUP BY d.NomeDepartamento
'''
media_salarios = pd.read_sql_query(query1, conn)
print(media_salarios)

# Consulta 2: Recursos Materiais mais Utilizados
query2 = '''
SELECT DescricaoRecurso, SUM(Quantidade) AS QuantidadeTotal
FROM recursos
WHERE TipoRecurso = 'Material'
GROUP BY DescricaoRecurso
ORDER BY QuantidadeTotal DESC
LIMIT 3
'''
recursos_materiais = pd.read_sql_query(query2, conn)
print(recursos_materiais)

# Consulta 3: Custo Total de Projetos Concluídos por Departamento
query3 = '''
SELECT d.NomeDepartamento, SUM(p.Custo) AS CustoTotal
FROM projetos p
JOIN funcionarios f ON p.FuncionarioResponsavelID = f.ID
JOIN departamentos d ON f.DepartamentoID = d.IDDepartamento
WHERE p.Status = 'Concluído'
GROUP BY d.NomeDepartamento
'''
custo_total_projetos = pd.read_sql_query(query3, conn)
print(custo_total_projetos)

# Consulta 4: Projetos em Execução com Detalhes do Funcionário Responsável
query4 = '''
SELECT p.NomeProjeto, p.Custo, p.DataInicio, p.DataConclusao, f.Nome AS NomeFuncionario
FROM projetos p
JOIN funcionarios f ON p.FuncionarioResponsavelID = f.ID
WHERE p.Status = 'Em Execução'
'''
projetos_em_execucao = pd.read_sql_query(query4, conn)
print(projetos_em_execucao)

# Consulta 5: Projeto com Mais Dependentes
query5 = '''
SELECT p.NomeProjeto, COUNT(d.ID) AS NumeroDependentes
FROM projetos p
JOIN funcionarios f ON p.FuncionarioResponsavelID = f.ID
JOIN dependentes d ON f.ID = d.FuncionarioID
GROUP BY p.IDProjeto
ORDER BY NumeroDependentes DESC
LIMIT 1
'''
projeto_com_mais_dependentes = pd.read_sql_query(query5, conn)
print(projeto_com_mais_dependentes)


# Converter os DataFrames em dicionários
media_salarios_dict = media_salarios.to_dict(orient='records')
recursos_materiais_dict = recursos_materiais.to_dict(orient='records')
custo_total_projetos_dict = custo_total_projetos.to_dict(orient='records')
projetos_em_execucao_dict = projetos_em_execucao.to_dict(orient='records')
projeto_com_mais_dependentes_dict = projeto_com_mais_dependentes.to_dict(orient='records')

# Escrever os dicionários em arquivos JSON
with open('media_salarios.json', 'w') as f:
    json.dump(media_salarios_dict, f, indent=4)

with open('recursos_materiais.json', 'w') as f:
    json.dump(recursos_materiais_dict, f, indent=4)

with open('custo_total_projetos.json', 'w') as f:
    json.dump(custo_total_projetos_dict, f, indent=4)

with open('projetos_em_execucao.json', 'w') as f:
    json.dump(projetos_em_execucao_dict, f, indent=4)

with open('projeto_com_mais_dependentes.json', 'w') as f:
    json.dump(projeto_com_mais_dependentes_dict, f, indent=4)