import importlib.util
import traceback
import pygame
import sys
import os

ROOT_PATH = os.getenv("ROOT_PATH")
sys.path.append(ROOT_PATH)
from scripts.character import Character
from scripts.animation import Animation
from scripts.animation_handler import AnimationHandler

class CharacterSelectMenu:
    def __init__(self, texts):
        """Inicializa o menu de seleção de personagens."""
        self.texts = texts
        self.characters = self.load_characters()
        self.selected_character = 0
        self.character_positions = []
        self.font = None  # 🔥 A fonte será inicializada apenas quando o pygame já estiver rodando
        self.current_sprite = None
        self.character_instance = None
        self.cooldown_click = 0
        print("🎭 Menu de Seleção de Personagem carregado!")
        self.load_selected_character()

    
    def load_characters(self):
        """Carrega automaticamente todos os personagens da pasta assets/characters/"""
        characters = []
        characters_path = os.path.join(ROOT_PATH, "assets", "characters")
        
        if not os.path.exists(characters_path):
            print("⚠️ Pasta de personagens não encontrada!")
            return characters
        
        for file in os.listdir(characters_path):
            if file.endswith(".py") and file != "__init__.py":
                file_path = os.path.join(characters_path, file)
                module_name = file[:-3]  # Remove o .py do nome do arquivo

                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)  # 🔥 Executa o módulo

                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and issubclass(obj, Character) and obj is not Character:
                            characters.append((attr, module_name))  # 🔥 Salva nome e nome do módulo

                except Exception as e:
                    print(f"⚠️ Erro ao carregar {file}: {e}")
        
        return characters

    def load_selected_character(self):
        """Carrega a animação idle do personagem selecionado."""
        if not self.characters:
            return
        
        character_name, module_name = self.characters[self.selected_character]

        try:
            # 🔥 Importa o módulo dinamicamente
            module = importlib.import_module(f"assets.characters.{module_name}")

            # 🔥 Obtém a classe do personagem
            character_class = getattr(module, character_name)
            self.character_instance = character_class()

            self.animation_handler = self.character_instance.animation_handler
            self.animation_handler.set_animation("idle")  # 🔥 Define a animação inicial

        except Exception as e:
            print(f"⚠️ Erro ao carregar personagem {character_name}: {e}")
            traceback.print_exc()
            self.character_instance = None
            self.animation_handler = None

    def update(self, params):
        """Gerencia entrada do usuário para selecionar personagens."""

        if self.selected_character is None:
            self.selected_character = 0
  
        if params["key_events"] == pygame.K_LEFT:
            self.selected_character = (self.selected_character - 1) % len(self.characters)
            self.load_selected_character()
        elif params["key_events"] == pygame.K_RIGHT:
            self.selected_character = (self.selected_character + 1) % len(self.characters)
            self.load_selected_character()
        elif params["key_events"] == pygame.K_RETURN:  # Enter confirma a escolha
            return self.confirm_selection(params)
        elif params["mouse_events"]["buttons"][0] == True and self.cooldown_click <= 0:
            self.cooldown_click = 2
            return self.confirm_selection(params)
        
        # Navegação com mouse
        mouse_x, mouse_y = params["mouse_events"]["pos"]
        for i, (x, y, w, h) in enumerate(self.character_positions):
            if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                self.selected_option = i

        if self.animation_handler:
            self.animation_handler.updateState(0.05)

        self.draw(params["screen"])
        self.cooldown_click -= 1 if self.cooldown_click > 0 else 0
        return self

    def confirm_selection(self, params):
        """Confirma a seleção do personagem e retorna ao menu principal."""
        if self.selected_character is None or not self.characters:
            return None

        character_name, module_name = self.characters[self.selected_character]

        try:
            print(f"✅ Personagem escolhido: {character_name}")
            params["main_update"]({"selected_character": self.character_instance})
            self.exit()
            return None

        except Exception as e:
            print(f"⚠️ Erro ao carregar personagem {character_name}: {e}")
            return None

    def exit(self):
        """Fecha a seleção de personagem e retorna ao menu principal."""
        print("↩ Retornando ao menu principal...")
        self.selected_character = None

    def draw(self, screen):
        """Desenha o menu de seleção de personagem com a animação redimensionada corretamente."""
        if self.font is None:
            self.font = pygame.font.Font(None, 50)

        screen.fill("darkblue")

        title_surface = self.font.render(self.texts["character_select"]["title"], True, "white")
        title_rect = title_surface.get_rect(center=(640, 100))
        screen.blit(title_surface, title_rect)

        for i, (character, _) in enumerate(self.characters):
            color = "yellow" if i == self.selected_character else "white"
            text_surface = self.font.render(character, True, color)
            text_rect = text_surface.get_rect(center=(640, 300))

            self.character_positions.append((text_rect.x, text_rect.y, text_rect.width, text_rect.height))
            screen.blit(text_surface, text_rect)

        if self.animation_handler:
            current_sprite = self.animation_handler.get_sprite()
            if current_sprite:
                # Obtém a largura e altura do personagem
                width = self.character_instance.width
                height = self.character_instance.height

                scaled_sprite = pygame.transform.scale(current_sprite, (width, height))
                sprite_rect = scaled_sprite.get_rect(center=(640, 400))  # 🔥 Ajustado para posicionamento correto
                screen.blit(scaled_sprite, sprite_rect)