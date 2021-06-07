import socket

HOST = "127.0.0.1"
PORT = 8000
CODER = "utf-8"
BUFFER = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Please login (use pattern -> login:password)")

    while True:
        msg = input(">>> ").encode(CODER)
        s.send(msg)
        data = s.recv(BUFFER).decode(CODER)

        if data == "CONNECTION CLOSED" or "Unsuported" in data or not data:
            print(data)
            break

        print("From Server --> " + "\n" + data)
