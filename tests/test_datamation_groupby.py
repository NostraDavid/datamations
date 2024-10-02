# Copyright (c) Microsoft Corporation
from pytest import approx
from datamations import DatamationFrame


def test_datamation_groupby(small_salary: DatamationFrame):
    # Group by Degree
    mean = small_salary.groupby("Degree").mean()

    assert "groupby" in mean.operations
    assert "mean" in mean.operations

    assert len(mean.states) == 2
    assert small_salary.equals(mean.states[0])

    assert mean.Salary.Masters == 90.22633400617633
    assert mean.Salary.PhD == 88.24560612632195

    # median
    median = small_salary.groupby("Degree").median()

    assert "groupby" in median.operations
    assert "median" in median.operations

    assert len(median.states) == 2
    assert small_salary.equals(median.states[0])

    assert median.Salary.Masters == 91.13211765489541
    assert median.Salary.PhD == 86.40630845562555

    # sum
    sum = small_salary.groupby("Degree").sum()

    assert "groupby" in sum.operations
    assert "sum" in sum.operations

    assert len(sum.states) == 2
    assert small_salary.equals(sum.states[0])

    assert sum.Salary.Masters == 6496.296048444696
    assert sum.Salary.PhD == 2470.8769715370145

    # product
    product = small_salary.groupby("Degree").prod()

    assert "groupby" in product.operations
    assert "product" in product.operations

    assert len(product.states) == 2
    assert small_salary.equals(product.states[0])

    assert product.Salary.PhD == 2.9426590692781414e54
    assert product.Salary.Masters == 5.892246828184284e140

    # Group by Work
    mean = small_salary.groupby("Work").mean()

    assert "groupby" in mean.operations
    assert "mean" in mean.operations

    assert len(mean.states) == 2
    assert small_salary.equals(mean.states[0])

    assert mean.Salary.Academia == 85.01222196154829
    assert mean.Salary.Industry == 91.48376118136609


def test_datamation_groupby_multiple(
    small_salary: DatamationFrame,
    load_penguins: DatamationFrame,
):
    # Group by Degree, Work
    mean = small_salary.groupby(["Degree", "Work"]).mean()

    assert "groupby" in mean.operations
    assert "mean" in mean.operations

    assert len(mean.states) == 2
    assert small_salary.equals(mean.states[0])

    assert mean.Salary.Masters.Academia == 84.0298831968801
    assert mean.Salary.Masters.Industry == 91.22576155606282
    assert mean.Salary.PhD.Academia == 85.55796571969728
    assert mean.Salary.PhD.Industry == 93.08335885824636

    # sum
    sum = small_salary.groupby(["Degree", "Work"]).sum()

    assert "groupby" in sum.operations
    assert "sum" in sum.operations

    assert len(sum.states) == 2
    assert small_salary.equals(sum.states[0])

    assert sum.Salary.Masters.Academia == 840.2988319688011
    assert sum.Salary.Masters.Industry == 5655.997216475895
    assert sum.Salary.PhD.Academia == 1540.043382954551
    assert sum.Salary.PhD.Industry == 930.8335885824636

    # product
    product = small_salary.groupby(["Degree", "Work"]).prod()

    assert "groupby" in product.operations
    assert "product" in product.operations

    assert len(product.states) == 2
    assert small_salary.equals(product.states[0])

    assert product.Salary.Masters.Academia == 1.753532557780977e19
    assert product.Salary.Masters.Industry == 3.3602152421057308e121
    assert product.Salary.PhD.Academia == 6.027761935702164e34
    assert product.Salary.PhD.Industry == 4.8818435443657834e19

    # Group by species, island, sex
    mean = load_penguins.groupby(["species", "island", "sex"]).mean()

    assert "groupby" in mean.operations
    assert "mean" in mean.operations

    assert len(mean.states) == 2
    assert load_penguins.equals(mean.states[0])

    assert mean.bill_length_mm.Adelie.Biscoe.male == approx(40.5909090909091)
    assert mean.bill_length_mm.Adelie.Biscoe.female == approx(37.35909090909092)
