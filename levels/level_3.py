from systems.level_generator import generate_fixed_level

class Level3:
    tempo = 60

    def load(self):
        print("ping 3")
        return generate_fixed_level(qtd_pecas=2)

    def setup_obstacles(self, obstacle_system, largura=1280, altura=720):
        """Inicia e configura a barreira vertical no sistema de obstáculos."""
        obstacle_system.configurar_barreira_vertical_fase3(largura_tela=largura, altura_tela=altura)
