def approximately_in(x, int_list, threshold):
    for y in int_list:
        if -threshold <= x - y <= threshold:
            return True
    else:
        return False

def approximate_intersection(l1, l2, threshold):
    inter = []
    for x in l1:
        if approximately_in(x, l2, threshold):
            inter.append(x)
    return inter
