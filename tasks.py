from invoke import task


@task
def test(c, test='test'):
    c.run(f'python -m pytest -v {test}')


@task
def docs(c):
    c.run('sphinx-build -b html docs docs/_build')
