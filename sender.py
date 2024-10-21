import socket
import hashlib
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def send_file(file_path, host, port):
    try:
        s = socket.socket()
        s.connect((host, port))
        log_message(f"Connected to {host}:{port}")
        
        file_size = os.path.getsize(file_path)
        s.send(f"{os.path.basename(file_path)}|{file_size}".encode())
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
            checksum = hashlib.md5(file_data).hexdigest()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                s.sendall(chunk)
                log_message(f"Sent chunk: {len(chunk)} bytes")
        
        s.send(checksum.encode())
        log_message("File transfer completed. Checksum sent.")
        
    except Exception as e:
        log_message(f"Error during file transfer: {e}")
    
    finally:
        s.close()
        log_message("Connection closed.")

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        entry_file_path.delete(0, tk.END)
        entry_file_path.insert(0, file_path)

def start_transfer():
    file_path = entry_file_path.get()
    host = entry_host.get()
    port = int(entry_port.get())
    
    if not file_path or not host or not port:
        messagebox.showerror("Input Error", "Please fill all fields.")
        return
    
    send_file(file_path, host, port)

def log_message(message):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, f"{message}\n")
    text_log.config(state=tk.DISABLED)

# Create GUI window
root = tk.Tk()
root.title("File Transfer")

# File path
label_file_path = tk.Label(root, text="File Path:")
label_file_path.grid(row=0, column=0, padx=10, pady=5)
entry_file_path = tk.Entry(root, width=50)
entry_file_path.grid(row=0, column=1, padx=10, pady=5)
button_browse = tk.Button(root, text="Browse", command=browse_file)
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

# Start transfer button
button_transfer = tk.Button(root, text="Start Transfer", command=start_transfer)
button_transfer.grid(row=3, column=1, pady=10)

# Log area
text_log = tk.Text(root, height=10, state=tk.DISABLED)
text_log.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

# Start GUI loop
root.mainloop()