from systems.level_generator import generate_basic_level

class Level2:
    tempo = 45

    def load(self):
        print("ping 2")
        return generate_basic_level(4)

    def setup_obstacles(self, obstacle_system):
        obstacle_system.limpar()

    def desenhar_obstaculos(self, tela):
        pass