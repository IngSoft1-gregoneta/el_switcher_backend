PYTHONPATH=app pytest -s app/tests --disable-warnings ||
PYTHONPATH=app coverage run -m pytest -v --disable-warnings||
PYTHONPATH=app coverage report -m