import pygame
from scripts.animation_handler import AnimationHandler
from scripts.gravity_component import GravityComponent
from scripts.collision_component import CollisionComponent

class Object:
    def __init__(self, x, y, animations, width=0, height=0, use_gravity=False, use_collision=False):
        """
        Classe base para objetos interativos do jogo.

        :param x: Posição X inicial
        :param y: Posição Y inicial
        :param animations: Dicionário de animações {nome: Animation}
        :param width: Largura do objeto (usado para colisão)
        :param height: Altura do objeto (usado para colisão)
        :param use_gravity: Define se o objeto será afetado pela gravidade
        :param use_collision: Define se o objeto terá colisão ativa
        """
        self.x = x
        self.y = y
        self.animation_handler = AnimationHandler(animations=animations)
        self.gravity_component = GravityComponent() if use_gravity else None
        self.collision_component = CollisionComponent(self, width, height) if use_collision else None

    def set_animation(self, animation_name):
        """Define a animação atual do objeto."""
        self.animation_handler.set_animation(animation_name)

    def update(self, dt):
        """Atualiza a animação do objeto."""
        self.animation_handler.updateState()

        if self.gravity_component:
            self.gravity_component.apply_gravity(dt)
            self.y += self.gravity_component.velocity_y

    def draw(self, screen):
        """Desenha o objeto na tela com a escala definida por width e height."""
        sprite = self.animation_handler.get_sprite()
        if sprite:
            if self.collision_component:  # 🔥 Se houver colisão, usamos o tamanho definido
                scaled_sprite = pygame.transform.scale(sprite, (self.collision_component.width, self.collision_component.height))
            else:
                scaled_sprite = sprite  # Usa o tamanho original se não houver colisão

            screen.blit(scaled_sprite, (self.x, self.y))