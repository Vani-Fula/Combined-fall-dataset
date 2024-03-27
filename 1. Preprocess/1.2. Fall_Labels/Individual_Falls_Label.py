import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Função para detectar mudanças bruscas em cada eixo
def detectar_mudancas_bruscas(dados, limiar=0.5):
    mudancas = []
    for i in range(1, len(dados)):
        diff = abs(dados[i] - dados[i-1])
        if diff > limiar:
            mudancas.append(i)
    return mudancas

def encontrar_indice_valor_max(dados, mudancas):
    indice_max = max(mudancas, key=lambda i: abs(dados[i] - dados[i-1]))
    return indice_max

# Função para encontrar os índices de início e fim da janela
def find_window_indices(dados, limiar=0.5, duracao_janela=4.0):
    aceleracao_x = dados['WristAccelerometer: x-axis (g)']
    aceleracao_y = dados['WristAccelerometer: y-axis (g)']
    aceleracao_z = dados['WristAccelerometer: z-axis (g)']

    mudancas_x = detectar_mudancas_bruscas(aceleracao_x, limiar)
    mudancas_y = detectar_mudancas_bruscas(aceleracao_y, limiar)
    mudancas_z = detectar_mudancas_bruscas(aceleracao_z, limiar)

    inicio_janela_x = encontrar_indice_valor_max(aceleracao_x, mudancas_x)
    inicio_janela_y = encontrar_indice_valor_max(aceleracao_y, mudancas_y)
    inicio_janela_z = encontrar_indice_valor_max(aceleracao_z, mudancas_z)
    inicio_janela = int(np.mean([inicio_janela_x, inicio_janela_y, inicio_janela_z])) if mudancas_x and mudancas_y and mudancas_z else 0

    # # Definindo o tempo de maior mudança
    # tempo_maior_mudanca = dados['TimeStamp'][inicio_janela]
    # # Definindo o término da janela 1.5 segundos antes da maior mudança
    # tempo_inicio_janela = tempo_maior_mudanca - 0.7
    # # Definindo o término da janela 1.5 segundos após a maior mudança
    # tempo_fim_janela = tempo_maior_mudanca + 2.8
    
    # Definindo o tempo de maior mudança
    tempo_maior_mudanca = dados['TimeStamp'][inicio_janela]
    # Definindo o término da janela 1.5 segundos antes da maior mudança
    tempo_inicio_janela = tempo_maior_mudanca - 1
    # Definindo o término da janela 1.5 segundos após a maior mudança
    tempo_fim_janela = tempo_maior_mudanca + 2.5 # 3,7 total de tempo

    idx_inicio_janela = dados.index[dados['TimeStamp'] >= tempo_inicio_janela]
    idx_fim_janela = dados.index[dados['TimeStamp'] >= tempo_fim_janela]

    # Verificando se o índice de fim da janela foi encontrado
    if len(idx_fim_janela) == 0:
        # Caso não tenha sido encontrado, definimos o índice de fim como o último índice do DataFrame
        idx_fim_janela = len(dados) - 1
    else:
        # Caso contrário, pegamos o primeiro índice encontrado
        idx_fim_janela = idx_fim_janela[0]

    # Verificando se o índice de início da janela foi encontrado
    if len(idx_inicio_janela) == 0:
        # Caso não tenha sido encontrado, definimos o índice de início como o primeiro índice do DataFrame
        idx_inicio_janela = 0
    else:
        # Caso contrário, pegamos o primeiro índice encontrado
        idx_inicio_janela = idx_inicio_janela[0]

    return idx_inicio_janela, idx_fim_janela

# Função para alterar os valores da última coluna dentro da janela para 1
def alterar_valores_janela(dados, idx_inicio_janela, idx_fim_janela, coluna_alterar):
    dados_alterados = dados.copy()
    dados_alterados.loc[idx_inicio_janela:idx_fim_janela, coluna_alterar] = "1"
    return dados_alterados

# Função para plotar os gráficos dos dados de aceleração e giroscópio com as janelas destacadas
def plot_data(ax, tempo, aceleracao_x, aceleracao_y, aceleracao_z, atividade_str, subject_str, trial_str, idx_inicio_janela, idx_fim_janela):
    # Plotando os dados do Acelerômetro
    ax.plot(tempo, aceleracao_x, label='Aceleração X')
    ax.plot(tempo, aceleracao_y, label='Aceleração Y')
    ax.plot(tempo, aceleracao_z, label='Aceleração Z')
    ax.set_xlabel('Tempo (s)')
    ax.set_ylabel('Aceleração')
    ax.set_title(f'Dados do Acelerômetro - {atividade_str} {subject_str} {trial_str}')
    ax.legend()

    # Plotando a janela com apenas duas linhas
    ax.axvline(x=tempo[idx_inicio_janela], color='red', linestyle='--', label='Início da Janela')
    ax.axvline(x=tempo[idx_fim_janela], color='blue', linestyle='--', label='Final da Janela')

    # Exibindo os gráficos
    ax.legend(loc='upper right')

# Caminho completo para o arquivo CSV que deseja processar
#caminho_csv = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\Base de dados\WEDA\WEDA FALL\Subjects\Subject6\Activity19\Trial3\Subject6Activity19Trial3.csv"
#caminho_csv = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\Base de dados\UMAFall_Dataset\Resultados\Subject15\Activity15\Trial3\UMAFALL_Subject15Activity15Trial3.csv"
#caminho_csv = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\Base de dados\Normalizados\UMA\Subject19\Activity15\Trial2\UMAFALL_Subject19Activity15Trial2.csv" S14A20T4
caminho_csv = r"C:\Users\Vanilson Fula\Downloads\Aulas\Tese\Bases de dados\Teste_2\Padrão\Individual\Sem_cross_val\WEDA\Subjects\Subject14\Activity20\Trial4\WEDAFALL_Subject14Activity20Trial4.csv"
# Defina o nome da coluna que deseja alterar (substituir por 1 na janela)
indice_coluna = "Tag"

# Ler o arquivo CSV
dados = pd.read_csv(caminho_csv)
dados["Tag"] = "0"

# Verifica se o DataFrame não está vazio e se possui as colunas de interesse
if not dados.empty and 'TimeStamp' in dados.columns and 'WristAccelerometer: x-axis (g)' in dados.columns:
    # Encontra os índices de início e fim da janela
    idx_inicio_janela, idx_fim_janela = find_window_indices(dados)

    # Altera os valores da última coluna dentro da janela para 1
    dados_alterados = alterar_valores_janela(dados, idx_inicio_janela, idx_fim_janela, indice_coluna)

    # Salva os dados alterados no mesmo arquivo original
    dados_alterados.to_csv(caminho_csv, index=False)

    # Plotar os gráficos dos dados com as janelas destacadas
    fig, axs = plt.subplots(1, 1, figsize=(12, 6))
    plot_data(axs, dados['TimeStamp'], dados['WristAccelerometer: x-axis (g)'], dados['WristAccelerometer: y-axis (g)'], dados['WristAccelerometer: z-axis (g)'], "Atividade", "Sujeito", "Tentativa", idx_inicio_janela, idx_fim_janela)
    plt.show()

else:
    print("DataFrame vazio ou colunas de interesse não encontradas no arquivo.")
