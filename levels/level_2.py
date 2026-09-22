from systems.level_generator import generate_basic_level

class Level2:
    def load(self):
        print("ping 2")
        return generate_basic_level(4)