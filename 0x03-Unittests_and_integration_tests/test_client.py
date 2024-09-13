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
        ("google", "https://api.github.com/orgs/google/repos", [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache"}},
        ], ["repo1", "repo2"]),
        ("abc", "https://api.github.com/orgs/abc/repos", [
            {"name": "repoA", "license": {"key": "mit"}},
            {"name": "repoB", "license": {"key": "gpl"}},
        ], ["repoA", "repoB"]),
    ])
    @patch('client.get_json')
    def test_public_repos(
        self, org_name, repos_url, mock_response, expected_repos, mock_get_json
    ):
        """Test that public_repos returns the correct list of repositories
        """

        # Define the mock response for get_json
        mock_get_json.return_value = mock_response

        # Patch the _public_repos_url property
        with patch.object(
            GithubOrgClient, '_public_repos_url', return_value=repos_url
        ):
            client = GithubOrgClient(org_name)

            # Call the public_repos method
            result = client.public_repos()

            # Assert the result is as expected
            self.assertEqual(result, expected_repos)

            # Assert get_json was called once with the expected URL
            mock_get_json.assert_called_once_with(repos_url)


if __name__ == '__main__':
    unittest.main()
