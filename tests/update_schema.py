from typing import Any

from plot_serializer.serializer import write_schema_json


def test_update_schema(request: Any) -> None:
    update_tests = request.config.getoption("--update-tests")
    if update_tests == "confirm":
        write_schema_json("./doc/static/specification/new_schema.json")
