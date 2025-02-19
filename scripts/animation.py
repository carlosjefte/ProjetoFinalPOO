import pygame
import json

class Animation:
    def __init__(self, spritesheet_path, json_path, use_velocity=False, loop=True):
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        self.frames = self.load_frames(json_path)
        self.animation_speed = 1
        self.current_frame = 0
        self.animation_time = 0
        self.use_velocity = use_velocity
        self.flipped = False
        self.loop = loop

    def load_frames(self, json_path):
        """Carrega os frames da spritesheet com base no JSON."""
        with open(json_path, "r") as file:
            data = json.load(file)

        frames = []
        for frame_info in data:
            x, y, width, height = frame_info["x"], frame_info["y"], frame_info["width"], frame_info["height"]
            frame = self.spritesheet.subsurface(pygame.Rect(x, y, width, height))
            frames.append(frame)

        return frames

    def frame_count(self):
        """Retorna o número total de frames na animação."""
        return len(self.frames)

    def update(self, velocity_factor=0):
        """Atualiza o frame da animação respeitando a velocidade e o loop."""

        if self.current_frame < len(self.frames) - 1 or self.loop:
            self.animation_time += 1 * velocity_factor if self.use_velocity else 1
            if self.animation_time >= self.animation_speed:
                self.animation_time = 0
                if self.loop:
                    self.current_frame = (self.current_frame + 1) % len(self.frames)
                else:
                    self.current_frame = min(self.current_frame + 1, len(self.frames) - 1)

    def set_loop(self, state):
        """Define se a animação deve repetir em loop."""
        self.loop = state

    def set_flipped(self, state):
        """Define se o sprite deve ser espelhado horizontalmente."""
        self.flipped = state

    def set_speed(self, new_speed):
        """Ajusta a velocidade da animação."""
        self.animation_speed = max(1, new_speed)  # Evita valores inválidos

    def get_frame(self):
        """Retorna o frame atual da animação, invertendo se necessário."""
        frame = self.frames[self.current_frame]
        if self.flipped:
            frame = pygame.transform.flip(frame, True, False)
        return frame
