import pygame
import json
import yaml
import sys
import os
from random import randint

# 🛠️ Adiciona o diretório raiz ao sys.path para permitir importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

ROOT_PATH = os.getenv("ROOT_PATH")
print(f"🔧 ROOT_PATH: {ROOT_PATH}")

from .character_selection_menu import CharacterSelectMenu
from ui.settings_menu import SettingsMenu
from assets.scenes.main_scene import MainScene

class MainMenu:
    SETTINGS = None
    def __init__(self):
        self.load_texts()
        self.CURRENT_LOCALE = self.SETTINGS["language"]
        self.MENUS = []
        self.open = False
        self.options = [
            self.texts["menu"]["start_game"],
            self.texts["menu"]["settings"],
            self.texts["menu"]["character_select"],
            self.texts["menu"]["exit"],
        ]
        self.selected_option = 0
        self.cooldown_click = 0
        self.option_positions = []
        self.font = None
        self.backgrounds = []
        self.background = []
        self.bg_width = 0
        print("📜 MainMenu carregado!")

    def load_texts(self):
        """Carrega os textos do arquivo YAML."""
        self.SETTINGS = json.loads(os.environ["SETTINGS"])
        with open(os.path.join(ROOT_PATH, "locales", f"{self.SETTINGS['language']}.yml"), "r", encoding="utf-8") as file:
            self.texts = yaml.safe_load(file)
    
    def load_and_scale_background(self, image_path, screen):
        """Carrega e reescala o background para que sua altura preencha a tela sem deformação."""
        screen_width, screen_height = screen.get_size()
        original_image = pygame.image.load(image_path)
        original_width, original_height = original_image.get_size()
        scale_factor = screen_height / original_height
        new_width = int(original_width * scale_factor)
        new_height = screen_height
        scaled_image = pygame.transform.scale(original_image, (new_width, new_height))
        return scaled_image
    
    def setup_backgrounds(self, screen):
        """Carrega os backgrounds e configura a cena."""
        root_path = os.getenv("ROOT_PATH")
        self.backgrounds = [
            self.load_and_scale_background(os.path.join(root_path, "assets", "sprites", "street", "background-1.png"), screen),
            self.load_and_scale_background(os.path.join(root_path, "assets", "sprites", "street", "background-2.png"), screen)
        ]
        self.background = [{"image": self.backgrounds[0], "x": 0, "y": 0}]
        self.bg_width = self.backgrounds[0].get_width()
    
    def update_background(self, screen):
        """Aplica parallax no fundo e adiciona/remova fundos conforme necessário."""
        if len(self.backgrounds) == 0:
            self.setup_backgrounds(screen)
        screen_width, _ = screen.get_size()

        for bg in self.background:
            bg["x"] -= 2

        if self.background[-1]["x"] + self.bg_width <= screen_width + 20:
            new_bg = {
                "image": self.backgrounds[randint(0, 1)],
                "x": self.background[-1]["x"] + self.bg_width,
                "y": 0
            }
            self.background.append(new_bg)

        if self.background[0]["x"] + self.bg_width < -50:
            self.background.pop(0)
    
    def update(self, params):
        """Gerencia entrada do usuário e atualiza a cena."""
        screen = params["screen"]
        self.update_background(screen)

        self.SETTINGS = json.loads(os.environ["SETTINGS"])

        if not self.open:
            self.open = True
        
        if self.CURRENT_LOCALE != self.SETTINGS["language"]:
            self.load_texts()
            self.CURRENT_LOCALE = self.SETTINGS["language"]
            self.options = [
                self.texts["menu"]["start_game"],
                self.texts["menu"]["settings"],
                self.texts["menu"]["character_select"],
                self.texts["menu"]["exit"],
            ]

        if not self.MENUS:
            self.MENUS = params["menus"]

        if params["key_events"] == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif params["key_events"] == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif params["key_events"] == pygame.K_RETURN:
            self.select_option(params)

        if params["mouse_events"]["buttons"][0] == True and self.cooldown_click <= 0:
            self.cooldown_click = 2
            self.select_option(params)

        mouse_x, mouse_y = params["mouse_events"]["pos"]
        for i, (x, y, w, h) in enumerate(self.option_positions):
            if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                self.selected_option = i
        
        self.cooldown_click -= 1 if self.cooldown_click > 0 else 0

    def select_option(self, params):
        """Executa a ação da opção selecionada."""
        option = self.options[self.selected_option]
        print(f"🟢 Selecionado: {option}")

        if option == self.texts["menu"]["start_game"]:
            print("🚀 Iniciando o jogo...")
            self.open_main_scene(params)
        elif option == self.texts["menu"]["settings"]:
            print("⚙️ Abrindo Configurações...")
            self.open_settings(params["main_update"])
        elif option == self.texts["menu"]["character_select"]:
            print("🎭 Abrindo Seleção de Personagem...")
            self.open_character_select(params["main_update"])
        elif option == self.texts["menu"]["exit"]:
            print("❌ Saindo do jogo...")
            self.open = False
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def open_character_select(self, main_update):
        """Abre a tela de seleção de personagem."""
        main_update({"current_menu": self.MENUS[2]})


    def open_settings(self, main_update):
        """Abre o menu de configurações."""
        main_update({"current_menu": self.MENUS[1]})

    def open_main_scene(self, params):
        """Abre a cena principal do jogo."""
        params["main_update"]({"current_menu": None})
        params["main_update"]({"current_scene": MainScene(params["screen"])})
    
    def draw(self, screen):
        """Desenha o menu e o fundo."""
        if not self.open:
            return

        for bg in self.background:
            screen.blit(bg["image"], (bg["x"], bg["y"]))

        if self.font is None:
            from assets.fonts.title_font import bitmap_font
            self.font = bitmap_font
        
        self.option_positions = []
        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_option else "white"
            text_surface = self.font.render(option, color, 32)
            text_rect = text_surface.get_rect(center=(640, 300 + i * 60))
            self.option_positions.append((text_rect.x, text_rect.y, text_rect.width, text_rect.height))
            screen.blit(text_surface, text_rect)
    
    def late_update(self, params):
        """Método chamado após o update()."""
        self.draw(params["screen"])
