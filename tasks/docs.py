from invoke import task


def make(c, command):
    c.run('cd docs; make {}'.format(command))


@task
def clean(c):
    """ Clean docs build """
    make(c, 'clean')


@task(clean)
def build(c):
    """ Clean and build Sphinx docs """
    make(c, 'html')


@task(build)
def release(c):
    """ Push docs to GitHub, triggering webhook to build Read The Docs """
    c.run('git push')
