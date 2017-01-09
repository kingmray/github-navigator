import json
import dateutil.parser
import logging
import sys

class GitHubFormater(object):

    """docstring for GitHubFormater"""
    def __init__(self, github):
        super(GitHubFormater, self).__init__()
        self.github = github

    def getRepositories(self, query_string):
        url = 'https://api.github.com/search/repositories?q={0}&sort=updated&page=1&per_page=5'.format(query_string)
        repositories_response = self.github.get(url)
        repositories = json.loads(repositories_response.text)

        return self.formatRepository(repositories)

    def formatRepository(self, repositories):
        if not 'items' in repositories:
            return []
        formated_repositories = []
        for item in repositories['items']:
            formated_repositories.append(self.formatResults(item))

        return formated_repositories

    def getLatestCommit(self, item):
        commits_url = 'https://api.github.com/repos/{0}/{1}/commits'.format(item['owner']['login'], item['name'])
        commits_response = self.github.get(commits_url)
        commits = json.loads(commits_response.text)

        try:
            return commits[0]
        except KeyError:
            return {}

    def formatResults(self, item):
        commit = self.getLatestCommit(item)
        
        repository = {
            'name': self.getFieldFromDict(item, ['name']),
            'avatar_url': self.getFieldFromDict(item, ['owner','avatar_url']),
            'html_url': self.getFieldFromDict(item,['html_url']),
            'created_at': self.formatDate(self.getFieldFromDict(item, ['created_at'])),
            'owner_login': self.getFieldFromDict(item, ['owner','login']),
            'sha': self.getFieldFromDict(commit, ['sha']),
            'commit_message': self.getFieldFromDict(commit, ['commit','message']),
            'commit_author_name': self.getFieldFromDict(commit, ['commit','author','name'])
        }

        return repository

    def formatDate(self, dateStr):
        try:
            date = dateutil.parser.parse(dateStr)
            return date.strftime('%Y-%m-%d')
        except (TypeError, ValueError) as e:
            return ''

    def getFieldFromDict(self, dictionary, fields):
        try:
            return self.recursive_get(dictionary, fields)
        except KeyError:
            return ""

    def recursive_get(self, d, keys):
        if len(keys) == 1:
            return d[keys[0]]
        return self.recursive_get(d[keys[0]], keys[1:])
        
        