# Datamation

## Installation

You can install datamations from this folder with:

```bash
pip install -e ../
```

## Usage

[datamation_sanddance()](https://github.com/microsoft/datamations/blob/main/datamations/datamation_frame.py#L380)
is the main function that a user will call to generate a datamation.

```python
from datamations import DatamationFrame

df = DatamationFrame(small_salary().df)

df.groupby('Degree').mean().datamation_sanddance()
```

![mean salary group by degree]("../../man/figures/README-mean_salary_group_by_degree.gif")

You can group by multiple variables, as in this example, grouping by
`Degree` and `Work` before calculating the mean `Salary`:

```python
df.groupby(['Degree', 'Work']).mean().datamation_sanddance()
```

![mean salary group by degree and work]("../../../../man/figures/README-mean_salary_group_by_degree_work.gif")
