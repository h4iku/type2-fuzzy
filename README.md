# Interval Type-2 Fuzzy Logic Stuff
This repo has python implementation for some Interval Type 2 Fuzzy Set (IT2 FS) concepts. Each module contains `main` function which shows the usage of that module.
#### Requirements:
* python 3.4+
* numpy
* openpyxl (only if you want to read data from an Excel file like the sample-data provided)

## Enhanced Interval Approach (EIA)
The `eia` package contains the implementation of the enhanced interval approach for encoding words into interval type-2 fuzzy sets. It both contains the "Data Part" and the "Fuzzy Set Part":
* `eia/eia_data_part.py`: This is the Data Part module which does the interval preprocessing. It can read word intervals from an excel file (`sample-data.xlsx` also provided) and will write results to `words.pickle` file. You can also extend it and use whatever input/output type you want.
* `eia/eia_fuzzy_set_part.py`: This is the Fuzzy Set Part which will generate FOUs from the word intervals of the previous phase. FOUs are stored to `words_status.pickle` file. They contain "Shape (interior, lef/right-shoulder)", "Embedded Interval Type-1s" and "Type-2 Membership values" for each word. The membership values are saved in a 9-point shape like this:

<p align="center">
<img src="https://cloud.githubusercontent.com/assets/3812788/21205088/a242af88-c26f-11e6-9fb9-fc04216e334a.png" width="450" />
</p>

## Utilities
The `utils` package contains some other tools and measures for IT2 FSs:
* `utils/centroid_it2fs.py`:
  - `centroid_it2`: Computes the centroid of an IT2 FS. Returns centroid boundaries and and center of centroid.
  - `ekm`: Implementation of the Enhanced KM algorithm.
* `linguistic_weighted_average.py`:
  - `fwa`: Computing the Fuzzy Weighted Average for trapezoidal T1 FSs.
  - `lwa`: Computing the Linguistic Weighted Average for IT2 FSs.
* `ranking_methods.py`:
  - `centroid_rank`: Implement the center-of-centroid based ranking method.
* `similarity_measures.py`:
  - `jaccard`: computing the Jaccard similarity measure between two IT2 FSs.

