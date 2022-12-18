import random, csv
client_file = "client's_key.csv"
server_file = "server's_key.csv"
allow_key = 'allow_key.csv'
class Ciphers:
    @staticmethod
    def encrypt(k, m):
        return ''.join(map(chr, [(x +  k) % 65536 for x in map(ord, m)]))

    @staticmethod
    def decrypt(k, m):
        return ''.join(map(chr, [(x - k) % 65536 for x in map(ord, m)]))

    @staticmethod
    def listening(m, k):
        while True:
            msg = m.recv(1024).decode()
            msg = Ciphers.decrypt(k, msg)
            print(msg)
    @staticmethod
    def getting_key_client(sock):
        global client_file
        key_from_server = sock.recv(1024).decode().split("|")
        key_from_server = [int(item) for item in key_from_server]
        try:
            keys = Ciphers.reading_keys_client(sock)
        except FileNotFoundError:
            ran = random.randint(100, 999)
            f_k = key_from_server[0]
            s_k = key_from_server[1]
            new_ran = pow(f_k, ran) % s_k
            serv_a = key_from_server[2]
            private = pow(serv_a, ran) % s_k
            keys = [ran, f_k, s_k, new_ran, serv_a, private]
            with open(client_file, "w", newline="") as keyfile:
                writer = csv.writer(keyfile, delimiter=";")
                writer.writerow(keys)
        sock.send(str(keys[3]).encode())
        return keys
    @staticmethod
    def reading_keys_client(sock):
        global client_file
        with open(client_file, "r", newline="") as file:
            reader = csv.reader(file, delimiter=";")
            return [int(item) for item in next(reader)]

    @staticmethod
    def reading_key_server(addr):
        with open(server_file, "r", newline="") as keyfile:
            reader = csv.reader(keyfile, delimiter=";")
            for row in reader:
                if row[0] == addr[0]:
                    return row[1:]
            else:
                raise FileNotFoundError

    @staticmethod
    def getting_key_server(conn, addr):
        try:
            keys = Ciphers.reading_key_server(addr)
        except FileNotFoundError:
            f_1, f_2, f_3 = [random.randint(100, 999) for _ in range(3)]
            my_a = pow(f_2, f_1) % f_3
            conn.send(f"{f_2}|{f_3}|{my_a}".encode())
            cli_b = int(conn.recv(1024).decode())
            private = pow(cli_b, f_1) % f_3
            keys = [f_1, f_2, f_3, my_a, cli_b, private]

            with open(server_file, "w", newline="") as keyfile:
                writer = csv.writer(keyfile, delimiter=";")
                writer.writerow((addr[0], *keys))
        else:
            keys = [int(item) for item in keys]
            conn.send(f"{keys[1]}|{keys[2]}|{keys[3]}".encode())
            cli_b = int(conn.recv(1024).decode())
        return keys[5], cli_b
    @staticmethod
    def permission(cli_b):
        with open(allow_key, "r", newline="") as keyfile:
            reader = csv.reader(keyfile, delimiter=";")
            for row in reader:
                if int(row[0]) == cli_b:
                    return True
            else:
                return False
