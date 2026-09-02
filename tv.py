"""
TV
==
No padrão COMMAND, esta classe é o "Receiver": quem sabe executar de fato
as ações (ligar, desligar, mudar volume, trocar canal).

No padrão MEMENTO, esta mesma classe é o "Originator": quem sabe criar
um snapshot do próprio estado (save) e se restaurar a partir dele (restore).
"""

from memento.memento import TVMemento


class TV:
    def __init__(self):
        self.ligada: bool = False
        self.volume: int = 10
        self.canal: int = 1

    # ---- usado pelos Commands ----
    def ligar(self) -> None:
        self.ligada = True

    def desligar(self) -> None:
        self.ligada = False

    def aumentar_volume(self) -> None:
        self.volume += 1

    def diminuir_volume(self) -> None:
        self.volume -= 1

    def mudar_canal(self, canal: int) -> None:
        self.canal = canal

    # ---- papel de Originator no Memento ----
    def save(self) -> TVMemento:
        """Cria um Memento (snapshot) do estado atual: canal + volume."""
        return TVMemento(canal=self.canal, volume=self.volume)

    def restore(self, memento: TVMemento) -> None:
        """Restaura canal e volume a partir de um memento salvo."""
        self.canal = memento.canal
        self.volume = memento.volume

    def __str__(self) -> str:
        estado = "ligada" if self.ligada else "desligada"
        return f"TV {estado} | canal {self.canal} | volume {self.volume}"
