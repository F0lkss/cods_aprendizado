import pygame

# Inicializar
pygame.init()

tamanho_tela = (600, 600)
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption('Jogo de teste')

tamanho_bola = 18
bola = pygame.Rect(300, 450, tamanho_bola, tamanho_bola)
tamanho_jogador = 150
jogador = pygame.Rect(0, 500, tamanho_jogador, 18)

qtde_blocos_linha = 6
qtde_linhas_blocos = 4
qtde_total_blocos = qtde_blocos_linha * qtde_linhas_blocos

def criar_blocos(qtde_blocos_linha, qtde_linhas_blocos):
    altura = tamanho_tela[1]
    largura = tamanho_tela[0]
    distancia_entre_blocos = 10
    largura_bloco = largura / 6 - distancia_entre_blocos
    altura_bloco = 18
    distancia_entre_linhas = altura_bloco + 10
    blocos = []
    # criar os blocos
    for j in range(qtde_linhas_blocos):
        for i in range(qtde_blocos_linha):
            # criar bloco
            bloco = pygame.Rect(i * (largura_bloco + distancia_entre_blocos), j * distancia_entre_linhas, largura_bloco, altura_bloco)
            # adicionar a lista de blocos
            blocos.append(bloco)
    return blocos

cores = {
    'branco': (255, 255, 255),
    'preto': (0, 0, 0),
    'amarelo': (255, 255, 0),
    'azul': (0, 0, 255),
    'verde': (0, 255, 0)
}

fim_jogo = False
pontuacao = 0
movimento_bola = [1, -1]

# Criar Funções
def movimentar_jogador(evento):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RIGHT:
            if (jogador.x + tamanho_jogador) < tamanho_tela[0]:
                jogador.x += 1
        if evento.key == pygame.K_LEFT:
            if jogador.x > 0:
                jogador.x -= 1

def movimentar_bola(bola):
    movimento = movimento_bola
    bola.x = bola.x + movimento[0]
    bola.y = bola.y + movimento[1]    

    if bola.x <= 0:
        movimento[0] = - movimento[0]
    if bola.y <= 0:
        movimento[1] = - movimento[1]
    if bola.x + tamanho_bola >= tamanho_tela[0]:
        movimento[0] = - movimento[0]
    if bola.y + tamanho_bola >= tamanho_tela[1]:
        movimento = None

    if jogador.collidepoint(bola.x, bola.y):
        movimento[1] = - movimento[1]
    for bloco in blocos:
        if bloco.collidepoint(bola.x, bola.y):
            blocos.remove(bloco)
            movimento[1] = - movimento[1]

    return movimento

def atualizar_pontuacao():
    global pontuacao
    pontuacao = qtde_total_blocos - len(blocos)
    fonte = pygame.font.Font(None, 30)
    texto = fonte.render(f'Pontuação: {pontuacao}', 1, cores['amarelo'])
    tela.blit(texto, (0, 580))
    if pontuacao >= qtde_total_blocos:
        return True
    else:
        return False
# Desenha coisas na tela
def desenhar_inicio_jogo():
    tela.fill(cores['preto'])
    pygame.draw.rect(tela, cores['azul'], jogador)
    pygame.draw.rect(tela, cores['branco'], bola)

def desenhar_blocos(blocos):
    for bloco in blocos:
        pygame.draw.rect(tela, cores['verde'], bloco)


blocos = criar_blocos(qtde_blocos_linha, qtde_linhas_blocos )
# Criar Loop infinito
while not fim_jogo:
    desenhar_inicio_jogo()
    desenhar_blocos(blocos)
    fim_jogo = atualizar_pontuacao()
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            fim_jogo = True
    movimentar_jogador(evento)

    movimento_bola = movimentar_bola(bola)

    if not movimento_bola:
        fim_jogo = True

    pygame.time.wait(1)
    pygame.display.flip()

pygame.quit()