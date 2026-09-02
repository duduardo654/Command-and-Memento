"""
Client
======
Monta os objetos e demonstra os dois padrões em conjunto, com o
RemoteControl (Invoker) bem separado da TV (Receiver) e dos Commands.

  COMMAND -> o Client cria os Commands (TurnOnCommand, VolumeUpCommand...)
             e os "entrega" para o RemoteControl (Invoker) apertar. O
             RemoteControl não sabe o que cada botão faz de verdade —
             só chama command.execute() / undo().

  MEMENTO -> a TV (Originator) sabe salvar/restaurar seu próprio estado
             (canal + volume). O PresetManager (Caretaker) guarda esses
             estados com um nome, sem entender o conteúdo.

Execute a partir da pasta tv_remote_patterns:
    python main.py
"""

from tv import TV
from command.invoker import RemoteControl
from command.commands import (
    TurnOnCommand,
    TurnOffCommand,
    VolumeUpCommand,
    VolumeDownCommand,
    ChangeChannelCommand,
)
from memento.caretaker import PresetManager


def main():
    tv = TV()
    remote = RemoteControl()
    presets = PresetManager()

    print("== 1) COMMAND: apertando botões do controle remoto ==")
    remote.pressionar_botao(TurnOnCommand(tv))
    print(f"  [Invoker] botão LIGAR pressionado -> {tv}")

    remote.pressionar_botao(ChangeChannelCommand(tv, 8))
    print(f"  [Invoker] botão CANAL+8 pressionado -> {tv}")

    remote.pressionar_botao(VolumeUpCommand(tv))
    remote.pressionar_botao(VolumeUpCommand(tv))
    print(f"  [Invoker] botão VOLUME+ pressionado 2x -> {tv}")

    print("\n-- apertando o botão de desfazer (Command.undo) --")
    remote.pressionar_desfazer()
    print(f"  [Invoker] após 1x DESFAZER -> {tv}")
    remote.pressionar_desfazer()
    print(f"  [Invoker] após 2x DESFAZER -> {tv}")

    print("\n== 2) MEMENTO: salvando um preset com o estado atual ==")
    presets.salvar_preset("Modo Filme", tv.save())

    print("\n-- continuando a usar a TV normalmente --")
    remote.pressionar_botao(ChangeChannelCommand(tv, 25))
    remote.pressionar_botao(VolumeDownCommand(tv))
    remote.pressionar_botao(VolumeDownCommand(tv))
    print(f"  estado atual -> {tv}")

    print("\n-- restaurando o preset salvo (Memento.restore) --")
    tv.restore(presets.obter_preset("Modo Filme"))
    print(f"  após restaurar 'Modo Filme' -> {tv}")


if __name__ == "__main__":
    main()
