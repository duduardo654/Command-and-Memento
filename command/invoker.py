"""
Editor (Invoker)
================
Dispara comandos e mantém o histórico deles, para permitir undo.
Não conhece a lógica interna de cada comando nem do Document
(o Receiver) — só chama execute()/undo().
"""

from typing import List
from document import Document
from command.commands import Command


class Editor:
    def __init__(self, document: Document):
        self.document = document
        self._history: List[Command] = []

    def run(self, command: Command) -> None:
        command.execute()
        self._history.append(command)
        print(f"  [Command] executado -> {self.document}")

    def undo_last(self) -> None:
        if not self._history:
            print("  [Command] nada para desfazer")
            return
        command = self._history.pop()
        command.undo()
        print(f"  [Command] undo -> {self.document}")
