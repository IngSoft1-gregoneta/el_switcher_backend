PYTHONPATH=app coverage run --rcfile=.coveragerc -m pytest --disable-warnings|| true
PYTHONPATH=app coverage report -m