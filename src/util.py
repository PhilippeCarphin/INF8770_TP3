
ground_truth = {
    'cuts': [350, 599, 1482, 1702, 1796, 2015],
    'fades': [
        [199, 206],
        [316, 322],
        [401, 407],
        [504, 512],
        [1253, 1272],
        [1351, 1355]
    ]
}

def cross_check_with_ground_truth(cut_list, threshold=10):


    found_cuts = []
    unfound_cuts = []
    for true_cut in ground_truth['cuts']:
        for cut in cut_list:
            if -threshold <= cut - true_cut <= threshold:
                found_cuts.append({
                    'cut': cut,
                    'true_cut': true_cut,
                })
                break
        else:
            unfound_cuts.append(true_cut)

    found_fades = []
    unfound_fades = []
    for interval in ground_truth['fades']:
        for cut in cut_list:
            if interval[0] <= cut <= interval[1]:
                found_fades.append({
                    'cut': cut,
                    'fade_interval': interval
                })
                break
        else:
            unfound_fades.append(interval)

    return {
        'input_list': cut_list,
        'found_cuts': found_cuts,
        'found_fades': found_fades,
        'unfound_cuts': unfound_cuts,
        'unfound_fades': unfound_fades,
    }




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
