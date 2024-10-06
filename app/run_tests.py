import pytest
import sys

def run_tests():
    # Esto ejecuta pytest en la carpeta `tests`
    exit_code = pytest.main(['tests'])
    sys.exit(exit_code)

if __name__ == "__main__":
    run_tests()
