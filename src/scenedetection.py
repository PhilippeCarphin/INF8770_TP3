""" Scene detection on video sequence using different algorithms

references:
https://bcastell.com/posts/scene-detection-tutorial-part-1/

"""
import sys
import cv2

from matplotlib import pyplot as plt


def main():
    if len(sys.argv) < 2:
        print("Error - file name must be specified as first argument.")
        return

    cap = cv2.VideoCapture()
    cap.open(sys.argv[1])

    if not cap.isOpened():
        print("Fatal error - could not open video %s." % sys.argv[1])
        return
    else:
        print("Parsing video %s..." % sys.argv[1])

    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print("Video Resolution: %d x %d" % (width, height))

    means = []
    cuts = []
    while True:
        (rv, im) = cap.read()   # im is a valid image if and only if rv is true
        if not rv:
            break
        frame_mean = im.mean()
        threshold = 20
        if means and abs(frame_mean - means[-1]) > threshold:
            frame_no = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
            cuts.append(frame_no)

        means.append(frame_mean)

    frame_count = cap.get(cv2.CAP_PROP_POS_FRAMES)  # current capture position
    print("Read %d frames from video." % frame_count)
    print("cuts detected on the following frames: ")
    print(cuts)

    plt.plot(means)
    plt.title("Mean variation through the video")
    plt.show()

    cap.release()

if __name__ == "__main__":
    main()
