"""
RemoteControl (Invoker)
========================
Este é o Invoker do padrão Command: o controle remoto em si.

Ele NÃO sabe como ligar a TV, mudar volume ou canal — ele só guarda uma
referência a um Command e, quando um "botão" é pressionado, chama
command.execute(). Isso é o desacoplamento clássico do padrão: o
RemoteControl poderia controlar uma TV, um som ou qualquer outro
Receiver, desde que receba os Commands certos.

Além disso, ele mantém um histórico de comandos executados para permitir
"desfazer" (undo) a última ação apertada.
"""

from typing import List
from command.commands import Command


class RemoteControl:
    def __init__(self):
        self._historico: List[Command] = []

    def pressionar_botao(self, command: Command) -> None:
        """Aperta um botão do controle: executa o Command associado."""
        command.execute()
        self._historico.append(command)

    def pressionar_desfazer(self) -> None:
        """Aperta o botão de 'desfazer' do controle."""
        if not self._historico:
            print("  [Invoker] nenhum comando para desfazer")
            return
        ultimo_comando = self._historico.pop()
        ultimo_comando.undo()
