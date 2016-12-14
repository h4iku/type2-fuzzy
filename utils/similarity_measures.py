from utils.centroid_it2fs import mg
import numpy as np

def jaccard(a, b):
    """computing the Jaccard similarity measure between two IT2 FSs.
    
    A, B: IT2 FSs each defined by nine parameters.
    """
    
    n = 200  # number of discretizations
    
    min_x = min(a[0], b[0])  # the range
    max_x = max(a[3], b[3]);
    x = list(np.linspace(min_x, max_x, num=n))
    
    lower_a = mg(x, a[4:8], [0, a[-1], a[-1], 0])
    upper_a = mg(x, a[:4])
    lower_b = mg(x, b[4:8], [0, b[-1], b[-1], 0])
    upper_b = mg(x, b[:4])
    
    s = sum(list(np.minimum(upper_a, upper_b)) + list(np.minimum(lower_a, lower_b))) / \
        sum(list(np.maximum(upper_a, upper_b)) + list(np.maximum(lower_a, lower_b)))
    return s
    

# Testing these functions
def main():
    
    import pickle
    
    with open('words_status.pickle', 'rb') as file:
        words_status = pickle.load(file)
    
    keys = [key for key in words_status.keys() if words_status[key]['shape'] == 'right-shoulder']
    a = jaccard(words_status[keys[0]]['MF'][1] + words_status[keys[0]]['MF'][0], words_status[keys[0]]['MF'][1] + words_status[keys[0]]['MF'][0])
    print(a)

if __name__ == '__main__':
    main()    