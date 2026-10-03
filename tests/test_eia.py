import json
from pathlib import Path

import pytest

from eia.data_part import process_data_part
from eia.fuzzy_set_part import process_fuzzy_set_part

tests_dir = Path(__file__).parent
fixtures_dir = tests_dir / "fixtures"


# TODO: Break this into data_part and fs_part later.
def test_eia():
    # define the input and expected dictionaries
    with open(fixtures_dir / "words.json") as file:
        expected_intervals = json.load(file)
    output_intervals = process_data_part(tests_dir.parent / "sample-data.xlsx")
    output_intervals = json.loads(json.dumps(output_intervals))
    assert output_intervals == expected_intervals

    with open(fixtures_dir / "words_status.json") as file:
        expected_status = json.load(file)
    output_status = process_fuzzy_set_part()

    assert output_status.keys() == expected_status.keys()

    for word, status in expected_status.items():
        output = output_status[word]
        assert output["shape"] == status["shape"]
        assert [*output["MF"][0], *output["MF"][1]] == pytest.approx(
            [*status["MF"][0], *status["MF"][1]]
        )
