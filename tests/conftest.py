from typing import Any


def pytest_addoption(parser: Any) -> None:
    parser.addoption("--update-tests", action="store", default="default", help="Reset the tests comparison files")
