import os
from github3 import login
from configparser import ConfigParser
import xml.etree.ElementTree as ElementTree


CONFIG_DIR = None
for config_dir in os.path.expanduser('~/.local/share/gitvotal/config'), os.path.join(os.curdir, 'config', 'dev'), \
                  os.path.join(os.curdir, 'config', 'prod'), '/etc/gitvotal':
    CONFIG_DIR = config_dir
    if os.path.isdir(CONFIG_DIR) and os.path.exists(CONFIG_DIR):
        break
CONFIG_FILE = os.path.join(CONFIG_DIR, 'config.ini')
config = ConfigParser()
with open(CONFIG_FILE, 'r') as fp:
    config.read_file(fp)


def get_github_issues():
    gh = login(token=config.get('github', 'token'))
    user = config.get('github', 'target_user', fallback='')
    result = ElementTree.Element('external_stories')
    result.set('type', 'array')
    for repo in config.get('github', 'target_repositories', fallback='').split(','):
        issues = gh.repository(user, repo).issues(state='open')
        for issue in issues:
            issue_element = ElementTree.SubElement(result, 'external_story')
            ElementTree.SubElement(issue_element, 'external_id').text = "{0}-{1}".format(repo, issue.number)
            ElementTree.SubElement(issue_element, 'name').text = issue.title
            ElementTree.SubElement(issue_element, 'description').text = issue.body_text
            ElementTree.SubElement(issue_element, 'requested_by').text = issue.user.login
            created_at_element = ElementTree.SubElement(issue_element, 'created_at')
            created_at_element.set('type', 'datetime')
            created_at_element.text = str(issue.created_at)
            ElementTree.SubElement(issue_element, 'story_type').text = 'feature'
            ElementTree.SubElement(issue_element, 'estimate_type').text = '1'
    return ElementTree.tostring(result)


def issue_url(the_id):
    repo_name, issue_id = the_id.rsplit('-', 1)
    user = config.get('github', 'target_user', fallback='')
    return "https://github.com/{0}/{1}/issues/{2}".format(user, repo_name, issue_id)
