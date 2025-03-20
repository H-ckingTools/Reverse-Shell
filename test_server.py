import socket
import os

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 7777))
    sock.listen()
    
    print("[*] Waiting for connection...")
    con, addr = sock.accept()
    print(f"[*] Connection established with {addr}")

    while True:
        get_cmd = con.recv(1024).decode().strip().lower()
        if not get_cmd:  
            print("[-] Connection closed by client.")
            break 

        try:
            if get_cmd.startswith('download '):  
                dfile = get_cmd.split()[1]
                if os.path.isfile(dfile):
                    with open(dfile, 'rb') as file:
                        con.sendfile(file)  # Send the file
                    con.shutdown(socket.SHUT_WR)  # Close sending side
                    con.close()  # Fully close connection
                    print(f"[+] File '{dfile}' sent successfully.")
                    break  # Exit loop after sending
                else:
                    con.send(f"Error: '{dfile}' is not a file.\n".encode())
            else:
                con.send(f"Invalid command: {get_cmd}\n".encode())

        except Exception as err:
            print(f"Error: {err}")
            con.send(str(err).encode())
            continue

    sock.close()

if __name__ == "__main__":
    main()
