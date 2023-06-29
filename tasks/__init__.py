import platform

from invoke import task, Collection
from . import docs, pypi


@task
def clean(c):
    """ Clean up the project root directory """
    if platform.system() == 'Windows':  # FIXME: Remove code for Windows
        c.run('PowerShell "Remove-Item -Verbose -Recurse -Force ./*.pyc, ./*.egg-info, ./*.pytest_cache, ./*.tox"')
    else:
        c.run('rm -vrf ./*.pyc ./*.egg-info ./*.pytest_cache ./*.tox')


namespace = Collection(docs, pypi)
namespace.add_task(clean)
