import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import unittest
import requests_mock
from tastytrade_api.authentication import TastytradeAuth
from tastytrade_api.account.account_handler import TastytradeAccount
from tastytrade_api import ValidationError, AccountError

def dummy_customer_resource_data(email: str, is_professional: bool):
    """
    Example data retrieved from:
    https://developer.tastytrade.com/open-api-spec/accounts-and-customers/
    """
    return {
        "has-institutional-assets": "string",
        "visa-expiration-date": "string",
        "gender": "string",
        "second-surname": "string",
        "last-name": "string",
        "political-organization": "string",
        "middle-name": "string",
        "entity": {
            "is-domestic": "string",
            "entity-type": "string",
            "entity-officers": [
                {
                    "relationship-to-entity": "string",
                    "visa-expiration-date": "2023-08-07",
                    "last-name": "string",
                    "middle-name": "string",
                    "work-phone-number": "string",
                    "prefix-name": "string",
                    "visa-type": "string",
                    "number-of-dependents": "string",
                    "suffix-name": "string",
                    "job-title": "string",
                    "birth-country": "string",
                    "first-name": "string",
                    "occupation": "string",
                    "marital-status": "string",
                    "tax-number": "string",
                    "citizenship-country": "string",
                    "usa-citizenship-type": "string",
                    "owner-of-record": True,
                    "is-foreign": "string",
                    "employment-status": "string",
                    "mobile-phone-number": "string",
                    "address": {
                        "is-domestic": "string",
                        "street-two": "string",
                        "city": "string",
                        "postal-code": "string",
                        "state-region": "string",
                        "is-foreign": "string",
                        "street-three": "string",
                        "country": "string",
                        "street-one": "string"
                    },
                    "home-phone-number": "string",
                    "id": "string",
                    "tax-number-type": "string",
                    "email": email,
                    "birth-date": "2023-08-07",
                    "employer-name": "string",
                    "external-id": "string"
                }
            ],
            "phone-number": "string",
            "grantor-birth-date": "string",
            "has-foreign-bank-affiliation": "string",
            "tax-number": "string",
            "grantor-email": "string",
            "has-foreign-institution-affiliation": "string",
            "entity-suitability": {
                "entity-id": 0,
                "tax-bracket": "string",
                "annual-net-income": 0,
                "liquid-net-worth": 0,
                "stock-trading-experience": "string",
                "futures-trading-experience": "string",
                "uncovered-options-trading-experience": "string",
                "id": "string",
                "covered-options-trading-experience": "string",
                "net-worth": 0
            },
            "grantor-last-name": "string",
            "business-nature": "string",
            "address": {
                "is-domestic": "string",
                "street-two": "string",
                "city": "string",
                "postal-code": "string",
                "state-region": "string",
                "is-foreign": "string",
                "street-three": "string",
                "country": "string",
                "street-one": "string"
            },
            "grantor-middle-name": "string",
            "grantor-first-name": "string",
            "grantor-tax-number": "string",
            "id": "string",
            "email": "string",
            "legal-name": "string",
            "foreign-institution": "string"
        },
        "work-phone-number": "string",
        "permitted-account-types": "string",
        "foreign-tax-number": "string",
        "listed-affiliation-symbol": "string",
        "prefix-name": "string",
        "visa-type": "string",
        "suffix-name": "string",
        "birth-country": "string",
        "first-name": "string",
        "signature-of-agreement": True,
        "is-professional": is_professional,
        "agreed-to-terms": True,
        "industry-affiliation-firm": "string",
        "subject-to-tax-withholding": True,
        "tax-number": "string",
        "citizenship-country": "string",
        "usa-citizenship-type": "string",
        "has-political-affiliation": True,
        "customer-suitability": {
            "tax-bracket": "string",
            "number-of-dependents": 0,
            "annual-net-income": 0,
            "job-title": "string",
            "customer-id": 0,
            "occupation": "string",
            "marital-status": "string",
            "liquid-net-worth": 0,
            "stock-trading-experience": "string",
            "employment-status": "string",
            "futures-trading-experience": "string",
            "uncovered-options-trading-experience": "string",
            "id": "string",
            "covered-options-trading-experience": "string",
            "employer-name": "string",
            "net-worth": 0
        },
        "identifiable-type": "string",
        "is-foreign": "string",
        "mailing-address": {
            "is-domestic": "string",
            "street-two": "string",
            "city": "string",
            "postal-code": "string",
            "state-region": "string",
            "is-foreign": "string",
            "street-three": "string",
            "country": "string",
            "street-one": "string"
        },
        "has-listed-affiliation": True,
        "is-investment-adviser": "string",
        "mobile-phone-number": "string",
        "has-industry-affiliation": True,
        "address": {
            "is-domestic": "string",
            "street-two": "string",
            "city": "string",
            "postal-code": "string",
            "state-region": "string",
            "is-foreign": "string",
            "street-three": "string",
            "country": "string",
            "street-one": "string"
        },
        "person": {
            "visa-expiration-date": "2023-08-07",
            "last-name": "string",
            "middle-name": "string",
            "prefix-name": "string",
            "visa-type": "string",
            "number-of-dependents": "string",
            "suffix-name": "string",
            "job-title": "string",
            "birth-country": "string",
            "first-name": "string",
            "occupation": "string",
            "marital-status": "string",
            "citizenship-country": "string",
            "usa-citizenship-type": "string",
            "employment-status": "string",
            "birth-date": "2023-08-07",
            "employer-name": "string",
            "external-id": "string"
        },
        "has-delayed-quotes": True,
        "desk-customer-id": "string",
        "home-phone-number": "string",
        "agreed-to-margining": True,
        "id": "string",
        "has-pending-or-approved-application": "string",
        "tax-number-type": "string",
        "email": email,
        "birth-date": "string",
        "user-id": "string",
        "external-id": "string",
        "family-member-names": "string",
        "first-surname": "string"
    }

def dummy_account_data(nickname: str):
    """
    Example data retrieved from:
    https://developer.tastytrade.com/open-api-spec/accounts-and-customers/
    """
    return {
        "account": {
            "day-trader-status": "string",
            "futures-account-purpose": "string",
            "liquidity-needs": "string",
            "account-number": "string",
            "nickname": nickname,
            "suitable-options-level": "string",
            "risk-tolerance": "string",
            "is-closed": True,
            "is-foreign": "string",
            "is-test-drive": "string",
            "is-firm-proprietary": True,
            "closed-at": "2023-08-07T19:30:11.834Z",
            "investment-time-horizon": "string",
            "ext-crm-id": "string",
            "submitting-user-id": "string",
            "opened-at": "2023-08-07T19:30:11.834Z",
            "is-futures-approved": True,
            "created-at": "2023-08-07T19:30:11.834Z",
            "external-fdid": "string",
            "is-firm-error": True,
            "external-id": "string",
            "funding-date": "2023-08-07",
            "account-type-name": "string",
            "margin-or-cash": "string",
            "investment-objective": "string"
        },
        "authority-level": "string"
    }

class MockAuth:
    def __init__(self, valid: bool, session_token):
        self.valid = valid
        self.session_token = session_token
        self.url = "https://api.tastyworks.com"

    def validate_session(self):
        if self.valid:
            return dict()
        else:
            raise ValidationError("Session not valid")


class TestTastytradeAccount(unittest.TestCase):
    def setUp(self):
        self.auth = MockAuth(True, "session_token")

    def test_init(self):
        with self.subTest("Check that account handler is created with valid session"):
            self.assertIsNotNone(TastytradeAccount(self.auth))

        with self.subTest("Check that the account handler fails with an invalid session"):
            self.auth.valid = False
            with self.assertRaises(ValidationError):
                TastytradeAccount(self.auth)

    @requests_mock.Mocker()
    def test_get_accounts(self, mock):
        mock_response = {
            "data": {
                "items": [dummy_account_data("dummy_nickname")]
            }
        }

        with self.subTest("Check that account list is returned"):
            mock.get(f"{self.auth.url}/customers/me/accounts", json=mock_response, status_code=200)
            account = TastytradeAccount(self.auth)
            data = account.get_accounts()
            self.assertIs(len(data), 1)
            self.assertEqual(data[0]["account"]["nickname"], "dummy_nickname")

        with self.subTest("Check that a bad request results in an exception"):
            mock.get(f"{self.auth.url}/customers/me/accounts", json=mock_response, status_code=400)
            with self.assertRaises(AccountError):
                data = account.get_accounts()

    @requests_mock.Mocker()
    def test_get_customer(self, mock):
        mock_response = {
            "data": dummy_customer_resource_data("email@gmail.com", False)
        }

        with self.subTest("Check that the full customer resource is returned"):
            mock.get(f"{self.auth.url}/customers/me", json=mock_response, status_code=200)
            account = TastytradeAccount(self.auth)
            data = account.get_customer()
            self.assertEqual(data["email"], "email@gmail.com")
            self.assertEqual(data["entity"]["entity-officers"][0]["email"], "email@gmail.com")
            self.assertEqual(data["is-professional"], False)

        with self.subTest("Check that a bad request results in an exception"):
            mock.get(f"{self.auth.url}/customers/me", json=mock_response, status_code=400)
            with self.assertRaises(AccountError):
                data = account.get_customer()

if __name__ == '__main__':
    unittest.main()
