# Documentando Padrões de Projeto: Command & Memento em Python 🐍💾

Este guia apresenta uma documentação intuitiva, focada em analogias do mundo real e conceitos práticos, explicando como os padrões comportamentais **Command** e **Memento** funcionam de forma independente e como eles se unem em Python para criar um sistema resiliente de **Desfazer/Refazer (Undo/Redo)** .

---

## 🍽️ 1. O Padrão Command: A Analogia do Restaurante

O padrão **Command** tem como objetivo principal **transformar uma ação/solicitação em um objeto independente**. 

### 📌 A Analogia do Mundo Real
Imagine que você vai a um restaurante jantar:
1. **Você (o Cliente / Client):** Decide o que quer comer e faz o pedido.
2. **O Garçom (o Remetente / Invoker):** Anota o seu pedido em um bloco de papel (o **Command**). Ele não precisa saber cozinhar; ele apenas "dispara" a solicitação pendurando o papel na parede da cozinha.
3. **O Bloco de Notas (o Command):** É um objeto físico. Ele contém todas as informações necessárias para a execução (quem pediu, qual o prato, observações). Ele pode ser enfileirado, adiado ou guardado em um histórico de vendas.
4. **O Chef (o Receptor / Receiver):** Lê o papel e executa a ação real (cozinha o prato). Ele tem a lógica de negócios para transformar ingredientes em comida.

```
[ Cliente (Você) ] 
       │ (Cria o comando)
       ▼
[ Invoker (Garçom) ] ──(Dispara execute())──> [ Command (Papel do Pedido) ] ──(Delega trabalho)──> [ Receiver (Chef) ]
```

### 💡 Por que isso é incrível em Python?
Em Python, as funções são objetos de primeira classe (podem ser passadas como argumentos, guardadas em listas, etc.). No entanto, para sistemas complexos que precisam de **histórico e reversão**, encapsular ações em **classes de Comando** é a escolha ideal:

* **Desacoplamento Total:** O botão de clique da interface visual (GUI) não precisa saber o que é um banco de dados ou como salvar um arquivo. Ele apenas recebe um objeto de comando e chama o método `.execute()` dele.
* **Flexibilidade Dinâmica:** Você pode facilmente enfileirar comandos em uma `list` ou `queue.Queue` do Python para execução tardia, ou até mesmo enviá-los de forma assíncrona.

---

## 🎮 2. O Padrão Memento: A Analogia do "Save State"

O padrão **Memento** permite **capturar e salvar o estado interno de um objeto** para que ele possa ser restaurado no futuro, tudo isso sem violar o encapsulamento (sem expor as variáveis privadas do objeto).

### 📌 A Analogia do Mundo Real
Pense em um videogame retrô extremamente difícil:
1. **O Jogo (o Criador / Originator):** Tem muitas variáveis complexas rodando por trás (sua vida atual, itens no inventário, coordenadas no mapa, pontuação).
2. **O Save State (o Memento):** Quando você aperta o botão de "Quick Save", o console tira uma "foto" exata da memória naquele microssegundo e guarda em um arquivo de save criptografado. Ninguém de fora consegue ler ou alterar os dados desse arquivo binário (preservando o encapsulamento).
3. **O Cartão de Memória (o Zelador / Caretaker):** Guarda o arquivo de save na ordem em que foram criados. Ele não sabe o que está escrito no save e não pode alterá-lo; ele apenas sabe que precisa segurar o arquivo e devolvê-lo quando você clicar em "Quick Load".

```
[ Caretaker (Cartão de Memória) ] ───(Apenas armazena)───> [ Memento (Arquivo de Save Criptografado) ]
                                                                             ▲
                                                           (Cria / Restaura sem expor variáveis)
                                                                             │
                                                                 [ Originator (O Jogo) ]
```

### 💡 O Desafio e a Solução em Python
Linguagens como Java e C++ usam classes aninhadas (*nested classes*) com modificadores `private` estritos para garantir que o Caretaker não mexa no estado privado do Memento. 

Em Python, **não existem membros verdadeiramente privados** no nível do interpretador. Para contornar esse trade-off em sistemas dinâmicos:
* **Uso de Convenções (`_` ou `__`):** O Originator e o Memento utilizam propriedades iniciadas com sublinhados (como `self._estado_interno` ou `self.__estado_privado`) para desencorajar o acesso externo.
* **Imutabilidade Dinâmica:** Idealmente, a classe Memento é projetada para ser imutável em Python (recebendo os dados apenas no método `__init__` e sem expor métodos setters de alteração).

---

## 🤝 3. O Casamento Perfeito: Construindo o mecanismo de "Desfazer" (Undo)

A verdadeira mágica acontece quando combinamos o **Command** e o **Memento**. Eles formam a base padrão da indústria para criar pilhas de desfazer e refazer (como as que você usa ao pressionar `Ctrl+Z` em editores).

Nessa parceria perfeita:
* O **Command** assume o papel de **Caretaker (Zelador)** do Memento.
* O **Receptor (Receiver)** do comando atua como o **Originator (Criador)** do Memento.

### 🔄 O Fluxo Passo a Passo
1. **Antes de agir:** O usuário aciona uma ação (ex: "Digitar Texto").
2. **O Backup:** O comando concreto, antes de fazer qualquer alteração no Editor (Originator), pede para o Editor gerar um snapshot dele mesmo: `self.backup = editor.create_snapshot()`.
3. **A Execução:** O comando faz a alteração necessária e avisa o sistema que foi executado com sucesso. Ele é empilhado no histórico.
4. **O Desfazer (Ctrl+Z):** Quando o usuário pede para desfazer, o sistema recupera o último comando da pilha e aciona o método `.undo()` .
5. **A Restauração:** Internamente, o método `.undo()` do comando simplesmente pega aquele snapshot guardado e diz: `self.backup.restore()`. O editor volta instantaneamente ao estado em que estava antes.

---

## 📋 Resumo Visual de Papéis

| Elemento Técnico | Papel na Analogia do Restaurante 🍽️ | Papel na Analogia do Videogame 🎮 | Função Principal no Sistema de Undo/Redo |
| :--- | :--- | :--- | :--- |
| **Command** | O papel com a anotação do pedido | O botão de ação que o jogador aperta | Encapsula a ação e segura o snapshot para o Undo. |
| **Invoker**  | O Garçom que leva o pedido | O controle do videogame | Dispara a execução da ação (chama o `.execute()`). |
| **Originator**  | - | O Jogo rodando em tempo real | É o dono do estado privado; cria e consome os mementos. |
| **Memento** | - | O arquivo criptografado de Save State | O snapshot imutável contendo o estado anterior lacrado. |
| **Caretaker**  | O mural da cozinha onde o pedido fica | O Cartão de Memória | Gerencia a linha do tempo e a coleção/pilha de estados salvos. |
| **Receiver** | O Chef que cozinha | O motor interno do jogo | Executa a lógica de negócios real delegada pelo comando. |

---
*Documentação de conceitos construída com base nos guias de padrões de projeto do portal Refactoring.Guru (2026).* 
