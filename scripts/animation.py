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

        # Calcula o tamanho máximo dos frames para manter a consistência da animação
        self.max_width, self.max_height = self.get_max_sprite_size()
        self.frames = self.normalize_frames(self.frames, self.max_width, self.max_height)

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

    def get_max_sprite_size(self):
        """Percorre todos os frames para encontrar o maior tamanho."""
        max_width = 0
        max_height = 0
        for frame in self.frames:
            width, height = frame.get_size()
            max_width = max(max_width, width)
            max_height = max(max_height, height)
        return max_width, max_height

    def normalize_frames(self, frames, max_width, max_height):
        """Ajusta os frames menores adicionando espaço transparente apenas na parte superior para manter o tamanho fixo."""
        normalized_frames = []
        for frame in frames:
            original_width, original_height = frame.get_size()

            # Criar um novo canvas transparente do tamanho do maior frame
            canvas = pygame.Surface((max_width, max_height), pygame.SRCALPHA)
            canvas.fill((0, 0, 0, 0))  # Fundo transparente

            # Centralizar horizontalmente e alinhar pela base
            x_offset = (max_width - original_width) // 2
            y_offset = max_height - original_height  # Alinha os pés na base do canvas

            # Desenhar o frame no canvas
            canvas.blit(frame, (x_offset, y_offset))
            normalized_frames.append(canvas)

        return normalized_frames

    def frame_count(self):
        """Retorna o número total de frames na animação."""
        return len(self.frames)

    def update(self, velocity_factor=0):
        """Atualiza o frame da animação respeitando a velocidade e o loop."""
        if self.current_frame < len(self.frames) - 1 or self.loop:
            self.animation_time += 1 * velocity_factor if self.use_velocity else 0.05
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

    def reset(self):
        """Reinicia a animação."""
        self.current_frame = 0
        self.animation_time = 0