class CollisionComponent:
    def __init__(self, owner, width, height):
        """
        Componente de colisão para impedir atravessamento de objetos.

        :param owner: Referência ao objeto que possui este componente.
        :param width: Largura do objeto.
        :param height: Altura do objeto.
        """
        self.owner = owner
        self.width = width
        self.height = height

    def check_collision(self, other):
        """
        Verifica se há colisão com outro objeto que também tenha um `CollisionComponent`.

        :param other: Outro objeto com `CollisionComponent`.
        :return: True se houver colisão, False caso contrário.
        """
        if not isinstance(other, CollisionComponent):
            return False

        return (
            self.owner.x < other.owner.x + other.width and
            self.owner.x + self.width > other.owner.x and
            self.owner.y < other.owner.y + other.height and
            self.owner.y + self.height > other.owner.y
        )

    def resolve_collision(self, other):
        """
        Resolve a colisão empurrando o objeto de volta.

        :param other: Outro objeto com `CollisionComponent`.
        """
        if self.check_collision(other):
            if self.owner.gravity_component:  # Se o objeto tem gravidade, impede a queda
                self.owner.gravity_component.reset_velocity()
                self.owner.y = other.owner.y - self.height  # Mantém o objeto acima do chão