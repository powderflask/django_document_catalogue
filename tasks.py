from invoke import task, Collection

def docs_make(c, command):
    c.run('cd docs; make {}'.format(command))

@task
def docs_clean(c):
    """ Clean docs build """
    docs_make(c, 'clean')

@task(docs_clean)
def docs_build(c):
    """ Clean and build Sphinx docs """
    docs_make(c, 'html')

@task(docs_build)
def docs_release(c):
    """ Push docs to github, triggering webhook to build readthedocs """
    c.run('cd docs; git push')

docs = Collection('docs')
docs.add_task(docs_build, 'build')
docs.add_task(docs_clean, 'clean')
docs.add_task(docs_release, 'release')


def setup(c, command):
    c.run('python setup.py {}'.format(command))

@task
def clean(c, docs=True):
    """ Clean setup / build directories """
    setup(c, 'clean')
    if docs:
        docs_clean(c)

@task(clean)
def build(c, docs=False):
    """ Clean and build a new distribution """
    setup(c, "sdist")
    if docs:
        docs_build(c)

@task
def version(c):
    """ Print current project versions found in source file(s) """
    setup(c, 'version')

@task
def upload(c, repo='testpypi'):
    """ Upload build to given PyPi repo"""
    c.run('twine upload --repository {}} dist/*'.format(repo))

@task(help={'dist': "Name of distirbution file under dist/ directory to check."})
def check(c, dist):
    """ Twine check the given distribution """
    c.run('twine check dist/{}'.format(dist))

@task(help={'repo': "Specify:  pypi  for a production release."})
def release(c, repo='testpypi'):
    print('Building new release and upload to {}'.format(repo))
    print('Current version in source:')
    version(c)
    if input('Continue? y/N ').lower()[0] != 'y':
        print('Release aborted')
        exit(0)
    build(c)
    upload(c, repo)