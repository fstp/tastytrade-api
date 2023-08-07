import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
import requests_mock
from tastytrade_api.authentication import TastytradeAuth
from tastytrade_api.account.account_handler import TastytradeAccount
from tastytrade_api import ValidationError, AccountError


class MockAuth:
    def __init__(self, valid: bool, session_token):
        self.valid = valid
        self.session_token = session_token
        self.url = "https://api.tastyworks.com/sessions"

    def validate_session(self):
        if self.valid:
            return dict()
        else:
            raise ValidationError("Session not valid")


class TestTastytradeAccount(unittest.TestCase):
    def setUp(self):
        self.auth = MockAuth(True, "session_token")

    @requests_mock.Mocker()
    def test_init_success(self, mock):
        with self.subTest("Check account handler created with valid session"):
            self.assertIsNotNone(TastytradeAccount(self.auth))

if __name__ == '__main__':
    unittest.main()
