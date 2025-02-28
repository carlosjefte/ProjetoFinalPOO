import pygame
from scripts.animation_handler import AnimationHandler
from scripts.gravity_component import GravityComponent
from scripts.collision_component import CollisionComponent

class Car(Object):
    def __init__(self, x, y, animations, width=0, height=0, use_gravity=False, use_collision=False):
        """
        Classe para carros que herdam de Object e são afetados pelo efeito de parallax.

        :param x: Posição X inicial
        :param y: Posição Y inicial
        :param animations: Dicionário de animações {nome: Animation}
        :param width: Largura do objeto (usado para colisão)
        :param height: Altura do objeto (usado para colisão)
        :param use_gravity: Define se o objeto será afetado pela gravidade
        :param use_collision: Define se o objeto terá colisão ativa
        """
        super().__init__(x, y, animations, width, height, use_gravity, use_collision)
        self.velocity_x = 0  # Velocidade horizontal do carro

    def move(self, dx):
        """
        Move o carro horizontalmente.

        :param dx: Deslocamento horizontal
        """
        self.velocity_x = dx
        self.x += dx

    def update(self, params):
        """
        Atualiza a posição do carro com base no efeito de parallax.
        """
        super().update(params.get("dt", 0))
        delta_x = params.get("delta_x", 0)  # Obtém delta_x dos parâmetros
        self.x += delta_x  # Ajusta a posição do carro com base no parallax

    def late_update(self, params):
        """
        Atualiza a posição do carro e desenha na tela.
        """
        super().late_update(params)