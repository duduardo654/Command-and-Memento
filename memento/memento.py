"""
TVMemento (Memento)
====================
Objeto imutável que guarda uma cópia do estado da TV (canal + volume).
Quem guarda a lista de mementos (PresetManager) não enxerga/mexe nesses
valores, só repassa o objeto de volta para a TV quando precisa restaurar.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TVMemento:
    canal: int
    volume: int
