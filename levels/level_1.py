from systems.level_generator import generate_basic_level

class Level1:
    tempo = 30

    def load(self):
        print("ping 1")
        return generate_basic_level(2)

    def setup_obstacles(self, obstacle_system):
        obstacle_system.limpar()

    def desenhar_obstaculos(self, tela):
        pass
