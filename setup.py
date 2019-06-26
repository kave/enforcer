import os
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'python-dotenv>=0.7.1,<0.11.0',
    'boto3==1.9.176',
    'pyperclip==1.7.0',
    'click==7.0',
    'colorama==0.4.1',
    'tabulate==0.8.3',
    'ruamel.yaml==0.15.97'
]

TEST_REQUIRES = [
    'flake8>=3.5,<3.8',
    'mock>=2.0,<3.1',
    'moto==1.3.8',
    'pytest>=3.4,<4.7',
    'pytest-cov>=2.5.1,<2.8.0',
    'tox>=2.9.1,<3.14.0',
    'yapf>=0.21,<0.28',
    'bandit==1.6.1',
]

try:
    import pypandoc

    DESCRIPTION = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    DESCRIPTION = "AWS SSM Parameter Store Management CLI"

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as version_file:
    version = version_file.read().strip()

DEPENDENCY_LINKS = []

setup(
    name='enforcer-reloaded',
    version=version,
    url='https://github.com/kave/enforcer',
    license='Apache 2.0',
    author="Emmanuel Apau",
    description='AWS SSM Parameter Store Management CLI',
    long_description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    test_requires=TEST_REQUIRES,
    extras_require={'dev': TEST_REQUIRES},
    dependency_links=DEPENDENCY_LINKS,
    classifiers=[],
    scripts=['bin/reloaded'])
