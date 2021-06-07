import json
import socket

from database import DataBase
from server_operations import Server

# run needed instances before creating connection
server = Server()
db = DataBase()
HOST = "127.0.0.1"
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    connection, address = s.accept()  # socket ojb to communicate with client

    with connection:
        print(f"Connected by: {address[0]} | {address[1]}")

        # LOGIN TO ACCOUNT
        while True:
            try:
                logged_user = server.user_login_to_account(db, connection)
            except IndexError:
                server.send_msg(connection, "Wrong login pattern! Try again")
                continue
            if logged_user:
                break

        # SERVER COMMAND HANDLING
        while True:
            key = server.recv_msg(connection)

            if key == "stop":
                server.connection_closed(connection)
                break
            elif key in ["help", "info", "uptime"]:
                handler = server.handlers[key]()
            else:
                try:
                    handler = server.handlers[key](db, logged_user, connection)
                except KeyError:
                    server.send_msg(connection, f'Unsuported command: "{key}"')
                    break
                except IndexError:
                    server.send_msg(
                        connection, f'Unsuported data format for command: "{key}"'
                    )
                    break

            key, value = handler[0], handler[1]
            msg = json.dumps({key: value}, indent=2)
            server.send_msg(connection, msg)
