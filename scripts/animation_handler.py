class AnimationHandler:
    def __init__(self, animations, default_animation="idle"):
        """
        Gerencia as animações do personagem.

        :param animations: Dicionário de animações {nome: Animation}
        :param default_animation: Animação inicial
        """
        self.animations = animations
        self.current_animation = animations.get(default_animation, None)
        if self.current_animation is None:
            raise ValueError(f"A animação padrão '{default_animation}' não foi encontrada!")
        self.velocity = 0.1  # Velocidade inicial

    def set_animation(self, name):
        """Muda a animação atual."""
        if name in self.animations and self.current_animation != self.animations[name]:
            self.current_animation = self.animations[name]
            self.current_animation.reset()

    def updateState(self, velocity=0.1):
        """Atualiza a animação, levando em conta a velocidade caso necessário."""
        self.velocity = velocity
        if self.current_animation:
            self.current_animation.update(velocity)

    def get_sprite(self):
        """Retorna o sprite da animação atual."""
        return self.current_animation.get_frame() if self.current_animation else None