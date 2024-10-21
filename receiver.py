import socket
import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def receive_file(save_path, host, port):
    try:
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        log_message(f"Listening on {host}:{port}...")

        conn, addr = s.accept()
        log_message(f"Connected by {addr}")

        file_info = conn.recv(1024).decode()
        file_name, file_size = file_info.split('|')
        file_size = int(file_size)
        save_file_path = os.path.join(save_path, file_name)

        log_message(f"Receiving file: {file_name} ({file_size} bytes)")

        received_data = b""
        while len(received_data) < file_size:
            chunk = conn.recv(1024)
            if not chunk:
                break
            received_data += chunk
            log_message(f"Received chunk: {len(chunk)} bytes")

        with open(save_file_path, 'wb') as f:
            f.write(received_data)
        log_message(f"File saved at {save_file_path}")

        checksum_received = conn.recv(1024).decode()
        checksum_calculated = hashlib.md5(received_data).hexdigest()

        if checksum_received == checksum_calculated:
            log_message("File received successfully with integrity intact.")
        else:
            log_message("Error: File corruption detected.")

    except Exception as e:
        log_message(f"Error during file reception: {e}")

    finally:
        conn.close()
        s.close()
        log_message("Connection closed.")

def browse_save_path():
    path = filedialog.askdirectory()
    if path:
        entry_save_path.delete(0, tk.END)
        entry_save_path.insert(0, path)

def start_receiving():
    save_path = entry_save_path.get()
    host = entry_host.get()
    port = int(entry_port.get())

    if not save_path or not host or not port:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return

    receive_file(save_path, host, port)

def log_message(message):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, f"{message}\n")
    text_log.config(state=tk.DISABLED)

# Create GUI window
root = tk.Tk()
root.title("File Receiver")

# Save path
label_save_path = tk.Label(root, text="Save Path:")
label_save_path.grid(row=0, column=0, padx=10, pady=5)
entry_save_path = tk.Entry(root, width=50)
entry_save_path.grid(row=0, column=1, padx=10, pady=5)
button_browse = tk.Button(root, text="Browse", command=browse_save_path)
button_browse.grid(row=0, column=2, padx=10, pady=5)

# Host address
label_host = tk.Label(root, text="Host:")
label_host.grid(row=1, column=0, padx=10, pady=5)
entry_host = tk.Entry(root, width=50)
entry_host.grid(row=1, column=1, padx=10, pady=5)
entry_host.insert(0, "127.0.0.1")  # Default host

# Port number
label_port = tk.Label(root, text="Port:")
label_port.grid(row=2, column=0, padx=10, pady=5)
entry_port = tk.Entry(root, width=50)
entry_port.grid(row=2, column=1, padx=10, pady=5)
entry_port.insert(0, "5001")

# Start receiving button
button_receive = tk.Button(root, text="Start Receiving", command=start_receiving)
button_receive.grid(row=3, column=1, pady=10)

# Log area
text_log = tk.Text(root, height=10, state=tk.DISABLED)
text_log.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Start GUI loop
root.mainloop()