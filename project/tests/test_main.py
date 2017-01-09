import unittest
import mock
import json

from project.server.main.models import GitHubFormater

class TestModelsGithubFormater(unittest.TestCase):

    GITHUBFIELDS = [
            'name',
            'avatar_url',
            'html_url',
            'created_at',
            'owner_login',
            'sha',
            'commit_message',
            'commit_author_name'
    ]

    def test_formatDate(self):
        githubFormatter = GitHubFormater(None)
        dateString = '2017-01-09T02:51:06Z'
        self.assertEqual(githubFormatter.formatDate(dateString), '2017-01-09')

        dateString = None
        self.assertEqual(githubFormatter.formatDate(dateString), '')

        dateString = 'not parseable'
        self.assertEqual(githubFormatter.formatDate(dateString), '')

    def test_formatRepositoryEmptyData(self):
        githubFormatter = GitHubFormater(None)
        githubFormatter.getLatestCommit = mock.Mock(return_value={})
        
        self.assertEqual(githubFormatter.formatRepository({}), [])

    def test_formatRepositoryEmptyItems(self):
        githubFormatter = GitHubFormater(None)
        githubFormatter.getLatestCommit = mock.Mock(return_value={})
        
        self.assertEqual(githubFormatter.formatRepository({'items': []}), [])

    def test_formatRepositoryEmptyFields(self):
        githubFormatter = GitHubFormater(None)
        githubFormatter.getLatestCommit = mock.Mock(return_value={})
        payload = json.loads('{"items": [{"meod": "some"}]}')
        result = githubFormatter.formatRepository(payload)
        self.assertEqual(result[0]['name'], '')
        self.assertTrue( all (k in self.GITHUBFIELDS for k in result[0]))

    def test_formatRepositorySomeFields(self):
        githubFormatter = GitHubFormater(None)
        githubFormatter.getLatestCommit = mock.Mock(return_value={})
        payload = json.loads('{"items": [{"name": "some"}]}')
        result = githubFormatter.formatRepository(payload)
        self.assertEqual(result[0]['name'], 'some')
        self.assertTrue( all (k in self.GITHUBFIELDS for k in result[0]))