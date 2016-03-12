=================================
Accountable - a Jira CLI
=================================
.. image:: https://travis-ci.org/wohlgejm/accountable.svg?branch=master
    :target: https://travis-ci.org/wohlgejm/accountable
.. image:: https://coveralls.io/repos/github/wohlgejm/accountable/badge.svg?branch=master
    :target: https://coveralls.io/github/wohlgejm/accountable?branch=master

Never leave the command line to update a ticket again!

Getting started
===============
Installtion:

``pip install accountable``

Once installed, configure your account:

``accountable configure``

List all projects:

``accountable projects``

List all issue types:

``accountable issuetypes``

List issue types for an individual project:

``accountable issuetypes AC``

List metadata for an individual issue:

``accountable issue DEV-101``


Using with Githooks
===================


Using worklogs with pomodoros
=============================


Why?
====
Jira already supports robust triggers, like changing a ticket's status
based on a pull request, or a branch being created. You can also transition tickets with commit messages.

However, there are times when these automated triggers aren't enough.

Often, you'll start work locally, and forget to put the ticket in progress. Or you'll forget to add a transition to a commit message. Multiple actions listed in your commit message also aren't relevant to the project's history.
