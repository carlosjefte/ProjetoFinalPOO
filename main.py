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
        
        while running:
            key_event = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                elif event.type == pygame.KEYDOWN:
                    key_event = event.key

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

    def save_settings(self, settings):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as file:
            json.dump(settings, file, indent=4)
        self.SETTINGS = settings
        print("💾 Configurações salvas com sucesso!")

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, "r", encoding="utf-8") as file:
                self.SETTINGS = json.load(file)
            print("🔄 Configurações carregadas com sucesso!")
        else:
            self.SETTINGS = {"sound": 100, "language": "en", "difficulty": "normal"}
            self.save_settings(self.SETTINGS)
            print("⚠️ Nenhuma configuração encontrada. Criando padrão.")
            
        os.environ["SETTINGS"] = json.dumps(self.SETTINGS)

if __name__ == "__main__":
    Main()