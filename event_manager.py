import importlib.util
import inspect
import os

class EventManager:
  MODULE_NAME = "event_manager"
  """Gerencia os objetos que precisam ser atualizados a cada frame."""
  def __init__(self):
    self.subscribers = []

  def subscribe(self, obj):
    """Adiciona um objeto à lista de atualização."""
    if obj not in self.subscribers:
      self.subscribers.append(obj)

  def unsubscribe(self, obj):
    """Remove um objeto da lista de atualização."""
    if obj in self.subscribers:
      self.subscribers.remove(obj)

  def update(self, params):
    """Chama o método update() de todos os inscritos."""
    for obj in self.subscribers:
      obj.update(params)

  def late_update(self, params):
    """Chama o método late_update() de todos os inscritos."""
    for obj in self.subscribers:
      if hasattr(obj, "late_update") and callable(getattr(obj, "late_update")):
        obj.late_update(params)

if __name__ == "__main__":
  event_manager = EventManager()
  print("✅ EventManager inicializado com sucesso!")