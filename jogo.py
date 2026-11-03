import pygame
import sys
import random
import json
import os
import math

pygame.init()

# =====================================================
# CONFIGURAÇÕES
# =====================================================

LARGURA = 1100
ALTURA = 700

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Football Evolution")

RELOGIO = pygame.time.Clock()

BRANCO = (255, 255, 255)
PRETO = (15, 15, 15)
VERDE = (35, 125, 55)
VERDE2 = (40, 145, 65)
AZUL = (35, 100, 240)
VERMELHO = (230, 45, 45)
AMARELO = (255, 220, 30)
CINZA = (130, 130, 130)

FONTE = pygame.font.SysFont("Arial", 28, bold=True)
PEQUENA = pygame.font.SysFont("Arial", 19)
GRANDE = pygame.font.SysFont("Arial", 48, bold=True)

RELOGIO_JOGO = 120
ARQUIVO_SAVE = "carreira.json"

TIMES = [
    ("Flamengo", (210, 20, 40)),
    ("Palmeiras", (20, 130, 65)),
    ("Corinthians", (30, 30, 30)),
    ("São Paulo", (220, 30, 30)),
    ("Santos", (240, 240, 240)),
    ("Grêmio", (30, 70, 180)),
    ("Botafogo", (20, 20, 20)),
    ("Atlético-MG", (40, 40, 40)),
]

# =====================================================
# SAVE
# =====================================================

try:
    with open(ARQUIVO_SAVE, "r") as arquivo:
        carreira = json.load(arquivo)
except:
    carreira = {
        "vitorias": 0,
        "derrotas": 0,
        "gols": 0,
        "moedas": 0,
        "time": 0
    }

atributos = {
    "velocidade": 5,
    "chute": 5,
    "controle": 5
}

time1 = 0
time2 = 1

estado = "menu"
modo_atual = "partida"

gols1 = 0
gols2 = 0
tempo = RELOGIO_JOGO

mensagem = ""
mensagem_tempo = 0

faltas1 = 0
faltas2 = 0

# =====================================================
# CAMPEONATO
# =====================================================

campeonato_ativo = False
campeonato_finalizado = False
rodada_atual = 0

tabela = {}
calendario = []

time_campeonato = 0

def criar_tabela():

    global tabela

    tabela = {}

    for i, time in enumerate(TIMES):

        tabela[i] = {
            "pontos": 0,
            "jogos": 0,
            "vitorias": 0,
            "empates": 0,
            "derrotas": 0,
            "gols_pro": 0,
            "gols_contra": 0
        }


def criar_calendario():

    global calendario

    times = list(range(len(TIMES)))

    calendario = []

    for rodada in range(7):

        jogos = []

        for i in range(4):

            mandante = times[i]
            visitante = times[7 - i]

            jogos.append((mandante, visitante))

        calendario.append(jogos)

        times = [
            times[0],
            times[7],
            times[1],
            times[2],
            times[3],
            times[4],
            times[5],
            times[6]
        ]


def iniciar_campeonato():

    global campeonato_ativo
    global campeonato_finalizado
    global rodada_atual
    global time_campeonato

    criar_tabela()
    criar_calendario()

    campeonato_ativo = True
    campeonato_finalizado = False
    rodada_atual = 0

    time_campeonato = time1

    iniciar_rodada()


def atualizar_tabela(time_a, time_b, gols_a, gols_b):

    a = tabela[time_a]
    b = tabela[time_b]

    a["jogos"] += 1
    b["jogos"] += 1

    a["gols_pro"] += gols_a
    a["gols_contra"] += gols_b

    b["gols_pro"] += gols_b
    b["gols_contra"] += gols_a

    if gols_a > gols_b:

        a["pontos"] += 3
        a["vitorias"] += 1

        b["derrotas"] += 1

    elif gols_b > gols_a:

        b["pontos"] += 3
        b["vitorias"] += 1

        a["derrotas"] += 1

    else:

        a["pontos"] += 1
        b["pontos"] += 1

        a["empates"] += 1
        b["empates"] += 1


def simular_jogo(time_a, time_b):

    gols_a = random.randint(0, 4)
    gols_b = random.randint(0, 4)

    atualizar_tabela(
        time_a,
        time_b,
        gols_a,
        gols_b
    )


def iniciar_rodada():

    global time1
    global time2

    jogos = calendario[rodada_atual]

    for mandante, visitante in jogos:

        if time_campeonato not in (mandante, visitante):

            simular_jogo(mandante, visitante)

        else:

            time1 = time_campeonato

            if mandante == time_campeonato:
                time2 = visitante
            else:
                time2 = mandante


def finalizar_rodada():

    global rodada_atual
    global campeonato_finalizado
    global estado

    atualizar_tabela(
        time1,
        time2,
        gols1,
        gols2
    )

    rodada_atual += 1

    if rodada_atual >= 7:

        campeonato_finalizado = True
        estado = "classificacao"

    else:

        iniciar_rodada()
        estado = "resultado_campeonato"


def ordenar_tabela():

    return sorted(
        tabela.items(),
        key=lambda item: (
            item[1]["pontos"],
            item[1]["vitorias"],
            item[1]["gols_pro"] - item[1]["gols_contra"],
            item[1]["gols_pro"]
        ),
        reverse=True
    )


def desenhar_classificacao():

    TELA.fill((20, 30, 50))

    centro(
        "CAMPEONATO BRASILEIRO",
        45,
        AMARELO,
        GRANDE
    )

    escrever("POS", 35, 115, AMARELO, PEQUENA)
    escrever("TIME", 110, 115, AMARELO, PEQUENA)
    escrever("PTS", 510, 115, AMARELO, PEQUENA)
    escrever("J", 600, 115, AMARELO, PEQUENA)
    escrever("V", 670, 115, AMARELO, PEQUENA)
    escrever("E", 735, 115, AMARELO, PEQUENA)
    escrever("D", 800, 115, AMARELO, PEQUENA)
    escrever("SG", 880, 115, AMARELO, PEQUENA)

    classificacao = ordenar_tabela()

    for posicao, (indice, dados) in enumerate(classificacao):

        y = 160 + posicao * 48

        saldo = dados["gols_pro"] - dados["gols_contra"]

        if posicao == 0:
            cor = AMARELO
        elif posicao >= 6:
            cor = VERMELHO
        else:
            cor = BRANCO

        escrever(posicao + 1, 45, y, cor, PEQUENA)

        escrever(
            TIMES[indice][0],
            110,
            y,
            TIMES[indice][1],
            PEQUENA
        )

        escrever(dados["pontos"], 515, y, cor, PEQUENA)
        escrever(dados["jogos"], 605, y, cor, PEQUENA)
        escrever(dados["vitorias"], 675, y, cor, PEQUENA)
        escrever(dados["empates"], 740, y, cor, PEQUENA)
        escrever(dados["derrotas"], 805, y, cor, PEQUENA)
        escrever(saldo, 890, y, cor, PEQUENA)

    if campeonato_finalizado:

        campeao = classificacao[0][0]

        centro(
            "CAMPEAO DO CAMPEONATO!",
            570,
            AMARELO,
            FONTE
        )

        centro(
            TIMES[campeao][0],
            610,
            TIMES[campeao][1],
            GRANDE
        )

    else:

        centro(
            f"RODADA {rodada_atual + 1} DE 7",
            570,
            AMARELO
        )

    centro(
        "ENTER - CONTINUAR",
        660,
        BRANCO,
        PEQUENA
    )


# =====================================================
# JOGADORES
# =====================================================

class Jogador:

    def __init__(self, x, y, numero, cor, controles):

        self.x = float(x)
        self.y = float(y)

        self.numero = numero
        self.cor = cor
        self.controles = controles

        self.raio = 19
        self.velocidade = 4
        self.direcao = pygame.Vector2(1, 0)

        self.carrinho = 0
        self.cooldown = 0

        self.rect = pygame.Rect(
            self.x - self.raio,
            self.y - self.raio,
            self.raio * 2,
            self.raio * 2
        )

    def mover(self, teclas):

        movimento = pygame.Vector2(0, 0)

        cima, baixo, esquerda, direita = self.controles

        if teclas[cima]:
            movimento.y -= 1

        if teclas[baixo]:
            movimento.y += 1

        if teclas[esquerda]:
            movimento.x -= 1

        if teclas[direita]:
            movimento.x += 1

        velocidade = self.velocidade

        if self.carrinho > 0:
            velocidade = 10
            self.carrinho -= 1

        if movimento.length() > 0:

            movimento = movimento.normalize()

            self.direcao = movimento

            self.x += movimento.x * velocidade
            self.y += movimento.y * velocidade

        self.x = max(55, min(1045, self.x))
        self.y = max(55, min(645, self.y))

        if self.cooldown > 0:
            self.cooldown -= 1

        self.rect.center = (int(self.x), int(self.y))

    def desenhar(self):

        pygame.draw.circle(
            TELA,
            self.cor,
            (int(self.x), int(self.y)),
            self.raio
        )

        pygame.draw.circle(
            TELA,
            BRANCO,
            (int(self.x), int(self.y)),
            self.raio,
            2
        )

        numero = PEQUENA.render(
            str(self.numero),
            True,
            BRANCO
        )

        TELA.blit(
            numero,
            numero.get_rect(center=(self.x, self.y))
        )


# =====================================================
# BOLA
# =====================================================

class Bola:

    def __init__(self):

        self.x = 550
        self.y = 350

        self.vel = pygame.Vector2(0, 0)

        self.dono = None
        self.ultimo_toque = None

        self.raio = 10

        self.bloqueio = 0
        self.rastro = []

    def desenhar(self):

        for i, pos in enumerate(self.rastro):

            pygame.draw.circle(
                TELA,
                (180, 180, 180),
                (int(pos[0]), int(pos[1])),
                max(2, i // 2 + 2)
            )

        pygame.draw.circle(
            TELA,
            BRANCO,
            (int(self.x), int(self.y)),
            self.raio
        )

        pygame.draw.circle(
            TELA,
            PRETO,
            (int(self.x), int(self.y)),
            self.raio,
            2
        )

    def atualizar(self):

        if self.bloqueio > 0:
            self.bloqueio -= 1

        if self.dono is not None:

            jogador = self.dono

            self.ultimo_toque = jogador.numero

            posicao = jogador.direcao * 30

            self.x = jogador.x + posicao.x
            self.y = jogador.y + posicao.y

            self.vel.update(0, 0)

            return

        if self.vel.length() > 1:

            self.rastro.append((self.x, self.y))

            if len(self.rastro) > 8:
                self.rastro.pop(0)

        else:
            self.rastro.clear()

        self.x += self.vel.x
        self.y += self.vel.y

        self.vel *= 0.985

        if abs(self.vel.x) < 0.12:
            self.vel.x = 0

        if abs(self.vel.y) < 0.12:
            self.vel.y = 0

        if self.x <= 45 and 270 < self.y < 430:

            marcar_gol(2)
            return

        if self.x >= 1055 and 270 < self.y < 430:

            marcar_gol(1)
            return

        if self.x <= 35 or self.x >= 1065:

            self.x = 550
            self.y = 350
            self.vel.update(0, 0)
            self.dono = None

            return

        if self.y <= 45 or self.y >= 655:
            self.vel.y *= -0.8

        self.y = max(45, min(655, self.y))


# =====================================================
# OBJETOS
# =====================================================

jogador1 = Jogador(
    300, 350, 1, AZUL,
    (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
)

jogador2 = Jogador(
    800, 350, 2, VERMELHO,
    (
        pygame.K_UP,
        pygame.K_DOWN,
        pygame.K_LEFT,
        pygame.K_RIGHT
    )
)

bola = Bola()

# =====================================================
# FUNÇÕES GERAIS
# =====================================================

def salvar():

    with open(ARQUIVO_SAVE, "w") as arquivo:
        json.dump(carreira, arquivo, indent=4)


def escrever(texto, x, y, cor=BRANCO, fonte=FONTE):

    imagem = fonte.render(str(texto), True, cor)
    TELA.blit(imagem, (x, y))


def centro(texto, y, cor=BRANCO, fonte=FONTE):

    imagem = fonte.render(str(texto), True, cor)

    TELA.blit(
        imagem,
        imagem.get_rect(center=(LARGURA // 2, y))
    )


def aviso(texto):

    global mensagem, mensagem_tempo

    mensagem = texto
    mensagem_tempo = 120


# =====================================================
# JOGO
# =====================================================

def novo_posicionamento():

    jogador1.x = 300
    jogador1.y = 350

    jogador2.x = 800
    jogador2.y = 350

    bola.x = 550
    bola.y = 350

    bola.dono = None
    bola.ultimo_toque = None
    bola.vel.update(0, 0)
    bola.rastro.clear()


def novo_jogo():

    global gols1, gols2, tempo
    global faltas1, faltas2

    gols1 = 0
    gols2 = 0

    tempo = RELOGIO_JOGO

    faltas1 = 0
    faltas2 = 0

    jogador1.cooldown = 0
    jogador2.cooldown = 0

    jogador1.carrinho = 0
    jogador2.carrinho = 0

    novo_posicionamento()


def marcar_gol(jogador):

    global gols1, gols2

    if jogador == 1:
        gols1 += 1
    else:
        gols2 += 1

    if modo_atual == "carreira":

        carreira["gols"] += 1
        salvar()

    novo_posicionamento()


def pegar_bola(jogador):

    if bola.bloqueio > 0:
        return

    distancia = math.hypot(
        bola.x - jogador.x,
        bola.y - jogador.y
    )

    if distancia < 43:

        bola.dono = jogador
        bola.ultimo_toque = jogador.numero


def chutar(jogador):

    distancia = math.hypot(
        bola.x - jogador.x,
        bola.y - jogador.y
    )

    if bola.dono == jogador or distancia < 55:

        if jogador.numero == 1:
            alvo = pygame.Vector2(1100, 350)
        else:
            alvo = pygame.Vector2(0, 350)

        direcao = alvo - pygame.Vector2(
            bola.x,
            bola.y
        )

        if direcao.length() == 0:
            return

        direcao = direcao.normalize()

        potencia = 15 + atributos["chute"] * 0.7

        bola.ultimo_toque = jogador.numero
        bola.dono = None
        bola.vel = direcao * potencia
        bola.bloqueio = 18
        bola.rastro.clear()


def carrinho(jogador, adversario):

    global faltas1, faltas2

    if jogador.cooldown > 0:
        return

    jogador.carrinho = 12
    jogador.cooldown = 65

    distancia = math.hypot(
        jogador.x - adversario.x,
        jogador.y - adversario.y
    )

    if distancia < 60:

        if jogador.numero == 1:
            faltas1 += 1
        else:
            faltas2 += 1

        if bola.dono == adversario:

            bola.dono = jogador
            bola.ultimo_toque = jogador.numero

        aviso("FALTA!")


def iniciar_partida(modo):

    global estado, modo_atual

    modo_atual = modo

    novo_jogo()

    if modo == "faltas":

        bola.x = 700
        bola.y = 350

        jogador1.x = 650
        jogador1.y = 350

        jogador2.x = 900
        jogador2.y = 350

    estado = "jogo"


def atualizar_partida():

    global estado, tempo

    teclas = pygame.key.get_pressed()

    jogador1.mover(teclas)
    jogador2.mover(teclas)

    if bola.dono is None:

        pegar_bola(jogador1)

        if bola.dono is None:
            pegar_bola(jogador2)

    distancia = math.hypot(
        jogador1.x - jogador2.x,
        jogador1.y - jogador2.y
    )

    if distancia < 38:

        if bola.dono == jogador1:

            bola.dono = jogador2
            bola.ultimo_toque = jogador2.numero

        elif bola.dono == jogador2:

            bola.dono = jogador1
            bola.ultimo_toque = jogador1.numero

    bola.atualizar()

    if modo_atual in ("partida", "carreira", "campeonato"):

        tempo -= 1 / 60

        if tempo <= 0:

            if modo_atual == "carreira":

                if gols1 > gols2:

                    carreira["vitorias"] += 1
                    carreira["moedas"] += 100

                else:

                    carreira["derrotas"] += 1

                salvar()

            if modo_atual == "campeonato":

                finalizar_rodada()

            else:

                estado = "resultado"


# =====================================================
# CAMPO
# =====================================================

def desenhar_campo():

    TELA.fill(VERDE)

    for x in range(0, LARGURA, 100):

        pygame.draw.rect(
            TELA,
            VERDE2,
            (x, 0, 50, ALTURA)
        )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (35, 35, 1030, 630),
        4
    )

    pygame.draw.line(
        TELA,
        BRANCO,
        (550, 35),
        (550, 665),
        4
    )

    pygame.draw.circle(
        TELA,
        BRANCO,
        (550, 350),
        85,
        4
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (35, 230, 130, 240),
        4
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (935, 230, 130, 240),
        4
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (0, 275, 35, 150),
        5
    )

    pygame.draw.rect(
        TELA,
        BRANCO,
        (1065, 275, 35, 150),
        5
    )


def desenhar_partida():

    desenhar_campo()

    jogador1.desenhar()
    jogador2.desenhar()
    bola.desenhar()

    escrever(
        TIMES[time1][0],
        80, 8,
        TIMES[time1][1],
        PEQUENA
    )

    escrever(
        TIMES[time2][0],
        850, 8,
        TIMES[time2][1],
        PEQUENA
    )

    escrever(
        f"{gols1}  X  {gols2}",
        490, 8,
        BRANCO
    )

    if modo_atual in ("partida", "carreira", "campeonato"):

        escrever(
            f"Tempo: {int(tempo)}",
            480, 670,
            AMARELO,
            PEQUENA
        )

    escrever(
        "J1: WASD | ESPACO: CHUTE | SHIFT: CARRINHO",
        30, 675,
        BRANCO,
        PEQUENA
    )

    escrever(
        "J2: SETAS | ENTER: CHUTE | CTRL: CARRINHO",
        600, 675,
        BRANCO,
        PEQUENA
    )

    if modo_atual == "campeonato":

        escrever(
            f"CAMPEONATO - RODADA {rodada_atual + 1}/7",
            390, 55,
            AMARELO,
            PEQUENA
        )

    if mensagem_tempo > 0:

        escrever(
            mensagem,
            400, 90,
            AMARELO,
            PEQUENA
        )


# =====================================================
# MENU
# =====================================================

def desenhar_menu():

    TELA.fill((20, 30, 50))

    centro(
        "FOOTBALL EVOLUTION",
        65,
        AMARELO,
        GRANDE
    )

    opcoes = [
        "1 - PARTIDA 2 JOGADORES",
        "2 - TREINO LIVRE",
        "3 - MODO FALTAS",
        "4 - MODO CARREIRA",
        "5 - ESCOLHER TIMES",
        "6 - CENTRO DE TREINAMENTO",
        "7 - VER ATRIBUTOS",
        "8 - CAMPEONATO",
        "ESC - SAIR"
    ]

    for i, opcao in enumerate(opcoes):

        centro(
            opcao,
            145 + i * 48,
            BRANCO,
            PEQUENA
        )

    centro(
        f"Carreira: {carreira['vitorias']} vitórias | "
        f"{carreira['gols']} gols",
        650,
        AMARELO,
        PEQUENA
    )


# =====================================================
# SELEÇÃO DE TIMES
# =====================================================

def tela_times():

    global time1, time2

    rodando = True

    while rodando:

        TELA.fill((20, 30, 50))

        centro(
            "ESCOLHA OS TIMES",
            65,
            AMARELO,
            GRANDE
        )

        centro(
            "JOGADOR 1: A / D PARA ESCOLHER",
            160,
            AZUL
        )

        centro(
            TIMES[time1][0],
            220,
            TIMES[time1][1],
            GRANDE
        )

        centro(
            "JOGADOR 2: SETAS ESQUERDA / DIREITA",
            330,
            VERMELHO
        )

        centro(
            TIMES[time2][0],
            390,
            TIMES[time2][1],
            GRANDE
        )

        centro(
            "ENTER - CONFIRMAR",
            530,
            AMARELO
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    rodando = False

                if evento.key == pygame.K_a:
                    time1 = (time1 - 1) % len(TIMES)

                if evento.key == pygame.K_d:
                    time1 = (time1 + 1) % len(TIMES)

                if evento.key == pygame.K_LEFT:
                    time2 = (time2 - 1) % len(TIMES)

                if evento.key == pygame.K_RIGHT:
                    time2 = (time2 + 1) % len(TIMES)

                if evento.key == pygame.K_RETURN:
                    rodando = False

        pygame.display.flip()
        RELOGIO.tick(60)


# =====================================================
# TREINAMENTO
# =====================================================

def tela_treino():

    global atributos

    rodando = True

    while rodando:

        TELA.fill((20, 30, 50))

        centro(
            "CENTRO DE TREINAMENTO",
            90,
            AMARELO,
            GRANDE
        )

        centro(
            f"1 - VELOCIDADE: {atributos['velocidade']}",
            230
        )

        centro(
            f"2 - CHUTE: {atributos['chute']}",
            300
        )

        centro(
            f"3 - CONTROLE: {atributos['controle']}",
            370
        )

        centro(
            "ENTER - VOLTAR AO MENU",
            520,
            AMARELO
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_1:

                    atributos["velocidade"] += 1
                    jogador1.velocidade += 0.3

                if evento.key == pygame.K_2:
                    atributos["chute"] += 1

                if evento.key == pygame.K_3:
                    atributos["controle"] += 1

                if evento.key == pygame.K_RETURN:
                    rodando = False

        pygame.display.flip()
        RELOGIO.tick(60)


# =====================================================
# ATRIBUTOS
# =====================================================

def tela_atributos():

    rodando = True

    while rodando:

        TELA.fill((20, 30, 50))

        centro(
            "ATRIBUTOS DO JOGADOR",
            100,
            AMARELO,
            GRANDE
        )

        y = 250

        for nome, valor in atributos.items():

            centro(
                f"{nome.upper()}: {valor}",
                y
            )

            y += 65

        centro(
            "ENTER PARA VOLTAR",
            550,
            AMARELO
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    rodando = False

        pygame.display.flip()
        RELOGIO.tick(60)


# =====================================================
# RESULTADO
# =====================================================

def tela_resultado():

    rodando = True

    while rodando:

        TELA.fill((20, 30, 50))

        centro(
            "FIM DE JOGO",
            120,
            AMARELO,
            GRANDE
        )

        centro(
            f"{TIMES[time1][0]}  {gols1} X {gols2}  {TIMES[time2][0]}",
            260
        )

        if gols1 > gols2:
            centro("JOGADOR 1 VENCEU!", 350, AZUL)

        elif gols2 > gols1:
            centro("JOGADOR 2 VENCEU!", 350, VERMELHO)

        else:
            centro("EMPATE!", 350, AMARELO)

        centro(
            "ENTER - MENU",
            480
        )

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:
                    rodando = False

        pygame.display.flip()
        RELOGIO.tick(60)


# =====================================================
# RESULTADO DO CAMPEONATO
# =====================================================

def tela_resultado_campeonato():

    TELA.fill((20, 30, 50))

    centro(
        f"RODADA {rodada_atual} FINALIZADA!",
        130,
        AMARELO,
        GRANDE
    )

    centro(
        f"{TIMES[time1][0]}  {gols1} X {gols2}  {TIMES[time2][0]}",
        260
    )

    if gols1 > gols2:
        centro("VITORIA!", 350, AZUL)

    elif gols2 > gols1:
        centro("DERROTA!", 350, VERMELHO)

    else:
        centro("EMPATE!", 350, AMARELO)

    centro(
        "ENTER - VER CLASSIFICACAO",
        500,
        BRANCO
    )


# =====================================================
# LOOP PRINCIPAL
# =====================================================

while True:

    RELOGIO.tick(60)

    if estado == "menu":

        desenhar_menu()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if evento.key == pygame.K_1:
                    iniciar_partida("partida")

                if evento.key == pygame.K_2:
                    iniciar_partida("treino")

                if evento.key == pygame.K_3:
                    iniciar_partida("faltas")

                if evento.key == pygame.K_4:

                    time1 = carreira["time"]
                    iniciar_partida("carreira")

                if evento.key == pygame.K_5:
                    tela_times()

                if evento.key == pygame.K_6:
                    tela_treino()

                if evento.key == pygame.K_7:
                    tela_atributos()

                if evento.key == pygame.K_8:

                    tela_times()
                    iniciar_campeonato()

                    iniciar_partida("campeonato")

    elif estado == "jogo":

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_ESCAPE:
                    estado = "menu"

                if evento.key == pygame.K_SPACE:
                    chutar(jogador1)

                if evento.key == pygame.K_RETURN:
                    chutar(jogador2)

                if evento.key == pygame.K_LSHIFT:
                    carrinho(jogador1, jogador2)

                if evento.key == pygame.K_RCTRL:
                    carrinho(jogador2, jogador1)

        atualizar_partida()

        if estado == "jogo":
            desenhar_partida()

        if mensagem_tempo > 0:
            mensagem_tempo -= 1

    elif estado == "resultado":

        tela_resultado()
        estado = "menu"

    elif estado == "resultado_campeonato":

        tela_resultado_campeonato()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:

                    if campeonato_finalizado:
                        estado = "classificacao"
                    else:
                        estado = "classificacao"

    elif estado == "classificacao":

        desenhar_classificacao()

        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_RETURN:

                    if campeonato_finalizado:

                        campeonato_ativo = False
                        estado = "menu"

                    else:

                        iniciar_partida("campeonato")

    pygame.display.flip()