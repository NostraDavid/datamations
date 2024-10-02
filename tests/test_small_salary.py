# Copyright (c) Microsoft Corporation
from pytest import CaptureFixture
from datamations import DatamationFrame


def test_small_salary(capsys: CaptureFixture, small_salary: DatamationFrame):
    print(small_salary.groupby("Work").mean())

    out, _ = capsys.readouterr()

    assert "Work" in out
    assert "Salary" in out
    assert "Academia" in out
    assert "Industry" in out
    assert "85.012222" in out
    assert "91.483761" in out
