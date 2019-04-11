"""Scene detection algorithms

references:
https://bcastell.com/posts/scene-detection-tutorial-part-1/
"""
import cv2

import numpy as np


def naive(cap: cv2.VideoCapture, **kwargs) -> []:
    """Compute the time of the cuts in the video,
    :return a list of the frame numbers where cut occurs
    """
    means = []
    cuts = []
    while True:
        (rv, im) = cap.read()  # im is a valid image if and only if rv is true
        if not rv:
            break
        frame_mean = im.mean()
        threshold = 20
        if means and abs(frame_mean - means[-1]) > threshold:
            frame_no = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cuts.append(frame_no)

        means.append(frame_mean)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind video for further uses
    return cuts


def fade_cut_generator(cap: cv2.VideoCapture, threshold=100):
    means = []
    while True:
        rv, im = cap.read()
        if not rv:
            break
        current_mean = im.mean()

        if means and ((current_mean >= threshold and means[-1] < threshold)
                      or (current_mean < threshold and means[-1] >= threshold)):
            yield int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        means.append(current_mean)


def fade_cuts(cap: cv2.VideoCapture, **kwargs) -> []:
    """ Compute the times of cuts in the video using the tutorial
    https://bcastell.com/posts/scene-detection-tutorial-part-1/
    which is used to solve the problem of fade-cuts getting passed the naive
    algorithm.
    """

    threshold = kwargs.get('threshold', 100)
    # Doing it with a for-loop simply to get prints as it finds them, otherwise,
    # just replace with:
    # return list(fade_cut_generator(cap, threshold)

    cuts = []
    for cut in fade_cut_generator(cap, threshold):
        # print("cut found at {}".format(cut))
        cuts.append(cut)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind video for further uses
    return cuts


def hybrid(cap: cv2.VideoCapture, **kwargs) -> []:
    return sorted(naive(cap, **kwargs) + fade_cuts(cap, **kwargs))


def manhattan_distance(l1, l2):
    return sum([abs(l1[i] - l2[i]) for i in range(4)])


def multimean(im):
    w = im.shape[0]
    h = im.shape[1]
    top_left = im[:w // 2, :h // 2, :]
    top_right = im[w // 2:, :h // 2, :]
    bottom_left = im[:w // 2, h // 2:, :]
    bottom_right = im[w // 2:, h // 2:, :]
    return [
        top_left.mean(),
        top_right.mean(),
        bottom_left.mean(),
        bottom_right.mean(),
    ]


def multimean_cuts_generator(cap: cv2.VideoCapture, **kwargs) -> []:
    threshold = kwargs.get('threshold', 30)
    multimeans = []
    while True:
        rv, im = cap.read()
        if not rv:
            break

        current_multimean = multimean(im)

        if multimeans and abs(manhattan_distance(multimeans[-1],
                                                 current_multimean)) > threshold:
            yield int(cap.get(cv2.CAP_PROP_POS_FRAMES))

        multimeans.append(current_multimean)


def multimean_cuts(cap: cv2.VideoCapture, **kwargs) -> []:
    cuts = []
    for cut in multimean_cuts_generator(cap, **kwargs):
        cuts.append(cut)

    return cuts
