import importlib.util
import traceback
import pygame
import json
import yaml
import sys
import os

ROOT_PATH = os.getenv("ROOT_PATH")
LANG_PATH = os.path.join(ROOT_PATH, "locales")
sys.path.append(ROOT_PATH)
from scripts.character import Character
from scripts.animation import Animation
from scripts.animation_handler import AnimationHandler

class CharacterSelectMenu:
    def __init__(self):
        """Inicializa o menu de seleção de personagens."""
        self.load_settings()
        self.texts = self.load_language(self.settings["language"])
        self.background = pygame.image.load(os.path.join(ROOT_PATH, "assets", "sprites", "luxurious_building", "character-selection-background.png"))
        self.MENUS = []
        self.characters = []
        self.selected_character = 0
        self.character_positions = []
        self.font = None
        self.animation_handler = None
        self.cooldown_click = 0
        self.current_language = self.settings["language"]
        print("🎭 Menu de Seleção de Personagem carregado!")

    def load_language(self, language):
        """Carrega os textos do YAML com base no idioma selecionado."""
        lang_file = os.path.join(LANG_PATH, f"{language}.yml")
        print(f"🌐 Carregando idioma: {lang_file}")
        if os.path.exists(lang_file):
            with open(lang_file, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        return {}

    def load_settings(self):
        """Carrega as configurações do jogo, incluindo o personagem selecionado."""
        if "SETTINGS" in os.environ:
          self.settings = json.loads(os.environ["SETTINGS"])
          print("🔄 Configurações carregadas com sucesso!")
        else:
            self.settings = {"sound": 100, "language": "en", "difficulty": "normal", "selected_character": None}
            self.save_settings(self.settings)
            print("⚠️ Nenhuma configuração encontrada. Criando padrão.")

        # Se houver um personagem salvo, define como o selecionado
        selected_character_name = self.settings.get("selected_character")
        if selected_character_name:
            print(f"🟢 Carregando personagem salvo: {selected_character_name}")
            self.SELECTED_CHARACTER = selected_character_name  # Nome do personagem salvo

        os.environ["SETTINGS"] = json.dumps(self.settings)

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
                module_name = file[:-3]

                try:
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    for attr in dir(module):
                        obj = getattr(module, attr)
                        if isinstance(obj, type) and issubclass(obj, Character) and obj is not Character:
                            character_class = obj
                            character_instance = character_class()
                            animation_handler = character_instance.animation_handler
                            animation_handler.set_animation("idle")
                            characters.append({
                                "name": attr.upper(),
                                "animation_handler": animation_handler,
                                "instance": character_instance
                            })

                            if self.SELECTED_CHARACTER == attr.upper():
                                self.selected_character = len(characters) - 1
                except Exception as e:
                    print(f"⚠️ Erro ao carregar {file}: {e}")
                    traceback.print_exc()

        return characters

    def update(self, params):
        """Gerencia entrada do usuário para selecionar personagens."""
        self.load_settings()

        if self.current_language != self.settings["language"]:
            print("🔄 Idioma alterado. Recarregando textos...")
            self.texts = self.load_language(self.settings["language"])
            self.current_language = self.settings["language"]

        if len(self.MENUS) == 0:
            self.MENUS = params["menus"]
        
        if not self.characters:
            self.characters = self.load_characters()

        keys = params["key_events"]
        mouse_pos = params["mouse_events"]["pos"]
        mouse_click = params["mouse_events"]["buttons"][0]

        if keys["type"] == pygame.KEYDOWN:
            if keys["key"] == pygame.K_LEFT:
                self.selected_character = (self.selected_character - 1) % len(self.characters)
            elif keys["key"] == pygame.K_RIGHT:
                self.selected_character = (self.selected_character + 1) % len(self.characters)
            elif keys["key"] == pygame.K_RETURN:
                self.confirm_selection(params)
            elif keys["key"] == pygame.K_ESCAPE:
                self.exit(params)

        # Verifica clique no personagem
        if mouse_click and self.cooldown_click <= 0:
            for i, (x, y) in enumerate(self.character_positions):
                char_width = self.characters[i]["instance"].width * (1.8 if i == self.selected_character else 1.6)
                char_height = self.characters[i]["instance"].height * (1.8 if i == self.selected_character else 1.6)
                char_rect = pygame.Rect(x - char_width // 2, y - char_height // 2, char_width, char_height)

                if char_rect.collidepoint(mouse_pos):
                    self.selected_character = i
                    self.cooldown_click = 10  # Pequeno cooldown para evitar múltiplos cliques rápidos
                    break

        # Atualiza a animação do personagem selecionado
        if self.characters:
            self.characters[self.selected_character]["animation_handler"].updateState(0.05)

        if self.cooldown_click > 0:
            self.cooldown_click -= 1

    def draw(self, screen):
        """Desenha o menu de seleção de personagem."""
        screen.fill((0, 0, 0))
        
        if self.font is None:
            from assets.fonts.title_font import bitmap_font
            self.font = bitmap_font

        # Redimensiona o background para ocupar toda a tela
        background_width = screen.get_width()
        background_height = screen.get_height()
        scale_background = pygame.transform.scale(self.background, (background_width, background_height))
        screen.blit(scale_background, (0, 0))

        # Título do menu
        title_surface = self.font.render(self.texts["character_select"]["title"], "white", 32)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 100))
        screen.blit(title_surface, title_rect)

        # Configuração para posicionamento dos personagens
        spacing = 200
        start_x = screen.get_width() // 2
        start_y = screen.get_height() // 1.6
        self.character_positions.clear()

        for i, character in enumerate(self.characters):
            x = start_x + (i - self.selected_character) * spacing
            y = start_y
            self.character_positions.append((x, y))

            # Obtém o sprite correto (apenas o primeiro frame para os não selecionados)
            sprite = (character["animation_handler"].get_sprite() 
                      if i == self.selected_character 
                      else character["animation_handler"].animations["idle"].frames[0])

            if sprite:
                # Define tamanhos diferentes para o personagem selecionado
                if i == self.selected_character:
                    width = character["instance"].width * 1.8
                    height = character["instance"].height * 1.8
                else:
                    width = character["instance"].width * 1.6
                    height = character["instance"].height * 1.6

                scaled_sprite = pygame.transform.scale(sprite, (width, height))
                sprite_rect = scaled_sprite.get_rect(center=(x, y))

                # Desenha o nome acima do personagem
                name_surface = self.font.render(character["name"], "white", 16 if i == self.selected_character else 14)
                name_rect = name_surface.get_rect(center=(x, y - height // 2 - 20))  # Nome acima do personagem

                screen.blit(name_surface, name_rect)
                screen.blit(scaled_sprite, sprite_rect)

    def confirm_selection(self, params):
        """Confirma a seleção do personagem e salva no settings.json."""
        if not self.characters:
            return

        try:
            selected_character_data = self.characters[self.selected_character]
            character_name = selected_character_data["name"]
            print(f"✅ Personagem escolhido: {character_name}")

            # Atualiza o personagem selecionado e salva no JSON
            params["main_update"]({
                "selected_character": selected_character_data["instance"],
                "settings": {"selected_character": character_name}
            })

            self.exit(params)
        except Exception as e:
            print(f"⚠️ Erro ao carregar personagem: {e}")
            traceback.print_exc()

    def exit(self, params):
        """Retorna ao menu principal."""
        print("↩ Retornando ao menu principal...")
        params["main_update"]({"current_menu": self.MENUS[0]})

    def late_update(self, params):
        """Atualizações finais do menu."""
        self.draw(params["screen"])