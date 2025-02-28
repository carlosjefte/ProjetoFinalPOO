import pygame
import yaml
import sys
import os
import json

ROOT_PATH = os.getenv("ROOT_PATH")
LANG_PATH = os.path.join(ROOT_PATH, "locales")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

class SettingsMenu:
    def __init__(self):
        """Inicializa o menu de configurações."""
        self.main_update = None
        self.MENUS = []
        self.font = None
        self.options = ["sound", "language", "difficulty", "back"]
        self.background = pygame.image.load(os.path.join(ROOT_PATH, "assets", "sprites", "bar", "settings-background.png"))
        self.selected_option = 0
        self.cooldown_click = 0
        self.open = False
        self.option_positions = []

        # Carrega as configurações e os textos do idioma
        self.settings = self.load_settings()
        self.texts = self.load_language(self.settings["language"])

    def load_settings(self):
        """Carrega as configurações do ENV ou usa valores padrão."""
        return json.loads(os.environ["SETTINGS"])

    def save_settings(self):
        """Salva as configurações no ENV e informa ao jogo."""
        os.environ["SETTINGS"] = json.dumps(self.settings)

        # Recarrega os textos se a linguagem for alterada
        if self.main_update is not None:
            self.main_update({"settings": self.settings})
        self.texts = self.load_language(self.settings["language"])

    def load_language(self, language):
        """Carrega os textos do YAML com base no idioma selecionado."""
        lang_file = os.path.join(LANG_PATH, f"{language}.yml")
        print(f"🌐 Carregando idioma: {lang_file}")
        if os.path.exists(lang_file):
            with open(lang_file, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        return {}

    def update(self, params):
        """Gerencia entrada do usuário para ajustar as configurações."""
        if len(self.MENUS) == 0:
            self.MENUS = params["menus"]
        if not self.main_update:
            self.main_update = params["main_update"]

        if params["key_events"]["key"] == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif params["key_events"]["key"] == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif params["key_events"]["key"] == pygame.K_RETURN:  # Enter confirma
            self.select_option()
        elif params["mouse_events"]["buttons"][0] and self.cooldown_click <= 0:
            self.cooldown_click = 2
            self.select_option()

        # Navegação com mouse
        mouse_x, mouse_y = params["mouse_events"]["pos"]
        for i, (x, y, w, h) in enumerate(self.option_positions):
            if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                self.selected_option = i

        self.cooldown_click -= 1 if self.cooldown_click > 0 else 0

    def select_option(self):
        """Altera configurações ou volta ao menu principal."""
        option = self.options[self.selected_option]

        if option == "sound":
            self.settings["sound"] = "off" if self.settings["sound"] == "on" else "on"
        elif option == "language":
            languages = list(self.texts["languages"].keys())  # Obtém a lista de idiomas disponíveis
            current_index = languages.index(self.settings["language"])
            self.settings["language"] = languages[(current_index + 1) % len(languages)]
        elif option == "difficulty":
            levels = [self.texts["difficulty"]["easy"], self.texts["difficulty"]["medium"], self.texts["difficulty"]["hard"]]
            levels_translate = ["easy", "medium", "hard"]
            current_index = levels_translate.index(self.settings["difficulty"])
            self.settings["difficulty"] = levels_translate[(current_index + 1) % len(levels)]
        elif option == "back":
            self.main_update({"current_menu": self.MENUS[0]}) 

        self.save_settings()

    def draw(self, screen):
        """Desenha o menu de configurações."""
        if self.font is None:
            from assets.fonts.title_font import bitmap_font
            self.font = bitmap_font

        # check if background size is the same as screen size
        screen_width, screen_height = screen.get_size()
        if self.background.get_height() != screen_height:
            factor = screen_width - self.background.get_height()
            self.background = pygame.transform.scale(self.background, (self.background.get_width() + factor, screen_height))

        screen.blit(self.background, (0, 0))

        self.option_positions = []
        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_option else "white"

            if option in self.settings:
                value = self.settings[option]
                if option == "difficulty":
                    value = self.texts["difficulty"].get(value, value)
                text = f"{self.texts['settings'][option]}: {value}".upper()
            else:
                text = self.texts["settings"]["back"]

            text_surface = self.font.render(text, color, 32)
            text_rect = text_surface.get_rect(center=(640, 300 + i * 60))
            self.option_positions.append((text_rect.x, text_rect.y, text_rect.width, text_rect.height))

            screen.blit(text_surface, text_rect)

    def late_update(self, params):
        """Método opcional chamado após o update()."""
        self.draw(params["screen"])