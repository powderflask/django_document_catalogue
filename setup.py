import sys, os

from setuptools import setup, Command
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


setup(
    name="django-document_catalogue",
    version="0.1",
    packages=['document_catalogue', 'document_catalogue.tests'],
    license="MIT",
    include_package_data = True,
    description=("Simple, light-weight, stand-alone, hierarchical document library as a reusable django app."),
    author="powderflask",
    author_email="powderflask@gmail.com",
    maintainer="powderflask",
    maintainer_email="powderflask@gmail.com",
    url="http://pypi.python.org/pypi/django-document_catalogue/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    cmdclass={
        'clean' : CleanCommand,
    },
    test_suite="dummy",
)

