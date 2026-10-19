from pathlib import Path

import numpy as np
import pytest

import jutuldarcy as jd

pytestmark = pytest.mark.integration
DECK = Path(__file__).parent / "data" / "tiny.DATA"


def test_data_file_and_parsed_deck():
    parsed = jd.parse_data_file(DECK)
    case = jd.setup_case_from_data_file(parsed)
    assert jd.number_of_cells(jd.reservoir_domain(case)) == 3
    output = jd.simulate_data_file(DECK, convert=True, info_level=-1)
    np.testing.assert_allclose(output["DAYS"], [1.0, 2.0])
    assert set(output["WELLS"]) == {"I", "P"}
    assert np.isfinite(output["STATES"][-1]["Pressure"]).all()
