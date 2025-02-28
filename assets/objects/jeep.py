import sys
import os

sys.path.append(os.getenv("ROOT_PATH"))
ROOT_PATH = os.getenv("ROOT_PATH")
from scripts.animation import Animation

class Jeep(Car):
    def __init__(self, x, y, width=0, height=0, use_gravity=False, use_collision=False):
        """
        Classe para jipes que herdam de Car.

        :param x: Posição X inicial
        :param y: Posição Y inicial
        :param width: Largura do objeto (usado para colisão)
        :param height: Altura do objeto (usado para colisão)
        :param use_gravity: Define se o objeto será afetado pela gravidade
        :param use_collision: Define se o objeto terá colisão ativa
        """
        animations = {
            "idle": Animation("./assets/sprites/jeep/idle.png", "./assets/animations/jeep/idle.json", use_velocity=False, loop=True),
            "move": Animation("./assets/sprites/jeep/move.png", "./assets/animations/jeep/move.json", use_velocity=True, loop=True),
        }
        super().__init__(x, y, animations, width, height, use_gravity, use_collision)
        self.velocity_x = -2  # Velocidade horizontal predeterminada
        self.lifetime = 300  # Tempo de vida em frames (5 segundos a 60 FPS)
        self.current_lifetime = 0  # Contador de tempo de vida

    def update(self, params):
        """
        Atualiza o jipe, movendo-o e verificando seu tempo de vida.
        """
        super().update(params)
        self.move(self.velocity_x)  # Move o jipe horizontalmente

        # Atualiza o tempo de vida
        self.current_lifetime += 1
        if self.current_lifetime >= self.lifetime:
            self.destroy()  # Remove o jipe da cena após o tempo de vida expirar

    def destroy(self):
        """
        Remove o jipe da cena.
        """
        # Aqui você pode adicionar lógica para remover o objeto da lista de objetos do jogo
        print("Jeep destroyed!")