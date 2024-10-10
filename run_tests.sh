PYTHONPATH=app coverage run -m pytest -v --disable-warnings|| true
PYTHONPATH=app coverage report -m