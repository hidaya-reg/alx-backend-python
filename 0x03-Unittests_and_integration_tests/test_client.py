#!/usr/bin/env python3
"""
Unit tests for the client.GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        Args:
            org_name (str): Organization name to test.
            mock_get_json: Mock object for get_json.
        """
        # Create an instance of GithubOrgClient
        client = GithubOrgClient(org_name)

        # Define the expected URL
        expected_url = f"https://api.github.com/orgs/{org_name}"

        # Mock the return value of get_json (although not used in this test)
        mock_get_json.return_value = {}

        # Call the org method
        client.org()

        # Assert get_json was called once with the correct URL
        mock_get_json.assert_called_once_with(expected_url)


if __name__ == "__main__":
    unittest.main()
