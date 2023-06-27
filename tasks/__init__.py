from invoke import task, Collection
from . import docs, pypi


@task
def clean(c):
    """ Clean up the project root directory """
    c.run('rm -vrf ./*.pyc ./*.egg-info')  # FIXME: Command fails in Windows


namespace = Collection(docs, pypi)
namespace.add_task(clean)
