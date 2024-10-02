# Copyright (c) Microsoft Corporation
import json
from typing import Any, TextIO
from pytest import approx
from datamations import DatamationFrame
from datamations import DatamationGroupBy
from pathlib import Path

PROJECT = Path.cwd()


def compare_specs_with_file(specs: list[dict[str, Any]], specs_file: TextIO) -> None:
    for i, spec in enumerate(json.load(specs_file)):
        for key in spec:
            if key == "data":
                for j, val in enumerate(spec["data"]["values"]):
                    assert val == approx(specs[i]["data"]["values"][j])
            elif key == "layer":
                for j, encoding in enumerate(spec["layer"]):
                    for field in encoding:
                        if field == "encoding":
                            for val in encoding[field]:
                                assert (
                                    encoding[field][val] == specs[i][key][j][field][val]
                                )
                        else:
                            assert encoding[field] == specs[i][key][j][field]
            elif key == "spec":
                for item in spec[key]:
                    if item == "layer":
                        for j, encoding in enumerate(spec[key]["layer"]):
                            for field in encoding:
                                if field == "encoding":
                                    for val in encoding[field]:
                                        if val == "y":
                                            for y_key in encoding[field][val]:
                                                if y_key == "scale":
                                                    for scale_key in encoding[field][
                                                        val
                                                    ][y_key]:
                                                        if scale_key == "domain":
                                                            assert encoding[field][val][
                                                                y_key
                                                            ][scale_key] == approx(
                                                                specs[i][key][item][j][
                                                                    field
                                                                ][val][y_key][scale_key]
                                                            )
                                                        else:
                                                            assert (
                                                                encoding[field][val][
                                                                    y_key
                                                                ][scale_key]
                                                                == specs[i][key][item][
                                                                    j
                                                                ][field][val][y_key][
                                                                    scale_key
                                                                ]
                                                            )
                                                else:
                                                    assert (
                                                        encoding[field][val][y_key]
                                                        == specs[i][key][item][j][
                                                            field
                                                        ][val][y_key]
                                                    )
                                        else:
                                            assert (
                                                encoding[field][val]
                                                == specs[i][key][item][j][field][val]
                                            )
                                else:
                                    assert (
                                        encoding[field] == specs[i][key][item][j][field]
                                    )
                    elif item == "encoding":
                        for val in spec[key][item]:
                            if val == "y":
                                for y_key in spec[key][item][val]:
                                    if y_key == "scale":
                                        for scale_key in spec[key][item][val][y_key]:
                                            if scale_key == "domain":
                                                assert spec[key][item][val][y_key][
                                                    scale_key
                                                ] == approx(
                                                    specs[i][key][item][val][y_key][
                                                        scale_key
                                                    ]
                                                )
                                            else:
                                                assert (
                                                    spec[key][item][val][y_key][
                                                        scale_key
                                                    ]
                                                    == specs[i][key][item][val][y_key][
                                                        scale_key
                                                    ]
                                                )
                                    else:
                                        assert (
                                            spec[key][item][val][y_key]
                                            == specs[i][key][item][val][y_key]
                                        )
                            else:
                                assert spec[key][item][val] == specs[i][key][item][val]
                    else:
                        assert spec[key][item] == specs[i][key][item]
            elif key == "encoding":
                for item in spec[key]:
                    if item == "y":
                        for y_key in spec[key][item]:
                            if y_key == "scale":
                                for scale_key in spec[key][item][y_key]:
                                    if scale_key == "domain":
                                        assert spec[key][item][y_key][
                                            scale_key
                                        ] == approx(
                                            specs[i][key][item][y_key][scale_key]
                                        )
                                    else:
                                        assert (
                                            encoding[field][val][y_key][scale_key]
                                            == specs[i][key][item][j][field][val][
                                                y_key
                                            ][scale_key]
                                        )
                            else:
                                assert (
                                    spec[key][item][y_key] == specs[i][key][item][y_key]
                                )
                    else:
                        assert spec[key][item] == specs[i][key][item]
            else:
                assert spec[key] == specs[i][key]


def test_datamation_frame_groupby(small_salary: DatamationFrame):
    grouped = small_salary.groupby("Work")

    assert "groupby" in grouped.operations
    assert small_salary.equals(grouped.states[0])


def test_datamation_frame_specs(small_salary: DatamationFrame):
    # Mean
    # Group by Degree
    specs: list[dict[str, Any]] = small_salary.groupby("Degree").mean().specs()

    with open(PROJECT / "inst" / "specs" / "raw_spec.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Group by Work
    specs = small_salary.groupby("Work").mean().specs()

    with open(PROJECT / "inst" / "specs" / "groupby_work.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Group by Degree, Work
    specs = small_salary.groupby(["Degree", "Work"]).mean().specs()

    with open(PROJECT / "inst" / "specs" / "groupby_degree_work.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Group by Work, Degree
    specs = small_salary.groupby(["Work", "Degree"]).mean().specs()

    with open(PROJECT / "inst" / "specs" / "groupby_work_degree.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Min
    # Group by Degree Min
    specs = small_salary.groupby("Degree").min("Salary").specs()
    with open(
        PROJECT / "sandbox" / "custom_animations" / "custom-animations-min-R.json"
    ) as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Group by Degree, Work Min
    specs = small_salary.groupby(["Degree", "Work"]).min("Salary").specs()
    with open(PROJECT / "inst" / "specs" / "min_specs_two_columns.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Max
    # Group by Degree Max
    specs = small_salary.groupby("Degree").max("Salary").specs()
    with open(
        PROJECT / "sandbox" / "custom_animations" / "custom-animations-max-R.json"
    ) as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Group by Degree, Work Max
    specs = small_salary.groupby(["Degree", "Work"]).max("Salary").specs()
    with open(PROJECT / "inst" / "specs" / "max_specs_two_columns.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Sum
    # Sum of Group by Degree
    specs = small_salary.groupby("Degree").sum().specs()
    with open(PROJECT / "inst" / "specs" / "sum_specs.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Sum of Group by Degree, Work
    specs = small_salary.groupby(["Degree", "Work"]).sum().specs()
    with open(PROJECT / "inst" / "specs" / "sum_specs_two_columns.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Product
    # Product of Group by Degree
    specs = small_salary.groupby("Degree").prod().specs()
    with open(PROJECT / "inst" / "specs" / "prod_specs.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Product of Group by Degree, Work
    specs = small_salary.groupby(["Degree", "Work"]).prod().specs()
    with open(PROJECT / "inst" / "specs" / "prod_specs_two_columns.json") as specs_file:
        compare_specs_with_file(specs, specs_file)

    # Count group by Degree
    count_spec = small_salary.groupby("Degree").count("Salary").specs()
    with open(PROJECT / "inst" / "specs" / "count_specs_one_column.json") as specs_file:
        compare_specs_with_file(count_spec, specs_file)

    # Count group by Degree, Work
    count_spec = small_salary.groupby(["Degree", "Work"]).count("Salary").specs()
    with open(
        PROJECT / "inst" / "specs" / "count_specs_two_columns.json"
    ) as specs_file:
        compare_specs_with_file(count_spec, specs_file)

    # Quantile group by Degree
    quant_spec = small_salary.groupby("Degree").quantile("Salary", 0.01).specs()
    with open(
        PROJECT / "sandbox" / "custom_animations" / "custom-animations-quantile-R.json"
    ) as specs_file:
        compare_specs_with_file(quant_spec, specs_file)

    # Quantile group by Degree, Work
    quant_spec = (
        small_salary.groupby(["Degree", "Work"]).quantile("Salary", 0.01).specs()
    )
    with open(
        PROJECT / "inst" / "specs" / "quantile_specs_two_columns.json"
    ) as specs_file:
        compare_specs_with_file(quant_spec, specs_file)


def test_three_variables_frame_specs(load_penguins: DatamationFrame):
    # three-variable grouping
    with open(PROJECT / "sandbox" / "penguins_three_groups.json") as specs_file:
        specs = (
            load_penguins.groupby(["species", "island", "sex"])
            .mean("bill_length_mm")
            .specs()
        )
        compare_specs_with_file(specs, specs_file)

    # median support
    with open(PROJECT / "sandbox" / "penguins_median_specs.json") as specs_file:
        specs = (
            load_penguins.groupby(["species", "island", "sex"])
            .median("bill_depth_mm")
            .specs()
        )
        compare_specs_with_file(specs, specs_file)


def test_datamation_frame_datamation_sanddance(small_salary: DatamationFrame):
    datamation = small_salary.groupby("Work").mean().datamation_sanddance()

    assert len(datamation.states) == 2
    assert len(datamation.operations) == 2

    assert small_salary.equals(datamation.states[0])
    assert isinstance(datamation.states[1], DatamationGroupBy)

    assert datamation.operations[0] == "groupby"
    assert datamation.operations[1] == "mean"

    assert isinstance(datamation.output, DatamationFrame)

    assert datamation.output.Salary.Academia == 85.01222196154829
    assert datamation.output.Salary.Industry == 91.48376118136609

    assert "Salary" in str(datamation)
