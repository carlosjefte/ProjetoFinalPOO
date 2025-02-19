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

CONFIG_PATH = os.path.join(ROOT_PATH, "config", "settings.json")

class Main:
    SELECTED_CHARACTER = None
    COLLIDABLES = []
    SETTINGS = {}

    def __init__(self):
        self.load_settings()
        self.event_manager = EventManager()
        self.__subscribe_main_events()
        self.run()

    def __subscribe_main_events(self):
        self.event_manager.subscribe(MainMenu())
        print(f"Eventos inscritos: {self.event_manager.subscribers}")

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 720))
        clock = pygame.time.Clock()
        running = True
        dt = 0

        while running:
            key_event = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_event = event.key

            pygame.display.flip()

            update_params = {
                "dt": dt,
                "screen": screen,
                "main_update": self.main_update,
                "collidables": self.COLLIDABLES,
                "key_events": key_event,
                "mouse_events": {"pos": pygame.mouse.get_pos(), "buttons": pygame.mouse.get_pressed()}
            }

            self.event_manager.update(update_params)
            self.event_manager.late_update(update_params)

            dt = clock.tick(60) / 1000

        pygame.quit()

    def main_update(self, params):
        if "selected_character" in params:
            print(f"🔵 Personagem selecionado: {params['selected_character']}")
            self.SELECTED_CHARACTER = params["selected_character"]
        if "collidable" in params:
            self.COLLIDABLES.append(params["collidable"])
        if "settings" in params:
            self.save_settings(params["settings"])

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