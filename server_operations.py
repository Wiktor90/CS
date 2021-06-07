from datetime import datetime

from users import User


class Server(object):
    @staticmethod
    def send_msg(conn, msg, coder="utf-8"):
        conn.send(msg.encode(coder))

    @staticmethod
    def recv_msg(conn, buffer=1024, coder="utf-8"):
        return conn.recv(buffer).decode(coder)

    @staticmethod
    def server_created_date():
        dt = datetime.now()
        dt = dt.strftime("%d/%m/%Y %H:%M:%S")
        return dt

    def __init__(self):
        self.version = "Server v.3.1"
        self.created = Server.server_created_date()
        self.start_time = datetime.now()
        self.commands = {
            "help": "commands list with short description",
            "uptime": "return server life time",
            "info": "info about server version, server created date",
            "send": "send direct message to another user",
            "read": "read messages from box",
            "clear": "delete all messages from box",
            "stop": "connection closed (end client / server)",
            "reset": "reset user password (ADMIN ONLY)",
            "create": "create new user (ADMIN ONLY)",
            "delete": "remove user from database (ADMIN ONLY)",
        }
        self.handlers = {
            "info": self.show_server_info,
            "help": self.show_server_commands,
            "uptime": self.show_server_uptime,
            "create": self.create_new_user,
            "delete": self.delete_user,
            "reset": self.reset_password,
            "send": self.send_msg_to_user,
            "read": self.read_msg_box,
            "clear": self.clear_user_box,
            "stop": self.connection_closed,
        }

    def server_uptaime(self):
        now = datetime.now()
        uptime = str(now - self.start_time)
        return uptime[:-7]

    # LOGIN
    def create_user(slef, data):
        userdata = data.split(":")
        if len(userdata) == 3 and userdata[2].upper() in ["USER", "ADMIN"]:
            return User(userdata[0], userdata[1], userdata[2])
        return None

    def login(self, username, password, rights):
        return User(username, password, rights)

    def user_login_to_account(self, db, conn):
        """Return User if exist in DB or None"""

        credentials = self.recv_msg(conn).split(":")
        rights = db.check_user_credentials(credentials[0], credentials[1])

        if rights:
            logged_user = self.login(credentials[0], credentials[1], rights)
            self.send_msg(
                conn,
                f"{logged_user.username}({logged_user.rights}) - Login successful.",
            )
            return logged_user

        self.send_msg(conn, f'"{credentials[0]}" NOT exists or password not match! Try again.')
        return None

    # HANDLERS
    def show_server_info(self):
        return "info", f"{self.version} | created: {self.created}"

    def show_server_commands(self):
        return "help", self.commands

    def show_server_uptime(self):
        return "uptime", self.server_uptaime()

    def create_new_user(self, db, logged_user, conn):
        if logged_user.rights == "ADMIN":
            self.send_msg(conn, "Create: Enter -> username:password:rights")
            recv = self.recv_msg(conn)
            user = self.create_user(recv)

            if user:
                db.add_user_to_DB(user.get_user_data())
                db.save_data_to_file()
                print("\n" + "DataBase updated:" + "\n", db.show_data())
                return user.username, user.password
            else:
                return "ERROR", "Invalid data"
        return "ERROR", "Permission denied"

    def delete_user(self, db, logged_user, conn):
        if logged_user.rights == "ADMIN":
            self.send_msg(conn, "Delete: Enter -> username")
            recv = self.recv_msg(conn)
            user = db.delete_user_from_DB(recv)

            if user:
                db.save_data_to_file()
                print("\n" + "DataBase updated:" + "\n", db.show_data())
                return user["username"], "DELETED"
            else:
                return recv, "NOT FOUND"
        return "ERROR", "Permission denied"

    def reset_password(self, db, logged_user, conn):
        if logged_user.rights == "ADMIN":
            self.send_msg(conn, "Reset: Enter -> user:(new)password")
            recv = self.recv_msg(conn).split(":")
            user_pass = db.password_reset(recv[0], recv[1])

            if user_pass:
                db.save_data_to_file()
                print("\n" + "DataBase updated:" + "\n", db.show_data())
                return user_pass["username"], user_pass["password"]
            else:
                return recv[0], "NOT FOUND"
        return "ERROR", "Permission denied"

    def send_msg_to_user(self, db, logged_user, conn):
        self.send_msg(conn, "Send MSG: Enter -> user:text(255)")
        recv = self.recv_msg(conn).split(":")
        direct_msg = db.send_direct_msg(recv[0], logged_user.username, recv[1])

        if direct_msg:
            db.save_data_to_file()
            print("\n" + "DataBase updated:" + "\n", db.show_data())
            return "SENT-STATUS", direct_msg
        else:
            return recv[0], "NOT FOUND"

    def read_msg_box(self, db, logged_user, conn):
        msg_box = db.read_msg_box(logged_user.username)
        return "Box", msg_box

    def clear_user_box(self, db, logged_user, conn):
        """func. clears users msg box by delault
        but admin has right to choose username"""

        if logged_user.rights == "ADMIN":
            self.send_msg(conn, "Clear Box: Enter -> username")
            recv = self.recv_msg(conn)
            clear_box = db.clear_msg_box(recv)

            if clear_box:
                db.save_data_to_file()
                print("\n" + "DataBase updated:" + "\n", db.show_data())
                return "Box", {}
            else:
                return recv, "NOT FOUND"

        clear_box = db.clear_msg_box(logged_user.username)
        db.save_data_to_file()
        print("\n" + "DataBase updated:" + "\n", db.show_data())
        return "Box", {}

    def connection_closed(self, conn):
        self.send_msg(conn, "CONNECTION CLOSED")
        print("CONNECTION CLOSED")
