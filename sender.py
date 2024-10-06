import socket
import hashlib
import os

def send_file(file_path, host, port):
    try:
        s = socket.socket()
        s.connect((host, port))
        print(f"Connected to {host}:{port}")
        
        file_size = os.path.getsize(file_path)
        
        s.send(f"{os.path.basename(file_path)}|{file_size}".encode())
        
        with open(file_path, 'rb') as f:
            file_data = f.read()
            checksum = hashlib.md5(file_data).hexdigest()
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                s.sendall(chunk)
                print(f"Sent chunk: {len(chunk)} bytes")
        
        s.send(checksum.encode())
        print("File transfer completed. Checksum sent.")
        
    except Exception as e:
        print(f"Error during file transfer: {e}")
    
    finally:
        s.close()
        print("Connection closed.")

if __name__ == "__main__":
    file_path = "path/to/your/file.txt"  # Specify the file you want to send
    host = '127.0.0.1'  # Replace with the receiver's IP address
    port = 5001  # Replace with the receiver's listening port
    
    send_file(file_path, host, port)