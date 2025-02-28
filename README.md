
# Retro 2.5D Game

Este é um jogo 2.5D retro desenvolvido como projeto final para a disciplina de Programação Orientada a Objetos (POO). O jogo possui um sistema de menus interativos, seleção de personagens, e transições de tela com efeitos de fade. 

## Tecnologias Usadas

- **Python 3.x**
- **Pygame**: Usado para o desenvolvimento da interface gráfica e gerenciamento de eventos.
- **JSON**: Para armazenar e carregar configurações do jogo.

## Funcionalidades

- **Menus interativos**: O jogo possui menus como o principal, de configurações e seleção de personagens.
- **Seleção de personagem**: O jogador pode escolher um personagem de uma lista de personagens definidos pelo sistema.
- **Efeitos de fade**: Transições suaves entre menus e telas.
- **Configurações**: O jogo carrega e salva configurações como som, idioma, dificuldade e o personagem selecionado.

## Como Executar

### Requisitos

Certifique-se de ter o Python 3.x instalado e as dependências necessárias. Para instalar as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
```

### Passos para rodar o jogo

1. **Clone o repositório** ou baixe o código.
2. **Instale as dependências** (se necessário):
   ```bash
   pip install -r requirements.txt
   ```
3. **Execute o arquivo principal**:
   ```bash
   python main.py
   ```

### Personalizações

- **Personagens**: Novos personagens podem ser adicionados na pasta `assets/characters/`. Cada personagem deve ser definido em um arquivo Python e herdar a classe `Character`.
- **Configurações**: As configurações são salvas no arquivo `config/settings.json`. A chave `selected_character` pode ser ajustada para definir o personagem que será carregado ao iniciar o jogo.

### Estrutura de Arquivos

- `main.py`: Arquivo principal que inicializa o jogo.
- `assets/`: Contém os recursos do jogo, como personagens e gráficos.
- `locales/`: Contém arquivos de tradução para diferentes idiomas.
- `config/`: Contém o arquivo de configurações `settings.json`.
- `scripts/`: Contém scripts auxiliares, como definição de classes pai.

### Menu e Transições

Ao iniciar o jogo, o jogador será apresentado ao **Main Menu** onde pode acessar as configurações e selecionar o personagem. As transições entre os menus são feitas com efeitos de fade, criando uma experiência suave e profissional.
