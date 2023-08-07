import requests
import json
from .exceptions import AccountError

class TastytradeAccount:
    """
    Initializes a new instance of the API client with the given session object.

    Args:
        auth (TastytradeAuth): Authenticated session object

    Raises:
        ValidationError: If the session is invalid.
    """

    def __init__(self, auth):
        auth.validate_session()
        self.session_token = auth.session_token
        self.url = auth.url
        self.headers = {"Authorization": f"{self.session_token}"}

    def _raise_account_error(self, msg, response):
        raise AccountError(
            f"\n{msg}\n"
            f"url: {self.url}\n"
            f"headers: {self.headers}\n"
            f"status_code: {response.status_code}\n"
            f"reason: {response.reason}\n"
            f"text: {response.text}"
        )

    def get_accounts(self):
        """
        Makes a GET request to the /customers/me/accounts API endpoint for the authenticated customer's accounts,
        and returns a list of account objects.

        Returns:
            list: List of account objects, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        response = requests.get(
            f"{self.url}/customers/me/accounts", headers=self.headers
        )
        if response.status_code == 200:
            response_data = json.loads(response.content)
            accounts = response_data["data"]["items"]
            return accounts
        else:
            self._raise_account_error("Error getting accounts", response)

    def get_customer(self):
        """
        Makes a GET request to the /customers/{customer_id} API endpoint for a specific customer,
        and returns the customer object.

        Returns:
            dict: The customer object, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        response = requests.get(f"{self.url}/customers/me", headers=self.headers)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            customer = response_data["data"]
            return customer
        else:
            self._raise_account_error("Error getting customer", response)

    def get_customer_account(self, account_number):
        """
        Makes a GET request to the /customers/me/accounts/{account_number} API endpoint for the authenticated customer's
        account details, and returns the account object.

        Args:
            account_number (str): The account number for the account to retrieve.

        Returns:
            dict: Dictionary containing the account details, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        response = requests.get(
            f"{self.url}/customers/me/accounts/{account_number}", headers=self.headers
        )
        if response.status_code == 200:
            response_data = json.loads(response.content)
            account = response_data["data"]
            return account
        else:
            self._raise_account_error(f"Error getting account {account_number}", response)

    def get_margin_requirements(self, account_number):
        """
        Makes a GET request to the /margin/accounts/{account_number}/requirements API endpoint
        for the specified account's margin/capital requirements report, and returns the report object.

        Args:
            account_number (str): The account number for the account to retrieve.

        Returns:
            dict: Dictionary containing the margin/capital requirements report, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        response = requests.get(
            f"{self.url}/margin/accounts/{account_number}/requirements",
            headers=self.headers,
        )
        if response.status_code == 200:
            response_data = json.loads(response.content)
            report = response_data["data"]
            return report
        else:
            self._raise_account_error(
                f"Error getting margin requirements for account {account_number}",
                response
            )

    def get_account_net_liq_history(
        self, account_number: str, time_back: str = None, start_time: str = None
    ) -> dict:
        """
        Makes a GET request to the /accounts/{account_number}/net-liq/history endpoint with the specified
        parameters, and returns the response as a JSON object.

        Args:
            account_number (str): The account number for the account to retrieve net liq history.

            time_back (str): The duration of time to retrieve net liq history for. If given, will return data for a specific
            period of time with a pre-defined time interval. Passing 1d will return the previous day of data in 5 minute
            intervals. This param is required if start-time is not given.
            1d - If equities market is open, this will return data starting from market open in 5 minute intervals.
            If market is closed, will return data from previous market open.

            start_time (str): The starting datetime to retrieve net liq history from.
            This param is required is time-back is not given.

        Returns:
            dict: Dictionary containing the response data, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        params = {"time-back": time_back, "start-time": start_time}
        response = requests.get(
            f"{self.url}/accounts/{account_number}/net-liq/history",
            headers=self.headers,
            params=params,
        )
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            self._raise_account_error("Error getting account net liq history", response)

    def get_effective_margin_requirements(self, account_number, underlying_symbol):
        """
        This method is similar to the get_margin_requirements method, except that it retrieves the effective margin
        requirements for a specific underlying symbol rather than the overall margin/capital requirements report.

        Makes a GET request to the /accounts/{account_number}/margin-requirements/{underlying_symbol}/effective endpoint
        for the specified account's effective margin requirements for the given underlying symbol, and returns the response
        as a JSON object.

        Args:
            account_number (str): The account number for the account to retrieve effective margin requirements for.
            underlying_symbol (str): The underlying symbol for which to retrieve effective margin requirements.

        Returns:
            dict: Dictionary containing the effective margin requirements, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        response = requests.get(
            f"{self.url}/accounts/{account_number}/margin-requirements/{underlying_symbol}/effective",
            headers=self.headers,
        )
        if response.status_code == 200:
            response_data = response.json()
            return response_data
        else:
            self._raise_account_error(
                f"Error getting effective margin requirements for account {account_number}",
                response
            )

    def get_position_limit(self, account_number):
        """
        Makes a GET request to the /accounts/{account_number}/position-limit API endpoint for the specified account's
        position limit, and returns the position limit.

        Args:
            account_number (str): The account number for the account to retrieve.

        Returns:
            int: The position limit for the account, as returned by the API.

        Raises:
            AccountError: If there was an error in the GET request or if the status code is not 200 OK.
        """
        response = requests.get(
            f"{self.url}/accounts/{account_number}/position-limit", headers=self.headers
        )
        if response.status_code == 200:
            response_data = json.loads(response.content)
            position_limit = response_data["data"]["positionLimit"]
            return position_limit
        else:
            self._raise_account_error(
                f"Error getting position limit for account {account_number}",
                response
            )
