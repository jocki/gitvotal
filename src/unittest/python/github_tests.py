import unittest
from gitvotal import github


class GithubTest(unittest.TestCase):

    def test_get_github_issue(self):
        github.get_github_issues()

    def test_open_issue(self):
        github.config.set('github', 'target_user', 'user1')
        self.assertEqual("https://github.com/user1/repo1/issues/148", github.issue_url('repo1-148'))
        self.assertEqual("https://github.com/user1/test-repo1/issues/148", github.issue_url('test-repo1-148'))
