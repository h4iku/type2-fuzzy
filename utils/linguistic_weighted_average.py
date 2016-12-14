from utils.centroid_it2fs import ekm
import numpy as np

def fwa(x, w, n=2):
    """# Computing the FWA for trapezoidal T1 FSs described by five parameters (e,f,g,i,h)
    If the T1 FS has only four parameters, then its height is considered as 1
    
    x: T1 FSs for the subcriteria
    w: T1 FSs for the weights. It must have the same number of elements as X.
    n: number of alpha-cuts. The default value is 2.
    
    return values:
    the FWA approximated by 5 parameters.
    y- and mu-coordinates of the FWA.
    """
    
    # If the T1 FS has only four parameters, then its height is considered as 1
    for fs in x:
        if len(fs) == 4:
            fs.append(1)
            
    for fs in w:
        if len(fs) == 4:
            fs.append(1)
    
    # height of the FWA
    hmin = min([i[4] for i in x] + [i[4] for i in w])
    
    # mu-coordinates of the FWA
    mu = hmin * np.concatenate([np.arange(0, 1 + 0.01, 1 / (n - 1)), np.arange(1, 0 - 0.01, -1 / (n - 1))])
    
    y = [None] * (2 * n)
    
    for i in range(n):
        a = []
        b = []
        c = []
        d = []
        
        for j, _ in enumerate(x):  # for each input, compute the alpha-cut
            # a,b: alpha-cut on x
            a.append(x[j][0] + (x[j][1] - x[j][0]) * mu[i] / x[j][4])
            b.append(x[j][3] - (x[j][3] - x[j][2]) * mu[i] / x[j][4])
            
            # c,d: alpha-cut on w
            c.append(w[j][0] + (w[j][1] - w[j][0]) * mu[i] / w[j][4])
            d.append(w[j][3] - (w[j][3] - w[j][2]) * mu[i] / w[j][4])
            
        y[i] = ekm(a, c, d, -1)
        y[-(i + 1)] = ekm(b, c, d, 1)
        
    return [[y[0], y[n - 1], y[n], y[-1] , hmin], y, mu.tolist()]

        
def lwa(x, w, n=2):
    """Computing the LWA for IT2 FSs determined by the nine parameters
    
    x and w: MFs of the subcriteria and weights. They have the same number of rows.
    n: number of alpha-cuts. Default is 2.
    
    return values:
    Y: the LWA approximated by 9 parameters.
    UMFYy and UMFYmu: y- and mu-coordinates of the UMF of the LWA
    LMFYy and LMFYmu: y- and mu-coordinates of the LMF of the LWA
    """
    
    # If the IT2 FS has only eight parameters, then its height is considered as 1
    for fs in x:
        if len(fs) == 8:
            fs.append(1)
            
    for fs in w:
        if len(fs) == 8:
            fs.append(1)
    
    Y_upper, UMFYy, UMFYmu = fwa([i[:4] for i in x], [i[:4] for i in w], n)
    Y_lower, LMFYy, LMFYmu = fwa([i[4:] for i in x], [i[4:] for i in w], n)
    
    return [Y_upper[:4] + Y_lower, LMFYy, LMFYmu, UMFYy, UMFYmu]
            

# Testing these functions
def main():
    
    import pickle
    
    with open('words_status.pickle', 'rb') as file:
        words_status = pickle.load(file)
    
    keys = {key for key in words_status.keys() if words_status[key]['shape'] == 'right-shoulder'}
    for key in keys:
        a = lwa([words_status[key]['MF'][1] + words_status[key]['MF'][0]], [[0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1]])
        print(a)

if __name__ == '__main__':
    main()