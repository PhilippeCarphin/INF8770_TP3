""" Scene detection on video sequence using different algorithms


"""
import sys
import cv2

import detectionalgo as algo


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

    print("video cuts detected at:")
    print(video.get_cuts())

    print("Using Algorithm fade_cuts")
    video.set_algo('fade_cuts')
    fade_cuts = video.get_cuts()
    ground_truth = [350, 599, 1482, 1702, 1796, 2015]
    print("Ground Truth : {}".format(ground_truth))
    print("fade_cuts : {}".format(fade_cuts))



if __name__ == "__main__":
    main()
