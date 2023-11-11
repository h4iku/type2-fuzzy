# Interval Type-2 Fuzzy Logic Stuff 
[![Tests](https://github.com/h4iku/type2-fuzzy/actions/workflows/tests.yml/badge.svg)](https://github.com/h4iku/type2-fuzzy/actions/workflows/tests.yml)

This repo has python implementation for some Interval Type 2 Fuzzy Set (IT2 FS) concepts. Each module contains a `main` function that shows the usage of that module.

## Enhanced Interval Approach (EIA)

The `eia` package contains the implementation of the [enhanced interval approach](https://ieeexplore.ieee.org/abstract/document/6086759) for encoding words into interval type-2 fuzzy sets. It both contains the "Data Part" and the "Fuzzy Set Part":

* `eia/data_part.py`: This is the Data Part module which does the interval preprocessing. It can read word intervals from an Excel file (`sample-data.xlsx` also provided) and will write results to `words.json` file. You can also extend it and use whatever input/output type you want.
* `eia/fuzzy_set_part.py`: This is the Fuzzy Set Part which will generate FOUs from the word intervals of the previous phase. FOUs are stored to `words_status.json` file. They contain "Shape (interior, left/right-shoulder)", "Embedded Interval Type-1s" and "Type-2 Membership values" for each word. The membership values are saved in a 9-point shape like this:

<p align="center">
<img src="https://cloud.githubusercontent.com/assets/3812788/21205088/a242af88-c26f-11e6-9fb9-fc04216e334a.png" width="450" />
</p>

## Utilities

The `utils` package contains some other tools and measures for IT2 FSs:

* `utils/centroid_it2fs.py`:
  * `centroid_it2`: Computes the centroid of an IT2 FS. Returns centroid boundaries and the center of centroid.
  * `ekm`: Implementation of the Enhanced KM algorithm.
* `linguistic_weighted_average.py`:
  * `fwa`: Computing the Fuzzy Weighted Average for trapezoidal T1 FSs.
  * `lwa`: Computing the Linguistic Weighted Average for IT2 FSs.
* `ranking_methods.py`:
  * `centroid_rank`: Implementation of the center-of-centroid based ranking method.
* `similarity_measures.py`:
  * `jaccard`: computing the Jaccard similarity measure between two IT2 FSs.
