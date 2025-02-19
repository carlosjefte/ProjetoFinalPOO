import pygame
from scripts.objects import Object
from scripts.animation_handler import AnimationHandler
from scripts.gravity_component import GravityComponent
from scripts.collision_component import CollisionComponent

class Character(Object):
    def __init__(self, x, y, width, height, animations, use_gravity=False):
        """
        Representa um personagem no jogo, herdando de Object.

        :param x: Posição X inicial.
        :param y: Posição Y inicial.
        :param width: Largura do personagem.
        :param height: Altura do personagem.
        :param animations: Dicionário de animações {nome: Animation}.
        :param use_gravity: Define se o personagem é afetado pela gravidade.
        """
        super().__init__(x=x, y=y, width=width, height=height, animations=animations, use_gravity=use_gravity, use_collision=True)
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 5

    def move(self, dx, dy):
        """Move o personagem e ajusta a velocidade."""
        self.velocity_x = dx
        self.velocity_y = dy
        self.x += dx
        self.y += dy

        # Define a animação com base no movimento
        if dx != 0:
            self.set_animation("run" if abs(dx) > 2 else "walk")
        elif dy != 0:
            self.set_animation("jump")

    def update(self, pramas):
        """Atualiza a animação, aplica gravidade e resolve colisões."""
        velocity_factor = max(abs(self.velocity_x), abs(self.velocity_y))
        self.animation_handler.updateState(velocity_factor)

        if self.gravity_component:
            self.gravity_component.apply_gravity(pramas["dt"])
            self.y += self.gravity_component.velocity_y

        self.control(keys)

        # Verifica colisões
        for obj in params["collidables"]:
            if obj.collision_component and obj is not self:
                self.collision_component.resolve_collision(obj)

    def control(self, key_events):
        """Controla o movimento do personagem com base nas teclas pressionadas."""
        dx, dy = 0, 0
        if key_events == pygame.K_LEFT:
            dx -= self.speed
        if key_events == pygame.K_RIGHT:
            dx += self.speed
        if key_events == pygame.K_UP:
            dy -= self.speed
        if key_events == pygame.K_DOWN:
            dy += self.speed

        self.move(dx, dy)
        