import sys
import cv2

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

    # Do stuff with cap here.

    cap.release()


if __name__ == "__main__":
    main()
