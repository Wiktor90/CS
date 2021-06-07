import sys

sys.path.insert(0, r"C:\Users\pl9891\Desktop\Pozamiataj\L002\CS")

import unittest

from database import DataBase


class TestDataBase(unittest.TestCase):
    def setUp(self):
        self.db = DataBase()
        # need to have real user from DB to proper tests (index 0 in DB.json)
        self.existing_user = {
            "username": "Wiktor",
            "password": "admin1",
            "rights": "ADMIN",
            "box": {"1. from Wiktor": "test msg"},
        }
        self.new_user = {
            "username": "Ola",
            "password": "test33",
            "rights": "USER",
            "box": {},
        }

    def test_check_user_index_in_DB(self):
        self.assertEqual(self.db.check_user_in_DB(self.existing_user["username"]), 0)
        self.assertEqual(self.db.check_user_in_DB(self.new_user["username"]), None)

    def test_is_only_new_user_added_to_DB(self):
        self.db.add_user_to_DB(self.new_user)
        self.assertIn(self.new_user, self.db.data["DB"])
        self.assertEqual(self.db.add_user_to_DB(self.existing_user), None)

    def test_is_user_deleted_properly(self):
        self.assertEqual(
            self.db.delete_user_from_DB(self.existing_user["username"]),
            self.existing_user,
        )
        self.assertEqual(self.db.delete_user_from_DB(self.new_user["username"]), None)

    def test_password_reset_works_properly(self):
        user_with_changed_pass = self.db.password_reset(
            self.existing_user["username"], "newPass123"
        )
        self.assertEqual(user_with_changed_pass["password"], "newPass123")

    def test_password_and_rights_check(self):
        self.assertEqual(
            self.db.check_user_credentials(
                self.existing_user["username"], self.existing_user["password"]
            ),
            self.existing_user["rights"],
        )

        self.assertEqual(
            self.db.check_user_credentials(
                self.new_user["username"], self.new_user["password"]
            ),
            None,
        )

    def test_sending_direct_message(self):
        msg = self.db.send_direct_msg(
            self.existing_user["username"],
            self.existing_user["username"],
            "beta msg test",
        )

        self.assertEqual(msg, "OK")
        self.assertEqual(
            list(self.db.data["DB"][0]["box"].values())[-1], "beta msg test"
        )

        msg = self.db.send_direct_msg(
            self.new_user["username"], self.existing_user["username"], "beta msg test"
        )

        self.assertEqual(msg, None)

    def test_user_can_read_msg_box(self):
        self.assertEqual(
            self.db.read_msg_box(self.existing_user["username"]),
            self.existing_user["box"],
        )

    def test_user_clear_msg_box(self):
        self.db.clear_msg_box(self.existing_user["username"])
        self.assertEqual(self.db.data["DB"][0]["box"], {})


if __name__ == "__main__":
    unittest.main()
