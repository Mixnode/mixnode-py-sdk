import os
import re
import sys

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

version = ''
with open('mixnode/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

packages = [
    'mixnode',
]

requires = [
    'requests'
]

tests_requires = [
    'nose',
    'mock',
    'Faker',
]

setup(
    name='Mixnode',
    description='Mixnode Python Library',
    author='Mixnode, Inc.',
    url='https://github.com/Mixnode/mixnode-py-sdk',
    download_url='https://github.com/Mixnode/mixnode-py-sdk',
    version=version,
    package_dir={' mixnode': 'mixnode'},
    packages=packages,
    install_requires=requires,
    tests_require=tests_requires,
    classifiers=[
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description=readme,
    package_data={'': ['LICENSE', 'README.rst']},
    include_package_data=True,
)
