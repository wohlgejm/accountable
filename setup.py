from setuptools import setup, find_packages

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='accountable',
    version='0.1',
    description='Command line tools for interacting with JIRA',
    long_description=long_description,
    url='https://github.com/wohlgejm/accountable',
    author='Jerry Wohlgemuth',
    author_email='wohlgejm@gmail.com',
    license='MIT',
    keywords='jira',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['click', 'requests', 'pyaml', 'gitpython',
                      'python-slugify'],
    entry_points='''
        [console_scripts]
        accountable=accountable.cli:cli
    ''',
)
