import tkinter as tk
from tkinter import simpledialog, messagebox, scrolledtext, ttk
import re
from client.client import ChatClient

TYPING_TIMER = None
client = None
username = None

def on_receive(message):
    if "typing" in message:
        typing_status_label.config(text=message)
    else:
        chat_box.config(state=tk.NORMAL)
        tag = 'self' if message.startswith(f"Inspetor(a) {username}") else 'other'
        chat_box.insert(tk.END, message + '\n', tag)
        chat_box.config(state=tk.DISABLED)
        chat_box.yview(tk.END)

def send_message(event=None):
    message = message_entry.get()
    entry_field.delete(0, tk.END)
    if message:
        formatted_message = f"Inspetor(a) {username}: {message}"
        client.send(formatted_message)
        stop_typing()

def on_typing(event=None):
    global TYPING_TIMER
    if TYPING_TIMER:
        root.after_cancel(TYPING_TIMER)
    try:
        client.send(f"{username} is typing...")
    except:
        pass
    TYPING_TIMER = root.after(1000, stop_typing)

def stop_typing(event=None):
    global TYPING_TIMER
    TYPING_TIMER = None
    try:
        client.send(f"{username} stopped typing.")
    except:
        pass

# GUI Setup
root = tk.Tk()
root.withdraw()
root.title("Painel do Inspetor(a)")
root.geometry("600x500")
root.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=10, background="#4CAF50", foreground="green")
style.map("TButton", background=[("active", "#45a049")])
style.configure("TEntry", font=("Segoe UI", 10), padding=10)
style.configure("TLabel", font=("Segoe UI", 10))

header_frame = ttk.Frame(root, padding="10")
header_frame.pack(fill=tk.X)
typing_status_label = ttk.Label(header_frame, text="", style="TLabel")
typing_status_label.pack(anchor=tk.W)

body_frame = ttk.Frame(root, padding="10")
body_frame.pack(fill=tk.BOTH, expand=True)
chat_box = scrolledtext.ScrolledText(body_frame, height=20, width=70, state=tk.DISABLED,
                                     wrap=tk.WORD, font=("Segoe UI", 10),
                                     bg="#ffffff", fg="#333333", relief=tk.FLAT, borderwidth=5)
chat_box.pack(fill=tk.BOTH, expand=True)
chat_box.config(cursor="arrow")
chat_box.tag_config('self', background="#e0f7fa", foreground="#00695c")
chat_box.tag_config('other', background="#fff9c4", foreground="#f57f17")

input_frame = ttk.Frame(root, padding="15")
input_frame.pack(fill=tk.X)
message_entry = tk.StringVar()
entry_field = ttk.Entry(input_frame, textvariable=message_entry, width=50, style="TEntry")
entry_field.bind("<Return>", send_message)
entry_field.bind("<KeyPress>", on_typing)
entry_field.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

send_button = ttk.Button(input_frame, text="Send", command=send_message, style="TButton")
send_button.pack(side=tk.RIGHT, padx=10)

# Username prompt
while not username or not re.match("^[A-Za-z]{3,20}$", str(username)):
    username = simpledialog.askstring("Username", "Digite um nome de usuário (apenas letras):", parent=root)
    if username is None:
        messagebox.showinfo("Encerrado", "Você cancelou o login. Encerrando.")
        root.destroy()
        exit()

client = ChatClient(username, on_receive)
root.deiconify()
root.protocol("WM_DELETE_WINDOW", lambda: (client.close(), root.quit()))
root.mainloop()
