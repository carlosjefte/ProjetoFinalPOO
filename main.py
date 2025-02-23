import pygame
import os
import sys
import json

ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
LANG_PATH = os.path.join(ROOT_PATH, "locales")
os.environ["ROOT_PATH"] = ROOT_PATH
os.environ["LANG_PATH"] = LANG_PATH

from event_manager import EventManager
from ui.main_menu import MainMenu
from ui.settings_menu import SettingsMenu
from ui.character_selection_menu import CharacterSelectMenu
from scripts.character import Character
from ui.bitmap_font import BitmapFont

CONFIG_PATH = os.path.join(ROOT_PATH, "config", "settings.json")

class Main:
    SELECTED_CHARACTER = None
    MENUS = []
    CURRENT_MENU = None
    CURRENT_SCENE = None
    COLLIDABLES = []
    SETTINGS = {}

    FADE_SURFACE = None
    FADE_ALPHA = 0
    FADING = False
    FADE_OUT = True
    NEXT_MENU = None

    def __init__(self):
        self.load_settings()
        self.event_manager = EventManager()
        self.__subscribe_main_events()
        self.run()

    def __subscribe_main_events(self):
        self.MENUS = [MainMenu(), SettingsMenu(), CharacterSelectMenu()]
        self.CURRENT_MENU = self.MENUS[0]
        self.__update_menus()

    def __update_menus(self):
        for menu in self.MENUS:
            if menu != self.CURRENT_MENU:
                self.event_manager.unsubscribe(menu)

        if self.CURRENT_MENU:
            self.event_manager.subscribe(self.CURRENT_MENU)
            print(f"📜 Menu atual: {self.CURRENT_MENU}")
            print(f"Eventos inscritos: {self.event_manager.subscribers}")

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True
        click_cooldown = 0
        dt = 0
        
        self.FADE_SURFACE = pygame.Surface((1280, 720))
        self.FADE_SURFACE.fill((0, 0, 0))

        if "selected_character" in self.SETTINGS:
            print(f"🔵 Personagem selecionado: {self.SETTINGS['selected_character']}")
            self.SELECTED_CHARACTER = self.get_character()
        
        while running:
            key_event = {"key": None, "type": None}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    key_event = {"key": event.key, "type": pygame.KEYDOWN}
                elif event.type == pygame.KEYUP:
                    key_event = {"key": event.key, "type": pygame.KEYUP}

            pygame.display.flip()
            mouse_pressed_event = pygame.mouse.get_pressed()
            if click_cooldown > 0:
                mouse_pressed_event = (False, False, False)
            else:
                click_cooldown = 5
            update_params = {
                "dt": dt,
                "screen": screen,
                "main_update": self.main_update,
                "collidables": self.COLLIDABLES,
                "key_events": key_event,
                "mouse_events": {"pos": pygame.mouse.get_pos(), "buttons": mouse_pressed_event},
                "selected_character": self.SELECTED_CHARACTER,
                "event_manager": self.event_manager,
                "menus": self.MENUS,
            }
            
            if self.FADING:
                self.handle_fade(screen)
            else:
                self.event_manager.update(update_params)
                self.event_manager.late_update(update_params)

            dt = clock.tick(60) / 1000
            click_cooldown -= 1

        pygame.quit()

    def main_update(self, params):
        if "selected_character" in params:
            print(f"🔵 Personagem selecionado: {params['selected_character']}")
            self.SELECTED_CHARACTER = params["selected_character"]
        if "collidable" in params:
            self.COLLIDABLES.append(params["collidable"])
        if "settings" in params:
            self.save_settings(params["settings"])
        if "current_scene" in params:
            self.CURRENT_SCENE = params["current_scene"]
            self.event_manager.subscribe(self.CURRENT_SCENE)
        if "current_menu" in params:
            self.start_fade(params["current_menu"])

    def get_character(self):
        characters = []

        characters_path = os.path.join(ROOT_PATH, "assets", "characters")
        for file in os.listdir(characters_path):
            if file.endswith(".py") and file != "__init__.py":
                character_module = file.replace(".py", "")
                print(f"🔵 Importando personagem: {character_module}")

                try:
                    module = __import__(f"assets.characters.{character_module}", fromlist=[character_module])
                    class_name = character_module.capitalize()  # Assume que a classe tem o mesmo nome do arquivo com a primeira letra maiúscula
                    character_class = getattr(module, class_name, None)

                    print(f"🔵 Classe encontrada: {character_class}\nNome da Classe: {class_name}")

                    if character_class and issubclass(character_class, Character):
                        characters.append(character_class())
                except Exception as e:
                    print(f"⚠️ Erro ao importar {character_module}: {e}")

        # Busca o personagem correspondente no JSON
        return next(
            (char for char in characters if char.__class__.__name__.upper() == self.SETTINGS["selected_character"].upper()),
            None
        )

    def start_fade(self, next_menu):
        """Inicia a transição de fade para o novo menu."""
        self.FADING = True
        self.FADE_ALPHA = 0 if not self.FADE_OUT else 255
        self.NEXT_MENU = next_menu
        self.FADE_OUT = True  # Primeiro, fazer fade para preto

    def handle_fade(self, screen):
        """Realiza o efeito de fade in/out durante a troca de menus."""
        if self.FADE_OUT:
            self.FADE_ALPHA += 15  # Velocidade do fade (ajuste se necessário)
            if self.FADE_ALPHA >= 255:
                self.FADE_ALPHA = 255
                self.FADE_OUT = False  # Agora começa o fade in
                self.CURRENT_MENU = self.NEXT_MENU
                self.__update_menus()
        else:
            self.FADE_ALPHA -= 15
            if self.FADE_ALPHA <= 0:
                self.FADE_ALPHA = 0
                self.FADING = False  # Transição concluída
        
        self.FADE_SURFACE.set_alpha(self.FADE_ALPHA)
        screen.blit(self.FADE_SURFACE, (0, 0))
        pygame.display.update()

    def save_settings(self, new_settings):
        """Atualiza ou adiciona configurações sem remover as existentes."""
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)

        # Carrega as configurações existentes, se houver
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                current_settings = json.load(file)
        else:
            current_settings = {}

        # Atualiza apenas as chaves fornecidas sem remover as outras
        current_settings.update(new_settings)

        # Salva de volta no arquivo JSON
        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(current_settings, file, indent=4)

        # Atualiza o dicionário de configurações da classe
        self.SETTINGS = current_settings

        print("💾 Configurações salvas com sucesso!")

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                self.SETTINGS = json.load(file)
            print("🔄 Configurações carregadas com sucesso!")
        else:
            self.SETTINGS = {"sound": 100, "language": "en", "difficulty": "normal", "selected_character": None}
            self.save_settings(self.SETTINGS)
            print("⚠️ Nenhuma configuração encontrada. Criando padrão.")
            
        os.environ["SETTINGS"] = json.dumps(self.SETTINGS)

if __name__ == "__main__":
    Main()