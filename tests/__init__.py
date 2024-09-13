import json
from typing import Any

from plot_serializer.serializer import Serializer

_TEST_EPSILON = 0.0001


def _read_plot(reference_file_name: str) -> str:
    with open(f"tests/plots/{reference_file_name}.json", "r", encoding="utf-8") as file:
        return file.read()


def _assert_equal(location: str, expected: Any, actual: Any) -> None:
    if isinstance(expected, (int, float)):
        assert isinstance(
            actual, (int, float)
        ), f"Mismatching types at: {location} (expected number, got {type(actual)})"

        assert (
            expected + _TEST_EPSILON > actual
        ), f"Mismatching number at: {location} (expected {expected}, got {actual})"

        assert (
            expected < actual + _TEST_EPSILON
        ), f"Mismatching number at: {location} (expected {expected}, got {actual})"

    elif isinstance(expected, list):
        assert isinstance(actual, list), f"Mismatching types at: {location} (expected list, got {type(actual)})"

        assert len(expected) == len(
            actual
        ), f"Mismatching list length at: {location} (expected length {len(expected)}, {len(actual)})"

        for i, (expected_element, actual_element) in enumerate(zip(expected, actual)):
            _assert_equal(f"{location}[{i}]", expected_element, actual_element)

    elif isinstance(expected, dict):
        assert isinstance(actual, dict), f"Mismatching types at: {location} (expected object, got {type(actual)})"

        # Check if all keys are there
        for key in expected.keys():
            assert isinstance(key, str)  # JSON only supports string keys in objects

            assert key in actual, f"Missing key {key} in object at: {location}"

            _assert_equal(f"{location}.{key}", expected[key], actual[key])

        # Check if there are any keys that shouldn't be there
        for key in actual.keys():
            assert isinstance(key, str)  # JSON only supports string keys in objects

            assert key in expected, f"Additional key {key} found in object at: {location}"

    else:
        assert expected == actual, (
            f"Mismatching values at: {location} (expected {expected} "
            + f"[{type(expected) if expected is not None else ''}],"
            + f" got {actual} [{type(actual) if actual is not None else ''}])"
        )


def validate_output(serializer: Serializer, reference_file_name: str) -> None:
    expected = json.loads(_read_plot(reference_file_name))
    actual = json.loads(serializer.to_json())

    _assert_equal("", expected, actual)
