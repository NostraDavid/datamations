from pathlib import Path
import pytest
import pandas as pd
from datamations import datamation_frame

HERE = Path(__file__).parent


@pytest.fixture
def load_penguins() -> datamation_frame.DatamationFrame:
    with (HERE / "data" / "penguins.csv").open() as f:
        df = pd.read_csv(f)
        return datamation_frame.DatamationFrame(df)


@pytest.fixture
def small_salary() -> datamation_frame.DatamationFrame:
    with (HERE / "data" / "small_salary.csv").open() as f:
        df = pd.read_csv(f)
        return datamation_frame.DatamationFrame(df)
