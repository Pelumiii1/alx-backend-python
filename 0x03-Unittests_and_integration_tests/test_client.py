#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock

from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    @patch('client.get_json')
    def test_org(self,org_name,mock_get_json):
        expected = {"login":org_name, "id":123}
        mock_get_json.return_value = expected
        
        client = GithubOrgClient(org_name)
        result = client.org
    
        self.assertEqual(result,expected)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        
    @patch.object(GithubOrgClient, "org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        expected_url = "https://api.github.com/orgs/testorg/repos"
        mock_org.return_value = {"repos_url": expected_url}

        client = GithubOrgClient("testorg")
        self.assertEqual(client._public_repos_url, expected_url)
        
    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):

        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_payload

        with patch.object(GithubOrgClient, "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2", "repo3"])

            mock_get_json.assert_called_once_with("https://api.github.com/orgs/testorg/repos")
            mock_url.assert_called_once()
            
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns correct boolean based on license key"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
