import itertools

import numpy as np

lower_bound = 0
upper_bound = 10


def bad_data_processing(interval):
    """Checking bad data intervals"""

    left = interval[0]
    right = interval[1]

    if lower_bound <= left < right <= upper_bound and (right - left) < upper_bound:
        return True
    else:
        return False


def outlier_processing(intervals):
    """Outlier processing"""

    if not intervals:
        return []

    left = [x[0] for x in intervals]
    right = [x[1] for x in intervals]

    # Compute Q(0.25), Q(0.75) and IQR for left-ends
    lq25, lq75 = np.percentile(left, [25, 75])
    liqr = lq75 - lq25

    # Compute Q(0.25), Q(0.75) and IQR for right-ends
    rq25, rq75 = np.percentile(right, [25, 75])
    riqr = rq75 - rq25

    # Outlier processing for Left and Right bounds
    left_filtered = [
        x for x in intervals if (lq25 - 1.5 * liqr) <= x[0] <= (lq75 + 1.5 * liqr)
    ]
    right_filtered = [
        x for x in left_filtered if (rq25 - 1.5 * riqr) <= x[1] <= (rq75 + 1.5 * riqr)
    ]

    # Compute Q(0.25), Q(0.75) and IQR for interval length
    len_values = [x[1] - x[0] for x in right_filtered]
    lenq25, lenq75 = np.percentile(len_values, [25, 75])
    leniqr = lenq75 - lenq25

    # Outlier processing for interval length
    len_filtered = [
        x if (lenq25 - 1.5 * leniqr) <= x <= (lenq75 + 1.5 * leniqr) else None
        for x in len_values
    ]
    selectors = [x is not None for x in len_filtered]
    filtered_intervals = list(itertools.compress(right_filtered, selectors))
    return filtered_intervals


def tolerance_limit_processing(intervals):
    """Tolerance limit processing"""

    if not intervals:
        return []

    left = [x[0] for x in intervals]
    right = [x[1] for x in intervals]
    mean_left = np.mean(left)
    std_left = np.std(left, ddof=1)
    mean_right = np.mean(right)
    std_right = np.std(right, ddof=1)

    limits = [
        32.019,
        32.019,
        8.380,
        5.369,
        4.275,
        3.712,
        3.369,
        3.136,
        2.967,
        2.839,
        2.737,
        2.655,
        2.587,
        2.529,
        2.48,
        2.437,
        2.4,
        2.366,
        2.337,
        2.31,
        2.31,
        2.31,
        2.31,
        2.31,
        2.208,
    ]
    k = limits[min(len(left), len(limits)) - 1]

    # Tolerance limit processing for Left and Right bounds
    left_filtered = [
        x
        for x in intervals
        if (mean_left - k * std_left) <= x[0] <= (mean_left + k * std_left)
    ]
    right_filtered = [
        x
        for x in left_filtered
        if (mean_right - k * std_right) <= x[1] <= (mean_right + k * std_right)
    ]

    # Tolerance limit processing for interval length
    len_values = [x[1] - x[0] for x in right_filtered]
    mean_len = np.mean(len_values)
    std_len = np.std(len_values, ddof=1)

    if std_len != 0:
        k = min(k, mean_len / std_len, (100 - mean_len) / std_len)

    len_filtered = [
        x if (mean_len - k * std_len) <= x <= (mean_len + k * std_len) else None
        for x in len_values
    ]
    selectors = [x is not None for x in len_filtered]
    filtered_intervals = list(itertools.compress(right_filtered, selectors))
    return filtered_intervals


def reasonable_interval_processing(intervals):
    """Reasonable interval processing"""

    if not intervals:
        return []

    left = [x[0] for x in intervals]
    right = [x[1] for x in intervals]
    mean_left = np.mean(left)
    std_left = np.std(left, ddof=1)
    mean_right = np.mean(right)
    std_right = np.std(right, ddof=1)

    # Determining sigma*
    if std_left == std_right:
        sigma_star = (mean_left + mean_right) / 2
    elif std_left == 0:
        sigma_star = mean_left + 0.01
    elif std_right == 0:
        sigma_star = mean_right - 0.01
    else:
        sigma1 = (
            mean_right * std_left**2
            - mean_left * std_right**2
            + std_left
            * std_right
            * np.sqrt(
                (mean_left - mean_right) ** 2
                + 2 * (std_left**2 - std_right**2) * np.log(std_left / std_right)
            )
        ) / (std_left**2 - std_right**2)

        sigma2 = (
            mean_right * std_left**2
            - mean_left * std_right**2
            - std_left
            * std_right
            * np.sqrt(
                (mean_left - mean_right) ** 2
                + 2 * (std_left**2 - std_right**2) * np.log(std_left / std_right)
            )
        ) / (std_left**2 - std_right**2)

        if mean_left <= sigma1 <= mean_right:
            sigma_star = sigma1
        else:
            sigma_star = sigma2

    # Checking reasonable intervals
    reasonable_intervals = [
        x
        for x in intervals
        if 2 * mean_left - sigma_star
        <= x[0]
        < sigma_star
        < x[1]
        <= 2 * mean_right - sigma_star
    ]
    return reasonable_intervals


def process_data_part(excel_workbook):
    import json

    from openpyxl import load_workbook

    # Open Excel file and get the active sheet
    wb = load_workbook(excel_workbook)
    ws = wb.active

    # A dictionary to keep the intervals of each word
    words = {
        word.value: zip(
            [l.value for l in lower if l.value is not None],
            [u.value for u in upper if u.value is not None],
        )
        for (word, *lower), (_, *upper) in zip(*[ws.columns] * 2)
    }

    # Data Part
    for w, intervals in words.items():
        words[w] = [x for x in intervals if bad_data_processing(x)]
    for w, intervals in words.items():
        words[w] = outlier_processing(intervals)
    for w, intervals in words.items():
        words[w] = tolerance_limit_processing(intervals)
    for w, intervals in words.items():
        words[w] = reasonable_interval_processing(intervals)

    # Serializing words dictionary as a json file
    with open("words.json", "w") as file:
        json.dump(words, file)

    return words


def main():
    process_data_part("sample-data.xlsx")


if __name__ == "__main__":
    main()
