from invoke import task


@task
def test(c, test='test'):
    c.run(f'python -m pytest -v {test}')


@task
def docs(c):
    c.run('sphinx-build -b html docs docs/_build')


@task
def build(c):
    c.run('python setup.py sdist bdist_wheel')


@task
def upload(c):
    c.run('python -m twine upload --repository pypi dist/*')
