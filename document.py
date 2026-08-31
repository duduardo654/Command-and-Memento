"""
Document
========
No padrão COMMAND, esta classe é o "Receiver": quem sabe executar de fato
a ação (digitar / apagar texto).

No padrão MEMENTO, esta mesma classe é o "Originator": quem sabe criar
um snapshot do próprio estado (save) e se restaurar a partir dele (restore).
"""

from memento.memento import DocumentMemento


class Document:
    def __init__(self):
        self.text: str = ""

    # ---- usado pelos Commands (TypeCommand / DeleteCommand) ----
    def type_text(self, text: str) -> None:
        self.text += text

    def delete_last(self, n: int) -> str:
        removed = self.text[-n:]
        self.text = self.text[:-n]
        return removed

    # ---- papel de Originator no Memento ----
    def save(self) -> DocumentMemento:
        """Cria um Memento (snapshot) do estado atual."""
        return DocumentMemento(self.text)

    def restore(self, memento: DocumentMemento) -> None:
        """Restaura o documento para o estado salvo no memento."""
        self.text = memento.get_state()

    def __str__(self) -> str:
        return f'"{self.text}"'
