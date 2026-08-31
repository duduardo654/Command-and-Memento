"""
DocumentMemento (Memento)
=========================
Objeto imutável que guarda uma cópia do estado do Document (Originator).
Quem guarda a lista de mementos (Caretaker) não enxerga/mexe no conteúdo,
só repassa o objeto de volta para o Originator quando precisa restaurar.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentMemento:
    _state: str

    def get_state(self) -> str:
        return self._state
