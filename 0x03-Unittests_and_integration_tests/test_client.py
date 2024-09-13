#!/usr/bin/env python3
"""Test GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value
        """

        # Define the mock response
        mock_response = {
            "repos_url": "https://api.github.com/orgs/{org}/repos"
        }
        mock_get_json.return_value = mock_response

        # Create a GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Call the org method
        result = client.org

        # Ensure get_json was called exactly once with the expected URL
        mock_get_json.assert_called_once_with(
            client.ORG_URL.format(org=org_name)
        )

        # Check if the result is as expected
        self.assertEqual(result, mock_response)


if __name__ == '__main__':
    unittest.main()
