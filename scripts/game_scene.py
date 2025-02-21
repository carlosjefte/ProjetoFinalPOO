
class GameScene:
    def __init__(self, screen):
        """
        Cena principal do jogo.

        :param screen: Superfície onde a cena será desenhada.
        """
        self.screen = screen
        self.objects = []

    def add_object(self, obj):
        """Adiciona um objeto à cena."""
        self.objects.append(obj)

    def update(self, params):
        """Atualiza todos os objetos na cena."""
        for obj in self.objects:
            obj.update(params)

    def late_update(self, params):
        """Atualiza todos os objetos na cena após o update."""
        for obj in self.objects:
            obj.late_update(params)