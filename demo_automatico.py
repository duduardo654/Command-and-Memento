"""
Client
======
Monta os objetos e demonstra os dois padrões em conjunto:

  COMMAND -> Editor (Invoker) executa TypeCommand/DeleteCommand sobre o
             Document (Receiver) e consegue desfazer a última ação.

  MEMENTO -> Document (Originator) cria/restaura snapshots (DocumentMemento)
             guardados pelo Caretaker, permitindo voltar a um checkpoint
             completo salvo manualmente, independente do histórico de comandos.

Execute a partir da pasta editor_patterns:
    python main.py
"""

from document import Document
from command.invoker import Editor
from command.commands import TypeCommand, DeleteCommand
from memento.caretaker import Caretaker


def main():
    doc = Document()
    editor = Editor(doc)
    caretaker = Caretaker()

    print("== 1) COMMAND: digitando com histórico de undo ==")
    editor.run(TypeCommand(doc, "Ola"))
    editor.run(TypeCommand(doc, ", mundo"))
    editor.run(TypeCommand(doc, "!!!"))

    print("\n-- desfazendo a última ação (Command.undo) --")
    editor.undo_last()   # remove "!!!"
    editor.undo_last()   # remove ", mundo"

    print("\n== 2) MEMENTO: salvando um checkpoint do estado atual ==")
    caretaker.save_checkpoint("depois_do_ola", doc.save())

    print("\n-- continuando a editar normalmente --")
    editor.run(TypeCommand(doc, ", Python"))
    editor.run(DeleteCommand(doc, 7))          # apaga ", Python"
    editor.run(TypeCommand(doc, " e Patterns!"))

    print(f"\nEstado atual do documento: {doc}")

    print("\n-- restaurando para o checkpoint salvo (Memento.restore) --")
    doc.restore(caretaker.get_checkpoint("depois_do_ola"))
    print(f"Estado após restaurar checkpoint: {doc}")


if __name__ == "__main__":
    main()
