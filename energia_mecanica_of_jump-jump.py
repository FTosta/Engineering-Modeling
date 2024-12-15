import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

# -------------------------------
# Constantes do sistema
# -------------------------------
# Parâmetros físicos do problema
m = 90           # Massa do sistema (kg)
g = 9.81         # Aceleração gravitacional (m/s^2)
x_max = 0.5      # Deformação máxima da mola (m)
y_max = 1        # Altura máxima atingida pelo corpo (m)

# Constante elástica da mola, calculada com base na conservação de energia
k = 2 * m * g * y_max / x_max**2  # Constante elástica (N/m)

# Amplitude do movimento (m)
A = y_max / 2

# Configuração do tempo para a simulação
t_total = 2 * np.pi  # Tempo total da simulação (s)
dt = 0.05           # Intervalo de tempo entre quadros (s)

# -------------------------------
# Função para cálculo das energias e velocidade
# -------------------------------
def calcular_Energias(y):
    """
    Calcula as energias do sistema (potencial gravitacional, elástica e cinética), bem como a velocidade.

    Parâmetros:
        y (float): Posição vertical do corpo (m)
    
    Retorna:
        tuple: Energia mecânica total (E_mec), energia cinética (K_c),
               energia potencial gravitacional (U_g), energia potencial elástica (U_el),
               velocidade (v) e deformação da mola (x)
    """
    # Deformação da mola quando o corpo está em contato com ela
    if y < x_max:  # Caso a altura seja menor que a posição limite da mola
        x = x_max - y  # Deformação da mola
    else:
        x = 0         # Sem contato com a mola

    # Ajusta valores muito próximos de zero para zero
    if np.any(np.isclose(y, 0.0, atol=1e-3)):
        y = 0

    # Cálculo das energias
    E_t = m * g * y_max       # Energia mecânica total do sistema
    U_g = m * g * y           # Energia potencial gravitacional
    U_el = 0.5 * k * x**2     # Energia potencial elástica

    # Cálculo da velocidade com base nas condições
    if x_max < y < y_max:  # Movimento fora do contato com a mola
        v = np.sqrt(2 * (E_t - U_g) / m)
    elif 0 < y < x_max:    # Movimento com contato com a mola
        v = np.sqrt(2 / m * (E_t - U_g - U_el))
    else:
        v = 0  # Posição estacionária

    # Energia cinética e total
    K_c = 0.5 * m * v**2      # Energia cinética
    E_mec = K_c + U_g + U_el  # Energia mecânica total

    return E_mec, K_c, U_g, U_el, v, x

# -------------------------------
# Inicialização das variáveis
# -------------------------------
# Vetores de tempo e posição ao longo da simulação
tempos = np.arange(0, t_total, dt)  # Vetor de tempo
posicoes = y_max * (1 + np.cos(tempos)) / 2  # Vetor de posição com oscilação suave

# Listas para armazenar resultados de velocidades e deformações
velocidades = []
deformacoes = []

# Cálculo prévio das velocidades e deformações para cada posição
for y in posicoes:
    _, _, _, _, v, x = calcular_Energias(y)
    velocidades.append(v)
    deformacoes.append(x)

# -------------------------------
# Configuração dos subplots
# -------------------------------
# Configuração da figura e dos subgráficos
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Subplot 1: Posição ao longo do tempo
linha_posicao, = axs[0, 0].plot([], [], color='orange', lw=2)
axs[0, 0].set_xlim(0, t_total)
axs[0, 0].set_ylim(0, max(posicoes) * 1.2)
axs[0, 0].set_title("Posição ao Longo do Tempo")
axs[0, 0].set_xlabel("Tempo (s)")
axs[0, 0].set_ylabel("Posição (m)")

# Subplot 2: Velocidade ao longo do tempo
linha_velocidade, = axs[0, 1].plot([], [], color='blue', lw=2)
axs[0, 1].set_xlim(0, t_total)
axs[0, 1].set_ylim(min(velocidades), max(velocidades) * 1.2)
axs[0, 1].set_title("Velocidade ao Longo do Tempo")
axs[0, 1].set_xlabel("Tempo (s)")
axs[0, 1].set_ylabel("Velocidade (m/s)")

# Subplot 3: Deformação da mola ao longo do tempo
linha_deformacao, = axs[1, 0].plot([], [], color='green', lw=2)
axs[1, 0].set_xlim(0, t_total)
axs[1, 0].set_ylim(0, max(deformacoes) * 1.2)
axs[1, 0].set_title("Deformação da Mola ao Longo do Tempo")
axs[1, 0].set_xlabel("Tempo (s)")
axs[1, 0].set_ylabel("Deformação (m)")

# Subplot 4: Gráfico de barras de energias
larguras = ["E", "K", "U_grav", "U_el"]
valores_iniciais = [0, 0, 0, 0]
barras = axs[1, 1].bar(larguras, valores_iniciais, color=["red", "blue", "green", "purple"])
axs[1, 1].set_title("Energia Mecânica do Sistema")
axs[1, 1].set_xlabel("Energias (J)")

# -------------------------------
# Função de atualização para animação
# -------------------------------
def update(frame):
    """
    Atualiza os dados dos gráficos a cada quadro da animação.

    Parâmetros:
        frame (int): Índice do quadro atual

    Retorna:
        tuple: Objetos de linha e barras atualizados
    """
    # Atualiza o gráfico de posição
    linha_posicao.set_data(tempos[:frame], posicoes[:frame])

    # Atualiza o gráfico de velocidade
    linha_velocidade.set_data(tempos[:frame], velocidades[:frame])

    # Atualiza o gráfico de deformação
    linha_deformacao.set_data(tempos[:frame], deformacoes[:frame])

    # Calcula as energias no quadro atual
    y = posicoes[frame]
    E_mec, K_c, U_g, U_el, _, _ = calcular_Energias(y)
    energias = [E_mec, K_c, U_g, U_el]

    # Atualiza as barras de energia
    for bar, energia in zip(barras, energias):
        bar.set_height(energia)
    axs[1, 1].set_ylim(0, max(energias) * 1.2)
    
    return linha_posicao, linha_velocidade, linha_deformacao, barras

# -------------------------------
# Criação e execução da animação
# -------------------------------
ani = FuncAnimation(fig, update, frames=range(0, len(tempos), 10), interval=50, repeat=True)

plt.tight_layout()
plt.show()
