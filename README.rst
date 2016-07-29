=================================
Accountable - a Jira CLI
=================================
.. image:: https://travis-ci.org/wohlgejm/accountable.svg?branch=master
    :target: https://travis-ci.org/wohlgejm/accountable
.. image:: https://coveralls.io/repos/github/wohlgejm/accountable/badge.svg?branch=master
    :target: https://coveralls.io/github/wohlgejm/accountable?branch=master
.. image:: https://requires.io/github/wohlgejm/accountable/requirements.svg?branch=master
     :target: https://requires.io/github/wohlgejm/accountable/requirements/?branch=master
     :alt: Requirements Status

Never leave the command line to update a ticket again.

Quickstart
===============
Installation:

``pip install accountable``

Once installed, configure your account:

``accountable configure``

List all projects:

``accountable projects``

List all issue types:

``accountable issuetypes`` or ``accountable issuetypes DEV``

List metadata for an individual issue:

``accountable issue DEV-101``

Add a comment to an issue:

``accountable issue DEV-102 addcomment "[~tpm] I'm BLOCKED"``

List available transitions for an issue:

``accountable issue DEV-103 transitions``

Do a transition for an issue:

``accountable issue DEV-104 dotransition 1``

Configuring
===========
Currently, only Basic Auth is supported. Running `accountable configure` will prompt you to enter
your username, password, and your Jira domain.

Since every account can be setup differently you might want to view custom fields for an issue.
By default, the following fields are displayed when examining an issue:

1. Reporter - Display name
2. Assignee - Display name
3. Issue type - name
4. Status - Status category - name
5. Summary
6. Description

These defaults can be changed by editing your `~/.accountable/config.yaml`. Nesting fields is supported. Check out
the Jira documentation `here <https://docs.atlassian.com/jira/REST/latest/#api/2/issue-getIssue>`_ for information
on fields in the payload.

Using with Githooks
===================

TODO
====
- Using with pomodoro
- OAuth


Why?
====
Jira already supports robust triggers, like changing a ticket's status
based on a pull request, or a branch being created. You can also transition tickets with commit messages.

However, there are times when these automated triggers aren't enough.

Often, you'll start work locally, and forget to put the ticket in progress. Or you'll forget to add
a transition to a commit message. Multiple actions listed in your commit message also aren't relevant
to the project's history.
