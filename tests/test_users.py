import os
import sys

sys.path.insert(0, os.getcwd())

import unittest

from server_operations import Server
from users import User


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.server = Server()
        self.user = User("Adam", "testing999", "user")
        self.data = "Adam:testing999:user"

    def test_is_created_user_User_instance(self):
        self.assertIsInstance(self.server.create_user(self.data), type(self.user))

    def test_is_logged_user_User_instance(self):
        self.assertIsInstance(
            self.server.login("TestUser", "pass", "user"), type(self.user)
        )

    def test_get_user_info_have_good_data_type(self):
        self.assertIs(type(self.user.get_user_data()), dict)


if __name__ == "__main__":
    unittest.main()
