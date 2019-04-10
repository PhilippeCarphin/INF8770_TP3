
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

def cross_check_with_ground_truth(cut_list, threshold=2):

    # TODO Add reporting of false positives:
    #  I.E. Elements in cut_list that do not correspond to an
    #  actual scene change
    #  Maybe if something is good, remove it  from cut_list (or temp working list)
    #  and return what is left of that as BS list elements.

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

    false_positives = []
    real_positives = []
    for cut in cut_list:
        if cut in found_cuts:
            real_positives.append(cut)

        else:
            for interval in found_fades:
                if cut == interval['cut']:
                    real_positives.append(cut)
            else:
                false_positives.append(cut)

    return {
        'found_cuts': found_cuts,
        'found_fades': found_fades,
        'unfound_cuts': unfound_cuts,
        'unfound_fades': unfound_fades,
        'false_positives': false_positives,
        'real_positives': real_positives,
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
