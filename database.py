import json


class DataBase:

    path = r"C:\Users\pl9891\Desktop\Pozamiataj\L002\CS\DB.json"

    @staticmethod
    def load_db_data(path=path):
        with open(path) as f:
            return json.load(f)

    def __init__(self):
        # self.data = {'DB' : []}
        self.data = DataBase.load_db_data()

    def show_data(self):
        return json.dumps(self.data, indent=2)

    def check_user_in_DB(self, username):
        """return user index if user exists"""
        users = [user["username"] for user in self.data["DB"]]
        if username in users:
            return users.index(username)
        return None

    def add_user_to_DB(self, object_data):
        index = self.check_user_in_DB(object_data["username"])
        if index is None:  # if username not exist in DB
            return self.data["DB"].append(object_data)
        return None

    def delete_user_from_DB(self, username):
        index = self.check_user_in_DB(username)
        if index is not None:
            return self.data["DB"].pop(index)
        return None

    def password_reset(self, username, new_pass):
        index = self.check_user_in_DB(username)
        if index is not None:
            self.data["DB"][index]["password"] = new_pass
            return self.data["DB"][index]
        return None

    def check_user_credentials(self, username, password):
        """checking user credentials and return user rights level"""
        index = self.check_user_in_DB(username)

        if index is not None and self.data["DB"][index]["password"] == password:
            return self.data["DB"][index]["rights"]
        return None

    def send_direct_msg(self, receiver, sender, text):
        index = self.check_user_in_DB(receiver)

        if index is not None:
            user_box = self.data["DB"][index]["box"]

            if len(user_box) < 5 and self.data["DB"][index]["rights"] == "USER":
                msg_index = len(user_box) + 1
                user_box[f"{msg_index}. from {sender}"] = text[:255]
                return "OK"

            elif self.data["DB"][index]["rights"] == "ADMIN":
                msg_index = len(user_box) + 1
                user_box[f"{msg_index}. from {sender}"] = text[:255]
                return "OK"

            else:
                return f"{self.data['DB'][index]['username']} has full msg box!"
        return None

    def read_msg_box(self, username):
        index = self.check_user_in_DB(username)
        if index is not None:
            return self.data["DB"][index]["box"]
        return None

    def clear_msg_box(self, username):
        index = self.check_user_in_DB(username)
        if index is not None:
            self.data["DB"][index]["box"].clear()
            return True
        return None

    def save_data_to_file(self, path=path):
        with open(path, "w") as f:
            json.dump(self.data, f, indent=2)
