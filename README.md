
<!-- README.md is generated from README.Rmd. Please edit that file -->

# datamations

<!-- badges: start -->

[![R-CMD-check](https://github.com/jhofman/datamations/workflows/R-CMD-check/badge.svg)](https://github.com/jhofman/datamations/actions)
<!-- badges: end -->

datamations is a framework for the automatic generation of explanation
of the steps of an analysis pipeline. It automatically turns code into
animations, showing the state of the data at each step of an analysis.

## Installation

You can install datamations from GitHub with:

``` r
# install.packages("devtools")
devtools::install_github("microsoft/datamations")
```

## Usage

To get started, load datamations and dplyr:

``` r
library(datamations)
library(dplyr)
```

A datamation shows a plot of what the data looks like at each step of a
tidyverse pipeline, animated by the transitions that lead to each state.
The following shows an example taking the built-in `small_salary` data
set, grouping by `Degree`, and calculating the mean `Salary`.

First, define the code for the pipeline, then generate the datamation
with `datamation_sanddance()`:

``` r
"small_salary %>% 
  group_by(Degree) %>%
  summarize(mean = mean(Salary))" %>%
  datamation_sanddance()
```

<img src="man/figures/README-mean_salary_group_by_degree.gif" width="80%" />

## Supported functions and conventions

datamations supports the following `dplyr` functions:

-   `group_by()`
-   `summarize()`/`summarise()`
-   `filter()`
-   `count()`

and constructs one *or more* frames for each step of a pipeline. In the
example pipeline above:

``` r
small_salary %>% 
  group_by(Degree) %>%
  summarize(mean = mean(Salary))
```

there are three steps:

1.  The initial data (`small_salary`)

    An information grid is shown, laying out the number of points in the
    data set.

2.  The grouped data (grouped by `Degree`)

    The data is separated into groups, retaining the informaton grid
    structure.

3.  The summarized data (mean of `Salary`)

    The distribution of `Salary` within the groups is shown, then the
    summary function (mean) is applied. Error bars are added to the mean
    and the final frame zooms in on the data.

### `group_by()` frames

datamations supports *up to three* grouping variables, showing one frame
per variable. The placement of the variables is as follows:

-   **One variable**: On the x-axis
-   **Two variables**: The first variable in column facets, the second
    on the x-axis
-   **Three variables**: The first variable in column facets, the second
    in row facets, the third in on the x-axis

### `summarize()` frames

datamations supports summarizing *one* variable. The `summarize()`
section of a pipeline will have the following frames:

1.  Distribution of the variable to be summarized
2.  Summarized variable
3.  Summarized variable with standard error (only if summary function is
    mean)
4.  Zoomed version of summarized variable

### `count()` frames

datamations treats `count()` equivalently to `group_by()` +
`summarize(n = n())`. It supports up to three “grouping” variables.

### `filter()` frames

datamation supports `filter()` at any point in the pipeline, whether it
comes after the initial data, while the data is grouped, or after it has
been summarized.

## Finer control

If you would like to change the default conventions, or to match an
existing plot style, datamations can take ggplot2 code as input.

For example, to match this plot, which has Work on the x-axis and Degree
in row facets:

``` r
library(ggplot2)

small_salary %>%
  group_by(Work, Degree) %>%
  summarize(mean_salary = mean(Salary)) %>%
  ggplot(aes(x = Work, y = mean_salary)) + 
  geom_point() + 
  facet_grid(rows = vars(Degree))
```

<img src="man/figures/README-ggplot2-existing-plot-1.png" width="80%" />

Simply define the code and pass to `datamation_sanddance()`, which will
produce an animation with desired plot layout.

``` r
"small_salary %>%
  group_by(Work, Degree) %>%
  summarize(mean_salary = mean(Salary)) %>%
  ggplot(aes(x = Work, y = mean_salary)) + 
  geom_point() + 
  facet_grid(rows = vars(Degree))" %>%
  datamation_sanddance()
```

<img src="man/figures/README-mean_salary_group_by_degree_work_ggplot.gif" width="80%" />

When ggplot2 code is provided, the order of animation is not determined
by the order in `group_by()`, but by the plot layout. Variables are
first animated by what’s in the column facets, then the row facets, by
the x-axis, and finally by color.

Some limitations:

-   `facet_wrap()` is not supported - please use `facet_grid()`
-   datamations expects different variables in the column and row facets
    than in the x-axis. datamations generated that do not match this
    layout may look different than the final plot!
-   Only `geom_point()` is supported, e.g. specifying `geom_bar()` will
    not produce a bar in the datamation.

Known limitations:

-   Three grouping variables (incl. in count)
-   Summary can only summarize one grouping variable
