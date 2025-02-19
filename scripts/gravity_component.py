class GravityComponent:
    def __init__(self, gravity=9.8, terminal_velocity=50):
        """
        Componente de gravidade para ser adicionado a objetos.

        :param gravity: Intensidade da gravidade (padrão: 9.8).
        :param terminal_velocity: Velocidade máxima de queda.
        """
        self.gravity = gravity
        self.terminal_velocity = terminal_velocity
        self.velocity_y = 0  # Velocidade inicial de queda

    def apply_gravity(self, dt):
        """Aplica a gravidade ao objeto."""
        self.velocity_y = min(self.velocity_y + self.gravity * dt, self.terminal_velocity)

    def reset_velocity(self):
        """Reseta a velocidade de queda (usado ao tocar o chão)."""
        self.velocity_y = 0