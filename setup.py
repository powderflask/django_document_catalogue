import sys, os

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


setup(
    name="django-document_catalogue",
    version="0.1.0",
    packages=find_packages(include=['document_catalogue', 'document_catalogue.*']),
    python_requires='>=3',
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
        'Programming Language :: Python :: 3',
        'Framework :: Django',
    ],
    cmdclass={
        'clean' : CleanCommand,
    },
    test_suite="dummy",
)

