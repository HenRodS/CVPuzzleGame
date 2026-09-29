import pygame

class ObstacleSystem:
    """
    Sistema responsável exclusivamente pela lógica de obstáculos:
    - Trata o obstáculo apenas como uma área/espaço de perigo (pygame.Rect).
    - Não trata como objeto de jogo (sem sprites, arrasto ou manipulação física).
    - Detecta colisão entre peças ativas e as áreas de perigo cadastradas.
    - Se qualquer peça encostar na área, sinaliza derrota (Game Over).

    A geração geométrica dos obstáculos e sua renderização na tela
    ficam a cargo dos arquivos específicos de cada fase (ex: level_3.py, level_4.py).
    """
    def __init__(self):
        self.areas = []
        self.ativo = False

    def definir_areas(self, areas):
        """Define a lista de áreas (pygame.Rect ou tuplas) que causam derrota ao toque."""
        self.areas = [pygame.Rect(a) for a in areas]
        self.ativo = len(self.areas) > 0

    def adicionar_area(self, rect_ou_coords):
        """Adiciona uma área de perigo retangular."""
        self.areas.append(pygame.Rect(rect_ou_coords))
        self.ativo = True

    def obter_areas(self):
        """Retorna a lista de áreas de perigo ativas."""
        return self.areas

    def limpar(self):
        """Remove todas as áreas de perigo e desativa o sistema."""
        self.areas.clear()
        self.ativo = False

    def parar(self):
        """Alias para limpar e desativar o sistema."""
        self.limpar()

    def esta_ativo(self):
        """Informa se há áreas de perigo ativas."""
        return self.ativo and len(self.areas) > 0

    def verificar_colisao(self, lista_pecas, tolerancia=14):
        """
        Verifica se alguma peça em jogo (que ainda não foi encaixada no alvo)
        colidiu com qualquer uma das áreas de perigo cadastradas.
        Retorna True caso haja colisão (gerando a derrota).
        """
        if not self.esta_ativo():
            return False

        for peca in lista_pecas:
            # Peças já encaixadas com sucesso no alvo não sofrem colisão
            if not getattr(peca, 'isMatched', False):
                # Reduz o rect da peça com tolerância para desconsiderar bordas transparentes do PNG
                rect_ajustado = peca.rect.inflate(-tolerancia * 2, -tolerancia * 2)
                for area in self.areas:
                    if area.colliderect(rect_ajustado):
                        return True
        return False

    def desenhar(self, tela):
        """
        Método de compatibilidade: o desenho dos obstáculos é realizado
        diretamente no arquivo de cada level específico.
        """
        pass
