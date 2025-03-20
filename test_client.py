import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 7777))

    while True:
        cmd = input(">>> ")
        if not cmd:
            continue
        elif cmd.startswith("download "):
            sock.send(cmd.encode())  # Send download request
            
            with open("client.file", "wb") as file:
                while True:
                    fetch_file = sock.recv(8192)
                    if not fetch_file:  # EOF detected (server closed connection)
                        break
                    file.write(fetch_file)
            
            print("[+] File received successfully.")
            break  # Exit after file transfer
        elif cmd in ('quit', 'exit'):
            sock.close()
            break
        else:
            sock.send(cmd.encode())
            output = sock.recv(1024).decode()
            print(output, end="\n", flush=True)

if __name__ == "__main__":
    main()
