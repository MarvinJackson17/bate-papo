import tkinter as tk
from tkinter import messagebox
import socket
import threading


class ChatApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("Guardian")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.label_host = tk.Label(self.frame, text="Host:")
        self.label_host.grid(row=0, column=0, sticky="e")
        self.entry_host = tk.Entry(self.frame)
        self.entry_host.insert(0, "127.0.0.1")
        self.entry_host.grid(row=0, column=1)

        self.label_port = tk.Label(self.frame, text="Port:")
        self.label_port.grid(row=1, column=0, sticky="e")
        self.entry_port = tk.Entry(self.frame)
        self.entry_port.insert(0, "5555")
        self.entry_port.grid(row=1, column=1)

        self.label_message = tk.Label(self.frame, text="Message:")
        self.label_message.grid(row=2, column=0, sticky="e")
        self.entry_message = tk.Entry(self.frame)
        self.entry_message.grid(row=2, column=1)

        self.button_connect = tk.Button(self.frame, text="Connect", command=self.connect)
        self.button_connect.grid(row=3, column=0, columnspan=2, pady=10)

        self.text_chat = tk.Text(self.frame, state="disabled", width=40, height=10)
        self.text_chat.grid(row=4, column=0, columnspan=2)

        self.button_send = tk.Button(self.frame, text="Send", command=self.send_message)
        self.button_send.grid(row=5, column=0, columnspan=2, pady=10)

        self.connected = False
        self.server_socket = None
        self.client_socket = None

    def connect(self):
        if self.connected:
            messagebox.showerror("Error", "Already connected!")
            return

        host = self.entry_host.get()
        port = int(self.entry_port.get())

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((host, port))
            self.connected = True
            threading.Thread(target=self.receive_messages).start()
            messagebox.showinfo("Info", "Connected!")
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def receive_messages(self):
        while self.connected:
            try:
                message = self.server_socket.recv(1024).decode('utf-8')
                self.text_chat.configure(state="normal")
                self.text_chat.insert(tk.END, message + '\n')
                self.text_chat.configure(state="disabled")
            except:
                self.server_socket.close()
                self.connected = False
                messagebox.showinfo("Info", "Disconnected!")
                break

    def send_message(self):
        if not self.connected:
            messagebox.showerror("Error", "Not connected!")
            return

        message = self.entry_message.get()
        if message:
            try:
                self.server_socket.send(message.encode('utf-8'))
                self.text_chat.configure(state="normal")
                self.text_chat.insert(tk.END, "You: " + message + '\n')
                self.text_chat.configure(state="disabled")
                self.entry_message.delete(0, tk.END)
            except:
                self.server_socket.close()
                self.connected = False
                messagebox.showinfo("Info", "Disconnected!")


def main():
    root = tk.Tk()
    app = ChatApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
