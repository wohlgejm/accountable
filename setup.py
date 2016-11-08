from setuptools import setup, find_packages
from pip.req import parse_requirements


with open('README.rst') as f:
    long_description = f.read()

install_reqs = parse_requirements('requirements.txt', session=False)
reqs = [str(ir.req) for ir in install_reqs]

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
    install_requires=reqs,
    entry_points='''
        [console_scripts]
        accountable=accountable.cli:cli
    ''',
)
