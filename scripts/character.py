import pygame
from scripts.objects import Object
from scripts.animation_handler import AnimationHandler
from scripts.gravity_component import GravityComponent
from scripts.collision_component import CollisionComponent

class Character(Object):
    def __init__(self, x, y, width, height, animations, use_gravity=False, min_y=0, max_y=0):
        super().__init__(x=x, y=y, width=width, height=height, animations=animations, use_gravity=use_gravity, use_collision=True)
        self.velocity_x = 0
        self.velocity_y = 0
        self.walk_speed = 5
        self.max_y = max_y  # 🔥 Posição do chão
        self.min_y = min_y
        self.speed = self.walk_speed
        self.gravity = 0.6
        self.jump_force = 12  # 🔥 Força inicial do pulo
        self.jump_time = 0
        self.max_jump_time = 30  # 🔥 Tempo máximo que pode segurar o pulo
        self.jump_cooldown = 0
        self.is_jumping = False
        self.top_speed = 10
        self.landing_y = self.max_y  # 🔥 Guarda a altura em que o personagem deveria estar no chão

    def move(self, dx, dy):
        """Move o personagem no chão e permite movimentação limitada no eixo Y."""
        self.velocity_x = dx
        self.velocity_y = dy / 2  # 🔥 Mantém movimentação fluida

        screen_height = pygame.display.get_surface().get_height()
        current_y = screen_height - self.y - self.height / 2

        # 🔥 Só muda de animação quando aterrissa
        if not self.is_jumping:
            if self.velocity_x != 0 or self.velocity_y != 0:
                self.set_animation("run" if abs(self.velocity_x) > self.walk_speed else "walk")
            else:
                self.set_animation("idle")

        if not self.is_jumping:
            if current_y > self.min_y and dy > 0 or current_y < self.max_y and dy < 0:
                self.y += dy
            self.landing_y += dy

        if self.is_jumping:
            self.set_animation("jump")

        if dx != 0:
            if dx < 0:
                self.animation_handler.current_animation.set_flipped(True)
            elif dx > 0:
                self.animation_handler.current_animation.set_flipped(False)

    def jump(self):
        """Inicia o pulo e mantém a altura de pouso fixa."""
        if not self.is_jumping and self.jump_cooldown <= 0:
            self.is_jumping = True
            self.jump_time = 0
            self.velocity_y = -self.jump_force  # 🔥 Impulso inicial para cima
            self.landing_y = self.y  # 🔥 Guarda a altura para aterrissagem

    def update(self, params):
        """Atualiza animações, aplica gravidade e resolve colisões."""
        if self.is_jumping:
            # 🔥 Movimento de arco: desacelera ao subir, acelera ao cair
            self.velocity_y += self.gravity  # 🔥 Aplica gravidade para criar o arco
            self.y += self.velocity_y

            # 🔥 Quando atinge a altura exata de pouso, aterrissa
            if self.y >= self.landing_y:
                self.y = self.landing_y
                self.is_jumping = False
                self.jump_time = 0
                self.velocity_y = 0
                self.jump_cooldown = 10  # 🔥 Pequeno cooldown para evitar spam de pulo

        self.control(pygame.key.get_pressed())

        for obj in params["collidables"]:
            if obj.collision_component and obj is not self:
                self.collision_component.resolve_collision(obj)
        
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1

    def control(self, keys):
        """Controla o personagem."""
        dx, dy = 0, 0
        if keys[pygame.K_LSHIFT]:
            self.speed = min(self.speed + 0.1, self.walk_speed * 2)
        else:
            self.speed = min(self.speed + 0.1, self.walk_speed)
        if keys[pygame.K_LEFT]:
            dx -= self.speed
        if keys[pygame.K_RIGHT]:
            dx += self.speed
        if keys[pygame.K_UP]:  # 🔥 Mantém movimentação no chão
            dy -= self.speed
        if keys[pygame.K_DOWN]:  # 🔥 Mantém movimentação no chão
            dy += self.speed
        if keys[pygame.K_SPACE]:  # 🔥 Agora o jogador pode segurar para pular mais alto
            self.jump()

        self.move(dx, dy)

    def set_position(self, x, y):
        """Define a posição do personagem."""
        self.x = x
        self.y = y

    def draw(self, screen):
        """Desenha o personagem na tela."""
        sprite = self.animation_handler.get_sprite()
        if sprite:
            scaled_sprite = pygame.transform.scale(sprite, (self.width, self.height))
            screen.blit(scaled_sprite, (self.x - self.width // 2, self.y - self.height // 2))

    def late_update(self, params):
        """Atualização tardia para ajustar a posição do personagem."""
        velocity_factor = max(abs(self.velocity_x), abs(self.velocity_y))
        velocity_factor = min(0.15, velocity_factor / self.speed)
        self.animation_handler.updateState(velocity_factor)
        self.draw(params["screen"])
        