import pytest

from accountable.accountable import Accountable


def config_values():
    return {
        'username': 'testusername',
        'password': 'testpassword',
        'domain': 'testdomain',
        'create_config': True,
    }


def projects():
    return [
        ('AC', 'Accountable'),
        ('EX', 'Example Project')
    ]


def issue_types():
    return {
        'AC': [{
            "self": "http://www.example.com/jira/rest/api/2/issueType/1",
            "id": "1",
            "description": "An error in the code",
            "iconUrl": "http://www.example.com/jira/images/icons/issuetypes/bug.png",
            "name": "Bug",
            "subtask": False,
            "fields": {
                "issuetype": {
                    "required": True,
                    "name": "Issue Type",
                    "hasDefaultValue": False,
                    "operations": [
                        "set"
                    ]
                }
            }
        }]
    }


def metadata_response():
    return {
        "expand": "projects",
        "projects": [
            {
                "self": "http://www.example.com/jira/rest/api/2/project/EX",
                "id": "10000",
                "key": "EX",
                "name": "Example Project",
                "avatarUrls": {
                    "48x48": "http://www.example.com/jira/secure/projectavatar?pid=10000&avatarId=10011",
                    "24x24": "http://www.example.com/jira/secure/projectavatar?size=small&pid=10000&avatarId=10011",
                    "16x16": "http://www.example.com/jira/secure/projectavatar?size=xsmall&pid=10000&avatarId=10011",
                    "32x32": "http://www.example.com/jira/secure/projectavatar?size=medium&pid=10000&avatarId=10011"
                },
                "issuetypes": [
                    {
                        "self": "http://www.example.com/jira/rest/api/2/issueType/1",
                        "id": "1",
                        "description": "An error in the code",
                        "iconUrl": "http://www.example.com/jira/images/icons/issuetypes/bug.png",
                        "name": "Bug",
                        "subtask": False,
                        "fields": {
                            "issuetype": {
                                "required": True,
                                "name": "Issue Type",
                                "hasDefaultValue": False,
                                "operations": [
                                    "set"
                                ]
                            }
                        }
                    }
                ]
            },
            {
                "self": "http://www.example.com/jira/rest/api/2/project/AC",
                "id": "10000",
                "key": "AC",
                "name": "Accountable",
                "avatarUrls": {
                    "48x48": "http://www.example.com/jira/secure/projectavatar?pid=10000&avatarId=10011",
                    "24x24": "http://www.example.com/jira/secure/projectavatar?size=small&pid=10000&avatarId=10011",
                    "16x16": "http://www.example.com/jira/secure/projectavatar?size=xsmall&pid=10000&avatarId=10011",
                    "32x32": "http://www.example.com/jira/secure/projectavatar?size=medium&pid=10000&avatarId=10011"
                },
                "issuetypes": [
                    {
                        "self": "http://www.example.com/jira/rest/api/2/issueType/1",
                        "id": "1",
                        "description": "An error in the code",
                        "iconUrl": "http://www.example.com/jira/images/icons/issuetypes/bug.png",
                        "name": "Bug",
                        "subtask": False,
                        "fields": {
                            "issuetype": {
                                "required": True,
                                "name": "Issue Type",
                                "hasDefaultValue": False,
                                "operations": [
                                    "set"
                                ]
                            }
                        }
                    }
                ]
            }
        ]
    }


def worklog():
    return {
    "startAt": 0,
    "maxResults": 1,
    "total": 1,
    "worklogs": [
        {
            "self": "http://www.example.com/jira/rest/api/2/issue/10010/worklog/10000",
            "author": {
                "self": "http://www.example.com/jira/rest/api/2/user?username=fred",
                "name": "fred",
                "displayName": "Fred F. User",
                "active": False
            },
            "updateAuthor": {
                "self": "http://www.example.com/jira/rest/api/2/user?username=fred",
                "name": "fred",
                "displayName": "Fred F. User",
                "active": False
            },
            "comment": "I did some work here.",
            "updated": "2016-02-11T01:20:19.847+0000",
            "visibility": {
                "type": "group",
                "value": "jira-developers"
            },
            "started": "2016-02-11T01:20:19.844+0000",
            "timeSpent": "3h 20m",
            "timeSpentSeconds": 12000,
            "id": "100028",
            "issueId": "10002"
        }
    ]
}


@pytest.fixture
def accountable(tmpdir, **kwargs):
    Accountable.CONFIG_DIR = '{}/.accountable'.format(str(tmpdir))
    Accountable.CONFIG_FILE = '{}/config.yaml'.format(Accountable.CONFIG_DIR)
    return Accountable(**kwargs)
