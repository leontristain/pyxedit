from invoke import task


@task
def build_docs(c):
    c.run('sphinx-build -b html docs docs/_build')
