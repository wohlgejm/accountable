from setuptools import setup, find_packages

setup(
    name='accountable',
    version='0.1',
    description='Command line tools for interacting with JIRA',
    url='https://github.com/wohlgejm/accountable',
    author='Jerry Wohlgemuth',
    author_email='wohlgejm@gmail.com',
    license='MIT',
    keywords='jira',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['click', 'requests', 'pyaml'],
    entry_points='''
        [console_scripts]
        accountable=accountable.cli:cli
    ''',
)
