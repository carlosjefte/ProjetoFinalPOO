import pygame
import json
import yaml
import sys
import os

# 🛠️ Adiciona o diretório raiz ao sys.path para permitir importações
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
# load the ROOT_PATH from the environment
ROOT_PATH = os.getenv("ROOT_PATH")
print(f"🔧 ROOT_PATH: {ROOT_PATH}")
from .character_selection_menu import CharacterSelectMenu
from ui.settings_menu import SettingsMenu

class MainMenu:
    SETTINGS = None
    def __init__(self):
        self.load_texts()
        self.options = [
            self.texts["menu"]["start_game"],
            self.texts["menu"]["settings"],
            self.texts["menu"]["character_select"],
            self.texts["menu"]["exit"],
        ]
        self.selected_option = 0
        self.cooldown_click = 0
        self.option_positions = []
        self.font = None  # 🔥 A fonte será inicializada apenas quando o pygame já estiver rodando
        self.character_select_menu = None  # Instância do menu de seleção de personagem
        self.settings_menu = None  # Instância do menu de configurações
        print("📜 MainMenu carregado!")

    def load_texts(self):
        """Carrega os textos do arquivo YAML."""
        self.SETTINGS = json.loads(os.environ["SETTINGS"])
        with open(os.path.join(ROOT_PATH, "locales", f"{self.SETTINGS['language']}.yml"), "r", encoding="utf-8") as file:
            self.texts = yaml.safe_load(file)

    def update(self, params):
        """Gerencia entrada do usuário via teclado e mouse."""
        # Se o menu de seleção de personagem estiver ativo, delega o update para ele
        if self.character_select_menu:
            self.character_select_menu = self.character_select_menu.update(params)
            return
        elif self.settings_menu:
            self.settings_menu = self.settings_menu.update(params)
            return

        # Navegação com teclado
        if params["key_events"] == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif params["key_events"] == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif params["key_events"] == pygame.K_RETURN:  # Enter confirma a opção
            self.select_option()
        if params["mouse_events"]["buttons"][0] == True and self.cooldown_click <= 0:
            self.cooldown_click = 2
            self.select_option()

        # Navegação com mouse
        mouse_x, mouse_y = params["mouse_events"]["pos"]
        for i, (x, y, w, h) in enumerate(self.option_positions):
            if x <= mouse_x <= x + w and y <= mouse_y <= y + h:
                self.selected_option = i  # Destaca a opção sob o mouse
        
        self.cooldown_click -= 1 if self.cooldown_click > 0 else 0

    def select_option(self):
        """Executa a ação da opção selecionada."""
        option = self.options[self.selected_option]
        print(f"🟢 Selecionado: {option}")

        if option == self.texts["menu"]["start_game"]:
            print("🚀 Iniciando o jogo...")
        elif option == self.texts["menu"]["settings"]:
            print("⚙️ Abrindo Configurações...")
            self.open_settings()
        elif option == self.texts["menu"]["character_select"]:
            print("🎭 Abrindo Seleção de Personagem...")
            self.open_character_select()
        elif option == self.texts["menu"]["exit"]:
            print("❌ Saindo do jogo...")
            pygame.quit()
            exit()

    def open_character_select(self):
        """Abre a tela de seleção de personagem."""
        self.character_select_menu = CharacterSelectMenu(self.texts)

    def open_settings(self):
        """Abre o menu de configurações."""
        self.settings_menu = SettingsMenu()

    def draw(self, screen):
        """Desenha o menu na tela."""
        if self.character_select_menu:
            self.character_select_menu.draw(screen)
            return

        if self.settings_menu:
            self.settings_menu.draw(screen)
            return

        if self.font is None:
            self.font = pygame.font.Font(None, 50)

        screen.fill("black")
        self.option_positions = []  # Reseta as posições calculadas

        for i, option in enumerate(self.options):
            color = "yellow" if i == self.selected_option else "white"
            text_surface = self.font.render(option, True, color)
            text_rect = text_surface.get_rect(center=(640, 300 + i * 60))
            
            # Guarda a posição do texto para detecção do mouse
            self.option_positions.append((text_rect.x, text_rect.y, text_rect.width, text_rect.height))
            
            screen.blit(text_surface, text_rect)

    def late_update(self, params):
        """Método opcional chamado após o update()."""
        self.draw(params["screen"])