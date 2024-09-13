#!/usr/bin/env python3
"""Test GithubOrgClient
"""

import unittest
from unittest.mock import patch
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class
    """

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the correct list of repositories
        """

        # Define the URL and payload
        test_url = "https://api.github.com/orgs/test-org/repos"
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache"}},
        ]
        expected_repos = ["repo1", "repo2"]

        # Mock get_json to return the test payload
        mock_get_json.return_value = test_payload

        # Patch _public_repos_url property
        with patch.object(
            GithubOrgClient, '_public_repos_url', return_value=test_url
        ):
            client = GithubOrgClient("test-org")

            # Call the public_repos method
            result = client.public_repos()

            # Assert the result is as expected
            self.assertEqual(result, expected_repos)

            # Assert get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(test_url)


if __name__ == '__main__':
    unittest.main()
