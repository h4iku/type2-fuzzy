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

    for (word1, status1), (word2, status2) in zip(
        output_status.items(), expected_status.items()
    ):
        assert status1["shape"] == status2["shape"]
        assert [*status1["MF"][0], *status1["MF"][1]] == pytest.approx(
            [*status2["MF"][0], *status2["MF"][1]]
        )
