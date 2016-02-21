=================================
Accountable - a Jira CLI (Alpha)
=================================
.. image:: https://travis-ci.org/wohlgejm/accountable.svg?branch=master
    :target: https://travis-ci.org/wohlgejm/accountable
.. image:: https://coveralls.io/repos/github/wohlgejm/accountable/badge.svg?branch=master 
    :target: https://coveralls.io/github/wohlgejm/accountable?branch=master

Never leave the command line to update a ticket again!

Getting started
===============
To install:

``pip install accountable``

Once installed, configure your account:

``accountable configure``

List all projects:

``accountable projects``

List all issue types:

``accountable issuetypes``

List issue types for an individual project:

``accountable issuetypes AC``


Why?
====
Jira already supports robus triggers, like changing a ticket's status
based on a pull request, or branch created. However, there are times
when these automated triggers aren't enough.

Often, you'll start work locally, and forget to put the ticket in progress.
