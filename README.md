# Chat App com Painel Admin💬

Aplicação desktop em Python com interface gráfica (Tkinter) que permite a comunicação em tempo real entre inspetores ambientais por meio de mensagens via **sockets** TCP/IP. Desenvolvido com foco em integração cliente-servidor, manipulação de eventos gráficos e lógica de comunicação assíncrona.

Este projeto foi desenvolvido como parte dos estudos de redes e interfaces gráficas com Python.

### Tecnologias Utilizadas:

* [x] Linguagem: Python
* [x] Interface Gráfica: Tkinter
* [x] Comunicação em rede: `socket` e `threading`

### Funcionalidades:

* Interface intuitiva e responsiva com `Tkinter`
* Comunicação em tempo real entre múltiplos usuários (clientes)
* Detecção e exibição de status "digitando..."
* Exibição de mensagens formatadas com nome do inspetor(a)
* Conexão automática ao servidor via socket TCP
* Organização do código com separação entre cliente, servidor e interface
* Estilização personalizada com `ttk.Style`

### Como executar este projeto:

#### 1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/painel-inspetores.git
```

#### 2. Execute o servidor:

```
python -m server.server
```

#### 3. Execute o painel do admin:

```bash
python server/admin_panel.py
```

#### 4. Em outro terminal, execute o cliente (interface):

```bash
python client/gui.py
```

> **Importante:** Execute o servidor primeiro para aceitar conexões dos inspetores.

---

### Objetivo:

Este projeto foi criado como um projeto da universidade (APS) para praticar os seguintes conceitos:

* Programação com sockets TCP/IP
* Multithreading e eventos assíncronos
* Comunicação em rede cliente-servidor

---

![image](https://github.com/user-attachments/assets/2dd755d6-c2ac-4842-8414-f31dbe51871c)
