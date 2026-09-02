"""
PresetManager (Caretaker)
==========================
Guarda os "presets" (mementos) com um nome, tipo "Modo Filme" ou
"Modo Jogo". Não conhece os detalhes internos da TV, só armazena e
devolve os snapshots quando pedido.
"""

from memento.memento import TVMemento


class PresetManager:
    def __init__(self):
        self._presets: dict[str, TVMemento] = {}

    def salvar_preset(self, nome: str, memento: TVMemento) -> None:
        self._presets[nome] = memento
        print(f"  [Memento] preset '{nome}' salvo -> canal {memento.canal}, volume {memento.volume}")

    def obter_preset(self, nome: str) -> TVMemento:
        return self._presets[nome]
