#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pandas', 'pandas_schema', 'pyyaml', 'pathlib']

test_requirements = []

setup(
    author="Pär Larsson",
    author_email='par.g.larsson@regionvasterbotten.se',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Package for pandas dataframe validation based on a separate dict template",
    entry_points={
        'console_scripts': [
            'validate_meta=validate_meta.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='validate_meta',
    name='validate_meta',
    packages=find_packages(include=['validate_meta', 'validate_meta.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gmc-norr/meta_validate',
    version='0.1.2',
    zip_safe=False,
)
