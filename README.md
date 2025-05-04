# Chat App com Painel Admin

Aplicativo de chat em Python com interface gráfica para usuários e painel administrativo.

## Funcionalidades

- Múltiplos clientes se conectam ao servidor e trocam mensagens públicas.
- Painel admin pode:
  - Ver todas as mensagens.
  - Enviar mensagens públicas ou privadas.
  - Listar usuários conectados.

## Requisitos

- Python 3.8+
- Bibliotecas  (Tkinter, socket, threading)

## Como executar este projeto:

1. Clone este repositório:

```bash
git clone https://github.com/maiamss/TCP-IP-chat-program.git
```

1. Inicie o servidor:

   ```
   python3 -m server.server
   ```
3. Inicie o painel admim:

   ```
   python3 -m server.admin_painel
   ```
4. Inicie os clientes:

   ```
   python3 -m client.gui
   ```
