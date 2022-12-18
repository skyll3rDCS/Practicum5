import socket, random, threading
from ciphers import Ciphers
m_port = 9090
HOST = 'localhost'
sock = ''

def sock_made(port = m_port):
    sock = socket.socket()
    sock.setblocking(True)
    sock.bind(('', port))
    print(f"Привязка к порту: {port}")
    sock.listen(0)
    conn, addr = sock.accept()
    return sock, conn, addr

def port_made(sock, conn, private_key):
    port = random.randint(1024,65535)
    Ch_p=Ciphers()
    conn.send(Ch_p.encrypt(private_key, str(port)).encode())
    sock.close()
    return sock_made(port)

def main():
    Ch_l = Ciphers()
    sock, conn, addr = sock_made()
    private_key, perm_key = Ch_l.getting_key_server(conn, addr)
    if True:
        sock, conn, addr = port_made(sock, conn, private_key)
        threading.Thread(target=Ch_l.listening, args=(conn,private_key,), daemon=True).start()
        while True:
            cmd = input()
            if cmd == "exit":
                break
            cmd = Ciphers.encrypt(private_key, cmd)
            conn.send(cmd.encode())
    else: print("Входящий сертификат не найден в списке")
    sock.close()
if __name__ == '__main__':
    main()
