# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

setup(
    name='sample',
    version='0.1',
    description='Command line tools for interacting with JIRA',
    url='https://github.com/wohlgejm/accountable',
    author_email='wohlgejm@gmail.com',
    license='MIT',
    keywords='jira',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[''],
    entry_points='''
        [console_scripts]
        accountable=accountable.cli:cli
    ''',
)
