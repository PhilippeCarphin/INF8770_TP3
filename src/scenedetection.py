""" Scene detection on video sequence using different algorithms


"""
import sys
import cv2
from pprint import pprint

import detectionalgo as algo
import util


class Video:
    def __init__(self, filename):
        self.cap = cv2.VideoCapture()
        self.cap.open(filename)
        if not self.cap.isOpened():
            raise ValueError(filename)
        self.detection_algo = getattr(algo, 'naive')

    def __del__(self):
        self.cap.release()

    def get_dimensions(self) -> {}:
        return {
            'height': self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            'width': self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        }

    def set_algo(self, algo_name):
        try:
            self.detection_algo = getattr(algo, algo_name)
        except:
            sys.exit('algorithm not found')

    def get_cuts(self, **kwargs) -> []:
        """Compute the time of the cuts in the video,
        :return a list of the frame numbers where cut occurs
        """
        cuts = self.detection_algo(self.cap, **kwargs)
        return cuts


def main():
    if len(sys.argv) < 2:
        print("Error - file name must be specified as first argument.")
        return

    filename = sys.argv[1]
    try:
        video = Video(filename)
    except ValueError:
        print("Could not open {}", filename)
        return

    naive_cuts = video.get_cuts()
    print("video cuts detected at: {}".format(naive_cuts))

    print("cross_check_with_ground_truth(naive_cuts :")
    pprint(util.cross_check_with_ground_truth(naive_cuts, 10))


    print("Using Algorithm fade_cuts")
    video.set_algo('fade_cuts')
    threshold = 100
    fade_cuts = video.get_cuts(threshold=threshold)

    print("cross_check_with_ground_truth :")
    pprint(util.cross_check_with_ground_truth(fade_cuts, 10))

if __name__ == "__main__":
    main()
