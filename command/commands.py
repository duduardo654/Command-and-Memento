"""
Command (interface) + Concrete Commands
========================================
Command -> interface comum, declara execute()/undo()
TurnOnCommand / TurnOffCommand / VolumeUpCommand / VolumeDownCommand /
ChangeChannelCommand -> comandos concretos. Cada um encapsula UMA ação
e sabe como aplicá-la na TV (Receiver) e como desfazê-la.

Repare que nenhum desses comandos sabe que existe um "RemoteControl".
Eles só conhecem a TV. Quem decide QUANDO executá-los é o Invoker.
"""

from abc import ABC, abstractmethod
from tv import TV


class Command(ABC):
    @abstractmethod
    def execute(self) -> None: ...

    @abstractmethod
    def undo(self) -> None: ...


class TurnOnCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self) -> None:
        self.tv.ligar()

    def undo(self) -> None:
        self.tv.desligar()


class TurnOffCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self) -> None:
        self.tv.desligar()

    def undo(self) -> None:
        self.tv.ligar()


class VolumeUpCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self) -> None:
        self.tv.aumentar_volume()

    def undo(self) -> None:
        self.tv.diminuir_volume()


class VolumeDownCommand(Command):
    def __init__(self, tv: TV):
        self.tv = tv

    def execute(self) -> None:
        self.tv.diminuir_volume()

    def undo(self) -> None:
        self.tv.aumentar_volume()


class ChangeChannelCommand(Command):
    def __init__(self, tv: TV, novo_canal: int):
        self.tv = tv
        self.novo_canal = novo_canal
        self._canal_anterior = None

    def execute(self) -> None:
        self._canal_anterior = self.tv.canal
        self.tv.mudar_canal(self.novo_canal)

    def undo(self) -> None:
        self.tv.mudar_canal(self._canal_anterior)
