""" Scene detection on video sequence using different algorithms

references:
https://bcastell.com/posts/scene-detection-tutorial-part-1/

"""
import sys
import cv2

from matplotlib import pyplot as plt


class Video:
    def __init__(self, filename):
        self.cap = cv2.VideoCapture()
        self.cap.open(filename)
        if not self.cap.isOpened():
            raise ValueError(filename)

    def __del__(self):
        self.cap.release()

    def get_dimensions(self) -> {}:
        return {
            'height': self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT),
            'width':  self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        }

    def get_cuts(self, algo='naive') -> []:
        """Compute the time of the cuts in the video,
        :return a list of the frame numbers where cut occurs
        """
        means = []
        cuts = []
        while True:
            (rv, im) = self.cap.read()  # im is a valid image if and only if rv is true
            if not rv:
                break
            frame_mean = im.mean()
            threshold = 20
            if means and abs(frame_mean - means[-1]) > threshold:
                frame_no = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                cuts.append(frame_no)

            means.append(frame_mean)

        # frame_count = self.cap.get(cv2.CAP_PROP_POS_FRAMES)  # current capture position
        return cuts

        # print("Read %d frames from video." % frame_count)
        # print("cuts detected on the following frames: ")
        # print(cuts)
        #
        # plt.plot(means)
        # plt.title("Mean variation through the video")
        # plt.show()


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


if __name__ == "__main__":
    main()
