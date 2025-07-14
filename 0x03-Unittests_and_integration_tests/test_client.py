#!/usr/bin/env python3

import unittest
from parameterized import parameterized
from parameterized import parameterized_class
from unittest.mock import patch, PropertyMock,Mock
from fixtures import TEST_PAYLOAD
from client import GithubOrgClient
from requests import HTTPError
 

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

@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Performs integration tests for the `GithubOrgClient` class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Sets up class fixtures before running tests."""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the `public_repos` method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the `public_repos` method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Removes the class fixtures after running all tests."""
        cls.get_patcher.stop()  
