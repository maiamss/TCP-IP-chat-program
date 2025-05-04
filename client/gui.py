import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, ttk
import re
from client.client import ChatClient

TYPING_TIMER = None
TYPING_STATE = False
client = None
username = None

def on_receive(message):

    if "está digitando..." in message and not message.startswith(username):
        typing_status_label.config(text=message)
    elif "parou de digitar." in message and not message.startswith(username):
        typing_status_label.config(text="")
    else:
        if not ("está digitando..." in message and message.startswith(username)) and \
           not ("parou de digitar." in message and message.startswith(username)):
            chat_box.config(state=tk.NORMAL)
            tag = 'self' if message.startswith(f"Inspetor(a) {username}") else 'other'
            chat_box.insert(tk.END, message + '\n', tag)
            chat_box.config(state=tk.DISABLED)
            chat_box.yview(tk.END)

def send_message(event=None):
    message = message_entry.get()
    if message:
        formatted_message = f"Inspetor(a) {username}: {message}"
        client.send(formatted_message)
        message_entry.set("")
        stop_typing()

def on_typing(event=None):
    global TYPING_TIMER, TYPING_STATE

    if event.keysym in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 
                       'Alt_L', 'Alt_R', 'Up', 'Down', 'Left', 'Right']:
        return

    if not TYPING_STATE:
        TYPING_STATE = True
        client.send(f"{username} está digitando...")

    if TYPING_TIMER:
        root.after_cancel(TYPING_TIMER)

    TYPING_TIMER = root.after(1500, stop_typing)

def stop_typing(event=None):
    global TYPING_TIMER, TYPING_STATE

    if TYPING_STATE:
        TYPING_STATE = False
        client.send(f"{username} parou de digitar.")

    if TYPING_TIMER:
        root.after_cancel(TYPING_TIMER)
        TYPING_TIMER = None

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')

    style.configure('.', background='#E8F5E9', foreground='#1B5E20', font=('Segoe UI', 10))

    style.configure('TButton', background='#4CAF50', foreground='white', 
                   borderwidth=1, focusthickness=3, focuscolor='#4CAF50',
                   font=('Segoe UI', 10, 'bold'))
    style.map('TButton',
              background=[('active', '#388E3C'), ('pressed', '#2E7D32')],
              foreground=[('active', 'white'), ('pressed', 'white')])

    style.configure('TEntry', fieldbackground='white', borderwidth=1, 
                   relief='solid', padding=5)

    style.configure('TLabel', background='#E8F5E9', foreground='#1B5E20')
    style.configure('TFrame', background='#E8F5E9')

# GUI Setup
root = tk.Tk()
root.withdraw()
root.title("Painel do Inspetor(a) - Secretaria de Meio Ambiente")
root.geometry("700x550")
root.configure(bg='#E8F5E9')

configure_styles()

header_frame = ttk.Frame(root, style='TFrame', padding="10")
header_frame.pack(fill=tk.X)

title_label = ttk.Label(header_frame,
                       text=f"Painel do Inspetor(a)",
                       font=('Segoe UI', 16, 'bold'),
                       style='TLabel')
title_label.pack(side=tk.LEFT)

user_label = ttk.Label(header_frame,
                      text=f"Usuário: {username}",
                      font=('Segoe UI', 10),
                      style='TLabel')
user_label.pack(side=tk.RIGHT)

typing_status_label = ttk.Label(root,
                               text="",
                               foreground="#689F38",
                               font=('Segoe UI', 9, 'italic'),
                               style='TLabel')
typing_status_label.pack(anchor=tk.W, padx=15)

chat_frame = ttk.Frame(root, style='TFrame')
chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

chat_box = scrolledtext.ScrolledText(
    chat_frame,
    height=20,
    width=70,
    state=tk.DISABLED,
    wrap=tk.WORD,
    font=('Segoe UI', 10),
    bg='white',
    fg='#1B5E20',
    padx=10,
    pady=10,
    insertbackground='#1B5E20',
    selectbackground='#A5D6A7',
    relief=tk.FLAT,
    borderwidth=5
)
chat_box.pack(fill=tk.BOTH, expand=True)
chat_box.config(cursor="arrow")
chat_box.tag_config('self', background="#E8F5E9", foreground="#1B5E20", lmargin1=10, lmargin2=10)
chat_box.tag_config('other', background="#C8E6C9", foreground="#2E7D32", lmargin1=10, lmargin2=10)

input_frame = ttk.Frame(root, style='TFrame', padding="15")
input_frame.pack(fill=tk.X)

message_entry = tk.StringVar()
entry_field = ttk.Entry(
    input_frame,
    textvariable=message_entry,
    width=50,
    style='TEntry'
)
entry_field.bind("<Return>", send_message)
entry_field.bind("<KeyPress>", on_typing)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

send_button = ttk.Button(
    input_frame,
    text="Enviar",
    command=send_message,
    style='TButton'
)
send_button.pack(side=tk.RIGHT, padx=10)

footer_frame = ttk.Frame(root, style='TFrame')
footer_frame.pack(fill=tk.X, padx=10, pady=10)
ttk.Label(
    footer_frame,
    text="Secretaria de Estado do Meio Ambiente © 2025",
    style='TLabel',
    font=('Segoe UI', 8)
).pack(side=tk.RIGHT)

while not username or not re.match("^[A-Za-z]{3,20}$", str(username)):
    username = simpledialog.askstring("Username", "Digite seu nome de inspetor (apenas letras, 3-20 caracteres):", parent=root)
    if username is None:
        messagebox.showinfo("Encerrado", "Você cancelou o login. Encerrando.")
        root.destroy()
        exit()

user_label.config(text=f"Usuário: {username}")

client = ChatClient(username, on_receive)
root.deiconify()
root.protocol("WM_DELETE_WINDOW", lambda: (client.close(), root.quit()))

entry_field.focus()

root.mainloop()