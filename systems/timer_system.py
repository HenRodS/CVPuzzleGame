import pygame

class TimerSystem:
    """Responsável apenas pela lógica e controle do tempo."""
    def __init__(self, duracao_padrao=30):
        self.duracao_padrao = duracao_padrao
        self.duracao_ms = int(duracao_padrao * 1000)
        self.start_ticks = 0
        self.tempo_restante_ms = self.duracao_ms
        self.pausado = False
        self.esgotado = False

    def iniciar(self, duracao_segundos=None):
        """Inicia ou reinicia a contagem do tempo."""
        if duracao_segundos is not None:
            self.duracao_ms = int(duracao_segundos * 1000)
        else:
            self.duracao_ms = int(self.duracao_padrao * 1000)
            
        self.start_ticks = pygame.time.get_ticks()
        self.tempo_restante_ms = self.duracao_ms
        self.pausado = False
        self.esgotado = False

    def pausar(self):
        """Pausa o temporizador (usado na vitória)."""
        self.pausado = True

    def atualizar(self):
        """Atualiza a contagem de tempo. Deve ser chamado no loop principal."""
        if self.pausado or self.esgotado:
            return

        passado = pygame.time.get_ticks() - self.start_ticks
        self.tempo_restante_ms = max(0, self.duracao_ms - passado)

        if self.tempo_restante_ms <= 0:
            self.esgotado = True

    def esta_esgotado(self):
        """Retorna se o tempo acabou."""
        return self.esgotado

    def tempo_restante_segundos(self):
        """Retorna o tempo restante em segundos (arredondado para cima)."""
        return max(0, (self.tempo_restante_ms + 999) // 1000)

    def get_progresso(self):
        """Retorna o progresso atual como um valor entre 0.0 e 1.0."""
        if self.duracao_ms > 0:
            return max(0.0, min(1.0, self.tempo_restante_ms / self.duracao_ms))
        return 0.0