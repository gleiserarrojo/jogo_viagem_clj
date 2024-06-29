import pygame
import sys
import time

# Inicializa o Pygame
pygame.init()

# Configurações da janela
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Jogo de Perguntas")

# Cores
white = (255, 255, 255)
black = (0, 0, 0)

# Fonte
font = pygame.font.Font(pygame.font.match_font("Agrandir Wide"), 48)

# Carregar a imagem de fundo
fundo = pygame.image.load('background.png')
fundo = pygame.transform.scale(fundo, (width, height))  # Ajusta o tamanho da imagem ao tamanho da janela

# Perguntas e respostas
perguntas = [
    "A Viagem",
    "Qual é o seu Destino?",
    "Quais itens você vai levar para essa viagem?",
    "Onde vai guardar esses itens?",
    "Qual meio de transporte você vai utilizar?",
    "Quem você vai levar nessa viagem?"
]
respostas = []
resposta_atual = ""

# Índice da pergunta atual
indice_pergunta = 0

# Configuração do cursor piscante
cursor_mostra = True
cursor_timer = time.time()

# Configuração da repetição de tecla
tecla_pressionada = None
repetir_delay = 0.5
repetir_intervalo = 0.05
ultima_repeticao = 0

def render_texto_centralizado(texto, posicao_y, cor=white, sombra_cor=(100, 100, 100), deslocamento_sombra=(2, 2)):
    # Desenha a sombra
    text_surface = font.render(texto, True, sombra_cor)
    text_rect = text_surface.get_rect(center=(width // 2 + deslocamento_sombra[0], posicao_y + deslocamento_sombra[1]))
    screen.blit(text_surface, text_rect)
    
    # Desenha o texto principal
    text_surface = font.render(texto, True, cor)
    text_rect = text_surface.get_rect(center=(width // 2, posicao_y))
    screen.blit(text_surface, text_rect)

def render_texto(texto, posicao, cor=white, sombra_cor=(100, 100, 100), deslocamento_sombra=(2, 2)):
    # Desenha a sombra
    text_surface = font.render(texto, True, sombra_cor)
    screen.blit(text_surface, (posicao[0] + deslocamento_sombra[0], posicao[1] + deslocamento_sombra[1]))

    # Desenha o texto principal
    text_surface = font.render(texto, True, cor)
    screen.blit(text_surface, posicao)

def mostrar_perguntas():
    global cursor_mostra
    screen.blit(fundo, (0, 0))  # Desenha a imagem de fundo
    if indice_pergunta == 0:
        render_texto_centralizado(perguntas[indice_pergunta], 400)
    else:
        render_texto_centralizado(perguntas[indice_pergunta], 50)
    resposta_mostrada = resposta_atual + ("|" if cursor_mostra else "")
    if indice_pergunta > 0:
        render_texto("Resposta: " + resposta_mostrada, (50, 150))
    pygame.display.flip()

def mostrar_respostas():
    screen.blit(fundo, (0, 0))  # Desenha a imagem de fundo
    y = 300

    if len(respostas) >= 3:
        frase = f"Você irá para {respostas[1]}"
        render_texto_centralizado(frase, y)
        y += 40

        frase = f"de {respostas[4]},"
        render_texto_centralizado(frase, y)
        y += 40

        frase = f"levando {respostas[2]}"
        render_texto_centralizado(frase, y)
        y += 40

        frase = f"no(a) {respostas[3]}"
        render_texto_centralizado(frase, y)
        y += 40

        frase = f"com {respostas[5]}"
        render_texto_centralizado(frase, y)
        y += 40

    # render_texto_centralizado("Pressione qualquer tecla para recomeçar", height - 50)
    pygame.display.flip()

def processar_tecla(tecla):
    global resposta_atual
    if tecla == pygame.K_RETURN:
        respostas.append(resposta_atual)
        resposta_atual = ""
        global indice_pergunta, mostrando_respostas
        indice_pergunta += 1
        if indice_pergunta >= len(perguntas):
            mostrando_respostas = True
            return False
    elif tecla == pygame.K_BACKSPACE:
        resposta_atual = resposta_atual[:-1]
    elif tecla == pygame.K_SPACE:
        resposta_atual += " "
    else:
        char = pygame.key.name(tecla)
        if len(resposta_atual) < 30 and char.isalpha():  # Verifica se a tecla pressionada é uma letra
            resposta_atual += char
    return True

def reiniciar_jogo():
    global respostas, resposta_atual, indice_pergunta, mostrando_respostas
    respostas = []
    resposta_atual = ""
    indice_pergunta = 0
    mostrando_respostas = False

# Loop principal
jogando = True
mostrando_respostas = False
while jogando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False
        elif event.type == pygame.KEYDOWN:
            if mostrando_respostas:
                if event.key == pygame.K_RETURN:
                    reiniciar_jogo()
            else:
                tecla_pressionada = event.key
                ultima_repeticao = time.time()
                processar_tecla(tecla_pressionada)
        elif event.type == pygame.KEYUP:
            tecla_pressionada = None

    # Processa a repetição de tecla
    if tecla_pressionada and time.time() - ultima_repeticao > repetir_delay:
        if time.time() - ultima_repeticao > repetir_intervalo:
            processar_tecla(tecla_pressionada)
            ultima_repeticao = time.time()

    # Alterna o cursor piscante
    if time.time() - cursor_timer > 0.5:
        cursor_mostra = not cursor_mostra
        cursor_timer = time.time()

    if mostrando_respostas:
        mostrar_respostas()
    else:
        if indice_pergunta < len(perguntas):
            mostrar_perguntas()
        else:
            mostrando_respostas = True

pygame.quit()
sys.exit()
