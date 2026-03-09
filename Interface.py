import cv2
import cvzone
import pygame

class Botao:
    def __init__(self, texto, pos, size, cor_base=(50, 50, 50), cor_hover=(0, 200, 0)):
        self.texto = texto
        self.rect = pygame.Rect(pos, size)
        self.cor_base = cor_base
        self.cor_hover = cor_hover
        self.fonte = pygame.font.SysFont("Arial", 32, bold = True)

    def desenhar(self, tela, cursor):
        # verifica a colisao
        colisao = self.rect.collidepoint(cursor)
        cor = self.cor_hover if colisao else self.cor_base

        # desenho do botão
        pygame.draw.rect(tela, (20, 20, 20), (self.rect.x + 5, self.rect.y + 5, self.rect.w, self.rect.h), border_radius=12)
        pygame.draw.rect(tela, cor, self.rect, border_radius=12)
        pygame.draw.rect(tela, (255, 255, 255), self.rect, 3, border_radius=12)

        # renderiza o texto centralizado
        txt_surf = self.fonte.render(self.texto, True, (255,255,255))
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        tela.blit(txt_surf, txt_rect)

        return colisao
    

# Instancie os botões fora do loop para não recriá-los toda hora (ganho de performance)
btn_fases = Botao("FASES", (515, 250), (250, 70))
btn_sair = Botao("SAIR", (515, 450), (250, 70))

def tela_menu_pygame(tela, largura_tela, cursor, click):
    # titulo
    fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    titulo = fonte_titulo.render("MENU PRINCIPAL", True, (255,255,0))
    tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 100))

    if btn_fases.desenhar(tela, cursor) and click:
        return "fases"
    
    if btn_sair.desenhar(tela, cursor) and click:
        return "sair"
    
    return "menu"

def tela_vitoria_pygame(tela, largura_tela, cursor, click):
    # tela com transparencia
    s = pygame.Surface((1280,720))
    s.set_alpha(180) # Nivel de transparencia
    s.fill((0,0,0))
    tela.blit(s, (0,0))

    # Texto de vitoria
    fonte_vitoria = pygame.font.SysFont("Arial", 50, bold=True)
    msg = fonte_vitoria.render("PARABÉNS, VOCÊ VENCEU!", True, (0,255,0))
    tela.blit(msg, (largura_tela // 2 - msg.get_width() // 2, 300))

    btn_cont = Botao("CONTINUAR", (500, 450), (280, 80), cor_base=(0,150,0))
    if btn_cont.desenhar(tela, cursor) and click:
        return True # Indica que clicou para continuar
    
    return False

# Instancia os botoes de fase (melhorar isso)
btn_fase1 = Botao("FASE 1", (200, 250), (200, 60))
btn_fase2 = Botao("FASE 2", (450, 250), (200, 60)) # Exemplo de mais uma fase
btn_voltar = Botao("VOLTAR", (540, 600), (200, 60), cor_base=(100, 100, 100))

def tela_fases_pygame(tela, largura_tela, cursor, click):
    # titulo centralizado
    # Explicação: Faz a superficie do titulo (titulo_surf) e "coloca" ela encima da moldura correta (titulo_rect)
    fonte_titulo = pygame.font.SysFont("Arial", 64, bold=True)
    titulo_surf = fonte_titulo.render("MENU PRINCIPAL", True, (255,255,0))

    titulo_rect = titulo_surf.get_rect(center=(largura_tela // 2, 100))
    tela.blit(titulo_surf, titulo_rect) # blit é a funcao que "carimba" uma superficie numa posicao especifica
    

    # Renderiza os botoes
    if btn_fase1.desenhar(tela, cursor) and click:
        return "jogando", 2 # indica o numero de peças
    
    if btn_fase2.desenhar(tela, cursor) and click:
        return "jogando", 4 
    
    if btn_voltar.desenhar(tela, cursor) and click:
        return "menu", None
    
    print("ping 2")
    return "fases", None