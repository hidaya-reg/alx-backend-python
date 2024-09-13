#!/usr/bin/env python3
"""A module for testing the client module.
"""

import unittest
from unittest.mock import (
    MagicMock,
    PropertyMock,
    patch,
)
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests the `GithubOrgClient` class."""

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method."""

        # Define test payload
        test_repos_url = "https://api.github.com/users/google/repos"
        test_payload = [
            {
                "id": 7697149,
                "name": "episodes.dart",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004,
                },
                "fork": False,
                "url": "https://api.github.com/repos/google/episodes.dart",
                "created_at": "2013-01-19T00:31:37Z",
                "updated_at": "2019-09-23T11:53:58Z",
                "has_issues": True,
                "forks": 22,
                "default_branch": "master",
            },
            {
                "id": 8566972,
                "name": "kratu",
                "private": False,
                "owner": {
                    "login": "google",
                    "id": 1342004,
                },
                "fork": False,
                "url": "https://api.github.com/repos/google/kratu",
                "created_at": "2013-03-04T22:52:33Z",
                "updated_at": "2019-11-15T22:22:16Z",
                "has_issues": True,
                "forks": 32,
                "default_branch": "master",
            }
        ]

        mock_get_json.return_value = test_payload

        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
                ) as mock_public_repos_url:

            mock_public_repos_url.return_value = test_repos_url

            gh_org_client = GithubOrgClient("google")
            self.assertEqual(
                gh_org_client.public_repos(),
                ["episodes.dart", "kratu"]
            )

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)


if __name__ == '__main__':
    unittest.main()
