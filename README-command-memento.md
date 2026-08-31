# Documentando Padrões de Projeto: Command & Memento em Python 🐍💾

Este guia apresenta uma documentação intuitiva, focada em analogias do mundo real e conceitos práticos, explicando como os padrões comportamentais **Command** [1] e **Memento** [25] funcionam de forma independente e como eles se unem em Python para criar um sistema resiliente de **Desfazer/Refazer (Undo/Redo)** [15, 18, 47].

---

## 🍽️ 1. O Padrão Command: A Analogia do Restaurante

O padrão **Command** tem como objetivo principal **transformar uma ação/solicitação em um objeto independente** [1]. 

### 📌 A Analogia do Mundo Real
Imagine que você vai a um restaurante jantar [9]:
1. **Você (o Cliente / Client):** Decide o que quer comer e faz o pedido [10].
2. **O Garçom (o Remetente / Invoker):** Anota o seu pedido em um bloco de papel (o **Command**) [9, 10]. Ele não precisa saber cozinhar; ele apenas "dispara" a solicitação pendurando o papel na parede da cozinha [9].
3. **O Bloco de Notas (o Command):** É um objeto físico. Ele contém todas as informações necessárias para a execução (quem pediu, qual o prato, observações) [10]. Ele pode ser enfileirado, adiado ou guardado em um histórico de vendas [1, 14, 15].
4. **O Chef (o Receptor / Receiver):** Lê o papel e executa a ação real (cozinha o prato) [9, 10]. Ele tem a lógica de negócios para transformar ingredientes em comida [10].

```
[ Cliente (Você) ] 
       │ (Cria o comando)
       ▼
[ Invoker (Garçom) ] ──(Dispara execute())──> [ Command (Papel do Pedido) ] ──(Delega trabalho)──> [ Receiver (Chef) ]
```

### 💡 Por que isso é incrível em Python?
Em Python, as funções são objetos de primeira classe (podem ser passadas como argumentos, guardadas em listas, etc.) [13]. No entanto, para sistemas complexos que precisam de **histórico e reversão**, encapsular ações em **classes de Comando** é a escolha ideal [15, 18]:

* **Desacoplamento Total:** O botão de clique da interface visual (GUI) não precisa saber o que é um banco de dados ou como salvar um arquivo [4]. Ele apenas recebe um objeto de comando e chama o método `.execute()` dele [6, 10].
* **Flexibilidade Dinâmica:** Você pode facilmente enfileirar comandos em uma `list` ou `queue.Queue` do Python para execução tardia, ou até mesmo enviá-los de forma assíncrona [1, 14].

---

## 🎮 2. O Padrão Memento: A Analogia do "Save State"

O padrão **Memento** permite **capturar e salvar o estado interno de um objeto** para que ele possa ser restaurado no futuro, tudo isso sem violar o encapsulamento (sem expor as variáveis privadas do objeto) [25, 38].

### 📌 A Analogia do Mundo Real
Pense em um videogame retrô extremamente difícil [26]:
1. **O Jogo (o Criador / Originator):** Tem muitas variáveis complexas rodando por trás (sua vida atual, itens no inventário, coordenadas no mapa, pontuação) [29, 33].
2. **O Save State (o Memento):** Quando você aperta o botão de "Quick Save", o console tira uma "foto" exata da memória naquele microssegundo e guarda em um arquivo de save criptografado [25, 31]. Ninguém de fora consegue ler ou alterar os dados desse arquivo binário (preservando o encapsulamento) [31, 32].
3. **O Cartão de Memória (o Zelador / Caretaker):** Guarda o arquivo de save na ordem em que foram criados [33]. Ele não sabe o que está escrito no save e não pode alterá-lo; ele apenas sabe que precisa segurar o arquivo e devolvê-lo quando você clicar em "Quick Load" [32, 33].

```
[ Caretaker (Cartão de Memória) ] ───(Apenas armazena)───> [ Memento (Arquivo de Save Criptografado) ]
                                                                             ▲
                                                           (Cria / Restaura sem expor variáveis)
                                                                             │
                                                                 [ Originator (O Jogo) ]
```

### 💡 O Desafio e a Solução em Python
Linguagens como Java e C++ usam classes aninhadas (*nested classes*) com modificadores `private` estritos para garantir que o Caretaker não mexa no estado privado do Memento [33]. 

Em Python, **não existem membros verdadeiramente privados** no nível do interpretador [40]. Para contornar esse trade-off em sistemas dinâmicos:
* **Uso de Convenções (`_` ou `__`):** O Originator e o Memento utilizam propriedades iniciadas com sublinhados (como `self._estado_interno` ou `self.__estado_privado`) para desencorajar o acesso externo [40].
* **Imutabilidade Dinâmica:** Idealmente, a classe Memento é projetada para ser imutável em Python (recebendo os dados apenas no método `__init__` e sem expor métodos setters de alteração) [33, 39].

---

## 🤝 3. O Casamento Perfeito: Construindo o mecanismo de "Desfazer" (Undo)

A verdadeira mágica acontece quando combinamos o **Command** e o **Memento** [47]. Eles formam a base padrão da indústria para criar pilhas de desfazer e refazer (como as que você usa ao pressionar `Ctrl+Z` em editores) [11, 15, 47].

Nessa parceria perfeita [47]:
* O **Command** assume o papel de **Caretaker (Zelador)** do Memento [36, 47].
* O **Receptor (Receiver)** do comando atua como o **Originator (Criador)** do Memento [31, 33].

### 🔄 O Fluxo Passo a Passo
1. **Antes de agir:** O usuário aciona uma ação (ex: "Digitar Texto") [11].
2. **O Backup:** O comando concreto, antes de fazer qualquer alteração no Editor (Originator), pede para o Editor gerar um snapshot dele mesmo: `self.backup = editor.create_snapshot()` [37].
3. **A Execução:** O comando faz a alteração necessária e avisa o sistema que foi executado com sucesso [11, 12]. Ele é empilhado no histórico [11, 12].
4. **O Desfazer (Ctrl+Z):** Quando o usuário pede para desfazer, o sistema recupera o último comando da pilha e aciona o método `.undo()` [12, 37].
5. **A Restauração:** Internamente, o método `.undo()` do comando simplesmente pega aquele snapshot guardado e diz: `self.backup.restore()` [37]. O editor volta instantaneamente ao estado em que estava antes [37].

---

## 📋 Resumo Visual de Papéis

| Elemento Técnico | Papel na Analogia do Restaurante 🍽️ | Papel na Analogia do Videogame 🎮 | Função Principal no Sistema de Undo/Redo |
| :--- | :--- | :--- | :--- |
| **Command** [10] | O papel com a anotação do pedido [9] | O botão de ação que o jogador aperta | Encapsula a ação e segura o snapshot para o Undo [37, 47]. |
| **Invoker** [10] | O Garçom que leva o pedido [9] | O controle do videogame | Dispara a execução da ação (chama o `.execute()`) [10]. |
| **Originator** [33] | - | O Jogo rodando em tempo real | É o dono do estado privado; cria e consome os mementos [33, 37]. |
| **Memento** [33] | - | O arquivo criptografado de Save State | O snapshot imutável contendo o estado anterior lacrado [33]. |
| **Caretaker** [33] | O mural da cozinha onde o pedido fica | O Cartão de Memória [32] | Gerencia a linha do tempo e a coleção/pilha de estados salvos [33]. |
| **Receiver** [10] | O Chef que cozinha [9] | O motor interno do jogo | Executa a lógica de negócios real delegada pelo comando [10]. |

---
*Documentação de conceitos construída com base nos guias de padrões de projeto do portal Refactoring.Guru (2026).* [44, 49]
