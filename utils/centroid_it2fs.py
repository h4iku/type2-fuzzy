import numpy as np
import itertools

def mg(x, xmf, umf=[0, 1, 1, 0]):
    """Function to compute the membership grades of each x on a T1 FS
    
    x: list of x values
    xmf: x parameters of the membership function
    umf: u parameters of the membership function
    """
    
    items = [item for item in sorted(zip(xmf, umf))]
    xmf = [i[0] for i in items]
    umf = [i[1] for i in items]

    u = [None] * len(x)  # membership grade of x
    for i, p in enumerate(x):
        if p <= xmf[0] or p >= xmf[-1]:
            u[i] = 0
        else:
            x_mf = np.array(xmf)
            left = np.nonzero(x_mf < p)[0][-1]
            right = left + 1
            u[i] = umf[left] + (umf[right] - umf[left]) * (p - xmf[left]) / (xmf[right] - xmf[left])
        
    return u
   

def ekm(x_point, w_lower, w_upper, max_flag):
    """Implementation of the Enhanced KM algorithm
    w_lower: lower membership values for each x
    w_upper: upper membership values for each x
    max_flag: 1 to output the maximum; -1 to output the minimum
    """
    
    if max(w_upper) == 0 or max(x_point) == 0:
        return 0
    
    if max(w_lower) == 0:
        if max_flag > 0:
            return max(x_point)
        else:
            return min(x_point)
        
    if len(x_point) == 1:
        return x_point[0]
    
    
    # removing items with 0 upper value
    zero_filtered = [x if x != 0 else None for x in w_upper]
    selectors = [x is not None for x in zero_filtered]
    x_point = list(itertools.compress(x_point, selectors))
    w_lower = list(itertools.compress(w_lower, selectors))
    w_upper = list(itertools.compress(w_upper, selectors))
    
    
    # combine zero Xs
    items = [item for item in sorted(zip(x_point, w_lower, w_upper))]
    x_point = [x[0] for x in items]
    
    if 0 in x_point and (len(x_point) - x_point.index(0) - 1) > 0:
        lower_sum = sum([x[1] for x in items if x[0] == 0])
        upper_sum = sum([x[2] for x in items if x[0] == 0])
        items = [x for x in items if x[0] != 0]
        items.insert(0, (0, lower_sum, upper_sum))
    
    # Starting the KM algorithm
    x_point = [x[0] for x in items]
    w_lower = [x[1] for x in items]
    w_upper = [x[2] for x in items]
    
    ly = len(x_point)
    if max_flag < 0:
        k = int(ly // 2.4)
        temp = w_upper[:k + 1] + w_lower[k + 1:]
    else:
        k = int(ly // 1.7)
        temp = w_lower[:k + 1] + w_upper[k + 1:]
       
    a = sum(np.array(x_point) * temp)
    b = sum(temp)
    y = a / b
    # rounded_xpoints = [round(x, 9) for x in x_point]
    k_new = np.nonzero(np.array(x_point) > y)[0] - 1
    
    if k_new.size != 0:
        k_new = k_new[0]
        
    while k != k_new:
        mink = min(k, k_new)
        maxk = max(k, k_new)
        temp = np.array(w_upper[mink + 1:maxk + 1]) - w_lower[mink + 1:maxk + 1]
        b = b - np.sign(k_new - k) * np.sign(max_flag) * sum(temp)
        a = a - np.sign(k_new - k) * np.sign(max_flag) * sum(temp * x_point[mink + 1:maxk + 1])
        y = a / b
        k = k_new
        k_new = np.nonzero(np.array(x_point) > y)[0] - 1
        if k_new.size != 0:
            k_new = k_new[0]
            
    return y
       
          
def centroid_it2(it2fs): 
    """To compute the centroid of an IT2 FS
    which is defined by nine parameters ([e, f, g, i, h], [a, b, c, d])     
    """
    
    lower = it2fs[0]
    upper = it2fs[1]
    xs = list(np.linspace(upper[0], upper[3], num=100))
    lmf = mg(xs, lower[:-1], [0, lower[-1], lower[-1], 0])
    umf = mg(xs, upper, [0, 1, 1, 0])
    ca_left = ekm(xs, lmf, umf, -1)
    ca_right = ekm(xs, lmf, umf, 1)
    ca = (ca_left + ca_right) / 2
    return [ca_left, ca_right, ca]
     

# Testing these functions
def main():
    
    import pickle
    
    with open('words_status.pickle', 'rb') as file:
        words_status = pickle.load(file)
    
    keys = {key for key in words_status.keys() if words_status[key]['shape'] == 'right-shoulder'}
    for key in keys:
        print(centroid_it2(words_status[key]['MF']))


if __name__ == '__main__':
    main()           