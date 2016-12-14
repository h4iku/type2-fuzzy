from utils.centroid_it2fs import centroid_it2
import numpy as np

def centroid_rank(mfs):
    """Implement the center-of-centroid based ranking method
    
    mfs: a list of lists containing 9 parameters of the IT2 FSs
    """
    
    cc = []  # a list for center-of-centroids of IT2 FSs
    
    for it2fs in mfs:
        cc.append(centroid_it2(it2fs)[-1])
        
    return np.argsort(cc)
    

def main():
    
    import pickle
    
    with open('words_status.pickle', 'rb') as file:
        words_status = pickle.load(file)
    
    keys = [key for key in words_status.keys() if words_status[key]['shape'] == 'right-shoulder']
    a = centroid_rank([words_status[keys[0]]['MF']
                       , words_status[keys[1]]['MF']
                       , words_status[keys[2]]['MF']
                       , words_status[keys[3]]['MF']])
    print(a)
    
if __name__ == '__main__':
    main()    