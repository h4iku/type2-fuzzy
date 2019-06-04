import numpy as np
import itertools

def bad_data_check(interval):
    """Checking bad data intervals"""
    
    left = interval[0]
    right = interval[1]
    if 0 <= left < right <= 100 and (right - left) < 100:
        return True
    else:
        return False
    
def outlier_processing(intervals):
    """Outlier processing"""
    
    left = [x[0] for x in intervals]
    right = [x[1] for x in intervals]
    
    # Compute Q(0.25), Q(0.75) and IQR for left-ends
    lq25, lq75 = np.percentile(left, [25, 75])
    liqr = lq75 - lq25
    
    # Compute Q(0.25), Q(0.75) and IQR for right-ends
    rq25, rq75 = np.percentile(right, [25, 75])
    riqr = rq75 - rq25
    
    # Outlier processing for Left and Right bounds
    left_filtered = [x for x in intervals if (lq25 - 1.5 * liqr) <= x[0] <= (lq75 + 1.5 * liqr)]
    right_filtered = [x for x in left_filtered if (rq25 - 1.5 * riqr) <= x[1] <= (rq75 + 1.5 * riqr)]
    
    # Compute Q(0.25), Q(0.75) and IQR for interval length
    len_values = [x[1] - x[0] for x in right_filtered]
    lenq25, lenq75 = np.percentile(len_values, [25, 75])
    leniqr = lenq75 - lenq25
    
    # Outlier processing for interval length
    len_filtered = [x if (lenq25 - 1.5 * leniqr) <= x <= (lenq75 + 1.5 * leniqr) else None for x in len_values]
    selectors = [x is not None for x in len_filtered]
    filtered_intervals = list(itertools.compress(right_filtered, selectors))
    return filtered_intervals

def tolerance_limit_processing(intervals):
    """Tolerance limit processing"""
    
    left = [x[0] for x in intervals]
    right = [x[1] for x in intervals]
    mean_left = np.mean(left)
    std_left = np.std(left, ddof=1)
    mean_right = np.mean(right)
    std_right = np.std(right, ddof=1)
    
    limits = [32.019, 32.019, 8.380, 5.369, 4.275, 3.712, 3.369, 3.136, 2.967, 2.839,
        2.737, 2.655, 2.587, 2.529, 2.48, 2.437, 2.4, 2.366, 2.337, 2.31, 2.31, 2.31,
        2.31, 2.31, 2.208]
    k = limits[min(len(left) - 1, 24)]
    
    # Tolerance limit processing for Left and Right bounds
    left_filtered = [x for x in intervals if (mean_left - k * std_left) <= x[0] <= (mean_left + k * std_left)]
    right_filtered = [x for x in left_filtered if (mean_right - k * std_right) <= x[1] <= (mean_right + k * std_right)]
    
    # Tolerance limit processing for interval length
    len_values = [x[1] - x[0] for x in right_filtered]
    mean_len = np.mean(len_values)
    std_len = np.std(len_values, ddof=1)

    if std_len != 0:
        k = min(k, mean_len / std_len, (100 - mean_len) / std_len)
        
    len_filtered = [x if (mean_len - k * std_len) <= x <= (mean_len + k * std_len) else None for x in len_values]
    selectors = [x is not None for x in len_filtered]
    filtered_intervals = list(itertools.compress(right_filtered, selectors))
    return filtered_intervals

def reasonable_interval_processing(intervals):
    """Reasonable interval processing"""
    
    left = [x[0] for x in intervals]
    right = [x[1] for x in intervals]
    mean_left = np.mean(left)
    std_left = np.std(left, ddof=1)
    mean_right = np.mean(right)
    std_right = np.std(right, ddof=1)
    
    # Determining epsilon* 
    if std_left == std_right:
        epsilon_star = (mean_left + mean_right) / 2
    elif std_left == 0:
        epsilon_star = mean_left + 0.01
    elif std_right == 0:
        epsilon_star = mean_right - 0.01
    else:
        epsilon_1 = ((mean_right * std_left ** 2 - mean_left * std_right ** 2) + \
            std_left * std_right * np.sqrt((mean_left - mean_right) ** 2 + \
            2 * (std_left ** 2 - std_right ** 2) * np.log(std_left / std_right))) / \
            (std_left ** 2 - std_right ** 2)
            
        epsilon_2 = ((mean_right * std_left ** 2 - mean_left * std_right ** 2) - \
            std_left * std_right * np.sqrt((mean_left - mean_right) ** 2 + \
            2 * (std_left ** 2 - std_right ** 2) * np.log(std_left / std_right))) / \
            (std_left ** 2 - std_right ** 2)
            
        if mean_left <= epsilon_1 <= mean_right:
            epsilon_star = epsilon_1
        else:
            epsilon_star = epsilon_2
                    
    # Checking reasonable intervals
    reasonable_intervals = [x for x in intervals if 2 * mean_left - epsilon_star <= x[0] < epsilon_star < x[1] <= 2 * mean_right - epsilon_star]    
    return reasonable_intervals


def main():

    from openpyxl import load_workbook
    import pickle

    # Open Excel file and get the active sheet
    wb = load_workbook('sample-data.xlsx')
    ws = wb.active

    # A dictionary to keep the intervals of each word
    words = {word.value : zip([l.value for l in lower], [u.value for u in upper])
                for (word, *lower), (_, *upper) in zip(*[ws.columns]*2)}


    # Data Part
    for w, intervals in words.items():
        words[w] = [x for x in intervals if bad_data_check(x)]
    for w, intervals in words.items():    
        words[w] = outlier_processing(intervals)
    for w, intervals in words.items():    
        words[w] = tolerance_limit_processing(intervals)
    for w, intervals in words.items():    
        words[w] = reasonable_interval_processing(intervals)
    
    # Serializing words dictionary as a pickle file    
    with open('words.pickle', 'wb') as file:
        pickle.dump(words, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    
if __name__ == '__main__': main()
