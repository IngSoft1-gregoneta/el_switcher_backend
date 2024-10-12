PYTHONPATH=app coverage run --rcfile=.coveragerc -m pytest -v --disable-warnings|| true
PYTHONPATH=app coverage report -m