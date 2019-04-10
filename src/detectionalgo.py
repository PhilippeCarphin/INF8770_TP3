"""Scene detection algorithms

references:
https://bcastell.com/posts/scene-detection-tutorial-part-1/
"""
import cv2


def naive(cap, **kwargs) -> []:
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
    last_mean = 0
    while True:
        rv, im = cap.read()
        if not rv:
            break
        current_mean = im.mean()
        if ((current_mean >= threshold and last_mean < threshold)
                or (current_mean < threshold and last_mean >= threshold)):
            yield int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        last_mean = current_mean


def fade_cuts(cap: cv2.VideoCapture, **kwargs) -> []:
    """ Compute the times of cuts in the video using the tutorial
    https://bcastell.com/posts/scene-detection-tutorial-part-1/
    which is used to solve the problem of fade-cuts getting passed the naive
    algorithm.
    """

    threshold = kwargs.get('threshold', 100)
    # Doint it with a for-loop simply to get prints as it finds them, otherwise,
    # just replace with:
    # return list(fade_cut_generator(cap, threshold)

    cuts = []
    for cut in fade_cut_generator(cap, threshold):
        # print("cut found at {}".format(cut))
        cuts.append(cut)
    return cuts
