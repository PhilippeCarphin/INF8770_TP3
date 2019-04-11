from termcolor import colored, cprint


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


def verify_result(cut_list, threshold=2) -> None:
    print('\nCuts:')
    print('expected\treal\tResult')
    for expected in ground_truth['cuts']:
        match = None
        for i in range(expected - threshold, expected + threshold):
            if i in cut_list:
                match = i
                break
        print(str(expected).ljust(4) + '\t\t' +
              (str(match) if match else '\t') + '\t', end='')
        print(colored('Found', 'green') if match else
              colored("Not found at all", "red"))

    print('\nFades:')
    cprint('expected\t\treal\tResult', attrs=['bold'])
    for expected in ground_truth['fades']:
        match = None
        for i in range(expected[0] - threshold, expected[1] + threshold):
            if i in cut_list:
                match = i
                break
        print((str(expected[0]) + '-' + str(expected[1])).ljust(9) + '\t\t' +
              (str(match).rjust(4) if match else '\t') + '\t', end='')
        print(colored('Found', 'green') if match else
              colored("Not found at all", "red"))


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
    def in_found_cuts(cut):
        for fc in found_cuts:
            if fc['cut'] == cut:
                return True
        else:
            return False

    def in_found_intervals(cut):
        for interval in found_fades:
            if cut == interval['cut']:
                return True
        else:
            return False

    for cut in cut_list:
        if in_found_cuts(cut):
            real_positives.append(cut)
        elif in_found_intervals(cut):
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
