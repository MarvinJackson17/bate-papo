import tkinter as tk
from tkinter import messagebox
import socket
import threading

class ChatApplication:
    def __init__(self, master):
        # Inicialização da aplicação
        self.master = master
        self.master.title("Chat")
        
        # Criação do frame principal
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        # Widgets para inserir o endereço IP e a porta do servidor
        self.label_host = tk.Label(self.frame, text="Host:")
        self.label_host.grid(row=0, column=0, sticky="e")
        self.entry_host = tk.Entry(self.frame)
        self.entry_host.insert(0, "127.0.0.1")  # Endereço padrão
        self.entry_host.grid(row=0, column=1)

        self.label_port = tk.Label(self.frame, text="Port:")
        self.label_port.grid(row=1, column=0, sticky="e")
        self.entry_port = tk.Entry(self.frame)
        self.entry_port.insert(0, "5555")  # Porta padrão
        self.entry_port.grid(row=1, column=1)

        # Widgets para inserir e enviar mensagens
        self.label_message = tk.Label(self.frame, text="Message:")
        self.label_message.grid(row=2, column=0, sticky="e")
        self.entry_message = tk.Entry(self.frame)
        self.entry_message.grid(row=2, column=1)

        # Botão para conectar ao servidor
        self.button_connect = tk.Button(self.frame, text="Connect", command=self.connect)
        self.button_connect.grid(row=3, column=0, columnspan=2, pady=10)

        # Área de exibição das mensagens do chat
        self.text_chat = tk.Text(self.frame, state="disabled", width=40, height=10)
        self.text_chat.grid(row=4, column=0, columnspan=2)

        # Botão para enviar mensagens
        self.button_send = tk.Button(self.frame, text="Send", command=self.send_message)
        self.button_send.grid(row=5, column=0, columnspan=2, pady=10)

        # Variáveis de controle da conexão
        self.connected = False
        self.server_socket = None
        self.client_socket = None

    def connect(self):
        # Função para conectar ao servidor
        if self.connected:
            messagebox.showerror("Error", "Already connected!")
            return

        host = self.entry_host.get()
        port = int(self.entry_port.get())

        try:
            # Criação do socket e conexão ao servidor
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((host, port))
            self.connected = True
            # Inicia uma thread para receber mensagens do servidor
            threading.Thread(target=self.receive_messages).start()
            messagebox.showinfo("Info", "Connected!")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def receive_messages(self):
        # Função para receber mensagens do servidor
        while self.connected:
            try:
                # Recebe uma mensagem do servidor
                message = self.server_socket.recv(1024).decode('utf-8')
                # Habilita a área de chat para adicionar mensagens
                self.text_chat.configure(state="normal")
                # Adiciona a mensagem recebida à área de chat
                self.text_chat.insert(tk.END, message + '\n')
                # Desabilita a área de chat novamente
                self.text_chat.configure(state="disabled")
            except:
                # Se ocorrer um erro na conexão, fecha o socket e atualiza a variável de controle
                self.server_socket.close()
                self.connected = False
                messagebox.showinfo("Info", "Disconnected!")
                break

    def send_message(self):
        # Função para enviar mensagens ao servidor
        if not self.connected:
            messagebox.showerror("Error", "Not connected!")
            return

        message = self.entry_message.get()
        if message:
            try:
                # Envia a mensagem para o servidor
                self.server_socket.send(message.encode('utf-8'))
                # Habilita a área de chat para adicionar mensagens
                self.text_chat.configure(state="normal")
                # Adiciona a mensagem enviada à área de chat
                self.text_chat.insert(tk.END, "You: " + message + '\n')
                # Desabilita a área de chat novamente
                self.text_chat.configure(state="disabled")
                # Limpa o campo de entrada de mensagem
                self.entry_message.delete(0, tk.END)
            except:
                # Se ocorrer um erro na conexão, fecha o socket e atualiza a variável de controle
                self.server_socket.close()
                self.connected = False
                messagebox.showinfo("Info", "Disconnected!")

def main():
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()

if __name__ == "__main__":
    main()
