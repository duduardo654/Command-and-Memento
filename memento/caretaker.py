"""
Caretaker
=========
Guarda os checkpoints (mementos) com um rótulo, sem conhecer os
detalhes internos do Document (Originator). Só armazena e devolve.
"""

from memento.memento import DocumentMemento


class Caretaker:
    def __init__(self):
        self._checkpoints: dict[str, DocumentMemento] = {}

    def save_checkpoint(self, name: str, memento: DocumentMemento) -> None:
        self._checkpoints[name] = memento
        print(f"  [Memento] checkpoint '{name}' salvo -> {memento.get_state()!r}")

    def get_checkpoint(self, name: str) -> DocumentMemento:
        return self._checkpoints[name]
