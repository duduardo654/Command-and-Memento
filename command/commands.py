"""
Command (interface) + Concrete Commands
========================================
Command  -> interface comum, declara execute()/undo()
TypeCommand / DeleteCommand -> comandos concretos, cada um sabe como
    executar a própria ação sobre o Receiver (Document) e como desfazê-la.
"""

from abc import ABC, abstractmethod
from document import Document


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class TypeCommand(Command):
    """Comando concreto: digitar um texto."""
    def __init__(self, document: Document, text: str):
        self.document = document
        self.text = text

    def execute(self) -> None:
        self.document.type_text(self.text)

    def undo(self) -> None:
        self.document.delete_last(len(self.text))


class DeleteCommand(Command):
    """Comando concreto: apagar os últimos N caracteres."""
    def __init__(self, document: Document, n: int):
        self.document = document
        self.n = n
        self._deleted = ""  # guarda o que foi apagado, para o undo

    def execute(self) -> None:
        self._deleted = self.document.delete_last(self.n)

    def undo(self) -> None:
        self.document.type_text(self._deleted)
