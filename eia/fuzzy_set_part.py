import numpy as np

lower_bound = 0
upper_bound = 10


def fuzzy_part(intervals):
    """Doing the fuzzy set part for each word"""

    # Keeping the words specification
    word_status = {}

    # Admissible region determination
    t_dist_table = [
        6.314,
        2.920,
        2.353,
        2.132,
        2.015,
        1.943,
        1.895,
        1.860,
        1.833,
        1.812,
        1.796,
        1.782,
        1.771,
        1.761,
        1.753,
        1.746,
        1.740,
        1.734,
        1.729,
        1.725,
        1.721,
        1.717,
        1.714,
        1.711,
        1.708,
        1.706,
        1.703,
        1.701,
        1.699,
        1.697,
        1.684,
    ]  # alpha = 0.05

    t_alpha = t_dist_table[min(len(intervals), len(t_dist_table)) - 1]

    mean_left = np.mean([x[0] for x in intervals])
    mean_right = np.mean([x[1] for x in intervals])

    c = [x[1] - 5.831 * x[0] for x in intervals]
    d = [x[1] - 0.171 * x[0] - 8.29 for x in intervals]
    shift1 = t_alpha * np.std(c, ddof=1) / np.sqrt(len(intervals))
    shift2 = t_alpha * np.std(d, ddof=1) / np.sqrt(len(intervals))

    # Establish the nature of FOUs
    if (
        mean_right > 5.831 * mean_left - shift1
        and mean_right < 0.171 * mean_left + 8.29 - shift2
    ):
        # left shoulder embedded T1 FS
        et1fs_left = [
            0.5 * (x[0] + x[1]) - (x[1] - x[0]) / np.sqrt(6) for x in intervals
        ]
        et1fs_right = [
            0.5 * (x[0] + x[1]) + np.sqrt(6) * (x[1] - x[0]) / 3 for x in intervals
        ]

        # Delete inadmissible embedded T1 FSs
        admissibles = [
            (x, y)
            for (x, y) in zip(et1fs_left, et1fs_right)
            if x >= lower_bound and y <= upper_bound
        ]

        fsl = np.array([x[0] for x in admissibles])
        fsr = np.array([x[1] for x in admissibles])

        # Compute the mathematical model for FOU(W~)
        umf = [0, 0, max(fsl), max(fsr)]
        lmf = [0, 0, min(fsl), min(fsr), 1]

        word_status["shape"] = "left-shoulder"

    elif (
        mean_right < 5.831 * mean_left - shift1
        and mean_right > 0.171 * mean_left + 8.29 - shift2
    ):
        # right shoulder embedded T1 FS
        et1fs_left = [
            0.5 * (x[0] + x[1]) - np.sqrt(6) * (x[1] - x[0]) / 3 for x in intervals
        ]
        et1fs_right = [
            0.5 * (x[0] + x[1]) + (x[1] - x[0]) / np.sqrt(6) for x in intervals
        ]

        # Delete inadmissible embedded T1 FSs
        admissibles = [
            (x, y)
            for (x, y) in zip(et1fs_left, et1fs_right)
            if x >= lower_bound and y <= upper_bound
        ]

        fsl = np.array([x[0] for x in admissibles])
        fsr = np.array([x[1] for x in admissibles])

        # Compute the mathematical model for FOU(W~)
        umf = [min(fsl), min(fsr), upper_bound, upper_bound]
        lmf = [max(fsl), max(fsr), upper_bound, upper_bound, 1]

        word_status["shape"] = "right-shoulder"

    else:
        # interior embedded T1 FS
        et1fs_left = [
            0.5 * (x[0] + x[1]) - np.sqrt(2) * (x[1] - x[0]) / 2 for x in intervals
        ]
        et1fs_right = [
            0.5 * (x[0] + x[1]) + np.sqrt(2) * (x[1] - x[0]) / 2 for x in intervals
        ]

        # Delete inadmissible embedded T1 FSs
        admissibles: list[tuple[float, float]] = [
            (x, y)
            for (x, y) in zip(et1fs_left, et1fs_right)
            if x >= lower_bound and y <= upper_bound
        ]

        fsl = np.array([x[0] for x in admissibles])
        fsr = np.array([x[1] for x in admissibles])
        fsc = np.array([(x[0] + x[1]) / 2 for x in admissibles])

        # Compute the mathematical model for FOU(W~)
        l1 = min(fsl)
        l2 = max(fsl)
        r1 = min(fsr)
        r2 = max(fsr)
        c1 = min(fsc)
        c2 = max(fsc)

        n = len(fsl)
        hs = np.zeros(n**2)

        for i in range(n):
            hs[i * n + np.arange(n)] = (fsr[i] - fsl) / (fsr[i] - fsl + fsc - fsc[i])

        h, index = np.min(hs), np.argmin(hs)
        i = index // n
        j = index % n
        p = fsl[j] + h * (fsc[j] - fsl[j])

        umf = [l1, c1, c2, r2]
        lmf = [l2, p, p, r1, h]

        word_status["shape"] = "interior"

    # collecting the final MF
    mf = [lmf, umf]
    word_status["MF"] = mf
    word_status["ET1FS"] = admissibles

    return word_status


def process_fuzzy_set_part():
    import json

    # Reading the preprocessed words dictionary from the json file
    with open("words.json") as file:
        words = json.load(file)
    words_status = {}

    for word, intervals in words.items():
        if intervals:
            words_status[word] = fuzzy_part(intervals)

    # Serializing words dictionary as a json file
    with open("words_status.json", "w") as file:
        json.dump(words_status, file)

    return words_status


def main():
    process_fuzzy_set_part()


if __name__ == "__main__":
    main()
