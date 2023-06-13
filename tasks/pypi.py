import re
from invoke import task
from . import docs as docs_task


@task
def clean(c, docs=True):
    """ Clean setup / build directories """
    c.run('invoke clean')
    if docs:
        docs_task.clean(c)


@task(clean)
def build(c, docs=False):
    """ Clean and build a new distribution """
    c.run('python -m build')
    if docs:
        docs_task.build(c)


def get_versions():
    """ Grab version numbers from various places they are explicitly defined and return dictionary """
    from document_catalogue import __version__  # FIXME: ModuleNotFoundError importing from document_catalogue

    with open("docs/.readthedocs.yml", "rb") as f:
        docs_version = str(re.search('version: (.+)', f.read().decode()).group(1))

    return {
        'Package version': __version__,
        'Docs version': docs_version,
    }


@task
def version(c):
    """ Print current project versions found in source file(s) """
    for k, v in get_versions().items():
        print('{label}: {version}'.format(label=k, version=v))


@task
def upload(c, repo='testpypi'):
    """ Upload build to given PyPI repo"""
    c.run('twine upload --repository {} dist/*'.format(repo))


@task(help={'dist': "Name of distribution file under dist/ directory to check."})
def check(c, dist):
    """ Twine check the given distribution """
    c.run('twine check dist/{}'.format(dist))


@task(help={'repo': "Specify:  pypi  for a production release."})
def release(c, repo='testpypi'):
    """ Build release and upload to PyPI """
    print('Building new release and uploading to {}'.format(repo))
    print('Current version in source:')
    version(c)
    if input('Continue? (y/n): ').lower()[0] != 'y':
        print('Release aborted')
        exit(0)
    build(c)
    upload(c, repo)
