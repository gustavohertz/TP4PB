import json

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
