import socket
import hashlib
import os

def receive_file(save_path, host, port):
    try:
        s = socket.socket()
        s.bind((host, port))
        s.listen(1)
        print(f"Listening on {host}:{port}...")
        
        conn, addr = s.accept()
        print(f"Connected by {addr}")
        
        file_info = conn.recv(1024).decode()
        file_name, file_size = file_info.split('|')
        file_size = int(file_size)
        save_file_path = os.path.join(save_path, file_name)
        
        print(f"Receiving file: {file_name} ({file_size} bytes)")
        
        received_data = b""
        while len(received_data) < file_size:
            chunk = conn.recv(1024)
            if not chunk:
                break
            received_data += chunk
            print(f"Received chunk: {len(chunk)} bytes")
        
        with open(save_file_path, 'wb') as f:
            f.write(received_data)
        print(f"File saved at {save_file_path}")
        
        checksum_received = conn.recv(1024).decode()
        
        checksum_calculated = hashlib.md5(received_data).hexdigest()
        
        if checksum_received == checksum_calculated:
            print("File received successfully with integrity intact.")
        else:
            print("Error: File corruption detected.")
    
    except Exception as e:
        print(f"Error during file reception: {e}")
    
    finally:
        conn.close()
        s.close()
        print("Connection closed.")

if __name__ == "__main__":
    save_path = "path/to/save/directory"  # Specify where to save the received file
    host = '127.0.0.1'  # Replace with the server's IP address
    port = 5001  # Replace with the port you want to listen on
    
    receive_file(save_path, host, port)