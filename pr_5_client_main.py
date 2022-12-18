import socket, threading
from ciphers import Ciphers
m_port = 9090
HOST = 'localhost'
sock = ''

def main():
    sock = socket.socket()
    sock.setblocking(True)
    Ch_p = Ciphers()
    sock.connect((HOST, m_port))
    print(f"Подсоединились к порту: {m_port}")
    keys = Ch_p.getting_key_client(sock)
    priv_k = keys[5]
    port = int(Ch_p.decrypt(priv_k, sock.recv(1024).decode()))
    sock.close()
    sock = socket.socket()
    sock.setblocking(True)
    sock.connect((HOST, port))
    print(f"Привязка к порту: {port}")
    threading.Thread(target=Ch_p.listening, args=(sock,priv_k,), daemon=True).start()
    while True:
        cmd = input()
        if cmd == "exit":
            break
        Ci_cm = Ciphers()
        cmd = Ci_cm.encrypt(priv_k, cmd)
        sock.send(cmd.encode())
    sock.close()

if __name__ == '__main__':
    main()
