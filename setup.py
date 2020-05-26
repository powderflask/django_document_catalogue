import sys, os, re

from setuptools import setup, Command, find_packages
from setuptools.command.test import test

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./*.pyc ./*.egg-info')


def run_tests(*args):
    from document_catalogue.tests import run_tests
    errors = run_tests()
    if errors:
        sys.exit(1)
    else:
        sys.exit(0)

test.run_tests = run_tests

NAME = "django-document-catalogue"

# get version without importing
with open("document_catalogue/__init__.py", "rb") as f:
    VERSION = str(re.search('__version__ = "(.+?)"', f.read().decode()).group(1))

with open("docs/.readthedocs.yml", "rb") as f:
    DOCS_VERSION = str(re.search('version: (.+)', f.read().decode()).group(1))


class VersionCommand(Command):
    description = 'print version numbers, from various places they exist in project'
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        print('Package {name} Version: {version}'.format(name=NAME, version=VERSION))
        print('Docs version: {version}'.format(version=DOCS_VERSION))

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(include=['document_catalogue', 'document_catalogue.*']),
    python_requires='>=3.5, <4',
    install_requires = [
        'Django>=2.2,<3.0',
        'django-mptt>=0.10.0',
        'django-private-storage>=2.2',
        'django-admin-sortable2',
        'django-constrainedfilefield>=3.2.0',
        'python-magic>=0.4.15',
        'setuptools-git',    # apparently needed to handle include_package_data from git repo?
    ],
    license="MIT",
    include_package_data = True,
    description=("Simple, light-weight, stand-alone, hierarchical document library as a reusable django app."),
    long_description=open("README.rst").read(),
    long_description_content_type="text/x-rst",
    author="powderflask",
    author_email="powderflask@gmail.com",
    maintainer="powderflask",
    maintainer_email="powderflask@gmail.com",
    url="https://github.com/powderflask/django_document_catalogue",
    download_url="https://github.com/powderflask/django_document_catalogue/archive/v{}.tar.gz".format(VERSION),
    project_urls={
        'ReadTheDocs'  : 'https://django-document-catalogue.readthedocs.io',
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    cmdclass={
        'clean' : CleanCommand,
        'version': VersionCommand,
    },
    test_suite="dummy",
)

