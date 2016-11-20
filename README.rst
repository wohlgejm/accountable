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
.. image:: https://codeclimate.com/github/wohlgejm/accountable/badges/gpa.svg
   :target: https://codeclimate.com/github/wohlgejm/accountable
   :alt: Code Climate

Never leave the command line to update a ticket again.

Installation
============
``pip install accountable``

or

.. code:: bash

  git clone https://github.com/wohlgejm/accountable
  cd accountable
  python setup.py install

Quickstart
===============
Once installed, configure your account:

``accountable configure``

List all projects:

``accountable projects``

List all issue types:

``accountable issuetypes`` or ``accountable issuetypes DEV``

Create an issue:

``accountable createissue project.id 10000 issuetype.id 3 summary 'Yuge bug'``

See the Jira API docs for a full list of fields. Custom fields are also supported.

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
Currently, only Basic Auth is supported. Running ``accountable configure`` will prompt you to enter
your username, password, and your Jira domain.

Since every account can be setup differently you might want to view custom fields for an issue.
By default, the following fields are displayed when examining an issue:

1. Reporter - Display name
2. Assignee - Display name
3. Issue type - name
4. Status - Status category - name
5. Summary
6. Description

These defaults can be changed by editing your ``~/.accountable/config.yaml``. Nesting fields is supported. Check out
the Jira documentation `here <https://docs.atlassian.com/jira/REST/latest/#api/2/issue-getIssue>`_ for information
on fields in the payload.

Using with git
==============
Accountable can be used in conjunction with git.

For example, if you want to start work and there isn't a ticket created for it, you can use the ``checkoutbranch`` command.

``accountable checkoutbranch summary 'Refactoring foo' project.id 1 issuetype.id 1000``

This will create a new ticket and check you out to a branch. The branch name will be the newly created ticket's key followed by the slugified summary.


TODO
====
- Using with pomodoro
- OAuth

Why?
====
Jira already supports robust triggers, like changing a ticket's status
based on a pull request or a branch being created. You can also transition tickets with commit messages.

However, there are times when these automated triggers fall short.

Here's where I get frustrated with Jira:

- I need to add a comment to a story for the product manager. Opening the browser to do this this breaks my concentration.
- I start work locally and don't push up a branch immediately. This doesn't trigger an automated transition.
- I don't like smart commit messages. Commit messages should reference the issue and be a concise, grepable implentation note for your fellow developers. Smart commits muck up the history.
- I start a story and realize that a refactor, usually to allow for extension, is required before work on the requirements can start. The refactor should be in it's own pull request, so I forget to create a ticket and that work goes untracked.

Paired with git, this project attempts to solve these issues.
